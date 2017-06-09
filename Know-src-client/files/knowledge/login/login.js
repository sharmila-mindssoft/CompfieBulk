var csrf_token = $('meta[name=csrf-token]').attr('content')
var btnLogin = $('#btn-login');
var Refresh = $('.refresh-captcha');
var landingPage = null;
var captchaStatus = false;
var captchaText = null;
var randomString = function (len, bits)
{
    bits = bits || 36;
    var outStr = "", newStr;
    while (outStr.length < len)
    {
        newStr = Math.random().toString(bits).slice(2);
        outStr += newStr.slice(0, Math.min(newStr.length, (len - outStr.length)));
    }
    return outStr.toUpperCase();
};
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
    window.sessionStorage.statutory_count = userProfile.s_count;
    window.sessionStorage.messages_count = userProfile.m_count;
    window.sessionStorage.userInfo = JSON.stringify(userProfile, null, ' ');
    if (shortName !== null) {
        window.localStorage.shortName = shortName;
    }
}

function setLandingPage(userProfile) {
    menus = userProfile.menu.menus;
    if ('Home' in menus) {
        landingPage = '/dashboard'; // landingPage = "/home";
    } else {
        landingPage = '/home';
    }
}

function getShortName() {
    var pathArray = window.location.pathname.split('/');
    short_name = null;
    if (typeof pathArray[2] === 'undefined') {
        short_name = null;
    } else if (pathArray[2] === 'login') {
        short_name = null;
    } else {
        short_name = pathArray[2];
    }
    return short_name;
}
//
// isLoginValidated, resetLoginUI, performLogin
//
function isLoginValidated(e_email, e_password, e_captcha) {
    if (e_email.val() == '') {
        displayLoginMessage('Enter username / password');
        reloadCaptcha();
        e_email.focus();
        return false;
    }
    if (e_email.val().trim().length > 20) {
        displayLoginMessage('Username Should not exceed 20 characters');
        reloadCaptcha();
        e_email.focus();
        return false;
    }
    if (e_password.val() == '') {
        displayLoginMessage('Enter username / password');
        reloadCaptcha();
        e_password.focus();
        return false;
    }
    if (e_password.val().trim().length > 20) {
        displayLoginMessage('Password Should not exceed 20 characters');
        reloadCaptcha();
        e_email.focus();
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
    if (captcha_text == null || captcha_text == 'null') {
        captchaStatus = false;
    } else {
        captchaStatus = true;
    }
    if (captchaStatus) {
        var myCanvas = document.getElementById('captchaCanvas');
        var myCanvasContext = myCanvas.getContext('2d');
        myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height);
        $('#captcha-view').show();
        var tCtx = document.getElementById('captchaCanvas').getContext('2d');
        tCtx.font = '18px Arial';
        tCtx.beginPath();
        tCtx.lineWidth = "1";
        tCtx.moveTo(0, 15);
        tCtx.lineTo(90, 15);
        tCtx.stroke(); // Draw it
        tCtx.strokeText(captcha_text, 10, 20);
        tCtx.beginPath();
        tCtx.moveTo(0, 0);
        tCtx.lineTo(350, 100);
        tCtx.stroke(); // Draw it
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
        'Login', {
            'login_type': 'Web',
            'username': username,
            'password': password,
            'short_name': short_name,
            'ip': ''
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

    function getCookie(name) {
        var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
        return r ? r[1] : undefined;
    }

    function makekey() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 5; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        return text;
    }
    // console.log(getCookie('_xsrf'));
    // url = BASE_URL + "login";
    actula_data = JSON.stringify(requestFrame, null, ' ');
    console.log(actula_data);
    $.ajax({
        url: BASE_URL + 'login',
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(actula_data),
        success: function(data, textStatus, jqXHR) {
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
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata, errorThrown);
        }
    });
}

function reloadCaptcha() {
    if(captchaStatus) {
        storeCaptcha(randomString(6));
        loadCaptcha();
    }
}

function performLogin(e_button, e_email, e_password, e_captcha) {
    displayLoginMessage('');
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
        }
        else if (status == 'DisabledUser') {
            disp_message = "Login prohibited. Kindly contact your Administrator";
        }
        else {
            status = status.replace(/([A-Z])/g, ' $1').trim();
            disp_message = status;
        }
        displayLoginMessage(disp_message);
        $('input').val('');
        resetLoginUI(e_button, e_email, e_password);
    }
    if (getShortName() === null) {
        processLogin(e_email.val(), e_password.val(), null, function(error, response) {
            if (error == null) {
                // onSuccess(response)
                resetLoginUI(e_button, e_email, e_password);
                clearCaptcha();
                window.location.href = '/knowledge/home';
                $('#captcha-view').hide();
            } else {
                onFailure(error);
            }
        });
    } else {
        processLogin(e_email.val(), e_password.val(), getShortName(), function(error, response) {
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
    $('#username').keydown(function(e) {
        if (e.keyCode == 13 && $(this).val() != '')
            $('#password').focus();
    });
    $('#password').keydown(function(e) {
        if (e.keyCode == 13 && $(this).val() != '')
            performLogin($(this), $('#username'), $('#password'), $('#txt-captcha'));
    });
    $('#txt-captcha').keydown(function(e) {
        if (e.keyCode == 13 && $(this).val() != '')
            performLogin($(this), $('#username'), $('#password'), $('#txt-captcha'));
    });
    btnLogin.on('click', function() {
        performLogin($(this), $('#username'), $('#password'), $('#txt-captcha'));
    });
}

$(document).keydown(function(e) {
    if ((e.keyCode == 116 && e.ctrlKey) || e.keyCode == 116) {
        window.location.reload(true);
    }
});
    
$(document).ready(function() {
    //console.log("inside document ready");
    $('#username').focus();
    short_name = getShortName();
    if (short_name === null) {
        var url = '/knowledge/forgot-password';
        $('.text-forgot-password a').attr('href', url);
    } else {
        var url = '/forgot_password/' + short_name;
        $('.text-forgot-password a').attr('href', url);
    }
    Refresh.click(function() {reloadCaptcha();});
    initializeLogin();
    reloadCaptcha();
});
$(window).resize(initializeUI);
