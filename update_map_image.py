import psycopg2
import os

from const import *


def update_map_image(map_list, update_db=False):

    # S3 image files indexed by map name
    s3_imagefiles = {}
    with open(map_list) as f:
        for line in f:
            imagefile = '/' + line.split()[3]
            if '/cc/' in imagefile:
                continue
            mapname = os.path.basename(imagefile)[0:8]
            s3_imagefiles.setdefault(mapname, set()).add(imagefile)

    with psycopg2.connect(DSN_PROD) as con, con.cursor() as cur:

        # Get a list of the maptypes
        cur.execute('SELECT array_agg(t.abbrev) maptypes FROM {table_maptype} t;'
                    .format(table_maptype=TABLE_PROD_MAPTYPE))
        maptypes = cur.fetchone()[0]

        map_image_insert = []
        for maptype in maptypes:
            cur.execute("""
                SELECT m.id map_id,
                    lpad(m.book::text, 3, '0') || lower(t.abbrev) || lpad(m.page::text, 3, '0') mapname,
                    array_remove(array_agg(mi.imagefile), NULL) imagefiles
                FROM {table_map} m
                JOIN {table_maptype} t ON t.id = m.maptype_id
                LEFT JOIN {table_map_image} mi ON mi.map_id = m.id
                WHERE t.abbrev = %(maptype)s
                GROUP BY m.id, t.id
                ORDER BY m.book, m.page
            """.format(
                table_map=TABLE_PROD_MAP,
                table_maptype=TABLE_PROD_MAPTYPE,
                table_map_image=TABLE_PROD_MAP_IMAGE
            ), {'maptype': maptype})

            for map_id, mapname, db_imagefiles in cur:

                db = set(db_imagefiles)
                s3 = s3_imagefiles.get(mapname, set())
                if s3 < db:
                    print('Missing s3 image: %s' % ', '.join(sorted(db - s3)))
                elif s3 > db:
                    print('Missing image record: %s' % ', '.join(sorted(s3 - db)))
                    page = 1
                    for imagefile in sorted(s3 - db):
                        map_image_insert.append((map_id, page, imagefile))
                        page += 1
                elif s3 != db:
                    print('Bad image record: db: %s s3: %s' % (', '.join(sorted(db)), ', '.join(sorted(s3))))

        if update_db and map_image_insert:
            cur.executemany("""
                INSERT INTO {table_map_image} (map_id, page, imagefile) VALUES (%s, %s, %s);
            """.format(table_map_image=TABLE_PROD_MAP_IMAGE), map_image_insert)
            con.commit()

            print('INSERT map_image: %d row%s' % (cur.rowcount, '' if cur.rowcount == 1 else 's'))


if __name__ == '__main__':

    map_list = 'maps/190321_map.txt'

    update_map_image(map_list, update_db=True)
