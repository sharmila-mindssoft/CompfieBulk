var assigneeWiseComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList;
var unitsList;
var assigneesList;

var totalRecord;
var sno = 0;
var fromCount = 0;
var perPage = 0;
var showFrom = 0;
var showTo = 0;
var cPage = 1;

var country = null;
var domain = null;
var businessgroup = null;
var legalentity = null;
var division = null;
var unit = null;
var assignee = null;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//get reports filter data from api
function getClientReportFilters() {
  function onSuccess(data) {
    countriesList = data.countries;
    domainsList = data.domains;
    businessGroupsList = data.business_groups;
    legalEntitiesList = data.legal_entities;
    divisionsList = data.divisions;
    unitsList = data.units;
    assigneesList = data.users;
    loadCountries(countriesList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getClientReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

function loadCompliances(complianceList) {

    $.each(complianceList, function (i, val) {
    var list = complianceList[i];
    var list_unit = val.user_wise_compliance;
    var bg = '-';
    if (list.business_group_name != null)
      bg = list.business_group_name;
    var dv = '-';
    if (list.division_name != null)
      dv = list.division_name;
    var le = list.legal_entity_name;
    
    var tableRow = $('#assignee-list-templates .table-assignee-list .table-row-assignee-list');
    var clone = tableRow.clone();
    
    $('.tbl_businessgroup', clone).text(bg);
    $('.tbl_division', clone).text(dv);
    $('.tbl_legalentity', clone).text(le);
    $('.tbody-assignee').append(clone);
    var tableRow1 = $('#assignee-head-templates .table-assignee-head .table-row-assignee-head');
    var clone1 = tableRow1.clone();
    $('.tbody-assignee').append(clone1);
    
    $.each(list_unit, function (i1, val1) {
        var assignee_ = val1.assignee;
        var concurrence = val1.concurrence_person;
        var approval_ = val1.approval_person;
        if (concurrence == null)
          concurrence = 'Nil';
        if (lastAssignee != assignee_ || lastConcurrence != concurrence || lastApproval != approval_) {
          var tableRow2 = $('#assignee-name-templates .table-assignee-name .table-row-assignee-name');
          var clone2 = tableRow2.clone();
          $('.tbl_assigneeheading', clone2).html('Assignee: ' + assignee_);
          $('.tbl_concurrenceheading', clone2).html('concurrence: ' + concurrence);
          $('.tbl_approvalheading', clone2).html('Approval: ' + approval_);
          $('.tbody-assignee').append(clone2);
        }
        var compliances = val1.compliances;
        $.each(compliances, function (i2, data) {
          var triggerdate = '';
          var statutorydate = '';
          for (j = 0; j < data.statutory_dates.length; j++) {
            var sDay = '';
            if (data.statutory_dates[j].statutory_date != null)
              sDay = data.statutory_dates[j].statutory_date;
            var sMonth = '';
            if (data.statutory_dates[j].statutory_month != null)
              sMonth = data.statutory_dates[j].statutory_month;
            var tDays = '';
            if (data.statutory_dates[j].trigger_before_days != null)
              tDays = data.statutory_dates[j].trigger_before_days;
            if (sMonth != '')
              sMonth = getMonth_IntegettoString(sMonth);
            triggerdate += tDays + ' Day(s), ';
            statutorydate += sMonth + ' ' + sDay + ', ';
          }
          if (data.statutory_dates.length <= 1) {
            statutorydate = '';
          }
          var summary = data.summary;
          if (statutorydate.trim() != '') {
            statutorydate = statutorydate.replace(/,\s*$/, '');
          }
          if (triggerdate.trim() != '') {
            triggerdate = triggerdate.replace(/,\s*$/, '');
          }
          if (summary != null) {
            if (statutorydate.trim() != '') {
              statutorydate = summary + ' (' + statutorydate + ')';
            } else {
              statutorydate = summary;
            }
          }

          var tableRow3 = $('#assignee-content-templates .table-assignee-content .table-row-assignee-content');
          var clone3 = tableRow3.clone();
          var cDescription = data.description;
          $('.tbl_sno', clone3).text(sno + 1);
          $('.tipso_style', clone3).attr('title', cDescription);
          $('.tbl_compliance', clone3).text(data.compliance_name);
          $('.tbl_unit', clone3).text(data.unit_address);
          $('.tbl_frequency', clone3).text(data.compliance_frequency);
          $('.tbl_statutorydate', clone3).text(statutorydate);
          $('.tbl_triggerbefore', clone3).text(triggerdate);
          var dDays = '-';
          if (data.due_date != null)
            dDays = data.due_date;
          $('.tbl_duedate', clone3).text(dDays);
          var vDays = '-';
          if (data.validity_date != null)
            vDays = data.validity_date;
          $('.tbl_validitydate', clone3).text(vDays);
          $('.tbody-assignee').append(clone3);
          sno++;
        });
    });
  });
}

//pagination process
function paginationLoad(page) {
  displayLoader();
  sno = (page - 1 ) * perPage;
  fromCount = sno;
  clearMessage();
  function onSuccess(data) {
    assigneeWiseComplianceList = data.compliance_list;

    showFrom = sno + 1;
    showTo = sno + perPage;
    if(showTo > totalRecord) showTo = totalRecord;
    $('.compliance_count').text('Showing ' + showFrom + ' to ' + showTo + ' of ' + totalRecord + ' entries');
    $('.tbody-assignee').find('tr').remove();

    loadCompliances(assigneeWiseComplianceList);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getAssigneewisecomplianceReport(
    parseInt(country), parseInt(domain), parseInt(businessgroup),
    parseInt(legalentity), parseInt(division), parseInt(unit),
    parseInt(assignee), fromCount, perPage,
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    });
};

function createPageView(perPage){
  $('#pagination-rpt').empty();
  $('#pagination-rpt').removeData('twbs-pagination');
  $('#pagination-rpt').unbind('page');
  $('#pagination-rpt').twbsPagination({
    totalPages: Math.ceil(totalRecord / perPage),
    visiblePages: visiblePageCount,
    onPageClick: function (event, page) {
        cPage = parseInt(page);
        paginationLoad(cPage);
        //if(page != 1) paginationLoad(cPage);
    }
  });
}

$('#items_per_page').on('change', function (e) {
  perPage = parseInt($(this).val());
  createPageView(perPage);
});

//get report data from api
$('#submit').click(function () {
  displayLoader();
  country = $('#country').val();
  domain = $('#domain').val();
  businessgroup = null;
  legalentity = null;
  division = null;
  unit = null;
  assignee = null;
  perPage = parseInt($('#items_per_page').val());
  if ($('#businessgroup').val() != '')
    businessgroup = $('#businessgroup').val();
  if ($('#legalentity').val() != '')
    legalentity = $('#legalentity').val();
  if ($('#division').val() != '')
    division = $('#division').val();
  if ($('#unit').val() != '')
    unit = $('#unit').val();
  if ($('#assignee').val() != '')
    assignee = $('#assignee').val();
  $('.tbody-assignee').find('tbody').remove();
  $('.compliance_count').text('');
  lastAssignee = '';
  lastConcurrence = '';
  lastApproval = '';
  lastBG = '';
  lastLE = '';
  lastDv = '';
  sno = 0;
  fromCount = 0;
  clearMessage();
  if (country.length == 0) {
    displayMessage(message.country_required);
    $('.grid-table-rpt').hide();
    hideLoader();
  } else if (domain.length == 0) {
    displayMessage(message.domain_required);
    $('.grid-table-rpt').hide();
    hideLoader();
  } else {
    function onSuccess(data) {

      $('.grid-table-rpt').show();
      $('.pagination-view').show();
      assigneeWiseComplianceList = data.compliance_list;
      totalRecord = data.total_count;

      if (totalRecord == 0) {
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Compliance Found');
        $('.tbody-unit').append(clone4);
        $('.pagination-view').hide();
      } else {
        createPageView(perPage);
        $('.pagination-view').show();
      }
      hideLoader();
    }
    function onFailure(error) {
      displayMessage(error);
      hideLoader();
    }
    client_mirror.getAssigneewisecomplianceReport(
      parseInt(country), parseInt(domain), parseInt(businessgroup),
      parseInt(legalentity), parseInt(division), parseInt(unit),
      parseInt(assignee), fromCount, perPage,
      function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
    });
  }
});
//Autocomplete Script Starts
//load country list
function loadCountries(countriesList) {
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function (key, values) {
    var countryId = countriesList[key].country_id;
    var countryName = countriesList[key].country_name;
    $('#country').append($('<option value="' + countryId + '">' + countryName + '</option>'));
  });
}
//retrive domain autocomplete value
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domain').val(val[0]);
  $('#domainval').focus();
}
//load domain list in autocomplete textbox  
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, callback, flag = true);
});
//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val) {
  $('#businessgroupval').val(val[1]);
  $('#businessgroup').val(val[0]);
  $('#businessgroupval').focus();
}
//load businessgroup form list in autocomplete text box  
$('#businessgroupval').keyup(function (e) {
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(e, textval, businessGroupsList, function (val) {
    onBusinessGroupSuccess(val);
  });
});
//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val) {
  $('#legalentityval').val(val[1]);
  $('#legalentity').val(val[0]);
  $('#legalentityval').focus();
}
//load legalentity form list in autocomplete text box  
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(e, textval, legalEntitiesList, function (val) {
    onLegalEntitySuccess(val);
  });
});
//retrive division form autocomplete value
function onDivisionSuccess(val) {
  $('#divisionval').val(val[1]);
  $('#division').val(val[0]);
  $('#divisionval').focus();
}
//load division form list in autocomplete text box  
$('#divisionval').keyup(function (e) {
  var textval = $(this).val();
  getClientDivisionAutocomplete(e, textval, divisionsList, function (val) {
    onDivisionSuccess(val);
  });
});
//retrive unit form autocomplete value
function onUnitSuccess(val) {
  $('#unitval').val(val[1]);
  $('#unit').val(val[0]);
  $('#unitval').focus();
}
//load unit  form list in autocomplete text box  
$('#unitval').keyup(function (e) {
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = $("#domain").val();
  getUnitAutocomplete(e, textval, unitsList, function (val) {
    onUnitSuccess(val);
  });
});
//retrive user autocomplete value
function onUserSuccess(val) {
  $('#assigneeval').val(val[1]);
  $('#assignee').val(val[0]);
  $('#assigneeval').focus();
}
//load user list in autocomplete text box  
$('#assigneeval').keyup(function (e) {
  var textval = $(this).val();
  getUserAutocomplete(e, textval, assigneesList, function (val) {
    onUserSuccess(val);
  });
});
//Autocomplete Script ends
//initialization
$(function () {
  $('.grid-table-rpt').hide();
  getClientReportFilters();
  $('#country').focus();
  loadItemsPerPage();
});
$(document).tooltip({
  position: {
    my: 'center bottom-20',
    at: 'center top',
    using: function (position, feedback) {
      $(this).css(position);
      $('<div>').addClass('arrow').addClass(feedback.vertical).addClass(feedback.horizontal).appendTo(this);
    }
  }
});