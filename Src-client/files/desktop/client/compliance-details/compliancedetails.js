var unitWiseComplianceList;
var countriesList;
var domainsList;
var actList;
var compliancesList;
var unitsList;
var usersList;

var on_current_page = 1;
var sno = 0;
var totalRecord;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//get compliance details filter from api
function getComplianceDetailsReportFilters() {
  function onSuccess(data) {
    countriesList = data.countries;
    domainsList = data.domains;
    actList = data.level_1_statutories;
    unitsList = data.units;
    usersList = data.users;
    compliancesList = data.compliances;
    loadCountries(countriesList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getComplianceDetailsReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}


function getValue(field_name){
   if (field_name == "country") {
        c_id = $('#country').val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }
    else if (field_name == "domain") {
        d_id = $('#domain').val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    }
    else if (field_name == "act") {
        act = $('#act').val().trim();
        if (act == '') {
            return null;
        }
        return act;
    }
    else if (field_name == "unit") {
        u_id = $('#unit').val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    }
    else if (field_name == "c_task") {
        ctask_id = $('#compliancetask').val().trim();
        if (ctask_id == '') {
            return null;
        }
        return parseInt(ctask_id);
    }
    else if (field_name == "user") {
        user_id = $('#assignee').val().trim();
        if (user_id == '') {
            return null;
        }
        return parseInt(user_id);
    }

    else if (field_name == "from_date") {
        f_date = $('#fromdate').val().trim();
        if (f_date == '') {
            return null;
        }
        return f_date;
    }

    else if (field_name == "to_date") {
        t_date = $('#todate').val().trim();
        if (t_date == '') {
            return null;
        }
        return t_date;
    }
    else if (field_name == "status") {
        status = $('#status').val().trim();
        if (status == '') {
            return null;
        }
        return status;
    }
};

function validateMandatory(){
    is_valid = true;
    if (getValue("country") == null) {
        displayMessage(message.country_required);
        is_valid = false;
    }
    else if (getValue("domain") == null) {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    else if (getValue("act") == null) {
        displayMessage(message.act_required);
        is_valid = false;
    }
    return is_valid;
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
function hidePagePan() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

function loadCompliances(complianceList){
  $('.tbody-unit').find('tbody').remove();
  var showFrom = sno + 1;
  var is_null = true;
  var country = $('#country').find('option:selected').text();
  var domain = $('#domainval').val();
  var act = $('#actval').val();
  var tableRow = $('#unit-list-templates .table-unit-list .table-row-unit-list');
  var clone = tableRow.clone();
  $('.tbl_country', clone).text(country);
  $('.tbl_domain', clone).text(domain);
  $('.tbl_act', clone).text(act);
  $('.tbody-unit').append(clone);
  var tableRow1 = $('#unit-head-templates .table-unit-head .table-row-unit-head');
  var clone1 = tableRow1.clone();
  $('.tbody-unit').append(clone1);
  $.each(complianceList, function (i, val) {
    console.log(val.unit_name)
    var tableRow2 = $('#unit-name-templates .table-unit-name .table-row-unit-name');
    var clone2 = tableRow2.clone();
    $('.heading', clone2).html(val.unit_name);
    $('.tbody-unit').append(clone2);

    var list_comp = val.compliances;
    $.each(list_comp, function (i1, val1) {
      is_null = false;
      var vDate = '-';
      if (val1.validity_date != null)
        vDate = val1.validity_date;
      var dueDate = '-';
      if (val1.due_date != null)
        dueDate = val1.due_date;
      var completionDate = '';
      if (val1.completion_date != null)
        completionDate = val1.completion_date;
      var tableRow3 = $('#unit-content-templates .table-unit-content .table-row-unit-content');
      var clone3 = tableRow3.clone();
      $('.tbl_sno', clone3).text(sno + 1);
      $('.tbl_compliance', clone3).html(val1.compliance_name);
      $('.tbl_assignee', clone3).text(val1.assignee);
      $('.tbl_duedate', clone3).text(dueDate);
      $('.tbl_completiondate', clone3).text(completionDate);
      $('.tbl_validitydate', clone3).text(vDate);
      $('.tbl_remarks', clone3).text(val1.remarks);
      if (val1.documents != null && val1.documents != '') {
        var documentsList = val1.documents;
        for (var i = 0; i < documentsList.length; i++) {
          $('.doc_link', clone3).attr('href', documentsList[i]);
          $('.doc_link', clone3).html('Download ' + (i + 1));
        }
      }
      $('.tbody-unit').append(clone3);
      sno++;

    });
  });
  hideLoader();
  if (is_null == true) {
    hidePagePan();
  }
  else {
    showPagePan(showFrom, sno, totalRecord);
  }
}

function createPageView(total_records) {
    perPage = parseInt($('#items_per_page').val());
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                
                on_current_page = cPage;
                fetchData(false);
            }
        }
    });
};

function fetchData (csv) {
    displayLoader();
    _country = getValue("country");
    _domain = getValue("domain");
    _act = getValue("act");
    _unit = getValue("unit");
    _compliance_task = getValue("c_task");
    _user = getValue("user");
    _from_date = getValue("from_date");
    _to_date = getValue("to_date");
    _status = getValue("status");
    _page_limit = parseInt($('#items_per_page').val());

    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    client_mirror.getComplianceDetailsReport(_country, _domain, _act, _unit, 
    _compliance_task, _user, _from_date, _to_date, _status, csv, sno, _page_limit,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
            }
            else {

              if (csv) {
                var download_url = response.link;
                window.open(download_url, '_blank'); 
                hideLoader();
              }else{
                sno  = sno;
                unitWiseComplianceList = response.unit_wise_compliancess;
                totalRecord = response.total_count;

                if (totalRecord == 0) {
                  $('.tbody-unit').find('tbody').remove();
                  var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                  var clone4 = tableRow4.clone();
                  $('.no_records', clone4).text('No Compliance Found');
                  $('.tbody-unit').append(clone4);
                  $('.pagination-view').hide();
                  hideLoader();
                } else {
                  if(sno==0){
                    createPageView(totalRecord);
                  }
                  $('.pagination-view').show();
                  loadCompliances(unitWiseComplianceList);
                  
                }
              }

            }
        }
    );
};

$('#items_per_page').on('change', function (e) {
  perPage = parseInt($(this).val());
  sno = 0;
  on_current_page = 1;
  createPageView(totalRecord);
  fetchData(false);
});

function loadCompliance(csv){
  is_valid = validateMandatory();
  if (is_valid == true) {
    $('.grid-table-rpt').show();
    fetchData(csv);
  }
}

$('#submit').click(function () {
  on_current_page = 1;
  loadCompliance(false);
});
$('#export').click(function () {
  loadCompliance(true);
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
//retrive statutory autocomplete value
function onStatutorySuccess(val) {
  $('#actval').val(val[1]);
  $('#act').val(val[0].replace(/##/gi, '"'));
  $('#actval').focus();
}
//load statutory list in autocomplete textbox
$('#actval').keyup(function (e) {
  var textval = $(this).val();
  getClientStatutoryAutocomplete(e, textval, actList, function (val) {
    onStatutorySuccess(val);
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
//retrive compliance task form autocomplete value
function onComplianceTaskSuccess(val) {
  $('#compliancetaskval').val(val[1]);
  $('#compliancetask').val(val[0]);
  $('#compliancetaskval').focus();
}
//load compliancetask form list in autocomplete text box
$('#compliancetaskval').keyup(function (e) {
  var textval = $(this).val();
  getComplianceTaskAutocomplete(e, textval, compliancesList, function (val) {
    onComplianceTaskSuccess(val);
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
  getUserAutocomplete(e, textval, usersList, function (val) {
    onUserSuccess(val);
  });
});
//Autocomplete Script ends
//initialization
$(function () {
  $('.grid-table-rpt').hide();
  getComplianceDetailsReportFilters();
  $('#country').focus();
  loadItemsPerPage();
});