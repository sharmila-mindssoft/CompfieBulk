import logging

ROOTPATH = ""
knowledge_log_path = "logs/knowledge/knowledge-log"
client_log_path = "logs/client/client-log"
client_login_log_path = "logs/client/login-log"
webfront_log_path = "logs/webfront_log"

knowledge_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
rotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    knowledge_log_path,
    when="midnight",
    backupCount=10
)
rotateFileHandler.suffix = "%Y-%m-%d"
rotateFileHandler.setFormatter(knowledge_log_format)
rotateFileHandler.setLevel(logging.DEBUG)

knowledgeLogger = logging.getLogger("knowledge_logger")
knowledgeLogger.setLevel(logging.DEBUG)
knowledgeLogger.addHandler(rotateFileHandler)

client_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
cRotateFileHandler = logging.handlers.TimedRotatingFileHandler(
    client_log_path,
    when="midnight",
    backupCount=10
)
cRotateFileHandler.suffix = "%Y-%m-%d"
cRotateFileHandler.setFormatter(client_log_format)
cRotateFileHandler.setLevel(logging.DEBUG)

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

login_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
lrotateFileHandler = logging.handlers.RotatingFileHandler(
    client_login_log_path,
    maxBytes=102400,
    backupCount=10
)
lrotateFileHandler.suffix = "%Y-%m-%d"
lrotateFileHandler.setFormatter(login_log_format)
lrotateFileHandler.setLevel(logging.INFO)

loginLogger = logging.getLogger("login_logger")
loginLogger.setLevel(logging.INFO)
loginLogger.addHandler(lrotateFileHandler)

def logLogin(log_level, ip, user, message):
    log_message = "%s : %s : %s" % (ip, user, message)
    if log_level == "error" :
        loginLogger.error(log_message)
    elif log_level == "debug" :
        loginLogger.debug(log_message)
    elif log_level == "info" :
        loginLogger.info(log_message)

webfront_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
wrotateFileHandler = logging.handlers.RotatingFileHandler(
    webfront_log_path,
    maxBytes=102400,
    backupCount=10
)
wrotateFileHandler.suffix = "%Y-%m-%d"
wrotateFileHandler.setFormatter(webfront_log_format)
wrotateFileHandler.setLevel(logging.INFO)

webfrontLogger = logging.getLogger("webfrontend_logger")
webfrontLogger.setLevel(logging.INFO)
webfrontLogger.addHandler(wrotateFileHandler)

def logWebfront(message):
    log_message = "%s" % (message)
    webfrontLogger.info(log_message)
