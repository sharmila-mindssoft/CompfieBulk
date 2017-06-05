var industriesList;
var countriesList;
var domainList;
var edit_mode = false;
var inactive_ctry = '';
var inactive_domain = '';

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterDomain = $('#search-domain-name');
var FilterOrgn = $('#search-organization-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

// auto complete - country
var country_val = $('#countryid');
var country_ac = $("#countryname");
var AcCountry = $('#ac-country');

// auto complete - domain
var domain_val = $('#domainid');
var domain_ac = $("#domainname");
var AcDomain = $('#ac-domain')

//input controls
var orgn_name = $('#organizationname');
var orgn_id = $('#organizationid');
var CurrentPassword = $('#current-password');

//button controls
var AddButton = $('#btn-orgn-add');
var CancelButton = $('#btn-orgn-cancel');
var SubmitButton = $('#btn-submit');
var PasswordSubmitButton = $('#password-submit');

//table controls
var viewTable = $('.tbody-organization-list');
var AddSCreen = $('#organization-add');
var viewScreen = $('#organization-view');

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

// get industries list from api
function getIndustries() {

	function onSuccess(data) {
		industriesList = data.industries;
		domainList = data.domains;
		countriesList = data.countries;
		loadIndustryList(industriesList);
	}
	function onFailure(error) {
		displayMessage(error);
	}
  displayLoader();
	mirror.getIndustryList(function (error, response) {
		if (error == null) {
		  onSuccess(response);
      hideLoader();
		} else {
		  onFailure(error);
      hideLoader();
		}
	});
}

function processSearch() {
    c_name = FilterCountry.val().toLowerCase();
    d_name = FilterDomain.val().toLowerCase();
    o_name = FilterOrgn.val().toLowerCase();

    usr_status = $('.search-status-li.active').attr('value');

    searchList = []

    for (var i in industriesList) {
        data = industriesList[i];

        data_c_name = data.country_name.toLowerCase();
        data_d_name = data.domain_name.toLowerCase();
        data_o_name = data.industry_name.toLowerCase();
        data_is_active = data.is_active;

        if (
            (~data_c_name.indexOf(c_name)) && (~data_d_name.indexOf(d_name)) &&
            (~data_o_name.indexOf(o_name))) {
            if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)) {
                searchList.push(data);
            }
        }
    }
    loadIndustryList(searchList);
}

//display industry list in view page
function loadIndustryList(data) {
  var j = 1;
  viewTable.find('tr').remove();
  if(data.length == 0){
    $('.tbody-organization-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-organization-list').append(clone4);
  }else{
    $.each(data, function (key, value) {
      statusmsg = "";
      var country_id = value.country_id;
      var country_name = value.country_name;
      var domain_id = value.domain_id;
      var domain_name = value.domain_name;
      var industryId = value.industry_id;
      var industryName = value.industry_name;
      var isActive = value.is_active;
      var passStatus = null;

      if (isActive == true) {
        passStatus = false;
      } else {
        passStatus = true;
      }

      var tableRow = $('#templates .table-orgn-master .table-row');
      var clone = tableRow.clone();
      $('.sno', clone).text(j);
      $('.country-name', clone).text(country_name);
      $('.domain-name', clone).text(domain_name);
      $('.organization-name', clone).text(industryName);

      //edit icon
      $('.edit').attr('title', 'Click Here to Edit');
      $('.edit', clone).addClass('fa-pencil text-primary');
      $('.edit', clone).attr("onClick", "displayEdit(" + country_id + ", " + domain_id + "," + industryId + ",'" + industryName + "')");

      if (value.is_active == false){
        $('.status', clone).removeClass('fa-check text-success');
        $('.status', clone).addClass('fa-times text-danger');
        $('.status').attr('title', 'Click Here to Activate');
      }
      else{
        $('.status', clone).removeClass('fa-times text-danger');
        $('.status', clone).addClass('fa-check text-success');
        $('.status').attr('title', 'Click Here to Deactivate');
      }
      $('.status', clone).attr("onClick", "showModalDialog(" + industryId + "," + isActive + ")");

      viewTable.append(clone);
      j = j + 1;
    });
  }
  $('[data-toggle="tooltip"]').tooltip();
}

//Status Title
function showTitle(e) {
    if (e.className == "fa c-pointer status fa-times text-danger") {
        e.title = 'Click Here to Activate';
    } else if (e.className == "fa c-pointer status fa-check text-success") {
        e.title = 'Click Here to Deactivate';
    }
}

//open password dialog
function showModalDialog(industryId, isActive) {
    var passStatus = null;
    if (isActive == true) {
        passStatus = false;
        statusmsg = message.deactive_message;
    } else {
        passStatus = true;
        statusmsg = message.active_message;
    }
    CurrentPassword.val('');
    confirm_alert(statusmsg, function(isConfirm) {
        if (isConfirm) {
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete: function() {
                    CurrentPassword.focus();
                    isAuthenticate = false;
                },
                close: function() {
                    if (isAuthenticate) {
                        changeStatus(industryId, isActive);
                    }
                },
            });
            //e.preventDefault();
        }
    });
}


//validate password
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
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

// validation
function formValidation() {

  if (country_val.val().trim().length == 0) {
    displayMessage(message.country_required);
    country_ac.focus();
    return false;
  }

  if (domain_val.val().trim().length == 0) {
    displayMessage(message.domainname_required);
    domain_ac.focus();
    return false;
  }

  if (orgn_name.val().trim().length == 0) {
    displayMessage(message.industryname_required);
    orgn_name.focus();
    return false;
  } else if(validateMaxLength("organization_name", orgn_name.val(), "Organization Name") == false) {
      return false;
  }

  return true;
}

function submitOrganization() {
    var countryId = country_val.val();
    var countryName = country_ac.val().trim();
    var domainId = domain_val.val();
    var domainName = domain_ac.val().trim();
    var industryId = orgn_id.val();
    var industryName = orgn_name.val().trim();

    //validate controls
    var returnValidation = formValidation();
    console.log(returnValidation)

    if (returnValidation == true) {
        console.log("save")
            //save organization
        if (industryId == '') {
            console.log("inside save")

            function onSuccess(response) {
                getIndustries();
                AddSCreen.hide();
                viewScreen.show();
                hideLoader();
            }

            function onFailure(error) {
                if (error == 'InvalidIndustryId') {
                    displayMessage(message.invalid_industryid);
                } else if (error == 'IndustryNameAlreadyExists') {
                    displayMessage(message.industryname_exists);
                } else {
                    displayMessage(error);
                }
            }
            industryDetail = [
                parseInt(countryId),
                parseInt(domainId),
                industryName
            ];
            console.log("a:" + industryDetail)
            industryDetailDict = mirror.getSaveIndustryDict(industryDetail);
            displayLoader();
            mirror.saveIndustry(industryDetailDict, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.organization_save_success);
                    onSuccess(response);
                } else {
                    hideLoader();
                    onFailure(error);
                }
            });
        } else //update organization
        {
            function onSuccess(response) {
                Search_status.removeClass();
                Search_status.addClass('fa');
                Search_status.text('All');
                getIndustries();
                AddSCreen.hide();
                viewScreen.show();
                hideLoader();
            }

            function onFailure(error) {
                if (error == 'IndustryNameAlreadyExists') {
                    displayMessage(message.industryname_exists);
                } else {
                    displayMessage(error);
                }
            }
            industryDetail = [
                parseInt(countryId),
                parseInt(domainId),
                parseInt(industryId),
                industryName
            ];
            var industryDetailDict = mirror.getUpdateIndustryDict(industryDetail);
            displayLoader();
            mirror.updateIndustry(industryDetailDict, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.organization_update_success)
                    onSuccess(response);
                } else {
                  hideLoader();
                  onFailure(error);
                }
            });
        }
    }
}

function loadCountries(countryId) {
    var i = 0;
    for (i in countriesList) {
        //alert("disp:"+countriesList[i].country_id);
        if (countriesList[i].country_id == countryId) {
            $('#countryid').val(countryId);
            $('#countryname').val(countriesList[i].country_name);
            if (countriesList[i].is_active == false)
                inactive_ctry = countryId;
            break;
        }
    }
}

function loadDomains(domainId) {
    var j = 0;
    for (j in domainList) {
        if (domainList[j].domain_id == domainId) {
            $('#domainid').val(domainList[j].domain_id);
            $('#domainname').val(domainList[j].domain_name);
            if (domainList[j].is_active == false) {
                inactive_domain = domainId;
            }
            break;
        }
    }
}
// edit industry master
function displayEdit(countryId, domainId, industryId, industryName) {
    viewScreen.hide();
    AddSCreen.show();
    edit_mode = true;

    //load countries
    loadCountries(countryId);

    //load domain name
    loadDomains(domainId);

    orgn_name.val(industryName.replace(/##/gi, '"'));
    orgn_id.val(industryId);
}

// activate / deactivate industry master
function changeStatus(industryId, isActive) {
    if (isActive == true) {
        isActive = false;
    } else {
        isActive = true;
    }
    displayLoader();
    mirror.changeIndustryStatus(industryId, isActive, function(error, response) {
        if (error == null) {
            if (isActive) {
                displaySuccessMessage(message.organization_status_active_success);
            } else {
                displaySuccessMessage(message.organization_status_deactive_success);
            }
            getIndustries();
            hideLoader();
        } else {
            hideLoader();
            displayMessage(error);
        }
    });
}

//enable add button
function displayAddMode() {
    viewScreen.hide();
    AddSCreen.show();
    country_ac.val('');
    country_val.val('');
    domain_ac.val('');
    domain_val.val('');
    orgn_name.val('');
    orgn_id.val('');
    country_ac.focus();
    inactive_ctry = '';
    inactive_domain = '';
    edit_mode = false;
}

//enable view button
function displayViewMode() {
    viewScreen.show();
    AddSCreen.hide();
    FilterCountry.val('');
    FilterDomain.val('');
    FilterOrgn.val('');
    var currentClass = $('.search-status-li.active').attr('class');
    Search_status.removeClass();
    Search_status.addClass('fa');
    Search_status.text('All');
    loadIndustryList(industriesList);
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

// key press events
function keyError() {
    orgn_name.on('input', function(e) {
        this.value = isCommon_Name($(this));
    });
}
//render controls
function renderControls(){
    getIndustries();

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

  domain_ac.keyup(function(e){
    var text_val = $(this).val();
    var domain_list = [];
    var c_ids = null;
    var check_val = false;
    if(country_val.val() != ''){
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
        submitOrganization();
    });
  Search_status.change(function() {
        processSearch();
    });
  PasswordSubmitButton.click(function() {
    validateAuthentication();
  });
}


//loading controls
function initialize() {
    renderControls();
    keyError();

}

//initialization

$(document).ready(function () {
  initialize();
});
