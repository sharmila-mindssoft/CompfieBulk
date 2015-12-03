import datetime
import calendar

__all__ = [
    "datetimeToTimestamp",
    "timestampToDatetime",
    "currentTimestamp",
    "stringToDatetime",
    "datetimeToString"
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

def datetimeToTimestamp(d) :
    return calendar.timegm(d.timetuple())

def timestampToDatetime(t) :
    return datetime.datetime.utcfromtimestamp(t)

def currentTimestamp() :
    return datetimeToTimestamp(datetime.datetime.utcnow())

def stringToDatetime(string):
    date = string.split("-")
    datetimeVal = datetime.datetime(year=int(date[2]), 
        month=IntegerMonths[date[1]], day=int(date[0]))
    return datetimeVal

def datetimeToString(datetimeVal):
    return "%d-%s-%d" % (datetimeVal.day, StringMonths[datetimeVal.month], 
    	datetimeVal.year)
