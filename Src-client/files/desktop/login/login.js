var landingPage = null;
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
function initSession(userProfile, shortName) {
    setLandingPage(userProfile);
    window.localStorage["userInfo"] = JSON.stringify(userProfile, null, " ");
    if (shortName !== null) {
        window.localStorage["shortName"] = shortName;
    }
}
function setLandingPage(userProfile) {
    menus = userProfile["menu"]["menus"];
    if ("Home" in menus) {
        landingPage = "/dashboard";
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

function isLoginValidated (e_email, e_password) {
    if (e_email.val() == "") {
        displayLoginMessage("Enter username / password");
        e_email.focus();
        return false;
    }

    if (e_password.val() == "") {
        displayLoginMessage("Enter username / password");
        e_password.focus();
        return false;
    }

    return true;
}

function resetLoginUI(e_button, e_email, e_password) {
    e_button.removeAttr("disabled", "disabled");
    e_email.removeAttr("disabled", "disabled");
    e_password.removeAttr("disabled", "disabled");
    e_email.focus();
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
    jQuery.post(
        BASE_URL + "login",
        JSON.stringify(requestFrame, null, " "),
        function (data) {
            var data = JSON.parse(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            if (status.toLowerCase().indexOf(matchString) != -1){
                initSession(response, shortName)
                callback(null, response);
            }
            else {
                callback(status, null);
            }
        }
    )
    .fail(
        function (jqXHR, textStatus, errorThrown) {
            callback(jqXHR["responseText"], errorThrown)
        }
    );
}
function performLogin(e_button, e_email, e_password) {
    if (!isLoginValidated(e_email, e_password))
        return;

    displayLoginLoader();
    // e_button.attr("disabled", "disabled");
    // e_email.attr("disabled", "disabled");
    // e_password.attr("disabled", "disabled");

    function onFailure(status) {
        console.log("status"+status);
        message = "Unable to login. Incorrect username / password!";
        if(status == "ContractExpired"){
            message = "Contract Expired"
        }else if (status == "NotConfigured"){
            message = "Please Wait...Your account configuration is under progress.."
        }else if (status == "ContractNotYetStarted"){
            message = "Contract not yet started"
        }
        else if (status.indexOf("timeout") >= 0) {
            message = "Connection Timeout"
        }
        displayLoginMessage(message);
        $("input").val("");
        resetLoginUI(e_button, e_email, e_password);
    }

    if (getShortName() === null){
        processLogin(
            e_email.val(),
            e_password.val(),
            null,
            function (error, response) {
                console.log(response)
                console.log(error)
                if (error == null){
                    // onSuccess(response)
                    resetLoginUI(e_button, e_email, e_password);
                    window.location.href = "/knowledge/home";
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
                console.log(response)
                console.log(error);
                if (error == null){
                    // onSuccess(response)
                    resetLoginUI(e_button, e_email, e_password);
                    window.location.href = landingPage;
                }
                else {
                    console.log("login failed")
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
}

function initializeLogin () {
    initializeUI();

    $("#txt-username").keydown(function (e) {
        if (e.keyCode == 13 && $(this).val() != "")
            $("#txt-password").focus();
    });

    $("#txt-password").keydown(function (e) {
        if (e.keyCode == 13 && $(this).val() != "")
            performLogin($(this), $("#txt-username"), $("#txt-password"));
    });

    $("#btn-login").on("click", function () {
        performLogin($(this), $("#txt-username"), $("#txt-password"));
    });
}

$(document).ready(function () {
    console.log("inside document ready");
    $("#txt-username").focus();
    short_name = getShortName()
    console.log("short name"+short_name);
    if (short_name === null) {
        console.log("short name null");
        var url = "/knowledge/forgot-password";
        $('.text-forgot-password a').attr('href', url);
    }
    else {
        console.log("short name not null");
        var url = "/forgot_password/"+short_name;
        $('.text-forgot-password a').attr('href', url);
    }


    initializeLogin();
});

$(window).resize(initializeUI);