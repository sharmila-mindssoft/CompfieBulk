import os
import io
import datetime
import pytz
import uuid
import random
import string
import hashlib
from server.constants import (
    LOCAL_TIMEZONE, KNOWLEDGE_FORMAT_PATH
)


########################################################
# Returns current date and time localized to Indian time
########################################################
def get_date_time() :
    time_stamp = datetime.datetime.utcnow()
    return str(localize(time_stamp))

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
    with io.FileIO(file_path, "wb") as fn :
        fn.write(file_content)
    return True

def new_uuid() :
        s = str(uuid.uuid4())
        return s.replace("-", "")


########################################################
# To check generate a random string with alpahbets
# and numbers
########################################################
def generate_random():
    characters = string.ascii_uppercase + string.digits
    return ''.join(
        random.SystemRandom().choice(characters) for _ in range(7)
    )

########################################################
# To generate random password encrypted with md5
# algorithm. This function return encrypted password and
# Original password
########################################################
def generate_and_return_password():
    password = generate_random()
    return encrypt(password), password

########################################################
# Encrypts the passed argument with md5 algorithm and
# returns the encrypted value
########################################################
def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()

########################################################
# Converts the passed date in string format to localized
# datetime format (Time zone is India)
########################################################
def string_to_datetime(string):
    string_in_date = string
    if string is not None:
        string_in_date = datetime.datetime.strptime(string, "%d-%b-%Y")
    return localize(string_in_date)

########################################################
# Coverts datetime passed in string format to datetime
# format
########################################################
def string_to_datetime_with_time(string):
    string_in_date = string
    if string is not None:
        string_in_date = datetime.datetime.strptime(string, "%d-%b-%Y %H:%M")
    return string_in_date

########################################################
# Localizes the given timestamp (Local Timezone is India)
########################################################
def localize(time_stamp):
    local_dt = LOCAL_TIMEZONE.localize(
        time_stamp
    )
    tzoffseet = local_dt.utcoffset()
    local_dt = local_dt.replace(tzinfo=None)
    local_dt = local_dt+tzoffseet
    return local_dt

########################################################
# Converts given datetime value to string (DATE format)
########################################################
def datetime_to_string(datetime_val):
    date_in_string = datetime_val
    if datetime_val is not None:
        date_in_string = datetime_val.strftime("%d-%b-%Y")
    return date_in_string

########################################################
# converts given datetime val to string (DATETIME format)
########################################################
def datetime_to_string_time(datetime_val):
    datetime_in_string = datetime_val
    if datetime_val is not None:
        datetime_in_string = datetime_val.strftime("%d-%b-%Y %H:%M")
    return datetime_in_string

def remove_uploaded_file(file_path):
    if os.path.exists(file_path) :
        os.remove(file_path)

def convert_base64_to_file(file_name, file_content, file_path=None):
    if file_path is None :
        file_path = "%s/%s" % (KNOWLEDGE_FORMAT_PATH, file_name)
    else:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            os.chmod(file_path, 0777)
        file_path = "%s/%s" % (file_path, file_name)
    remove_uploaded_file(file_path)
    if file_content is not None:
        new_file = open(file_path, "wb")
        new_file.write(file_content.decode('base64'))
        new_file.close()
