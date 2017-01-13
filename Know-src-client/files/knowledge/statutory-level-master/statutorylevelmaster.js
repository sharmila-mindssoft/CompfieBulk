var countriesList;
var domainList;
var statutoryLevelsList;
// auto complete - country
var country_val = $('#country');
var country_ac = $("#countryval");
var AcCountry = $('#ac-country');

// auto complete - domain
var domain_val = $('#domain');
var domain_ac = $("#domainval");
var AcDomain = $('#ac-domain')
$('.btn-statutorylevel-cancel').click(function () {
  resetFields();
});

function resetFields(){
  console.log("1")
  $('#countryval').val('');
  $('#country').val('');
  console.log($('#country').val());
  $('#domainval').val('');
  $('#domain').val('');
  $('.input-sm').val('');
  $('.hiddenvalue').val('');
}
//get statutory level master data from api
function GetStatutoryLevels() {
  function onSuccess(data) {
    statutoryLevelsList = data.statutory_levels;
    console.log(statutoryLevelsList)
    countriesList = data.countries;
    domainList = data.domains;
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
//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'country'){
      $('#domainval').focus();
      //loadstatutoryLevelsList();
    }
    else if(current_id == 'domain'){
      $('#level1').focus();
      loadstatutoryLevelsList();
    }
}

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

  domain_ac.keyup(function(e){
    var text_val = $(this).val();
    var domain_list = [];
    var c_ids = null;
    var check_val = false;
    if(country_val.val() != ''){
      console.log("ctry:"+country_val.val())
      for(var i=0;i<domainList.length;i++){
        c_ids = domainList[i].country_ids;

        for(var j=0;j<c_ids.length;j++){
          if(c_ids[j] == country_val.val())
          {
            check_val = true;
          }
        }

        if(check_val == true && domainList[i].is_active == true){
          domain_list.push({
            "domain_id": domainList[i].domain_id,
            "domain_name": domainList[i].domain_name
          });
          check_val = false;
          //break;
        }
      }
      commonAutoComplete(
        e, AcDomain, domain_val, text_val,
        domain_list, "domain_name", "domain_id", function (val) {
            onAutoCompleteSuccess(domain_ac, domain_val, val);
        });
    }
    else{
      displayMessage(message.country_required);
    }

  });

//Autocomplete Script ends
//load statutory level according to country & domain
function loadstatutoryLevelsList() {
  console.log("1:")
  $('.error-message').html('');
  //$('.input-sm').val('');
  //$('.hiddenvalue').val('');
  var countryval = $('#country').val();
  var domainval = $('#domain').val();
  var levellist;
  console.log("data:"+countryval in statutoryLevelsList)
  if (countryval in statutoryLevelsList && domainval in statutoryLevelsList[countryval]) {
    levellist = statutoryLevelsList[countryval][domainval];
    console.log("len:"+levellist.length)
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
  console.log($('#country').val())
  var checkLength = statutoryLevelValidate();
  if (checkLength) {
    if ($('#country').val().trim().length == 0) {
      displayMessage(message.country_required);
    } else if ($('#domain').val().trim().length == 0) {
      displayMessage(message.domain_required);
    } else if ($('#level1').val().trim().length == 0) {
      displayMessage(message.levelone_title_required);
    } else {
      //displayMessage('');
      return true;
    }
  }
}
//save/update statutory level master
$('#submit').click(function () {
  //displayMessage('');
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
          console.log(('level' + k),$('#level' + k).val())
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
        GetStatutoryLevels();
        resetFields();
        $('#countryval').focus();
      }
      function onFailure(error, response) {
        console.log("e:"+error, response)
        if (error == 'DuplicateStatutoryLevelsExists') {
          displayMessage(message.statutorylevel_exists);
        }else if (error == 'LevelShouldNotbeEmpty') {
          var levelValue = response.level_id;
          var msg = 'Level ' + levelValue + ' cannot be deleted, hence name';
          displayMessage(msg + message.shouldnot_empty);
        } else {
          displayMessage(error);
        }
      }
      mirror.saveAndUpdateStatutoryLevels(parseInt(country), parseInt(domain), passlevellist, function (error, response) {
        if (error == null) {
          $('.input-sm').val('');
          $('.hiddenvalue').val('');
          onSuccess(response);
        } else {
          onFailure(error, response);
        }
      });
    } else {
      displayMessage(message.intermediatelevel_required);
    }
  }
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
//initialization
$(document).ready(function () {
  GetStatutoryLevels();
  $('#countryval').focus();
});
$('.input-sm').on('input', function (e) {
  this.value = isAlphabetic($(this));
});