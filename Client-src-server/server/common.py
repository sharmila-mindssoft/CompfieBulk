import os
import io
import datetime
import pytz
import uuid
import random
import string
import hashlib
from calendar import monthrange
from server.constants import (
    LOCAL_TIMEZONE, KNOWLEDGE_FORMAT_PATH
)


########################################################
# Returns current date and time localized to Indian time
########################################################

string_months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

def get_date_time():
    time_stamp = datetime.datetime.utcnow()
    return str(localize(time_stamp))


def get_date_time_in_date():
    time_stamp = datetime.datetime.utcnow()
    return localize(time_stamp)

def get_current_date():
    time_stamp = datetime.datetime.utcnow()
    return localize(time_stamp).date()

def get_system_date():
    date = datetime.datetime.today()
    return date


def get_current_month():
    month = get_system_date().month
    return month


def addMonth(value, due_date):
    try:
        m = due_date.month - 1 + value
        y = (due_date.year + m / 12)
        m = m % 12 + 1
        m_range = monthrange(y, m)
        d = min(due_date.day, m_range[1])
        new_date = datetime.date(y, m, d)
        return new_date
    except Exception, e:
        print e


def addDays(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value))
    return new_date

def addHours(value, due_date):
    new_date = (due_date + datetime.timedelta(hours=value))
    return new_date

def addYear(value, due_date):
    try:
        m = due_date.month - 1
        y = due_date.year + value
        m = m % 12 + 1
        m_range = monthrange(y, m)
        d = min(due_date.day, m_range[1])
        new_date = datetime.date(y, m, d)
        return new_date
    except Exception, e:
        print e


def addYears(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value * 366))
    return new_date


def convert_string_to_date(due_date):
    due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    return due_date


def create_new_date(date, days, month):
    current_date = date
    try:
        date = date.replace(day=int(days), month=int(month))
    except ValueError:
        if date.month == 12:
            days = 31
        else:
            days = (
                date.replace(
                    month=date.month+1, day=1) - datetime.timedelta(days=1)
            ).day
        date = date.replace(day=days)

    if date < current_date:
        date = date.replace(year=date.year+1)
    return date


def convert_to_dict(data_list, columns):
    assert type(data_list) in (list, tuple)
    if len(data_list) > 0:
        if type(data_list[0]) is tuple:
            result_list = []
            if len(data_list[0]) == len(columns):
                for data in data_list:
                    result = {}
                    for i, d in enumerate(data):
                        result[columns[i]] = d
                    result_list.append(result)
            return result_list
        else:
            result = {}
            if len(data_list) == len(columns):
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result
    else:
        return []


def convert_to_key_dict(data_list, columns):
    assert type(data_list) in (list, tuple)
    if len(data_list) > 0:
        if type(data_list[0]) is tuple:
            result_list = {}
            if len(data_list[0]) == len(columns):
                for data in data_list:
                    result = {}
                    for i, d in enumerate(data):
                        result[columns[i]] = d
                    result_list[int(data[0])] = result
            return result_list
        else:
            result = {}
            if len(data_list) == len(columns):
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result
    else:
        return []


def time_convertion(time_zone):
    current_time = datetime.datetime.utcnow()
    CT_TIMEZONE = pytz.timezone(str(time_zone))
    dt = CT_TIMEZONE.localize(current_time)
    tzoffset = dt.utcoffset()
    dt = dt.replace(tzinfo=None)
    dt = dt+tzoffset
    return dt


def return_hour_minute(current_time):
    return current_time.strftime("%H:%M")


def return_date(current_time):
    return current_time.date()


def insert(table, columns, values):
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
    with io.FileIO(file_path, "wb") as fn:
        fn.write(file_content)
    return True


def new_uuid():
        s = str(uuid.uuid4())
        return s.replace("-", "")


########################################################
# To check generate a random string with alpahbets
# and numbers
########################################################
def generate_random(length=7):
    characters = string.ascii_uppercase + string.digits
    return ''.join(
        random.SystemRandom().choice(characters) for _ in range(length)
    )

def generate_special_random(length=7):
    characters = string.ascii_uppercase + string.digits
    return ''.join(
        random.SystemRandom().choice(characters) for _ in range(length)
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


# def get_current_date():
#     date = datetime.datetime.today()
#     return date


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
    print time_stamp
    local_dt = LOCAL_TIMEZONE.localize(
        time_stamp
    )
    tzoffseet = local_dt.utcoffset()
    local_dt = local_dt.replace(tzinfo=None)
    local_dt = local_dt+tzoffseet
    print local_dt.date()
    print type(local_dt)
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

########################################################
# converts given datetime val to string (DATETIME format)
########################################################
def datetime_to_moth_year(datetime_val):
    datetime_in_string = datetime_val
    if datetime_val is not None:
        datetime_in_string = datetime_val.strftime("%b'%Y")
    return datetime_in_string


def remove_uploaded_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def convert_base64_to_file(file_name, file_content, file_path=None):
    if file_path is None:
        file_path = "%s/%s" % (KNOWLEDGE_FORMAT_PATH, file_name)
    else:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            os.chmod(file_path, 0777)
        file_path = "%s/%s" % (file_path, file_name)
    remove_uploaded_file(file_path)
    if file_content is not None:
        with io.FileIO(file_path, "wb") as fn:
            fn.write(file_content.decode('base64'))

def make_summary(data, data_type, c):
    string_months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    summary = ""
    sdates = ""
    triggers = ""
    if data_type == 1 :
        if len(data) > 0:
            dat = data[0].statutory_date
            mon = data[0].statutory_month
            day = data[0].trigger_before_days
            if mon is not None :
                summary += string_months.get(mon)
            if dat is not None :
                summary += " " + str(dat)

            triggers = " Trigger : %s days" % (day)

            return summary, None, triggers
        else:
            return None, None, None

    elif data_type in (2, 3) :
        dates = []
        trigger = []
        if len(data) > 0:
            for d in data :
                dat_summary = ""
                dat = d.statutory_date
                mon = d.statutory_month
                day = d.trigger_before_days
                if mon is not None :
                    dat_summary += string_months.get(mon)
                if dat is not None :
                    dat_summary += " " + str(dat)

                dates.append(dat_summary)
                if day is not None :
                    trigger.append(" %s days " % (day))

            summary = "Repeats every %s - %s. " % (
                c["repeats_every"], c["repeat_type"]
            )
            sdates = ", ".join(dates)
            if len(trigger) > 0 :
                triggers = " Trigger : " + ", ".join(trigger)

    elif data_type == 4:
        dates = []
        trigger = []
        if len(data) > 0:
            for d in data :
                dat_summary = ""
                dat = d.statutory_date
                mon = d.statutory_month
                day = d.trigger_before_days
                if mon is not None :
                    dat_summary += string_months.get(mon)
                if dat is not None :
                    dat_summary += " " + str(dat)

                dates.append(dat_summary)

                if day is not None :
                    trigger.append(" %s days " % (day))
            summary = "Repeats every "
            is_none = True
            if c["repeats_every"] is not None :
                summary += str(c["repeats_every"])
                is_none = False

            if c["repeat_type"] is not None :
                summary += " - " + c["repeat_type"]
                is_none = False

            if is_none:
                summary = ""
            sdates = ", ".join(dates)
            if len(trigger) > 0 :
                triggers = " Trigger : " + ", ".join(trigger)

    elif data_type == 5 :
        summary = "To complete within %s - %s" % (
            c["duration"], c["duration_type"]
        )
        sdates = None

    return summary, sdates, triggers
