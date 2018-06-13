import io
import os
import uuid
import csv
import requests
import xlsxwriter
import pyexcel
from datetime import datetime

from bulkupload.client_bulkconstants import (
    BULKUPLOAD_INVALID_PATH, BULKUPLOAD_CSV_PATH, REJECTED_DOWNLOAD_PATH,
    REJECTED_DOWNLOAD_BASE_PATH, CLIENT_DOCS_BASE_PATH, LOCAL_TIMEZONE,
    string_months, TEMP_FILE_SERVER
)


#   returns: unique random string
def new_uuid():
        s = str(uuid.uuid4())
        return s.replace("-", "")


#    remove the already exists file.
def remove_uploaded_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def frame_file_name(file_name):
    return "%s_%s.csv" % (
        file_name, new_uuid()
    )


def localize(time_stamp):
    local_dt = LOCAL_TIMEZONE.localize(
        time_stamp
    )
    tzoffseet = local_dt.utcoffset()
    local_dt = local_dt.replace(tzinfo=None)
    local_dt = local_dt + tzoffseet
    return local_dt


def string_to_datetime(string):
    string_in_date = string
    if string is not None:
        string_in_date = datetime.strptime(string, "%d-%b-%Y")
    return localize(string_in_date)


########################################################
'''
   convert base64 data into csv file
    :param
        src_path: file source path location
        file_name: actual file name
        file_content: data in base64 format
    :type
        src_path: String
        file_name: string
        file_content: base64
    :returns
        result: framed_file_name is actual file name with unique string
    rtype:
        result: string
'''
########################################################


def convert_base64_to_file(
    src_path, file_name, file_content
):
    fileSplitString = file_name.split(".")
    framed_file_name = frame_file_name(fileSplitString[0])
    file_folder_path = "%s/csv/" % (src_path)
    file_path = "%s/csv/%s" % (src_path, framed_file_name)

    if not os.path.exists(file_folder_path):
        os.makedirs(file_folder_path)
    with open(file_path, "wb") as fn:
        fn.write(file_content.decode("base64"))
    return framed_file_name


def save_file_in_client_docs(
    src_path, file_name, file_content
):
    caller_name = (
        "%sclient/copycsv?framed_file_name=%s&file_content=%s"
    ) % (
        TEMP_FILE_SERVER, file_name, file_content
    )
    response = requests.post(caller_name)
    return response

########################################################
'''
   read data from csv file and save into dictionary
    :param
        file_name_in_full_path: actual file location
    :type
        file_name_in_full_path: string
    :returns
        mapped_data:  return dictionary
    rtype:
        result: string
'''
########################################################


def read_data_from_csv(file_name):
    mapped_data = []
    headerrow = []
    csv_path = os.path.join(BULKUPLOAD_CSV_PATH, "csv")
    file_path = os.path.join(csv_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fn:
            rows = csv.reader(
                fn, quotechar='"', delimiter=",",
                quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            for idx, r in enumerate(rows):
                if idx == 0:
                    for c in r:
                        c = c.replace("*", "")
                        headerrow.append(c.strip())
                else:
                    data = {}
                    for cdx, c in enumerate(r):
                        val = c.strip()
                        data[headerrow[cdx]] = val
                    mapped_data.append(data)
    return headerrow, mapped_data


def write_data_to_excel(
    file_src_path, file_name, headers, column_data,
    data_error_dict, header_dict, sheet_name
):
    if not os.path.exists(file_src_path):
        os.makedirs(file_src_path)
    file_path = os.path.join(file_src_path, file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.set_column("A:A", 30)
    bold = workbook.add_format({"bold": 1})
    error_format = workbook.add_format({
        "font_color": "red"
    })
    cells = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
        "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
        "Y", "Z"]
    for idx, h in enumerate(headers):
        if idx < 26:
            x = idx
        else:
            x = idx - 26

        c = "%s%s" % (cells[x], 1)
        worksheet.write(c, h, bold)

    row = 1
    col = 0

    for idx, dat in enumerate(column_data):

        for i, h in enumerate(headers):
            error_col = header_dict.get(h)
            d = str(dat.get(h))
            if h == "Error Description":
                error_text = data_error_dict.get(idx)
                if error_text is None:
                    e = ""
                else:
                    e = "|;|".join(error_text)
                worksheet.write_string(row, col + i, e)
            else:
                if error_col is not None:
                    if idx in error_col:
                        worksheet.write_string(
                            row, col + i, d, error_format)
                    else:
                        worksheet.write_string(row, col + i, d)
                else:
                        worksheet.write_string(row, col + i, d)
        row += 1

    # summary sheet
    summarySheet = workbook.add_worksheet("summary")
    for idx, h in enumerate(["Field Name", "Count"]):
        c = "%s%s" % (cells[idx], 1)
        summarySheet.write(c, h, bold)

    srow = 1
    for i, col in enumerate(headers):
        value = 0
        error_count = header_dict.get(col)
        if error_count is not None:
            value = len(error_count)
        summarySheet.write_string(srow, 0, col)
        summarySheet.write_string(srow, 1, str(value))
        srow += 1

    # workbook.close()


def rename_file_type(src_file_name, des_file_type):
    src_path = os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx")
    str_split = src_file_name.split(".")
    new_file = str_split[0] + "." + des_file_type

    dst_dir = os.path.join(BULKUPLOAD_INVALID_PATH, des_file_type)
    src_file = os.path.join(src_path, src_file_name)

    new_dst_file_name = os.path.join(dst_dir, new_file)
    if des_file_type == "txt":
        general_txt_file(src_file, new_dst_file_name)
    else:
        pyexcel.save_as(
            file_name=src_file, dest_file_name=new_dst_file_name
        )


def general_txt_file(src_file, dst_txt_file_name):
    src_file = src_file.replace("xlsx", "csv")
    with open(dst_txt_file_name, "w") as my_output_file:
        with open(src_file, "r") as my_input_file:
            for row in csv.reader(my_input_file):
                my_output_file.write(" ".join(row) + "\n")


def generate_valid_file(src_file_name):
    f_types = ["xlsx", "ods"]
    for f in f_types:
        src_path = os.path.join(BULKUPLOAD_CSV_PATH, "csv")
        str_split = src_file_name.split(".")
        new_file = str_split[0] + "." + f

        dst_dir = os.path.join(BULKUPLOAD_CSV_PATH, f)
        src_file = os.path.join(src_path, src_file_name)

        new_dst_file_name = os.path.join(dst_dir, new_file)
        pyexcel.save_as(file_name=src_file, dest_file_name=new_dst_file_name)


def rename_download_file_type(src_file_name, des_file_type):
    src_path = os.path.join(REJECTED_DOWNLOAD_PATH, "xlsx")

    str_split = src_file_name.split(".")
    new_file = str_split[0] + "." + des_file_type

    dst_dir = os.path.join(REJECTED_DOWNLOAD_PATH, des_file_type)
    src_file = os.path.join(src_path, src_file_name)

    new_dst_file_name = os.path.join(dst_dir, new_file)
    pyexcel.save_as(file_name=src_file, dest_file_name=new_dst_file_name)

    download_path_link = os.path.join(
        REJECTED_DOWNLOAD_BASE_PATH, des_file_type, new_file
    )
    return download_path_link
