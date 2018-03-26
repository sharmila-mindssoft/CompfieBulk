import os
import pytz
import time
ROOT_PATH = os.path.join(os.path.split(__file__)[0])
#
# File upload path
#
KNOWLEDGE_FORMAT_PATH = os.path.join(ROOT_PATH, "knowledgeformat")
CLIENT_LOGO_PATH = os.path.join(ROOT_PATH, "clientlogo")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")

REJECTED_DOWNLOAD_PATH = os.path.join(ROOT_PATH, "..", "..", "rejected-downloads")
REJECTED_DOWNLOAD_BASE_PATH = "/knowledge/rejected/downloads/"


BULKUPLOAD_CSV_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadcsv")
BULKUPLOAD_INVALID_PATH = os.path.join(ROOT_PATH, "..", "..", "bulkuploadinvalid")
#
# File download url
#
KNOWLEDGE_FORMAT_DOWNLOAD_URL = "compliance_format"
LOGO_URL = "knowledge/clientlogo"
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
CSV_DOWNLOAD_URL = "/knowledge/downloadcsv"

# # Log flag #
ENABLE_API_LOG = False
ENABLE_QUERY_LOG = True
ENABLE_DEBUG_LOG = True
#
# Timezone
#
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")
IS_DEVELOPMENT = True
VERSION = 1
SEND_EMAIL = False
RECORD_DISPLAY_COUNT = 20
CAPTCHA_LENGTH = 6
NO_OF_FAILURE_ATTEMPTS = 3
FILE_TYPES = ["exe", "xhtml", "htm", "html", "py", "js", "zip"]
FILE_MAX_LIMIT = 1024 * 1024 * 50  # 50 MB
SESSION_CUTOFF = 15   # minutes
REGISTRATION_EXPIRY = 48  # Hours
FORGOTPASSWORD_EXPIRY = 48  # Hours
DOWNLOAD_EXPIRY = 48  # Hours
USER_ENABLE_CUTOFF = 30  # days


KNOWLEDGE_DB_POOL_SIZE = 200
KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "123456"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge_new"

URL = "http://localhost:8080/"
CLIENT_URL = URL
KNOWLEDGE_URL = URL + "knowledge"


BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
BULK_UPLOAD_DB_PASSWORD = "123456"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload"

CSV_DELIMITER = '|;|'
CSV_MAX_LINES = 1000
MAX_REJECTED_COUNT = 5

if IS_DEVELOPMENT is True :
    VERSION = time.time()

TEMP_FILE_SERVER = "http://localhost:9000/temp/"
