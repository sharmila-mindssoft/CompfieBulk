messages = {
    "E001": "Industry creation failed",
    "E002": "Industry updation failed",
    "E003": "Industry status updation failed",
    "E004": "Statutory nature creation failed",
    "E005": "Statutory nature updation failed",
    "E006": "Statutory nature status update failed",
    "E007": "Statutory levels creation failed",
    "E008": "Statutory levels updation failed",
    "E009": "Level(s) deletion failed",
    "E010": "Geography levels creation failed",
    "E011": "Geography levels updation failed",
    "E012": "Geography location creation failed",
    "E013": "Geography location updation failed",
    "E014": "Geography location status updation failed",
    "E015": "Statutory creation failed",
    "E016": "Statutory updation failed",
    "E017": "Duplicate compliance name validation failed",
    "E018": "Stautory mapping creation failed",
    "E019": "Compliance creation failed",
    "E020": "Duplicate statutory mapping found",
    "E021": "Compliance updation failed",
    "E022": "Save statutory mapping backup failed",
    "E023": "Save stautory notification failed",
    "E024": "Domain creation failed",
    "E025": "Domain updation failed",
    "E026": "Domain status updation failed",
    "E027": "Country creation failed",
    "E028": "Country updation failed",
    "E029": "Country status updation failed",
    "E030": "User group creation failed",
    "E031": "User group updation failed",
    "E032": "User group status updation failed",
    "E033": "User creation failed",
    "E034": "User country creation failed",
    "E035": "User domain creation failed",
    "E036": "User details updation failed",
    "E037": "User country updation failed",
    "E038": "User domain updation failed",
    "E039": "User status updation failed",
    "E040": "Client group creation failed",
    "E041": "Client countries creation failed",
    "E042": "Client domains creation failed",
    "E043": "Client incharge person creation failed",
    "E044": "Client user creation failed",
    "E045": "Notify incharge person failed",
    "E046": "Client group updation failed",
    "E047": "Client date configuration creation failed",
    "E048": "Client date configuration updation failed",
    "E049": "Client group status updation failed",
    "E050": "Business group creation failed",
    "E051": "Business group updation failed",
    "E052": "Legal entity creation failed",
    "E053": "Legal entity updation failed",
    "E054": "Division creation failed",
    "E055": "Division updation failed",
    "E056": "Unit creation failed",
    "E057": "Unit updation failed",
    "E058": "Unit activation failed",
    "E059": "Client admin creation failed",
    "E060": "Client statutories creation failed",
    "E061": "Client info not found",
    "E062": "Client log save failed",
    "E063": "Geography used in statutory mapping",
    "E064": "Geography have child level entries ",
    "E065": "User group is inactive, cannot activate user",
    "E066": "Business group name already exists",
    "E067": "Invalid Image File",
    "E068": "Legal Entity name already exists",
    "E069": "Invalid number of licence",
    "E070": "Invalid File space",
    "E071": "Save Organization failed",
    "E072": "Unit Approval failed",
    "E073": "Client Group Approval failed",
    "E074": "Configuring Database server failed",
    "E075": "Configuring Client server failed",
    "E076": "Allocating Database environment failed",
    "E077": "Configuring File Storage failed",
    "E078": "Configuring auto deletion failed",
    "E079": "Save User Mapping Failed",
    "E080": "Assign Units Failed",
    "E081": "Save Reassign user account history failed",
    "E082": "Save Reassign user account failed",
    "E083": "There are no common countries among the selected units",
    "E084": "There are no common geographical location among the selected units",
    "E085": "There are no common domains among the selected units",
    "E086": "There are no common organisations among the selected units",
    "E087": "Invalid statutory mapping",
    "E088": "Save process failed",
    "E089": "Invalid status code",
    "E090": "Group admin registration mail send failed",
    "E091": "Unit Count exceeds the existing active unit count",

}


def process_error(msg_code):
    return RuntimeError(messages.get(msg_code))

def fetch_run_error(msg):
    return RuntimeError(str(msg))

def fetch_error():
    return RuntimeError("Transaction failed while processing data.")

def not_found_error(msg_code):
    return ValueError(messages.get(msg_code))

def process_procedure_error(name, args, error):
    msg = '%s- %s- %s' % (name, args, error)
    return RuntimeError(msg)

def return_Knowledge_message(code):
    return messages[code]

def process_error_with_msg(msg_code, msg):
    msgstr = '%s for %s' % (messages.get(msg_code), msg)
    return RuntimeError(msgstr)
