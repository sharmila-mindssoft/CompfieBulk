
import os
import io
import datetime
import fileprotocol
from constants import (FILE_MAX_LIMIT, CLIENT_DOCS_BASE_PATH, LOCAL_TIMEZONE)

def localize(time_stamp):
    local_dt = LOCAL_TIMEZONE.localize(
        time_stamp
    )
    tzoffseet = local_dt.utcoffset()
    local_dt = local_dt.replace(tzinfo=None)
    local_dt = local_dt+tzoffseet
    return local_dt


def string_to_datetime(string):
    string_in_date = string
    if string is not None:
        string_in_date = datetime.datetime.strptime(string, "%d-%b-%Y")
    return localize(string_in_date)


def save_file_in_path(file_path, content, file_name):
    create_path = "%s/%s" % (file_path, file_name)
    try :
        with io.FileIO(create_path, "wb") as fn :
            fn.write(content.decode('base64'))
        return True
    except IOError, e :
        print e

def upload_file(request) :
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    country_id = request.country_id
    domain_id = request.domain_id
    unit_id = request.unit_id
    start_date = string_to_datetime(request.start_date).date()
    year = start_date.year
    file_info = request.file_info

    file_path = "%s/%s/%s/%s/%s/%s/%s/%s" % (
        CLIENT_DOCS_BASE_PATH, client_id, country_id, legal_entity_id,
        unit_id, domain_id, year, start_date
    )

    if not os.path.exists(file_path):
        print "path created ", file_path
        os.makedirs(file_path)

    is_success = False

    for f in file_info :
        print f
        file_name = f.file_name
        file_content = f.file_content

        file_info = file_name.split('.')
        if len(file_info) == 1 or len(file_info) > 2 :
            raise ValueError("Invalid File")

        elif len(file_content) == 0:
            raise ValueError("File cannot be empty")

        elif len(file_content) > FILE_MAX_LIMIT :
            raise ValueError("File max limit exceeded")

        if save_file_in_path(file_path, file_content, file_name):
            print os.path.exists("%s/%s" % (file_path, file_name))
            is_success = True

    if is_success :
        return fileprotocol.FileUploadSuccess()
    else :
        return fileprotocol.FileUploadFailed()

def remove_file(request):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    country_id = request.country_id
    domain_id = request.domain_id
    unit_id = request.unit_id
    start_date = string_to_datetime(request.start_date).date()
    year = start_date.year
    file_name = request.file_name

    file_path = "%s/%s/%s/%s/%s/%s/%s/%s/%s" % (
        CLIENT_DOCS_BASE_PATH, client_id, country_id, legal_entity_id,
        unit_id, domain_id, year, start_date, file_name
    )

    if os.path.exists(file_path) :
        os.remove(file_path)
        return fileprotocol.FileRemoved()
    else :
        return fileprotocol.FileRemoveFailed()

