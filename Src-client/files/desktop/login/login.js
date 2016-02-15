
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
        displayLoginMessage("Enter email");
        e_email.focus();
        return false;
    }

    if (e_password.val() == "") {
        displayLoginMessage("Enter password");
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

    function onFailure (status) {
        displayLoginMessage("Unable to login. Incorrect email / password?");
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
                console.log(error)
                if (error == null){
                    // onSuccess(response)
                    window.location.href = "/home";
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
    if (mirror.verifyLoggedIn()) {
        navigateToHome()
        return;
    }

    initializeLogin();
});

$(window).resize(initializeUI);