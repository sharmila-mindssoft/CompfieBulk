import datetime
import calendar

__all__ = [
    "datetime_to_timestamp",
    "timestamp_to_datetime",
    "current_timestamp",
]

def datetime_to_timestamp(d) :
    return calendar.timegm(d.timetuple())

def timestamp_to_datetime(t) :
    return datetime.datetime.utcfromtimestamp(t)

def current_timestamp() :
    return datetime_to_timestamp(datetime.datetime.utcnow())
