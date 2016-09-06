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
    "E065": "User group is inactive, cannot activate user"
}

client_message = {
    "E001": "Service provider creation failed",
    "E002": "Service provider updation failed",
    "E003": "Servie provider status updation failed",
    "E004": "User group creation failed",
    "E005": "User group updation failed",
    "E006": "User group status updation failed",
    "E007": "User creation failed",
    "E008": "User's countries creation failed",
    "E009": "User's domains creation failed",
    "E010": "User's units creation failed",
    "E011": "User details updation failed",
    "E012": "User status updation failed",
    "E013": "Admin status updation failed",
    "E014": "Unit close failed",
    "E015": "Save past records failed",
    "E016": "Reassign compliance failed",
    "E017": "On occurrence compliance start failed",
    "E018": "Compliance activity creation failed",
    "E019": "Create notification failed",
    "E020": "Save compliance activity failed",
    "E021": "Core file space update failed",
    "E022": "Client user details save failed in core",
    "E023": "Client user details update failed in core",
    "E024": "Client user status update failed in core",
    "E025": "Client unit closure failed in core",
    "E026": "Client opted status save failed in core",
    "E027": "Client active status validation failed",
    "E028": "Email notification got failed",
    "E029": "Saving reset token failed",
    "E030": "User group is inactive, cannot activate user"
}


def process_error(msg_code):
    return RuntimeError(messages.get(msg_code))


def client_process_error(msg_code):
    return RuntimeError(client_message.get(msg_code))


def fetch_error():
    return RuntimeError("Transaction failed while processing data.")


def not_found_error(msg_code):
    return ValueError(messages.get(msg_code))
