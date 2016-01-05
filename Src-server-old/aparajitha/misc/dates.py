import datetime
import calendar

__all__ = [
    "datetime_to_timestamp",
    "timestamp_to_datetime",
    "current_timestamp",
    "string_to_datetime",
    "datetime_to_string"
]

IntegerMonths = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

StringMonths = {
     1 : "Jan",
     2 : "Feb",
     3 : "Mar",
     4 : "Apr",
     5 : "May",
     6 : "Jun",
     7 : "Jul",
     8 : "Aug",
     9 : "Sep",
     10 : "Oct",
     11 : "Nov",
     12 : "Dec",
}

def datetime_to_timestamp(d) :
    return calendar.timegm(d.timetuple())

def timestamp_to_datetime(t) :
    return datetime.datetime.utcfromtimestamp(t)

def current_timestamp() :
    return datetime_to_timestamp(datetime.datetime.utcnow())

def string_to_datetime(string):
    date = string.split("-")
    datetime_val = datetime.datetime(year=int(date[2]), 
        month=IntegerMonths[date[1]], day=int(date[0]))
    return datetime_val

def datetime_to_string(datetime_val):
    return "%d-%s-%d" % (datetime_val.day, StringMonths[datetime_val.month], 
    	datetime_val.year)
