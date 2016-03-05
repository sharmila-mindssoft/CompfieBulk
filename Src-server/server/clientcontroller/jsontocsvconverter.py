import os
import json
import csv
import uuid

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
FILE_DOWNLOAD_PATH = "/download/csv"

class ConvertJsonToCSV(object):

    def __init__(self, jsonObj):
        self.reduced_item = {}
        self.header = []
        self.format = {}
        self.initializeFormatStrings()
        s = str(uuid.uuid4())
        file_name = "%s.csv" % s.replace("-", "")
        self.CSV_PATH = "%s/exported_reports" % ROOT_PATH
        self.FILE_PATH = "%s/%s" % (FILE_DOWNLOAD_PATH, file_name)
        if not os.path.exists(self.CSV_PATH):
            os.makedirs(self.CSV_PATH)
        with open(file_name, 'wb+') as f:
            self.writer = csv.writer(f)#self.header, quoting=csv.QUOTE_ALL) 
            self.convert_json_to_csv(jsonObj)

    def to_string(self, s):
        try:
            return str(s)
        except:
            return s.encode('utf-8')

    def write_csv(self, header, values=None):
        if self.header != header:
            self.writer.writerow(header)
            if values:   
                self.header = header
        if values:
            self.writer.writerow(values)
            

    def separate_values_and_objects(self, key, item):
        sub_header = []
        original_sub_header = []
        sub_values = {}
        main_header = []
        main_values = []
        for key in item:
            if (type(item[key]) is list) or (type(item[key]) is dict):
                try:
                    sub_header.append(self.format[key])
                except Exception, ex:
                    sub_header.append(key)
                original_sub_header.append(key)
            else:
                main_header.append(self.format[key])
                main_values.append(item[key])
        print "sub_header:{}".format(sub_header)
        print "main_header:{}".format(main_header)
        print "main_values:{}".format(main_values)
        self.write_csv(main_header, main_values)
        self.write_csv(sub_header)
        for header in original_sub_header:
            self.check_and_parse(header, item[header], item)

    def check_and_parse(self, key, item, items):
        if type(item) is list:
            self.parse_list(key, item)
        elif type(item) is dict:
            self.separate_values_and_objects(key, item)
        else:
            header = [key]
            values = items
            self.write_csv(header, values)

    def parse_dict(self, item):
        for key in item:
            self.check_and_parse(key, item[key], item)

    def parse_list(self, key, items):
        for item in items:
            print "inside parse list : key: {}".format(key)
            self.check_and_parse(key, item, items)

    def convert_json_to_csv(self, jsonObj):
        for key in jsonObj:
            self.check_and_parse(key, jsonObj[key], jsonObj)
        # print "Just completed writing csv file"

    def initializeFormatStrings(self):
        self.format["unit_name"] = "Unit Name"
        self.format["address"] = "Address"
        self.format["remarks"] = "Remarks"
        self.format["activity_date"] = "Activity Date"
        self.format["compliance_status"] = "Compliance Status"
        self.format["activity_status"] = "Activity Status"
        self.format["statutory_wise_compliances"] = "Statutory Wise Compliances"