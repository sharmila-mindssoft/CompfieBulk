
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

function performLogin(e_button, e_email, e_password) {
    if (!isLoginValidated(e_email, e_password))
        return;

    displayLoginLoader();
    e_button.attr("disabled", "disabled");
    e_email.attr("disabled", "disabled");
    e_password.attr("disabled", "disabled");

    function onFailure(status) {
        console.log("status"+status);
        message = "Unable to login. Incorrect username / password!";
        if(status == "ContractExpired"){
            message = "Contract Expired"
        }else if (status == "NotConfigured"){
            message = "Please Wait...Your account configuration is under progress.."
        }
        displayLoginMessage(message);
        $("input").val("");
        resetLoginUI(e_button, e_email, e_password);
    }

    // function onSuccess (response) {
    //     // mirror.initSession(response);
    //     window.location.href = "/home";
    // }
    if (getShortName() === null){
        mirror.login(
            e_email.val(),
            e_password.val(),
            null,
            function (error, response) {
                console.log(error)
                if (error == null){
                    // onSuccess(response)
                    window.location.href = "/knowledge/home";
                }
                else {
                    onFailure(error)
                }
            }
        );
    }else{
        client_mirror.login(
            e_email.val(),
            e_password.val(),
            getShortName(),
            function (error, response) {
                console.log(error);
                if (error == null){
                    // onSuccess(response)
                    window.location.href = "/home";
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

function navigateToHome(){
    client_name = client_mirror.getClientShortName()
    if ((client_name === null) || (client_name === undefined)) {
        window.location.href = "/knowledge/home";
    } else {
        window.location.href = "/home";
    }
}

$(document).ready(function () {
    console.log("inside document ready");
    $("#txt-username").focus();
    short_name = getShortName()
    console.log("short name"+short_name);
    if (short_name === null) {
        console.log("short name null");
        // if (mirror.verifyLoggedIn()) {
        //     navigateToHome()
        //     return;
        // }
        var url = "/knowledge/forgot-password";
        $('.text-forgot-password a').attr('href', url);
    }
    else {
        console.log("short name not null");
        var url = "/forgot_password/"+short_name;
        $('.text-forgot-password a').attr('href', url);
        // if (short_name == client_mirror.getClientShortName()) {
        //     navigateToHome();
        // }
        // else  {
        //     client_mirror.clearSession();
        // }
    }


    initializeLogin();
});

$(window).resize(initializeUI);