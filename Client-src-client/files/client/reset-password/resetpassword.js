var passwordStrength = 'Weak';


function clearFPMessage() {
  $('.forgot-password-error-message').hide();
  $('.forgot-password-error-message span').text('');
}
function displayFPMessage(message) {
  $('.forgot-password-error-message span').text(message);
  $('.forgot-password-error-message').show();
}

function resetPasswordValidate() {
  if ($('#newpassword').val().trim().length > 20) {
    displayFPMessage('New Password Should not exceed 20 characters');
    return false;
  } else if ($('#confirmpassword').val().trim().length > 20) {
    displayFPMessage('Confirm Password Should not exceed 20 characters');
    return false;
  } else {
    displayFPMessage();
    return true;
  }
}

$('#btn_submit').click(function () {
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  var resetToken = reset_token;
  var newpassword = $('#newpassword').val().trim();
  var confirmpassword = $('#confirmpassword').val().trim();
  var checkLength = resetPasswordValidate();
  if (checkLength) {
    if (newpassword.length == 0) {
      displayFPMessage("New Password Required");
    } else if (confirmpassword.length == 0) {
      displayFPMessage("Confirm Password Required");
    } else if (confirmpassword != newpassword) {
      displayFPMessage("New Password & Confirm Password should match");
    } else if (passwordStrength == 'Weak') {
      displayFPMessage("Password should not be Weak");
    } else {
      url = window.location.href;
      url_parameters = url.split('/');
      reset_token = url_parameters[url_parameters.length - 1];
      if (url_parameters[url_parameters.length - 2] != 'reset-password') {
        function onSuccess(data) {
          displayFPMessage("Password Reset Successfully");
          $('#newpassword').val('');
          $('#confirmpassword').val('');
        }
        function onFailure(error) {
          if (error == 'InvalidResetToken') {
            displayFPMessage('Invalid Reset Token');
          } else if (error == 'EnterDifferentPassword') {
            displayFPMessage('Password Already Used');
          } else {
            displayFPMessage(error);
          }
        }
        var request = [
          'ResetPassword',
          {
            'reset_token': resetToken,
            'new_password': newpassword,
            'short_name': url_parameters[url_parameters.length - 2]
          }
        ];
        call_api(request, url_parameters[url_parameters.length - 2], function(status, data) {
            hideLoader();
            if (status == null) {
              onSuccess(data);
            } else {
              onFailure(status);
            }
        });
      }
    }
  }
});

function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
}

function makekey()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}
function call_api(request, short_name, callback) {
    var requestFrame = [
      short_name,
      request
    ];

    $.ajax({
      url: '/api/login',
      headers: { 'X-Xsrftoken': getCookie('_xsrf') },
      type: 'POST',
      contentType: 'application/json',
      data: makekey() + btoa(JSON.stringify(requestFrame, null, ' ')),
      success: function (data, textStatus, jqXHR) {
        data = atob(data.substring(5));
        data = JSON.parse(data);
        var status = data[0];
        var response = data[1];
        matchString = 'success';
        if (status.toLowerCase().indexOf(matchString) != -1) {
          callback(null, response);
        } else {
          callback(data, null);
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        rdata = JSON.parse(jqXHR.responseText);
        rdata = atob(rdata.substring(5));
        callback(rdata, null);
      }
    });
}

validateToken = function() {
    var paths = window.location.href.split("/");
    reset_token = paths[paths.length - 1];
    short_name = paths[paths.length - 2];
    validate_api(reset_token);
    displayLoader();
    function validate_api(token) {
        var request = [
            "ResetTokenValidation", {
                'reset_token': reset_token,
                'short_name': short_name

            }
        ];
        call_api(request, short_name, function(status, data) {
            hideLoader();
            if (status == null) {
                _rtoken = reset_token;
                IS_VALID = true;
            }
            else {
                displayFPMessage("Session expired");
                IS_VALID = false;
            }
        });
    }
};

$(document).ready(function () {
  $('#newpassword').keyup('input', function (event) {
    this.value = this.value.replace(/\s/g, '');
   
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
    displayFPMessage('Invalid Reset Token');
  }
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  validateToken();
});
$('#newpassword').focus(function () {
  $('#password-hint').css('display', 'inline-block');
});
$('#newpassword').focusout(function () {
  $('#password-hint').css('display', 'none');
});