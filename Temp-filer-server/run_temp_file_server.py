import os
import glob
from flask import (
    Flask, request,
    send_from_directory
)
from shutil import rmtree
import thread
from zipfile import ZipFile

import argparse
import socket
import mysql.connector

from constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME
    # FORMAT_UPLOAD_PATH
)
from database import Database

# import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'bulkuploadcomplianceformat'
print app.config['UPLOAD_PATH']
zipping_in_process = []

# In DB
file_status = {}

# STATIC_PATHS = [
#     ("/uploadedformat/<csvid>/<filename>", app.config['UPLOAD_PATH'])
# ]

# def staticTemplate(csvid, filename):
#     pathname = os.path.join(app.config['UPLOAD_PATH'], csvid)
#     print pathname, filename
#     return send_from_directory(pathname, filename)


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
    try :
        _db_con = knowledge_db_connect()
        _db = Database(_db_con)
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


def update_file_status(file_name, csv_id):
    res_ponse_data = None
    try :
        _db_con = bulkupload_db_connect()
        _db = Database(_db_con)
        _db.begin()
        if _db.update_file_status(csv_id, file_name) is None:
            res_ponse_data = False
        _db.commit()
    except Exception:
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return res_ponse_data

@app.route('/temp/upload', methods=['POST'])
def upload():
    print request
    if request.method == 'POST':
        f = request.files['file']

        session_id = request.args.get('session_id')
        session_output = validate_session(session_id)
        if session_output is False :
            return "invalid session token"
        else :
            csvid = request.args.get("csvid")
            load_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
            if not os.path.exists(load_path):
                os.makedirs(load_path)
                os.chmod(load_path, 0777)

            actual_file = os.path.join(load_path, f.filename)
            zip_f_name = actual_file + ".zip"
            # f.save(actual_file)
            f.save(zip_f_name)
            zip_ref = ZipFile(zip_f_name, 'r')
            zip_ref.extractall(load_path)
            zip_ref.close()
            os.remove(zip_f_name)
            if update_file_status(f.filename, csvid) is False :
                return "update failed"
            # f.save(f_name)
        # document_id = request.args.get('csvid')
        # validate session_id and document_id here
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
    print folder_path
    files = glob.glob(os.path.join(folder_path, "*"))
    files = [x for x in files if os.path.isfile(x)]
    with ZipFile(zip_f_name, "w") as newzip:
        for f in files:
            newzip.write(f)
    print "*" * 10
    print "Completed", zip_f_name
    print "*" * 10
    zipping_in_process.remove(folder_name)
    file_status[folder_name] = "Zipping Completed"

@app.route('/temp/approve', methods=['GET'])
def approve():
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if folder_name in zipping_in_process:
        return "Already Started"
    thread.start_new_thread(zip_folder, (folder_name, folder_path))
    return "started zipping"

@app.route('/temp/downloadfile', methods=['GET'])
def downloadfile():
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    zip_f_name = get_zip_file(folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if not os.path.isfile(zip_f_name):
        return "file not found"
    return send_from_directory(
        directory=app.config['UPLOAD_PATH'],
        filename="%s.zip" % (folder_name,)
    )

@app.route('/temp/removefile', methods=['GET'])
def removefile():
    folder_name = request.args.get('folder_name')
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

@app.route('/uploadedformat/<csvid>/<filename>', methods=['GET'])
def downloadformatfile(csvid, filename):
    print csvid, filename
    # folder_name = request.args.get('folder_name')
    assert filename is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
    print folder_path

    return send_from_directory(
        directory=folder_path,
        filename=filename
    )


args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    "port",
    help="port to listen at (PORT)"
)

def parse_port(port):
    try :
        port = int(port)
        assert (port > 0) and (port <= 65535)
        return port
    except Exception :
        return None

def parse_ip_address(ip_address):
    try :
        ip_address = ip_address.split(":")
        ip = ip_address[0].strip()
        socket.inet_aton(ip)
        port = ip_address[1].strip()
        port = parse_port(port)
        if port is None :
            return None

    except Exception :
        return None

    assert ip is not None
    assert port is not None
    return ip, port

def main():
    args = args_parser.parse_args()
    # address = parse_ip_address(args.address)
    # if address is None :
    #     msg = "error: ip address is not IP:PORT format: %s"
    #     print msg % (args.address,)
    # ip, port = address

    port = parse_port(args.port)
    if port is None :
        msg = "error: port is not in PORT format: %s"
        print msg % (args.port,)
        return

    print "Listening at %s" % (port)

    # for path in STATIC_PATHS:
    #     app.add_url_rule(
    #         path[0], view_func=staticTemplate, methods=['GET'],
    #         defaults={'pathname': path[1]}
    #     )

    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)

if __name__ == "__main__":
    main()
