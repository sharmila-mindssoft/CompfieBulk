
import re
import datetime

__all__ = [
    "csv_params", "parse_csv_dictionary_values"
]

def expectation_error(expected, received):
    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, str(received)))


def allow_specialchar(value):
    r = re.compile("^[0-9a-zA-Z- _& ,.;:/+=$%@#&*()<>?:\n]*$")
    if r.match(value):
        return True
    else :
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
    r = re.compile("^[0-9a-zA-Z&@,-.>>| ]*$")
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

def is_valid_statutory_date_input(value, irange):
    flag = True
    if value != "" :
        if only_numeric(int(value)) :
            if int(value) > irange:
                flag = False
        else :
            flag = False
    return flag

def statutory_month(value):
    return is_valid_statutory_date_input(value, 12)

def statutory_date(value):
    return is_valid_statutory_date_input(value, 31)

def trigger_days(value):
    return is_valid_statutory_date_input(value, 100)

def duration_and_repeats(value):
    flag = True
    if only_numeric(value):
        if int(value) > 999 :
            flag = False
    else :
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

def is_date(string):
    string_in_date = string
    try:
        if string is not None:
            if string_in_date != datetime.datetime.strptime(string_in_date, "%d-%b-%Y").strftime('%d-%b-%Y'):
                raise ValueError
            return True
    except ValueError:
        return False

def is_url(value):
    r = re.compile("^[a-zA-Z0-9=/:.-]*$")  # a-z with special char
    if r.match(value):
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
        raise False

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

def parse_csv_dictionary_values(key, val):
    error_count = {
        "mandatory": 0,
        "max_length": 0,
        "invalid_char": 0,
        "invalid_date": 0
    }
    csvparam = csv_params.get(key)

    if csvparam is None:
        raise ValueError('%s is not configured in csv parameter' % (key))

    _mandatory = csvparam.get("check_mandatory")
    _maxlength = csvparam.get("max_length")

    _validation_method = csvparam.get("validation_method")

    msg = []
    if _mandatory is True and (len(val) == 0 or val == '') :
        msg.append(key + " - Field is blank")
        error_count["mandatory"] = 1

    if _maxlength is not None and len(val) > _maxlength :
        msg.append(key + " - Cannot exceed max length")
        error_count["max_length"] = 1

    if _validation_method is not None :
        if _validation_method(val) is False:
            if key == "Due_Date" or key == "Completion_Date" :
                msg.append(key + " - Invalid Date Format")
                error_count["invalid_date"] = 1
            else :
                msg.append(key + " - Invalid character")
                error_count["invalid_char"] = 1
    if len(msg) == 0 :
        return True, error_count
    else :
        return msg, error_count

########################################################
'''
    frame the validation constraints based on the given param
    :param

        keyType: type of key name
        isMandatoryCheck=False: to enable mandatory validation value has to be True,
            otherwise it will not validate
        maxLengthCheck=None: to enable max length validation value should not be None
        isValidCharCheck=False: to enable character validation value should be True
        validation_method=None: corresponding validation will done if the isValidCharCheck is True
        isFoundCheck=False: to check data already found given value should be True
        isActiveCheck=False: to check data status given value shoould be True

        if the param boolean value False means it will skip the corresponding validation
        maxlength param is not meant for INT type if the value not None means that will check maximum given value not length

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
    isMandatoryCheck=False, maxLengthCheck=None, isValidCharCheck=False, validation_method=None,
    isFoundCheck=False, isActiveCheck=False
):
    constraints = {
        'key_type': keyType
    }

    if isMandatoryCheck is True :
        constraints["check_mandatory"] = True

    if maxLengthCheck is not None :
        constraints["max_length"] = maxLengthCheck

    if isValidCharCheck is not False and validation_method is not None:
        constraints["validation_method"] = validation_method

    if isFoundCheck is not False :
        constraints["check_is_exists"] = True

    if isActiveCheck is not False :
        constraints["check_is_active"] = True

    return constraints


# key name should be as it is in csv file

csv_params = {
    'Legal_Entity': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True, isActiveCheck=True
    ),
    'Domain': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=30, isValidCharCheck=True,
        validation_method=is_domain, isFoundCheck=True, isActiveCheck=True
    ),
    'Unit_Code': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=20, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Unit_Name': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=50, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Compliance_Frequency': make_required_validation(
        keyType='STRING', isValidCharCheck=True,
        validation_method=is_alphabet, isFoundCheck=True
    ),
    'Primary_Legislation': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Secondary_Legislation': make_required_validation(
        keyType='STRING', maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Compliance_Task': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=100, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Compliance_Description': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, maxLengthCheck=500, isValidCharCheck=True,
        validation_method=is_alpha_numeric, isFoundCheck=True
    ),
    'Statutory_Date': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=False
    ),
    'Due_Date': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=True, validation_method=is_date
    ),
    'Assignee': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=False, isFoundCheck=True
    ),
    'Completion_Date': make_required_validation(
        keyType='STRING', isMandatoryCheck=True, isValidCharCheck=True, validation_method=is_date
    ),
    'Document_Name': make_required_validation(
        keyType='STRING', isValidCharCheck=False
    ),
    #  isMandatoryCheck=False, maxLengthCheck=None, isValidCharCheck=False, validation_method=None,
    # isFoundCheck=False, isActiveCheck=False
}
