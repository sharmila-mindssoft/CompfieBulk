function sortForms(forms) {
    forms.sort(function(a, b) {
        return a.form_id - b.form_id;
    });
    return forms;
}

function toUpperCamelCase(s) {
    parts = s.split(' ');
    parts2 = [];
    for (var i = 0; i < parts.length; i++) {
        var part = parts[i].toLowerCase();
        part0 = part[0].toUpperCase();
        part1 = part.slice(1);
        parts2.push(part0.concat(part1));
    }
    return parts2.join(' ');
}

function initializeNavBar() {
    function getItemObject(form_url, form_name) {
        var itemObject = $('#nav-bar-templates .sub-menu-item li').clone();
        if (form_url !== null) {
            $('.menu-url', itemObject).attr('href', form_url);
        }
        if (form_name == "Logout") {
            $('.menu-url', itemObject).append('<i class ="ti-power-off m-r-5"></i>');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else if (form_name == "Change Password") {
            $('.menu-url', itemObject).append('<i class ="ti-settings m-r-5"></i>');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else if (form_name == "View Profile") {
            $('.menu-url', itemObject).append('<i class="ti-user m-r-5"></i>');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else if (form_name == "Client View Profile") {
            $('.menu-url', itemObject).append('<i class="ti-user m-r-5"></i>');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else if (form_name == "Settings") {
            $('.menu-url', itemObject).append('<i class="ti-settings m-r-5"></i>');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else if (form_name == "Themes") {
            $('.menu-url', itemObject).append('<i class="fa fa-clone m-r-5">');
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        } else {
            $('.menu-url', itemObject).append('<span>' + form_name + '</span>');
        }
        return itemObject;
    }

    var frm = window.location.href;
    var navBarItems = null;
    navBarItems = client_mirror.getUserMenu();
    if(navBarItems.Dashboard != undefined)
        $('.dashboard-to-menu').show();
    else
        $('.dashboard-to-menu').hide();
    if (navBarItems === null || navBarItems == undefined)
        return;
    var menus = null;
    menus = [
        'Master',
        'Transaction',
        'Report',
        'My Accounts'
    ];

    if (menus.length == 0) {
        client_mirror.clearSession();
        window.location.href = '/login';
    }
    for (var i = 0; i < menus.length; i++) {
        var key = menus[i];
        if (key == "My Accounts")
            continue;
        if (!(key in navBarItems))
            continue;
        var liObject = $('#nav-bar-templates .sub-menu-name li').clone();
        $('.menu-name', liObject).append(key.toUpperCase());
        $('.menu-name', liObject).append('<span class="caret"></span>')
        $('.menu-items-ul', liObject).addClass('menu');
        var forms = sortForms(navBarItems[key]);
        var forms2 = {};
        for (var form_key in forms) {
            var form = navBarItems[key][form_key];
            var parentMenu = form.parent_menu;
            
            if (parentMenu === null)
                forms2[form.form_id] = [form];
            else {
                if (!(parentMenu in forms2))
                    forms2[parentMenu] = [];

                forms2[parentMenu].push(form);
            }
        }
        for (var form in forms2) {
            if (forms2[form].length == 1) {
                var item = getItemObject(forms2[form][0].form_url, forms2[form][0].form_name);
                $('.menu-items-ul.menu', liObject).append(item);
            } else {
                var parentLi = $('#nav-bar-templates .sub-menu-name li').clone();
                parentLi.addClass('dropdown-submenu')
                $('.menu-name', parentLi).text(toUpperCamelCase(form));
                for (var j = 0; j < forms2[form].length; j++) {
                    var item = getItemObject(forms2[form][j].form_url, forms2[form][j].form_name);
                    $('.menu-items-ul', parentLi).append(item);
                }
                $('.menu-items-ul.menu', liObject).append(parentLi);
            }
        }
        $('.cssmenu .menu-ul').append(liObject);
    }

    var user = client_mirror.getUserInfo();
    var settingsMenu = navBarItems["My Accounts"];
    var settingsMenuObject = $('#nav-bar-templates .settings-menu .dropdown').clone();
    $('.username', settingsMenuObject).text(user.emp_name);
    for (var form_key in settingsMenu) {
        var form = navBarItems["My Accounts"][form_key];
        if (form.form_name != "Reminders" && form.form_name != "Statutory Notifications" && form.form_name != "Escalations" && form.form_name != "Messages") {
            var item = getItemObject(form.form_url, form.form_name);
            $('ul', settingsMenuObject).append(item);
        }
    }

    var item = getItemObject(null, 'Logout');
    item.on('click', function() {
        client_mirror.logout(function(args) {
            custom_alert(args);
        });
    });

    $('ul', settingsMenuObject).append(item);

    var notification_type = "";
    $('.cssmenu .menu-ul').append(settingsMenuObject);
    for (var form_key in settingsMenu) {
        var form = navBarItems["My Accounts"][form_key];
        if (form.form_name == "Reminders") {
            var liObject = $('#nav-bar-templates .reminders li').clone();
            $('.cssmenu .menu-ul').append(liObject);
            $('.reminder-menu').on('click', function(event) {
                $('.reminder-items-ul').empty();
                var LEIDS = client_mirror.getLEids();
                displayLoader();
                client_mirror.getNotifications(LEIDS, 2, 0, 2, function(error, response) {
                    if (error == null) {
                        data = response.reminders;
                        reminder_expire_count = response.reminder_expire_count;
                        $.each(data, function(k, v) {
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-heading', msgObject).text(limits(v.notification_text, 22));
                            $('.statu-content', msgObject).text(v.created_on);
                            $('.slink', msgObject).attr('href', '/reminders');
                            $('.reminder-items-ul').append(msgObject);
                            if (k == 1) return false;
                        });
                        if(data.length == 0) {
                            window.sessionStorage.reminder_count = 0;
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-content', msgObject).text("No Records Found");
                            $('.reminder-items-ul').append(msgObject);
                        } else {
                            window.sessionStorage.reminder_count = data.length;
                            $('.reminder-menu').find('.notify-icon-container').show();
                        }
                        if(data.length >= 2) {
                            var msgObject1 = $('#nav-bar-templates .reminders-read-all li').clone();
                            $('.reminder-items-ul').append(msgObject1);
                        } else {
                            $('.reminder-items-ul').find(".divider:last").remove();
                        }
                        if(data.length > 0) {
                            if(reminder_expire_count == 0) {
                                window.sessionStorage.reminder_expire_count = 0;
                                $('.reminder-menu').find('.zmdi-timer').removeClass("blink");
                            } else {
                                displayMessage(message.reminder_expire);
                                window.sessionStorage.reminder_expire_count = reminder_expire_count;
                                $('.reminder-menu').find('.zmdi-timer').addClass("blink");
                            }
                        }
                    }
                    hideLoader();
                });
            });
        } else if (form.form_name == "Statutory Notifications") {
            var liObject = $('#nav-bar-templates .notifications li').clone();
            $('.cssmenu .menu-ul').append(liObject);
            $('.notification-menu').on('click', function(event) {
                $('.notification-items-ul').empty();
                var LEIDS = client_mirror.getLEids();
                displayLoader();
                client_mirror.getStatutoryNotifications(LEIDS, 0, 3, function(error, response) {
                    if (error == null) {
                        data = response.statutory;
                        $.each(data, function(k, v) {
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-heading', msgObject).text(limits(v.notification_text, 22));
                            $('.statu-content', msgObject).text(v.created_on);
                            $('.slink', msgObject).attr('href', '/notifications');
                            $('.notification-items-ul').append(msgObject);
                            if (k == 1) return false;
                        });
                        if(data.length == 0) {
                            window.sessionStorage.statutory_count = 0;
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-content', msgObject).text("No Records Found");
                            $('.notification-items-ul').append(msgObject);
                        } else {
                            window.sessionStorage.statutory_count = data.length;
                            $('.notification-menu').find('.notify-icon-container').show();
                        }
                        if(data.length >= 2) {
                            var msgObject1 = $('#nav-bar-templates .notifications-read-all li').clone();
                            $('.notification-items-ul').append(msgObject1);
                        } else {
                            $('.notification-items-ul').find(".divider:last").remove();
                        }   
                    }
                    hideLoader();
                });
            });
        } else if (form.form_name == "Escalations") {
            var liObject = $('#nav-bar-templates .escalations li').clone();
            $('.cssmenu .menu-ul').append(liObject);
            $('.escalation-menu').on('click', function(event) {
                $('.escalation-items-ul').empty();
                var LEIDS = client_mirror.getLEids();
                displayLoader();
                client_mirror.getNotifications(LEIDS, 3, 0, 3, function(error, response) {
                    if (error == null) {
                        data = response.escalations;
                        $.each(data, function(k, v) {
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-heading', msgObject).text(limits(v.notification_text, 22));
                            $('.statu-content', msgObject).text(v.created_on);
                            $('.slink', msgObject).attr('href', '/escalations');
                            $('.escalation-items-ul').append(msgObject);
                            if (k == 1) return false;
                        });
                        if(data.length == 0) {
                            window.sessionStorage.escalation_count = 0
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-content', msgObject).text("No Records Found");
                            $('.escalation-items-ul').append(msgObject);
                        } else {
                            window.sessionStorage.escalation_count = data.length;
                            $('.escalation-menu').find('.notify-icon-container').show();
                        }
                        if(data.length >= 2) {
                            var msgObject1 = $('#nav-bar-templates .escalations-read-all li').clone();
                            // $('.mlink').attr('href', '/escalations');
                            $('.escalation-items-ul').append(msgObject1);
                        } else {
                            $('.escalation-items-ul').find(".divider:last").remove();
                        }
                    }
                    hideLoader();
                });
            });
        } else if (form.form_name == "Messages") {
            var liObject = $('#nav-bar-templates .messages li').clone();
            $('.cssmenu .menu-ul').append(liObject);
            $('.message-menu').on('click', function(event) {
                $('.msg-items-ul').empty();
                var LEIDS = client_mirror.getLEids();
                displayLoader();
                client_mirror.getNotifications(LEIDS, 4, 0, 2, function(error, response) {
                    if (error == null) {
                        data = response.messages;
                        $.each(data, function(k, v) {
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-heading', msgObject).text(limits(v.notification_text, 22));
                            $('.statu-content', msgObject).text(v.created_on);
                            $('.slink', msgObject).attr('href', '/message');
                            $('.msg-items-ul').append(msgObject);
                            if (k == 1) return false;
                        });
                        if(data.length == 0) {
                            window.sessionStorage.messages_count = 0;
                            var msgObject = $('#nav-bar-templates .notifications-list li').clone();
                            $('.statu-content', msgObject).text("No Records Found");
                            $('.msg-items-ul').append(msgObject);
                        } else {
                            window.sessionStorage.messages_count = data.length;
                            $('.message-menu').find('.notify-icon-container').show();
                        }
                        if(data.length >= 2) {
                            var msgObject1 = $('#nav-bar-templates .message-read-all li').clone();
                            $('.msg-items-ul').append(msgObject1);
                        } else {
                            $('.msg-items-ul').find(".divider:last").remove();
                        }
                    }
                    hideLoader();
                });
            });
        }
    }
    
    if(window.sessionStorage.statutory_count) {
        if(parseInt(window.sessionStorage.statutory_count) > 0) {
            $('.notification-menu').find('.notify-icon-container').show();
        } else {
            $('.notification-menu').find('.notify-icon-container').hide();
        }
    }

    if(window.sessionStorage.reminder_count) {
        if(parseInt(window.sessionStorage.reminder_count) > 0) {
            $('.reminder-menu').find('.notify-icon-container').show();
        } else {
            $('.reminder-menu').find('.notify-icon-container').hide();
        }
    }

    if(window.sessionStorage.reminder_expire_count) {
        if(parseInt(window.sessionStorage.reminder_expire_count) > 0) {
            $('.reminder-menu').find('.zmdi-timer').addClass("blink");
        } else {
            $('.reminder-menu').find('.zmdi-timer').removeClass("blink");
        }
    }

    if(window.sessionStorage.escalation_count) {
        if(parseInt(window.sessionStorage.escalation_count) > 0) {
            $('.escalation-menu').find('.notify-icon-container').show();
        } else {
            $('.escalation-menu').find('.notify-icon-container').hide();
        }
    }

    if(window.sessionStorage.messages_count) {
        if(parseInt(window.sessionStorage.messages_count) > 0) {
            $('.message-menu').find('.notify-icon-container').show();
        } else {
            $('.message-menu').find('.notify-icon-container').hide();
        }
    }
}

function persistNavBar() {
    frms = window.location.href.split('/');
    ac_menu = client_mirror.getPageUrl();
    form_name = '/' + frms[frms.length - 2] + '/' + frms[frms.length - 1];
    if (ac_menu.indexOf(form_name) == -1) {
        client_mirror.clearSession();
        window.location.href = '/login';
    }

}
$(document).ready(function() {
    initializeNavBar();
});
