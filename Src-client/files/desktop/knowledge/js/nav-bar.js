function sortForms (forms) {
    forms.sort(function(a, b) {
        return a.form_id - b.form_id;
    });
    return forms;
}

function toUpperCamelCase (s) {
    parts = s.split(" ");
    parts2 = []
    for (var i = 0; i < parts.length; i++) {
        var part = parts[i].toLowerCase();
        part0 = part[0].toUpperCase();
        part1 = part.slice(1);
        parts2.push(part0.concat(part1));
    }
    return parts2.join(" ");
}

function initializeNavBar () {
    function getItemObject (form_url, form_name) {
        var itemObject = $("#nav-bar-templates .sub-menu-item li").clone();
        if (form_url !== null)
            $(".menu-url", itemObject).attr("href", form_url);
        $(".menu-item", itemObject).text(form_name);
        return itemObject;
    }
    var frm = window.location.href
    var navBarItems = null
    navBarItems = mirror.getUserMenu();

    if (navBarItems === null || navBarItems == undefined)
        return;
    var menus = null
    if (window.localStorage["shortName"] != null){
        menus = ["Master", "Transaction", "Report"];
    }else{
        menus = ["Master", "Transaction", "Report"];
    }
    var homeMenu = $("#cssmenu .menu-ul .home-menu");
    if ("Home" in navBarItems) {
        homeMenu.attr("href", "/dashboard")
    }
    else {
        homeMenu.attr("href", "/home")
    }

    for (var i = 0; i < menus.length; i++) {
        var key = menus[i];
        if (!(key in navBarItems))
            continue
        var liObject = $("#nav-bar-templates .sub-menu-name li").clone();
        $(".menu-name", liObject).text(toUpperCamelCase(key));
        $(".menu-items-ul", liObject).addClass("menu");

        var forms = sortForms(navBarItems[key]);
        var forms2 = {};
        for (var form_key in forms) {
            var form = navBarItems[key][form_key];
            var parentMenu = form["parent_menu"];
            if (parentMenu === null)
                forms2[form["form_id"]] = [form];
            else {
                if (!(parentMenu in forms2))
                    forms2[parentMenu] = []
                forms2[parentMenu].push(form);
            }
        }

        for (var form in forms2) {
            if (forms2[form].length == 1) {
                var item = getItemObject(
                    forms2[form][0]["form_url"],
                    forms2[form][0]["form_name"]
                );
                $(".menu-items-ul.menu", liObject).append(item);
            }
            else {
                var parentLi = $("#nav-bar-templates .sub-menu-name li").clone();
                $(".menu-name", parentLi).text(toUpperCamelCase(form));
                for (var j = 0; j < forms2[form].length; j++) {
                    var item = getItemObject(
                        forms2[form][j]["form_url"],
                        forms2[form][j]["form_name"]
                    );
                    $(".menu-items-ul", parentLi).append(item);
                }
                $(".menu-items-ul.menu", liObject).append(parentLi);
            }
        }
        $("#cssmenu .menu-ul").append(liObject);
    }

    var user = mirror.getUserInfo();
    var settingsMenu = navBarItems["Settings"];
    var settingsMenuObject = $("#nav-bar-templates .settings-menu .user-icon").clone();
    $(".username", settingsMenuObject).text(user["employee_name"]);

    for (var form_key in settingsMenu) {
        var form = navBarItems["Settings"][form_key];
        var item = getItemObject(form["form_url"], form["form_name"]);
        $("ul", settingsMenuObject).append(item);
    }

    var employee_name = mirror.getEmployeeName();

    profile_url = "/knowledge/profile";
    change_password_url = "/knowledge/change-password";


    if (
        (typeof(employee_name) == "undefined") ||
        (employee_name != "Administrator")
    ){
        var item = getItemObject(profile_url, "View Profile");
        $("ul", settingsMenuObject).append(item);
    }
    var item = getItemObject(change_password_url, "Change Password");
    $("ul", settingsMenuObject).append(item);

    var item = getItemObject(null, "Logout");
    item.on("click", function () {
            mirror.logout(function(args) {
                custom_alert(args);
            });
    });

    $("ul", settingsMenuObject).append(item);
    $("#cssmenu .menu-ul").append(settingsMenuObject)

}

function showDeletionPopup(notification_text){
    $('.overlay-nav-bar').css("visibility","visible");
    $('.overlay-nav-bar').css("opacity","1");
    $("#msg").html(notification_text);
    $('.close').click(function(){
        $('.overlay-nav-bar').css("visibility","hidden");
        $('.overlay-nav-bar').css("opacity","0");
    });
}

function persistNavBar() {
    frms = window.location.href.split("/");
    ac_menu = mirror.getPageUrl();
    form_name = "/" + frms[frms.length - 2] + "/" + frms[frms.length - 1];
    if (ac_menu.indexOf(form_name) == -1)
        window.location.href = "/knowledge/login";

}
$(document).ready(function () {
    initializeNavBar();
    persistNavBar();
});
