var statutorynatureList;
var countriesList;
var edit_mode = false;
var inactive_ctry = '';

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterStatutoryNature = $('#search-statutory-nature-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

// auto complete - country
var country_val = $('#countryid');
var country_ac = $("#countryname");
var AcCountry = $('#ac-country');

//input controls
var statutory_nature_name = $('#statutorynaturename');
var statutory_nature_id = $('#statutorynatureid');
var CurrentPassword = $('#current-password');

//button controls
var AddButton = $('#btn-statutory-nature-add');
var CancelButton = $('#btn-statutory-nature-cancel');
var SubmitButton = $('#btn-submit');
var PasswordSubmitButton = $('#password-submit');

//table controls
var viewTable = $('.tbody-statutory-nature-list');
var AddSCreen = $('#statutory-nature-add');
var viewScreen = $('#statutory-nature-view');

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

// get statutory nature list from api
function getStatutorynatures() {
	function onSuccess(data) {
		  countriesList = data.countries;
    	statutorynatureList = data.statutory_natures;
		  loadStatNatureData(statutorynatureList);
      hideLoader();
	}
	function onFailure(error) {
		displayMessage(error);
	}
  displayLoader();
	mirror.getStatutoryNatureList(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		} else {
      hideLoader();
		  onFailure(error);
		}
	});
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();
  s_n_name = FilterStatutoryNature.val().toLowerCase();

  nature_status = $('.search-status-li.active').attr('value');

  searchList = []

  for(var i in statutorynatureList){
    data = statutorynatureList[i];

    data_c_name = data.country_name.toLowerCase();
    data_s_n_name = data.statutory_nature_name.toLowerCase();
    data_is_active = data.is_active;

    if ((~data_c_name.indexOf(c_name)) && (~data_s_n_name.indexOf(s_n_name)))
    {
      if ((nature_status == 'all' || Boolean(parseInt(nature_status)) == data.is_active)){
        searchList.push(data);
      }
    }
  }
  loadStatNatureData(searchList);
}

//display statutory nature list in view page
function loadStatNatureData(data) {
  var j = 1;
  viewTable.find('tr').remove();
  if(data.length == 0){
    viewTable.empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    viewTable.append(clone4);
  }else{
    $.each(data, function (key, value) {
      var countryId = value.country_id;
      var countryName = value.country_name;
      var statNatureId = value.statutory_nature_id;
      var statNatureName = value.statutory_nature_name;
      var isActive = value.is_active;
      var passStatus = null;

      if (isActive == true) {
        passStatus = false;
      } else {
        passStatus = true;
      }

      var tableRow = $('#templates .table-statutory-nature-master .table-row');
      var clone = tableRow.clone();
      $('.sno', clone).text(j);
      $('.country-name', clone).text(countryName);
      $('.statutory-nature-name', clone).text(statNatureName);

      //edit icon
      $('.edit').attr('title', 'Click Here to Edit');
      $('.edit', clone).addClass('fa-pencil text-primary');
      $('.edit', clone).attr("onClick", "statNature_edit(" + statNatureId + ",'" + statNatureName + "'," + countryId + ")");
      if (isActive == true){
        $('.status', clone).removeClass('fa-times text-danger');
        $('.status', clone).addClass('fa-check text-success');
        $('.status').attr('title', 'Click Here to Deactivate');
      }
      else{
        console.log(isActive)

        $('.status', clone).removeClass('fa-check text-success');
        $('.status', clone).addClass('fa-times text-danger');
        $('.status').attr('title', 'Click Here to Activate');
      }
      $('.status', clone).attr("onClick", "showModalDialog(" + statNatureId + "," + isActive + ")");
      viewTable.append(clone);
      j = j + 1;
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
function showModalDialog(e, statNatureId, isActive){
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
            statNature_active(statNatureId, passStatus);
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
    displayMessage(message.password_required);
    CurrentPassword.focus();
    return false;
  }
  else if(validateMaxLength('password', password, "Password") == false) {
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

// validation
function formValidation() {
  if (country_val.val().trim().length == 0) {
    displayMessage(message.country_required);
    country_ac.focus();
    return false;
  }

  if (statutory_nature_name.val().trim().length == 0) {
    displayMessage(message.statutorynature_required);
    statutory_nature_name.focus();
    return false;
  }
  else if (validateMaxLength('statutory_nature_name', statutory_nature_name.val(), "Statutory Nature Name") == false){
    return false;
  }
  return true;
}

function submitStatutoryNature()
{
	var countryId = country_val.val();
	var countryName = country_ac.val().trim();
	var statutorynatureId = statutory_nature_id.val();
	var statutorynatureName = statutory_nature_name.val().trim();

	//validate controls
	var returnValidation = formValidation();

	if(returnValidation == true){
		//save statutory nature
		if(statutorynatureId == '')
		{
			function onSuccess(response) {
				getStatutorynatures();
				AddSCreen.hide();
				viewScreen.show();
        hideLoader();
			}
			function onFailure(error) {
				if (error == 'StatutoryNatureNameAlreadyExists') {
					displayMessage(message.statutoty_nature_name_exists);
				} else {
					displayMessage(error);
				}
			}
			statutoryNatureDetail = [
				statutorynatureName,
				parseInt(countryId)
			];
			statutoryNatureDetailDict = mirror.getSaveStatutoryNatureDict(statutoryNatureDetail);
      displayLoader();
			mirror.saveStatutoryNature(statutoryNatureDetailDict, function (error, response) {
				if (error == null) {
					displaySuccessMessage(message.statutoty_nature_save_success);
					onSuccess(response);
				} else {
          hideLoader();
					onFailure(error);
				}
			});
		}
		else //update organization
		{
			function onSuccess(response) {
				getStatutorynatures();
				AddSCreen.hide();
				viewScreen.show();
        hideLoader();
			}
			function onFailure(error) {
				if (error == 'StatutoryNatureNameAlreadyExists') {
					displayMessage(message.statutoty_nature_name_exists);
				} else {
					displayMessage(error);
				}
			}
			statutoryNatureDetail = [
				parseInt(statutorynatureId),
				statutorynatureName,
				parseInt(countryId)
			];
			statutoryNatureDetailDict = mirror.getUpdateStatutoryNatureDict(statutoryNatureDetail);
      displayLoader();
    	mirror.updateStatutoryNature(statutoryNatureDetailDict, function (error, response) {
				if (error == null) {
					displaySuccessMessage(message.statutoty_nature_update_success)
					onSuccess(response);
				} else {
          hideLoader();
					onFailure(error);
				}
			});
		}
	}
}

function loadCountries(countryId)
{
	var i=0;
	for(i in countriesList)
	{
		if(countriesList[i].country_id == countryId)
		{
			$('#countryid').val(countryId);
			$('#countryname').val(countriesList[i].country_name);
			if(countriesList[i].is_active == false)
				inactive_ctry = countryId;
				break;
		}
	}
}

// edit statutory nature master
function statNature_edit(statNatureId, statNatureName, countryId) {
  viewScreen.hide();
  AddSCreen.show();
  edit_mode = true;

  //load countries
  loadCountries(countryId);

  statutory_nature_name.val(statNatureName.replace(/##/gi, '"'));
  statutory_nature_id.val(statNatureId);
}

// activate / deactivate industry master
function statNature_active(statNatureId, isActive) {
  displayLoader();
	mirror.changeStatutoryNatureStatus(parseInt(statNatureId), isActive, function (error, response) {
    if (error == null) {
      hideLoader();
      if (isActive) {
        displaySuccessMessage(message.statutoty_nature_status_active_success);
      }
      else
      {
        displaySuccessMessage(message.statutoty_nature_status_deactive_success);
      }
      getStatutorynatures();
      //onSuccess(response);
    } else {
      hideLoader();
      displayMessage(error);
    }
  });
}

//enable add button
function displayAddMode(){
  viewScreen.hide();
  AddSCreen.show();
  country_ac.val('');
  country_val.val('');
  statutory_nature_name.val('');
  statutory_nature_id.val('');
  country_ac.focus();
  inactive_ctry = '';
  edit_mode = false;
}

//enable view button
function displayViewMode(){
  viewScreen.show();
  AddSCreen.hide();
  FilterCountry.val('');
  FilterStatutoryNature.val('');
  var currentClass = $('.search-status-li.active').attr('class');
  Search_status.removeClass();
  Search_status.addClass('fa');
  Search_status.text('All');
  loadStatNatureData(statutorynatureList);
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

// key press events
function keyError()
{
  statutory_nature_name.on('input', function (e) {
    this.value = isCommon_Name($(this));
  });
}
//render controls
function renderControls(){
	getStatutorynatures();

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


	FilterBox.keyup(function() {
	    processSearch();
	});
  CancelButton.click(function() {
	    displayViewMode();
	});
  AddButton.click(function() {
	    displayAddMode();
	});
  SubmitButton.click(function() {
	    submitStatutoryNature();
	});
  Search_status.change(function() {
	    processSearch();
	});
  PasswordSubmitButton.click(function() {
    validateAuthentication();
  });
}


//loading controls
function initialize()
{
	renderControls();
  	keyError();
}

//initialization
$(document).ready(function () {
  initialize();
});
