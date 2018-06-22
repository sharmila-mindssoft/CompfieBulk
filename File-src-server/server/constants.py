import os
import pytz

FILE_MAX_LIMIT = 1020 * 1024 * 50  # 50 MB
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")

FILE_TYPE = [
    "doc", "docx", "rtf", "pdf", "txt", "png", "jpeg", "gif", "csv", "xls", "xlsx",
    "rar", "tar", "gz", "ppt", "pptx", "jpg", "bmp", "odt", "odf", "ods"
]

EXPORT_PATH = os.path.join(ROOT_PATH, "exported_reports")
# "zip",

TEMP_FILE_SERVER = "http://localhost:8083/temp/"
CLIENT_TEMP_FILE_SERVER = "http://localhost:8086/clienttemp/"
