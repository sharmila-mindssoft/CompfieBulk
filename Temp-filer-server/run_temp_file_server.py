import os
import glob
from os import rename
from flask import (
    Flask, request,
    send_from_directory
)
from shutil import rmtree
import thread
import zipfile

import argparse
import socket
import mysql.connector
import random
import string


from constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME
    # FORMAT_UPLOAD_PATH
)
from database import Database

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'bulkuploadcomplianceformat'
app.config['CLIENT_DOCUMENT_UPLOAD_PATH'] = 'bulkuploadclientdocuments'

print app.config['UPLOAD_PATH']
zipping_in_process = []

# In DB
file_status = {}

def knowledge_db_connect():
    cnx = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    return cnx


def bulkupload_db_connect():
    cnx_pool = mysql.connector.connect(
        user=BULK_UPLOAD_DB_USERNAME,
        password=BULK_UPLOAD_DB_PASSWORD,
        host=BULK_UPLOAD_DB_HOST,
        database=BULK_UPLOAD_DATABASE_NAME,
        port=BULK_UPLOAD_DB_PORT,
        autocommit=False,
    )
    return cnx_pool


def validate_session(session_id):
    res_ponse_data = None
    _db_con = knowledge_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        if _db.validate_session_token(session_id) is None:
            res_ponse_data = False
        _db.commit()
    except Exception:
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return res_ponse_data


def generate_random(length=7):
    characters = string.digits
    return ''.join(
        random.SystemRandom().choice(characters) for _ in range(length)
    )


def update_file_status(old_file_name, new_file_name, file_size, csv_id):
    print "File size in update fn-> ", file_size
    res_ponse_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        print "update file status"
        if _db.update_file_status(old_file_name, csv_id, new_file_name, file_size) is None:
            res_ponse_data = False
            print "update failed"
        _db.commit()
    except Exception:
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return res_ponse_data


def update_file_status_client(old_file_name, new_file_name, file_size, csv_id):
    res_ponse_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        print "update file status"
        if (
            _db.update_file_status_client(
                old_file_name, csv_id, new_file_name, file_size)
        ) is None:
            res_ponse_data = False
            print "update failed"
        _db.commit()
    except Exception:
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return res_ponse_data


def update_file_ddwnload_status(csv_id, status):
    res_ponse_data = None
    _db_con = bulkupload_db_connect()
    print "DB CON ", _db_con
    _db = Database(_db_con)
    print "_db- >", _db
    try:
        _db.begin()
        print "update format file status *** db ", _db
        db_stat = _db.update_format_file_status(csv_id, status)
        print "db_stat-> ", db_stat
        if db_stat is None:
            res_ponse_data = False
            print "update failed"
        _db.commit()
    except Exception:
        print "In Exception"
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    print "res_ponse_data-> ", res_ponse_data
    return res_ponse_data


def update_document_download_status(csv_id, status):
    res_ponse_data = None
    _db_con = bulkupload_db_connect()
    print "DB CON ", _db_con
    _db = Database(_db_con)
    print "_db- >", _db
    try:
        _db.begin()
        print "update past data doc file status *** db ", _db
        db_stat = _db.update_pastdata_document_status(csv_id, status)
        print "db_stat-> ", db_stat
        if db_stat is None:
            res_ponse_data = False
            print "update failed"
        _db.commit()
    except Exception, e:
        print "In Exception", e
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    print "res_ponse_data-> ", res_ponse_data
    return res_ponse_data


def delete_declined_docs(csv_id):
    print "csv_id-> ", csv_id
    res_ponse_data = None
    _db_con = bulkupload_db_connect()
    print "_db_con>> ", _db_con
    _db = Database(_db_con)
    try:
        _db.begin()

        db_stat = _db.get_declined_docs(csv_id)
        print "db_stat-> ", db_stat
        if db_stat is not None:
            res_ponse_data = db_stat
        # _db.commit()
    except Exception, e:
        print "In Exception"
        raise RuntimeError(str(e))
        # _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    print "res_ponse_data-> ", res_ponse_data
    return res_ponse_data


@app.route('/temp/upload', methods=['POST'])
def upload():
    print request
    if request.method == 'POST':
        f = request.files['file']

        session_id = request.args.get('session_id')
        session_output = validate_session(session_id)
        if session_output is False:
            return "invalid session token"
        else:
            csvid = request.args.get("csvid")
            load_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
            print "load_path-> ", load_path
            if not os.path.exists(load_path):
                os.makedirs(load_path)
                os.chmod(load_path, 0777)

            random_string = generate_random(5)
            print "Random string=> ", random_string
            print "f.filename->>> ", f.filename
            fn = f.filename
            fname = (fn).split(".")
            random_file_name = fname[0] + '-' + random_string + "." + fname[1]
            print "name->> ", f.name
            print "random_file_name>> ", random_file_name
            actual_file = os.path.join(load_path, f.filename)
            print "Actual file -> ", actual_file
            zip_f_name = actual_file + ".zip"
            print "zip_f_name--> ", zip_f_name
            print "F... ", f
            f.save(zip_f_name)
            zip_ref = zipfile.ZipFile(zip_f_name, 'r')
            print "zip ref", zip_ref
            print "load Path -> ", load_path
            zip_ref.extractall(load_path)
            zip_ref.close()
            print "load_path + f.filename> ", load_path + f.filename
            print "loadrandom_file_name", load_path + '/' + random_file_name
            os.rename(actual_file, load_path + '/' + random_file_name)
            renamed_file = os.path.join(load_path, random_file_name)
            os.remove(zip_f_name)
            renamed_file_size = os.path.getsize(renamed_file)
            print "actual_file_size-> ", renamed_file_size
            if update_file_status(
                f.filename, random_file_name, renamed_file_size, csvid
            ) is False:
                return "update failed"

        return "success"


@app.route('/client/temp/upload', methods=['POST'])
def upload_client():
    print request
    if request.method == 'POST':
        f = request.files['file']
        session_id = request.args.get('session_id')
        session_output = validate_session(session_id)

        random_string = generate_random(5)
        fn = f.filename
        fname = (fn).split(".")
        random_file_name = fname[0] + '-' + random_string + "." + fname[1]
        csvid = request.args.get("csvid")
        load_path = os.path.join(
            app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], csvid
        )
        if not os.path.exists(load_path):
            os.makedirs(load_path)
            os.chmod(load_path, 0777)

        actual_file = os.path.join(load_path, f.filename)
        zip_f_name = actual_file + ".zip"
        f.save(zip_f_name)
        zip_ref = zipfile.ZipFile(zip_f_name, 'r')
        zip_ref.extractall(load_path)
        zip_ref.close()
        os.rename(actual_file, load_path + '/' + random_file_name)
        renamed_file = os.path.join(load_path, random_file_name)
        renamed_file_size = os.path.getsize(renamed_file)
        os.remove(zip_f_name)
        if update_file_status_client(
            f.filename, random_file_name, renamed_file_size, csvid
        ) is False:
            return "update failed"

        return "success"


def get_zip_file(folder_name):
    zip_f_name = os.path.join(
        app.config['UPLOAD_PATH'], "%s.zip" % (folder_name)
    )
    return zip_f_name


def zip_folder(folder_name, folder_path):
    assert folder_name not in zipping_in_process
    zipping_in_process.append(folder_name)
    file_status[folder_name] = "Zipping Started"
    zip_f_name = get_zip_file(folder_name)
    print "folder_path-> ", folder_path
    files = glob.glob(os.path.join(folder_path, "*"))
    print "Files ->", files
    files = [x for x in files if os.path.isfile(x)]
    print files
    with zipfile.ZipFile(zip_f_name, "w", zipfile.ZIP_DEFLATED) as newzip:
        for f in files:
            arcname = f[len(folder_path) + 0:]
            newzip.write(f, arcname)
    print "*" * 10
    print "Completed", zip_f_name
    print "*" * 10
    if update_file_ddwnload_status(folder_name, "completed") is False:
        return "download status update failed"
    zipping_in_process.remove(folder_name)
    file_status[folder_name] = "Zipping Completed"


@app.route('/temp/approve', methods=['POST'])
def approve():
    print "CAME IN APPROVE"
    csv_id = request.args.get('csvid')
    dec_docs = delete_declined_docs(csv_id)
    folder_name = request.args.get('csvid')
    print "folder_name-> ", folder_name
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    print "Folder path->> ", folder_path
    for dd in dec_docs:
        print "dd>> ", dd
        if not os.path.isfile(folder_path + '/' + dd):
            return "File not exists"
        else:
            os.remove(folder_path + '/' + dd)

    if not os.path.exists(folder_path):
        return "Error"
    if folder_name in zipping_in_process:
        return "Already Started"
    thread.start_new_thread(zip_folder, (folder_name, folder_path))
    print "Thred ", thread
    # if update_file_ddwnload_status(folder_name, "inprogress") is False:
        # return "download status update failed"
    print " at before started zippng"
    return "started zipping"


@app.route('/temp/downloadfile', methods=['GET'])
def downloadfile():
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    print "FOLDER pATH IN DOWNLOAD"
    zip_f_name = get_zip_file(folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if not os.path.isfile(zip_f_name):
        return "file not found"
    return send_from_directory(
        directory=app.config['UPLOAD_PATH'],
        filename="%s.zip" % (folder_name,)
    )

@app.route('/temp/removefile', methods=['POST'])
def removefile():
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    zip_f_name = get_zip_file(folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if not os.path.isfile(zip_f_name):
        return "file not found"
    os.remove(zip_f_name)
    rmtree(folder_path)
    return "removed zip file"


@app.route('/temp/removeclientfile', methods=['POST'])
def removeclientfile():
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], folder_name)
    zip_f_name = get_client_zip_file(folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if not os.path.isfile(zip_f_name):
        return "file not found"
    os.remove(zip_f_name)
    rmtree(folder_path)
    return "removed zip file"


@app.route('/uploadedformat/<csvid>/<filename>', methods=['GET'])
def downloadformatfile(csvid, filename):
    print csvid, filename
    # folder_name = request.args.get('folder_name')
    assert csvid is not None
    assert filename is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
    print folder_path

    return send_from_directory(
        directory=folder_path,
        filename=filename
    )


@app.route('/temp/docsubmit', methods=['POST'])
def approve_client():
    print "CAME IN Client APPROVE"
    folder_name = request.args.get('csvid')
    print "folder_name-> ", folder_name
    print "country id>>", request.args.get('c_id')
    assert folder_name is not None
    folder_path = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], folder_name
    )
    print "Folder path->> ", folder_path

    if not os.path.exists(folder_path):
        return "Error"
    if folder_name in zipping_in_process:
        return "Already Started"
    thread.start_new_thread(client_zip_folder, (folder_name, folder_path))
    print "Thred ", thread
    print " at before started zippng"
    return "started zipping"


def client_zip_folder(folder_name, folder_path):
    assert folder_name not in zipping_in_process
    zipping_in_process.append(folder_name)
    file_status[folder_name] = "Zipping Started"
    zip_f_name = get_client_zip_file(folder_name)
    print "folder_path-> ", folder_path
    files = glob.glob(os.path.join(folder_path, "*"))
    print "Files ->", files
    files = [x for x in files if os.path.isfile(x)]
    print files
    with zipfile.ZipFile(zip_f_name, "w", zipfile.ZIP_DEFLATED) as newzip:
        for f in files:
            arcname = f[len(folder_path) + 0:]
            newzip.write(f, arcname)
    print "@" * 10
    print "Completed", zip_f_name
    print "@" * 10
    if update_document_download_status(folder_name, "completed") is False:
        return "download status update failed"
    zipping_in_process.remove(folder_name)
    file_status[folder_name] = "Zipping Completed"


def get_client_zip_file(folder_name):
    zip_f_name = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], "%s.zip" % (folder_name)
    )
    return zip_f_name


@app.route('/temp/downloadclientfile', methods=['GET'])
def download_client_file():
    print "in download client file"
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    print "folder Name-> ", folder_name
    folder_path = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], folder_name)
    print "FOLDER pATH IN DOWNLOAD"
    zip_f_name = get_client_zip_file(folder_name)
    print 'Path Exists ->>>', os.path.exists(folder_path)
    print 'zip size ->>> ', os.path.getsize(folder_path)

    if not os.path.exists(folder_path):
        return "Error"
    if not os.path.isfile(zip_f_name):
        return "file not found"
    return send_from_directory(
        directory=app.config['CLIENT_DOCUMENT_UPLOAD_PATH'],
        filename="%s.zip" % (folder_name,)
    )


args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    "port",
    help="port to listen at (PORT)"
)


def parse_port(port):
    try:
        port = int(port)
        assert (port > 0) and (port <= 65535)
        return port
    except Exception:
        return None


def parse_ip_address(ip_address):
    try:
        ip_address = ip_address.split(":")
        ip = ip_address[0].strip()
        socket.inet_aton(ip)
        port = ip_address[1].strip()
        port = parse_port(port)
        if port is None:
            return None

    except Exception:
        return None

    assert ip is not None
    assert port is not None
    return ip, port


def main():
    args = args_parser.parse_args()

    port = parse_port(args.port)
    if port is None:
        msg = "error: port is not in PORT format: %s"
        print msg % (args.port,)
        return

    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)


if __name__ == "__main__":
    main()
