from server.common import (
    
    )
from server.clientdatabase.general import (
    get_user_company_details, get_countries_for_user,
    get_domains_for_user
    )

all__ = [
    "report_unitwise_compliance",
    "return_unitwise_report",
    "report_assigneewise_compliance",
    "return_assignee_report_data",
    "report_serviceproviderwise_compliance",
    "return_serviceprovider_report_data",
    "report_statutory_notifications_list",
    "report_compliance_details",
    "report_reassigned_history"
]

def report_unitwise_compliance(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, assignee,
    session_user, from_count, to_count
):
    data, total = self.report_assigneewise_compliance(
        country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, assignee,
        session_user, from_count, to_count
    )
    return data, total

# assigneewise compliance report
def report_assigneewise_compliance(
    self, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, assignee,
    session_user, from_count, to_count
):
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date",
        "compliance_task", "document_name", "description", "frequency_id",
        "assignee_name", "concurrence_name", "approval_name",
        "assignee", "concurrance", "approval",
        "business_group", "legal_entity", "division",
        "unit_code", "unit_name", "frequency",
        "duration_type", "repeat_type", "duration",
        "repeat_every"
    ]
    qry_where = ""
    admin_id = self.get_admin_id()
    if business_group_id is not None :
        qry_where += " AND u.business_group_id = %s " % (business_group_id)
    if legal_entity_id is not None :
        qry_where += " AND u.legal_entity_id = %s " % (legal_entity_id)
    if division_id is not None :
        qry_where += " AND u.division_id = %s " % (division_id)
    if unit_id is not None :
        qry_where += " AND u.unit_id = %s" % (unit_id)
    if assignee is not None :
        qry_where += " AND ac.assignee = %s" % (assignee)
    if session_user > 0 and session_user != admin_id :
        qry_where += " AND u.unit_id in \
            (select us.unit_id from tbl_user_units us where \
                us.user_id = %s\
            )" % int(session_user)

    q_count = " SELECT  \
        count(ac.compliance_id) \
    FROM tbl_assigned_compliances ac \
        INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
        INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
        WHERE c.is_active = 1 \
        and ac.country_id = %s and c.domain_id = %s \
        %s \
    " % (
        country_id, domain_id,
        qry_where
    )
    row = self.select_one(q_count)
    if row :
        count = row[0]
    else :
        count = 0


    q = " SELECT  \
        ac.country_id, ac.unit_id, ac.compliance_id, ac.statutory_dates ,\
        ac. trigger_before_days, ac.due_date, ac.validity_date, \
        c.compliance_task, c.document_name, c.compliance_description, c.frequency_id, \
        IFNULL((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a \
            where a.user_id = ac.assignee \
        ), 'Administrator') assignee_name, \
        (select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a  \
            where a.user_id = ac.concurrence_person \
        ) concurrence_name, \
        IFNULL((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a  \
            where a.user_id = ac.approval_person \
        ), 'Administrator') approval_name,  \
        ac.assignee, ac.concurrence_person, ac.approval_person, \
        (select b.business_group_name from tbl_business_groups b \
            where b.business_group_id = u.business_group_id \
        )business_group_name, \
        (select l.legal_entity_name from tbl_legal_entities l \
            where l.legal_entity_id = u.legal_entity_id \
        )legal_entity_name, \
        (select d.division_name from tbl_divisions d \
            where d.division_id = u.division_id \
        )business_group_name, \
        u.unit_code, u.unit_name, \
        (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) frequency, \
        (select duration_type from tbl_compliance_duration_type where duration_type_id = c.duration_type_id) AS duration_type, \
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = c.repeats_type_id) AS repeat_type, \
        c.duration, c.repeats_every \
    FROM tbl_assigned_compliances ac \
        INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
        INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
        WHERE c.is_active = 1 \
        and ac.country_id = %s and c.domain_id = %s \
        %s \
    ORDER BY u.legal_entity_id, ac.assignee, u.unit_id \
    limit %s, %s" % (
        country_id, domain_id,
        qry_where, from_count, to_count
    )

    rows = self.select_all(q)
    data = self.convert_to_dict(rows, columns)
    return data, count

def return_unitwise_report(data):
    legal_wise = {}
    for d in data :
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates :
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = core.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = self.datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = self.datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3) :
            summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
        elif d["frequency_id"] == 4 :
            summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
        else :
            summary = None

        if d["document_name"] in ["None", None, ""] :
            name = d["compliance_task"]
        else :
            name = d["document_name"] + " - " + d["compliance_task"]
        uname = d["unit_code"] + " - " + d["unit_name"]
        compliance = clientreport.ComplianceUnit(
            name, uname,
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )

        group_by_legal = legal_wise.get(d["legal_entity"])
        if group_by_legal is None :
            unit_wise = {}
            unit_wise[uname] = [compliance]
            AC = clientreport.UnitCompliance(
                d["business_group"], d["legal_entity"],
                d["division"], unit_wise
            )
            AC.to_structure()
            legal_wise[d["legal_entity"]] = AC
        else :
            unit_wise_list = group_by_legal.unit_wise_compliances
            if unit_wise_list is None :
                unit_wise_list = {}
                unit_wise_list[uname] = [compliance]
            else :
                lst = unit_wise_list.get(uname)
                if lst is None :
                    lst = []
                lst.append(compliance)
                unit_wise_list[uname] = lst

            group_by_legal.unit_wise_compliances = unit_wise_list
            legal_wise[d["legal_entity"]] = group_by_legal
    return legal_wise.values()

def return_assignee_report_data(data):
    legal_wise = {}
    for d in data :
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates :
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = core.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = self.datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = self.datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3) :
            summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
        elif d["frequency_id"] == 4 :
            summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
        else :
            summary = None

        if d["document_name"] in ["None", None, ""] :
            name = d["compliance_task"]
        else :
            name = d["document_name"] + " - " + d["compliance_task"]
        compliance = clientreport.ComplianceUnit(
            name, d["unit_code"] + " - " + d["unit_name"],
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )
        user_wise_compliance = clientreport.UserWiseCompliance(
            d["assignee_name"], d["concurrence_name"],
            d["approval_name"], [compliance]
        )
        group_by_legal = legal_wise.get(d["legal_entity"])
        if group_by_legal is None :
            AC = clientreport.AssigneeCompliance(
                d["business_group"], d["legal_entity"],
                d["division"], [user_wise_compliance]
            )
            AC.to_structure()
            legal_wise[d["legal_entity"]] = AC
        else :
            user_wise_list = group_by_legal.user_wise_compliance
            if user_wise_list is None :
                user_wise_list = []
                user_wise_list.append(user_wise_compliance)
            else :
                is_added = False
                for u in user_wise_list :
                    if (
                        d["assignee_name"] == u.assignee and
                        d["concurrence_name"] == u.concurrence_person and
                        d["approval_name"] == u.approval_person
                    ):
                        lst = u.compliances
                        if lst is None :
                            lst = []
                        lst.append(compliance)
                        u.complaince = lst
                        is_added = True
                if is_added is False:
                    user_wise_list.append(user_wise_compliance)

            group_by_legal.user_wise_compliance = user_wise_list
            legal_wise[d["legal_entity"]] = group_by_legal
    return legal_wise.values()

def report_serviceproviderwise_compliance(
    self, country_id, domain_id, statutory_id, unit_id,
    service_provider_id, session_user, from_count, to_count
):
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date",
        "compliance_task", "document_name", "description", "frequency_id",
        "assignee", "service_provider_id",
        "service_provider_name", "address", "contract_from",
        "contract_to", "contact_person", "contact_no",
        "unit_code", "unit_name", "frequency",
        "duration_type", "repeat_type", "duration",
        "repeat_every"
    ]
    qry_where = ""
    admin_id = self.get_admin_id()

    if unit_id is not None :
        qry_where += " AND u.unit_id = %s" % (unit_id)
    if service_provider_id is not None :
        qry_where += " AND s.service_provider_id = %s" % (service_provider_id)
    if session_user > 0 and session_user != admin_id :
        qry_where += " AND u.unit_id in \
            (select us.unit_id from tbl_user_units us where \
                us.user_id = %s\
            )" % int(session_user)

    q_count = " SELECT  \
        count(ac.compliance_id) \
    FROM tbl_assigned_compliances ac \
        INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
        INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
        INNER JOIN tbl_users ur on ur.user_id = ac.assignee and ur.is_service_provider = 1 \
        INNER JOIN tbl_service_providers s on s.service_provider_id = ur.service_provider_id \
        WHERE c.is_active = 1 \
        and ac.country_id = %s and c.domain_id = %s  \
        AND SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1),'>>',- 1) = '%s'\
        %s \
    " % (
        country_id, domain_id, statutory_id,
        qry_where
    )

    row = self.select_one(q_count)
    if row :
        count = row[0]
    else :
        count = 0


    q = " SELECT  \
        ac.country_id, ac.unit_id, ac.compliance_id, ac.statutory_dates ,\
        ac.trigger_before_days, ac.due_date, ac.validity_date, \
        c.compliance_task, c.document_name, c.compliance_description, c.frequency_id, \
        ac.assignee, \
        s.service_provider_id, s.service_provider_name, s.address, s.contract_from, s.contract_to, s.contact_person, s.contact_no,  \
        u.unit_code, u.unit_name, \
        (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) frequency, \
        (select duration_type from tbl_compliance_duration_type where duration_type_id = c.duration_type_id) AS duration_type, \
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = c.repeats_type_id) AS repeat_type, \
        c.duration, c.repeats_every \
    FROM tbl_assigned_compliances ac \
        INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
        INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
        INNER JOIN tbl_users ur on ur.user_id = ac.assignee and ur.is_service_provider = 1 \
        INNER JOIN tbl_service_providers s on s.service_provider_id = ur.service_provider_id \
        WHERE c.is_active = 1 \
        and ac.country_id = %s and c.domain_id = %s \
        AND SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1),'>>',- 1) = '%s'\
        %s \
    ORDER BY ac.assignee, u.unit_id \
    limit %s, %s" % (
        country_id, domain_id, statutory_id,
        qry_where, from_count, to_count
    )

    rows = self.select_all(q)
    data = self.convert_to_dict(rows, columns)
    return data, count

def return_serviceprovider_report_data(data):
    serviceprovider_wise = {}
    for d in data :
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates :
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = core.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = self.datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = self.datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3) :
            summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
        elif d["frequency_id"] == 4 :
            summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
        else :
            summary = None

        if d["document_name"] in ["None", None, ""] :
            name = d["compliance_task"]
        else :
            name = d["document_name"] + " - " + d["compliance_task"]
        uname = d["unit_code"] + " - " + d["unit_name"]
        compliance = clientreport.ComplianceUnit(
            name, uname,
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )

        group_by_serviceprovider = serviceprovider_wise.get(d["service_provider_name"])
        if group_by_serviceprovider is None :
            unit_wise = {}
            unit_wise[uname] = [compliance]
            AC = clientreport.ServiceProviderCompliance(
                d["service_provider_name"], d["address"],
                self.datetime_to_string(d["contract_from"]),self.datetime_to_string(d["contract_to"]),
                d["contact_person"], d["contact_no"], unit_wise
            )
            AC.to_structure()
            serviceprovider_wise[d["service_provider_name"]] = AC
        else :
            unit_wise_list = group_by_serviceprovider.unit_wise_compliance
            if unit_wise_list is None :
                unit_wise_list = {}
                unit_wise_list[uname] = [compliance]
            else :
                lst = unit_wise_list.get(uname)
                if lst is None :
                    lst = []
                lst.append(compliance)
                unit_wise_list[uname] = lst

            group_by_serviceprovider.unit_wise_compliances = unit_wise_list
            serviceprovider_wise[d["service_provider_name"]] = group_by_serviceprovider
    return serviceprovider_wise.values()

def report_statutory_notifications_list(db, request_data):
    country_name = request_data.country_name
    domain_name = request_data.domain_name
    business_group_id = request_data.business_group_id
    legal_entity_id = request_data.legal_entity_id
    division_id = request_data.division_id
    unit_id = request_data.unit_id
    level_1_statutory_name = request_data.level_1_statutory_name
    from_date = request_data.from_date
    to_date = request_data.to_date
    condition = ""
    if from_date is not None and to_date is not None :
        from_date = self.string_to_datetime(from_date).date()
        to_date = self.string_to_datetime(to_date).date()
        condition += " AND date(snl.updated_on) >= '%s' AND date(snl.updated_on) <= '%s'" % (from_date, to_date)
    if business_group_id is not None:
        condition += " AND u.business_group_id = '%s'" % business_group_id
    if legal_entity_id is not None:
        condition += " AND u.legal_entity_id = '%s'" % legal_entity_id
    if division_id is not None:
        condition += " AND u.division_id = '%s'" % division_id
    if unit_id is not None:
        condition += " AND u.unit_id = '%s'" % unit_id

    if level_1_statutory_name is not None :
        condition += " AND snl.statutory_provision like '%s'" % str((level_1_statutory_name + '%'))

    query = "SELECT \
        (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id), \
        (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
        (select division_name from tbl_divisions where division_id = u.division_id), \
        u.unit_code, \
        u.unit_name, \
        u.address, \
        snl.statutory_provision, \
        snl.notification_text, \
        snl.updated_on \
    from \
        tbl_statutory_notifications_log snl \
            INNER JOIN \
        tbl_statutory_notifications_units snu \
    ON snl.statutory_notification_id = snu.statutory_notification_id \
            INNER JOIN \
        tbl_units u ON snu.unit_id = u.unit_id \
        INNER JOIN tbl_countries tc ON \
        tc.country_id = snl.country_name \
        INNER JOIN tbl_domains td ON \
        td.domain_id = snl.domain_name \
    where \
        tc.country_name = '%s' \
        and td.domain_name = '%s' \
        %s \
        ORDER BY snl.updated_on" % (
                country_name, domain_name,
                condition
            )
    rows = self.select_all(query)
    columns = [
        "business_group", "legal_entity", "division", "unit_code", "unit_name",
        "address", "statutory_provision", "notification_text", "updated_on"
    ]
    data = self.convert_to_dict(rows, columns)
    legal_wise = {}
    for d in data :
        unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
        statutories = d["statutory_provision"].split(">>")
        level_1_statutory_name = statutories[0].strip()

        level_1_statutory_wise_notifications = {}
        notify = clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS(
            d["statutory_provision"],
            unit_name,
            d["notification_text"],
            self.datetime_to_string(d["updated_on"])
        )
        level_1_statutory_wise_notifications[level_1_statutory_name] = [notify]
        legal_wise_data = legal_wise.get(d["legal_entity"])
        if legal_wise_data is None :
            legal_wise_data = clientreport.STATUTORY_WISE_NOTIFICATIONS(
                d["business_group"], d["legal_entity"], d["division"],
                level_1_statutory_wise_notifications
            )
        else :
            dict_level_1 = legal_wise_data.level_1_statutory_wise_notifications
            if dict_level_1 is None :
                dict_level_1 = {}
            lst = dict_level_1.get(level_1_statutory_name)
            if lst is None :
                lst = []
            else :
                lst.append(notify)
            dict_level_1[level_1_statutory_name] = lst
            legal_wise_data.level_1_statutory_wise_notifications = dict_level_1
        legal_wise[d["legal_entity"]] = legal_wise_data

    notification_lst = []
    for k in sorted(legal_wise):
        notification_lst.append(legal_wise.get(k))
    return notification_lst

def report_compliance_details(
    self, client_id, country_id, domain_id, statutory_id,
    unit_id, compliance_id, assignee,
    from_date, to_date, compliance_status,
    session_user, from_count, to_count
) :

    qry_where = get_where_query_for_compliance_details_report(
        db, country_id, domain_id, statutory_id,
        unit_id, compliance_id, assignee,
        from_date, to_date, compliance_status,
        session_user
    )

    total = get_compliance_details_total_count(
        db, country_id, domain_id, statutory_id, qry_where
    )

    result = get_compliance_details(
        db, country_id, domain_id, statutory_id,
        qry_where, from_count, to_count
    )

    return self.return_cmopliance_details_report(client_id, compliance_status, result, total)

def return_cmopliance_details_report(client_id, compliance_status, result, total):
    unitWise = {}
    for r in result :
        uname = r["unit_code"] + ' - ' + r["unit_name"]
        if r["document_name"] == "None" :
            compliance_name = r["compliance_task"]
        else :
            compliance_name = r["document_name"] + ' - ' + r["compliance_task"]

        if r["assigneename"] is None :
            assignee = 'Administrator'
        else :
            assignee = r["assigneename"]

        due_date = None
        if(r["due_date"] != None):
            due_date = self.datetime_to_string(r["due_date"])

        validity_date = None
        if(r["validity_date"] != None):
            validity_date = self.datetime_to_string(r["validity_date"])

        documents = [x for x in r["documents"].split(",")] if r["documents"] != None else None
        doc_urls = []
        if documents is not None :
            for d in documents :
                if d != "" :
                    t = "%s/%s/%s" % (CLIENT_DOCS_DOWNLOAD_URL, str(client_id), str(d))
                    doc_urls.append(t)

        completion_date = None
        if(r["completion_date"] != None):
            completion_date = self.datetime_to_string(r["completion_date"])

        remarks = self.calculate_ageing(r["due_date"], r["fname"], r["completion_date"])[1]

        compliance = clientreport.ComplianceDetails(
            compliance_name, assignee, due_date,
            completion_date, validity_date,
            doc_urls, remarks
        )
        unit_compliance = unitWise.get(uname)
        if unit_compliance is None :
            unit_compliance = clientreport.ComplianceDetailsUnitWise(
                r["unit_id"], uname, r["address"],
                [compliance]
            )
        else :
            compliance_lst = unit_compliance.Compliances
            if compliance_lst is None :
                compliance_lst = []
            compliance_lst.append(compliance)
            unit_compliance.Compliances = compliance_lst
        unitWise[uname] = unit_compliance

    final_lst = []
    for k in sorted(unitWise):
        final_lst.append(unitWise.get(k))

    return final_lst, total

def get_where_query_for_compliance_details_report(
    self, country_id, domain_id, statutory_id,
    unit_id, compliance_id, assignee,
    from_date, to_date, compliance_status,
    session_user
):
    q_c = "SELECT t.period_from, t.period_to FROM tbl_client_configurations t \
            where t.country_id = %s and t.domain_id = %s " % (country_id, domain_id)
    r_c = self.select_one(q_c)
    f_date = t_date = None
    if r_c :
        year_list = self.calculate_years(int(r_c[0]), int(r_c[1]))[0]

        f_date = datetime.date(int(year_list[0]), int(r_c[0]), 1)
        if int(r_c[1]) == 12 :
            t_date = datetime.date(int(year_list[0]), int(r_c[1]), 31)
        else :
            t_date = datetime.date(int(year_list[0]), int(r_c[1])+1, 1) - datetime.timedelta(days=1)

    qry_where = ""
    admin_id = self.get_admin_id()
    if unit_id is not None :
        qry_where += " AND ch.unit_id = %s" % (unit_id)
    if compliance_id is not None :
        qry_where += " AND ch.compliance_id = %s " % (compliance_id)
    if assignee is not None :
        qry_where += " AND ch.completed_by = %s" % (assignee)
    if session_user > 0 and session_user != admin_id :
        qry_where += " AND ch.unit_id in \
            (select us.unit_id from tbl_user_units us where \
                us.user_id = %s\
            )" % int(session_user)
        qry_where += " and c.domain_id IN \
            (SELECT ud.domain_id FROM tbl_user_domains ud \
            where ud.user_id = %s)" % int(session_user)

    if(compliance_status == 'Complied'):
        c_status = " AND ch.due_date >= ch.completion_date \
            AND IFNULL(ch.approve_status,0) = 1"
    elif(compliance_status == 'Delayed Compliance'):
        c_status = " AND ch.due_date < ch.completion_date \
            AND IFNULL(ch.approve_status,0) = 1"
    elif(compliance_status == 'Inprogress'):
        c_status = " AND ((c.duration_type_id =2 AND ch.due_date >= now()) or (c.duration_type_id != 2 and ch.due_date >= CURDATE())) \
            AND IFNULL(ch.approve_status,0) <> 1"
    elif(compliance_status == 'Not Complied'):
        c_status = " AND ((c.duration_type_id =2 AND ch.due_date < now()) or (c.duration_type_id != 2 and ch.due_date < CURDATE())) \
            AND IFNULL(ch.approve_status,0) <> 1"
    else:
        c_status = ''

    qry_where += c_status

    if from_date is not None and to_date is not None :
        start_date = self.string_to_datetime(from_date)
        end_date = self.string_to_datetime(to_date)
        qry_where += " AND ch.due_date between '%s' and '%s'" % (start_date, end_date)

    else :

        qry_where += " AND ch.due_date >= '%s' \
            AND ch.due_date <= '%s'" % (f_date, t_date)
    return qry_where

def get_compliance_details_total_count(
    self, country_id, domain_id, statutory_id, qry_where
):
    qry_count = "SELECT \
        count(distinct ch.compliance_history_id) \
    from \
        tbl_compliance_history ch  \
        inner join  \
        tbl_compliances c on ch.compliance_id = c.compliance_id  \
        inner join  \
        tbl_units ut on ch.unit_id = ut.unit_id \
    where ut.country_id = %s \
            AND c.domain_id = %s \
            AND c.statutory_mapping like '%s' \
            %s \
    order by ch.due_date desc \
     " % (
        country_id, domain_id,
        str(statutory_id+"%"),
        qry_where
    )

    row = self.select_one(qry_count)
    if row :
        total = int(row[0])
    else :
        total = 0
    return total

def get_compliance_details(
    self, country_id, domain_id, statutory_id,
    qry_where, from_count, to_count
):

    columns = [
        "compliance_history_id", "document_name",
        "compliance_description", "validity_date",
        "due_date", "completed_by", "status", "assigneename", "documents",
        "completion_date", "compliance_task", "frequency_id", "fname",
        "unit_id", "unit_code", "unit_name", "address"
    ]
    qry = "SELECT \
        distinct ch.compliance_history_id, \
        c.document_name, \
        c.compliance_description, \
        ch.validity_date, \
        ch.due_date, \
        ch.completed_by, \
        ifnull(ch.approve_status, 0) status,\
        (SELECT  \
                concat(u.employee_code, '-', u.employee_name) \
            FROM \
                tbl_users u \
            WHERE \
                u.user_id = ch.completed_by) AS assigneename, \
        ch.documents, \
        ch.completion_date, \
        c.compliance_task, \
        c.frequency_id, \
        (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) fname, \
        ch.unit_id, ut.unit_code, ut.unit_name, ut.address\
    from \
        tbl_compliance_history ch  \
        inner join  \
        tbl_compliances c on ch.compliance_id = c.compliance_id  \
        inner join  \
        tbl_units ut on ch.unit_id = ut.unit_id \
    where ut.country_id = %s \
            AND c.domain_id = %s \
            AND c.statutory_mapping like '%s' \
            %s \
    order by ch.due_date desc limit %s, %s \
    " % (
        country_id, domain_id,
        str(statutory_id+"%"),
        qry_where, from_count, to_count
    )
    rows = self.select_all(qry)
    result = self.convert_to_dict(rows, columns)
    return result

def report_reassigned_history(
    self, country_id, domain_id, level_1_statutory_name,
    unit_id, compliance_id, user_id, from_date, to_date, session_user,
    from_count, to_count
):
    qry_where = get_where_query_for_reassigned_history_report(
        db, country_id, domain_id, level_1_statutory_name,
        unit_id, compliance_id, user_id, from_date, to_date, session_user
    )
    result = get_reassigned_history_report_data(
        db, country_id, domain_id, qry_where,
        from_count, to_count
    )
    count = get_reassigned_history_report_count(
        db, country_id, domain_id, qry_where
    )
    return return_reassinged_history_report(
        result, count
    )

def return_reassinged_history_report(self, result, total):
    level_wise = {}
    for r in result :
        if r["document_name"] is not None :
            cname = " %s - %s" % (r["document_name"], r["compliance_task"])
        else :
            cname = r["compliance_task"]

        uname = r["unit_code"] + ' - ' + r["unit_name"]
        uid = r["unit_id"]

        mappings = r["statutory_mapping"].split('>>')
        statutory_name = mappings[0].strip()
        statutory_name = statutory_name.strip()

        reassign = clientreport.ReassignHistory(
            r["oldassignee"], r["assigneename"],
            self.datetime_to_string(r["reassigned_date"]),
            r["remarks"]
        )
        reassignCompliance = clientreport.ReassignCompliance(
            cname, self.datetime_to_string(r["due_date"]),
            [reassign]
        )
        unitcompliance = clientreport.ReassignUnitCompliance(
            uid,
            uname,
            r["address"], [reassignCompliance]
        )
        level_unit = level_wise.get(statutory_name)
        if level_unit is None :
            level_unit = clientreport.StatutoryReassignCompliance(
                statutory_name, [unitcompliance]
            )
        else :
            unitcompliancelst = level_unit.compliance
            if unitcompliancelst is None :
                unitcompliancelst = []
            u_new = True
            for c in unitcompliancelst :
                if uid == c.unit_id :
                    u_new = False
                    reassing_compliance_lst = c.reassign_compliances
                    if reassing_compliance_lst is None :
                        reassing_compliance_lst = []
                    r_new = True
                    for r in reassing_compliance_lst :
                        if cname == r.compliance_name :
                            r_new = False
                            history_lst = r.reassign_history
                            if history_lst is None :
                                history_lst = []
                            history_lst.append(reassign)
                            r.reassign_history = history_lst
                    if r_new is True :
                        reassing_compliance_lst.append(reassignCompliance)
            if u_new is True :
                unitcompliancelst.append(unitcompliance)
            level_unit.compliance = unitcompliancelst
        level_wise[statutory_name] = level_unit
    final_list = []
    for k in sorted(level_wise) :
        final_list.append(level_wise.get(k))
    return final_list, total

def get_where_query_for_reassigned_history_report(
    self, country_id, domain_id, level_1_statutory_name,
    unit_id, compliance_id, user_id, from_date, to_date, session_user
):
    qry_where = ""
    admin_id = self.get_admin_id()
    if level_1_statutory_name is not None :
        qry_where += " AND t3.statutory_mapping like '%s'" % (str(level_1_statutory_name+'%'))
    if unit_id is not None :
        qry_where += " And t1.unit_id = %s" % (unit_id)

    if compliance_id is not None :
        qry_where += " AND t1.compliance_id = %s" % (compliance_id)
    if user_id is not None :
        qry_where += " AND t1.assignee = %s " % (user_id)

    if from_date is not None and to_date is not None :
        start_date = self.string_to_datetime(from_date).date()
        end_date = self.string_to_datetime(to_date).date()
        qry_where += " AND t1.reassigned_date between '%s' and '%s' " % (start_date, end_date)
    elif from_date is not None:
        start_date = self.string_to_datetime(from_date).date()
        qry_where += " AND t1.reassigned_date > DATE_SUB('%s', INTERVAL 1 DAY)" % (start_date)
    elif to_date is not None:
        end_date = self.string_to_datetime(from_date).date()
        qry_where += " AND t1.reassigned_date < DATE_SUB('%s', INTERVAL 1 DAY)" % (end_date)

    if session_user > 0 and session_user != admin_id :
        qry_where += " AND t1.unit_id in \
            (select us.unit_id from tbl_user_units us where \
                us.user_id = %s\
            )" % int(session_user)
        qry_where += " and t3.domain_id IN \
            (SELECT ud.domain_id FROM tbl_user_domains ud \
            where ud.user_id = %s)" % int(session_user)
    return qry_where

def get_reassigned_history_report_data(
    self, country_id, domain_id, qry_where,
    from_count, to_count
):
    columns = [
        "compliance_id", "assignee", "reassigned_from", "reassigned_date",
        "remarks", "due_date", "compliance_task",
        "document_name", "unit_code", "unit_name", "address",
        "assigneename", "oldassignee", "unit_id", "statutory_mapping"
    ]
    qry = " SELECT distinct t1.compliance_id, t1.assignee, t1.reassigned_from, \
        t1.reassigned_date, t1.remarks, t2.due_date, t3.compliance_task, \
        t3.document_name, t4.unit_code, t4.unit_name, t4.address, \
        ifnull((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a where a.user_id = t1.assignee), 'Administrator') assigneename, \
        ifnull((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a where a.user_id = t1.reassigned_from) , 'Administrator') oldassignee, \
        t1.unit_id, t3.statutory_mapping \
        FROM tbl_reassigned_compliances_history t1 \
        INNER JOIN tbl_assigned_compliances t2 on t1.compliance_id = t2.compliance_id \
        AND t1.unit_id = t2.unit_id \
        INNEr JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id \
        INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id \
        WHERE t4.country_id = %s \
        AND t3.domain_id = %s \
        %s \
        order by SUBSTRING_INDEX(SUBSTRING_INDEX(t3.statutory_mapping, '>>', 1), \
        '>>', - 1), t1.unit_id,  t1.reassigned_date desc \
        limit %s, %s" % (
            country_id, domain_id,
            qry_where,
            from_count, to_count

        )
    rows = self.select_all(qry)
    result = self.convert_to_dict(rows, columns)
    return result

def get_reassigned_history_report_count(
    self, country_id, domain_id, qry_where
):
    qry_count = "SELECT sum(t.c_count) from \
    (SELECT \
        count(distinct t1.compliance_id) c_count \
    FROM \
        tbl_reassigned_compliances_history t1 \
            INNER JOIN \
        tbl_assigned_compliances t2 ON t1.compliance_id = t2.compliance_id \
            AND t1.unit_id = t2.unit_id \
            INNEr JOIN \
        tbl_compliances t3 ON t1.compliance_id = t3.compliance_id \
            INNER JOIN \
        tbl_units t4 ON t1.unit_id = t4.unit_id \
    WHERE \
        t4.country_id = %s AND t3.domain_id = %s \
        %s \
    group by t1.unit_id) t " % (
        country_id, domain_id,
        qry_where,
    )
    rcount = self.select_one(qry_count)
    if rcount[0] :
        count = int(rcount[0])
    else :
        count = 0
    return count