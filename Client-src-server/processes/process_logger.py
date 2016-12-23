import logging
from logging import handlers
import sys

def _get_rotate_file_obj(logger_name, log_path):
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
    rotateFileHandler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=10000000, backupCount=10
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

process_error_log_path = "logs/daily_process_error-log"
processErrorLogger = _get_rotate_file_obj("process_error_log", process_error_log_path)
def logProcessError(callername, message):
    log_message = "%s : %s \n" % (callername, message)
    processErrorLogger.error(log_message)

process_info_log_path = "logs/daily_process_info-log"
processInfoLogger = _get_rotate_file_obj("process_info_log", process_info_log_path)
def logProcessInfo(callername, message):
    log_message = "%s : %s \n" % (callername, message)
    processInfoLogger.error(log_message)


notify_error_log_path = "logs/daily_notify_error-log"
notifyErrorLogger = _get_rotate_file_obj("notify_error_log", notify_error_log_path)
def logNotifyError(callername, message):
    log_message = "%s : %s \n" % (callername, message)
    notifyErrorLogger.error(log_message)

notify_info_log_path = "logs/daily_notify_info-log"
notifyInfoLogger = _get_rotate_file_obj("notify_info_log", notify_info_log_path)
def logNotifyInfo(callername, message):
    log_message = "%s : %s \n" % (callername, message)
    notifyInfoLogger.error(log_message)
