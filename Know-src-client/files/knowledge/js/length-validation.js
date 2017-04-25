///////////////////////////

var max_length = {
  'countryname': 50,
  'domainname': 50,
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
  'organization_name': 100,
  'password': 20,
  'remark': 500,
  'application_server': 50,
  'ip': 15,
  'port': 4,
  'countrycode': 3,
  'areacode': 4,
  'designation':50
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
