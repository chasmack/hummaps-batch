import psycopg2
from openpyxl import load_workbook
from dateutil.parser import parse
import datetime
from trs_path import expand_paths, abbrev_paths, trs_path_sortkey
import re

from const import *


def check_update(update_xl=False):

    validate_error = False

    # Get the Excel update
    wb = load_workbook(XLSX_DATA_MAP)

    # Get a list of surveyor fullnames
    surveyor_fullnames = []
    ws = wb['surveyor']
    xl_cols = list(c.value for c in ws[1])
    for xl_row in ws.iter_rows(min_row=2):
        xl_rec = dict(zip((k.lower() for k in xl_cols), (c.value for c in xl_row)))
        surveyor_fullnames.append(xl_rec['fullname'])

    # Get the parcel map numbers indexed by book-page
    pm_number = {}
    ws = wb['pm_number']
    xl_cols = list(c.value for c in ws[1])
    for xl_row in ws.iter_rows(min_row=2):
        xl_rec = dict(zip((k.lower() for k in xl_cols), (c.value for c in xl_row)))
        book_page = '%s-%s' % (xl_rec['book'], xl_rec['page'])
        pm_number[book_page] = xl_rec['pm_number']

    # Get the subdivision tract numbers indexed by book-page
    tract_number = {}
    ws = wb['tract_number']
    xl_cols = list(c.value for c in ws[1])
    for xl_row in ws.iter_rows(min_row=2):
        xl_rec = dict(zip((k.lower() for k in xl_cols), (c.value for c in xl_row)))
        book_page = '%s-%s' % (xl_rec['book'], xl_rec['page'])
        tract_number[book_page] = xl_rec['tract_number']

    # Get the map update
    ws = wb['update']
    xl_cols = list(c.value for c in ws[1])

    map_ids = set()
    for xl_row in ws.iter_rows(min_row=2):

        xl_cell = dict(zip((k.lower() for k in xl_cols), xl_row))
        xl_rec = dict(zip((k.lower() for k in xl_cols), (c.value for c in xl_row)))
        xl_row_number = xl_row[0].row

        if all(c.value is None for c in xl_row):
            continue

        # Validate map id
        map_id = xl_rec['map_id']
        if map_id is None:
            print('ERROR [%d]: No map id' % xl_row_number)
            validate_error = True
            break
        if map_id in map_ids:
            print('ERROR [%d]: Duplicate map ids' % xl_row_number)
            validate_error = True
            break
        map_ids.add(map_id)

        # Validate maptype/book/page
        if any(xl_rec[col] is None for col in ('maptype', 'book', 'page')):
            print('ERROR [%d]: Missing maptype/book/page' % (xl_row_number))
            validate_error = True
            break

        # Validate any trs path spec
        if xl_rec['trs_paths']:
            try:
                expand_paths(re.split(';?\s+', xl_rec['trs_paths']))
            except ValueError as err:
                print('ERROR [%d]: %s' % (xl_row_number, err))
                validate_error = True
                break

        # Validate recdate
        if xl_rec['recdate']:
            try:
                parse(xl_rec['recdate'])
            except Exception as err:
                print('ERROR [%d]: Bad recdate: %s' % (xl_row_number, err))
                validate_error = True
                break

        # Validate surveyors
        if xl_rec['surveyors']:
            surveyors = sorted(re.split('\s*,\s*', xl_rec['surveyors']))
            for i in range(len(surveyors)):
                if surveyors[i] not in surveyor_fullnames:
                    print('ERROR [%d]: Bad surveyor fullname: %s' % (xl_row_number, surveyors[i]))
                    validate_error = True
            if validate_error:
                break

        # Check for parcel map/tract numbers
        if xl_rec['client']:
            book_page = '{}-{}'.format(xl_rec['book'], xl_rec['page'])
            if xl_rec['maptype'] == 'Parcel Map' and book_page not in pm_number:
                print('WARNING [{}]: No PM number found: {} {}s {}'.format(
                    xl_row_number, xl_rec['book'], xl_rec['maptype'], xl_rec['page']
                ))
            elif xl_rec['maptype'] == 'Record Map' and book_page not in tract_number:
                print('WARNING [{}]: No tract number found: {} {}s {}'.format(
                    xl_row_number, xl_rec['book'], xl_rec['maptype'], xl_rec['page']
                ))

    if update_xl and not validate_error:
        wb.save(filename=XLSX_DATA_MAP)
    wb.close()


if __name__ == '__main__':

    check_update(update_xl=False)
