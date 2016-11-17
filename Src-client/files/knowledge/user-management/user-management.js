
var UsersList;
var DomainsList;
var CountryList;
var CategoryList;
var UserGroupList;

// Add screen fields
var AddScreen = $('#user-add');
var ViewScreen = $('#user-view');
var FilterBox = $('.filter-text-box');
var UserStatus = $('.usr-status');
var AddButton = $('#btn-user-add');
var CancelButton = $('#btn-user-cancel');
var SubmitButton = $('#btn-submit');

var User_id = $('#userid');
var Emp_name = $('#employeename');
var Emp_code = $('#employeeid');
var Address = $('#address');
var Email_id = $('#emailid');
var Country_code = $('#countrycode');
var Area_code = $('#areacode');
var Contact_no = $('#contactno');
var mCountry_code = $('#mcountrycode');
var Mobile_no = $('#mobileno');
var Designation = $("#designation");
// select box
var User_category = $('#usercatval');
// auto complete
var User_group_val = $('#usergroup');
var User_group_ac = $("#usergroupval");
// multi select textbox
var Countries = $("#countries");
var Domains = $('#domains');

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list'); 
var Search_status_li = $('.search-status-li');

var Search_disable = $('#search-disable');
var Search_disable_ul = $('.search-disable-list'); 
var Search_disable_li = $('.search-disable-li');

var ACUserGroup = $('#ac-usergroup');


var Domain_ids = [];
var Country_ids = [];
var msg = message;

function sendCredentials(_u_id, _u_name, _e_id ) {
  req_dict = {
    'user_id': _u_id,
    'username': _u_name,
    'email_id': _e_id
  };
  //custom_alert(req_dict);
  mirror.sendRegistration(req_dict, function(error, response) {

    if (error == null) {
      displaySuccessMessage(msg.resend);
    }
    else {
      displayMessage(error);
    }

  });
}
// User List render process
function renderUserList(response) {
    renderUserData = function() {
      _userList = []
      if (response == null) {
        _userList = UsersList;
      }
      else {
        _userList = response
      }
      $('.tbody-user-list').find('tr').remove();
      var j = 1;
      $.each(_userList, function(k, v) {
        var tableRow = $('#templates .table-user-master .table-row');
        var rowClone = tableRow.clone();

        $('.sno', rowClone).text(j);
        ename = v.employee_code + ' - ' + v.employee_name;
        $('.employee-name', rowClone).html(ename);
        $('.username',rowClone).html(v.username_id);
        $('.email-id', rowClone).html(v.email_id);
        $('.cat-name', rowClone).html(v.user_category_name);
        if (v.username_id == null){
          $('.popup-link', rowClone).show();
          $('.popup-link', rowClone).on('click', function() {
            sendCredentials(v.user_id, v.employee_code + ' - ' + v.employee_name, v.email_id);
          });
        }
        else {
          $('.popup-link', rowClone).hide();
        }
       
        $('.edit').attr('title', 'Click Here to Edit');
        $('.edit', rowClone).addClass('fa-pencil text-primary');
        $('.edit', rowClone).on('click', function () {
          displayEdit(v.user_id);
        });

        if (v.is_active == true){
          statusmsg = message.deactive_message;
          $('.status').attr('title', 'Click Here to Deactivate');
          $('.status', rowClone).removeClass('fa-times text-danger');
          $('.status', rowClone).addClass('fa-check text-success');
        }
        else{
          statusmsg = message.active_message;
          $('.status').attr('title', 'Click Here to Activate');
          $('.status', rowClone).removeClass('fa-check text-success');
          $('.status', rowClone).addClass('fa-times text-danger');
        }
        $('.status', rowClone).on('click', function () {
          confirm_alert(statusmsg, function(isConfirm){
            if(isConfirm){
              changeStatus(v.user_id, v.is_active);
            }
          });
        });

        if (v.is_disable == true) {
          disablemsg = message.enable_message;
          $('.disable').attr('title', 'Click Here to Disable');
          $('.disable', rowClone).removeClass('fa-ban text-muted');
          $('.disable', rowClone).addClass('fa-ban text-danger');
        }
        else{
          disablemsg = message.disable_message;
          $('.disable').attr('title', 'Click Here to Enable');
          $('.disable', rowClone).removeClass('fa-ban text-danger');
          $('.disable', rowClone).addClass('fa-ban text-muted');
        }
        $('.disable', rowClone).on('click', function () {
          confirm_alert(disablemsg, function(isConfirm){
            if(isConfirm){
              changeDisable(v.user_id, v.is_disable);
            }
          });
        });


        $('.tbody-user-list').append(rowClone);
        j = j + 1;
      });
    }

    fetchUserData = function() {
      mirror.getAdminUserList(function(error, response) {
        if (error != null) {
          displayMessage(error);
        }
        else {
          UsersList = response.user_details;
          DomainsList = response.domains;
          CountryList = response.countries;
          CategoryList = response.user_categories;
          UserGroupList = response.user_groups;
          renderUserData();
        }
      });
    }
    if (response == null) {
      fetchUserData();
    }
    else {
      renderUserData();
    }
}

function resetValues(){
  User_id.val('');
  Emp_name.val('');
  Emp_code.val('');
  Address.val('');
  Email_id.val('');
  Area_code.val('');
  Contact_no.val('');
  Mobile_no.val('');
  User_group_val.val('');
  User_group_ac.val('');
  Designation.val('');
  Country_ids = [];
  Domain_ids = [];
  loadUserCategories();
  loadCountries();
  loadDomains();
  User_category.focus();
}

function showList() {
  renderUserList(null);
  AddScreen.hide();
  ViewScreen.show();
}
// Enable Add/Edit Screen
function showAddScreen() {
  ViewScreen.hide();
  AddScreen.show();
  resetValues();
}

function loadUserCategories() {
  User_category.empty();
  User_category.append($('<option></option>').val('').html('Select'));
  $.each(CategoryList, function (key, value) {
    User_category.append($('<option></option>').val(CategoryList[key].user_category_id).html(CategoryList[key].user_category_name));
  });
}

function loadCountries() {
  Countries.empty();
  $.each(CountryList, function (key, value) {
    var optText = '<option></option>';
    if($.inArray(CountryList[key].country_id, Country_ids) >= 0){
      optText = '<option selected="selected"></option>';
    }
    Countries.append($(optText).val(CountryList[key].country_id).html(CountryList[key].country_name));
  });
  Countries.multiselect('rebuild');
}

function loadDomains() {
  Domains.empty();
  $.each(DomainsList, function (key, value) {
    var optText = '<option></option>';
    if($.inArray(DomainsList[key].domain_id, Domain_ids) >= 0){
      optText = '<option selected="selected"></option>';
    }
    Domains.append($(optText).val(DomainsList[key].domain_id).html(DomainsList[key].domain_name));
  });
  Domains.multiselect('rebuild');
}


// Api failure messages
function possibleFailures(error) {
  if (error == 'EmailIDAlreadyExists') {
    displayMessage(msg.emailid_exists);
  }
  else if (error == 'ContactNumberAlreadyExists') {
    displayMessage(msg.contactno_exists);
  }
  else if (error == 'EmployeeCodeAlreadyExists') {
    displayMessage(msg.employeeid_exists);
  }
  else if (error == 'InvalidUserId') {
    displayMessage(msg.invalid_userid);
  }
  else if (error == 'InvalidUserId') {
    displayMessage(message.invalid_userid);
  }
  else {
    displayMessage(error);
  }
}
// View field values in edit mode
function displayEdit(userId) {
  showAddScreen();
  //displayMessage('');
  User_id.val(parseInt(userId));
  for (var v in UsersList) {
    data = UsersList[v];
    if (data.user_id == userId) {
      userCatId = data.user_category_id;
      // loadFormCategories();
      $('#usercatval option[value = ' + userCatId + ']').attr('selected', 'selected');
      Emp_name.val(data.employee_name);
      Emp_code.val(data.employee_code);
      Address.val(data.address);
      Designation.val(data.designation);
      if (data.contact_no != null) {
        var contact = data.contact_no.split('-');
        Country_code.val(contact[0]);
        Area_code.val(contact[1]);
        Contact_no.val(contact[2]);
      }
      var mobile = data.mobile_no.split('-');
      mCountry_code.val(mobile[0]);
      Mobile_no.val(mobile[1]);
      User_group_val.val(data.user_group_id);
      for (var k in UserGroupList) {
        if (UserGroupList[k].user_group_id == data.user_group_id) {
          User_group_ac.val(UserGroupList[k].user_group_name);
          break;
        }
      }
      Designation.val(data.designation);
      Address.val(data.address);

      Domain_ids = data.domain_ids;
      loadDomains();

      Country_ids = data.country_ids;
      loadCountries()

      Email_id.val(data.email_id);
      break;
    }
  }
}
// Submit button process
function submitUserData(){
  function validateMaxLength(key_name, value, show_name) {
    e_n_msg = validateLength(key_name, value.trim())
    if (e_n_msg != true) {
      displayMessage(show_name + e_n_msg);
      return false;
    }
    return true;
  }

  function validateMandatory() {
    //displayMessage('');
    if (User_category.val().trim().length == 0) {
      displayMessage(msg.user_category_required);
      User_category.focus();
      return false;
    }

    if (Emp_name.val().trim().length == 0) {
      displayMessage(msg.employeename_required);
      Emp_name.focus();
      return false;
    }
    else {
      validateMaxLength('employeename', Emp_name.val(), "Employee name");
    }

    if (Emp_code.val().trim().length == 0) {
      displayMessage(msg.employeeid_required);
      Emp_code.focus();
      return false;
    }
    else {
      validateMaxLength('employeeid', Emp_code.val(), "Employee id");
    }

    if (Email_id.val().trim().length == 0) {
      displayMessage(msg.emailid_required);
      Email_id.focus();
      return false;
    }
    else {
      validateMaxLength('email_id', Email_id.val(), "Email id");
      var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
      if (reg.test(Email_id.val().trim()) == false) {
        displayMessage(msg.invalid_emailid);
        Email_id.focus();
        return false;
      }
    }

    if (Mobile_no.val().trim().length == 0) {
      displayMessage(msg.mobile_required);
      Mobile_no.focus();
      return false;
    }

    if (User_group_val.val().trim().length == 0) {
      displayMessage(msg.usergroup_required);
      User_group_ac.focus();
      return false;
    }
    
    if (Countries.val() == null) {
      displayMessage(msg.country_required);
      Countries.focus();
      return false;
    }else{
      Country_ids = Countries.val().map(Number);
    }

    if (Domains.val() == null) {
      displayMessage(msg.domain_required);
      Domains.focus();
      return false;
    }else{
      Domain_ids=Domains.val().map(Number);
    }

    return true;
  }

  function process_submit() {
    if (validateMandatory() == false)
    {
      return false;
    }
    else {
      userDetail = {
        'u_cat_id': parseInt(User_category.val()),
        'ug_id': parseInt(User_group_val.val().trim()),
        'employee_name': Emp_name.val().trim(),
        'employee_code': Emp_code.val().trim(),
        'email_id': Email_id.val().trim(),
        'contact_no': Country_code.val().trim() + '-' + Area_code.val().trim() + '-' + Contact_no.val().trim(),
        'mobile_no':  mCountry_code.val().trim() + '-' + Mobile_no.val().trim(),
        'address': Address.val().trim(),
        'designation': Designation.val().trim(),
        'country_ids':  Country_ids,
        'domain_ids': Domain_ids,
      };
      console.log(userDetail);
      if (User_id.val() == '') {
        mirror.saveAdminUser(userDetail, function(error, response) {
          if (error == null) {
            displaySuccessMessage(msg.save_success);
            showList();
          }
          else {
            possibleFailures(error);
          }
        });
      }
      else {
        userDetail["user_id"] = parseInt(User_id.val());
        mirror.updateAdminUser(userDetail, function(error, response) {
          if (error == null) {
            displaySuccessMessage(msg.update_success);
            showList();
          }
          else {
            possibleFailures(error);
          }
        });
      }
    }
  }
  process_submit();
}
// change status event action
function changeStatus(userId, isActive) {
  if(isActive == true){
    isActive = false;
  }else{
    isActive = true;
  }
  mirror.changeAdminUserStatus(userId, isActive, function(error, response) {
    if (error == null) {
      showList();
    }
    else {
      possibleFailures(error);
    }
  });
}
// disable action
function changeDisable(userId, isDisable) {
  if(isDisable == true){
    isDisable = false;
  }else{
    isDisable = true;
  }
  mirror.changeAdminDisaleStatus(userId, isDisable, function(error, response) {
    if (error == null) {
      showList();
    }
    else {
      possibleFailures(error);
    }
  });
}

// tab key order
function fieldOrder() {
  Emp_name.on('input', function (e) {
    this.value = isCommon_Name($(this));
  });
  Emp_code.on('input', function (e) {
    this.value = isCommon($(this));
  });
  Address.on('input', function (e) {
    this.value = isCommon_Address($(this));
  });
  Designation.on('input', function (e) {
    this.value = isCommon($(this));
  });
  Area_code.on('input', function (e) {
    this.value = isNumbers($(this));
  });
  Country_code.on('input', function (e) {
    this.value = isNumbers_Countrycode($(this));
  });
  Contact_no.on('input', function (e) {
    this.value = isNumbers($(this));
  });
  mCountry_code.on('input', function (e) {
    this.value = isNumbers_Countrycode($(this));
  });
  Mobile_no.on('input', function (e) {
    this.value = isNumbers_Countrycode($(this));
  });
}
// List filter process
function processFilter() {
  ename_search = $('#search-employee-name').val().toLowerCase();
  uname_search = $('#search-user-id').val().toLowerCase();
  email_search = $('#search-email-id').val().toLowerCase();
  cat_search = $('#search-category-name').val().toLowerCase();

  usr_status = $('.search-status-li.active').attr('value');
  usr_disable = $('.search-disable-li.active').attr('value');

  filteredList = []
  for(var v in UsersList) {
    data = UsersList[v];
    en = data.employee_name.toLowerCase();
    ec = data.employee_code.toLowerCase();
    concat = ec + ' - ' + en;
    uname = data.username_id;
    if (uname)
      uname = uname.toLowerCase();
    else
      uname = '';
    email = data.email_id.toLowerCase();
    cat = data.user_category_name.toLowerCase();
    if (
      (~concat.indexOf(ename_search)) && (~uname.indexOf(uname_search)) &&
      (~email.indexOf(email_search)) && (~cat.indexOf(cat_search))
    ){
      if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active) &&
        (usr_disable == 'all' || Boolean(parseInt(usr_disable)) == data.is_disable)){
        filteredList.push(data);
      }
      
    }
  }
  renderUserList(filteredList);
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

function pageControls() {

  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }
    processFilter();
  });

  Search_disable_ul.click(function (event) {
    Search_disable_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    Search_disable.removeClass();
    if(currentClass != undefined){
      Search_disable.addClass(currentClass);
      Search_disable.text('');
    }else{
      Search_disable.addClass('fa');
      Search_disable.text('All');
    }
    processFilter();
  });

  User_group_ac.keyup(function(e){
    var condition_fields = ["is_active"];
    var condition_values = [true];
    if(User_category.val() != ''){
      condition_fields.push("user_category_id");
      condition_values.push(User_category.val());

      var text_val = $(this).val();
      commonAutoComplete(
        e, ACUserGroup, User_group_val, text_val, 
        UserGroupList, "user_group_name", "user_group_id", function (val) {
            onAutoCompleteSuccess(User_group_ac, User_group_val, val);
        }, condition_fields, condition_values);
    }
  });

  FilterBox.keyup(function() {
    processFilter();
  });
  CancelButton.click(function() {
    showList();
  });
  AddButton.click(function() {
    showAddScreen();
  });
  SubmitButton.click(function() {
    submitUserData();
  });
  UserStatus.change(function() {
    processFilter();
  });
}
// page load
function initialize() {
  renderUserList(null);
  pageControls();
  //Emp_name.focus();
  fieldOrder();
}

$(document).ready(function () {
  initialize();
});
