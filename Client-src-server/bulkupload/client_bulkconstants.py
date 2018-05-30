import os
import pytz
import time
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

BULKUPLOAD_CSV_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadcsv")
BULKUPLOAD_INVALID_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadinvalid")

REJECTED_DOWNLOAD_PATH = os.path.join(ROOT_PATH, "..", "..", "rejected-downloads")
REJECTED_DOWNLOAD_BASE_PATH = "/knowledge/rejected/downloads/"

CSV_DOWNLOAD_URL = "/download/csv"

BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
BULK_UPLOAD_DB_PASSWORD = "123456"
# BULK_UPLOAD_DB_PASSWORD = "root"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload"

TEMP_FILE_SERVER = "http://localhost:8083/temp/"
FILE_SERVER = "http://localhost:8084/"


CSV_DELIMITER = '|;|'
CSV_MAX_LINE_ITEM = 100
