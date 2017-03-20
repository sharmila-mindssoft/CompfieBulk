var passwordStrength = 'Weak';
function displayMessage(message) {
  $('.error-message').html(message);
  $('.error-message').show();
}
$('#submit').click(function () {
  $('.error-message').html('');
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  var resetToken = reset_token;
  var newpassword = $('#newpassword').val().trim();
  var confirmpassword = $('#confirmpassword').val().trim();
  var checkLength = resetPasswordValidate();
  if (checkLength) {
    if (newpassword.length == 0) {
      $('.error-message').html(message.npassword_required);
    } else if (confirmpassword.length == 0) {
      $('.error-message').html(message.conpassword_required);
    } else if (confirmpassword != newpassword) {
      $('.error-message').html(message.password_notmatch);
    } else if (passwordStrength == 'Weak') {
      $('.error-message').html(message.password_weak);
    } else {
      url = window.location.href;
      url_parameters = url.split('/');
      reset_token = url_parameters[url_parameters.length - 1];
      if (url_parameters[url_parameters.length - 2] != 'reset-password') {
        function onSuccess(data) {
          displayMessage(message.password_reset_success);
          $('#newpassword').val('');
          $('#confirmpassword').val('');
        }
        function onFailure(error) {
          if (error == 'InvalidResetToken') {
            displayMessage(message.invalid_reset_token);
          } else if (error == 'EnterDifferentPassword') {
            displayMessage(message.password_already_used);
          } else {
            displayMessage(error);
          }
        }
        client_mirror.resetPassword(resetToken, newpassword, url_parameters[url_parameters.length - 2], function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      } else {
        function onSuccess(data) {
          displayMessage(message.password_reset_success);
          $('#newpassword').val('');
          $('#confirmpassword').val('');
        }
        function onFailure(error) {
          if (error == 'InvalidResetToken') {
            displayMessage(message.invalid_reset_token);
          } else if (error == 'EnterDifferentPassword') {
            displayMessage(message.password_already_used);
          } else {
            displayMessage(error);
          }
        }
        mirror.resetPassword(resetToken, newpassword, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
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
function call_api(request, callback) {
    var requestFrame = [
      'kitkat',
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

        /*url: '/knowledge/api/login',
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
        }*/
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

/*  function onSuccess(data) {
  }
  function onFailure(error) {
    $('.error-message').html('Invalid Reset Token');
    $('.error-message').show();
  }
  url = window.location.href;
  url_parameters = url.split('/');
  reset_token = url_parameters[url_parameters.length - 1];
  if (url_parameters[url_parameters.length - 2] != 'reset-password') {
    client_mirror.validateResetToken(reset_token, url_parameters[url_parameters.length - 2], function (error, response) {
      alert(error)
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  } else {
    mirror.validateResetToken(reset_token, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }*/
});
$('#newpassword').focus(function () {
  $('#password-hint').css('display', 'inline-block');
});
$('#newpassword').focusout(function () {
  $('#password-hint').css('display', 'none');
});