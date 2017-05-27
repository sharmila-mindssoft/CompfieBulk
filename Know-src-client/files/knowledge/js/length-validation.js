var max_length = {
  'countryname': 30,
  'domainname': 30,
  'usergroupname': 50,
  'employeename': 50,
  'employeeid': 20,
  'email_id': 100,
  'mcountrycode': 3,
  'mobileno': 10,
  'contactno': 7,
  'address': 250,
  'designation': 50,
  'db_server_name': 50,
  'username': 50,
  'organization_name': 50,
  'password': 20,
  'remark': 500,
  'application_server': 50,
  'ip': 15,
  'port': 4,
  'countrycode': 3,
  'areacode': 4,
  'groupname':50,
  'shortname':20,
  'nooflicence':3,
  'business_group_name':50,
  'legal_entity_name':50,
  'licence':3,
  'file_space':3,
  'serviceprovidername': 50,
  'serviceprovider_shortname': 20,
  'serviceprovider_contact_person': 50,
  'serviceprovider_contact_number': 10,
  'serviceprovider_address': 500,
  'division_name': 50,
  'category_name': 50,
  'unit_code': 20,
  'unit_name': 50,
  'unit_address': 250,
  'unit_post_code': 6,
  'file_server': 50,
  'level_value': 30,
  'geography_lvl': 50,
  'validity_days': 3,
  'statutoryname': 100,
  'provision': 500,
  'taskname': 100,
  'docname': 100,
  'description': 500,
  'penal': 500,
  'referlink': 500,
  'no_of_units': 3,
  'logo': 50,
  'statutory_nature_name': 50,
}


function expectationError(expected, received){
  msg = "expected " + expected + ", but received : " + received
  return msg
}


function validateLength(key_name, value) {
  v = max_length[key_name];
  if (value.length > v) {
    msg = " should not exceed " + v + " characters";
    return msg;
  }
  return true
}


function validateMaxLength(key_name, value, show_name) {
  if(value.trim() != "") {
    e_n_msg = validateLength(key_name, value.trim())
    if (e_n_msg != true) {
      displayMessage(show_name + e_n_msg);
      return false;
    }
  }
  return true;
}
