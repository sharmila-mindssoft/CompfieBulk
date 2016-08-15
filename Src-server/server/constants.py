import os
import pytz
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

#
# File upload path
#

KNOWLEDGE_FORMAT_PATH = os.path.join(ROOT_PATH, "knowledgeformat")
CLIENT_LOGO_PATH = os.path.join(ROOT_PATH, "clientlogo")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")
#
# File download url
#

KNOWLEDGE_FORMAT_DOWNLOAD_URL = "compliance_format"
LOGO_URL = "knowledge/clientlogo"
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"

#
# Log flag
#
ENABLE_INFO_LOG = False
ENABLE_QUERY_LOG = False

#
# Timezone
#

LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")

IS_DEVELOPMENT = True
VERSION = 1
SEND_EMAIL = False
RECORD_DISPLAY_COUNT = 100
FILE_TYPES = ["exe", "xhtml", "htm", "html", "py", "js"]
FILE_MAX_LIMIT = 1024 * 1024 * 50  # 50 MB

KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "123456"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge"

CLIENT_URL = "http://localhost:8080/"
KNOWLEDGE_URL = "http://localhost:8082/knowledge"
