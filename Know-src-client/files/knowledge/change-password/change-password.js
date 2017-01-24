var passwordStrength = 'Weak';

var CurrentPassword = $('#currentpassword');
var NewPassword = $('#newpassword');
var ConfirmPassword = $('#confirmpassword');

var SubmitButton = $('#submit');
var PasswordHintSpan = $('#password-hint');


//save change password process for knowledge
SubmitButton.click(function () {
  var checkLength = changePasswordValidate();
  if (checkLength) {
    var currentpassword = CurrentPassword.val().trim();
    var newpassword = NewPassword.val().trim();
    var confirmpassword = ConfirmPassword.val().trim();

    if (currentpassword.length == 0) {
      displayMessage(message.cpassword_required);
    } else if (newpassword.length == 0) {
      displayMessage(message.npassword_required);
    } else if (confirmpassword.length == 0) {
      displayMessage(message.conpassword_required);
    } else if (confirmpassword != newpassword) {
      displayMessage(message.password_notmatch);
    } else if (passwordStrength == 'Weak') {
      displayMessage(message.password_weak);
    } else {
      function onSuccess(data) {
        displaySuccessMessage(message.password_changed_success);
        mirror.logout();
      }
      function onFailure(error) {
        if (error == 'InvalidCurrentPassword') {
          displayMessage(message.invalid_cpassword);
        }else if (error == 'CurrentandNewPasswordSame') {
          displayMessage(message.current_new_password_same);
        } else {
          displayMessage(error);
        }
      }
      mirror.changePassword(currentpassword, newpassword, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
  }
});

function getItemObject(form_url, form_name) {
  var itemObject = $('#nav-bar-templates .sub-menu-item li').clone();
  if (form_url !== null)
    $('.menu-url', itemObject).attr('href', form_url);
    $('.menu-item', itemObject).text(form_name);
    return itemObject;
}

$(document).ready(function () {
  CurrentPassword.focus();
  CurrentPassword.keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
  });
    NewPassword.keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
    /*
        assigning keyup event to password field
        so everytime user type code will execute
      */
    passwordStrength = checkStrength(NewPassword.val());
    if (passwordStrength == 'Strong') {
      PasswordHintSpan.css('display', 'none');
    } else {
      PasswordHintSpan.css('display', 'inline-block');
    }
    $('#pw-result').html(passwordStrength);
  });
  ConfirmPassword.keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
  });
});

NewPassword.focus(function () {
  PasswordHintSpan.css('display', 'inline-block');
});
NewPassword.focusout(function () {
  PasswordHintSpan.css('display', 'none');
});