import os
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

BULKUPLOAD_CSV_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadcsv")
BULKUPLOAD_INVALID_PATH = os.path.join(
    ROOT_PATH, "..", "..", "bulkuploadinvalid"
)

BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
BULK_UPLOAD_DB_PASSWORD = "Msft!@#$%^"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload"

CSV_DELIMITER = '|;|'
CSV_MAX_LINES = 1000
MAX_REJECTED_COUNT = 20

TEMP_FILE_SERVER = "http://localhost:8083/temp/"

REJECTED_DOWNLOAD_PATH = os.path.join(
    ROOT_PATH, "..", "..", "rejected-downloads"
)
REJECTED_DOWNLOAD_BASE_PATH = "/knowledge/rejected/downloads/"

SYSTEM_REJECTED_BY = "COMPFIE"
REJECTED_FILE_DOWNLOADCOUNT = 2
