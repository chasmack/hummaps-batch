from datetime import datetime
import re
import time
import requests
from lxml import html
import os

MAP_LIST = '190321_map.txt'
PDF_LIST = '190321_pdf.txt'

MAPS_ROOT = 'C:/Temp/hummaps/maps.hummaps.org/'
MAPS_SEARCH = {
    'cr': [13,14],
    'pm': [35,36],
    'rm': [24,25],
    'rs': [72,73],
    'ur': [3,4,5,6]
}

URL_BASE = 'https://hummaps.com/'

def sync_maps():

    map_paths = []
    with open(MAP_LIST) as f:
        for line in f:
            map_paths.append(line.split()[3])

    pdf_paths = []
    with open(PDF_LIST) as f:
        for line in f:
            pdf_paths.append(line.split()[3])

    for maptype in MAPS_SEARCH.keys():
        for book in MAPS_SEARCH[maptype]:
            params = {maptype: 'y', 'b': book, 'page': 1}
            while True:
                r = requests.get(URL_BASE + 'maps', params=params)
                if r.status_code != 200:
                    break

                # print(r.url)
                doc = html.fromstring(r.content)
                for map_record in doc.find_class('hmps-map'):

                    bookpage = map_record.find('./div/h4').text
                    m = re.match('(\d+)\D*(\d+)?', bookpage)
                    if not m:
                        print('Bad book/page: %s' % bookpage)
                        continue
                    book, page = map(int, m.groups())
                    map_root = 'map/{maptype}/{book:03d}/{book:03d}{maptype}{page:03d}'.format(
                        book=book, maptype=maptype, page=page
                    )

                    sheet = 1
                    while True:
                        map_image = '{root}-{sheet:03d}.jpg'.format(root=map_root, sheet=sheet)
                        if map_image not in map_paths:
                            r = requests.get(URL_BASE + map_image)
                            if r.status_code != 200:
                                break
                            print('Download: %s' % map_image)
                            imagefile = os.path.join(MAPS_ROOT, map_image)
                            os.makedirs(os.path.dirname(imagefile), exist_ok=True)
                            with open(imagefile, 'wb') as i:
                                i.write(r.content)
                        sheet += 1

                    pdf_file = 'pdf/{maptype}/{book:03d}/{book:03d}{maptype}{page:03d}.pdf'.format(
                        book=book, maptype=maptype, page=page
                    )
                    if pdf_file not in pdf_paths:
                        r = requests.get(URL_BASE + pdf_file)
                        if r.status_code != 200:
                            print('Error %d reading pdf: %s' % (r.status_code, pdf_file))
                        else:
                            print('Download: %s' % pdf_file)
                            pdf_file = os.path.join(MAPS_ROOT, pdf_file)
                            os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
                            with open(pdf_file, 'wb') as i:
                                i.write(r.content)

                params['page'] += 1


if __name__ == '__main__':

    sync_maps()
