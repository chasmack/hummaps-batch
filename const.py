
# const.py - common constants

# XLSX_DATA_MAP = 'data/test65.xlsx'
XLSX_DATA_MAP = 'data/update65.xlsx'

XLSX_DATA_SURVEYOR = 'data/surveyor.xlsx'
XLSX_DATA_PM = 'data/pm.xlsx'
XLSX_DATA_TRACT = 'data/tract.xlsx'
XLSX_DATA_CC = 'data/cc.xlsx'

S3_BUCKET_MAPS = 'maps.hummaps.com'

MAPTYPES = (
    ("Corner Record", "CR"),
    ("Highway Map", "HM"),
    ("Monument Map", "MM"),
    ("Parcel Map", "PM"),
    ("Record Map", "RM"),
    ("Survey", "RS"),
    ("Unrecorded Map", "UR"),
)

# Source values for legacy trs records
TRS_SOURCE_HOLLINS_SECTION = 0
TRS_SOURCE_HOLLINS_SUBSECTION = 1
TRS_SOURCE_PARSED_SECTION = 2
TRS_SOURCE_PARSED_SUBSECTION = 3
TRS_SOURCE_XLSX_DATA = 4

# Source id for current trs records
TRS_SOURCE = {
    'source_id': 65,
    'description': 'Batch update 65',
    'quality': None
}

PG_USER_POSTGRES = 'postgres'
PG_USER_ADMIN = 'pgadmin'
PG_USER_PROD = 'hummaps'

PG_DATABASE_PROD = 'production'
PG_DATABASE_POSTGRES = 'postgres'

PG_HOST = 'p3'

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


SCHEMA_STAGING = 'hummaps_staging'

TABLE_STAGING_HOLLINS_MAP = SCHEMA_STAGING + '.' + 'hollins_map'
TABLE_STAGING_HOLLINS_MAP_QQ = SCHEMA_STAGING + '.' + 'hollins_map_qq'
TABLE_STAGING_HOLLINS_SUBSECTION_LIST = SCHEMA_STAGING + '.' + 'hollins_subsection_list'
TABLE_STAGING_HOLLINS_SURVEYOR = SCHEMA_STAGING + '.' + 'hollins_surveyor'
TABLE_STAGING_HOLLINS_TRS = SCHEMA_STAGING + '.' + 'hollins_trs'
TABLE_STAGING_HOLLINS_FULLNAME = SCHEMA_STAGING + '.' + 'hollins_fullname'

TABLE_STAGING_CC = SCHEMA_STAGING + '.' + 'cc'
TABLE_STAGING_CC_IMAGE = SCHEMA_STAGING + '.' + 'cc_image'
TABLE_STAGING_MAP = SCHEMA_STAGING + '.' + 'map'
TABLE_STAGING_MAP_IMAGE = SCHEMA_STAGING + '.' + 'map_image'
TABLE_STAGING_MAPTYPE = SCHEMA_STAGING + '.' + 'maptype'
TABLE_STAGING_PDF = SCHEMA_STAGING + '.' + 'pdf'
TABLE_STAGING_SCAN = SCHEMA_STAGING + '.' + 'scan'
TABLE_STAGING_SIGNED_BY = SCHEMA_STAGING + '.' + 'signed_by'
TABLE_STAGING_SOURCE = SCHEMA_STAGING + '.' + 'source'
TABLE_STAGING_SUBSEC_NAMES = SCHEMA_STAGING + '.' + 'subsec_names'
TABLE_STAGING_SURVEYOR = SCHEMA_STAGING + '.' + 'surveyor'
TABLE_STAGING_TRS = SCHEMA_STAGING + '.' + 'trs'
TABLE_STAGING_TRS_PATH = SCHEMA_STAGING + '.' + 'trs_path'

SEQUENCE_MAP_ID = SCHEMA_STAGING + '.' + 'map_id_seq'

FUNCTION_MAP_ID = SCHEMA_STAGING + '.' + 'map_id'
FUNCTION_MAP_NAME = SCHEMA_STAGING + '.' + 'map_name'
FUNCTION_TOWNSHIP_NUMBER = SCHEMA_STAGING + '.' + 'township_number'
FUNCTION_TOWNSHIP_STR = SCHEMA_STAGING + '.' + 'township_str'
FUNCTION_RANGE_NUMBER = SCHEMA_STAGING + '.' + 'range_number'
FUNCTION_RANGE_STR = SCHEMA_STAGING + '.' + 'range_str'
FUNCTION_SUBSEC_BITS = SCHEMA_STAGING + '.' + 'subsec_bits'
FUNCTION_SUBSEC_STR = SCHEMA_STAGING + '.' + 'subsec_str'
FUNCTION_HOLLINS_SUBSEC = SCHEMA_STAGING + '.' + 'hollins_subsec'

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
