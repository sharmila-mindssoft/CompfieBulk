function initializeUI () {
    var windowHeight = $(window).height();
    var boxHeight = $(".welcome-msg").outerHeight();
    var getEmptySpace = windowHeight - boxHeight;
    var contentAreaTop = parseInt($(".content-area").css("padding-top"));
    var navBarHeight = $(".header-section").outerHeight();
    var marginTop = (getEmptySpace / 2) - navBarHeight - contentAreaTop;
    $(".welcome-msg").css("margin-top", marginTop);
}


$(document).ready(function () {
    if (!client_mirror.verifyLoggedIn())
        return;

    var user = client_mirror.getUserProfile();
    $(".welcome-msg").text("Welcome " + user["employee_name"] + "!");
    initializeUI();
});

$(window).resize(initializeUI);