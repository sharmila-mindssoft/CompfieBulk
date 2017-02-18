import json
import datetime
from dateutil import relativedelta
from clientprotocol import (clientcore, dashboard)
from server.clientdatabase.tables import *
from server.clientdatabase.common import (
    get_last_7_years, get_country_domain_timelines,
    calculate_ageing_in_hours, calculate_years,
    get_country_domain_timelines_dict
)

from server.common import (
    get_date_time_in_date, convert_to_dict,
    datetime_to_string_time, datetime_to_string
)
from server.clientdatabase.general import (
    get_user_unit_ids, calculate_ageing, get_admin_id,
    get_user_domains, get_group_name, is_primary_admin,
    get_all_users, convert_datetime_to_date
)
