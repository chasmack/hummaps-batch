import psycopg2
import os

from const import *


def update_pdf(pdf_list, update_db=False):

    # S3 PDF files indexed by map name
    s3_pdffile = {}
    with open(pdf_list) as f:
        for line in f:
            pdffile = '/' + line.split()[3]
            mapname = os.path.basename(pdffile)[0:8]
            s3_pdffile[mapname] = pdffile

    with psycopg2.connect(DSN_PROD) as con, con.cursor() as cur:

        # Get a list of the maptypes
        cur.execute("""
            SELECT t.abbrev FROM {table_maptype} t ORDER BY t.abbrev;
        """.format(table_maptype=TABLE_PROD_MAPTYPE))
        maptypes = list(cur)

        pdf_insert = []
        for maptype in maptypes:
            cur.execute("""
                SELECT m.id map_id,
                    lpad(m.book::text, 3, '0') || lower(t.abbrev) || lpad(m.page::text, 3, '0') mapname, pdf.pdffile
                FROM {table_map} m
                JOIN {table_maptype} t ON t.id = m.maptype_id
                LEFT JOIN {table_pdf} pdf ON pdf.map_id = m.id
                WHERE t.abbrev = %(maptype)s
                ORDER BY m.book, m.page
                ;
            """.format(
                table_map=TABLE_PROD_MAP,
                table_maptype=TABLE_PROD_MAPTYPE,
                table_pdf=TABLE_PROD_PDF
            ), {'maptype': maptype})

            for map_id, mapname, db_pdffile in cur:

                db = db_pdffile
                s3 = s3_pdffile.get(mapname)
                if db and not s3:
                    print('Missing s3 pdf: %s' % db)
                elif s3 and not db:
                    print('Missing pdf record: %s' % s3)
                    pdf_insert.append((map_id, s3))
                elif s3 != db:
                    print('Bad pdf record: db: %s  s3: %s' % (db, s3))

        if update_db and pdf_insert:
            cur.executemany("""
                INSERT INTO {table_pdf} (map_id, pdffile) VALUES (%s, %s);
            """.format(table_pdf=TABLE_PROD_PDF), pdf_insert)
            con.commit()

            print('INSERT pdf: %d row%s' % (cur.rowcount, '' if cur.rowcount == 1 else 's'))


if __name__ == '__main__':

    pdf_list = 'maps/190321_pdf.txt'

    update_pdf(pdf_list, update_db=True)
