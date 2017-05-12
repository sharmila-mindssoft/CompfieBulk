Spin_icon = $('.loading-indicator-spin');
Msg_pan = $('.err-msg');
Uname = $("#uname");
Pword = $("#pword");
CPword = $("#cpword");
Captcha = $("#txt-captcha");
Show_Captcha = $("#captchaCanvas");
Refresh = $(".refresh-captcha");
Submit_btn = $(".btn-submit");
Pword_hint = $("#password-hint");
passwordStrength = 'Weak';
Status_check = $('#status-check');
Status_msg = $('.status-msg');
var csrf_token = $('meta[name=csrf-token]').attr('content')
register_page = null;
_rtoken = null;
_captcha = null;
IS_VALID = 0;

function makekey() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 5; i++)
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
            } else {
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

function setCaptcha(val) {
    if (val != "") {
        $(".captcha-tr").show();
        Refresh.show();
        Captcha.show();
        var myCanvas = document.getElementById('captchaCanvas');
        var myCanvasContext = myCanvas.getContext('2d');
        myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height);
        var tCtx = document.getElementById('captchaCanvas').getContext('2d');
        tCtx.font = '18px Times New Roman';
        tCtx.beginPath();
        tCtx.lineWidth = "1";
        tCtx.moveTo(0, 15);
        tCtx.lineTo(90, 15);
        tCtx.stroke(); // Draw it
        tCtx.strokeText(val, 10, 20);
        tCtx.beginPath();
        tCtx.strokeStyle = "purple"; // Purple path
        tCtx.moveTo(0, 0);
        tCtx.lineTo(350, 100);
        tCtx.stroke(); // Draw it
    }
}

displayLoader = function() {
    Spin_icon.show();
};

hideLoader = function() {
    Spin_icon.hide();
};

resetField = function() {
    setCaptcha('');
    Uname.val('');
    Pword.val('');
    CPword.val('');
    Captcha.val('');
    Captcha.hide();
    Status_msg.text('');
    Status_check.removeClass()

};

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
                var _is_register = data.is_register;
                if (_is_register == false) {
                    displayMessage("Invalid Regsitration Link");
                    Captcha.hide();
                    IS_VALID = 2;
                } else {
                    _captcha = data.captcha;
                    setCaptcha(data.captcha);
                    IS_VALID = 1;
                }
            } else {
                displayMessage("Session expired");
                Captcha.hide();
                IS_VALID = 0;
            }
        });
    }
};

saveData = function() {
    req_dict = {
        'uname': Uname.val(),
        'pword': Pword.val(),
        'captcha': Captcha.val(),
        'token': _rtoken
    }
    request_list = [
        'SaveRegistraion', req_dict
    ];
    displayLoader();
    call_api(request_list, function(status, data) {
        hideLoader();
        if (status == null) {
            resetField();
            displaySuccessMessage("Registered Successfully");
            setTimeout(function() {
                delete window.sessionStorage.captcha;
                location.href = "../login";
            }, 2000);
        } else {
            if (status == "UsernameAlreadyExists") {
                displayMessage("User Name Already Exists");
            } else {
                displayMessage(status);
            }
        }
    });
};

validateMandatory = function() {
    if (IS_VALID == 2) {
        displayMessage("Invalid Registration Link");
        return false
    }
    if (IS_VALID == 0) {
        displayMessage("Session expired");
        return false;
    }
    if (Uname.val().trim().length == 0) {
        displayMessage("User ID required");
        validateToken();
        return false;
    } else if (Uname.val().trim().length > 20) {
        displayMessage('User ID Should not exceed 20 characters');
        validateToken();
        return false;
    } else if (Pword.val().trim().length == 0) {
        displayMessage("Password required");
        validateToken();
        return false;
    } else if (Pword.val().trim().length > 20) {
        displayMessage('Password Should not exceed 20 characters');
        validateToken();
        return false;
    } else if (CPword.val().trim().length == 0) {
        displayMessage("Confirm password required");
        validateToken();
        return false;
    } else if (CPword.val().trim().length > 20) {
        displayMessage('Confirm password Should not exceed 20 characters');
        validateToken();
        return false;
    } else if (Pword.val().trim() != CPword.val().trim()) {
        displayMessage("Confirm password should match with password");
        validateToken();
        return false;
    } else if (passwordStrength == 'Weak') {
        displayMessage("Password should not be Weak");
        Pword.val("");
        CPword.val("");
        validateToken();
        return false;
    } else if (Captcha.val().trim().length == 0) {
        displayMessage("Captcha required");
        validateToken();
        return false;
    } else if (Captcha.val().trim() != _captcha) {
        displayMessage("Invalid captcha");
        validateToken();
        return false;
    }
    return true;
};

checkAvailability = function() {
    if (Uname.val().length == 0) {
        displayMessage("User ID required");
        return;
    } else if (Uname.val().length > 20) {
        displayMessage("Username should not exceed 20 character");
        return;
    } else if (IS_VALID == 0) {
        displayMessage("Session expired");
        return;
    }
    request = [
        "CheckUsername", {
            'uname': Uname.val()
        }
    ];
    // Status_check.show();
    Status_check.addClass("load-icon");
    call_api(request, function(status, data) {
        Status_check.removeClass();
        Status_msg.text('User ID Already Exists');
        if (status == null) {
            Status_msg.text('');
            Status_check.addClass("tick-icon");
        } else {
            Status_msg.text('User ID Already Exists');
        }
    });
};

function isAlphanumeric(inputElm) {
    //allowed => alphanumeric
    return inputElm.val().replace(/[^0-9A-Za-z_-]/gi, '');
}
$(function() {
    Pword_hint.css('display', 'none');
    hideLoader();
    resetField();
    validateToken();
    Submit_btn.click(function() {
        is_valid = validateMandatory();
        if (is_valid == true) {
            saveData();
        }
    });
    Refresh.click(function() {
        validateToken();
    });
    Pword.keyup('input', function(eve) {
        this.value = this.value.replace(/\s/g, '');
        passwordStrength = checkStrength(Pword.val());
        if (passwordStrength == 'Strong') {
            Pword_hint.css('display', 'none');
        } else {
            Pword_hint.css('display', 'inline-block');
        }
    });
    Pword.focus(function() {
        Pword_hint.css('display', 'inline-block');
    });
    Pword.focusout(function() {
        Pword_hint.css('display', 'none');
    });
    Uname.focusout(function() {
        checkAvailability();
    });
    Uname.focus(function() {
        Status_msg.text('');
        Status_check.removeClass();
    });
    Uname.on('input', function(e) {
        this.value = isAlphanumeric($(this));
    });
    CPword.keyup('input', function(e) {
        this.value = this.value.replace(/\s/g, '');
    });
});
