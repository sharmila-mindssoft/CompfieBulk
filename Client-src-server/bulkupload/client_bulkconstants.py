import os
import pytz

ROOT_PATH = os.path.join(os.path.split(__file__)[0])
BULKUPLOAD_CSV_PATH = os.path.join(
    ROOT_PATH, "..", "..", "bulkuploadcsv")
BULKUPLOAD_INVALID_PATH = os.path.join(
    ROOT_PATH, "..", "..", "bulkuploadinvalid")
REJECTED_DOWNLOAD_PATH = os.path.join(
    ROOT_PATH, "..", "..", "rejected-downloads")
REJECTED_DOWNLOAD_BASE_PATH = "/knowledge/rejected/downloads/"
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "..", "..", "clientdocuments")

CSV_DOWNLOAD_URL = "/download/csv"

BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
# BULK_UPLOAD_DB_PASSWORD = "123456"
BULK_UPLOAD_DB_PASSWORD = "root"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload"

CLIENT_TEMP_FILE_SERVER = "http://localhost:8086/clienttemp/"
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")


CSV_DELIMITER = "|;|"
CSV_MAX_LINE_ITEM = 100

string_months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}
