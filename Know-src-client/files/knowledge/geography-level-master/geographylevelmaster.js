var countriesList;
// auto complete - country
var country_val = $('#country');
var country_ac = $("#countryval");
var AcCountry = $('#ac-country');
var insertValueText = null;

var geographyLevelsList;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

$('.btn-geographylevel-cancel').click(function () {
  $('.input-sm').val('');
  $('.hiddenvalue').val('');
  $('#countryval').val('');
  $('#country').val('');
  $('#insertvalue').val('');
  $('#view-insert-level').hide();
  $('#add').show();
});
$('.add-insert-level').click(function () {
  $('#view-insert-level').show();
  $('#add').hide();
});
$('.insert-level-cancel').click(function () {
  loadLevels();
  $('#insertvalue').val('');
  $('#view-insert-level').hide();
  $('#add').show();
});
//get geography level master from api
function GetGeographyLevels() {
  function onSuccess(data) {
    geographyLevelsList = data.geography_levels;
    countriesList = data.countries;
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getGeographyLevels(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}
//Autocomplete Script Starts
//load country list in autocomplete text box
//var chosen = "";
/*$("#countryval").keyup(function(e){
	/*if (e.keyCode == 40) {
        if(chosen === "") {
            chosen = 0;
        } else if((chosen+1) < $('#ulist_text li').length) {
            chosen++;
        }
        $('#ulist_text li').removeClass('auto-selected');
        $('#ulist_text li:eq('+chosen+')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if(chosen === "") {
            chosen = 0;
        } else if(chosen > 0) {
            chosen--;
        }
        $('#ulist_text li').removeClass('auto-selected');
        $('#ulist_text li:eq('+chosen+')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 13) {
    	var id = $('.country_auto.auto-selected').attr('id');
    	var id_val = $('.country_auto.auto-selected').text().trim();
        activate_text(id,id_val);
        return false;
    }*/
/*var textval = $(this).val();
  	$("#autocompleteview").show();
  	var countries = countriesList;
  	var suggestions = [];
  	$('#ulist_text').empty();
  	if(textval.length>0){
	    for(var i in countries){
	      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == true) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]);
	    }
	    var str='';
	    for(var i in suggestions){
	        str += '<li class="country_auto" id="'+suggestions[i][0]+'"onclick="activate_text(this)">'+suggestions[i][1]+'</li>';
	    }
	    $('#ulist_text').append(str);
	    $("#country").val('');
    }else{
    	$("#country").val('');
    	$("#autocompleteview").hide();
    }
});*/
//set selected autocomplte value to textbox
/*function activate_text (element) {
  $("#autocompleteview").hide();
  $("#countryval").val($(element).text());
  $("#country").val($(element).attr('id'));
  $("#view-insert-level").hide();
  $("#add").show();
  loadGeographyLevelsList($(element).attr('id'));
}*/
//Autocomplete Script ends*/
//Autocomplete Script Starts
//retrive country autocomplete value
//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
  value_element.val(val[1]);
  id_element.val(val[0]);
  value_element.focus();
  for(var i=1;i<=10;i++){
    $('#level'+i).val('');
    $('#levelid'+i).val('');
  }
  $('#view-insert-level').hide();
  $('#add').show();
  loadGeographyLevelsList(val[0]);
  $('#level1').focus();
}

//load country list in autocomplete text box
country_ac.keyup(function (e) {
  var condition_fields = ["is_active"];
  var condition_values = [true];
  var text_val = $(this).val();
  commonAutoComplete(
    e, AcCountry, country_val, text_val,
    countriesList, "country_name", "country_id", function (val) {
        onAutoCompleteSuccess(country_ac, country_val, val);
    }, condition_fields, condition_values);
});
//Autocomplete Script ends
//display geography level master for selected country
function loadGeographyLevelsList(countryval) {
  $('.error-message').html('');
  //$('.input-sm').val('');
  //$('.hiddenvalue').val('');
  var levellist;
  if (geographyLevelsList[countryval] != undefined) {
    levellist = geographyLevelsList[countryval];
      for (var entity in levellist) {
        var levelPosition = levellist[entity].l_position;
        var levelName = levellist[entity].l_name;
        var levelId = levellist[entity].l_id;
        $('#level' + levelPosition).val(levelName);
        $('#levelid' + levelPosition).val(levelId);
      }
      if (levellist.length < 10)
        $('#add').show();
      else
        $('#add').hide();
    }

}
//validation
function geographyLevelValidate() {
    if (validateMaxLength("level_value", $('#insertvalue').val(), "Title Name") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level1').val(), "Level 1") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level2').val(), "Level 2") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level3').val(), "Level 3") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level4').val(), "Level 4") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level5').val(), "Level 5") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level6').val(), "Level 6") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level7').val(), "Level 7") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level8').val(), "Level 8") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level9').val(), "Level 9") == false) {
        return false;
    } else if (validateMaxLength("level_value", $('#level10').val(), "Level 10") == false) {
        return false;
    } else {
        //displayMessage();
        return true;
    }
}
function validate() {
  var checkLength = geographyLevelValidate();
  if (checkLength) {
    if ($('#country').val().trim().length == 0) {
      displayMessage(message.country_required);
    } else if ($('#level1').val().trim().length == 0) {
      displayMessage(message.levelone_title_required.replace('name', "one"));
    } else {
      //displayMessage('');
      return true;
    }
  }
}
//save or update geography level master
$('#submit').click(function () {
  var country = $('#country').val();
  if (validate()) {
    for (var k = 1; k <= 10; k++) {
      if ($('#level' + k).val().trim().length > 0) {
        var maxlevel = k;
      }
    }
    var result = true;
    for (var k = 1; k <= maxlevel; k++) {
      if ($('#level' + k).val().trim().length == 0) {
        result = false;
      }
    }
    if (result) {
      var passlevellist = [];
      var isAdd = true;
      for (var k = 1; k <= 10; k++) {
        if ($('#levelid' + k).val() != '') {
          var isRemove = false;
          if ($('#level' + k).val().trim() == '') {
            isRemove = true;
          }
          passlevellist.push({
            'l_position': k,
            'l_name': $('#level' + k).val().trim(),
            'l_id': parseInt($('#levelid' + k).val()),
            'is_remove': isRemove
          });
          isAdd = false;
        } else {
          if ($('#level' + k).val().trim() != '') {
            passlevellist.push({
              'l_position': k,
              'l_name': $('#level' + k).val().trim(),
              'l_id': null,
              'is_remove': false
            });
          }
        }
      }
      function onSuccess(response) {
        if (isAdd) {
          displaySuccessMessage(message.record_added);
        } else {
          displaySuccessMessage(message.record_updated);
        }
        jQuery('.btn-geographylevel-cancel').focus().click();
        GetGeographyLevels();
        hideLoader();
      }
      function onFailure(error, response) {
        if (error == 'DuplicateGeographyLevelsExists') {
          displayMessage(message.geographylevel_exists);
        } else if (error == 'LevelShouldNotbeEmpty') {
          var levelValue = response.level_id;
          var msg = 'Level ' + levelValue + ' cannot be deleted, hence name';
          displayMessage(message.geography_level_empty.replace('levelValue', levelValue) + message.shouldnot_empty);
        } else {
          displayMessage(error);
        }
      }
      displayLoader();
      mirror.saveAndUpdateGeographyLevels(parseInt(country), passlevellist, insertValueText, function (error, response) {
        if (error == null) {
          $('.input-sm').val('');
          $('.hiddenvalue').val('');
          $('#country').val('');
          onSuccess(response);
        } else {
          hideLoader();
          onFailure(error, response);
        }
      });
    } else {
      displayMessage(message.intermediatelevel_required);
    }
  }
});
//insert a new level in between levels
$('#insert-record').click(function () {
  var insertlvl = parseInt($('#levelslist').val());
  var insertvalue = $('#insertvalue').val().trim();
  var inserlevelstatus = true;
  if (insertvalue.length > 0 && validateMaxLength("level_value", $('#insertvalue').val(), "Title Name") == true && $('#level' + (insertlvl-1)).val() != "") {
    for (var x = 10; x >= insertlvl; x--) {
      var s = x - 1;
      if (x == insertlvl) {
        $('#level' + x).val(insertvalue);
        $('#levelid' + x).val('');
        insertValueText = insertValueText + "," + "Geography Level \""+insertvalue+"\" is inserted between \""+$('#level' + s).val()+ "\" and \""+$('#level' + (x+1)).val()+"\"";
      } else {
        $('#level' + x).val($('#level' + s).val());
        $('#levelid' + x).val($('#levelid' + s).val());
      }
    }
    $('#levelslist').val('2');
    $('#insertvalue').val('');
    $('#view-insert-level').hide();
    $('#add').show();
    //displayMessage('');
  } else {
    if ($('#country').val().trim().length == 0) {
      displayMessage(message.country_required);
    }else if (insertvalue.length == 0){
      displayMessage(message.title_required);
    }else if(validateMaxLength("level_value", insertvalue, "Title Name") == false) {
        displayMessage(message.title_max50);
    } else if($('#level' + (insertlvl-1)).val() == "") {
      displayMessage(message.levelone_title_required.replace('name', (insertlvl-1)));
    }
    $('#add').hide();
    inserlevelstatus = false;
  }
  for (var i = 1; i <= 10; i++) {
    if ($('#level' + i).val() == '') {
      $('#add').show();
    } else {
      $('#add').hide();
    }
  }
  if (inserlevelstatus == false)
    $('#add').hide();
});
//initialization
$(document).ready(function () {
  GetGeographyLevels();
  $('#countryval').focus();
  loadLevels();
});
$('.input-sm').keyup(function (evt) {
  var element = $(evt.target);
  var tabIndex = element.attr('tabIndex');
  if (evt.keyCode == 13) {
    if (tabIndex == 10) {
      if (validate()) {
        jQuery('#submit').focus().click();
      }
    } else {
      var nextElement = $('input[tabIndex=' + (parseInt(tabIndex) + 1) + ']');
      if (nextElement) {
        nextElement.focus();
      }
      return false;
    }
  }
});
function loadLevels() {
  $('#levelslist').empty();
  for(var i=2;i<=10;i++)
  {
    $('#levelslist').append($('<option></option>').val(i).html("Level "+i));
  }
}

/*$('#levelslist').on('change', function(e) {
  $('#levelslist  option:gt(0)').remove();
  loadLevels();
});*/

$('#insertvalue').on('input', function (e) {
  this.value = isCommon_Name($(this));
});

for (var k = 1; k <= 10; k++) {
  $('#level'+k).on('input', function (e) {
    this.value = isCommon_Name($(this));
  });
}