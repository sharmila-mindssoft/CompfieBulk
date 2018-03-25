import os


KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "123456"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge_new"
ROOT_PATH = os.path.join(os.path.split(__file__)[0])

FORMAT_UPLOAD_PATH = os.path.join(ROOT_PATH, "bulkuploadcomplianceformat")
