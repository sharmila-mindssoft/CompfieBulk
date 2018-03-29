import os
from server.constants import (
    CSV_DELIMITER, REJECTED_DOWNLOAD_PATH, REJECTED_DOWNLOAD_BASE_PATH
)
from ..bulkuploadcommon import (
    rename_download_file_type, write_download_data_to_excel
)

__all__ = [
    "ValidateRejectedDownloadBulkData"
]

###################################################################
# ValidateRejectedDownloadBulkData is a common class to generate and download
# - Rejected Reports
# format files
###################################################################


class ValidateRejectedDownloadBulkData():
    def __init__(self, db, source_data, session_user, download_format,
                 csv_name, csv_header, csv_column_name, sheet_name):
        self._source_data = source_data
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._csv_column_name = csv_column_name
        self._sheet_name = sheet_name

    ###################################################################
    # Validate the Source Data
    ###################################################################
    def perform_validation(self):
        mapped_header_dict = {}
        is_return = False
        sno = 0
        for row_idx, data in enumerate(self._source_data):
            sno = sno + 1
            for key in self._csv_header:
                v_col_key = data.get(key)

                if (key == "remarks" and v_col_key is not None):
                    split_key_value = v_col_key.strip().split(CSV_DELIMITER)

                    for summary_row_title in split_key_value:
                        row_value = summary_row_title.strip().split(' - ')

                        if(row_value[1] != ""):
                            summary_key = row_value[0].lower()
                            summary_key = summary_key.replace(" ", "_")
                            e_count = mapped_header_dict[summary_key]

                            if(int(e_count) >= 1):
                                e_count = e_count + 1
                                mapped_header_dict[summary_key] = int(e_count)
                                is_return = True
                            else:
                                mapped_header_dict[summary_key] = int(1)
                                is_return = True
                elif(key == "remarks" and v_col_key is None):
                    is_return = True
                elif(key is "is_fully_rejected" or key is "rejected_reason"):
                    mapped_header_dict[key] = ''
                    is_return = True
                else:
                    if(sno == 1):
                        mapped_header_dict[key] = 0
        if is_return is True:
            is_return = False
            return self.generateDownloadFiles(mapped_header_dict)

    ######################################################
    # Generate Download file formats XLSX, CSV, TXT, ODS
    ######################################################

    def generateDownloadFiles(self, mapped_header_dict):
        fileString = self._csv_name.split('.')
        file_name = "%s_%s.%s" % (
            fileString[0], "download", "xlsx"
        )
        final_hearder = self._csv_header
        final_header_column = self._csv_column_name
        write_download_data_to_excel(
            os.path.join(REJECTED_DOWNLOAD_PATH, "xlsx"), file_name,
            final_hearder, final_header_column, self._source_data,
            mapped_header_dict, self._sheet_name
        )

        xlsx_download_path = REJECTED_DOWNLOAD_BASE_PATH + "xlsx/"
        xlsx_link = os.path.join(xlsx_download_path, file_name)

        csv_link = rename_download_file_type(file_name, "csv")

        ods_link = rename_download_file_type(file_name, "ods")

        txt_link = rename_download_file_type(file_name, "txt")
        return {
            "xlsx_link": xlsx_link,
            "csv_link": csv_link,
            "ods_link": ods_link,
            "txt_link": txt_link
        }
