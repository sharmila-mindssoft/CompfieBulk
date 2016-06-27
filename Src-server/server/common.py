import datetime
import pytz
import uuid

def get_system_date():
    date = datetime.datetime.today()
    return date

def get_current_month():
    month = get_system_date().month
    return month

def addMonth(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value*366 / 12))
    return new_date

def addDays(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value))
    return new_date

def addYears(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value * 366))
    return new_date

def convert_string_to_date(due_date):
    due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    return due_date

def create_new_date(date, days, month):
    current_date = date
    try :
        date = date.replace(day=int(days), month=int(month))
    except ValueError :
        if date.month == 12 :
            days = 31
        else :
            days = (date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)).day
        date = date.replace(day=days)

    if date < current_date :
        date = date.replace(year=date.year+1)
    return date

def convert_to_dict(data_list, columns) :
    assert type(data_list) in (list, tuple)
    if len(data_list) > 0:
        if type(data_list[0]) is tuple :
            result_list = []
            if len(data_list[0]) == len(columns) :
                for data in data_list:
                    result = {}
                    for i, d in enumerate(data):
                        result[columns[i]] = d
                    result_list.append(result)
            return result_list
        else :
            result = {}
            if len(data_list) == len(columns) :
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result
    else:
        return []

def time_convertion(time_zone):
    current_time = datetime.datetime.utcnow()
    print "current_time"
    print current_time
    CT_TIMEZONE = pytz.timezone(str(time_zone))
    print CT_TIMEZONE
    dt = CT_TIMEZONE.localize(current_time)
    tzoffset = dt.utcoffset()
    dt = dt.replace(tzinfo=None)
    dt = dt+tzoffset
    print dt
    return dt

def return_hour_minute(current_time):
    return current_time.strftime("%H:%M")

def return_date(current_time):
    return current_time.date()

def insert(table, columns, values) :
    columns = ",".join(columns)
    stringValue = ""
    for index, value in enumerate(values):
        if(index < len(values)-1):
            stringValue = stringValue+"'"+str(value)+"',"
        else:
            stringValue = stringValue+"'"+str(value)+"'"
    query = "INSERT INTO %s (%s) VALUES (%s)" % (
        table, columns, stringValue
    )
    return query

def save_file_in_path(file_path, file_content, file_name):
    with open(file_path, "wb") as fn :
        fn.write(file_content)
    return True

def new_uuid(self) :
        s = str(uuid.uuid4())
        return s.replace("-", "")
