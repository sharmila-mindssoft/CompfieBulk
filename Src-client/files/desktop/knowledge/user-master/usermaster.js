
var UsersList;
var DomainsList;
var CountryList;
var CategoryList;
var UserGroupList;

// Add screen fields
var AddScreen = $('#user-add');
var ViewScreen = $('#user-view');
var FilterBox = $('.filter-text-box');
var AddButton = $('.btn-user-add');
var CancelButton = $('.btn-user-cancel');
var SubmitButton = $('.btn-submit');

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
var Country = $("#countryselected");
var Domains = $('#domainselected');
var Select_Box = $('#selectboxview');
var Select_Box_Country = $('#selectboxview-country');
var Domain_li_list = $('#ulist');
var Country_li_list = $('#ulist-country');

var Domain_li_active = "active_selectbox";
var Country_li_active = "active_selectbox_country";

var Domain_ids = [];
var Country_ids = [];
var item_selected = '';
var msg = message;
// Confirmation dialog
function popupWarning(message, callback) {
  var Warning_popup = $('.warning-confirm');
  Warning_popup.dialog({
    title: msg.title_status_change,
    buttons: {
      Ok: function() {
        $(this).dialog('close');
        callback(true);
      },
      Cancel: function() {
        $(this).dialog('close');
        callback(false);
      }
    },
    open: function() {
      $('.warning-message').html(message);
    }
  });
}
function sendCredentials(_u_id, _u_name, _e_id ) {
  req_dict = {
    'user_id': _u_id,
    'username': _u_name,
    'email_id': _e_id
  };
  custom_alert(req_dict);
  mirror.sendRegistration(req_dict, function(error, response) {

    if (error == null) {
      custom_alert(msg.resend);
    }
    else {
      custom_alert(error);
    }

  });
}
// User List render process
function renderUserList(response) {
    FilterBox.val('');
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
            sendCredentials(v.user_id, ename, v.email_id);
          });
        }
        else {
          $('.popup-link', rowClone).hide();
        }
        // $('.user-group', rowClone).text(usergroup);
        // $('.designation', rowClone).text(designation);
        $('.edit-icon').attr('title', 'Edit');
        $('.edit-icon', rowClone).on('click', function () {
          displayEdit(v.user_id);
        });

        if (v.is_active == true){
          classValue = "active-icon";
          $('.status', rowClone).addClass(classValue);
          $('.active-icon', rowClone).attr('title', msg.active_tooltip);
        }
        else{
          classValue = "inactive-icon";
          $('.status', rowClone).addClass(classValue);
          $('.inactive-icon', rowClone).attr('title', msg.deactive_tooltip);
        }

        $('.status', rowClone).on('click', function () {
          if (v.is_active == true) {
            passStatus = false;
          }
          else {
            passStatus = true;
          }
          changeStatus(v.user_id, passStatus);
        });
        if (v.is_disable == true) {
          classDValue = "enable-icon";
          $('.disable', rowClone).addClass(classDValue);
          $('.enable-icon', rowClone).attr('title', msg.disable_tooltip);
        }
        else{
          classDValue = "disable-icon";
          $('.disable', rowClone).addClass(classDValue);
          $('.disable-icon', rowClone).attr('title', msg.enable_tooltip);
        }

        $('.disable', rowClone).on('click', function () {
          if (v.is_disable == true)
            passDstatus = false;
          else
            passDstatus = true;
          changeDisable(v.user_id, passDstatus);
        });
        $('.tbody-user-list').append(rowClone);
        j = j + 1;
      });
    }

    fetchUserData = function() {
      mirror.getAdminUserList(function(error, response) {
        if (error != null) {
          custom_alert(error);
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
}

function showList() {
  renderUserList(null);
  Country_ids = [];
  Domain_ids = [];
  AddScreen.hide();
  ViewScreen.show();
}
// Enable Add/Edit Screen
function showAddScreen() {
  ViewScreen.hide();
  AddScreen.show();
  User_id.val('');
  displayMessage('');
  loadUserCategories();
  Country_ids = [];
  Domain_ids = [];
  User_category.focus();
}

function loadUserCategories() {
  var User_category = $('#usercatval');
  $.each(CategoryList, function (key, value) {
    User_category.append($('<option></option>').val(CategoryList[key].user_category_id).html(CategoryList[key].user_category_name));
  });
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
  displayMessage('');
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
      Domains.val(Domain_ids.length + ' Selected');
      Country_ids = data.country_ids;
      Country.val(Country_ids.length + ' Selected');
      Email_id.val(data.email_id);
      break;
    }
  }
}
// Submit button process
function submitUserData(){
  function validateMaxLength(key_name, value) {
    e_n_msg = validateLength(key_name, value.trim())
    if (e_n_msg != true) {
      displayMessage(e_n_msg);
      return false;
    }
  }

  function validateMandatory() {
    displayMessage('');
    if (length(Emp_name.val().trim()) == 0) {
      displayMessage(msg.employeename_required);
      Emp_name.focus();
      return false;
    }
    else {
      validateMaxLength('employeename', Emp_name.val());
    }

    if (length(Emp_code.val().trim()) == 0) {
      displayMessage(msg.employeeid_required);
      Emp_code.focus();
      return false;
    }
    else {
      validateMaxLength('employeeid', Emp_code.val());
    }

    if (length(Email_id.val().trim()) == 0) {
      displayMessage(msg.emailid_required);
      Email_id.focus();
      return false;
    }
    else {
      validateMaxLength('email_id', Email_id.val());
      var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
      if (reg.test(Email_id.val().trim()) == false) {
        displayMessage(msg.invalid_emailid);
        Email_id.focus();
        return false;
      }
    }

    if (length(User_group_val.val().trim()) == 0) {
      displayMessage(msg.usergroup_required);
      User_group_ac.focus();
      return false;
    }
    else if (Country_ids.length == 0) {
      displayMessage(msg.country_required);
      Country.focus().click();
      return false;
    }
    else if (Domain_ids.length == 0) {
      displayMessage(msg.domain_required);
      Domains.focus().click();
      return false;
    }
    return true;
  }

  function process_submit() {
    if (validateMandatory == false)
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
  var msgstatus = msg.deactive_message;
  if (isActive) {
    msgstatus = msg.active_message;
  }
  popupWarning(msgstatus , function(isConfirm) {
    if (isConfirm) {
      mirror.changeAdminUserStatus(userId, isActive, function(error, response) {
        if (error == null) {
          showList();
        }
        else {
          possibleFailures(error);
        }
      });
    }
  });
}
// disable action
function changeDisable(userId, isDisable) {
  var msgstatus = msg.enable_message;
  if (isDisable) {
    msgstatus = msg.disable_message;
  }
  popupWarning(msgstatus , function(isConfirm) {
    if (isConfirm) {
      mirror.changeAdminDisaleStatus(userId, isDisable, function(error, response) {
        if (error == null) {
          showList();
        }
        else {
          possibleFailures(error);
        }
      });
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
  uname_search = $('#search-username').val().toLowerCase();
  email_search = $('#search-email').val().toLowerCase();
  cat_search = $('#search-category').val().toLowerCase();
  status_search = $('#search-status').val();

  filteredList = []
  for(var v in UsersList) {
    data = UsersList[v];
    en = data.employee_name.toLowerCase();
    ec = data.employee_code.toLowerCase();
    concat = ec + ' - ' + en;
    uname = data.username.toLowerCase();
    email = data.email_id.toLowerCase();
    cat = data.category_name.toLowerCase();
    if (
      (~concat.indexOf(ename_search)) && (~uname.indexOf(uname_search)) &&
      (~email.indexOf(email_search)) && (~cat.indexOf(cat_search))
    ){
      filteredList.push(data);
    }
  }
  renderUserList(filteredList);
}

function active_click(element) {
  domains_class = 'active_selectbox';
  country_class = 'active_selectbox_country';

  e_type = ''
  klass = $(element).attr('class');
  if (e_type) {
    if (klass == domains_class) {
      $(element).removeClass(domains_class);
      Domain_ids.splice(Domain_ids.indexOf(parseInt(element.id)));
    }
    else {
      $(element).addClass(domains_class);
      Domain_ids.push(parseInt(element.id));
    }
    Domains.val(Domain_ids.length + ' Selected');
  }
  else {
    if (klass == country_class) {
      $(element).removeClass(country_class);
      Country_ids.splice(Country_ids.indexOf(parseInt(element.id)));
    }
    else {
      $(element).addClass(country_class);
      Country_ids.push(parseInt(element.id));
    }
    Country.val(Country_ids.length + ' Selected');
  }
}
function chkbox_select(item, id, name, active) {
  console.log(item);
  if (item == 'ulist') {
    a_klass = Domain_li_active;
  }
  else {
    a_klass = Country_li_active;
  }
  eveClick = "";
  li_string= ''
  if (active == true) {
    li_string  = '<li id="'+ id +'" class="'+ a_klass + '" onclick=active_click(this) >'+ name +'</li>';
  }
  else {
   li_string  = '<li id="'+ id +'" onclick=active_click(this) >'+ name +'</li>';
  }
  return li_string;
}

function pageControls() {
  function onKeyUpDownSelect(e, item) {
    // Key code : 40- down arrow , 38- up arrow , 32- space , 13- enter key.

    function highlight_row(n_item) {
      li_val = $('#' + item + ' li');
      li_val.removeClass('auto-selected');
      $('#' + item + ' li:eq('+ n_item + ')').addClass('auto-selected');
    }

    function remove_select(n_item, rklass) {
      $('#' + item + ' li:eq('+ n_item + ')').removeClass(rklass);
    }

    function add_select(n_item, aklass) {
      $('#' + item + ' li:eq('+ n_item + ')').addClass(aklass);
    }

    function get_id(n_item) {
      g_id = $('#' + item + ' li:eq('+ n_item + ')').attr('id');
      return g_id;
    }

    function get_class(n_item) {
      g_c = $('#' + item + ' li:eq('+ n_item + ')').attr('class');
      return g_c;
    }

    if(e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 32) {
      item_selected = '';
    }
    if (e.keyCode == 13) {
      Select_Box.hide();
      Select_Box_Country.hide()
    }

    if (e.keyCode == 40) {
      if(item_selected == '') {
        item_selected = 0;
      }
      else if (item_selected + 1 < li_val.length) {
        item_selected += 1;
      }
      highlight_row(item_selected);
      return false;
    }

    if (e.keyCode == 38) {
      if(item_selected == '') {
        item_selected = 0;
      }
      else if (item_selected > 0) {
        item_selected -= 1;
      }
      highlight_row(item_selected);
      return false;
    }

    if (e.keyCode == 32) {
      remove_select(item_selected, 'auto-selected');
      var multi_select_id = parseInt(get_id(item_selected));
      var item_class = get_class(item_selected);

      if (item == 'ulist') {
        // Domain select box
        if (item_class == Domain_li_active) {
          remove_select(item_selected, Domain_li_active);
          Domain_ids.splice(Domain_ids.indexOf(multi_select_id));
        }
        else {
          add_select(item_selected, Domain_li_active);
          Domain_ids.push(multi_select_id);
        }
        Domains.val(Domain_ids.length + ' Selected');
      }
      else {
        // country select box
        if (item == Country_li_active) {
          remove_select(item_selected, Country_li_active);
          Country_ids.splice(Country_ids.indexOf(multi_select_id));
        }
        else {
          add_select(item_selected, Country_li_active);
          Country_ids.push(multi_select_id);
        }
        Country.val(Country_ids.length + ' Selected');
      }
      return false;
    }
  }

  $('.hideselect').mouseleave(function() {
    item_selected = '';
    Select_Box.hide();
    Select_Box_Country.hide();
  });

  Domains.focus(function() {
    Select_Box.show();
    Domain_li_list.empty();
    var str = '';
    for (var i in DomainsList) {
      d = DomainsList[i];
      if (d.is_active == true) {
        active = false;
        if ($.inArray(d.domain_id, Domain_ids) >= 0) {
          active = true;
        }
        else {
          active = false;
        }
        str += chkbox_select('ulist', d.domain_id, d.domain_name, active);
      }
    }
    Domain_li_list.append(str);
  });
  Domains.keyup(function(e) {
    onKeyUpDownSelect(e, 'ulist');
    console.log(Domain_ids);
  });

  Country.focus(function() {
    Select_Box_Country.show();
    Country_li_list.empty();
    var str = '';
    for (var i in CountryList) {
      d = CountryList[i];
      if (d.is_active == true) {
        active = false;
        if ($.inArray(d.country_id, Country_ids) >= 0) {
          active = true;
        }
        else {
          active = false;
        }
        str += chkbox_select('ulist-country', d.country_id, d.country_name, active);
      }
    }
    Country_li_list.append(str);
  });
  Country.keyup(function(e) {
    onKeyUpDownSelect(e, 'ulist-country');
    console.log("countries");
    console.log(Country_ids);
  });

  User_group_ac.keyup(function(e) {
    var textVal = $(this).val();
    getUserGroupAutocomplete(e, User_category.val(), textVal, UserGroupList, function(val) {
      User_group_ac.val(val[1]);
      User_group_val.val(val[0]);
      User_group_ac.focus();
    });
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
}
// page load
function initialize() {
  renderUserList(null);
  pageControls();
  console.log(AddButton);
  Emp_name.focus();
  fieldOrder();
}

$(document).ready(function () {
  initialize();
});

