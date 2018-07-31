import io
import os
import glob
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
import logger
import traceback

from constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME,
    CLIENT_TEMP_FILE_SERVER
)
from database import Database

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'bulkuploadcomplianceformat'
app.config['CLIENT_DOCUMENT_UPLOAD_PATH'] = 'bulkuploadclientdocuments'

# app.config['UPLOAD_PATH']
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
    response_data = None
    _db_con = knowledge_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        if _db.validate_session_token(session_id) is None:
            response_data = False
        _db.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > validate_session()", str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > validate_session()",
            str(traceback.format_exc())
        )
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return response_data


def generate_random(length=7):
    characters = string.digits
    return ''.join(
        random.SystemRandom().choice(characters) for _ in range(length)
    )


def update_file_status(old_file_name, new_file_name, file_size, csv_id):
    response_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        if _db.update_file_status(
            old_file_name, csv_id, new_file_name, file_size
        ) is None:
            response_data = False
        _db.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_status()", str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_status()",
            str(traceback.format_exc())
        )
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return response_data


def update_file_status_client(update_tuples):
    response_data = None
    _db_con = bulkupload_db_connect()
    # _db = Database(_db_con)
    try:
        # _db_con.begin()
        query = ""
        for data in update_tuples:
            old_file_name = data[0]
            new_file_name = data[1]
            file_size = data[2]
            csv_id = data[3]
            q1 = "update tbl_bulk_past_data set document_upload_status = 1, \
            document_file_size = %s , document_name = '%s' \
            where csv_past_id = %s and document_name='%s';" % (
                file_size, new_file_name, csv_id, old_file_name
            )
            query += q1
        q2 = "update tbl_bulk_past_data_csv \
            set uploaded_documents = uploaded_documents + %s \
            where csv_past_id = %s and uploaded_documents \
            < total_documents;" % (len(update_tuples), csv_id)
        q3 = "UPDATE tbl_bulk_past_data_csv SET upload_status = 1 WHERE \
            uploaded_documents = total_documents AND csv_past_id = %s;" % (
                csv_id
            )
        query += q2 + q3 
        result = _db_con.cmd_query_iter(query)
        _db_con.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_status_client()",
            str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_status_client()",
            str(traceback.format_exc())
        )
        _db_con.rollback()

    finally:
        _db_con.close()
    return response_data


def update_file_download_status(csv_id, status):
    response_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        db_stat = _db.update_format_file_status(csv_id, status)
        if db_stat is None:
            response_data = False
        _db.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_download_status()",
            str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > update_file_download_status()",
            str(traceback.format_exc())
        )
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()
    return response_data


def update_document_download_status(csv_id, status):
    response_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()
        db_stat = _db.update_past_data_document_status(csv_id, status)
        if db_stat is None:
            response_data = False
        _db.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > update_document_download_status",
            str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > update_document_download_status",
            str(traceback.format_exc())
        )
        _db.rollback()

    finally:
        _db.close()
        _db_con.close()

    return response_data


def delete_declined_docs(csv_id):
    response_data = None
    _db_con = bulkupload_db_connect()
    _db = Database(_db_con)
    try:
        _db.begin()

        db_stat = _db.get_declined_docs(csv_id)
        if db_stat is not None:
            response_data = db_stat
        _db.commit()
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > delete_declined_docs", str(e)
        )
        logger.logTempFiler(
            "error", "run_tempfile_server > delete_declined_docs",
            str(traceback.format_exc())
        )
        _db.rollback()
        raise RuntimeError(str(e))

    finally:
        _db.close()
        _db_con.close()

    return response_data


@app.route('/knowledgetemp/upload', methods=['POST'])
def upload():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/upload > Request", request
    )
    if request.method == 'POST':
        f = request.files['file']

        session_id = request.args.get('session_id')
        session_output = validate_session(session_id)
        if session_output is False:
            return "invalid session token"
        else:
            csvid = request.args.get("csvid")
            load_path = os.path.join(app.config['UPLOAD_PATH'], csvid)
            if not os.path.exists(load_path):
                os.makedirs(load_path)
                os.chmod(load_path, 0777)

            random_string = generate_random(5)
            fn = f.filename
            fname = fn.split(".")
            random_file_name = fname[0] + '-' + random_string + "." + fname[1]
            actual_file = os.path.join(load_path, f.filename)
            zip_f_name = actual_file + ".zip"
            f.save(zip_f_name)
            zip_ref = zipfile.ZipFile(zip_f_name, 'r')
            zip_ref.extractall(load_path)
            zip_ref.close()
            os.rename(actual_file, load_path + '/' + random_file_name)
            renamed_file = os.path.join(load_path, random_file_name)
            os.remove(zip_f_name)
            renamed_file_size = os.path.getsize(renamed_file)
            if update_file_status(
                f.filename, random_file_name, renamed_file_size, csvid
            ) is False:
                logger.logTempFiler(
                    "info", "run_tempfile_server > /temp/upload",
                    "update file status failed"
                )
                return "update failed"

        return "success"


@app.route('/clienttemp/upload', methods=['POST'])
def upload_client():
    logger.logTempFiler(
        "info", "run_tempfile_server > /client/temp/upload > Request", request
    )
    update_tuples = []
    if request.method == 'POST':
        csvid = request.args.get("csvid")
        load_path = os.path.join(
            app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], csvid
        )
        if not os.path.exists(load_path):
            os.makedirs(load_path)
            os.chmod(load_path, 0777)
        for key, zf in request.files.iteritems():
            actual_file = os.path.join(load_path, zf.filename)
            zip_f_name = actual_file + ".zip"
            zf.save(zip_f_name)
            zip_ref = zipfile.ZipFile(zip_f_name, 'r')
            for f in zip_ref.infolist():
                actual_file = os.path.join(load_path, f.filename)
                random_string = generate_random(5)
                fn = f.filename
                fname = fn.split(".")
                random_file_name = fname[
                    0] + '-' + random_string + "." + fname[1]
                zip_ref.extract(fn, load_path)
                os.rename(actual_file, load_path + '/' + random_file_name)
                renamed_file = os.path.join(load_path, random_file_name)
                renamed_file_size = os.path.getsize(renamed_file)
                update_tuples.append(
                    [fn, random_file_name, renamed_file_size, csvid])
            if update_file_status_client(update_tuples) is False:
                logger.logTempFiler(
                    "info", "run_tempfile_server > /client/temp/upload",
                    "update file status failed"
                )
                return "update failed"
            zip_ref.close()
            os.remove(zip_f_name)
        return "success"


def get_zip_file(folder_name):
    zip_f_name = os.path.join(
        app.config['UPLOAD_PATH'], "%s.zip" % folder_name
    )
    return zip_f_name


def zip_folder(folder_name, folder_path):
    assert folder_name not in zipping_in_process
    zipping_in_process.append(folder_name)
    file_status[folder_name] = "Zipping Started"
    zip_f_name = get_zip_file(folder_name)
    files = glob.glob(os.path.join(folder_path, "*"))
    files = [x for x in files if os.path.isfile(x)]
    with zipfile.ZipFile(zip_f_name, "w", zipfile.ZIP_DEFLATED) as newzip:
        for f in files:
            arcname = f[len(folder_path) + 0:]
            newzip.write(f, arcname)
    if update_file_download_status(folder_name, "completed") is False:
        logger.logTempFiler(
            "info", "run_tempfile_server > zip_folder",
            "download status update failed"
        )
        return "download status update failed"
    zipping_in_process.remove(folder_name)
    file_status[folder_name] = "Zipping Completed"


@app.route('/clienttemp/downloadzip', methods=['POST'])
def get_files_as_zip():
    csv_id = request.args.get("csv_id")
    csv_name = None
    ROOT_PATH = os.path.join(os.path.split(__file__)[0])
    BULK_CSV_PATH = os.path.join(ROOT_PATH, "bulkuploadclientdocuments")
    CSV_PATH = os.path.join(BULK_CSV_PATH, "csv")
    file_path = "%s/%s" % (
        BULK_CSV_PATH, csv_id
    )
    _bulk_db_con = bulkupload_db_connect()
    _bulk_db = Database(_bulk_db_con)
    _bulk_db.begin()
    q = "select csv_name from tbl_bulk_past_data_csv " + \
        " where csv_past_id = %s"
    row = _bulk_db.select_one(q, [csv_id])
    if row:
        csv_name = row["csv_name"]
    zip_file_name = csv_name + "_zip" + ".zip"
    zip_path = os.path.join(BULK_CSV_PATH, zip_file_name)
    zfw = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    csv_absname = os.path.join(CSV_PATH, csv_name)
    csv_arcname = csv_absname[len(CSV_PATH) + 0:]
    zfw.write(csv_absname, csv_arcname)
    for dirname, subdirs, files in os.walk(file_path):
        for file in files:
            absname = os.path.join(dirname, file)
            arcname = absname[
                len(file_path) + 0:
            ]
            zfw.write(absname, arcname)
    zfw.close()
    download_link = "%s/%s" % ("download/zip", zip_file_name)
    url = "%s%s" % (CLIENT_TEMP_FILE_SERVER, download_link)
    return url


@app.route('/temp/approve', methods=['POST'])
def approve():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/approve > Request", request
    )
    csv_id = request.args.get('csvid')
    dec_docs = delete_declined_docs(csv_id)
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    for dd in dec_docs:
        if not os.path.isfile(folder_path + '/' + dd):
            logger.logTempFiler(
                "info", "run_tempfile_server > /temp/approve",
                "Declined File not exists"
            )
            return "File not exists"
        else:
            os.remove(folder_path + '/' + dd)

    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/approve",
            "folder_path not exists"
        )
        return "Error"
    if folder_name in zipping_in_process:
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/approve",
            "Already Started for zipping"
        )
        return "Already Started"
    thread.start_new_thread(zip_folder, (folder_name, folder_path))
    # if update_file_download_status(folder_name, "inprogress") is False:
    #   return "download status update failed"
    return "started zipping"


@app.route('/temp/downloadfile', methods=['GET'])
def downloadfile():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/downloadfile > Request", request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    zip_f_name = get_zip_file(folder_name)
    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/downloadfile",
            "Path not exists for downloading file"
        )
        return "Error"
    if not os.path.isfile(zip_f_name):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/downloadfile",
            "File not found for downloading"
        )
        return "file not found"
    return send_from_directory(
        directory=app.config['UPLOAD_PATH'],
        filename="%s.zip" % (folder_name,)
    )


@app.route('/temp/removefile', methods=['POST'])
def removefile():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/removefile > Request", request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    zip_f_name = get_zip_file(folder_name)
    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/removefile",
            "Path not exists for removing file"
        )
        return "Error"
    if not os.path.isfile(zip_f_name):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/removefile",
            "File not found for removing file"
        )
        return "file not found"
    os.remove(zip_f_name)
    rmtree(folder_path)
    return "removed zip file"


@app.route('/clienttemp/removeclientfile', methods=['POST'])
def removeclientfile():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/removeclientfile > Request",
        request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'],
        folder_name)
    zip_f_name = get_client_zip_file(folder_name)
    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/removeclientfile",
            "Path not exists for removing client file"
        )
        return "Error"
    if not os.path.isfile(zip_f_name):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/removeclientfile",
            "File not found for removing client file"
        )
        return "file not found"
    os.remove(zip_f_name)
    rmtree(folder_path)
    return "removed zip file"


@app.route('/uploadedformat/<csvid>/<filename>', methods=['GET'])
def download_format_file(csvid, filename):
    # folder_name = request.args.get('folder_name')
    logger.logTempFiler(
        "info", "run_tempfile_server > download_format_file > Request", request
    )
    assert csvid is not None
    assert filename is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], csvid)

    return send_from_directory(
        directory=folder_path,
        filename=filename
    )


@app.route('/clienttemp/docsubmit', methods=['POST'])
def approve_client():
    logger.logTempFiler(
        "info", "run_tempfile_server > approve_client > Request", request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], folder_name
    )
    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/docsubmit",
            "Path not exists for docsubmit client"
        )
        return "Error"
    if folder_name in zipping_in_process:
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/docsubmit",
            "Already Started Zipping docsubmit"
        )
        return "Already Started"
    thread.start_new_thread(client_zip_folder, (folder_name, folder_path))
    return "started zipping"


def client_zip_folder(folder_name, folder_path):
    assert folder_name not in zipping_in_process
    zipping_in_process.append(folder_name)
    file_status[folder_name] = "Zipping Started"
    zip_f_name = get_client_zip_file(folder_name)
    files = glob.glob(os.path.join(folder_path, "*"))
    files = [x for x in files if os.path.isfile(x)]
    with zipfile.ZipFile(zip_f_name, "w", zipfile.ZIP_DEFLATED) as newzip:
        for f in files:
            arcname = f[len(folder_path) + 0:]
            newzip.write(f, arcname)
    if update_document_download_status(folder_name, "completed") is False:
        logger.logTempFiler(
            "info", "run_tempfile_server > client_zip_folder",
            "download status update failed"
        )
        return "download status update failed"
    zipping_in_process.remove(folder_name)
    file_status[folder_name] = "Zipping Completed"


def get_client_zip_file(folder_name):
    zip_f_name = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], "%s.zip" % folder_name
    )
    return zip_f_name


@app.route('/clienttemp/downloadclientfile', methods=['GET'])
def download_client_file():
    logger.logTempFiler(
        "info", "run_tempfile_server > download_client_file > Request", request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(
        app.config['CLIENT_DOCUMENT_UPLOAD_PATH'], folder_name)
    zip_f_name = get_client_zip_file(folder_name)

    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/downloadclientfile",
            "Path not exists for downloadclientfile client"
        )
        return "Error"
    if not os.path.isfile(zip_f_name):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/downloadclientfile",
            "File not exists for downloadclientfile client"
        )
        return "file not found"
    return send_from_directory(
        directory=app.config['CLIENT_DOCUMENT_UPLOAD_PATH'],
        filename="%s.zip" % (folder_name,)
    )


@app.route('/temp/removefolders', methods=['POST'])
def remove_rejected_folders():
    logger.logTempFiler(
        "info", "run_tempfile_server > /temp/removefolders > Request", request
    )
    folder_name = request.args.get('csvid')
    assert folder_name is not None
    folder_path = os.path.join(app.config['UPLOAD_PATH'], folder_name)
    if not os.path.exists(folder_path):
        logger.logTempFiler(
            "info", "run_tempfile_server > /temp/removefolders",
            "Path not exists for removing file"
        )
        return "Error"
    rmtree(folder_path)
    return "removed rejected folders"

@app.route('/clienttemp/copycsv', methods=['POST'])
def upload_csv():
    framed_file_name = request.args.get("framed_file_name")
    file_content = request.args.get("file_content")

    ROOT_PATH = os.path.join(os.path.split(__file__)[0])
    BULK_CSV_PATH = os.path.join(ROOT_PATH, "bulkuploadclientdocuments")
    file_path = "%s/csv" % (
        BULK_CSV_PATH
    )
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    create_path = "%s/%s" % (file_path, framed_file_name)
    try:
        with io.FileIO(create_path, "wb") as fn:
            fn.write(file_content.decode('base64'))
        return "True"
    except IOError, e:
        print e
    return "success"

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
    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > parse_port()", str(e)
        )
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

    except Exception, e:
        logger.logTempFiler(
            "error", "run_tempfile_server > parse_ip_address()", str(e)
        )
        return None

    assert ip is not None
    assert port is not None
    return ip, port


def staticTemplate(pathname, filename):
    return send_from_directory(pathname, filename)


def main():
    args = args_parser.parse_args()

    port = parse_port(args.port)
    if port is None:
        msg = "error: port is not in PORT format: %s"
        logger.logTempFiler(
            "error", "run_tempfile_server > main()", msg % (args.port,)
        )
        return
    ROOT_PATH = os.path.join(os.path.split(__file__)[0])
    BULK_CSV_UPLOAD_PATH_CSV = os.path.join(
        ROOT_PATH, "bulkuploadclientdocuments"
    )
    STATIC_PATHS = [
        ("/download/zip/<path:filename>", BULK_CSV_UPLOAD_PATH_CSV)
    ]
    for path in STATIC_PATHS:
        app.add_url_rule(
            path[0], view_func=staticTemplate, methods=['GET'],
            defaults={'pathname': path[1]}
        )

    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)


if __name__ == "__main__":
    main()
