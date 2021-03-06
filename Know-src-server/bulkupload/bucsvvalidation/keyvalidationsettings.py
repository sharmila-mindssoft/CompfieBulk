
import re

__all__ = [
    "csv_params", "parse_csv_dictionary_values",
    "parse_csv_dictionary_values_as", "csv_params_as", "is_numeric"
]


def expectation_error(expected, received):

    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, str(received)))


def allow_specialchar(value):

    r = re.compile("^[0-9a-zA-Z- _& ,.;:/+=$%@#&*()<>?:\n]*$")
    if r.match(value):
        return True
    else:
        return False


def is_alphabet(value):

    r = re.compile("^[a-zA-Z ]*$")  # a-z with space
    if r.match(value):
        return True
    else:
        return False


def is_applicable_location(value):

    r = re.compile("^[a-zA-Z>>| ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_statutory(value):

    r = re.compile("^[0-9a-zA-Z&@,-.>>|()_ ]*$")
    if r.match(value):
        return True
    else:
        return False


def only_numeric(value):

    r = re.compile("^[0-9]*$")
    if r.match(str(value)):
        return True
    else:
        return False


def is_numeric(value):

    r = re.compile("^[0-9 ]*$")  # 0-9 with space
    if r.match(str(value)):
        return True
    else:
        return False


def is_numeric_with_delimiter(value):

    r = re.compile("^[0-9|;| ]*$")  # 0-9 with |;|
    if r.match(str(value)):
        return True
    else:
        return False


def is_valid_statutory_month_input(value, irange):

    flag = True
    if value != "":
        if only_numeric(value):
            if int(value) == 0:
                flag = False
            elif int(value) > irange:
                flag = "%s should be between 1 - %s" % (value, irange)
        else:
            flag = False
    return flag


def is_valid_statutory_date_input(value, irange):

    flag = True
    if value != "":
        if only_numeric(value):
            if int(value) == 0:
                flag = False

            elif int(value) > irange:
                flag = "%s cannot exceed %s" % (value, irange)
        else:
            flag = False
    return flag


def statutory_month(value):

    return is_valid_statutory_month_input(value, 12)


def statutory_date(value):

    return is_valid_statutory_date_input(value, 31)


def trigger_days(value):

    return is_valid_statutory_date_input(value, 100)


def duration_and_repeats(value):

    flag = True
    if value != "":
        if only_numeric(value):
            if int(value) == 0:
                flag = False
            # elif int(value) > 999:
            #     flag = "cannot exceed maxlength 999"
        else:
            flag = False
    return flag


def duration_and_repeats_type(value):

    r = re.compile("^[a-zA-Z() ]*$")
    if r.match(value):
        return True
    else:
        return False


def repeats_by(value):

    if value in ["DOM", "EOM"]:
        return True
    else:
        return False


def multiple_input_selection(value):

    if value in ["Yes", "No"]:
        return True
    else:
        return False


def is_alpha_numeric(value):

    #    a-z and 0-9 with space
    r = re.compile("^[A-Za-z0-9-_.,@ ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_url(value):

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    if regex.search(value):
        return True
    else:
        return False


def is_address(value):

    # a-z0-9 with special char and space
    r = re.compile("^[a-zA-Z0-9_.,-@# ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_alphabet_withdot(value):

    r = re.compile("^[a-zA-Z-. ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_domain(value):

    # a-z0-9 with special char and space with delimiter
    r = re.compile("^[a-zA-Z0-9|;| ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_domain_orgn(value):

    # a-z0-9 with special char and space with delimiter
    r = re.compile("^[a-zA-Z0-9|;|>> ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_postal_code(value):

    # a-z0-9 with special char and space with delimiter
    r = re.compile("^[a-zA-Z0-9 ]*$")
    if r.match(value):
        return True
    else:
        return False


def is_unit_code(value):
    r = re.compile("^[a-zA-Z0-9_ ]*$")
    if r.match(value):
        return True
    else:
        return False


def parse_csv_dictionary_values(key, val):

    error_count = {
        "mandatory": 0,
        "max_length": 0,
        "invalid_char": 0
    }
    csvparam = csv_params.get(key)

    if csvparam is None:
        raise ValueError('%s is not configured in csv parameter' % (key))

    _mandatory = csvparam.get("check_mandatory")
    _maxlength = csvparam.get("max_length")
    _validation_method = csvparam.get("validation_method")

    msg = []
    if _mandatory is True and (len(val) == 0 or val == ''):
        msg.append(key + " - Field is blank")
        error_count["mandatory"] = 1

    if _maxlength is not None and len(val) > _maxlength:
        msg.append(key + " - " + val + " Cannot exceed max length")
        error_count["max_length"] = 1

    if val != "":
        if _validation_method is not None:
            _result = _validation_method(val)

            if _result is False:
                msg.append(key + " - " + val + " Invalid character")
                error_count["invalid_char"] = 1

            elif _result is not True:
                msg.append("%s - %s" % (key, _result))
                error_count["max_length"] += 1

    if len(msg) == 0:
        return True, error_count
    else:
        return msg, error_count


def parse_csv_dictionary_values_as(key, val):

    error_count = {
        "mandatory": 0,
        "max_length": 0,
        "invalid_char": 0
    }
    csvparam = csv_params_as.get(key)

    if csvparam is None:
        raise ValueError('%s is not configured in csv parameter' % (key))

    _mandatory = csvparam.get("check_mandatory")
    _maxlength = csvparam.get("max_length")

    _validation_method = csvparam.get("validation_method")

    msg = []
    if _mandatory is True and (len(val) == 0 or val == ''):
        msg.append(key + " - Field is blank")
        error_count["mandatory"] = 1

    if _maxlength is not None and len(val) > _maxlength:
        msg.append(key + " - Cannot exceed max length")
        error_count["max_length"] = 1

    if _validation_method is not None:
        if _validation_method(val) is False:
            msg.append(key + " - Invalid character")
            error_count["invalid_char"] = 1
    if len(msg) == 0:
        return True, error_count
    else:
        return msg, error_count

########################################################
'''
    frame the validation constraints based on the given param
   :param

        keyType: type of key name
        isMandatoryCheck=False: to enable mandatory validation value
            has to be True,
            otherwise it will not validate
        maxLengthCheck=None: to enable max length validation value
            should not be None
        isValidCharCheck=False: to enable character validation
            value should be True
        validation_method=None: corresponding validation will
            be done if the isValidCharCheck is True
        isFoundCheck=False: to check data already found
            given value should be True
        isActiveCheck=False: to check data status given value shoould be True

        if the param boolean value False means it will
        skip the corresponding validation
        maxlength param is not meant for INT type if the value not None
        means that will check maximum given value not length

   :type
        keyName: string
        keyType: type could be Int, String, Boolean, Float
        isMandatoryCheck: Boolean
        maxLengthCheck: None or Int
        isValidCharCheck: Boolean
        validation_method: None or method name
        isFoundCheck: Boolean
        isActiveCheck: Boolean

   :returns
        result: formulated dictionary
    rtype:
        result: dictionary
'''
########################################################


def make_required_validation(
    keyType,
    isMandatoryCheck=False, maxLengthCheck=None, isValidCharCheck=False,
    validation_method=None,
    isFoundCheck=False, isActiveCheck=False
):

    constraints = {
        'key_type': keyType
    }

    if isMandatoryCheck is True:
        constraints["check_mandatory"] = True

    if maxLengthCheck is not None:
        constraints["max_length"] = maxLengthCheck

    if isValidCharCheck is not False and validation_method is not None:
        constraints["validation_method"] = validation_method

    if isFoundCheck is not False:
        constraints["check_is_exists"] = True

    if isActiveCheck is not False:
        constraints["check_is_active"] = True

    return constraints


# key name should be as it is in csv file

csv_params = {
    'Organization': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True,
        validation_method=is_domain_orgn, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Applicable_Location': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=True,
        validation_method=is_applicable_location, isFoundCheck=True,
        isActiveCheck=True, maxLengthCheck=500
    ),
    'Statutory_Nature': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True,
        validation_method=is_alphabet, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Statutory': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=100,
        isValidCharCheck=True,
        validation_method=is_statutory, isFoundCheck=True, isActiveCheck=True
    ),

    'Statutory_Provision': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),

    'Compliance_Task': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=100,
        isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'Compliance_Document': make_required_validation(
        keyType='STRING', maxLengthCheck=100, isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'Task_ID': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=25,
        isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'Compliance_Description': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'Penal_Consequences': make_required_validation(
        keyType='STRING', maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'Task_Type': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=150,
        isValidCharCheck=True,
        validation_method=is_alphabet, isFoundCheck=True
    ),
    'Reference_Link': make_required_validation(
        keyType='STRING', maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_url
    ),
    'Compliance_Frequency': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=20,
        isValidCharCheck=True,
        validation_method=is_alphabet, isFoundCheck=True
    ),
    'Statutory_Month': make_required_validation(
        keyType='STRING', isValidCharCheck=True,
        validation_method=statutory_month
    ),
    'Statutory_Date': make_required_validation(
        keyType='STRING', isValidCharCheck=True,
        validation_method=statutory_date
    ),
    'Trigger_Days': make_required_validation(
        keyType='STRING', isValidCharCheck=True,
        validation_method=trigger_days
    ),
    'Repeats_Every': make_required_validation(
        keyType='INT', isValidCharCheck=True,
        validation_method=duration_and_repeats
    ),

    'Repeats_Type': make_required_validation(
        keyType='STRING', maxLengthCheck=20, isValidCharCheck=True,
        validation_method=duration_and_repeats_type,
        isFoundCheck=True
    ),
    'Repeats_By (DOM/EOM)': make_required_validation(
        keyType='STRING', isValidCharCheck=True, validation_method=repeats_by
    ),
    'Duration': make_required_validation(
        keyType='INT', isValidCharCheck=True,
        validation_method=duration_and_repeats
    ),
    'Duration_Type': make_required_validation(
        keyType='STRING', maxLengthCheck=20, isValidCharCheck=True,
        validation_method=duration_and_repeats_type,
        isFoundCheck=True
    ),
    'Multiple_Input_Section': make_required_validation(
        keyType='STRING', isValidCharCheck=True,
        validation_method=multiple_input_selection,
        isFoundCheck=True
    ),
    'Format': make_required_validation(
        keyType='STRING', maxLengthCheck=150, isValidCharCheck=True,
        validation_method=is_alpha_numeric,
    ),
    'Legal_Entity': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Division': make_required_validation(
        keyType='STRING', maxLengthCheck=50, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Category': make_required_validation(
        keyType='STRING', maxLengthCheck=50, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Geography_Level': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True,
        validation_method=is_address, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Unit_Location': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True, validation_method=is_statutory,
        isFoundCheck=True, isActiveCheck=True
    ),
    'Unit_Code': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=20,
        isValidCharCheck=True, validation_method=is_unit_code,
        isFoundCheck=True
    ),
    'Unit_Name': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'Unit_Address': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=250,
        isValidCharCheck=True, validation_method=is_address
    ),
    'City': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=20,
        isValidCharCheck=True, validation_method=is_alphabet_withdot
    ),
    'State': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=20,
        isValidCharCheck=True, validation_method=is_alphabet_withdot
    ),
    'Postal_Code': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=6,
        isValidCharCheck=True, validation_method=is_postal_code
    ),
    'Domain': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=30,
        isValidCharCheck=True, validation_method=is_domain,
        isFoundCheck=True, isActiveCheck=True
    ),
    'Statutory_Applicable_Status': make_required_validation(
        keyType='INT', isMandatoryCheck=True, isValidCharCheck=True,
        validation_method=is_numeric
    ),
    'Compliance_Applicable_Status': make_required_validation(
        keyType='INT', isMandatoryCheck=True, isValidCharCheck=True,
        validation_method=is_numeric
    ),
    'Statutory_remarks': make_required_validation(
        keyType='STRING', maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric
    ),
    'S.No': make_required_validation(
        keyType='INT', isValidCharCheck=True, validation_method=is_numeric
    ),
    'Primary_Legislation': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'Secondary_Legislaion': make_required_validation(
        keyType='STRING', maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Client_Group': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=True,
        validation_method=is_alphabet, isFoundCheck=True
    ),
    'Organisation': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50,
        isValidCharCheck=True, validation_method=is_alphabet,
        isFoundCheck=True, isActiveCheck=True
    ),
    'csv_name': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'uploaded_by': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'uploaded_on': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'total_records': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'total_rejected_records': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'approved_by': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'rejected_by': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'approved_on': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),

    'rejected_on': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'is_fully_rejected': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'approve_status': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'Statutory_Provision_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Compliance_Task_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Compliance_Description_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Unit_Name_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Primary_Legislation_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Statutory_Applicable_Status_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Compliance_Applicable_Status_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Unit_Location_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Unit_Code_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Organisation_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Domain_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Legal_Entity_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Client_Group_Column': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
}


csv_params_as = {
    'Statutory_remarks': make_required_validation(
        keyType='STRING', maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'Statutory_remarks_': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500,
        isValidCharCheck=True, validation_method=is_alpha_numeric
    ),
    'S.No': make_required_validation(
        keyType='INT', isValidCharCheck=True, validation_method=is_numeric
    ),
    'Secondary_Legislation': make_required_validation(
        keyType='STRING', isFoundCheck=True
    ),
    'Statutory_Provision': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Compliance_Task': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Compliance_Description': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Unit_Name': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Primary_Legislation': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Statutory_Applicable_Status': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Compliance_Applicable_Status': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Unit_Location': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Unit_Code': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Organization': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Domain': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Legal_Entity': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True,
        isActiveCheck=True
    ),
    'Client_Group': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
    'Country': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isFoundCheck=True
    ),
}
