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

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

$('#btn-country-add').click(function () {
  $('#ctry-view').hide();
  $('#country-add').show();
  $('#country-name').val('');
  $('#country-id').val('');
  $('#country-name').focus();
});
$('#btn-country-cancel').click(function () {
  $('#country-add').hide();
  $('#ctry-view').show();
  $('#search-country-name').val('');
  // loadCountriesList(counList);
  Search_status.removeClass();
  Search_status.addClass('fa');
  Search_status.text('All');
  loadCountriesList(counList);
});
//get countries list from api
function initialize() {
  function onSuccess(data) {
    Search_status.removeClass();
    Search_status.addClass('fa');
    Search_status.text('All');
    $('#search-country-name').val('');
    counList = data;
    onLoadList(data);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error)
  }
  displayLoader();
  mirror.getCountryList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}
function onLoadList(data){
  counList = [];
  if(data.countries.length == 0){
    $('.tbody-countries-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-countries-list').append(clone4);
  }else{
    $.each(data, function (i, value) {
    var country = data[i];
    $.each(country, function (j, value) {
        counList.push(country[j]);
      });
    });
    loadCountriesList(counList);
  }

}
//display cpuntry details in view page
function loadCountriesList(countriesList) {
  $('.tbody-countries-list').find('tr').remove();
  var sno = 0;
   if(countriesList.length == 0){
    $('.tbody-countries-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-countries-list').append(clone4);
  }else{
    $.each(countriesList, function (j, value) {
      var countryId = countriesList[j].country_id;
      var countryName = countriesList[j].country_name;
      var isActive = countriesList[j].is_active;
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
      $('.edit', clone).attr("onClick", "country_edit(" + countryId + ",'" + countryName + "')");

      if (isActive == false){
        $('.status', clone).removeClass('fa-check text-success');
        $('.status', clone).addClass('fa-times text-danger');
        $('.status').attr('title', 'Click Here to Activate');
      }
      else{
        $('.status', clone).removeClass('fa-times text-danger');
        $('.status', clone).addClass('fa-check text-success');
        $('.status').attr('title', 'Click Here to Deactivate');
      }
      $('.status', clone).attr("onClick", "showModalDialog(" + countryId + "," + isActive + ")");
      $('.tbody-countries-list').append(clone);
    });
  }
  $('[data-toggle="tooltip"]').tooltip();
}

//Status Title
function showTitle(e){
  console.log(e.target.className)
  if(e.target.className == "fa c-pointer status fa-times text-danger"){
    e.target.title = 'Click Here to Activate';
  }
  else if(e.target.className == "fa c-pointer status fa-check text-success")
  {
    e.target.title = 'Click Here to Deactivate';
  }
}

//open password dialog
function showModalDialog(countryId, isActive){
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
    } else {
      hideLoader();
      if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
      }
    }
  });
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
  var checkLength = validateMaxLength('countryname', countryNameValue, "Country Name");
  if (checkLength) {
    if (countryNameValue.length == 0) {
      displayMessage(message.country_required);
    } else if(countryNameValue.indexOf("..") >= 0) {
      displayMessage(message.countryname_invalid);
    } else if(countryNameValue.indexOf("--") >= 0) {
      displayMessage(message.countryname_invalid);
    } else {
      if (countryIdValue == '') {
        function onSuccess(response) {
          $('#country-add').hide();
          $('#ctry-view').show();
          $('#search-country-name').val('');
          displaySuccessMessage(message.country_save_success);
          initialize();
        }
        function onFailure(error) {
          if (error == 'CountryNameAlreadyExists') {
            displayMessage(message.countryname_exists);
          } else {
            displayMessage(error);
          }
        }
        displayLoader();
        mirror.saveCountry(countryNameValue, function (error, response) {
          if (error == null) {
            onSuccess(response);
            hideLoader();
          } else {
            onFailure(error);
            hideLoader();
          }
        });
      } else {
        function onSuccess(response) {
          $('#country-add').hide();
          $('#ctry-view').show();
          displaySuccessMessage(message.country_update_success);
          initialize();
          hideLoader();
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
        displayLoader();
        mirror.updateCountry(parseInt(countryIdValue), countryNameValue, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            hideLoader();
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
  displayLoader();
  mirror.changeCountryStatus(parseInt(countryId), isActive, function (error, response) {
    if (error == null) {
      if (isActive == 1)
        displaySuccessMessage(message.country_active);
      else
        displaySuccessMessage(message.country_deactive);
      initialize();
      hideLoader();
    } else {
      hideLoader();
      displayMessage(error);
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

  $.each(counList, function (j, value) {
    data = counList[j];
    data_is_active = counList[j].is_active;
    if ((usr_status == 'all') || (Boolean(parseInt(usr_status)) == data_is_active)){
      searchList.push(data);
    }
  });

  loadCountriesList(searchList);
}

function renderSearch() {
  // body...
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
}



$(function () {
  initialize();
  renderSearch();
});
$('#country-name').on('input', function (e) {
  this.value = isCommon_Name($(this));
});
Search_status.change(function() {
    processSearch();
});
PasswordSubmitButton.click(function() {
  validateAuthentication();
});
