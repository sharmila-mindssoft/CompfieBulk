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
    var navBarItems = null
    if (window.localStorage["shortName"] != null){
        navBarItems = client_mirror.getUserMenu();
    }else{
        navBarItems = mirror.getUserMenu();
    }
    if (navBarItems === null)
        return;
    var menus = null
    if (window.localStorage["shortName"] != null){
        menus = ["Home", "Master", "Transaction", "Report"];
    }else{
        menus = ["Home", "Master", "Transaction", "Report"];
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

    var client_name = client_mirror.getClientShortName();
    var employee_name = mirror.getEmployeeName();
    
    if ((typeof(client_name) == "undefined") || (client_name == null) ){
        profile_url = "/knowledge/profile";
        change_password_url = "/knowledge/change-password";
    }
    else {
        profile_url = "/profile";
        change_password_url = "/change-password";
        if (
            (employee_name == "Administrator")
        ){
            settings_url = "/settings"
            var item = getItemObject(settings_url, "Settings");
            $("ul", settingsMenuObject).append(item);
        }
    }

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
        client_name = client_mirror.getClientShortName()
        if ((client_name === null) || (client_name === undefined)) {
            mirror.logout();
        }
        else {
            client_mirror.logout();
        }

    });

    $("ul", settingsMenuObject).append(item);
    $("#cssmenu .menu-ul").append(settingsMenuObject)

    if ((typeof(client_name) != "undefined") && (client_name != null) ){
        var liObject = $("#nav-bar-templates .reminder li").clone();
        $("#cssmenu .menu-ul").append(liObject);

        var liObject = $("#nav-bar-templates .notification li").clone();
        $("#cssmenu .menu-ul").append(liObject);

        var liObject = $("#nav-bar-templates .escalations li").clone();
        $("#cssmenu .menu-ul").append(liObject);
        get_notification_count()
        setInterval(function() {
            get_notification_count();
        }, 10000);
        
    }
}

function get_notification_count(){
    client_mirror.checkContractExpiration(function (status, data) {
            if (data == null) {
                return
                $(".contract_timer_container").hide()
            }else{
                no_of_days_left = data.no_of_days_left
                $(".contract_timer_container").show()
                if (no_of_days_left <= 30){
                    $(".contract_timer").html(
                        "Contract Expires in "+no_of_days_left+" days"
                    )
                }
                else{
                    // alert("Contract not expired yet"+no_of_days_left)
                }
                notification_count = data.notification_count;
                reminder_count = data.reminder_count;
                escalation_count = data.escalation_count;
                $("#notification_count").text(notification_count);
                $("#reminder_count").text(reminder_count);
                $("#escalation_count").text(escalation_count);
            }
        }
    )
}
    
$(document).ready(function () {
    initializeNavBar();
});