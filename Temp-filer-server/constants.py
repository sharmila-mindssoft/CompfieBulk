import os

KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "root"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge_new"
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

FORMAT_UPLOAD_PATH = os.path.join(ROOT_PATH, "bulkuploadcomplianceformat")
CLIENT_DOCUMENT_UPLOAD_PATH = os.path.join(
    ROOT_PATH, "bulkuploadclientdocuments"
)


BULK_UPLOAD_DB_HOST = "localhost"
BULK_UPLOAD_DB_PORT = 3306
BULK_UPLOAD_DB_USERNAME = "root"
BULK_UPLOAD_DB_PASSWORD = "root"
BULK_UPLOAD_DATABASE_NAME = "compfie_bulkupload"

ENABLE_API_LOG = False
ENABLE_QUERY_LOG = True
ENABLE_DEBUG_LOG = True

CLIENT_TEMP_FILE_SERVER = "http://localhost:8086/"
