var countriesList;
var domainsList;
var statutoryLevelsList;
$('.btn-statutorylevel-cancel').click(function () {
  $('.fieldvalue').val('');
  $('.hiddenvalue').val('');
  $('#countryval').val('');
  $('#country').val('');
  $('#domainval').val('');
  $('#domain').val('');
});
//get statutory level master data from api
function GetStatutoryLevels() {
  function onSuccess(data) {
    statutoryLevelsList = data.statutory_levels;
    countriesList = data.countries;
    domainsList = data.domains;
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getStatutoryLevels(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//Autocomplete Script Starts
//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country').val(val[0]);
  $('#domainval').focus();
  loadstatutoryLevelsList();
}
//load country list in autocomplete text box  
$('#countryval').keyup(function (e) {
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, function (val) {
    onCountrySuccess(val);
  });
});
//retrive domain autocomplete value
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domain').val(val[0]);
  $('#level1').focus();
  loadstatutoryLevelsList();
}
//load domain list in autocomplete textbox  
$('#domainval').keyup(function (e) {
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, function (val) {
    onDomainSuccess(val);
  });
});
//Autocomplete Script ends
//load statutory level according to country & domain
function loadstatutoryLevelsList() {
  $('.error-message').html('');
  $('.fieldvalue').val('');
  $('.hiddenvalue').val('');
  var countryval = $('#country').val();
  var domainval = $('#domain').val();
  var levellist;
  if (countryval in statutoryLevelsList && domainval in statutoryLevelsList[countryval]) {
    levellist = statutoryLevelsList[countryval][domainval];
    for (var entity in levellist) {
      var levelPosition = levellist[entity].l_position;
      var levelName = levellist[entity].l_name;
      var levelId = levellist[entity].l_id;
      $('#level' + levelPosition).val(levelName);
      $('#levelid' + levelPosition).val(levelId);
    }
  }
}
//validation
function validate() {
  var checkLength = statutoryLevelValidate();
  if (checkLength) {
    if ($('#country').val().trim().length == 0) {
      displayMessage(message.country_required);
    } else if ($('#domain').val().trim().length == 0) {
      displayMessage(message.domain_required);
    } else if ($('#level1').val().trim().length == 0) {
      displayMessage(message.levelone_title_required);
    } else {
      displayMessage('');
      return true;
    }
  }
}
//save/update statutory level master
$('#submit').click(function () {
  displayMessage('');
  var country = $('#country').val();
  var domain = $('#domain').val();
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
      var isAdd = true;
      var passlevellist = [];
      for (var k = 1; k <= 10; k++) {
        if ($('#levelid' + k).val().trim() != '') {
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
        }  /*            if($("#levelid"+k).val().trim().length > 0 && $("#level"+k).val().trim().length == 0){
              var msg = "Level "+ k;
              displayMessage(msg + message.shouldnot_empty)
              return false;
            }else if($("#level"+k).val().trim().length > 0){
              if($("#levelid"+k).val().trim().length > 0){
                passlevellist.push({"l_position" : k, "l_name" : $("#level"+k).val().trim(), "l_id" : parseInt($("#levelid"+k).val())});
                isAdd = false;
              }else{
                passlevellist.push({"l_position" : k, "l_name" : $("#level"+k).val().trim(), "l_id" : null});
              }
            }*/
      }
      function onSuccess(response) {
        if (isAdd) {
          displayMessage(message.record_added);
        } else {
          displayMessage(message.record_updated);
        }
        GetStatutoryLevels();
        jQuery('.btn-statutorylevel-cancel').focus().click();
        $('#countryval').focus();
      }
      function onFailure(error) {
        if (error == 'DuplicateStatutoryLevelsExists') {
          displayMessage(message.statutorylevel_exists);
        } else {
          displayMessage(error);
        }
      }
      mirror.saveAndUpdateStatutoryLevels(parseInt(country), parseInt(domain), passlevellist, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    } else {
      displayMessage(message.intermediatelevel_required);
    }
  }
});
$('.fieldvalue').keyup(function (evt) {
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
//initialization
$(document).ready(function () {
  GetStatutoryLevels();
  $('#countryval').focus();
});
$('.fieldvalue').on('input', function (e) {
  this.value = isAlphabetic($(this));
});