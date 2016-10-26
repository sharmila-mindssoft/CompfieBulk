Spin_icon = $('.loading-indicator-spin');

Uname = $("#uname");
Pword = $("#pword");
CPword = $("#cpword");
Captcha = $("#txt-captcha");
Show_Captcha = $("#captchaCanvas");
Submit_btn = $(".btn-submit");
Pword_hint = $("#password-hint");
passwordStrength = 'Weak';

register_page = null;
_rtoken = null;
_captcha = null;

function call_api(request, callback) {
    console.log(JSON.stringify(request, null, ''));
    $.ajax({
        url: '/knowledge/api/login',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(request, null, ''),
        success: function(data, textStatus, jqXHR) {
            console.log(data);
            var data = JSON.parse(data);

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
            callback(jqXHR.responseText, errorThrown);
        }
    });
}

function setCaptcha(val) {
    var myCanvas = document.getElementById('captchaCanvas');
    var myCanvasContext = myCanvas.getContext('2d');
    myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height);
    var tCtx = document.getElementById('captchaCanvas').getContext('2d');
    tCtx.font = '18px Arial';
    tCtx.strokeText(val, 10, 20);
}

displayMessage = function(message){
    alert(message);
};

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
            }
            else {
                displayMessage(status);
                Captcha.hide();
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
            displayMessage("Saved Successfully");
        }
        else {
            displayMessage(status);
        }
    });
};

validateMandatory = function() {
    if (Uname.val().trim().length == 0){
        displayMessage("Username required");
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

$(function () {
    Pword_hint.css('display', 'none');
    hideLoader();
    resetField();
    validateToken();

    Submit_btn.click(function() {
        is_valid = validateMandatory();
        alert(is_valid);
        if (is_valid == true) {
            saveData();
        }
        else {
            return;
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

    CPword.keyup('input', function(e) {
        this.value = this.value.replace(/\s/g, '');
    });

});
