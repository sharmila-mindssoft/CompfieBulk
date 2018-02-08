
import os
import io
import uuid
import xlsxwriter
import shutil

from server.constants import(BULKUPLOAD_INVALID_PATH)
#   returns: unique random string
def new_uuid():
        s = str(uuid.uuid4())
        return s.replace("-", "")


#    remove the already exists file.
def remove_uploaded_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


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

def convert_base64_to_file(src_path, file_name, file_content):
    framed_file_name = file_name + "_" + new_uuid()

    file_path = "%s/%s" % (src_path, framed_file_name)

    if os.path.exists(file_path):
        framed_file_name = file_name + "_" + new_uuid()

    if not os.path.exists(file_path):
        os.makedirs(file_path)
        os.chmod(file_path, 0777)
    file_path = "%s/%s" % (file_path, framed_file_name)

    if file_content is not None:
        with io.FileIO(file_path, "wb") as fn:
            fn.write(file_content.decode('base64'))

    return framed_file_name

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

def read_data_from_csv(file_name_in_full_path):
    mapped_data = []
    headerrow = []
    if os.path.exists(file_name_in_full_path):
        with io.FileIO(file_name_in_full_path, "rb") as fn :
            rows = fn.readlines()

            for idx, r in enumerate(rows) :
                if idx == 0 :
                    headerrow = r
                else :
                    data = {}
                    for cdx, c in enumerate(r) :
                        data[headerrow[cdx]] = c
                    mapped_data.append(data)
    return headerrow, mapped_data


def write_data_to_excel(
    file_src_path, file_name, headers, column_data,
    data_error_dict, header_dict, sheet_name
):
    file_path = os.path.join(file_src_path, file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.set_column('A:A', 30)
    bold = workbook.add_format({'bold': 1})
    error_format = workbook.add_format({
        'font_color': 'red'
    })
    cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for idx, h in enumerate(headers):
        if idx < 26 :
            x = idx
        else :
            x = idx - 26

        c = "%s%s" % (cells[x], 1)
        worksheet.write(c, h, bold)

    row = 1
    col = 0

    for idx, dat in enumerate(column_data):
        error_col = header_dict.get(idx)
        for i, d in enumerate(dat[:-1]):
            if error_col is not None :
                if i in error_col :
                    worksheet.write_string(row, col+i, d, error_format)
            else :
                worksheet.write_string(row, col+i, d)
        row += 1

    # summary sheet
    summarySheet = workbook.add_worksheet("summary")
    for idx, h in enumerate(["Field Name", "Count"]):
        c = "%s%s" % (cells[idx], 1)
        summarySheet.write(c)

    srow = 1
    for i, col in headers :

        value = 0
        error_count = header_dict.get(i)
        if error_count is not None :
            value = len(error_count)
        summarySheet.write_string(srow, 0, col)
        summarySheet.write_string(srow, 0, value)
        srow += 1

def rename_file_type(file_name, des_file_type):
    src_path = os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx")
    str_split = file_name.split('.')
    new_file = str_split[0] + "." + des_file_type

    dst_dir = os.path.join(BULKUPLOAD_INVALID_PATH, des_file_type)
    src_file = os.path.join(src_path, file_name)
    shutil.copy(src_file, dst_dir)

    dst_file = os.path.join(dst_dir, file_name)

    new_dst_file_name = os.path.join(dst_dir, new_file)
    os.rename(dst_file, new_dst_file_name)
