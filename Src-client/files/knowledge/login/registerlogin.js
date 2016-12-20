Spin_icon = $('.loading-indicator-spin');
Msg_pan = $('.err-msg');
Uname = $("#uname");
Pword = $("#pword");
CPword = $("#cpword");
Captcha = $("#txt-captcha");
Show_Captcha = $("#captchaCanvas");
Submit_btn = $(".btn-submit");
Pword_hint = $("#password-hint");
passwordStrength = 'Weak';
Status_check = $('#status-check');
Status_msg = $('.status-msg');
var csrf_token = $('meta[name=csrf-token]').attr('content')
register_page = null;
_rtoken = null;
_captcha = null;
IS_VALID = false;

function call_api(request, callback) {
    console.log(JSON.stringify(request, null, ''));
    $.ajax({
        url: '/knowledge/api/login',
        type: 'POST',
        contentType: 'application/json',
        headers: { 'X-CSRFToken': csrf_token },
        data: JSON.stringify(request, null, ''),
        success: function(data, textStatus, jqXHR) {

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
            console.log(jqXHR.responseText)
            console.log(errorThrown);
            console.log(textStatus);
            callback(jqXHR.responseText, null);
        }
    });
}

function setCaptcha(val) {
    Captcha.show();
    var myCanvas = document.getElementById('captchaCanvas');
    var myCanvasContext = myCanvas.getContext('2d');
    myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height);
    var tCtx = document.getElementById('captchaCanvas').getContext('2d');
    tCtx.font = '18px Arial';
    tCtx.strokeText(val, 10, 20);
}


displayLoader = function(){
    Spin_icon.show();
};

hideLoader = function() {
    Spin_icon.hide();
};

resetField = function() {
    Uname.val('');
    Pword.val('');
    CPword.val('');
    Captcha.val('');
    Status_msg.text('');
    setCaptcha('');
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
                _captcha = data.captcha;
                setCaptcha(data.captcha);
                IS_VALID = true;
            }
            else {
                displayMessage("Session expired");
                Captcha.hide();
                IS_VALID = false;
            }
        });
    }
};

saveData = function() {
    req_dict = {
        'uname' : Uname.val(),
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
            displaySuccessMessage("Saved Successfully");
        }
        else {
            displayMessage(status);
        }
    });
};

validateMandatory = function() {
    if (IS_VALID == false) {
        displayMessage("Session expired");
        return false
    }
    if (Uname.val().trim().length == 0){
        displayMessage("User ID required");
        return false;
    }

    else if (Pword.val().trim().length == 0){
        displayMessage("Password required");
        return false;
    }

    else if (CPword.val().trim().length ==0){
        displayMessage("Confirm password required");
        return false;
    }

    else if (Pword.val().trim() != CPword.val().trim()){
        displayMessage("Confirm password should match with password");
        return false;
    }

    else if (passwordStrength == 'Weak') {
        displayMessage("Password should not weak");
        return false;
    }

    else if (Captcha.val().trim().length == 0) {
        displayMessage("Captcha required");
        return false;
    }

    else if (Captcha.val().trim() != _captcha) {
        displayMessage("Invalid captcha");
        return false;
    }
    return true;
};

checkAvailability = function() {
    if (Uname.val().length == 0){
        displayMessage("Username required");
        return;
    }
    else if (IS_VALID == false) {
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
        Status_msg.text('User name already exists');
        if (status == null) {
            Status_msg.text('')
            Status_check.addClass("tick-icon");
        }
        else {
            Status_msg.text('User name already exists');
        }
    });
};

$(function () {
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

    Pword.keyup('input', function(eve) {
        this.value = this.value.replace(/\s/g, '');
        passwordStrength = checkStrength(Pword.val());
        if (passwordStrength == 'Strong') {
            Pword_hint.css('display', 'none');
        }
        else {
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

    CPword.keyup('input', function(e) {
        this.value = this.value.replace(/\s/g, '');
    });


});
