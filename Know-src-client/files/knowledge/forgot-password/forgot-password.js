var csrf_token = $('meta[name=csrf-token]').attr('content')
// function clearMessage() {
//   $('.error-message').hide();
//   $('.error-message').text('');
// }
// function displayMessage(message) {
//   $('.error-message').text(message);
//   $('.error-message').show();
// }
// function displayLoader() {
//   $('.loading-indicator-spin').show();
// }
// function hideLoader() {
//   $('.loading-indicator-spin').hide();
// }
//check the url is client or knowledge
function getShortName() {
  var pathArray = window.location.pathname.split('/');
  short_name = null;
  if (typeof pathArray[2] === 'undefined') {
    short_name = null;
  }
  if (pathArray[1] == 'knowledge') {
    short_name = null;
  } else if (pathArray[2] === 'login') {
    short_name = null;
  } else {
    short_name = pathArray[2];
  }
  return short_name;
}
$('.btn-forgotpassword-cancel').click(function () {
  window.location.href = '/knowledge/login';
});
//validation email
function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test($email);
}
function makekey()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function parseJSON(data) {
    return JSON.parse(data);
}
function processForgotpassword(username, shortName, callback) {
    displayLoader();
    var request = [
      'ForgotPassword',
      {
        'username': username,
        'short_name': null,
        'login_type': 'Web'
      }
    ];
    if (shortName == null) {
      var requestFrame = request;
      BASE_URL = '/knowledge/api/';
    } else {
      var requestFrame = [
        shortName,
        request
      ];
      BASE_URL = '/api/';
    }

  // jQuery.post(BASE_URL + 'login', JSON.stringify(requestFrame, null, ' '), function (data) {
  //   var data = JSON.parse(data);
  //   if (typeof data != 'string') {
  //     var status = data[0];
  //     var response = data[1];
  //   } else {
  //     status = data;
  //   }
  //   matchString = 'success';
  //   if (status.toLowerCase().indexOf(matchString) != -1) {
  //     callback(null, response);
  //   } else {
  //     callback(status, null);
  //   }
  // });
  actula_data = JSON.stringify(requestFrame, null, ' ');
  console.log(actula_data);
  $.ajax({
    url: BASE_URL + 'login',
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    contentType: 'application/json',
    data: makekey() + btoa(actula_data),
    success: function (data, textStatus, jqXHR) {
      console.log(data);
      data = atob(data.substring(5));
      data = JSON.parse(data);
      var status = data[0];
      var response = data[1];

      matchString = 'success';
      if (status.toLowerCase().indexOf(matchString) != -1) {
        callback(null, response);
      } else {
        callback(status, null);
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      rdata = parseJSON(jqXHR.responseText);
      rdata = atob(rdata.substring(5));
      displayMessage(rdata);
      callback(rdata, errorThrown);
    }
  });
}

//submit forgot password process
$('#submit').click(function () {
  $('.forgot-password-error-message').html('');
  var username = $('#username').val().trim();
  if (username.length == 0) {
    displayMessage('Username Required');
    return false;
  }
  else if(username.length > 20){
    displayMessage('Username should not exceed 20 characters'); 
    return false;
  } else {
    displayLoader();
    function onSuccess(data) {
      displaySuccessMessage('Password reset link has been sent to your email Id');
      $('#username').val('');
      hideLoader();
    }
    function onFailure(error) {
      if (error == 'InvalidUserName') {
        displayMessage("No User Exists");
      } else {
        displayMessage(error);
      }
      hideLoader();
    }
    if (getShortName() == null || getShortName() == 'forgot-password') {
      processForgotpassword(username, null, function (error, response) {
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
  $('#username').focus();
});
