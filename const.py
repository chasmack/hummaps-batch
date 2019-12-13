
# const.py - common constants

UPDATE_ID = 66
UPDATE_DIR = 'data/update%d' % UPDATE_ID

IMAGE_DIR = r'C:\Temp\hummaps\update%d' % UPDATE_ID
IMAGE_FILES_DIR = IMAGE_DIR + r'\files'
IMAGE_SCAN_DIR = IMAGE_DIR + r'\scan'
IMAGE_MAP_DIR = IMAGE_DIR + r'\map'
IMAGE_PDF_DIR = IMAGE_DIR + r'\pdf'

MAP_DPI = 160
MAP_QUALITY = 75

MAPTYPES = dict([
    ("Corner Record", "CR"),
    ("Highway Map", "HM"),
    ("Monument Map", "MM"),
    ("Parcel Map", "PM"),
    ("Record Map", "RM"),
    ("Survey", "RS"),
    ("Unrecorded Map", "UR"),
])

MAGICK = r'C:\Program Files\ImageMagick-6.9.5-Q16\magick.exe'

XML_DATA_UPDATE_MAP = '%s/map%d.xml' % (UPDATE_DIR, UPDATE_ID)
XML_DATA_UPDATE_TRS = '%s/trs%d.xml' % (UPDATE_DIR, UPDATE_ID)

XLSX_DATA_UPDATE = '%s/update%d.xlsx' % (UPDATE_DIR, UPDATE_ID)

XLSX_SHEET_UPDATE_NEW = 'update_new'
XLSX_SHEET_UPDATE_MODIFIED = 'update_modified'
XLSX_SHEET_UPDATE_MISSING = 'update_missing'
XLSX_SHEET_TRS_PATH = 'trs_path'
XLSX_SHEET_MAPTYPE = 'maptype'
XLSX_SHEET_SURVEYOR = 'surveyor'
XLSX_SHEET_PM_NUMBER = 'pm_number'
XLSX_SHEET_TRACT_NUMBER = 'tract_number'
XLSX_SHEET_CC = 'cc'

# Source values for legacy trs records
TRS_SOURCE_HOLLINS_SECTION = 0
TRS_SOURCE_HOLLINS_SUBSECTION = 1
TRS_SOURCE_PARSED_SECTION = 2
TRS_SOURCE_PARSED_SUBSECTION = 3
TRS_SOURCE_XLSX_DATA = 4

# Source id for current trs records
TRS_SOURCE = {
    'SOURCE_ID': UPDATE_ID,
    'DESCRIPTION': 'Update %d' % UPDATE_ID,
    'QUALITY': None
}

PG_USER_POSTGRES = 'postgres'
PG_USER_ADMIN = 'pgadmin'
PG_USER_PROD = 'hummaps'

PG_DATABASE_PROD = 'production'
PG_DATABASE_POSTGRES = 'postgres'

PG_HOST = 'localhost'

# IPV4 connection
DSN_PROD = 'dbname={database} user={user} host={host}'.format(
    database=PG_DATABASE_PROD,
    user=PG_USER_ADMIN,
    host=PG_HOST
)

# UNIX domain socket connection
# DSN_PROD = 'dbname={database} user={user}'.format(
#     database=PG_DATABASE_PROD, user=PG_USER_ADMIN
# )


SCHEMA_UPDATE = 'update%d' % UPDATE_ID

TABLE_UPDATE_MAP = SCHEMA_UPDATE + '.' + 'map'
TABLE_UPDATE_TRS_PATH = SCHEMA_UPDATE + '.' + 'trs_path'
TABLE_UPDATE_SURVEYOR = SCHEMA_UPDATE + '.' + 'surveyor'
TABLE_UPDATE_PM_NUMBER = SCHEMA_UPDATE + '.' + 'pm_number'
TABLE_UPDATE_TRACT_NUMBER = SCHEMA_UPDATE + '.' + 'tract_number'
TABLE_UPDATE_CC = SCHEMA_UPDATE + '.' + 'cc'

SCHEMA_PROD = 'hummaps'

TABLE_PROD_CC = SCHEMA_PROD + '.' + 'cc'
TABLE_PROD_CC_IMAGE = SCHEMA_PROD + '.' + 'cc_image'
TABLE_PROD_MAP = SCHEMA_PROD + '.' + 'map'
TABLE_PROD_MAP_IMAGE = SCHEMA_PROD + '.' + 'map_image'
TABLE_PROD_MAPTYPE = SCHEMA_PROD + '.' + 'maptype'
TABLE_PROD_PDF = SCHEMA_PROD + '.' + 'pdf'
TABLE_PROD_SCAN = SCHEMA_PROD + '.' + 'scan'
TABLE_PROD_SIGNED_BY = SCHEMA_PROD + '.' + 'signed_by'
TABLE_PROD_SOURCE = SCHEMA_PROD + '.' + 'source'
TABLE_PROD_SURVEYOR = SCHEMA_PROD + '.' + 'surveyor'
TABLE_PROD_TRS = SCHEMA_PROD + '.' + 'trs'
TABLE_PROD_TRS_PATH = SCHEMA_PROD + '.' + 'trs_path'

SEQUENCE_PROD_MAP_ID = SCHEMA_PROD + '.' + 'map_id_seq'
SEQUENCE_PROD_SURVEYOR_ID = SCHEMA_PROD + '.' + 'surveyor_id_seq'
SEQUENCE_PROD_TRS_PATH_ID = SCHEMA_PROD + '.' + 'trs_path_id_seq'

FUNCTION_MAP_ID = SCHEMA_PROD + '.' + 'map_id'
FUNCTION_MAP_NAME = SCHEMA_PROD + '.' + 'map_name'
FUNCTION_TOWNSHIP_NUMBER = SCHEMA_PROD + '.' + 'township_number'
FUNCTION_TOWNSHIP_STR = SCHEMA_PROD + '.' + 'township_str'
FUNCTION_RANGE_NUMBER = SCHEMA_PROD + '.' + 'range_number'
FUNCTION_RANGE_STR = SCHEMA_PROD + '.' + 'range_str'
FUNCTION_SUBSEC_BITS = SCHEMA_PROD + '.' + 'subsec_bits'
FUNCTION_SUBSEC_STR = SCHEMA_PROD + '.' + 'subsec_str'
FUNCTION_HOLLINS_SUBSEC = SCHEMA_PROD + '.' + 'hollins_subsec'
