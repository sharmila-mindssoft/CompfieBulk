//Convert Number to Srting of Month
function getMonth_IntegettoString(intMonth) {
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
      Ok: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
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
function isCommon_Name(inputElm) {
  //allowed => alphanumeric, dot
  return inputElm.val().replace(/[^ A-Za-z.]/gi, '');
}
function isCommon_Address(inputElm) {
  //allowed => alphanumeric, dot, comma, Hyphen, @, hash
  return inputElm.val().replace(/[^ A-Za-z_.,-@#]/gi, '');
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
//move to top function
jQuery(document).ready(function () {
  var offset = 220;
  var duration = 500;
  jQuery(window).scroll(function () {
    if (jQuery(this).scrollTop() > offset) {
      jQuery('.back-to-top').fadeIn(duration);
    } else {
      jQuery('.back-to-top').fadeOut(duration);
    }
  });
  jQuery('.back-to-top').click(function (event) {
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
  }  /*else if (strength == 2 )
  {
    $('#pw-result').removeClass()
    $('#pw-result').addClass('pw-good')
    return 'Good'  + strength;
  }*/ else {
    $('#pw-result').removeClass();
    $('#pw-result').addClass('pw-strong');
    return 'Strong';
  }
}
function onArrowKey(e, ac_item, callback) {
  if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
    chosen = '';
  }
  if (e.keyCode == 40) {
    if (chosen === '') {
      chosen = 0;
    } else if (chosen + 1 < $('#' + ac_item + ' li').length) {
      chosen++;
    }
    $('#' + ac_item + ' li').removeClass('auto-selected');
    $('#' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 38) {
    if (chosen === '') {
      chosen = 0;
    } else if (chosen > 0) {
      chosen--;
    }
    $('#' + ac_item + ' li').removeClass('auto-selected');
    $('#' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
    return false;
  }
  if (e.keyCode == 13) {
    var ac_id = $('#' + ac_item + ' li:eq(' + chosen + ')').attr('id');
    var ac_name = $('#' + ac_item + ' li:eq(' + chosen + ')').text();
    activate_text_arrow(ac_id, ac_name, callback);
    return false;
  }
}
//country autocomplete function
var chosen = '';
function getCountryAutocomplete(e, textval, listval, callback, flag) {
  $('#country').val('');
  $('#ac-country').show();
  var countries = listval;
  var suggestions = [];
  $('#ac-country ul').empty();
  if (textval.length > 0) {
    if (flag == undefined)
      flag = false;
    var isFlag = flag;
    for (var i in countries) {
      if (isFlag == false) {
        isFlag = countries[i].is_active;
      }
      if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase()) && isFlag)
        suggestions.push([
          countries[i].country_id,
          countries[i].country_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-country ul').append(str);  //$("#country").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-country', callback);
}
//domain autocomplete function
function getDomainAutocomplete(e, textval, listval, callback, flag) {
  $('#domain').val('');
  $('#ac-domain').show();
  var domains = listval;
  var suggestions = [];
  $('#ac-domain ul').empty();
  if (textval.length > 0) {
    if (flag == undefined)
      flag = false;
    var isFlag = flag;
    for (var i in domains) {
      if (isFlag == false) {
        isFlag = domains[i].is_active;
      }
      if (~domains[i].domain_name.toLowerCase().indexOf(textval.toLowerCase()) && isFlag)
        suggestions.push([
          domains[i].domain_id,
          domains[i].domain_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-domain ul').append(str);  //$("#domain").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-domain', callback);
}
//usergroup autocomplete function
function getUserGroupAutocomplete(e, textval, listval, callback) {
  $('#ac-usergroup').show();
  $('#usergroup').val('');
  var usergroups = listval;
  var suggestions = [];
  $('#ac-usergroup ul').empty();
  if (textval.length > 0) {
    for (var i in usergroups) {
      if (~usergroups[i].user_group_name.toLowerCase().indexOf(textval.toLowerCase()) && usergroups[i].is_active == true)
        suggestions.push([
          usergroups[i].user_group_id,
          usergroups[i].user_group_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-usergroup ul').append(str);  //$("#usergroup").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-usergroup', callback);
}
//industry autocomplete function
function getIndustryAutocomplete(e, textval, listval, callback, flag) {
  $('#ac-industry').show();
  $('#industry').val('');
  var industries = listval;
  var suggestions = [];
  $('#ac-industry ul').empty();
  if (textval.length > 0) {
    if (flag == undefined)
      flag = false;
    var isFlag = flag;
    for (var i in industries) {
      if (isFlag == false) {
        isFlag = industries[i].is_active;
      }
      if (~industries[i].industry_name.toLowerCase().indexOf(textval.toLowerCase()) && isFlag)
        suggestions.push([
          industries[i].industry_id,
          industries[i].industry_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-industry ul').append(str);  //$("#industry").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-industry', callback);
}
//statutorynature autocomplete function
function getStatutoryNatureAutocomplete(e, textval, listval, callback, flag) {
  $('#ac-statutorynature').show();
  $('#statutorynature').val('');
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ac-statutorynature ul').empty();
  if (textval.length > 0) {
    if (flag == undefined)
      flag = false;
    var isFlag = flag;
    for (var i in statutorynatures) {
      if (isFlag == false) {
        isFlag = statutorynatures[i].is_active;
      }
      if (~statutorynatures[i].statutory_nature_name.toLowerCase().indexOf(textval.toLowerCase()) && isFlag)
        suggestions.push([
          statutorynatures[i].statutory_nature_id,
          statutorynatures[i].statutory_nature_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-statutorynature ul').append(str);  //$("#statutorynature").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-statutorynature', callback);
}
//geography autocomplete function
function getGeographyAutocomplete(e, textval, listval, callback, flag) {
  $('#ac-geography').show();
  $('#geography').val('');
  var geographies = listval;
  var suggestions = [];
  $('#ac-geography ul').empty();
  if (textval.length > 0) {
    if (flag == undefined)
      flag = false;
    var isFlag = flag;
    for (var i in geographies) {
      if (isFlag == false) {
        isFlag = geographies[i].is_active;
      }
      if (~geographies[i].geography_name.toLowerCase().indexOf(textval.toLowerCase()) && isFlag)
        suggestions.push([
          geographies[i].geography_id,
          geographies[i].geography_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-geography ul').append(str);  //$("#geography").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-geography', callback);
}
//statutory autocomplete function
function getStatutoryAutocomplete(e, textval, listval, callback) {
  $('#ac-statutory').show();
  $('#statutory').val('');
  $('#level1id').val('');
  var statutories = listval;
  var suggestions = [];
  $('#ac-statutory ul').empty();
  if (textval.length > 0) {
    for (var i in statutories) {
      if (~statutories[i].statutory_name.toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          statutories[i].statutory_id,
          statutories[i].statutory_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-statutory ul').append(str);  //$("#statutory").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-statutory', callback);
}
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
    $('#ac-user ul').append(str);  //$("#userid").val('');
                                   //$("#assignee").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-user', callback);
}
//form autocomplete function
function getFormAutocomplete(e, textval, listval, callback) {
  $('#ac-form').show();
  $('#formid').val('');
  var forms = listval;
  var suggestions = [];
  $('#ac-form ul').empty();
  if (textval.length > 0) {
    for (var i in forms) {
      if (~forms[i].form_name.toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          forms[i].form_id,
          forms[i].form_name
        ]);
    }
    //var str='<li id="0" onclick="activate_text(this,'+callback+')">Login</li>';
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-form ul').append(str);  //$("#formid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-form', callback);
}
//group autocomplete function
function getGroupAutocomplete(e, textval, listval, callback) {
  $('#ac-group').show();
  $('#group-id').val('');
  var groups = listval;
  var suggestions = [];
  $('#ac-group ul').empty();
  if (textval.length > 0) {
    for (var i in groups) {
      if (groups[i].is_active == true) {
        if (~groups[i].group_name.toLowerCase().indexOf(textval.toLowerCase()))
          suggestions.push([
            groups[i].client_id,
            groups[i].group_name
          ]);
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-group ul').append(str);  //$("#group-id").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-group', callback);
}
//businessgroup autocomplete function
function getBusinessGroupAutocomplete(e, textval, listval, callback) {
  $('#ac-businessgroup').show();
  $('#businessgroupid').val('');
  var bgroups = listval;
  var suggestions = [];
  $('#ac-businessgroup ul').empty();
  if (textval.length > 0) {
    for (var i in bgroups) {
      if (bgroups[i].client_id == $('#group-id').val()) {
        if (~bgroups[i].business_group_name.toLowerCase().indexOf(textval.toLowerCase()))
          suggestions.push([
            bgroups[i].business_group_id,
            bgroups[i].business_group_name
          ]);
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-businessgroup ul').append(str);  // $("#businessgroupid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-businessgroup', callback);
}
//legalentity autocomplete function
function getLegalEntityAutocomplete(e, textval, listval, callback) {
  $('#ac-legalentity').show();
  $('#legalentityid').val('');
  var lentity = listval;
  var suggestions = [];
  $('#ac-legalentity ul').empty();
  if (textval.length > 0) {
    for (var i in lentity) {
      if ($('#businessgroupid').val() != '') {
        if (lentity[i].business_group_id == $('#businessgroupid').val()) {
          if (~lentity[i].legal_entity_name.toLowerCase().indexOf(textval.toLowerCase()))
            suggestions.push([
              lentity[i].legal_entity_id,
              lentity[i].legal_entity_name
            ]);
        }
      } else {
        if (lentity[i].client_id == $('#group-id').val()) {
          if (~lentity[i].legal_entity_name.toLowerCase().indexOf(textval.toLowerCase()))
            suggestions.push([
              lentity[i].legal_entity_id,
              lentity[i].legal_entity_name
            ]);
        }
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-legalentity ul').append(str);  //$("#legalentityid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-legalentity', callback);
}
//division autocomplete function
function getDivisionAutocomplete(e, textval, listval, callback) {
  $('#ac-division').show();
  $('#divisionid').val('');
  var division = listval;
  var suggestions = [];
  $('#ac-division ul').empty();
  if (textval.length > 0) {
    for (var i in division) {
      if ($('#legalentityid').val() != '') {
        if (division[i].legal_entity_id == $('#legalentityid').val()) {
          if (~division[i].division_name.toLowerCase().indexOf(textval.toLowerCase()))
            suggestions.push([
              division[i].division_id,
              division[i].division_name
            ]);
        }
      } else {
        if (division[i].client_id == $('#group-id').val()) {
          if (~division[i].division_name.toLowerCase().indexOf(textval.toLowerCase()))
            suggestions.push([
              division[i].division_id,
              division[i].division_name
            ]);
        }
      }
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '" onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-division ul').append(str);  //$("#divisionid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-division', callback);
}
//unit autocomplete function
function getUnitAutocomplete(e, textval, listval, callback) {
  $('#ac-unit').show();
  $('#seatingunit').val('');
  $('#unit').val('');
  $('#unitid').val('');
  var units = listval;
  var suggestions = [];
  $('#ac-unit ul').empty();
  if (textval.length > 0) {
    for (var i in units) {
      var combineUnitName = '';
      if (units[i].unit_code != undefined) {
        combineUnitName = units[i].unit_code + '-' + units[i].unit_name;
      } else {
        combineUnitName = units[i].unit_name;
      }
      if (~combineUnitName.toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          units[i].unit_id,
          combineUnitName
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-unit ul').append(str);  //$("#seatingunit").val('');
                                   //$("#unit").val('');
                                   //$("#unitid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-unit', callback);
}
//reassignuser autocomplete function
function getReassignUserAutocomplete(e, textval, listval, callback) {
  $('#ac-user').show();
  $('#user').val('');
  var sUnit = $('#seatingunit').val();
  var assignees = listval;
  var suggestions = [];
  $('#ac-user ul').empty();
  if (textval.length > 0) {
    for (var i in assignees) {
      if (sUnit == '' || sUnit == assignees[i].seating_unit_id) {
        if (~assignees[i].user_name.toLowerCase().indexOf(textval.toLowerCase()))
          suggestions.push([
            assignees[i].user_id,
            assignees[i].user_name
          ]);
      }
    }
    var str = '<li id="0"onclick="activate_text(this,' + callback + ')">Client Admin</li>';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-user ul').append(str);  //$("#user").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-user', callback);
}
//client statutory autocomplete function
function getClientStatutoryAutocomplete(e, textval, listval, callback) {
  $('#ac-statutory').show();
  $('#act').val('');
  $('#level1id').val('');
  var acts = listval;
  var suggestions = [];
  $('#ac-statutory ul').empty();
  if (textval.length > 0) {
    for (var i in acts) {
      if (~acts[i].toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          acts[i].replace(/"/gi, '##'),
          acts[i]
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-statutory ul').append(str);  //$("#act").val('');
                                        //$("#level1id").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-statutory', callback);
}
//client statutory autocomplete function
function getComplianceTaskAutocomplete(e, textval, listval, callback) {
  $('#ac-compliancetask').show();
  $('#compliancetask').val('');
  $('#complianceid').val('');
  $('#compliancesid').val('');
  var compliancetasks = listval;
  var suggestions = [];
  $('#ac-compliancetask ul').empty();
  if (textval.length > 0) {
    for (var i in compliancetasks) {
      if (~compliancetasks[i].compliance_name.toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          compliancetasks[i].compliance_id,
          compliancetasks[i].compliance_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-compliancetask ul').append(str);  //$("#compliancetask").val('');
                                             //$("#complianceid").val('');
                                             //$("#compliancesid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-compliancetask', callback);
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
    $('#ac-businessgroup ul').append(str);  //$("#businessgroup").val('');
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
    $('#ac-legalentity ul').append(str);  //$("#legalentity").val('');
                                          //$("#legalentityid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-legalentity', callback);
}
//client division autocomplete function
function getClientDivisionAutocomplete(e, textval, listval, callback) {
  $('#ac-division').show();
  $('#division').val('');
  $('#divisionid').val('');
  var division = listval;
  var suggestions = [];
  $('#ac-division ul').empty();
  if (textval.length > 0) {
    for (var i in division) {
      if (~division[i].division_name.toLowerCase().indexOf(textval.toLowerCase()))
        suggestions.push([
          division[i].division_id,
          division[i].division_name
        ]);
    }
    var str = '';
    for (var i in suggestions) {
      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this,' + callback + ')">' + suggestions[i][1] + '</li>';
    }
    $('#ac-division ul').append(str);  //$("#division").val('');
                                       //$("#divisionid").val('');
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, 'ac-division', callback);
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