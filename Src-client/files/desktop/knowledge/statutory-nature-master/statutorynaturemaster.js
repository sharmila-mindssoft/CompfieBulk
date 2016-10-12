var countriesList;
$('#btn-statutory-nature-add').click(function () {
  $('#statutory-nature-view').hide();
  $('#statutory-nature-add').show();
  $('#statutory-nature-name').val('');
  $('#statutory-nature-id').val('');
  $('#country-id').val('');
  $('#country-name').val('');
  displayMessage('');
  $('#country-name').focus();
});
$('#btn-statutory-nature-cancel').click(function () {
  $('#statutory-nature-add').hide();
  $('#statutory-nature-view').show();
});
function initialize() {
  clearMessage();
  $('.filter-country-text-box').val();
  $('.filter-text-box').val();
  function onSuccess(data) {
    loadStatNatureData(data.statutory_natures);
    countriesList = data.countries;
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getStatutoryNatureList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
function loadStatNatureData(statNatureList) {
alert("inside load")
  $('.tbody-statutory-nature-list').find('tr').remove();
  var sno = 0;
  //for (var i in statNatureList) {
    var statNature = statNatureList;
    $.each(statNature, function (key, value) {
      var statNatureName = value.statutory_nature_name;
      var statNatureId = value.statutory_nature_id;
      var countryName = value.country_name;
      var countryId = value.country_id;
      var statNatureActive = value.is_active;
      var passStatus = null;
      var classValue = null;
      if (statNatureActive == true) {
        passStatus = false;
        classValue = 'active-icon';
      } else {
        passStatus = true;
        classValue = 'inactive-icon';
      }
      var tableRow = $('#templates .table-statutory-nature-list .table-row');
      var clone = tableRow.clone();
      sno = sno + 1;
      $('.sno', clone).text(sno);
      $('.statutory-nature-name', clone).text(statNatureName);
      $('.country-name', clone).text(countryName);
      $('.edit-icon').attr('title', 'Edit');
      $('.edit-icon', clone).on('click', function () {
        statNature_edit(statNatureId, statNatureName, countryId);
      });
      $('.status', clone).addClass(classValue);
      $('.active-icon').attr('title', 'Deactivate');
      $('.inactive-icon').attr('title', 'Activate');
      $('.status', clone).on('click', function () {
        statNature_active(statNatureId, passStatus);
      });
      $('.tbody-statutory-nature-list').append(clone);
    });
  //}
}
$('#statutory-nature-name').keypress(function (e) {
  var statutoryNatureNameVal = $('#statutory-nature-name').val().trim();
  if (e.which == 13) {
    if (statutoryNatureNameVal == '') {
      displayMessage(message.statutorynature_required);
    } else {
      jQuery('#btn-statutory-nature-submit').focus().click();
    }
  }
});
$('#btn-statutory-nature-submit').click(function () {
  clearMessage();
  var statutoryNatureIdVal = $('#statutory-nature-id').val();
  var statutoryNatureNameVal = $('#statutory-nature-name').val().trim();
  var countryIdVal = $('#country-id').val();
  var countryNameVal = $('#country-name').val().trim();
  var checkLength = statutoryNatureValidate();
  if (checkLength) {
    if (countryNameVal == '') {
      displayMessage(message.country_required);
    }
    if (statutoryNatureNameVal == '') {
      displayMessage(message.statutorynature_required);
    } else if (statutoryNatureIdVal == '') {

      function onSuccess(data) {
        $('#statutory-nature-add').hide();
        $('#statutory-nature-view').show();
        $('#search-statutory-nature-name').val('');
        initialize();
      }
      function onFailure(error) {
        if (error == 'StatutoryNatureNameAlreadyExists') {
          displayMessage(message.statutoryname_exists);
        } else {
          displayMessage(error);
        }
      }
      statutoryNatureDetail = [
        statutoryNatureNameVal,
        parseInt(countryIdVal)
      ];

      statutoryNatureDetailDict = mirror.getSaveStatutoryNatureDict(statutoryNatureDetail);

      mirror.saveStatutoryNature(statutoryNatureDetailDict, function (error, response) {
        if (error == null) {
          alert(message.statutoty_nature_save_success);
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    } else {
      function onSuccess(data) {
        $('#statutory-nature-add').hide();
        $('#statutory-nature-view').show();
        $('#search-statutory-nature-name').val('');
        initialize();
        clearMessage();
      }
      function onFailure(error) {
        if (error == 'InvalidStatutoryNatureId') {
          displayMessage(message.stat_nature_invalid);
        } else if (error == 'StatutoryNatureNameAlreadyExists') {
          displayMessage(message.statutoryname_exists);
        } else {
          displayMessage(error);
        }
      }
      statutoryNatureDetail = [
        parseInt(statutoryNatureIdVal),
        statutoryNatureNameVal,
        parseInt(countryIdVal)
      ];

      statutoryNatureDetailDict = mirror.getUpdateStatutoryNatureDict(statutoryNatureDetail);

      mirror.updateStatutoryNature(statutoryNatureDetailDict, function (error, response) {
        if (error == null) {
          alert(message.statutoty_nature_update_success);
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
  }
});
function statNature_edit(statNatureId, statNatureName, countryId) {
  clearMessage();
  $('#statutory-nature-add').show();
  $('#statutory-nature-view').hide();
  $('#statutory-nature-name').val(statNatureName.replace(/##/gi, '"'));
  $('#statutory-nature-id').val(statNatureId);
  $('#country-id').val(countryId);
  $('#statutory-nature-name').focus();
  ////load country name
  for(var i in countriesList)
  {
    if(countriesList[i].country_id == countryId)
    {
        $('#country-id').val(countryId);
        $('#country-name').val(countriesList[i].country_name);
        break;
      }
  }

}
function statNature_active(statNatureId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function success(status, data) {
            if (status == null)
            {
              if (isActive) {
                alert(message.statutoty_nature_status_active_success);
              }
              else
              {
                alert(message.statutoty_nature_status_deactive_success);
              }
            }
          $('#search-statutory-nature-name').val('');
          initialize();
        }
        function failure(error) {
          if (error == 'TransactionExists') {
            custom_alert(message.trasaction_exists);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeStatutoryNatureStatus(parseInt(statNatureId), isActive, success, failure)
          /*{if (error == null) {
            if (isActive) {
              alert(message.statutoty_nature_status_active_success);
            }
            else
            {
              alert(message.statutoty_nature_status_deactive_success);
            }
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });*/
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
}

//load country list in autocomplete text box
$('#country-name').keyup(function (e) {
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, function (val) {
    onCountrynameSuccess(val);
  });
});

//store the selected country name and id
function onCountrynameSuccess(val)
{
  $('#country-name').val(val[1]);
  $('#country-id').val(val[0]);
  $('#country-name').focus();
}

$('#search-statutory-nature-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.statutory-nature-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
});

$('#search-country-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.country-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
});
$(function () {
  initialize();
});
$('#statutory-nature-name').on('input', function (e) {
  this.value = isAlphabetic($(this));
});