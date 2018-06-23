function displayLoader() {
    $(".loading-indicator-spin").show();
}

function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function displayMessage(message) {
    if ($('.toast-error').css('display') == "block") {
        $('.toast').remove();
    }
    var toastPan = import_toast();
    Command: toastPan["error"](message)
}

function displaySuccessMessage(message) {
    if ($('.toast-error').css('display') == "block") {
        $('.toast').remove();
    }
    var toastPan = import_toast();
    Command: toastPan["success"](message)

}

function import_toast() {
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    return toastr;

}

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
  displayLoader();
  var username = $('#username').val().trim();
  var groupname = $('#shortname').val().trim();
  if (username.length == 0) {
    displayMessage('User Id Required');
    return false;
  }else if(username.length > 50){
    displayMessage("User Name is maximum 50 characters Allowed");
    return false;
  }else if (groupname.length == 0) {
    displayMessage('Group Short Name Required');
    return false;
  }else if(groupname.length > 50){
    displayMessage("Group Short Name is maximum 50 characters Allowed");
    return false;
  } else {
    
    function onSuccess(data) {
      displaySuccessMessage('Password reset link has been sent to your email Id');
      $('#username').val('');
      $('#shortname').val('');
      hideLoader();
    }
    function onFailure(error) {
      if (error == 'InvalidUserName') {
        displayMessage("No User Exists");
      } else if (error == "client not found") {
        displayMessage("Invalid shortname");
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

$(document).keydown(function(e) {
    if ((e.keyCode == 116 && e.ctrlKey) || e.keyCode == 116) {
        window.location.reload(true);
    }
});

$(document).ready(function () {
  $('#username').focus();
});
