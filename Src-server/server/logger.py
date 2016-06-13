import logging
import sys

ROOTPATH = ""
knowledge_log_path = "logs/knowledge/knowledge-log"
client_log_path = "logs/client/client-log"
client_login_log_path = "logs/client/login-log"
webfront_log_path = "logs/webfront-log"
trace_log_path = "logs/client/trace-log"
know_trace_log_path = "logs/knowledge/trace-log"

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
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(webfront_log_format)
webfrontLogger.addHandler(ch)
webfrontLogger.addHandler(wrotateFileHandler)

def logWebfront(message):
    log_message = "%s" % (message)
    webfrontLogger.info(log_message)

trace_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
trotateFileHandler = logging.handlers.RotatingFileHandler(
    trace_log_path,
    maxBytes=50000,
    backupCount=20
)
trotateFileHandler.suffix = "%Y-%m-%d"
trotateFileHandler.setFormatter(trace_log_format)
trotateFileHandler.setLevel(logging.INFO)

traceLogger = logging.getLogger("trace_log")
traceLogger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(trace_log_format)
traceLogger.addHandler(ch)
traceLogger.addHandler(trotateFileHandler)

def logClientApi(callername, message):
    log_message = "%s: %s" % (callername, message)
    traceLogger.info(log_message)

know_trace_log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
knowrotateFileHandler = logging.handlers.RotatingFileHandler(
    know_trace_log_path,
    maxBytes=50000,
    backupCount=10
)
knowrotateFileHandler.suffix = "%Y-%m-%d"
knowrotateFileHandler.setFormatter(know_trace_log_format)
knowrotateFileHandler.setLevel(logging.INFO)

knowtraceLogger = logging.getLogger("know_trace_log")
knowtraceLogger.setLevel(logging.INFO)
knowtraceLogger.addHandler(knowrotateFileHandler)

def logKnowledgeApi(callername, message):
    log_message = "%s: %s" % (callername, message)
    knowtraceLogger.info(log_message)
