var max_length = {
    'countryname': 30,
    'domainname': 30,
    'usergroupname': 50,
    'employeename': 50,
    'employeeid': 50,
    'email_id': 100,
    'mcountrycode': 4,
    'mobileno': 10,
    'contactno': 10,
    'address': 250,
    'designation': 50,
    'db_server_name': 50,
    'username': 50,
    'organization_name': 50,
    'password': 20,
    'remark': 500,
    'serviceprovidername': 50,
    'serviceprovider_shortname': 20,
    'serviceprovider_contact_person': 50,
    'serviceprovider_contact_number': 7,
    'serviceprovider_address': 500,
    'serviceprovider_mcountrycode': 3,
    'serviceprovider_countrycode': 3,
    'application_server': 50,
    'ip': 15,
    'port': 4,
    'division_name': 50,
    'category_name': 50,
    'unit_code': 20,
    'unit_name': 50,
    'unit_address': 250,
    'unit_post_code': 6,
    'db_server_name': 50,
    'file_server': 50,
    'level_value': 30,
    'geography_lvl': 50,
    'countrycode': 3,
    'areacode': 4,
    'designation': 50,
    'validity_days': 3,
    'repeatevery': 3,
}


function expectationError(expected, received) {
    msg = "expected " + expected + ", but received : " + received
    return msg
}


function validateLength(key_name, value) {
    v = max_length[key_name];
    // console.log(value);
    if (value.length > v) {
        msg = " should not exceed " + v + " characters";
        return msg;
    }
    return true
}


function validateMaxLength(key_name, value, show_name) {
    e_n_msg = validateLength(key_name, value.trim())
        // console.log(e_n_msg);
    if (e_n_msg != true) {
        displayMessage(show_name + e_n_msg);
        return false;
    }
    return true;
}