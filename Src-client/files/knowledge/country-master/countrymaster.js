
var counList;

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');
var CurrentPassword = $('#current-password');
var PasswordSubmitButton = $('#password-submit');

$('#btn-country-add').click(function () {
  $('#ctry-view').hide();
  $('#country-add').show();
  $('#country-name').val('');
  $('#country-id').val('');
  //displayMessage('');  // $("#country-name").focus();
                       // $('#country-name').select();
                       // $('#country-name').trigger('focus');
});
$('#btn-country-cancel').click(function () {
  $('#country-add').hide();
  $('#ctry-view').show();
  $('#search-country-name').val('');
  loadCountriesList(counList);
});
//get countries list from api
function initialize() {
  function onSuccess(data) {
    $('#search-country-name').val('');
    counList = data;
    loadCountriesList(data);
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getCountryList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//display cpuntry details in view page
function loadCountriesList(countriesList) {
  $('.tbody-countries-list').find('tr').remove();
  var sno = 0;
  $.each(countriesList, function (i, value) {
    var countries = countriesList[i];
    $.each(countries, function (j, value) {
      var countryId = countries[j].country_id;
      var countryName = countries[j].country_name;
      var isActive = countries[j].is_active;
      var passStatus = null;
      var classValue = null;

      var tableRow = $('#templates .table-countries-list .table-row');
      var clone = tableRow.clone();
      sno = sno + 1;
      $('.sno', clone).text(sno);
      $('.country-name', clone).text(countryName);

      //edit icon
      $('.edit').attr('title', 'Click Here to Edit');
      $('.edit', clone).addClass('fa-pencil text-primary');
      $('.edit', clone).on('click', function () {
        country_edit(countryId, countryName);
      });

      if (isActive == false){
        //$('.status').attr('title', 'Click Here to Deactivate');
        $('.status', clone).removeClass('fa-check text-success');
        $('.status', clone).addClass('fa-times text-danger');
      }
      else{
        //$('.status').attr('title', 'Click Here to Activate');
        $('.status', clone).removeClass('fa-times text-danger');
        $('.status', clone).addClass('fa-check text-success');
      }
      $('.status', clone).on('click', function (e) {
        showModalDialog(e, countryId, isActive);
      });

      $('.status').hover(function(){
        showTitle(this);
      });

      $('.tbody-countries-list').append(clone);
    });
  });
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
function showModalDialog(e, countryId, isActive){
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
            country_active(countryId, passStatus);
          }
        },
      });
      e.preventDefault();
    }
  });
}


//validate password
function validateAuthentication(){
  var password = CurrentPassword.val().trim();
  if (password.length == 0) {
    displayMessage(msg.password_required);
    CurrentPassword.focus();
    return false;
  }
  else {
    validateMaxLength('password', password, "Password");
  }
  mirror.verifyPassword(password, function(error, response) {
    if (error == null) {
      isAuthenticate = true;
      Custombox.close();
    }
    else {
      if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
      }
    }
  });
}

//length validation
function validateMaxLength(key_name, value, show_name) {
  console.log("inside length"+ show_name)
  e_n_msg = validateLength(key_name, value.trim())
  if (e_n_msg != true) {
    displayMessage(show_name + e_n_msg);
    return false;
  }
  return true;
}

$('#country-name').keypress(function (e) {
  var countryNameValue = $('#country-name').val();
  if (e.which == 13 && $(this).val() != '') {
    jQuery('#submit').focus().click();
  }
});
//save/update country details
$('#btn-submit').click(function () {
  var countryIdValue = $('#country-id').val();
  var countryNameValue = $('#country-name').val().trim();
  var checkLength = countryValidate();
  if (checkLength) {
    if (countryNameValue.length == 0) {
      displayMessage(message.country_required);
    } else {
      if (countryIdValue == '') {
        function onSuccess(response) {
          $('#country-add').hide();
          $('#ctry-view').show();
          $('#search-country-name').val('');
          displayMessage(message.save_success);
          initialize();
        }
        function onFailure(error) {
          if (error == 'CountryNameAlreadyExists') {
            displayMessage(message.countryname_exists);
          } else {
            displayMessage(error);
          }
        }
        mirror.saveCountry(countryNameValue, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      } else {
        function onSuccess(response) {
          $('#country-add').hide();
          $('#ctry-view').show();
          displayMessage(message.update_success);
          initialize();
        }
        function onFailure(error) {
          if (error == 'InvalidCountryId') {
            displayMessage(message.countryname_invalid);
          } else if (error == 'CountryNameAlreadyExists') {
            displayMessage(message.countryname_exists);
          } else {
            displayMessage(error);
          }
        }
        mirror.updateCountry(parseInt(countryIdValue), countryNameValue, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      }
    }
  }
});
//edit country
function country_edit(countryId, countryName) {
  $('#ctry-view').hide();
  $('#country-add').show();
  clearMessage();
  $('#country-name').val(countryName.replace(/##/gi, '"'));
  $('#country-id').val(countryId);
}
//activate/deactivate country
function country_active(countryId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        $('#country-id').val(countryId);
        function onSuccess(response) {
          initialize();
        }
        function onFailure(error) {
          if (error == 'TransactionExists') {
            custom_alert(message.trasaction_exists);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeCountryStatus(parseInt(countryId), isActive, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
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
//filter process
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

function processSearch(){
  usr_status = $('.search-status-li.active').attr('value');

  searchList = []

  for(var i in counList){
    data = counList[i];
    data_is_active = data.is_active;
    if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)){
        searchList.push(data);
    }
  }
  loadCountriesList(searchList);
}

//initialization
$(function () {
  initialize();
});
$('#country-name').on('input', function (e) {
  this.value = isAlphabetic($(this));
});
Search_status.change(function() {
    processSearch();
});
PasswordSubmitButton.click(function() {
  validateAuthentication();
});
