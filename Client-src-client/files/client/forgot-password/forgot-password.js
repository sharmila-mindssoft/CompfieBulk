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
        'short_name': shortName,
        'login_type': 'Web'
      }
    ];
    var requestFrame = [
      shortName,
      request
    ];
    BASE_URL = '/api/';

  function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
  }

  $.ajax({
    url: BASE_URL + 'login',
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
        //initSession(response, shortName);
        callback(null, response);
      } else {
        callback(status, null);
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      rdata = JSON.parse(jqXHR.responseText);
      rdata = atob(rdata.substring(5));
      callback(rdata, null);
    }
  });
}


//submit forgot password process
$('#submit').click(function () {
  var username = $('#username').val().trim();
  var groupname = $('#shortname').val().trim();
  if (username.length == 0) {
    displayMessage('User Id Required');
  }else if(isLengthMinMax($('#username'), 1, 50, message.user_name_max50) == false){
    return false;
  }else if (groupname.length == 0) {
    displayMessage('Group Name Required');
  }else if(isLengthMinMax($('#shortname'), 1, 50, message.group_name_max50) == false){
    return false;
  } else {
    displayLoader();
    function onSuccess(data) {
      displaySuccessMessage('Password reset link has been sent to your email Id');
      $('#username').val('');
      $('#shortname').val('');
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
    processForgotpassword(username, groupname, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
});
$(document).ready(function () {
  $('#username').focus();
});
