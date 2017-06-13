var visiblePageCount = 10;
var m_names = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', "Dec");
//Load count values in pagination selectbox
var pageList = [25, 50, 100];

var UserTypeString = '[{"id":1,"name":"Assignee"},{"id":2,"name":"Concurrence"},{"id":3,"name":"Approval"}]';
var UserTypes = jQuery.parseJSON(UserTypeString);

var ComplianceTaskStatusString = '[{"name":"Assigned"},{"name":"Un-Assigned"},{"name":"Not Opted"}]';
var ComplianceTaskStatuses = jQuery.parseJSON(ComplianceTaskStatusString);

var TaskStatusString = '[{"name":"Complied"},{"name":"Delayed Compliance"},{"name":"In Progress"},{"name":"Not Complied"}]';
var TaskStatuses = jQuery.parseJSON(TaskStatusString);

function loadItemsPerPage() {
    for (var i = 0; i < pageList.length; i++) {
        var Id = pageList[i];
        $('#items_per_page').append($('<option value="' + Id + '">' + Id + '</option>'));
    };
}

function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test($email);
}

function ValidateIPaddress(ipaddress) {
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress)) {
        return true;
    }
    return false;
}

function clearMessage() {
    $('.error-message').hide();
    $('.error-message').text('');
}

function date_format(date) {
    day = date.getDate();
    if (day < 10) {
        day = '0' + day;
    }
    month = m_names[date.getMonth()];
    year = date.getFullYear();
    return day + '-' + month + '-' + year;
}

function datetime_format(date) {
    var day = date.getDate();
    var hour = date.getHours();
    var minutes = date.getMinutes();
    if (day < 10) {
        day = '0' + day;
    }
    month = m_names[date.getMonth()];
    year = date.getFullYear();
    return day + '-' + month + '-' + year + ' ' + hour + ":" + minutes;
}

function current_date(callback) {
    client_mirror.getCurrentDate(function(c_date) {
        c_date = date_format(new Date(c_date))
        callback(c_date)
    });
}

function current_date_ymd(callback) {
    client_mirror.getCurrentDate(function(c_date) {
        c_date = new Date(c_date);
        callback(c_date)
    });
}

function current_date_time(callback) {
    client_mirror.getCurrentDate(function(c_date) {
        c_date = datetime_format(new Date(c_date))
        callback(c_date)
    });
}

function past_days(days) {
    dat = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * days);
    return date_format(dat);
}

function hideMessage() {
    $('.toast').remove();
}

function displayMessage(message) {
    // $('.error-message').text(message);
    // $('.error-message').show();
    if ($('.toast-error').css('display') == "block") {
        $('.toast').remove();
    }
    var toastPan = import_toast();
    Command: toastPan["error"](message)

}

function displaySuccessMessage(message) {
    if ($('.toast-error').css('display') == "block") {
        $('.toast').remove();
    }
    var toastPan = import_toast();
    Command: toastPan["success"](message)

}

//Convert Number to String of Month
function getMonth_IntegertoString(intMonth) {
    var stringMonth = '';
    if (intMonth == 1)
        stringMonth = 'Jan';
    else if (intMonth == 2)
        stringMonth = 'Feb';
    else if (intMonth == 3)
        stringMonth = 'Mar';
    else if (intMonth == 4)
        stringMonth = 'Apr';
    else if (intMonth == 5)
        stringMonth = 'May';
    else if (intMonth == 6)
        stringMonth = 'Jun';
    else if (intMonth == 7)
        stringMonth = 'Jul';
    else if (intMonth == 8)
        stringMonth = 'Aug';
    else if (intMonth == 9)
        stringMonth = 'Sep';
    else if (intMonth == 10)
        stringMonth = 'Oct';
    else if (intMonth == 11)
        stringMonth = 'Nov';
    else if (intMonth == 12)
        stringMonth = 'Dec';
    return stringMonth;
}
//display custom alert box
function custom_alert(output_msg) {
    $('.alert-confirm').dialog({
        buttons: {
            Ok: function() {
                $(this).dialog('close');
            }
        },
        open: function() {
            $('.alert-message').html(output_msg);
        }
    });
}
//Validate that input value contains only one or more letters
function isCommon(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen
    return inputElm.val().replace(/[^ 0-9A-Za-z_.,-]/gi, '');
}

function isAlphabetic(inputElm) {
    //allowed => alphabetic
    return inputElm.val().replace(/[^ A-Za-z]/gi, '');
}

function isAlphanumeric(inputElm) {
    //allowed => alphanumeric
    return inputElm.val().replace(/[^ 0-9A-Za-z]/gi, '');
}

function isNumbers(inputElm) {
    //allowed => only numbers
    return inputElm.val().replace(/[^0-9]/gi, '');
}

function isNumbersWithDot(inputElm) {
    //allowed => only numbers
    return inputElm.val().replace(/[^0-9.]/gi, '');
}

function isNonZeroNumbers(inputElm) {
    //allowed => only numbers
    return inputElm.val().replace(/[^1-9]/gi, '');
}

function isCommon_Name(inputElm) {
    //allowed => alphanumeric, dot
    return inputElm.val().replace(/[^ A-Za-z.]/gi, '');
}

function isCommon_Address(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen, @, hash
    return inputElm.val().replace(/[^ A-Za-z_.,-@#\n]/gi, '');
}

function isNumbers_Countrycode(inputElm) {
    //allowed => only numbers,+
    return inputElm.val().replace(/[^0-9+]/gi, '');
}

function isAlphanumeric_Shortname(inputElm) {
    //allowed => alphanumeric
    return inputElm.val().replace(/[^0-9a-z]/gi, '');
}

function isCommon_Unitcode(inputElm) {
    //allowed => alphanumeric
    return inputElm.val().replace(/[^0-9A-Za-z]/gi, '');
}

function isCommon_Email(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen, @, hash
    return inputElm.val().replace(/[^A-Za-z_.,-@#]/gi, '');
    // return inputElm.val().replace(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/gi, '');
}

//move to top function
jQuery(document).ready(function() {
    var offset = 220;
    var duration = 500;
    jQuery(window).scroll(function() {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.back-to-top').fadeIn(duration);
        } else {
            jQuery('.back-to-top').fadeOut(duration);
        }
    });
    jQuery('.back-to-top').click(function(event) {
        event.preventDefault();
        jQuery('html, body').animate({ scrollTop: 0 }, duration);
        return false;
    });
});
/*
  checkStrength is function which will do the
  main password strength checking for us
*/
function checkStrength(password) {
    //initial strength
    var strength = 0;
    //if the password length is less than 6, return message.
    if (password.length < 6) {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-short');
        return 'Weak';
    }
    /*//if length is 8 characters or more, increase strength value
    if (password.length > 7) strength += 1

    //if password contains both lower and uppercase characters, increase strength value
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))  strength += 1*/
    //if it has numbers and characters, increase strength value
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))
        strength += 1;
    //if it has one special character, increase strength value
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/))
        strength += 1;
    /* //if it has two special characters, increase strength value
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1*/
    //now we have calculated strength value, we can return messages
    //if value is less than 2
    if (strength < 2) {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-short');
        return 'Weak';
    } else {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-strong');
        return 'Strong';
    }
}
//country autocomplete function
var chosen = '';

function activate_text_arrow(ac_id, ac_name, callback) {
    $('.ac-textbox').hide();
    var ac_result = [
        ac_id,
        ac_name
    ];
    callback(ac_result);
}

var month_id_name_map = {}
month_id_name_map[1] = "January"
month_id_name_map[2] = "February"
month_id_name_map[3] = "March"
month_id_name_map[4] = "April"
month_id_name_map[5] = "May"
month_id_name_map[6] = "June"
month_id_name_map[7] = "July"
month_id_name_map[8] = "August"
month_id_name_map[9] = "September"
month_id_name_map[10] = "October"
month_id_name_map[11] = "November"
month_id_name_map[12] = "December"


function commonAutoComplete(
    e, ac_div, id_element, text_val, list_val, field_name, id_name,
    callback, condition_fields, condition_values
) {
    ac_div.show();
    id_element.val('');
    var suggestions = [];
    ac_div.find('ul').empty();

    var checkKey = [16, 20, 27, 42, 17, 18, 91];

    if (text_val.length > 0 && $.inArray(e.keyCode, checkKey) == -1) {
        for (var i in list_val) {
            validation_result = true;
            if (condition_fields != undefined && condition_fields.length > 0) {
                validation_results = [];
                $.each(condition_fields, function(key, value) {
                    var condition_result;
                    if (jQuery.type(list_val[i][value]) == 'array') {
                        condition_result = ($.inArray(parseInt(condition_values[key]), list_val[i][value]) >= 0);
                    } else if (jQuery.type(condition_values[key]) == 'array') {
                        condition_result = ($.inArray(list_val[i][value], condition_values[key]) >= 0);
                    } else {
                        condition_result = (list_val[i][value] == condition_values[key]);
                    }
                    validation_results.push(
                        condition_result
                    )
                });
                validation_result = null;
                $.each(validation_results, function(key, value) {
                    if (key == 0) {
                        validation_result = value
                    } else {
                        validation_result = validation_result && value
                    }
                });
            }
            if (list_val[i][field_name] != null && (~list_val[i][field_name].toLowerCase().indexOf(
                    text_val.toLowerCase())) && validation_result) {
                var occur = -1;
                for (var j = 0; j < suggestions.length; j++) {
                    if (suggestions[j][1] == list_val[i][field_name]) {
                        occur = 1;
                        break;
                    }
                }
                if (occur < 0) {
                    suggestions.push([
                        list_val[i][id_name],
                        list_val[i][field_name]
                    ]);
                }
            }
        }
        var str = '';
        for (var i in suggestions) {
            str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
        }
        ac_div.find('ul').append(str);
        onCommonArrowKey(e, ac_div, callback);
    } else {
        $('.ac-textbox').hide();
    }
}

//autocomplete function callback
function activate_text(element, callback) {
    $('.ac-textbox').hide();
    var ac_id = $(element).attr('id');
    var ac_name = $(element).text();
    var ac_result = [
        ac_id,
        ac_name
    ];
    callback(ac_result);
}

function onCommonArrowKey(e, ac_item, callback) {
    if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
        chosen = '';
    }
    if (e.keyCode == 40) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen + 1 < ac_item.find('li').length) {
            chosen++;
        }
        ac_item.find(' li').removeClass('auto-selected');
        ac_item.find(' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen > 0) {
            chosen--;
        }
        ac_item.find(' li').removeClass('auto-selected');
        ac_item.find(' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 13) {
        var ac_id = ac_item.find(' li:eq(' + chosen + ')').attr('id');
        var ac_name = ac_item.find(' li:eq(' + chosen + ')').text();
        activate_text_arrow(ac_id, ac_name, callback);
        return false;
    }
}


function import_toast() {
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    return toastr;

}

function confirm_alert(message, callback) {
    swal({
        title: "Are you sure?",
        text: message,
        type: "success",
        showCancelButton: true,
        confirmButtonClass: 'btn-success waves-effect waves-light',
        confirmButtonText: 'Yes'
    }, function(isConfirm) {
        if (isConfirm) {
            callback(true);
        } else {
            callback(false);
        }
    });
}

function displayLoader() {
    $(".loading-indicator-spin").show();
}

function hideLoader() {
    $(".loading-indicator-spin").hide();
}

$(function() {
    $(":input").attr('autocomplete', 'off');

    //sort
    $(document).on('click', ".sort", function() {
        var ele = $(this);
        var table = ele.closest("table");
        var tbody = table.find('tbody');
        var col_num = ele.closest("th").index();
        if (ele.hasClass("asc")) {
            table.find("th span").each(function(i) {
                $(this).removeClass('desc');
                $(this).removeClass('asc');
            });
            ele.addClass("desc");
            ele.removeClass("asc");
        } else {
            table.find("th span").each(function(i) {
                $(this).removeClass('desc');
                $(this).removeClass('asc');
            });
            ele.addClass("asc");
            ele.removeClass("desc");
        }

        function extract_value(tr) {
            var td = $(tr).find('td')[col_num];
            var sort_value = $(td).html();
            var data_sort_value = $(td).attr('data-sort-value');
            if (typeof data_sort_value !== "undefined") {
                sort_value = data_sort_value;
            }
            return sort_value;
        }

        var allTrs = tbody.find('tr');
        tbody.find('tr').remove();

        allTrs.sort(function(tr_a, tr_b) {
            var aval = extract_value(tr_a);
            var bval = extract_value(tr_b);
            if (isNaN(aval) || isNaN(bval)) {
                return aval.localeCompare(bval);
            } else {
                aval = parseFloat(aval);
                bval = parseFloat(bval);
                return (aval > bval ? 1 : (bval > aval) ? -1 : 0);
            }
        });

        if (ele.hasClass("asc")) {
            for (var i = allTrs.length - 1; i >= 0; i--) {
                $(allTrs[i]).appendTo(tbody);
            };
        } else {
            for (var i = 0; i < allTrs.length; i++) {
                $(allTrs[i]).appendTo(tbody);
            };
        }
        table.find("th span.none-sort-sno").each(function(i) {
            var th_index = $(this).parent().index();
            var rows = table.children("tbody").children("tr");
            if (rows.length > 1) {
                rows.each(function(index, tr) {
                    $(tr).children().eq(th_index).html(index + 1);
                });
            }
        });
    });
});

function hyphenatedToUpperCamelCase(a) {
    var b = parseHyphenated(a);
    return hypToUpperCamelCase(b);
}

function parseHyphenated(a) {
    return a.split('-');
}

function hypToUpperCamelCase(d) {
    var a = [];
    for (var b = 0; b < d.length; ++b) {
        var c = d[b];
        c = c[0].toUpperCase() + c.slice(1);
        a.push(c);
    }
    return a.join('');
}

function limits(str, num) {
    if (str.length >= parseInt(num))
        return str.substr(0, parseInt(num)) + '...';
    else
        return str;
}

function convert_date(data) {
    var date = data.split('-');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for (var j = 0; j < months.length; j++) {
        if (date[1] == months[j]) {
            date[1] = months.indexOf(months[j]) + 1;
        }
    }
    if (date[1] < 10) {
        date[1] = '0' + date[1];
    }
    return new Date(date[2], date[1] - 1, date[0]);
}

//find date difference between two dates
function daydiff(first, second) {
    return (second - first) / (1000 * 60 * 60 * 24);
}


function confirm_ok_alert(message, callback_url) {
    hideLoader();
    swal({
        title: '',
        text: message,
        confirmButtonClass: 'btn-success waves-effect waves-light',
        confirmButtonText: 'Ok'
    }, function(isConfirm) {
        if (isConfirm) {
            if (callback_url == null) {
                window.location.href = '/login';
            } else {
                window.location.href = callback_url;
            }
        }
    });
}

$(document).keydown(function(e) {
    if ((e.keyCode == 116 && e.ctrlKey) || e.keyCode == 116) {
        $("input").val('');
        window.location.reload(true);
    }
});