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

function isLoginValidated (e_email, e_password) {
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
    function getCookie(name) {
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
    }
    // console.log(getCookie('_xsrf'));
    // url = BASE_URL + "login";


    // jQuery.postJSON = function(url, args, callback) {
    //     alert("called");
    //     args._xsrf = getCookie("_xsrf");
    //     $.ajax({url: url, data: $.param(args), type: "POST",
    //         success: function(response) {
    //             alert(response);
    //             if (callback) callback(eval("(" + response + ")"));
    //         },
    //         error: function(response) {
    //             console.log("ERROR:", response)
    //         }
    //     });
    // };
    // $.postJSON(url, requestFrame, function(data) {
    //     var data = parseJSON(data);
    //     alert(data);
    // });



    // x_request = {
    //     "_xsrf": getCookie('_xsrf'),
    //     "data": requestFrame
    // }
    $.ajax({
        url : BASE_URL + "login",
        headers: {'X-Xsrftoken' : getCookie('_xsrf') },
        type: "POST",
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
                callback(status, null);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            //if fails
        }
    });
    // jQuery.post(
    //     BASE_URL + "login",
    //     JSON.stringify(requestFrame, null, " "),
    //     function (data) {
    //         var data = JSON.parse(data);
    //         var status = data[0];
    //         var response = data[1];
    //         matchString = 'success';
    //         if (status.toLowerCase().indexOf(matchString) != -1){
    //             initSession(response, shortName)
    //             callback(null, response);
    //         }
    //         else {
    //             callback(status, null);
    //         }
    //     }
    // )
    // .fail(
    //     function (jqXHR, textStatus, errorThrown) {
    //         callback(jqXHR["responseText"], errorThrown)
    //     }
    // );
}
function performLogin(e_button, e_email, e_password) {
    if (!isLoginValidated(e_email, e_password))
        return;

    displayLoginLoader();
    // e_button.attr("disabled", "disabled");
    // e_email.attr("disabled", "disabled");
    // e_password.attr("disabled", "disabled");

    function onFailure(status) {
        //console.log("status"+status);
        var disp_message = message.invalid_username_password;
        if(status == "ContractExpired"){
            disp_message = message.contract_expired;
        }else if (status == "NotConfigured"){
            disp_message = message.accountconfiguration_underprogress;
        }else if (status == "ContractNotYetStarted"){
            disp_message = message.contract_notstart;
        }
        else if (status.indexOf("timeout") >= 0) {
            disp_message = message.connection_timeout
        }else{
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
                if (error == null){
                    // onSuccess(response)
                    resetLoginUI(e_button, e_email, e_password);
                    window.location.href = landingPage;
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