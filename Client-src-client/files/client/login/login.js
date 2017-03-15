var landingPage = null;
var captchaStatus = false;
var captchaText = null;
function clearLoginMessage() {
  $('.login-error-message').hide();
  $('.login-error-message span').text('');
}
function displayLoginMessage(message) {
  $('.loading-indicator-spin').hide();
  $('.login-error-message span').text(message);
  $('.login-error-message').show();
}
function displayLoginLoader() {
  $('.loading-indicator-spin').show();
}
function storeCaptcha(captcha_text) {
  window.sessionStorage.captcha = captcha_text;
}
function getCaptcha() {
  captcha = window.sessionStorage.captcha;
  if (captcha != null && captcha != undefined && captcha != 'undefined') {
    return captcha;
  } else {
    return null;
  }
}
function clearCaptcha() {
  delete window.sessionStorage.captcha;
}
function initSession(userProfile, shortName) {
  setLandingPage(userProfile);
  window.sessionStorage.userInfo = JSON.stringify(userProfile, null, ' ');
  console.log(window.sessionStorage.userInfo);
  if (shortName !== null) {
    window.localStorage.shortName = shortName;
  }
}
function setLandingPage(userProfile) {
  menus = userProfile.menu;
  user_entities = userProfile.entity_info;
  window.localStorage.theme_name = userProfile.theme;
  //legal_entity_list = userProfile.entity_info;
  //window.sessionStorage.available_legal_entities = userProfile.entity_info;
  if ('Home' in menus) {
    landingPage = '/dashboard';  // landingPage = "/home";
  } else {
    if(user_entities.length > 1){
      landingPage = '/welcome';
    }else{
      var selected_entity_name = '';
      $.each(user_entities, function(key, value) {
        selected_entity_name = value.le_name;
      });
      window.sessionStorage.selectedEntity = JSON.stringify(user_entities, null, ' ');
      window.sessionStorage.selectedEntityName = selected_entity_name;
      landingPage = '/home';
    }
  }

}
//
// isLoginValidated, resetLoginUI, performLogin
//
function isLoginValidated(e_email, e_password, e_captcha) {
  if (e_email.val() == '') {
    displayLoginMessage('Enter username / password');
    e_email.focus();
    return false;
  }
  if (e_password.val() == '') {
    displayLoginMessage('Enter username / password');
    e_password.focus();
    return false;
  }
  if (e_captcha.val() == '' && captchaStatus == true) {
    displayLoginMessage('Enter Captcha');
    e_captcha.focus();
    return false;
  }
  if (e_captcha.val() != '' && getCaptcha() != e_captcha.val()) {
    displayLoginMessage('Invalid Captcha');
    e_captcha.focus();
    return false;
  }
  return true;
}
function loadCaptcha() {
  captcha_text = getCaptcha();
  console.log('captcha_text : ' + captcha_text);
  if (captcha_text == null || captcha_text == 'null') {
    captchaStatus = false;
  } else {
    captchaStatus = true;
  }
  console.log('captcha status :' + captchaStatus);
  if (captchaStatus) {
    var myCanvas = document.getElementById('captchaCanvas');
    var myCanvasContext = myCanvas.getContext('2d');
    myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height);
    $('#captcha-view').show();
    var tCtx = document.getElementById('captchaCanvas').getContext('2d');
    tCtx.font = '18px Arial';
    tCtx.strokeText(captcha_text, 10, 20);
  } else {
    $('#captcha-view').hide();
  }
}
function resetLoginUI(e_button, e_email, e_password) {
  e_button.removeAttr('disabled', 'disabled');
  e_email.removeAttr('disabled', 'disabled');
  e_password.removeAttr('disabled', 'disabled');
  e_email.focus();
  loadCaptcha();
}
function parseJSON(data) {
  // data = JSON.stringify(data);
  return JSON.parse(data);
}
function processLogin(username, password, shortName, callback) {
  var request = [
    'Login',
    {
      'login_type': 'Web',
      'username': username,
      'password': password,
      'short_name': shortName,
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
  function makekey()
  {
      var text = "";
      var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

      for( var i=0; i < 5; i++ )
          text += possible.charAt(Math.floor(Math.random() * possible.length));
      return text;
  }
  // console.log(getCookie('_xsrf'));
  // url = BASE_URL + "login";
  actula_data = JSON.stringify(requestFrame, null, ' ');
  $.ajax({
    url: BASE_URL + 'login',
    headers: { 'X-Xsrftoken': getCookie('_xsrf') },
    type: 'POST',
    contentType: 'application/json',
    data: makekey() + btoa(actula_data),
    success: function (data, textStatus, jqXHR) {
      data = atob(data.substring(5));
      data = parseJSON(data);
      var status = data[0];
      var response = data[1];
      matchString = 'success';
      if (status.toLowerCase().indexOf(matchString) != -1) {
        initSession(response, shortName);
        callback(null, response);
      } else {
        callback(data, null);
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      rdata = parseJSON(jqXHR.responseText);
      rdata = atob(rdata.substring(5));
      callback(rdata, errorThrown);
    }
  });
}
function performLogin(e_button, e_email, e_password, e_shortname, e_captcha) {
  if (!isLoginValidated(e_email, e_password, e_captcha))
    return;
  displayLoginLoader();
  // e_button.attr("disabled", "disabled");
  // e_email.attr("disabled", "disabled");
  // e_password.attr("disabled", "disabled");
  function onFailure(data) {
    //console.log("status"+status);
    if (typeof data != 'string') {
      status = data[0];
      captcha_text = data[1].captcha_text;
      storeCaptcha(captcha_text);
    } else {
      status = data;
    }
    var disp_message = 'Unable to login. Incorrect username / password!';
    if (status == 'NotConfigured') {
      disp_message = 'Please Wait...Your account configuration is under progress..';
    } else if (status.indexOf('timeout') >= 0) {
      disp_message = 'Connection Timeout';
    } else {
      status = status.replace(/([A-Z])/g, ' $1').trim();
      disp_message = status;
    }
    displayLoginMessage(disp_message);
    $('input').val('');
    resetLoginUI(e_button, e_email, e_password);
  }

  processLogin(e_email.val(), e_password.val(), e_shortname.val(), function (error, response) {
    if (error == null) {
      // onSuccess(response)
      resetLoginUI(e_button, e_email, e_password);
      clearCaptcha();
      window.location.href = landingPage;
      $('#captcha-view').hide();
    } else {
      onFailure(error);
    }
  });

}
function initializeUI() {
  var windowHHeight = $(window).height();
  var loginBoxHeight = $('.login-box-inner').outerHeight();
  var getEmptySpace = windowHHeight - loginBoxHeight;
  var topPadding = getEmptySpace / 2;
  $('.login-box-inner').css('margin-top', topPadding);
  loadCaptcha();
}
function initializeLogin() {
  initializeUI();
  $('#txt-username').keydown(function (e) {
    if (e.keyCode == 13 && $(this).val() != '')
      $('#txt-password').focus();
  });
  $('#txt-password').keydown(function (e) {
    if (e.keyCode == 13 && $(this).val() != '')
      $('#txt-shortname').focus();
  });
  $('#txt-shortname').keydown(function (e) {
    if (e.keyCode == 13 && $(this).val() != '')
      performLogin($(this), $('#txt-username'), $('#txt-password'), $('#txt-shortname'), $('#txt-captcha'));
  });
  $('#txt-captcha').keydown(function (e) {
    if (e.keyCode == 13 && $(this).val() != '')
      //performLogin($(this), $("#txt-username"), $("#txt-password"));
      performLogin($(this), $('#txt-username'), $('#txt-password'), $('#txt-shortname'), $('#txt-captcha'));
  });
  $('#btn-login').on('click', function () {
    //performLogin($(this), $("#txt-username"), $("#txt-password"));
    performLogin($(this), $('#txt-username'), $('#txt-password'), $('#txt-shortname'), $('#txt-captcha'));
  });
}
function clearold_session() {
  delete window.sessionStorage["userInfo"];
}

$(document).ready(function () {
  //console.log("inside document ready");
  clearold_session();
  $('#txt-username').focus();


  // var url = '/forgot_password/' + short_name;
  // $('.text-forgot-password a').attr('href', url);

  initializeLogin();
});
$(window).resize(initializeUI);
