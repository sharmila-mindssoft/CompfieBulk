import logging
from logging import handlers
import sys

from constants import (
    ENABLE_QUERY_LOG, ENABLE_DEBUG_LOG,
    ENABLE_API_LOG
)

temp_file_info_log_path = "logs/tempfile/tempfile-info-log"
temp_file_error_log_path = "logs/tempfile/tempfile-error-log"
temp_file_debug_log_path = "logs/tempfile/tempfile-debug-log"
temp_file_log_path = "logs/tempfile/tempfile-query-log"


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

tempFileApiLogger = _get_time_rotate_file_obj("tempfile_api", temp_file_info_log_path)
tempFileInfoLogger = _get_time_rotate_file_obj("tempfile_info", temp_file_info_log_path)
tempFileErrorLogger = _get_time_rotate_file_obj("tempfile_error", temp_file_error_log_path)
tempFileDebugLogger = _get_time_rotate_file_obj("tempfile_debug", temp_file_debug_log_path)
tempFileQueryLogger = _get_time_rotate_file_obj("tempfile_query", temp_file_log_path)


def logTempFiler(log_level, from_file_name, message):
    log_message = "%s : %s \n" % (from_file_name, message)
    if log_level == "info":
        tempFileInfoLogger.info(log_message)
    elif log_level == "error":
        tempFileErrorLogger.error(log_message)
    elif log_level == "query" and ENABLE_QUERY_LOG:
        tempFileQueryLogger.info(log_message)
    elif log_level == "api" and ENABLE_API_LOG:
        tempFileApiLogger.info(log_message)

    if ENABLE_DEBUG_LOG:
        tempFileDebugLogger.debug(log_message)
