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
// var csrf_token = $('meta[name=csrf-token]').attr('content')
register_page = null;
_rtoken = null;
_captcha = null;
IS_VALID = false;
var short_name;

function makekey() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
}

function call_api(request, short_name, callback) {
    var requestFrame = [
        short_name,
        request
    ];

    $.ajax({
        url: '/api/login',
        type: 'POST',
        contentType: 'application/json',
        headers: { 'X-Xsrftoken': getCookie('_xsrf') },
        data: makekey() + btoa(JSON.stringify(requestFrame, null, '')),
        success: function(rsdata, textStatus, jqXHR) {
            rsdata = atob(rsdata.substring(5));
            rsdata = JSON.parse(rsdata);
            var status = rsdata[0];
            var response = rsdata[1];
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
        Captcha.show();
        Refresh.show();
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
    short_name = paths[paths.length - 2];
    validate_api(reset_token);
    displayLoader();

    function validate_api(token) {
        var request = [
            "CheckRegistrationToken", {
                'reset_token': token
            }
        ];
        call_api(request, short_name, function(status, data) {
            hideLoader();
            if (status == null) {
                _rtoken = reset_token;
                _captcha = data.captcha;
                setCaptcha(data.captcha);
                IS_VALID = true;
            } else {
                displayMessage("Session expired");
                Captcha.hide();
                IS_VALID = false;
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
        'SaveRegistration', req_dict
    ];
    displayLoader();
    call_api(request_list, short_name, function(status, data) {
        hideLoader();
        if (status == null) {
            $(".captcha-tr").hide();
            resetField();
            displaySuccessMessage("Saved Successfully");
            setTimeout(function() {
                delete window.sessionStorage.captcha;
                location.href = "../../login";
            }, 2000);
        } else {
            if (status == "UsernameAlreadyExists") {
                displayMessage("User Name Already Exists");
            } else if (status == "DuplicateClientUserCreation") {
                displayMessage("Client User already Exists");
            } else
                displayMessage(status);
        }
    });
};

validateMandatory = function() {
    if (IS_VALID == false) {
        displayMessage("Session expired");
        return false
    }
    if (Uname.val().trim().length == 0) {
        displayMessage("User ID required");
        validateToken();
        return false;
    } else if (Pword.val().trim().length == 0) {
        displayMessage("Password required");
        validateToken();
        return false;
    } else if (CPword.val().trim().length == 0) {
        displayMessage("Confirm password required");
        validateToken();
        return false;
    } else if (Pword.val().trim() != CPword.val().trim()) {
        displayMessage("Confirm password should match with password");
        validateToken();
        return false;
    } else if (passwordStrength == 'Weak') {
        displayMessage("Password should not weak");
        validateToken();
        return false;
    } else if (Captcha.val().trim().length == 0) {
        displayMessage("Captcha required");
        return false;
    } else if (Captcha.val().trim() != _captcha) {
        displayMessage("Invalid captcha");
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
    } else if (IS_VALID == false) {
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
    call_api(request, short_name, function(status, data) {
        Status_check.removeClass();
        Status_msg.text('User ID Already Exists');
        if (status == null) {
            Status_msg.text('')
            Status_check.addClass("tick-icon");
        } else {
            Status_msg.text('User ID Already Exists');
        }
    });
};

function isAlphanumeric(inputElm) {
    //allowed => alphanumeric
    //return inputElm.val().replace(/[^0-9A-Za-z_-]/gi, '');
    var start = inputElm.selectionStart, end = inputElm.selectionEnd;
    inputElm.value = $(inputElm).val().replace(/[^ 0-9A-Za-z]/gi, '');
    inputElm.setSelectionRange(start, end);
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
        //this.value = isAlphanumeric($(this));
        isAlphanumeric(this);
    });
    CPword.keyup('input', function(e) {
        this.value = this.value.replace(/\s/g, '');
    });
});

// From Common Functions.
/*
  checkStrength is function which will do the
  main password strength checking for us
*/
function checkStrength(password) {
    //initial strength
    var strength = 0;
    //if the password length is less than 6, return message.
    if (password.length < 6) {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-short');
        return 'Weak';
    }
    /*//if length is 8 characters or more, increase strength value
    if (password.length > 7) strength += 1

    //if password contains both lower and uppercase characters, increase strength value
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))  strength += 1*/
    //if it has numbers and characters, increase strength value
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))
        strength += 1;
    //if it has one special character, increase strength value
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/))
        strength += 1;
    /* //if it has two special characters, increase strength value
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1*/
    //now we have calculated strength value, we can return messages
    //if value is less than 2
    if (strength < 2) {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-short');
        return 'Weak';
    } else {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-strong');
        return 'Strong';
    }
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