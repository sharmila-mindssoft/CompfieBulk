var visiblePageCount = 10;
var m_names = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', "Dec");
//Load count values in pagination selectbox
var pageList = [25, 50, 100];
var ValidityDays = 90;
var unitsPerPage = 50;
var max_limit = 1024 * 1024 * 50; // 

function loadItemsPerPage() {
    for (var i = 0; i < pageList.length; i++) {
        var Id = pageList[i];
        $('#items_per_page').append($('<option value="' + Id + '">' + Id + '</option>'));
    };
}

function checkValidityDays() {
    return parseInt(ValidityDays);
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

function current_date() {
    return date_format(new Date());
}

function past_days(days) {
    dat = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * days);
    return date_format(dat);
}

function displayMessage(message) {
    if ($('.toast').css('display') == "block") {
        $('.toast').remove();
    }
    var toastPan = import_toast();
    Command: toastPan["error"](message)

}

function displaySuccessMessage(message) {
    if ($('.toast').css('display') == "block") {
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
                mirror.logout();
            } else {
                window.location.href = callback_url;
            }
        }
    });
}

//Validate that input value contains only one or more letters
function isCommon(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen
    return inputElm.val().replace(/[^ 0-9A-Za-z_\n.,-]/gi, '');
}

function isAllowSpecialChar(inputElm) {
    return inputElm.val().replace(/[^ 0-9A-Za-z_\n.,-@#&*()]/gi, '');
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
    return inputElm.val().replace(/[^0-9]/gi, '');
}

function isCommon_Name(inputElm) {
    //allowed => alphanumeric, dot
    return inputElm.val().replace(/[^ A-Za-z.-]/gi, '');
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
    return inputElm.val().replace(/[^0-9a-z]/gi, ''); ///[^0-9a-z]/gi
}

function isCommon_Unitcode(inputElm) {
    //allowed => alphanumeric
    return inputElm.val().replace(/[^0-9A-Za-z]/gi, '');
}

function isNumbers_Dot(inputElm) {
    //allowed => only numbers and dot
    return inputElm.val().replace(/[^0-9.]/gi, '');
}

function isNumbers_Dot_Comma(inputElm) {
    //allowed => only numbers and dot
    return inputElm.val().replace(/[^0-9., ]/gi, '');
}

function isWebUrl(inputElm) {
    // var urlregex = new RegExp("^(http:\/\/www.|https:\/\/){1}([0-9A-Za-z]+\.)");
    // return urlregex.test(inputElm.val());
    // var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    var re = /^(((ht|f){1}(tp:[/][/]){1})|((www.){1}))[-a-zA-Z0-9@:%_\+.~#?&//=]+$/;
    return re.test(inputElm.val());
}

function isCommon_input(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen, @, hash
    return inputElm.val().replace(/[^ 0-9A-Za-z_.,-]/gi, '');
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
    }
    /*else if (strength == 2 )
    {
      $('#pw-result').removeClass()
      $('#pw-result').addClass('pw-good')
      return 'Good'  + strength;
    }*/
    else {
        $('#pw-result').removeClass();
        $('#pw-result').addClass('pw-strong');
        return 'Strong';
    }
}

function onArrowKey(e, ac_item, callback, type) {

    var selector = "#"
    if (type == "class") {
        selector = "."
    }
    if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
        chosen = '';
    }
    if (e.keyCode == 40) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen + 1 < $(selector + ac_item + ' li').length) {
            chosen++;
        }
        $(selector + ac_item + ' li').removeClass('auto-selected');
        $(selector + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen > 0) {
            chosen--;
        }
        $(selector + ac_item + ' li').removeClass('auto-selected');
        $(selector + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 13) {
        var ac_id = $(selector + ac_item + ' li:eq(' + chosen + ')').attr('id');
        var ac_name = $(selector + ac_item + ' li:eq(' + chosen + ')').text();
        activate_text_arrow(ac_id, ac_name, callback);
        return false;
    }
}

var chosen = '';
//user autocomplete function
function getUserAutocomplete(e, textval, listval, callback) {
    $('#ac-user').show();
    $('#userid').val('');
    $('#assignee').val('');
    var users = listval;
    var suggestions = [];
    $('#ac-user ul').empty();
    if (textval.length > 0) {
        for (var i in users) {
            var combineUserName = '';
            if (users[i].employee_code != undefined) {
                combineUserName = users[i].employee_code + '-' + users[i].employee_name;
            } else {
                combineUserName = users[i].employee_name;
            }
            var user_id;
            if (users[i].user_id != undefined) {
                user_id = users[i].user_id;
            } else {
                user_id = users[i].employee_id;
            }
            if (~users[i].employee_name.toLowerCase().indexOf(textval.toLowerCase()))
                suggestions.push([
                    user_id,
                    combineUserName
                ]);
        }
        var str = '';
        for (var i in suggestions) {
            str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
        }
        $('#ac-user ul').append(str); //$("#userid").val('');
        //$("#assignee").val('');
    } else {
        $('.ac-textbox').hide();
    }
    onArrowKey(e, 'ac-user', callback);
}
//client businessgroup autocomplete function
function getClientBusinessGroupAutocomplete(e, textval, listval, callback) {
    $('#ac-businessgroup').show();
    $('#businessgroup').val('');
    $('#businessgroupid').val('');
    var bgroups = listval;
    var suggestions = [];
    $('#ac-businessgroup ul').empty();
    if (textval.length > 0) {
        for (var i in bgroups) {
            if (~bgroups[i].business_group_name.toLowerCase().indexOf(textval.toLowerCase()))
                suggestions.push([
                    bgroups[i].business_group_id,
                    bgroups[i].business_group_name
                ]);
        }
        var str = '';
        for (var i in suggestions) {
            str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
        }
        $('#ac-businessgroup ul').append(str); //$("#businessgroup").val('');
        //$("#businessgroupid").val('');
    } else {
        $('.ac-textbox').hide();
    }
    onArrowKey(e, 'ac-businessgroup', callback);
}
//client legalentity autocomplete function
function getClientLegalEntityAutocomplete(e, textval, listval, callback) {
    $('#ac-legalentity').show();
    $('#legalentity').val('');
    $('#legalentityid').val('');
    var lentity = listval;
    var suggestions = [];
    $('#ac-legalentity ul').empty();
    if (textval.length > 0) {
        for (var i in lentity) {
            if (~lentity[i].legal_entity_name.toLowerCase().indexOf(textval.toLowerCase()))
                suggestions.push([
                    lentity[i].legal_entity_id,
                    lentity[i].legal_entity_name
                ]);
        }
        var str = '';
        for (var i in suggestions) {
            str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
        }
        $('#ac-legalentity ul').append(str); //$("#legalentity").val('');
        //$("#legalentityid").val('');
    } else {
        $('.ac-textbox').hide();
    }
    onArrowKey(e, 'ac-legalentity', callback);
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
    e, ac_div, id_element, text_val, list_val, field_name, id_name, callback,
    condition_fields, condition_values
) {
    ac_div.show();
    id_element.val('');
    var suggestions = [];
    ac_div.find('ul').empty();
    if (text_val.length > 0) {
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

            if (~list_val[i][field_name].toLowerCase().indexOf(
                    text_val.toLowerCase()
                ) && validation_result

            )
                suggestions.push([
                    list_val[i][id_name],
                    list_val[i][field_name]
                ]);
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

function containsAll(arr1, arr2) {
    for (var i = 0, len = arr1.length; i < len; i++) {
        if ($.inArray(arr1[i], arr2) == -1) return false;
    }
    return true;
}


function containsOne(arr1, arr2) {
    var common_values = $.grep(arr1, function(element) {
        return $.inArray(element, arr2) !== -1;
    });
    if (common_values.length > 0) {
        return true;
    } else {
        return false;
    }
}

function commonAutoComplete1(
    e, ac_div, id_element, text_val, list_val, field_name, id_name, callback,
    condition_fields, condition_values
) {
    ac_div.show();
    id_element.val('');
    var suggestions = [];
    ac_div.find('ul').empty();
    if (text_val.length > 0) {
        for (var i in list_val) {
            validation_result = true;
            if (condition_fields != undefined && condition_fields.length > 0) {
                validation_results = [];
                $.each(condition_fields, function(key, value) {
                    var condition_result;
                    /*alert(jQuery.type(list_val[i][value]))
                    alert(JSON.stringify(list_val[i][value]))*/
                    if (jQuery.type(list_val[i][value]) == 'array') {
                        if (value == 'country_domains_parent') {
                            ccount = 0;
                            $.each(condition_values[key], function(key1, value1) {
                                for (var k = 0; k < list_val[i][value].length; k++) {
                                    if (value1.p_user_ids != undefined) {
                                        if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id &&
                                            containsAll(value1.p_user_ids, list_val[i][value][k]["p_user_ids"])) {
                                            //alert(JSON.stringify(value1.p_user_ids) + ' in ' + JSON.stringify(list_val[i][value][k]["p_user_ids"]))
                                            //alert(containsAll(value1.p_user_ids, list_val[i][value][k]["p_user_ids"]))
                                            ccount++;
                                        }
                                    } else {
                                        if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id) {
                                            ccount++;
                                        }
                                    }
                                }
                                //var te = value.user_id +'-'+ value1.c_id +'-'+ value1.d_id ;
                                //alert(JSON.stringify(value1))
                                //TE_PARANTS[te] = value1;
                            });
                            //alert(condition_values[key].length + '==' + ccount + '>>' + list_val[i][field_name])
                            if (condition_values[key].length == ccount) {
                                condition_result = true;
                            } else {
                                condition_result = false;
                            }
                            /*for (var j = 0; j < condition_values[key][0].length; j++) {
                                var cresult = false;
                                for (var k = 0; k < list_val[i][value].length; k++) {
                                    if (list_val[i][value][k]["c_id"] == condition_values[key][0][j]) {
                                        cresult = true;
                                    }
                                }
                            }
                            for (var j = 0; j < condition_values[key][1].length; j++) {
                                var dresult = false;
                                for (var k = 0; k < list_val[i][value].length; k++) {
                                    if (list_val[i][value][k]["d_id"] == condition_values[key][1][j]) {
                                        dresult = true;
                                    }
                                }

                            }
                            if (cresult && dresult) {
                                condition_result = true;
                            } else {
                                condition_result = false;
                            }*/


                            /*var cresult = false;
                            var dresult = false;
                            for(var j=0; j<list_val[i][value].length; j++){
                              if($.inArray(list_val[i][value][j]["c_id"], condition_values[key][0]) >= 0){
                                cresult = true;
                              }
                              if($.inArray(list_val[i][value][j]["d_id"], condition_values[key][1]) >= 0){
                                dresult = true;
                              }
                            }
                            if(cresult && dresult){
                              condition_result = true;
                            }else{
                              condition_result = false;
                            }*/
                            /* }else if (value == 'country_domains') {
                                 ccount = 0;
                                 $.each(condition_values[key], function(key1, value1) {
                                     for (var k = 0; k < list_val[i][value].length; k++) {
                                         if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id) {
                                             ccount++;
                                         }
                                     }
                                 });
                                 alert(condition_values[key].length)
                                 alert(ccount)
                                 if(condition_values[key].length == ccount){
                                     condition_result = true;
                                 }else{
                                     condition_result = false;
                                 }*/
                        } else if (value == 'mapped_country_domains') {
                            ccount = 0;
                            $.each(condition_values[key], function(key1, value1) {
                                for (var k = 0; k < list_val[i][value].length; k++) {
                                    if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id) {
                                        ccount++;
                                    }
                                }
                            });
                            if (condition_values[key].length == ccount) {
                                condition_result = true;
                            } else {
                                condition_result = false;
                            }
                        } else if (value == 'p_user_ids' && jQuery.type(condition_values[key]) == 'array') {
                            var array1 = condition_values[key];
                            var array2 = list_val[i][value];

                            //alert(JSON.stringify(array1))
                            //alert(JSON.stringify(array2))
                            var common_values = $.grep(array1, function(element) {
                                return $.inArray(element, array2) !== -1;
                            });

                            /*jQuery.grep(array1, function(el) {
                                if (jQuery.inArray(el, array2) == 0) common_values.push(el);
                            });*/
                            //alert('Common: ' + JSON.stringify(common_values))
                            if (common_values.length > 0) {
                                condition_result = true;
                            } else {
                                condition_result = false;
                            }
                        } else {
                            condition_result = ($.inArray(parseInt(condition_values[key]), list_val[i][value]) >= 0);
                        }

                    } else {
                        if (value == 'user_id') {
                            condition_result = (list_val[i][value] != condition_values[key]);
                        } else {
                            condition_result = (list_val[i][value] == condition_values[key]);
                        }
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
            if (~list_val[i][field_name].toLowerCase().indexOf(
                    text_val.toLowerCase()
                ) && validation_result)
                suggestions.push([
                    list_val[i][id_name],
                    list_val[i][field_name]
                ]);
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


function commonAutoComplete2(
    e, ac_div, id_element, text_val, list_val, field_name, id_name, callback,
    condition_fields, condition_values
) {
    ac_div.show();
    id_element.val('');
    var suggestions = [];
    ac_div.find('ul').empty();
    if (text_val.length > 0) {
        for (var i in list_val) {
            validation_result = true;
            if (condition_fields != undefined && condition_fields.length > 0) {
                validation_results = [];
                $.each(condition_fields, function(key, value) {
                    var condition_result;
                    if (jQuery.type(list_val[i][value]) == 'array') {
                        if (value == 'country_domains_parent') {
                            ccount = 0;
                            $.each(condition_values[key], function(key1, value1) {
                                for (var k = 0; k < list_val[i][value].length; k++) {
                                    if (value1.p_user_ids != undefined) {
                                        if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id &&
                                            containsOne(value1.p_user_ids, list_val[i][value][k]["p_user_ids"])) {
                                            //alert(JSON.stringify(value1.p_user_ids) + ' in ' + JSON.stringify(list_val[i][value][k]["p_user_ids"]))
                                            //alert(containsAll(value1.p_user_ids, list_val[i][value][k]["p_user_ids"]))
                                            ccount++;
                                        }
                                    } else {
                                        if (list_val[i][value][k]["c_id"] == value1.c_id && list_val[i][value][k]["d_id"] == value1.d_id) {
                                            ccount++;
                                        }
                                    }
                                }
                            });
                            if (condition_values[key].length == ccount) {
                                condition_result = true;
                            } else {
                                condition_result = false;
                            }
                        } else {
                            condition_result = ($.inArray(parseInt(condition_values[key]), list_val[i][value]) >= 0);
                        }

                    } else {
                        if (value == 'user_id') {
                            condition_result = (list_val[i][value] != condition_values[key]);
                        } else {
                            condition_result = (list_val[i][value] == condition_values[key]);
                        }
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
            if (~list_val[i][field_name].toLowerCase().indexOf(
                    text_val.toLowerCase()
                ) && validation_result)
                suggestions.push([
                    list_val[i][id_name],
                    list_val[i][field_name]
                ]);
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
        "timeOut": "20000",
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

function convert_date(data) {
    var date = data.split('-');
    var months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
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
            if(rows.length > 1) {
                rows.each(function(index, tr) {
                    $(tr).children().eq(th_index).html(index + 1);
                });
            }
        });
    });
});

$(document).bind('keydown keyup', function(e) {
    if ((e.keyCode == 116 && e.ctrlKey) || e.keyCode == 116) {
        $("input").val('');
        window.location.reload(true);
    }
});