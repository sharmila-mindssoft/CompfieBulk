
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
    else:
        return False


def is_alpha_numeric_allow_spl(value):
    r = re.compile("^[0-9A-Za-z_.,-@#&*() ]*$")
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
    if value != "":
        if only_numeric(int(value)):
            if int(value) > irange:
                flag = False
        else:
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
        if int(value) > 999:
            flag = False
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


def is_alpha_numeric_with_brace(value):
    val = value.replace("(", "")
    val1 = val.replace(")", "")
    return is_alpha_numeric(val1)


def check_document_name(value):
    # alphanumeric with space, hyphen, dot and underscore
    val = value.replace("-", "").replace(".", "").replace("_", "")
    return is_alpha_numeric(val)


def is_date(string):
    string_in_date = string
    try:
        if string is not None:
            if string != datetime.datetime.strptime(
                string_in_date, "%d-%b-%Y"
            ).strftime("%d-%b-%Y"):
                raise ValueError
            else:
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
        raise ValueError("%s is not configured in csv parameter" % key)

    _mandatory = csvparam.get("check_mandatory")
    _maxlength = csvparam.get("max_length")
    _validation_method = csvparam.get("validation_method")

    msg = []
    if _mandatory is True and (len(val) == 0 or val == ""):
        msg.append(key + " - Field is blank")
        error_count["mandatory"] = 1

    if _maxlength is not None and len(val) > _maxlength:
        msg.append(key + " - Cannot exceed max length")
        error_count["max_length"] = 1

    if _validation_method is not None and val != "":
        if _validation_method(val) is False:
            if key == "Due_Date" or key == "Completion_Date":
                msg.append(key + " - Invalid Date Format")
                error_count["invalid_date"] = 1
            else:
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
        isMandatoryCheck=False: to enable mandatory validation
        value has to be True,
            otherwise it will not validate
        maxLengthCheck=None: to enable max length validation
        value should not be None
        isValidCharCheck=False: to enable character validation
        value should be True
        validation_method=None: corresponding validation will
        done if the isValidCharCheck is True
        isFoundCheck=False: to check data already found given
        value should be True
        isActiveCheck=False: to check data status given value shoould be True

        if the param boolean value False means it will skip the
        corresponding validation
        maxlength param is not meant for INT type if the value not
        None means that will check maximum given value not length

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
    key_type,
    is_mandatory_check=False, max_length_check=None, is_valid_char_check=False,
    validation_method=None, is_found_check=False, is_active_check=False,
    is_valid_due_date=False, is_valid_completion_date=False
):
    constraints = {
        "key_type": key_type
    }

    if is_mandatory_check is True:
        constraints["check_mandatory"] = True

    if max_length_check is not None:
        constraints["max_length"] = max_length_check

    if is_valid_char_check is not False and validation_method is not None:
        constraints["validation_method"] = validation_method

    if is_found_check is not False:
        constraints["check_is_exists"] = True

    if is_active_check is not False:
        constraints["check_is_active"] = True

    if is_valid_due_date is not False:
        constraints["check_due_date"] = True

    if is_valid_completion_date is not False:
        constraints["check_completion_date"] = True
    return constraints


# key name should be as it is in csv file

csv_params = {
    "Legal_Entity": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=50,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric, is_found_check=True,
        is_active_check=True
    ),
    "Domain": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=30,
        is_valid_char_check=True,
        validation_method=is_domain, is_found_check=True, is_active_check=True
    ),
    "Unit_Code": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=20,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric, is_found_check=True
    ),
    "Unit_Name": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=50,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric, is_found_check=True
    ),
    "Compliance_Frequency": make_required_validation(
        key_type="STRING", is_valid_char_check=True, is_mandatory_check=True,
        validation_method=is_alphabet, is_found_check=True
    ),
    "Primary_Legislation": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=500,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric, is_found_check=True
    ),
    "Secondary_Legislation": make_required_validation(
        key_type="STRING", max_length_check=500, is_valid_char_check=True,
        validation_method=is_alpha_numeric, is_found_check=True,
        is_active_check=True
    ),
    "Compliance_Task": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=100,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric_allow_spl, is_found_check=True
    ),
    "Compliance_Description": make_required_validation(
        key_type="STRING", is_mandatory_check=True, max_length_check=500,
        is_valid_char_check=True,
        validation_method=is_alpha_numeric_allow_spl, is_found_check=True
    ),
    "Statutory_Date": make_required_validation(
        key_type="STRING", is_mandatory_check=True, is_valid_char_check=True,
        validation_method=is_alpha_numeric_with_brace
    ),
    "Due_Date": make_required_validation(
        key_type="STRING", is_mandatory_check=True, is_valid_char_check=True,
        validation_method=is_date, is_valid_due_date=True
    ),
    "Assignee": make_required_validation(
        key_type="STRING", is_mandatory_check=True, is_valid_char_check=False,
        is_found_check=True
    ),
    "Completion_Date": make_required_validation(
        key_type="STRING", is_mandatory_check=True, is_valid_char_check=True,
        validation_method=is_date, is_valid_completion_date=True
    ),
    "Document_Name": make_required_validation(
        key_type="STRING", is_valid_char_check=True,
        validation_method=check_document_name
    )
}
