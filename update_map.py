import psycopg2
import requests
from openpyxl import load_workbook
from dateutil.parser import parse
import datetime
from trs_path import expand_paths, abbrev_paths, trs_path_sortkey
import re

from const import *

def check_maps():

    with psycopg2.connect(DSN_PROD) as con, con.cursor() as cur:

        # Get the maptypes
        cur.execute('SELECT t.maptype FROM {table_maptype} t;'
        .format(table_maptype=TABLE_PROD_MAPTYPE))
        maptypes = list(v[0] for v in cur)

        # Get the surveyors and hollins aliases
        surveyors = []
        hollins_surveyor = {}
        wb = load_workbook(XLSX_DATA_SURVEYOR, read_only=True)
        xl = wb.active
        ws_cols = list(c.value for c in xl[1])
        for ws_row in xl.iter_rows(min_row=2):
            xl = dict(zip((v.lower() for v in ws_cols), (v.value for v in ws_row)))
            surveyors.append(xl['fullname'])
            hollins_surveyor[xl['hollins_fullname']] = xl['fullname']
        wb.close()

        # Get the parcel map numbers indexed by book/page
        pm_number = {}
        wb = load_workbook(XLSX_DATA_PM, read_only=True)
        xl = wb.active
        ws_cols = list(c.value for c in xl[1])
        for ws_row in xl.iter_rows(min_row=2):
            xl = dict(zip((v.lower() for v in ws_cols), (v.value for v in ws_row)))
            book_page = '{1} {0} {2}'.format(xl['maptype'], xl['book'], xl['page'])
            pm_number[book_page] = '(PM%s)' % xl['pm_number']
        wb.close()

        # Get the subdivision tract numbers indexed by book/page
        tract_number = {}
        wb = load_workbook(XLSX_DATA_TRACT, read_only=True)
        xl = wb.active
        ws_cols = list(c.value for c in xl[1])
        for ws_row in xl.iter_rows(min_row=2):
            xl = dict(zip((v.lower() for v in ws_cols), (v.value for v in ws_row)))
            book_page = '{1} {0} {2}'.format(xl['maptype'], xl['book'], xl['page'])
            tract_number[book_page] = '(TR%s)' % xl['tract_number']
        wb.close

        # Get the Excel map data
        wb = load_workbook(XLSX_DATA_MAP)
        xl = wb.active
        ws_cols = list(c.value for c in xl[1])

        sql = """
            WITH q1 AS (
                SELECT m.id map_id
                FROM {table_map} m
                JOIN {table_maptype} t ON t.id = m.maptype_id
                WHERE t.maptype = %s AND m.book = %s AND m.page = %s
            ), q2 AS (
                SELECT q1.map_id, array_remove(array_agg(p.trs_path::text), NULL) trs_paths
                FROM q1
                LEFT JOIN {table_trs_path} p USING (map_id)
                GROUP BY q1.map_id
            ), q3 AS (
                SELECT q1.map_id, array_remove(array_agg(s.fullname), NULL) surveyors
                FROM q1
                LEFT JOIN {table_signed_by} sb USING (map_id)
                LEFT JOIN {table_surveyor} s ON s.id = sb.surveyor_id
                GROUP BY q1.map_id
            )
            SELECT q1.map_id,
                m.npages, m.recdate, m.client, m.description, m.note,
                q2.trs_paths, q3.surveyors
            FROM {table_map} m
            JOIN q1 ON q1.map_id = m.id
            LEFT JOIN q2 ON q2.map_id = m.id
            LEFT JOIN q3 ON q3.map_id = m.id
            ;
        """.format(
            table_map=TABLE_PROD_MAP,
            table_maptype=TABLE_PROD_MAPTYPE,
            table_trs_path=TABLE_PROD_TRS_PATH,
            table_signed_by=TABLE_PROD_SIGNED_BY,
            table_surveyor=TABLE_PROD_SURVEYOR
        )

        for ws_row in xl.iter_rows(min_row=2):
            xl = dict(zip((v.lower() for v in ws_cols), (v.value for v in ws_row)))
            xl_cell = dict(zip((v.lower() for v in ws_cols), ws_row))

            if any(v is None for v in (xl['maptype'], xl['book'], xl['page'])):
                if all(c.value is None for c in ws_row):
                    continue    # Blank lines are permitted
                print('ERROR: Missing maptype/book/page: row=%d' % (ws_row[0].row))
                exit(-1)

            # Validate maptype/book/page
            if xl['maptype'] not in maptypes:
                print('ERROR: Bad maptype: row=%d, maptype=%s' % (ws_row[0].row, str(xl['maptype'])))
                exit(-1)
            xl_maptype = xl['maptype']
            if type(xl['book']) is int:
                xl_book = xl['book']
            else:
                try:
                    xl_cell['book'].value = xl_book = int(xl['book'])
                except ValueError as err:
                    print('ERROR: Bad book number: row=%d, book=%s' % (ws_row[0].row, str(xl['book'])))
                    exit(-1)
            if type(xl['page']) is int:
                xl_page = xl['page']
            else:
                try:
                    xl_cell['page'].value = xl_page = int(xl['page'])
                except ValueError as err:
                    print('ERROR: Bad page number: row=%d, page=%s' % (ws_row[0].row, str(xl['page'])))
                    exit(-1)
            book_page = '%d %s %d' % (xl_book, xl_maptype, xl_page)

            # Validate any trs path spec
            try:
                xl_paths = expand_paths(xl['trs_paths']) if xl['trs_paths'] else []
            except ValueError as err:
                print('ERROR: %s: %s' % (book_page, err))
                exit(-1)

            # Validate recdate

            if xl['recdate'] is None:
                xl_recdate = None
            elif type(xl['recdate']) is datetime.datetime:
                xl_recdate = xl['recdate'].date()
            else:
                try:
                    xl_cell['recdate'].value  = xl_recdate = parse(xl['recdate']).date()
                except Exception as err:
                    print('ERROR: %s: Bad recdate: %s' % (book_page, err))
                    exit(-1)

            # Validate surveyors
            xl_surveyors = sorted(re.split('\s*,\s*', xl['surveyors'])) if xl['surveyors'] else []
            for i in range(len(xl_surveyors)):
                if xl_surveyors[i] in hollins_surveyor:
                    # replace hollins fullanme with hummaps fullname
                    xl_surveyors[i] = hollins_surveyor[xl_surveyors[i]]
                    xl_cell['surveyors'].value = ', '.join(xl_surveyors)
                elif xl_surveyors[i] not in surveyors:
                    print('ERROR: %s: Missing surveyor: %s' % (book_page, xl_surveyors[i]))
                    exit(-1)

            # Need to add parcel map/tract numbers to client records
            xl_client = xl['client']
            if xl['maptype'] == 'Parcel Map':
                if book_page in pm_number:
                    xl_client += ' ' + pm_number[book_page]
                else:
                    print('WARNING: %s: No PM number found.' % book_page)
            elif xl['maptype'] == 'Record Map':
                if book_page in tract_number:
                    xl_client += ' ' + tract_number[book_page]
                else:
                    print('WARNING: %s: No Tract number found.' % book_page)

            # Fetch the database record
            cur.execute(sql, (xl['maptype'], xl['book'], xl['page']))

            if cur.rowcount == 0:
                print('%s: No database record.' % book_page)
                continue
            if cur.rowcount > 1:
                print('ERROR: %s: Multiple database records.' % book_page)
                exit(-1)
            db = dict(zip((v.name for v in cur.description), cur.fetchone()))

            # Compare worksheet and database data
            db_paths = sorted(db['trs_paths'], key=trs_path_sortkey)
            if xl_paths != db_paths:
                xl_paths = '; '.join(abbrev_paths(xl_paths)) if xl_paths else None
                db_paths = '; '.join(abbrev_paths(db_paths)) if db_paths else None
                print('%s: Compare trs_paths: xl=%s db=%s' % (book_page, xl_paths, db_paths))

            db_surveyors = sorted(db['surveyors'])
            if xl_surveyors != db_surveyors:
                print('%s: Compare surveyors: xl=%s db=%s' % (book_page, xl_surveyors, db_surveyors))

            db_recdate = db['recdate']
            if xl_recdate != db_recdate:
                print('%s: Compare recdate: xl=%s db=%s' % (book_page, xl_recdate, db_recdate))

            db_client = db['client']
            if xl_client != db_client:
                print('%s: Compare client: xl=%s db=%s' % (book_page, xl_client, db_client))

            for c in ('map_id', 'npages', 'description', 'note'):
                if xl[c] != db[c]:
                    print('%s: Compare %s: xl=%s db=%s' % (book_page, c, str(xl[c]), str(db[c])))

    # wb.save(filename=XLSX_DATA_MAP)
    wb.close()


def update_maps():

    wb = load_workbook(XLSX_DATA_MAP)
    ws = wb['Maps']

    ws_cols = list(c.value for c in ws[1])

    with psycopg2.connect(DSN_PROD) as con, con.cursor() as cur:

        missing_map_images = []
        missing_pdfs = []

        for cell in (dict(zip(ws_cols, row)) for row in ws.iter_rows(min_row=2)):

            cur.execute("""
                SELECT m.id, t.maptype, lower(t.abbrev) abbrev, m.book, m.page,
                  count(distinct i.id) map_images, count(distinct pdf.id) pdfs
                FROM {table_map} m
                JOIN {table_maptype} t ON t.id = m.maptype_id
                LEFT JOIN {table_map_image} i ON i.map_id = m.id
                LEFT JOIN {table_pdf} pdf ON pdf.map_id = m.id
                WHERE t.maptype = %s AND m.book = %s AND m.page = %s
                GROUP BY m.id, t.maptype, t.abbrev, m.book, m.page
                ;
            """.format(
                table_map=TABLE_PROD_MAP,
                table_maptype=TABLE_PROD_MAPTYPE,
                table_map_image=TABLE_PROD_MAP_IMAGE,
                table_pdf=TABLE_PROD_PDF,
            ), (cell['MAPTYPE'].value, cell['BOOK'].value, cell['PAGE'].value))

            for row in cur:
                map_id = row[0]
                abbrev, book, page = row[2:5]
                map_images, pdfs = row[5:7]

                cell['MAP_ID'].value = map_id

                url_base = 'https://hummaps.com'
                map_name = '%03d%s%03d' % (book, abbrev, page)
                image_base = '/map/%s/%03d/%s' % (abbrev, book, map_name)
                imagefiles = []
                while True:
                    f = image_base + '-%03d.jpg' % (len(imagefiles) + 1)
                    r = requests.head(url_base + f)
                    if r.status_code == 200:
                        imagefiles.append(f)
                        print('%s: %d' % (f, r.status_code))
                    else:
                        break

                if map_images > 0 and map_images != len(imagefiles):
                    print('WARNING: %s: image_pages=%d imagefiles=%d' % (map_name, map_images, len(imagefiles)))
                else:
                    cell['MAP_IMAGES'].value = len(imagefiles)
                if map_images == 0:
                    for i in range(len(imagefiles)):
                        missing_map_images.append((map_id, i + 1, imagefiles[i]))

                pdffile = '/pdf/%s/%03d/%s.pdf' % (abbrev, book, map_name)
                r = requests.head(url_base + pdffile)
                if r.status_code == 200:
                    cell['PDFS'].value = 1
                    print('%s: %d' % (pdffile, r.status_code))
                    if pdfs == 0:
                        missing_pdfs.append((map_id, pdffile))

        cur.executemany("""
            INSERT INTO {table_map_image} (map_id, page, imagefile)
            VALUES (%s, %s, %s);
        """.format(
            table_map_image=TABLE_PROD_MAP_IMAGE,
        ), missing_map_images)
        con.commit()

        print('INSERT map_image: %d rows effected' % cur.rowcount)

        cur.executemany("""
            INSERT INTO {table_pdf} (map_id, pdffile)
            VALUES (%s, %s);
        """.format(
            table_pdf=TABLE_PROD_PDF,
        ), missing_pdfs)
        con.commit()

        print('INSERT pdf: %d rows effected' % cur.rowcount)

        wb.save(filename=XLSX_DATA_MAP)


if __name__ == '__main__':

    check_maps()
