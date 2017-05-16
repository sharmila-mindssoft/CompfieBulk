var passwordStrength = 'Weak';
var csrf_token = $('meta[name=csrf-token]').attr('content');
var max20 = 20;

// function displayMessage(message) {
//   $('.reset-password-error-message').text(message);
//   $('.reset-password-error-message').show();
// }
$('#submit').click(function () {
  $('.reset-password-error-message').html('');
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  var resetToken = reset_token;
  var newpassword = $('#newpassword').val().trim();
  var confirmpassword = $('#confirmpassword').val().trim();
  var checkLength = resetPasswordValidate();
  if (checkLength) {
    if (newpassword.length == 0) {
      displayMessage("New Password Required");
    } else if (confirmpassword.length == 0) {
      displayMessage("Confirm Password Required");
    } else if (confirmpassword != newpassword) {
      displayMessage("New Password & Confirm Password should match");
    } else if (passwordStrength == 'Weak') {
      displayMessage("Password should not be Weak");
    } else {
      url = window.location.href;
      url_parameters = url.split('/');
      reset_token = url_parameters[url_parameters.length - 1];
      if (url_parameters[url_parameters.length - 2] != 'reset-password') {
        function onSuccess(data) {          
          displaySuccessMessage(message.password_reset_success);
          $('#newpassword').val('');
          $('#confirmpassword').val('');
        }
        function onFailure(error) {
          if (error == 'InvalidResetToken') {
            displayMessage(message.invalid_reset_token);
            return false;
          } else if (error == 'EnterDifferentPassword') {
            displayMessage(message.password_already_used);
            return false;
          } else {
            displayMessage(error);
          }
        }
        mirror.resetPassword(resetToken, newpassword, url_parameters[url_parameters.length - 2], function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      } else {
        function onSuccess(data) {
          displaySuccessMessage("Password Reset Successfully");
          $('#newpassword').val('');
          $('#confirmpassword').val('');
        }
        function onFailure(error) {
          if (error == 'InvalidResetToken') {
            displayMessage("Invalid Reset Token");
            return false;
          } else if (error == 'EnterDifferentPassword') {
            displayMessage("Password already used. Enter different password'");
            return false;
          } else {
            displayMessage(error);
          }
        }
        var request = [
          'ResetPassword',
          {
            'reset_token': resetToken,
            'new_password': newpassword,
            'short_name': null
          }
        ];
        call_api(request, function(status, data) {
            hideLoader();
            if (status == null) {
              onSuccess(data);
            } else {
              onFailure(status);
            }
        });

        // mirror.resetPassword(resetToken, newpassword, function (error, response) {
        //   if (error == null) {
        //     onSuccess(response);
        //   } else {
        //     onFailure(error);
        //   }
        // });
      }
    }
  }
});
function makekey()
{
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for( var i=0; i < 5; i++ )
      text += possible.charAt(Math.floor(Math.random() * possible.length));
  return text;
}
function call_api(request, callback) {

    $.ajax({
        url: '/knowledge/api/login',
        type: 'POST',
        contentType: 'application/json',
        headers: { 'X-CSRFToken': csrf_token },
        data: makekey() + btoa(JSON.stringify(request, null, '')),
        success: function(data, textStatus, jqXHR) {
            data = atob(data.substring(5));
            data = JSON.parse(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            }
            else {
                callback(status, response);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = JSON.parse(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
           callback(rdata, null);
        }
    });
}

validateToken = function() {
    var paths = window.location.href.split("/");
    reset_token = paths[paths.length - 1];
    validate_api(reset_token);
    displayLoader();
    function validate_api(token) {
        var request = [
            "CheckRegistrationToken", {
                'reset_token': token
            }
        ];
        call_api(request, function(status, data) {
            hideLoader();
            if (status == null) {
                _rtoken = reset_token;
                IS_VALID = true;
            }
            else {
                displayMessage("Session expired");
                IS_VALID = false;
            }
        });
    }
};

function resetPasswordValidate() {
  if ($('#newpassword').val().trim().length > max20) {
    displayMessage('New Password' + message.should_not_exceed + max20 + ' characters');
    return false;
  } else if ($('#confirmpassword').val().trim().length > max20) {
    displayMessage('Confirm Password' + message.should_not_exceed + max20 + ' characters');
    return false;
  } else {
    displayMessage();
    return true;
  }
}

$(document).ready(function () {
  
  $('#newpassword').keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
    /*
        assigning keyup event to password field
        so everytime user type code will execute
      */
    passwordStrength = checkStrength($('#newpassword').val());
    if (passwordStrength == 'Strong') {
      $('#password-hint').css('display', 'none');
    } else {
      $('#password-hint').css('display', 'inline-block');
    }
    $('#pw-result').html(passwordStrength);
  });
  $('#confirmpassword').keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
  });
  function onSuccess(data) {
  }
  function onFailure(error) {
    displayMessage('Invalid Reset Token');
  }
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  validateToken();
    // mirror.validateResetToken(reset_token, function (error, response) {
    //   if (error == null) {
    //     onSuccess(response);
    //   } else {
    //     onFailure(error);
    //   }
    // });
  $('#newpassword').focus();
  $('#password-hint').css('display', 'none');
});
$('#newpassword').focus(function () {
  $('#password-hint').css('display', 'inline-block');
});
$('#newpassword').focusout(function () {
  $('#password-hint').css('display', 'none');
});
