var countriesList;
var geographyLevelsList;
var geographiesList;

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#filter1');
var FilterLevel = $('#filter2');
var FilterName = $('#filter3');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

// auto complete - country
var country_val = $('#country');
var country_ac = $("#countryval");
var AcCountry = $('#ac-country');
var CurrentPassword = $('#current-password');
var PasswordSubmitButton = $('#password-submit');

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

$('#btn-geography-add').click(function () {
  $('#geography-view').hide();
  $('#geography-add').show();
  $('#country').val('');
  $('#countryval').val('');
  $('.error-message').html('');
  $('.tbody-geography-level').find('div').remove();
  $('#countryval').focus();
});
$('#btn-geography-back').click(function () {
  GetGeographies();
  $('#geography-view').show();
  $('#geography-add').hide();
  $('#country').val('');
  $('#countryval').val('');
  $('.error-message').html('');
  $('.tbody-geography-level').find('div').remove();
});
// display geographies list in view page
function loadGeographiesList(geographiesList) {
  var j = 1;
  $('.tbody-geography-list').find('tr').remove();
  $.each(geographiesList, function (keys, values) {
    var countryName = '';
    var geographyList = values;
    for (var countryList in countriesList) {
      if (countriesList[countryList].country_id == keys) {
        countryName = countriesList[countryList].country_name;
        break;
      }
    }
    $.each(geographyList, function (key, value) {
      var geographyId = value.geography_id;
      var geographyName = value.geography_name;
      var isActive = value.is_active;
      var level = '';
      var lposition = 0;
      var parentid = value.parent_id;
      var geographyLevelList = geographyLevelsList[keys];
      for (var i in geographyLevelList) {
        if (geographyLevelList[i].l_id == value.level_id) {
          level = geographyLevelList[i].l_name;
          lposition = geographyLevelList[i].l_position;
          break;
        }
      }
      var tableRow = $('#templates .table-geography-master .table-row');
      var clone = tableRow.clone();
      $('.sno', clone).text(j);
      $('.country', clone).text(countryName);
      $('.level', clone).text(level);
      $('.name', clone).text(geographyName);
      //edit icon
      $('.edit i', clone).attr("onClick", "displayEdit(" + geographyId + ",'" + geographyName + "', '" + countryName + "', "+ keys +", " + lposition + ", " + parentid + ")");
      if (value.is_active == true) {
          $('.status i', clone).attr('title', 'Click Here to DeActivate');
          $('.status i', clone).removeClass('fa-times text-danger');
          $('.status i', clone).addClass('fa-check text-success');
      } else {
          $('.status i', clone).attr('title', 'Click Here to Activate');
          $('.status i', clone).removeClass('fa-check text-success');
          $('.status i', clone).addClass('fa-times text-danger');
      }
      $('.status i', clone).attr("onClick", "showModalDialog(" + geographyId + ", " + isActive + ")");
      $('.tbody-geography-list').append(clone);
      j = j + 1;
    });
    $('[data-toggle="tooltip"]').tooltip();
  });
  if($('.tbody-geography-list').find('tr').length == 0){
      $('.tbody-geography-list').empty();
      var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
      var clone4 = tableRow4.clone();
      $('.no_records', clone4).text('No Records Found');
      $('.tbody-geography-list').append(clone4);
    }
}

//Status Title
function showTitle(e){
  if(e.className == "fa c-pointer status fa-times text-danger"){
    e.title = 'Click Here to Activate';
  }
  else if(e.className == "fa c-pointer status fa-check text-success")
  {
    e.title = 'Click Here to Deactivate';
  }
}

//open password dialog
function showModalDialog(geographyId, isActive){
  var passStatus = null;
  if (isActive == true) {
    passStatus = false;
    statusmsg = message.deactive_message;
  } else {
    passStatus = true;
    statusmsg = message.active_message;
  }
  CurrentPassword.val('');
  confirm_alert(statusmsg, function(isConfirm){
    if(isConfirm){
        Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete:   function() {
          CurrentPassword.focus();
          isAuthenticate = false;
        },
        close:   function() {
          if(isAuthenticate){
            changeStatus(geographyId, passStatus);
          }
        },
      });
      //e.preventDefault();
    }
  });
}


//validate password
function validateAuthentication(){
  var password = CurrentPassword.val().trim();
  if (password.length == 0) {
    displayMessage(message.password_required);
    CurrentPassword.focus();
    return false;
  } else if(validateMaxLength('password', password, "Password") == false) {
    return false;
  }
  displayLoader();
  mirror.verifyPassword(password, function(error, response) {
    if (error == null) {
      hideLoader();
      isAuthenticate = true;
      Custombox.close();
    }
    else {
      hideLoader();
      if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
      }
    }
  });
}

// activate/deactivate geographies
function changeStatus(geographyId, isActive) {
  function onSuccess(response) {
    if (isActive == false) {
      displaySuccessMessage(message.record_deactive);
    }
    else {
      displaySuccessMessage(message.record_active);
    }

    GetGeographies();
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.changeGeographyStatus(geographyId, isActive, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}
//Autocomplete Script Starts
//retrive country autocomplete value

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    loadGeographyFirstLevels(val[0]);
}

//Autocomplete Script ends
// dynamically load geograph first levels data according to geography level
function loadGeographyFirstLevels(saverecord) {
  //.log(if(! (saverecord in geographyLevelsList)));
  $('.tbody-geography-level').find('div').remove();
  var geographyLevelList = geographyLevelsList[saverecord];
  var levelposition;
  if((saverecord in geographyLevelsList)){
      $.each(geographyLevelList, function (key, value) {
      levelposition = value.l_position;
      var tableRow = $('#geography-level-templates');
      var clone = tableRow.clone();
      $('.title', clone).text(value.l_name);
      $('.geography-list', clone).attr('id', 'ulist' + levelposition);
      $('.addleft', clone).attr('id', 'datavalue' + levelposition);
      $('.addleft', clone).on('keypress', function (event) {
        saverecord1(value.l_position, event);
      });
      $('.popup-link', clone).attr('id', 'update' + levelposition);
      $('.add-geo', clone).on('click', function () {
        saverecord1(value.l_position, 'clickimage');
      });
      $('.glmid-class', clone).attr('id', 'glmid' + levelposition);
      $('.glmid-class', clone).val(value.l_id);
      $('.level-class', clone).attr('id', 'level' + levelposition);
      $('.level-class', clone).val(levelposition);
      $('.tbody-geography-level').append(clone);
      $('#geography-level-templates').show();
    });
  }
  else
  {
    displayMessage(message.no_records)
  }

  var setlevelstage = 1;
  $('#datavalue' + setlevelstage).val('');
  $('#ulist' + setlevelstage).empty();
  var firstlevelid = $('#glmid' + setlevelstage).val();
  var str = '';
  var idval = '';
  var clsval = '.list' + setlevelstage;
  var clsval1 = 'list' + setlevelstage;
  var geographyList = geographiesList[saverecord];
  for (var i in geographyList) {
    var setgeographyid = geographyList[i].geography_id;
    if (geographyList[i].level_id == firstlevelid && geographyList[i].is_active == true) {
      str += '<li id="' + setgeographyid + '" class="' + clsval1 + '" onclick="activate(this,' + setgeographyid + ',\'' + clsval + '\',' + saverecord + ',' + setlevelstage + ')" >' + geographyList[i].geography_name + '</li>';
    }
  }
  $('#ulist' + setlevelstage).append(str);
  $('.addleft').on('input', function (e) {
    //this.value = isCommon_Name($(this));
    isCommon_Name(this);
  });
}
//check & uncheck list data
function activate(element, id, type, country, level) {
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'list' + level + ' active') {
    $(element).removeClass('active');
    $(element).find('i').remove();
    for (var i = level + 1; i <= 10; i++) {
      $('#ulist' + i).empty();
    }
  } else {
    $(type).each(function (index, el) {
      $(el).removeClass('active');
      $(el).find('i').remove();
    });
    $(element).addClass('active');
    $(element).append('<i class="fa fa-check pull-right"></i>');
    load(id, level, country);
  }
}
//load geographymapping sub level data dynamically
function load(id, level, country) {
  var levelstages = parseInt(level) + 1;
  for (var k = levelstages; k <= 10; k++) {
    var setlevelstage = k;
    if ($('#geographyid').val() == '') {
      $('#datavalue' + setlevelstage).val('');
    }
    $('#ulist' + setlevelstage).empty();
    var str = '';
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var geographyLevelList = geographyLevelsList[country];
    var levelid = $('#glmid' + setlevelstage).val();
    var geographyList = geographiesList[country];
    for (var i in geographyList) {
      var setgeographyid = geographyList[i].geography_id;
      if (id == geographyList[i].parent_id && geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
        str += '<li id="' + setgeographyid + '" class="' + clsval1 + '" onclick="activate(this,' + setgeographyid + ',\'' + clsval + '\',' + country + ',' + setlevelstage + ')" >' + geographyList[i].geography_name + '</li>';
      }
    }
    $('#ulist' + setlevelstage).append(str);
  }
}
//filter process
$('.listfilter').keyup(function () {
  processSearch();
});

function processSearch(){
  var filter1 = $('#filter1').val().toLowerCase();
  var filter2 = $('#filter2').val().toLowerCase();
  var filter3 = $('#filter3').val().toLowerCase();
  usr_status = $('.search-status-li.active').attr('value');

  var filteredList = {};
  for (var entity in geographiesList) {
    var flist = [];
    var countryGeographyList = geographiesList[entity];
    for (var geography in countryGeographyList) {
      var cName = '';
      for (country in countriesList) {
        var cId = countriesList[country].country_id;
        if (cId == entity) {
          cName = countriesList[country].country_name;
        }
      }
      var lName = '';
      for (level in geographyLevelsList) {
        var cGeography = geographyLevelsList[level];
        for (g in cGeography) {
          var lId = cGeography[g].l_id;
          if (lId == countryGeographyList[geography].level_id) {
            lName = cGeography[g].l_name;
          }
        }
      }
      var filter1val = cName;
      var filter2val = lName;
      var filter3val = countryGeographyList[geography].geography_name;
      if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3)) {
        if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == countryGeographyList[geography].is_active)){
          flist.push(countryGeographyList[geography]);
        }
      }
      filteredList[entity] = flist;
    }
  }
  loadGeographiesList(filteredList);
}

//validate and insert records in geograpahymapping table
function saverecord1(j, e) {
  var data = e.keyCode;
  if (data == 13 || data == undefined) {
    var checkLength = validateMaxLength("geography_lvl", $('#datavalue' + j).val(), "Geography Level")
    if (checkLength) {
      //displayMessage('');
      var levelstage = $('#level' + j).val();
      var glm_id = $('#glmid' + j).val();
      var datavalue = $('#datavalue' + j).val().trim();
      var map_gm_id = [];
      var map_gm_name = [];
      map_gm_name.push($('#countryval').val());
      var last_geography_id = 0;
      var last_level = 0;
      for (k = 1; k < j; k++) {
        $('.list' + k + '.active').each(function (index, el) {
          map_gm_id.push(parseInt(el.id));
          map_gm_name.push(el.innerHTML.replace(/<i class="fa fa-check pull-right"><\/i>/gi, ''));
          last_geography_id = el.id;
          last_level = k;
        });
      }
      if (map_gm_id == 0 && levelstage > 1) {
        displayMessage(message.levelselection_required);
      } else if (datavalue.length == 0) {
        var msg = 'Level-' + levelstage;
        displayMessage(msg + message.shouldnot_empty);
      } else {
        function onSuccess(response) {
          displaySuccessMessage(message.added_success);
          $('#datavalue' + j).val('');
          reload(last_geography_id, last_level, $('#country').val());
          hideLoader();
        }
        function onFailure(error) {
          if (error == 'GeographyNameAlreadyExists') {
            displayMessage(message.geographyname_exists);
          } else {
            displayMessage(error);
          }
        }
        countryId = parseInt($('#country').val());
        if (map_gm_id.length == 0) {
          map_gm_id.push(0);
        }
        displayLoader();
        mirror.saveGeography(parseInt(glm_id), datavalue, map_gm_id, map_gm_name, countryId, function (error, response) {
          if (error == null) {
            onSuccess(response);
            $('.listfilter').val('');
          } else {
            hideLoader();
            onFailure(error);
          }
        });
      }
    }
  }
}
// reload newly added data in geography list
function reload(last_geography_id, last_level, cny) {
  function onSuccess(data) {
    geographiesList = data.geographies;
    load(last_geography_id, last_level, cny);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getGeographies(function (error, response) {
    if (error == null) {
      onSuccess(response);
      $('.listfilter').val('');
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}
// edit geography master process
function displayEdit(geographyId, geographyName, country, countryid, lposition, parentidval) {
  $('.error-message').html('');
  $('#geography-view').hide();
  $('#geography-add').show();
  $('#geographyid').val(geographyId);
  $('#countryval').val(country.replace(/##/gi, '"'));
  $('#country').val(countryid);
  $('.tbody-geography-level').find('div').remove();
  var geographyLevelList = geographyLevelsList[countryid];
  var levelposition;
  $.each(geographyLevelList, function (key, value) {
    levelposition = value.l_position;
    var tableRow = $('#geography-level-templates');
    var clone = tableRow.clone();
    $('.title', clone).text(value.l_name);
    $('.addleft', clone).on('input', function(e) {
        this.value = isAlphabetic($(this));
    });
    if (levelposition == lposition) {
      $('.geography-list', clone).attr('id', 'ulist' + levelposition);
      $('.addleft', clone).attr('readonly', false);
      $('.addleft', clone).attr('id', 'datavalue' + levelposition);
      $('.addleft', clone).on('keypress', function (event) {
        updaterecord(value.l_name, value.l_position, event);
      });
      $('.popup-link', clone).attr('id', 'update' + levelposition);
      $('.add-geo', clone).on('click', function () {
        updaterecord(value.l_name, value.l_position, 'clickimage');
      });
      $('.glmid-class', clone).attr('id', 'glmid' + levelposition);
      $('.glmid-class', clone).val(value.l_id);
      $('.level-class', clone).attr('id', 'level' + levelposition);
      $('.level-class', clone).val(levelposition);
    } else {
      $('.geography-list', clone).attr('id', 'ulist' + levelposition);
      $('.addleft', clone).attr('readonly', true);
      $('.addleft', clone).attr('id', 'datavalue' + levelposition);

      $('.addleft', clone).on('keypress', function (event) {
        saverecord1(value.l_position, event);
      });
      /*$('.popup-link', clone).attr('id', 'update'+levelposition);
      $(".add-geo", clone).on("click", function() {
        saverecord1(value["l_position"], 'clickimage');
      });*/
      $('.glmid-class', clone).attr('id', 'glmid' + levelposition);
      $('.glmid-class', clone).val(value.l_id);
      $('.level-class', clone).attr('id', 'level' + levelposition);
      $('.level-class', clone).val(levelposition);
      $('.visible-class', clone).attr('id', 'visible' + levelposition);
    }
    $('.tbody-geography-level').append(clone);
    $('#geography-level-templates').show();
  });
  $('#datavalue' + lposition).val(geographyName.replace(/##/gi, '"'));
  var levelstages = lposition - 1;
  var parentid = parentidval;
  var parentid1 = parentidval;
  var dispparentid = 1;
  for (var k = levelstages; k >= 1; k--) {
    var setlevelstage = k;
    $('#datavalue' + setlevelstage).val('');
    $('#ulist' + setlevelstage).empty();
    var str = '';
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var geographyLevelList = geographyLevelsList[countryid];
    var levelid = $('#glmid' + setlevelstage).val();
    var geographyList = geographiesList[countryid];
    for (var i in geographyList) {
      var setgeographyid = geographyList[i].geography_id;
      if (geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
        if (parentid1 == geographyList[i].geography_id) {
          parentid1 = geographyList[i].parent_id;
          $('#visible' + setlevelstage).val(parentid1);
        }
      }
    }
    for (var i in geographyList) {
      var setgeographyid = geographyList[i].geography_id;
      if ($('#visible' + setlevelstage).val() == geographyList[i].parent_id && geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
        if (parentid == geographyList[i].geography_id) {
          str += '<li id="' + setgeographyid + '" class="' + clsval1 + ' active" onclick="activateedit(this,' + setgeographyid + ',\'' + clsval + '\',' + countryid + ',' + setlevelstage + ',' + levelstages + ')" >' + geographyList[i].geography_name + '</li>';
          parentid = geographyList[i].parent_id;
        } else {
          str += '<li id="' + setgeographyid + '" class="' + clsval1 + '" onclick="activateedit(this,' + setgeographyid + ',\'' + clsval + '\',' + countryid + ',' + setlevelstage + ',' + levelstages + ')" >' + geographyList[i].geography_name + '</li>';
        }
      }
    }
    $('#ulist' + setlevelstage).append(str);
  }
  $('.addleft').on('input', function (e) {
    //this.value = isCommon($(this));
    isCommon(this);
  });
}
//update geography master
function updaterecord(lname, j, e) {
  var data = e.keyCode;
  if (data == 13 || data == undefined) {
    var checkLength = validateMaxLength("geography_lvl", $('#datavalue' + j).val(), "Geography Level")
    if (checkLength) {
      $('.error-message').html('');
      var levelstage = $('#level' + j).val();
      var glm_id = $('#glmid' + j).val();
      var geographyid = $('#geographyid').val();
      var datavalue = $('#datavalue' + j).val().trim();
      var map_gm_id = [];
      var map_gm_name = [];
      map_gm_name.push($('#countryval').val());
      var last_geography_id = 0;
      var last_level = 0;
      for (k = 1; k < j; k++) {
        $('.list' + k + '.active').each(function (index, el) {
          map_gm_id.push(parseInt(el.id));
          map_gm_name.push(el.innerHTML);
          last_geography_id = el.id;
          last_level = k;
        });
      }
      if (map_gm_id == 0 && levelstage > 1) {
        displayMessage(message.levelselection_required);
      } else if (datavalue.length == 0) {
        var msg = 'Level-' + levelstage;
        displayMessage(msg + message.shouldnot_empty);
      } else {
        function onSuccess(response) {
          Search_status.removeClass();
          Search_status.addClass('fa');
          Search_status.text('All');
          displaySuccessMessage(lname + " " + message.updated_success);
          GetGeographies();
          $('#geography-view').show();
          $('#geography-add').hide();
          hideLoader();
        }
        function onFailure(error) {
          if (error == 'GeographyNameAlreadyExists') {
            displayMessage(message.geographyname_exists);
          } else if (error == 'InvalidGeographyId') {
            displayMessage(message.invalid_geographyid);
          } else {
            displayMessage(error);
          }
        }
        if (map_gm_id.length == 0) {
          map_gm_id.push(0);
        }
        displayLoader();
        mirror.updateGeography(parseInt(geographyid), parseInt(glm_id), datavalue, map_gm_id, map_gm_name, parseInt($('#country').val()), function (error, response) {
          if (error == null) {
            onSuccess(response);
            $('.listfilter').val('');
          } else {
            hideLoader();
            onFailure(error);
          }
        });
      }
    }
  }
}
//check & uncheck list data
function activateedit(element, id, type, country, level, levelstage) {
  $(type).each(function (index, el) {
    $(el).removeClass('active');
  });
  $(element).addClass('active');
  loadedit(id, level, country, levelstage);
}
//load geographymapping sub level data dynamically
function loadedit(id, level, country, levelstagemax) {
  var levelstages = parseInt(level) + 1;
  for (var k = levelstages; k <= levelstagemax; k++) {
    var setlevelstage = k;
    if ($('#geographyid').val() == '') {
      $('#datavalue' + setlevelstage).val('');
    }
    $('#ulist' + setlevelstage).empty();
    var str = '';
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var geographyLevelList = geographyLevelsList[country];
    var levelid = $('#glmid' + setlevelstage).val();
    var geographyList = geographiesList[country];
    for (var i in geographyList) {
      var setgeographyid = geographyList[i].geography_id;
      if (id == geographyList[i].parent_id && geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
        str += '<li id="' + setgeographyid + '" class="' + clsval1 + '" onclick="activateedit(this,' + setgeographyid + ',\'' + clsval + '\',' + country + ',' + setlevelstage + ',' + levelstagemax + ')" >' + geographyList[i].geography_name + '</li>';
      }
    }
    $('#ulist' + setlevelstage).append(str);
  }
}
// get geography master list from api
function GetGeographies() {
  function onSuccess(data) {
    geographyLevelsList = data.geography_levels;
    geographiesList = data.geographies;
    countriesList = data.countries;
    loadGeographiesList(geographiesList);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getGeographies(function (error, response) {
    if (error == null) {
      onSuccess(response);
      $('.listfilter').val('');
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}

function renderControls(){
  GetGeographies();

  //status of the list
  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }
    processSearch();
  });

  country_ac.keyup(function(e){
    var condition_fields = ["is_active"];
    var condition_values = [true];
    var text_val = $(this).val();
    commonAutoComplete(
      e, AcCountry, country_val, text_val,
      countriesList, "country_name", "country_id", function (val) {
          onAutoCompleteSuccess(country_ac, country_val, val);
      }, condition_fields, condition_values);
  });

  Search_status.change(function() {
      processSearch();
  });
  PasswordSubmitButton.click(function() {
    validateAuthentication();
  });

}

//initialization
$(document).ready(function () {
  renderControls();
});
