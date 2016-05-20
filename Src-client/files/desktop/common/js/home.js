function initializeUI () {
    var windowHeight = $(window).height();
    var boxHeight = $(".welcome-msg").outerHeight();
    var getEmptySpace = windowHeight - boxHeight;
    var contentAreaTop = parseInt($(".content-area").css("padding-top"));
    var navBarHeight = $(".header-section").outerHeight();
    var marginTop = (getEmptySpace / 2) - navBarHeight - contentAreaTop;
    $(".welcome-msg").css("margin-top", marginTop);
    get_notification_count();
    $("#notification_count").text(window.localStorage["CLIENT_NOTIFICATION_COUNT"]);
    $("#reminder_count").text(window.localStorage["CLIENT_REMINDER_COUNT"]);
    $("#escalation_count").text(window.localStorage["CLIENT_ESCALATION_COUNT"] );

}


$(document).ready(function () {
    if (!mirror.verifyLoggedIn())
        return;

    var user = mirror.getUserProfile();
    $(".welcome-msg").text("Welcome " + user["employee_name"] + "!");

    initializeUI();
});

$(window).resize(initializeUI);