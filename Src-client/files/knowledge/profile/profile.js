var EmployeeName  = $('.employee-name');
var Designation  = $('.designation');
var EmailId  = $('.email-id');
var CountryCode  = $('.countrycode');
var AreaCode  = $('.areacode');
var ContactNo  = $('.contactno');
var MCountryCode  = $('.mcountrycode');
var MobileNo  = $('.mobileno');
var EmployeeId  = $('.employee-id');
var UserId  = $('.user-id');
var UserGroup = $('.user-group');
var Address = $('.address');

var SubmitBtn = $('#submit');

function initialize() {
  var userprofile = mirror.getUserProfile();
  clearMessage();
  console.log(userprofile)

  EmployeeName.text(userprofile.employee_name);

  if (userprofile.designation != null) {
    Designation.text(userprofile.designation);
  }

  EmailId.val(userprofile.email_id);

  if(userprofile.contact_no != null){
    var cNo = userprofile.contact_no.split('-');
    CountryCode.val(cNo[0]);
    AreaCode.val(cNo[1]);
    ContactNo.val(cNo[2]);
  }

  if(userprofile.mobile_no != null){
    var mNo = userprofile.mobile_no.split('-');
    MCountryCode.val(mNo[0]);
    MobileNo.val(mNo[1]);
  }

  EmployeeId.text(userprofile.employee_code);

  UserId.text(userprofile.user_name);

  UserGroup.text(userprofile.user_group);

  if (userprofile.address != null) {
    Address.val(userprofile.address);
  }
}


//validate max length
function validateMaxLength(key_name, value, show_name) {
  e_n_msg = validateLength(key_name, value.trim())
  if (e_n_msg != true) {
    displayMessage(show_name + e_n_msg);
    return false;
  }
  return true;
}


function validateMandatory() {
  if (EmailId.val().trim().length == 0) {
    displayMessage(msg.emailid_required);
    Email_id.focus();
    return false;
  }
  else {
    validateMaxLength('email_id', EmailId.val(), "Email id");
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (reg.test(EmailId.val().trim()) == false) {
      displayMessage(msg.invalid_emailid);
      EmailId.focus();
      return false;
    }
  }

  if (MobileNo.val().trim().length == 0) {
    displayMessage(msg.mobile_required);
    MobileNo.focus();
    return false;
  }
  return true;
}

SubmitBtn.click(function () {
/*  var checkLength = profileValidate();
  if (checkLength) {*/

    if (validateMandatory())
    {
      var countrycode_ = CountryCode.val().trim();
      var areacode_ = AreaCode.val().trim();
      var contactno_ = ContactNo.val().trim();
      var address_ = Address.val().trim();

      var emailid_ = EmailId.val().trim();
      var mcountrycode_ = MCountryCode.val().trim();
      var mobileno_ = MobileNo.val().trim();

      path = window.location.pathname;
      if (path == '/knowledge/profile') {
        function onSuccess(data) {
          initialize();
          displaySuccessMessage(message.updated_success);
        }
        function onFailure(error) {
          displayMessage(error);
        }
        mirror.updateUserProfile(countrycode_ + '-' + areacode_ + '-' + contactno_, address_, mcountrycode_ + '-' + mobileno_, emailid_, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      }
    }
  
});


$(function () {
  initialize();
});

Address.on('input', function (e) {
  this.value = isCommon_Address($(this));
});
ContactNo.on('input', function (e) {
  this.value = isNumbers($(this));
});
AreaCode.on('input', function (e) {
  this.value = isNumbers($(this));
});
CountryCode.on('input', function (e) {
  this.value = isNumbers_Countrycode($(this));
});
MCountryCode.on('input', function (e) {
  this.value = isNumbers_Countrycode($(this));
});
MobileNo.on('input', function (e) {
  this.value = isNumbers($(this));
});