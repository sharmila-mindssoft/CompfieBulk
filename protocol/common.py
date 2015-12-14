from protocol.types import *

# SESSION_TOKEN = Text
# USERNAME = Text


# STATUTORY_ID = Int8

# Test_Custom_level_integer = CustomIntegerType(0,100)
# Test_Custom_level_string = CustomTextType(100)
# Text50 = CustomTextType(50)
# normal_text = Text50

Text20 = CustomTextType(20)
Text50 = CustomTextType(50)
Text100 = CustomTextType(100)
Text250 = CustomTextType(250)
Text500 = CustomTextType(500)

SESSION_TOKEN = Text50
USERNAME = Text100
PASSWORD = Text20
URL = Text250
MENU_NAME = Text50
EMPLOYEE_CODE = Text50
USER_GROUP_NAME = Text50
EMAIL_ID = Text100
ADDRESS = Text250
FORM_NAME = Text50
MAPPING_NAME = Text500
DOCUMENT_NAME =  Text50
COMPLIANCE_NAME = Text50
FORMAT_FILE_NAME = Text50
GEOGRAPHY_MAPPING_NAME = Text500
UNIT_CODE = Text20
LEVEL_1_STATUTORY_NAME = Text50
CONTACT_NUMBER = Text20
UNIT_NAME = Text50
EMPLOYEE_NAME = Text50
COMPLIANCE_TASK_NAME = Text50
RESET_TOKEN = Text50
DATE = Text20
COUNTRY_NAME = Text50
DOMAIN_NAME = Text50
LEVEL_NAME = Text50
GEOGRAPHY_NAME = Text50
INDUSTRY_NAME = Text50
STATUTORY_NATURE_NAME = Text50
STATUTORY_NAME = Text50
STATUTORY_PROVISION = Text500
DESCRIPTION = Text500
CLIENT_NAME = Text50
BUSINESS_GROUP_NAME = Text50
LEGAL_ENTITY_NAME = Text50
DIVISION_NAME= Text50
SERVICE_PROVIDER_NAME= Text50
DESIGNATION = Text50
NOTIFICATION_TYPE = Text20
NOTIFICATION_TEXT = Text
STATUTORY_LEVEL1_NAME = Text50
FILTER_NAME = Text100
CONTACT_PERSON = Text50

LEVEL_ID = Int8
STATUTORY_ID = Int8
STATUTORY_MAPPING_ID = Int8
GROUP_ID = Int8
CLIENT_ID = Int8
BUSINESS_GROUP_ID = Int8
LEGAL_ENTITY_ID = Int8
DIVISION_ID = Int8
UNIT_ID = Int8
COMPLIANCE_HISTORY_ID = Int8
SERVICE_PROVIDER_ID = Int8
CLIENT_USER_GROUP_ID = Int8
COMPLIANCE_ID = Int8
STATUTORY_NATURE_ID = Int8
COUNTRY_ID = Int8
DOMAIN_ID = Int8
FORM_ID = Int8
INDUSTRY_ID = Int8
USER_ID = Int8
USER_GROUP_ID = Int8
GEOGRAPHY_LEVEL_ID = Int8
GEOGRAPHY_ID = Int8
STATUTORY_LEVEL_ID = Int8
LEVEL_1_STATUTORY_ID = Int8
NO_OF_USER_LICENCE = Int8
REMAINING_USER_LICENCE = Int8
TOTAL_DISK_SPACE = Int8
NOTIFICATION_ID = Int8
USED_DISK_SPACE = Int8
CLIENT_SAVED_STATUTORY_ID = Int8
CLIENT_ASSIGNED_STATUTORY_ID = Int8
FILTER_ID = Int8
NO_OF_COMPLIANCES = Int8
AGEING = Int8

STATUS	= Bool
IS_ACTIVE = Bool
HAS_READ = Bool


TIMESTAMP = Float

USER_LEVEL = CustomIntegerType(1,10)
LEVEL_POSITION = CustomIntegerType(1,10)
STATUTORY_DATE = CustomIntegerType(1, 31)
STATUTORY_MONTH = CustomIntegerType(1, 12)
REMINDER_DAYS = CustomIntegerType(1, 7)

