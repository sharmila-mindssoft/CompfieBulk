import logging

ROOTPATH = ""
knowledge_log_path = "logs/knowledge/knowledge-log"
client_log_path = "logs/client/client-log"

knowledge_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")


rotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    knowledge_log_path,
    when="midnight",
    backupCount=1
)
rotateFileHandler.suffix = "%Y-%m-%d"
rotateFileHandler.setFormatter(knowledge_log_format)

knowledgeLogger = logging.getLogger("knowledge_logger")
knowledgeLogger.setLevel(logging.DEBUG)
knowledgeLogger.addHandler(rotateFileHandler)

client_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
cRotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    client_log_path,
    when="midnight",
    backupCount=1
)
cRotateFileHandler.suffix = "%Y-%m-%d"
cRotateFileHandler.setFormatter(client_log_format)

clientLogger = logging.getLogger("client_logger")
clientLogger.setLevel(logging.DEBUG)
clientLogger.addHandler(cRotateFileHandler)

def logKnowledge(log_level, from_file_name, message) :
    print "logKnowledge"
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
