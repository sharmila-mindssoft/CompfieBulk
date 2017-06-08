var passwordStrength = 'Weak';
var max20 = 20;
var CurrentPassword = $('#currentpassword');
var NewPassword = $('#newpassword');
var ConfirmPassword = $('#confirmpassword');

var SubmitButton = $('#btn_submit');
var PasswordHintSpan = $('#password-hint');


//save change password process for knowledge
function changePasswordValidate() {
    if ($('#currentpassword').val().trim().length > max20) {
        displayMessage('Current Password' + message.should_not_exceed + max20 + ' characters');
        return false;
    } else if ($('#newpassword').val().trim().length > max20) {
        displayMessage('New Password' + message.should_not_exceed + max20 + ' characters');
        return false;
    } else if ($('#confirmpassword').val().trim().length > max20) {
        displayMessage('Confirm Password' + message.should_not_exceed + max20 + ' characters');
        return false;
    } else {
        //displayMessage();
        return true;
    }
}
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
    } else if (passwordStrength == 'Weak') {
      displayMessage(message.password_weak);
    } else {
      function onSuccess(data) {
        //displaySuccessMessage(message.password_changed_success);
        //client_mirror.logout();
        confirm_ok_alert(message.password_changed_success, null);
      }
      function onFailure(error) {
        if (error == 'InvalidCurrentPassword') {
          displayMessage(message.invalid_cpassword);
        } else if (error == 'CurrentandNewPasswordSame') {
          displayMessage(message.current_password_same);
        } else if(error == 'CurrentandConfirmPasswordSame') {
          displayMessage(message.confirm_password_same);
        } else if (confirmpassword != newpassword) {
          displayMessage(message.password_notmatch);
        }else {
          displayMessage(error);
        }
      }
      client_mirror.changePassword(currentpassword, newpassword, confirmpassword, function (error, response) {
        console.log(error, response)
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
  }
});



$(document).ready(function () {
  CurrentPassword.focus();
  CurrentPassword.keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
  });
    NewPassword.keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
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