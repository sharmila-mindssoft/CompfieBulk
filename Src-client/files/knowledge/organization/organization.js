var industriesList;
var countriesList;
var domainList;
var edit_mode = false;
var inactive_ctry = '';
var msg = message;
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

//button controls
var AddButton = $('#btn-orgn-add');
var CancelButton = $('#btn-orgn-cancel');
var SubmitButton = $('#btn-submit');

//table controls
var viewTable = $('.tbody-organization-list');
var AddSCreen = $('#organization-add');
var viewScreen = $('#organization-view');


// get industries list from api
function getIndustries() {
	function onSuccess(data) {
		industriesList = data.industries;
		domainList = data.domains;
		countriesList = data.countries;
		console.log("list:"+data)
		loadIndustryList(industriesList);
	}
	function onFailure(error) {
		custom_alert(error);
	}
	mirror.getIndustryList(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		} else {
		  onFailure(error);
		}
	});
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();
  d_name = FilterDomain.val().toLowerCase();
  o_name = FilterOrgn.val().toLowerCase();

  usr_status = $('.search-status-li.active').attr('value');

  searchList = []

  for(var i in industriesList){
    data = industriesList[i];

    data_c_name = data.country_name.toLowerCase();
    data_d_name = data.domain_name.toLowerCase();
    data_o_name = data.industry_name.toLowerCase();
    data_is_active = data.is_active;

    if (
      (~data_c_name.indexOf(c_name)) && (~data_d_name.indexOf(d_name)) &&
      (~data_o_name.indexOf(o_name)))
    {
      if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)){
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

  $.each(data, function (key, value) {
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
    $('.edit', clone).on('click', function () {
      displayEdit(country_id, domain_id, industryId, industryName);
    });

    if (isActive == true){
      statusmsg = message.deactive_message;
      $('.status').attr('title', 'Click Here to Deactivate');
      $('.status', clone).removeClass('fa-times text-danger');
      $('.status', clone).addClass('fa-check text-success');
    }
    else{
      statusmsg = message.active_message;
      $('.status').attr('title', 'Click Here to Activate');
      $('.status', clone).removeClass('fa-check text-success');
      $('.status', clone).addClass('fa-times text-danger');
    }
    $('.status', clone).on('click', function () {
      confirm_alert(statusmsg, function(isConfirm){
        if(isConfirm){
          changeStatus(industryId, passStatus);
        }
      });
    });

    viewTable.append(clone);
    j = j + 1;
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

// validation
function formValidation() {
  console.log("inside form")
  if (country_val.val().trim().length == 0) {
    displayMessage(msg.country_required);
    country_ac.focus();
    return false;
  }

  if (domain_val.val().trim().length == 0) {
    displayMessage(msg.domainname_required);
    domain_ac.focus();
    return false;
  }

  if (orgn_name.val().trim().length == 0) {
    displayMessage(msg.industryname_required);
    orgn_name.focus();
    return false;
  }
  else {
    validateMaxLength('organization_name', orgn_name.val(), "Organization Name");
  }
  return true;

}

function submitOrganization()
{
  var countryId = country_val.val();
  var countryName = country_ac.val().trim();
  var domainId = domain_val.val();
  var domainName = domain_ac.val().trim();
  var industryId = orgn_id.val();
  var industryName = orgn_name.val().trim();

  //validate controls
  var returnValidation = formValidation();
  console.log(returnValidation)

  if(returnValidation == true){
    console.log("save")
    //save organization
    if(industryId == '')
    {
      console.log("inside save")
      function onSuccess(response) {
        getIndustries();
        AddSCreen.hide();
        viewScreen.show();
      }
      function onFailure(error) {
        if (error == 'InvalidIndustryId') {
          displayMessage(msg.invalid_industryid);
        } else if (error == 'IndustryNameAlreadyExists') {
          displayMessage(msg.industryname_exists);
        } else {
          displayMessage(error);
        }
      }
      industryDetail = [
        parseInt(countryId),
        parseInt(domainId),
        industryName
      ];
      console.log("a:"+industryDetail)
      industryDetailDict = mirror.getSaveIndustryDict(industryDetail);
      mirror.saveIndustry(industryDetailDict, function (error, response) {
        if (error == null) {
          alert(msg.organization_save_success);
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
    else //update organization
    {
      function onSuccess(response) {
        getIndustries();
        AddSCreen.hide();
        viewScreen.show();
      }
      function onFailure(error) {
        if (error == 'IndustryNameAlreadyExists') {
          displayMessage(msg.industryname_exists);
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
      //alert(industryDetail);
      var industryDetailDict = mirror.getUpdateIndustryDict(industryDetail);

      mirror.updateIndustry(industryDetailDict, function (error, response) {
        if (error == null) {
          alert(msg.organization_update_success)
          onSuccess(response);
        } else {
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
    //alert("disp:"+countriesList[i].country_id);
    if(countriesList[i].country_id == countryId) {
      $('#countryid').val(countryId);
      $('#countryname').val(countriesList[i].country_name);
      if(countriesList[i].is_active == false)
        inactive_ctry = countryId;
      break;
    }
  }
}

function loadDomains(domainId)
{
  var j=0;
  for(j in domainList)
  {
    if(domainList[j].domain_id == domainId) {
      $('#domainid').val(domainList[j].domain_id);
      $('#domainname').val(domainList[j].domain_name);
      if(domainList[j].is_active == false)
      {
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
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(response) {
          getIndustries();
        }
        function onFailure(error) {
          if (error == 'TransactionExists') {
            custom_alert(message.trasaction_exists);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeIndustryStatus(industryId, isActive, function (error, response) {
          if (error == null) {
            if (isActive) {
              alert(message.organization_status_active_success);
            }
            else
            {
              alert(message.organization_status_deactive_success);
            }
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

//enable add button
function displayAddMode(){
  viewScreen.hide();
  AddSCreen.show();
  country_ac.val('');
  country_val.val('');
  domain_ac.val('');
  domain_val.val('');
  orgn_name.val('');
  country_ac.focus();
  inactive_ctry = '';
  inactive_domain = '';
  edit_mode = false;
}

//enable view button
function displayViewMode(){
  viewScreen.show();
  AddSCreen.hide();
  loadIndustryList(industriesList);
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
  orgn_name.on('input', function (e) {
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
    var condition_fields = ["is_active"];
    var condition_values = [true];
    var text_val = $(this).val();
    commonAutoComplete(
      e, AcDomain, domain_val, text_val,
      domainList, "domain_name", "domain_id", function (val) {
          onAutoCompleteSuccess(domain_ac, domain_val, val);
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
	    submitOrganization();
	});
  Search_status.change(function() {
	    processSearch();
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
