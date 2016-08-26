var landingPage = null;
var captchaStatus = false;
var captchaText = null;
function clearLoginMessage() {
    $(".login-error-message").hide();
    $(".login-error-message span").text("");
}

function displayLoginMessage(message) {
    $(".loading-indicator-spin").hide();
    $(".login-error-message span").text(message);
    $(".login-error-message").show();
}

function displayLoginLoader() {
    $(".loading-indicator-spin").show();
}

function storeCaptcha(captcha_text){
    window.sessionStorage["captcha"] = captcha_text;
}

function getCaptcha(){
    captcha = window.sessionStorage["captcha"]
    if(captcha != null && captcha != undefined && captcha != 'undefined'){
        return captcha;
    }else{
        return null;
    }
}

function clearCaptcha(){
    delete window.sessionStorage["captcha"];
}

function initSession(userProfile, shortName) {
    setLandingPage(userProfile);
    window.sessionStorage["userInfo"] = JSON.stringify(userProfile, null, " ");
    if (shortName !== null) {
        window.localStorage["shortName"] = shortName;
    }
}
function setLandingPage(userProfile) {
    menus = userProfile["menu"]["menus"];
    if ("Home" in menus) {
        landingPage = "/dashboard";
        // landingPage = "/home";
    }
    else {
        landingPage = "/home";
    }
}
function getShortName(){
    var pathArray = window.location.pathname.split( '/' );
    short_name = null;
    if(typeof pathArray[2] === 'undefined'){
        short_name = null;
    }
    else if (pathArray[2] === "login") {
        short_name = null
    }
    else{
        short_name = pathArray[2]
    }
    return short_name
}

//
// isLoginValidated, resetLoginUI, performLogin
//

function isLoginValidated (e_email, e_password, e_captcha) {
    if (e_email.val() == "") {
        displayLoginMessage(message.username_password_required);
        e_email.focus();
        return false;
    }
    if (e_password.val() == "") {
        displayLoginMessage(message.username_password_required);
        e_password.focus();
        return false;
    }
    if (e_captcha.val() == "" && captchaStatus == true) {
        displayLoginMessage(message.captcha_required);
        e_captcha.focus();
        return false;
    }
    if (e_captcha.val() != "" && getCaptcha() != e_captcha.val()) {
        displayLoginMessage(message.invalid_captcha);
        e_captcha.focus();
        return false;
    }
    return true;
}

function loadCaptcha(){
    captcha_text = getCaptcha();
    console.log("captcha_text : "+ captcha_text);
    if(captcha_text == null || captcha_text == "null"){
        captchaStatus = false;
    }else{
        captchaStatus = true;
    }
    console.log("captcha status :"+captchaStatus);
    if(captchaStatus){
        var myCanvas = document.getElementById("captchaCanvas");
        var myCanvasContext = myCanvas.getContext('2d');
        myCanvasContext.clearRect(0, 0, myCanvas.width, myCanvas.height)

        $("#captcha-view").show();
        var tCtx = document.getElementById('captchaCanvas').getContext('2d');
        tCtx.font = "18px Arial";
        tCtx.strokeText(captcha_text, 10, 20);
    }else{
        $("#captcha-view").hide();
    }
}

function resetLoginUI(e_button, e_email, e_password) {
    e_button.removeAttr("disabled", "disabled");
    e_email.removeAttr("disabled", "disabled");
    e_password.removeAttr("disabled", "disabled");
    e_email.focus();
    loadCaptcha();
}
function processLogin(username, password, shortName, callback) {

    var request = [
        "Login", {
            "login_type": "Web",
            "username": username,
            "password": password,
            "short_name": short_name,
            "ip" : ''
        }
    ];
    if (shortName == null) {
        var requestFrame = request;
        BASE_URL = "/knowledge/api/"
    }
    else {
        var requestFrame = [
            shortName,
            request
        ];
        BASE_URL = "/api/"
    }
    function getCookie(name) {
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
    }
    // console.log(getCookie('_xsrf'));
    // url = BASE_URL + "login";


    $.ajax({
        url : BASE_URL + "login",
        headers: {'X-Xsrftoken' : getCookie('_xsrf')},
        type: "POST",
        contentType: "application/json",
        data : JSON.stringify(requestFrame, null, " "),
        success:function(data, textStatus, jqXHR){
            var data = JSON.parse(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            if (status.toLowerCase().indexOf(matchString) != -1){
                initSession(response, shortName)
                callback(null, response);
            }
            else {
                callback(data, null);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            callback(jqXHR["responseText"], errorThrown)
        }
    });

}
function performLogin(e_button, e_email, e_password, e_captcha) {
    if (!isLoginValidated(e_email, e_password, e_captcha))
        return;

    displayLoginLoader();
    // e_button.attr("disabled", "disabled");
    // e_email.attr("disabled", "disabled");
    // e_password.attr("disabled", "disabled");

    function onFailure(data) {
        //console.log("status"+status);
        status = data[0]
        captcha_text = data[1].captcha_text
        storeCaptcha(captcha_text);
        var disp_message = message.invalid_username_password;
        if (status == "NotConfigured"){
            disp_message = message.accountconfiguration_underprogress;
        }
        else if (status.indexOf("timeout") >= 0) {
            disp_message = message.connection_timeout
        }else{
            status = status.replace(/([A-Z])/g, ' $1').trim();
            disp_message = status
        }
        displayLoginMessage(disp_message);
        $("input").val("");

        resetLoginUI(e_button, e_email, e_password);

    }

    if (getShortName() === null){
        processLogin(
            e_email.val(),
            e_password.val(),
            null,
            function (error, response) {
                if (error == null){
                    // onSuccess(response)
                    resetLoginUI(e_button, e_email, e_password);
                    clearCaptcha();
                    window.location.href = "/knowledge/home";
                    $("#captcha-view").hide();
                }
                else {
                    onFailure(error)
                }
            }
        );
    }else{
        processLogin(
            e_email.val(),
            e_password.val(),
            getShortName(),
            function (error, response) {
                if (error == null){
                    // onSuccess(response)
                    resetLoginUI(e_button, e_email, e_password);
                    clearCaptcha();
                    window.location.href = landingPage;
                    $("#captcha-view").hide();
                }
                else {
                    onFailure(error)
                }
            }
        );
    }
}

function initializeUI () {
    var windowHHeight = $(window).height();
    var loginBoxHeight = $(".login-box-inner").outerHeight();
    var getEmptySpace = windowHHeight - loginBoxHeight;
    var topPadding = getEmptySpace / 2;
    $(".login-box-inner").css("margin-top", topPadding);
    loadCaptcha();
}

function initializeLogin () {
    initializeUI();

    $("#txt-username").keydown(function (e) {
        if (e.keyCode == 13 && $(this).val() != "")
            $("#txt-password").focus();
    });

    $("#txt-password").keydown(function (e) {
        if (e.keyCode == 13 && $(this).val() != "")
            //performLogin($(this), $("#txt-username"), $("#txt-password"));
            performLogin($(this), $("#txt-username"), $("#txt-password"), $("#txt-captcha"));
    });

    $("#txt-captcha").keydown(function (e) {
        if (e.keyCode == 13 && $(this).val() != "")
            //performLogin($(this), $("#txt-username"), $("#txt-password"));
            performLogin($(this), $("#txt-username"), $("#txt-password"), $("#txt-captcha"));
    });

    $("#btn-login").on("click", function () {
        //performLogin($(this), $("#txt-username"), $("#txt-password"));
        performLogin($(this), $("#txt-username"), $("#txt-password"), $("#txt-captcha"));
    });
}

$(document).ready(function () {
    //console.log("inside document ready");
    $("#txt-username").focus();
    short_name = getShortName()
    if (short_name === null) {
        var url = "/knowledge/forgot-password";
        $('.text-forgot-password a').attr('href', url);
    }
    else {
        var url = "/forgot_password/"+short_name;
        $('.text-forgot-password a').attr('href', url);
    }


    initializeLogin();
});

$(window).resize(initializeUI);