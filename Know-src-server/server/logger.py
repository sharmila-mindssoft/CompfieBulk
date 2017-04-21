import logging
from logging import handlers
import sys

from server.constants import (
    ENABLE_QUERY_LOG, ENABLE_DEBUG_LOG,
    ENABLE_API_LOG
)

knowledge_info_log_path = "logs/knowledge/knowledge-info-log"
knowledge_error_log_path = "logs/knowledge/knowledge-error-log"
knowledge_debug_log_path = "logs/knowledge/knowledge-debug-log"
know_query_log_path = "logs/knowledge/knowledge-query-log"

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

knowledgeApiLogger = _get_time_rotate_file_obj("knowledge_api", knowledge_info_log_path)
knowledgeInfoLogger = _get_time_rotate_file_obj("knowledge_info", knowledge_info_log_path)
knowledgeErrorLogger = _get_time_rotate_file_obj("knowledge_error", knowledge_error_log_path)
knowledgeDebugLogger = _get_time_rotate_file_obj("knowledge_debug", knowledge_debug_log_path)
knowledgeQueryLogger = _get_time_rotate_file_obj("knowledge_query", know_query_log_path)

def logKnowledge(log_level, from_file_name, message) :
    log_message = "%s : %s \n" % (from_file_name, message)

    if log_level == "info" :
        knowledgeInfoLogger.info(log_message)
    elif log_level == "error" :
        knowledgeErrorLogger.error(log_message)
    elif log_level == "query" and ENABLE_QUERY_LOG:
        knowledgeQueryLogger.info(log_message)
    elif log_level == "api" and ENABLE_API_LOG :
        knowledgeApiLogger.info(log_message)

    if ENABLE_DEBUG_LOG :
        knowledgeDebugLogger.debug(log_message)
