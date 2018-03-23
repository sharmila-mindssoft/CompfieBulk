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
    # FORMAT_UPLOAD_PATH
)
from database import Database

# import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'bulkuploadcomplianceformat'

zipping_in_process = []

# In DB
file_status = {}


def before_first_request():
    cnx_pool = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    return cnx_pool

def validate_session(session_id):
    res_ponse_data = None
    try :
        session_id = request.args.get("sessionid")
        _db_con = before_first_request()
        _db = Database(_db_con)
        _db.begin()
        if _db.validate_session_token(session_id) is None:
            res_ponse_data = "Invalid session token"
    finally:
        _db.rollback()
        _db.close()
        _db_con.close()

    return res_ponse_data

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        session_id = request.args.get('session_id')
        session_output = validate_session(session_id)
        if session_output is None :
            return "invalid session token"
        else :
            csvid = request.args.get("csvid")
            load_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
            if not os.path.exists(load_path):
                os.makedirs(load_path)
                os.chmod(load_path, 0777)
            actual_file = os.path.join(load_path, f.filename)
            f.save(actual_file)
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

@app.route('/approve', methods=['GET'])
def approve():
    folder_name = request.args.get('folder_name')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    if not os.path.exists(folder_path):
        return "Error"
    if folder_name in zipping_in_process:
        return "Already Started"
    thread.start_new_thread(zip_folder, (folder_name, folder_path))
    return "started zipping"

@app.route('/downloadfile', methods=['GET'])
def downloadfile():
    folder_name = request.args.get('folder_name')
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

@app.route('/removefile', methods=['GET'])
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

    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)

if __name__ == "__main__":
    main()
