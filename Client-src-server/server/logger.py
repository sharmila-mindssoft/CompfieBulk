import logging
from logging import handlers
import sys

from server.constants import (
    ENABLE_QUERY_LOG, ENABLE_DEBUG_LOG,
    ENABLE_API_LOG
)

client_info_log_path = "logs/client/client-info-log"
client_error_log_path = "logs/client/client-error-log"
client_debug_log_path = "logs/client/client-debug-log"
client_query_log_path = "logs/client/client-query-log"

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


clientApiLogger = _get_time_rotate_file_obj("client_api", client_info_log_path)
clientInfoLogger = _get_time_rotate_file_obj("client_info", client_info_log_path)
clientErrorLogger = _get_time_rotate_file_obj("client_error", client_error_log_path)
clientDebugLogger = _get_time_rotate_file_obj("client_debug", client_debug_log_path)
clientQueryLogger = _get_time_rotate_file_obj("client_query", client_query_log_path)

def logclient(log_level, from_file_name, message) :
    log_message = "%s : %s \n" % (from_file_name, message)

    if log_level == "info" :
        clientInfoLogger.info(log_message)
    elif log_level == "error" :
        clientErrorLogger.error(log_message)
    elif log_level == "query" and ENABLE_QUERY_LOG:
        clientQueryLogger.info(log_message)
    elif log_level == "api" and ENABLE_API_LOG :
        clientApiLogger.info(log_message)

    if ENABLE_DEBUG_LOG :
        clientDebugLogger.debug(log_message)
