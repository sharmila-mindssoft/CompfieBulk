import logging

ROOTPATH = ""
knowledge_log_path = "logs/knowledge/knowledge-log"
client_log_path = "logs/client/client-log"

log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")

rotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    knowledge_log_path,
    when="midnight",
    backupCount=10
)
rotateFileHandler.setFormatter(log_format)

knowledgeLogger = logging.getLogger("knowledge_logger")
knowledgeLogger.setLevel(logging.DEBUG)
knowledgeLogger.addHandler(rotateFileHandler)

cRotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    client_log_path,
    when="midnight",
    backupCount=10
)
cRotateFileHandler.setFormatter(log_format)

clientLogger = logging.getLogger("client_logger")
clientLogger.setLevel(logging.DEBUG)
clientLogger.addHandler(cRotateFileHandler)

def logKnowledge(log_level, from_file_name, message) :
    log_message = "%s : %s" % (from_file_name, message)
    if log_level == "debug" :
        knowledgeLogger.debug(log_message)
    elif log_level == "info" :
        knowledgeLogger.info(log_message)
    elif log_level == "error" :
        knowledgeLogger.error(log_message)


def logClient(log_level, from_file_name, message) :
    log_message = "%s : %s" % (from_file_name, message)
    if log_level == "debug" :
        clientLogger.debug(log_message)
    elif log_level == "info" :
        clientLogger.info(log_message)
    elif log_level == "error" :
        clientLogger.error(log_message)
