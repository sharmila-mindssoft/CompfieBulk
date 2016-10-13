var countriesList;
var businessgroupsList;
var divisionsList;
var domainsList;
var legalEntityList;
var unitList;
var unitRecordList;

var on_current_page = 1;
var sno = 0;
var totalRecord;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function initialize() {
  function onSuccess(data) {
    countriesList = data.countries;
    businessgroupsList = data.business_groups;
    divisionsList = data.divisions;
    domainsList = data.domains;
    legalEntityList = data.legal_entities;
    unitList = data.units;
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getClientDetailsReportFilters(function (error, response) {
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
        }else{
            var arrayDomainsVal = d_id.split(',');
            var arrayDomains = [];
            for (var j = 0; j < arrayDomainsVal.length; j++) {
              arrayDomains[j] = parseInt(arrayDomainsVal[j]);
            }
            return arrayDomains;
        }
    }
    else if (field_name == "bg") {
        bg_id = $('#businessgroupid').val().trim();
        if (bg_id == '') {
            return null;
        }
        return parseInt(bg_id);;
    }
    else if (field_name == "le") {
        le_id = $('#legalentityid').val().trim();
        if (le_id == '') {
            return null;
        }
        return parseInt(le_id);
    }
    else if (field_name == "division") {
        dv_id = $('#divisionid').val().trim();
        if (dv_id == '') {
            return null;
        }
        return parseInt(dv_id);
    }
    else if (field_name == "unit") {
        u_id = $('#unitid').val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    }
    
};

function validateMandatory(){
    is_valid = true;
    if (getValue("country") == null) {
        displayMessage(message.country_required);
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


function getdomainnames(list) {
  var domainsNames = '';
  $.each(domainsList, function (key, value) {
    var domainid = domainsList[key].domain_id;
    var domainname = domainsList[key].domain_name;
    if (jQuery.inArray(domainid, list) > -1) {
      domainsNames += domainname + ', ';
    }
  });
  return domainsNames;
}
function loadUnitDetailsList(data) {
  $('.tbody-unitdetails-list tr').remove();
  var showFrom = sno + 1;
  var is_null = true;
  var countryText = $('#countryval').val();
  $.each(data, function (key, value) {
    var bg = '-';
    if (data[key].business_group_name != null)
      bg = data[key].business_group_name;
    var dv = '-';
    if (data[key].division_name != null)
      dv = data[key].division_name;
    var le = data[key].legal_entity_name;
    var tableRowHeading = $('#templates .table-unitdetails-list .filter-heading-list');
    var cloneHeading = tableRowHeading.clone();
    $('.filter-country-name', cloneHeading).text(countryText);
    $('.filter-business-group-name', cloneHeading).text(bg);
    $('.filter-legal-entity-name', cloneHeading).text(le);
    $('.filter-division-name', cloneHeading).text(dv);
    $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeading);
    var tableRowHeadingth = $('#templates .table-unitdetails-list .heading-list');
    var cloneHeadingth = tableRowHeadingth.clone();
    $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeadingth);
      
    var list = data[key].units;
    $.each(list, function (k, valu) {
      is_null = false;
      var tableRowvalues = $('#templates .table-unitdetails-list .table-row');
      var cloneval = tableRowvalues.clone();
      sno = sno + 1;
      $('.sno', cloneval).text(sno);
      $('.unit-name', cloneval).html(list[k].unit_code + ' - ' + list[k].unit_name);
      $('.domain-name', cloneval).html(getdomainnames(list[k].domain_ids));
      $('.unit-address', cloneval).html(list[k].unit_address);
      $('.unit-location', cloneval).html(list[k].geography_name);
      $('.pincode', cloneval).html(list[k].postal_code);
      $('.unitdetails-list .tbody-unitdetails-list').append(cloneval);
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
    _le = getValue("le");
    _bg = getValue("bg");
    _division = getValue("division");
    _unit = getValue("unit");
    _domain = getValue("domain");
    
    
    _page_limit = parseInt($('#items_per_page').val());

    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    client_mirror.getClientDetailsReportData(_country, _bg, _le, _division, 
      _unit, _domain, csv, sno, _page_limit,
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
                unitRecordList = response.units;
                totalRecord = response.total_count;

                if (totalRecord == 0) {
                  $('.tbody-unitdetails-list tr').remove();
                  var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                  var clone4 = tableRow4.clone();
                  $('.no_records', clone4).text('No Compliance Found');
                  $('.tbody-unitdetails-list').append(clone4);
                  $('.pagination-view').hide();
                  hideLoader();
                } else {
                  if(sno==0){
                    createPageView(totalRecord);
                  }
                  $('.pagination-view').show();
                  loadUnitDetailsList(unitRecordList);
                  
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

function loadunitdetailsreport(csv){
  is_valid = validateMandatory();
  if (is_valid == true) {
    $('.grid-table-rpt').show();
    fetchData(csv);
  }
}

$('#show-button').click(function () {
  on_current_page = 1;
  loadunitdetailsreport(false);
});
$('#export-button').click(function () {
  loadunitdetailsreport(true);
});


//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country').val(val[0]);
}
//load country list in autocomplete text box  
$('#countryval').keyup(function (e) {
  function callback(val) {
    onCountrySuccess(val);
  }
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, callback, flag = true);
});
//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val) {
  $('#businessgroupsval').val(val[1]);
  $('#businessgroupid').val(val[0]);
}
//load businessgroup form list in autocomplete text box  
$('#businessgroupsval').keyup(function (e) {
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(e, textval, businessgroupsList, function (val) {
    onBusinessGroupSuccess(val);
  });
});
//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val) {
  $('#legalentityval').val(val[1]);
  $('#legalentityid').val(val[0]);
}
//load legalentity form list in autocomplete text box  
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(e, textval, legalEntityList, function (val) {
    onLegalEntitySuccess(val);
  });
});
//retrive division form autocomplete value
function onDivisionSuccess(val) {
  $('#divisionval').val(val[1]);
  $('#divisionid').val(val[0]);
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
  $('#unitid').val(val[0]);
}
//load unit  form list in autocomplete text box  
$('#unitval').keyup(function (e) {
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = 0;
  getUnitAutocomplete(e, textval, unitList, function (val) {
    onUnitSuccess(val);
  });
});
//domain selet box
function hidemenudomains() {
  document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains() {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var editdomainval = [];
  if ($('#domain').val() != '') {
    editdomainval = $('#domain').val().split(',');
  }
  var domains = domainsList;
  $('#selectboxview-domains ul').empty();
  var str = '';
  for (var i in domains) {
    var selectdomainstatus = '';
    for (var j = 0; j < editdomainval.length; j++) {
      if (editdomainval[j] == domains[i].domain_id) {
        selectdomainstatus = 'checked';
      }
    }
    var domainId = parseInt(domains[i].domain_id);
    var domainName = domains[i].domain_name;
    if (selectdomainstatus == 'checked') {
      str += '<li id="' + domainId + '" class="active_selectbox" onclick="activate(this)" >' + domainName + '</li> ';
    } else {
      str += '<li id="' + domainId + '" onclick="activate(this)" >' + domainName + '</li> ';
    }
  }
  $('#selectboxview-domains ul').append(str);
  $('#domainselected').val(editdomainval.length + ' Selected')  // }
;
}
//check & uncheck process
function activate(element) {
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'active_selectbox') {
    $(element).removeClass('active_selectbox');
  } else {
    $(element).addClass('active_selectbox');
  }
  var selids = '';
  var totalcount = $('.active_selectbox').length;
  $('.active_selectbox').each(function (index, el) {
    if (index === totalcount - 1) {
      selids = selids + el.id;
    } else {
      selids = selids + el.id + ',';
    }
  });
  $('#domainselected').val(totalcount + ' Selected');
  $('#domain').val(selids);
}
$(function () {
  $('.grid-table-rpt').hide();
  loadItemsPerPage();
  initialize();
});