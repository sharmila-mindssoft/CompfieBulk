import logging
from logging import handlers
import sys

from server.constants import ENABLE_INFO_LOG, ENABLE_QUERY_LOG

ROOTPATH = ""
knowledge_log_path = "logs/knowledge/knowledge-log"
client_log_path = "logs/client/client-log"
client_login_log_path = "logs/client/login-log"
webfront_log_path = "logs/webfront-log"
trace_log_path = "logs/client/trace-log"
know_trace_log_path = "logs/knowledge/trace-log"
process_error_log_path = "logs/daily_process_error-log"
know_query_log_path = "logs/knowledge/query-log"
client_query_log_path = "logs/client/query-log"


def _get_time_rotate_file_obj(logger_name, log_path):
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
    rotateFileHandler = handlers.TimedRotatingFileHandler(
        log_path, when="midnight", backupCount=10
    )
    rotateFileHandler.suffix = "%Y-%m-%d"
    rotateFileHandler.setFormatter(log_format)
    rotateFileHandler.setLevel(logging.DEBUG)
    r_logger = logging.getLogger(logger_name)
    r_logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format)
    r_logger.addHandler(ch)
    r_logger.addHandler(rotateFileHandler)
    return r_logger


knowledgeLogger = _get_time_rotate_file_obj("knowledge_logger", knowledge_log_path)
def logKnowledge(log_level, from_file_name, message) :
    print "logKnowledge"
    log_message = "%s : %s" % (from_file_name, message)
    if log_level == "debug" :
        knowledgeLogger.debug(log_message)
    elif log_level == "info" :
        knowledgeLogger.info(log_message)
    elif log_level == "error" :
        knowledgeLogger.error(log_message)

clientLogger = _get_time_rotate_file_obj("client_logger", client_log_path)
def logClient(log_level, from_file_name, message) :
    log_message = "%s : %s" % (from_file_name, message)
    if log_level == "debug" :
        clientLogger.debug(log_message)
    elif log_level == "info" :
        clientLogger.info(log_message)
    elif log_level == "error" :
        clientLogger.error(log_message)

def _get_rotate_file_obj(logger_name, log_path):
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
    rotateFileHandler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=5000000, backupCount=10
    )
    rotateFileHandler.suffix = "%Y-%m-%d"
    rotateFileHandler.setFormatter(log_format)
    rotateFileHandler.setLevel(logging.INFO)
    r_logger = logging.getLogger(logger_name)
    r_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format)
    r_logger.addHandler(ch)
    r_logger.addHandler(rotateFileHandler)
    return r_logger

loginLogger = _get_rotate_file_obj("login_logger", client_login_log_path)

def logLogin(log_level, ip, user, message):
    log_message = "%s : %s : %s" % (ip, user, message)
    if log_level == "error" :
        loginLogger.error(log_message)
    elif log_level == "debug" :
        loginLogger.debug(log_message)
    elif log_level == "info" :
        loginLogger.info(log_message)


webfrontLogger = _get_rotate_file_obj("webfrontend_logger", webfront_log_path)
def logWebfront(message):
    log_message = "%s" % (message)
    if ENABLE_INFO_LOG :
        webfrontLogger.info(log_message)

traceLogger = _get_rotate_file_obj("trace_log", trace_log_path)
def logClientApi(callername, message):
    log_message = "%s: %s" % (callername, message)
    if ENABLE_INFO_LOG :
        traceLogger.info(log_message)

knowtraceLogger = _get_rotate_file_obj("know_trace_log", know_trace_log_path)
def logKnowledgeApi(callername, message):
    log_message = "%s: %s" % (callername, message)
    if ENABLE_INFO_LOG :
        knowtraceLogger.info(log_message)

processErrorLogger = _get_rotate_file_obj("process_error_log", process_error_log_path)
def logProcessError(callername, message):
    log_message = "%s : %s " % (callername, message)
    processErrorLogger.error(log_message)

knowtQueryLogger = _get_rotate_file_obj("know_query_log", know_query_log_path)
clientQueryLogger = _get_rotate_file_obj("client_query_log", client_query_log_path)
def logQuery(knowledge_qry, callername, message):
    log_message = "%s: %s" % (callername, message)
    if ENABLE_QUERY_LOG :
        if knowledge_qry :
            knowtQueryLogger.info(log_message)
        else :
            clientQueryLogger.info(log_message)
