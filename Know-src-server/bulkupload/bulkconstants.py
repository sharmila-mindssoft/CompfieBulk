import os
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

BULKUPLOAD_CSV_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadcsv")
BULKUPLOAD_INVALID_PATH = os.path.join(
    ROOT_PATH, "..", "..", "bulkuploadinvalid"
)

BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
BULK_UPLOAD_DB_PASSWORD = "123456"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload_apr_13"

CSV_DELIMITER = '|;|'
CSV_MAX_LINES = 1000
MAX_REJECTED_COUNT = 20

TEMP_FILE_SERVER = "http://localhost:8083/temp/"

#
# Constants For Bulk Upload Reports & Rejected
#
REJECTED_DOWNLOAD_PATH = os.path.join(
    ROOT_PATH, "..", "..", "rejected-downloads"
)
REJECTED_DOWNLOAD_BASE_PATH = "/knowledge/rejected/downloads/"

KM_USER_CATEGORY = 3
KE_USER_CATEGORY = 4
TM_USER_CATEGORY = 5
TE_USER_CATEGORY = 6
DM_USER_CATEGORY = 7
DE_USER_CATEGORY = 8

SYSTEM_REJECTED_BY = "COMPFIE"
REJECTED_FILE_DOWNLOADCOUNT = 2
SHOW_REMOVE_ICON = 1
SYSTEM_REJECT_ACTION_STATUS = 3
IS_FULLY_REJECT_ACTION_STATUS = 1
#
# Constants For Bulk Upload Reports & Rejected;
#
