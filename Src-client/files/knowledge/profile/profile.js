function initialize() {
  var userprofile = mirror.getUserProfile();
  clearMessage();
  console.log(userprofile)
  var contactNo = userprofile.contact_no.split('-');
  $('.employee-name').text(userprofile.employee_name);
  if (userprofile.designation == null || userprofile.designation == 'None') {
    $('.designation').text('');
  } else {
    $('.designation').text(userprofile.designation);
  }
  $('.email-id').val(userprofile.email_id);
  $('.countrycode').val(contactNo[0]);
  $('.areacode').val(contactNo[1]);
  $('.mobile').val(contactNo[2]);
  $('.employee-id').text(userprofile.employee_code);
  $('.usergroup').text(userprofile.user_group);
  if (userprofile.address == null || userprofile.address == 'None') {
    $('.textarea.address').val('');
  } else {
    $('textarea.address').val(userprofile.address);
  }
  $('.userid').val(userprofile.user_id);
}
$('#submit').click(function () {
  var checkLength = profileValidate();
  if (checkLength) {
    var countrycode = $('.countrycode').val().trim();
    var areacode = $('.areacode').val().trim();
    var mobile = $('.mobile').val().trim();
    var address = $('.address').val().trim();
    path = window.location.pathname;
    if (path == '/knowledge/profile') {
      function onSuccess(data) {
        initialize();
        displayMessage(message.updated_success);
      }
      function onFailure(error) {
        displayMessage(error);
      }
      mirror.updateUserProfile(countrycode + '-' + areacode + '-' + mobile, address, function (error, response) {
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
$('#address').on('input', function (e) {
  this.value = isCommon_Address($(this));
});
$('#mobile').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#areacode').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#countrycode').on('input', function (e) {
  this.value = isNumbers_Countrycode($(this));
});