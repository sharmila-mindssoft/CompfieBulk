
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
        console.log(status)
        console.log("calling onFailure")
        displayLoginMessage("Unable to login. Incorrect email / password?");
        $("input").val("");
        resetLoginUI(e_button, e_email, e_password);
    }

    function onSuccess (response) {
        console.log(response);
        mirror.initSession(response);
        console.log(mirror.getUserMenu())
        window.location.href = "/home";
        // mirror.getRedirectUrl();
        // if (status == "LoginSuccess") {
        //     window.location.href = mirror.getRedirectUrl();
        // }
        // else if (status == "LoginFailed") {
        //     onFailure();
        // }
    }

    mirror.login(
        e_email.val(),
        e_password.val(),
        function (error, response) {
            console.log(error)
            console.log(response)
            if (error == null){
                onSuccess(response)
            }
            else {
                onFailure(error)
            }
        }
    );
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
    if (mirror.verifyLoggedIn()) {
        // window.location.href = "/home";
        return;
    }

    initializeLogin();
});

$(window).resize(initializeUI);