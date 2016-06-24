import os
import pytz
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

#
# File upload path
#

KNOWLEDGE_FORMAT_PATH = os.path.join(ROOT_PATH, "knowledgeformat")
CLIENT_LOGO_PATH = os.path.join(ROOT_PATH, "clientlogo")

#
# File download url
#

FORMAT_DOWNLOAD_URL = "compliance_format"
LOGO_URL = "knowledge/clientlogo"

#
# Timezone
#

LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")

IS_DEVELOPMENT = True
VERSION = 1
SEND_EMAIL = False
RECORD_DISPLAY_COUNT = 100

KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "123456"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge"

CLIENT_URL = "http://localhost:8080/"
KNOWLEDGE_URL = "http://localhost:8082/knowledge"
