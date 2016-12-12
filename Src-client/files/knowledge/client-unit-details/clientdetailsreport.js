var countriesList;
var businessgroupsList;
var industriesList;
var domainsList;
var groupList;
var legalEntityList;
var unitList;
var countriesText;
var groupsval;
var businessgroupsval;
var legalentityval;
var divisionval;
var unitval;
var sno = 0;
var totalRecord;
var lastBG = '';
var lastLE = '';
var lastDV = '';
var matchedUnits;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
var ACOrgtype = $('#ac-industry');
var ACDomain = $('#ac-domain');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country-id');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var BusinessGroupVal = $('#businessgroupval');
var BusinessGroup = $('#businessgroupid');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UnitVal = $('#unitval');
var Unit = $('#unitid');
var OrgtypeVal = $('#orgtypeval');
var Orgtype = $('#orgtypeid');
var DomainVal = $('#domainval');
var Domain = $('#domainid');
var FromDate = $('#from-date');
var ToDate = $('#to-date');
var SubmitButton = $('#show-button');
var ExportButton = $('#export');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
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
    businessgroupsList = data.statutory_business_groups;
    domainsList = data.domains;
    groupList = data.statutory_groups;
    unitList = data.units_report;
    industriesList = data.industry_name_id;
    console.log(data)
    resetAllfilter();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getClientDetailsReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
$('#show-button').click(function () {
  sno = 0;
  lastBG = '';
  lastLE = '';
  lastDv = '';
  $('.tbody-clientdetails-list').empty();
  $('.details').show();
  $('#compliance_animation')
    .removeClass().addClass('bounceInLeft animated')
    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
    $(this).removeClass();
  });
  loadunitdetailsreport();
});

function loadunitdetailsreport() {
  clearMessage();
  var unit_details = [];
  var countries = $('#country-id').val();
  countriesText = $('#countryval').val();
  console.log("countries:"+countries)

  var groupid = $('#group-id').val();
  groupsval = $('#groupsval').val();
  console.log("clients:"+groupid)

  var bgroups = $('#businessgroupid').val();
  if (bgroups != '') {
    var businessgroupid = parseInt(bgroups);
  } else {
    var businessgroupid = 0;
  }
  businessgroupsval = $('#businessgroupsval').val();
  console.log("businessgroupid:"+businessgroupid)

  var legalentity = $('#legalentityid').val();
  if (legalentity != '') {
    var lentityid = parseInt(legalentity);
  } else {
    var lentityid = 0;
  }
  legalentityval = $('#legalentityval').val();
  console.log("lentityid:"+lentityid)

  var units = $('#unitid').val();
  if (units != '') {
    var unitid = parseInt(units);
  } else {
    var unitid = 0;
  }
  unitval = $('#unitval').val();
  console.log("unitid:"+unitid)

  var domains = $('#domainid').val();
  if (domains != '') {
    var domainid = parseInt(domains);
  } else {
    var domainid = 0;
  }
  domainval = $('#domainval').val();
  console.log("domainid:"+domainid)

  var orgtype = $('#orgtypeid').val();
  if (orgtype != '') {
    var orgtypeid = parseInt(orgtype);
  } else {
    var orgtypeid = 0;
  }
  orgtypeval = $('#orgtypeval').val();
  console.log("orgtypeid:"+orgtypeid)


  if (countries == '') {
    displayMessage(message.country_required);
  } else if (groupid == '') {
    displayMessage(message.group_required);
  } else if (legalentity == '') {
    displayMessage(message.legal_entity_required);
  }
   else {
    console.log("insdie report")
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = businessgroupid>0?(businessgroupid == unitList[i].business_group_id):false;
      var unit_check = unitid>0?(unitid == unitList[i].unit_id):false;
      var domain_check = domainid>0?(jQuery.inArray(domain_id, unitList[i].d_ids)):false;
      var org_check = orgtypeid>0?(jQuery.inArray(orgtypeid, unitList[i].i_ids)):false;
      var created_bool = matchCreatedDates(unitList[i]);
      console.log(created_bool)

      if((unitList[i].country_id == countries && unitList[i].client_id == groupid &&
        unitList[i].legal_entity_id == legalentity) && (bg_check == true || bg_check == false) &&
        (unit_check == true || unit_check == false) && (domain_check == true || domain_check == false)
        && (org_check == true || org_check == false) && (created_bool == true))
      {
        unit_details.push(unitList[i]);
      }
    }
  }
  console.log("list:"+unit_details.length);
  matchedUnits = unit_details;
  totalRecord = unit_details.length;
  processPaging();
  //loadClientDetailsList(unit_details);
}
function matchCreatedDates(data)
{
  var date_check = false;

  var db_date = null;
  if(data.check_date != null)
  {
    db_date = Date.parse(data.check_date);
  }
  console.log("db_dat:"+db_date)

  var fromdate = null;
  if($('#from-date').val() != '')
  {
    fromdate = Date.parse($('#from-date').val());
  }
  console.log("fromdate:"+fromdate)
  var todate = null;
  if($('#to-date').val() != '')
  {
    todate = Date.parse($('#to-date').val());
  }
  console.log("todate:"+todate)

  if(fromdate != null && todate != null && db_date != null)
  {
    if(db_date >= fromdate && db_date <= todate)
    {
      date_check = true;
    }
  }
  else if(fromdate != null && todate == null && db_date != null)
  {
    if(db_date >= fromdate)
    {
      date_check = true;
    }
  }
  else if(fromdate == null && todate != null && db_date != null)
  {
    if(db_date <= todate)
    {
      date_check = true;
    }
  }
  else if(fromdate == null && todate == null && db_date != null)
  {
    date_check = true;
  }
  else if(fromdate != null && todate != null && db_date == null)
  {
    date_check = true;
  }
  return date_check;
}

//pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processPaging();
            }
        }
    });
};

function processPaging(){
  _page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  totalRecord = matchedUnits.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.tbody-clientdetails-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-clientdetails-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadClientDetailsList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  console.log(totalRecord,_page_limit)
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<matchedUnits.length;i++)
  {
    is_null = false;
    data.push(matchedUnits[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
  if (is_null == true) {
    hidePagePan();
  }
  else {
    if(recordLength < totalRecord)
      showPagePan(showFrom, recordLength, totalRecord);
    else
      showPagePan(showFrom, totalRecord, totalRecord);
  }
  return data;
}

function loadClientDetailsList(data) {

  $('.tbody-clientdetails-list').find('tr').remove();
  var status = $('#unit-status').val();
  //totalRecord = data.length;
  console.log("status:"+status)
  $('.grid-table-rpt').show();
  /*var tablefilter = $('#templates .tr-filter');
  var clonefilter = tablefilter.clone();
  $('.countrynameval', clonefilter).text($('#countryval').val());
  $('.groupsval', clonefilter).text($('#groupsval').val());
  if($('#businessgroupsval').val() != '')
  {
    $('.bgroupsval', clonefilter).text($('#businessgroupsval').val());
  }
  else
  {
    $('.bgroupsval', clonefilter).text("--");
  }
  $('.lentityval', clonefilter).text($('#legalentityval').val());
  $('.tbody-clientdetails-list').append(clonefilter);*/

  $('.countrynameval').text($('#countryval').val());
  $('.groupsval').text($('#groupsval').val());
  if($('#businessgroupsval').val() != '')
  {
    $('.bgroupsval').text($('#businessgroupsval').val());
  }
  else
  {
    $('.bgroupsval').text("--");
  }
  $('.lentityval').text($('#legalentityval').val());

  var tableheading = $('#templates .tr-heading');
  var cloneheading = tableheading.clone();
  $('.tbody-clientdetails-list').append(cloneheading);
  var row_no = 1;
  if(status == "-1")
  {
    for(var i=0;i<data.length;i++)
    {
      var domainsNames = '';
      var orgnames = '';
      val = data[i];
      var tableRow = $('#templates .table-row');
      var clone = tableRow.clone();
      $('.sno', clone).text(row_no);
      $('.unit-code', clone).text(val.unit_code);
      $('.unit-name', clone).html(val.unit_name);
      if (val.division_name != '' || val.division_name != null)
        $('.division', clone).text(val.division_name);
      else
        $('.division', clone).text("-Nil-");
      console.log(val.category_name)
      if(val.category_name == null){
        $('.category', clone).text("-Nil-");
      }
      else{
        $('.category', clone).text(val.category_name);
      }
      arr = val.d_ids;
      var d_names= [];
      $.each(domainsList, function (key, value) {
        var domianid = value.domain_id;
        var domainname = value.domain_name;
        if (jQuery.inArray(domianid, arr) > -1) {
          d_names.push(domainname);
        }
      });
      domainsNames = d_names.join(', ');
      console.log("domains:"+domainsNames)
      //$('.domain', clone).html(domainsNames);
      arr = val.i_ids;
      var o_names = [];
      $.each(industriesList, function (key, value) {
        var orgid = value.industry_id;
        var orgname = value.industry_name;
        if (jQuery.inArray(orgid, arr) > -1) {
          o_names.push(orgname);
        }
      });
      orgnames = o_names.join(', ');
      console.log("orgs:"+orgnames)
      var domain_org = '';
      if(domainsNames != '' && domainsNames.indexOf(",") >= 0)
      {
        if(domainsNames.length == orgnames.length)
        {
          for(var j=0;j<domainsNames.split(',').length;j++)
          {
            domain_org += domainsNames[j] + '-'+orgnames.split(',')[j] +'\n';
          }
        }
        else
        {
          for(var j=0;j<domainsNames.split(',').length;j++)
          {
            console.log("orgbbbb:"+orgnames.split(',')[j])
            if(orgnames.split(',')[j] == "" || orgnames.split(',')[j] == null || orgnames.split(',')[j] == undefined)
            {
              console.log("undefined")
              domain_org += domainsNames.split(',')[j] + '-'+'Nil'+'\n';
            }
            else
            {
              domain_org += domainsNames.split(',')[j] + '-'+orgnames.split(',')[j] +'\n';
            }
          }
        }
      }
      else if(domainsNames != '' && domainsNames.indexOf(",") < 0)
      {
        domain_org = domainsNames;
        if(orgnames != '' && orgnames.indexOf(",")<0)
        {
          domain_org = domainsNames + ' - '+orgnames;
        }
        else
        {
          domain_org = domainsNames + ' - '+'Nil';
        }
      }
      else
      {
        domainsNames = "Nil";
        if(orgnames != '' && orgnames.indexOf(",")<0)
        {
          domain_org = domainsNames + ' - '+orgnames;
        }
        else
        {
          domain_org = domainsNames + ' - '+'Nil';
        }
      }
      $('.domain', clone).html(domain_org);
      $('.unit-address', clone).text(val.address + ', ' + val.postal_code);
      $('.createdby', clone).text(val.emp_code_name);
      $('.createdon', clone).html(val.created_on);
      if(val.is_active == 1)
      {
        $('.status', clone).html("Active");
      }
      else if(val.is_active == 0)
      {
        $('.status', clone).html("Closed"+'\n'+val.closed_on);
      }
      else
      {
        $('.status', clone).html("--")
      }
      $('.tbody-clientdetails-list').append(clone);
      row_no = row_no + 1;
    }
  }
  else
  {
    for(var i=0;i<data.length;i++)
    {
      if(status.indexOf(data[i].is_active) >= 0)
      {
        var domainsNames = '';
        var orgnames = '';
        val = data[i];
        var tableRow = $('#templates .table-row');
        var clone = tableRow.clone();

        $('.sno', clone).text(row_no);
        $('.unit-code', clone).text(val.unit_code);
        $('.unit-name', clone).html(val.unit_name);
        $('.division', clone).text(val.division_name);
        $('.category', clone).text(val.category_name);
        arr = val.d_ids;
        $.each(domainsList, function (key, value) {
          var domianid = value.domain_id;
          var domainname = value.domain_name;
          if (jQuery.inArray(domianid, arr) > -1) {
            domainsNames += domainname + ', ';
          }
        });
        console.log("domains:"+domainsNames)
        //$('.domain', clone).html(domainsNames);
        arr = val.i_ids;
        $.each(industriesList, function (key, value) {
          var orgid = value.industry_id;
          var orgname = value.industry_name;
          if (jQuery.inArray(orgid, arr) > -1) {
            orgnames += orgnames + ', ';
          }
        });
        console.log("orgs:"+orgnames)
        var domain_org = null;
        if(domainsNames != '' && domainsNames.indexOf(",") > 0)
        {
          if(domainsNames.length == orgnames.length)
          {
            for(var j=0;j<domainsNames.split(',').length;j++)
            {
              domain_org += domainsNames[j] + '-'+orgnames.split(',')[j] +'\n';
            }
          }
        }
        else if(domainsNames != '' && domainsNames.indexOf(",") < 0)
        {
          domain_org = domainsNames + ' - '+orgnames;
        }
        $('.domain', clone).html(domain_org);
        $('.unit-address', clone).text(val.address + ', ' + val.postal_code);
        $('.createdby', clone).text(val.emp_code_name);
        $('.createdon', clone).html(val.created_on);
        if(val.is_active == 1)
        {
          $('.status', clone).html("Active");
        }
        else if(val.is_active == 0)
        {
          $('.status', clone).html("Closed"+'\n'+val.closed_on);
        }
        else
        {
          $('.status', clone).html("--")
        }
        $('.tbody-clientdetails-list').append(clone);
        row_no = row_no + 1;
      }
    }
  }


}
//Countries---------------------------------------------------------------------------------------------------------------
//retrive country autocomplete value
//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'country'){
      resetfilter('countries');
    }else if(current_id == 'group-id'){
      resetfilter('clients');
    }else if(current_id == 'businessgroupid'){
      resetfilter('bg');
    }
    else if(current_id == 'legalentityid'){
      resetfilter('le');
    }else if(current_id == 'unitid'){
      resetfilter('unit');
    }else if(current_id == 'domainid'){
      resetfilter('domian');
    }
}

//load country list in autocomplete textbox
$('#countryval').keyup(function (e) {
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    countriesList, "country_name", "country_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
  });
});


//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  var text_val = $(this).val();
  var ctry_grps=[];
  if($('#country-id').val() > 0)
  {
    for(var i=0;i<groupList.length;i++)
    {
      if(groupList[i].country_id == $('#country-id').val())
      {
        ctry_grps.push({
          "client_id": groupList[i].client_id,
          "group_name": groupList[i].short_name,
          "is_active": groupList[i].is_active
        });
      }
    }
    commonAutoComplete(
      e, ACGroup, Group, text_val,
      ctry_grps, "group_name", "client_id", function (val) {
        onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  else
  {
    displayMessage(message.country_required);
  }
});
//retrive businessgroup form autocomplete value

//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
  var text_val = $(this).val();
  var bg_grp = [];
  if($('#group-id').val() > 0)
  {
    var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
    for(var i=0;i<businessgroupsList.length;i++)
    {
      if(businessgroupsList[i].client_id == $('#group-id').val())
      {
        bg_grp.push({
            "client_id": businessgroupsList[i].client_id,
            "business_group_id": businessgroupsList[i].business_group_id,
            "business_group_name": businessgroupsList[i].business_group_name
        });
      }
    }
    console.log(bg_grp.length)
    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroup, text_val,
      bg_grp, "business_group_name", "business_group_id", function (val) {
        onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
    }, condition_fields, condition_values);
  }
  else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});
//retrive legelentity form autocomplete value

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
  var le_list = [];
  var bg_id = $('#businessgroupid').val();
  if($('#group-id').val() > 0)
  {
    var condition_fields = [];
    var condition_values = [];
    if(Group.val() != ''){
      condition_fields.push("client_id");
      condition_values.push(Group.val());
    }
    if(BusinessGroup.val() != ''){
      condition_fields.push("business_group_id");
      condition_values.push(BusinessGroup.val());
    }

    for(var i=0;i<businessgroupsList.length;i++)
    {
      var bg_check = bg_id>0?(bg_id == businessgroupsList[i].business_group_id):false;
      if(($('#group-id').val() == businessgroupsList[i].client_id) && (bg_check == true || bg_check == false))
      {
        le_list.push({
          "client_id": businessgroupsList[i].client_id,
          "business_group_id": businessgroupsList[i].business_group_id,
          "legal_entity_id": businessgroupsList[i].legal_entity_id,
          "legal_entity_name": businessgroupsList[i].legal_entity_name
        });
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACLegalEntity, LegalEntity, text_val,
      le_list, "legal_entity_name", "legal_entity_id", function (val) {
          onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
      }, condition_fields, condition_values);
  }
  else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});

//retrive unit with condition form autocomplete value

//load unit wwith condition form list in autocomplete text box
$('#unitval').keyup(function (e) {
  var unit_list = [];
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bg_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = bg_id>0?(bg_id == unitList[i].business_group_id):false;
      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && (bg_check == true || bg_check == false))
      {
        unit_list.push({
          "unit_id": unitList[i].unit_id,
          "unit_name": unitList[i].unit_code+"-"+unitList[i].unit_name
        });
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
    e, ACUnit, Unit, text_val,
    unit_list, "unit_id", "unit_name", function (val) {
        onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
});
//Domains------------------------------------------------------------------------------------------------
function onDomainSuccess(val) {
  console.log("domain val:"+val)
  $('#domainval').val(val[1]);
  $('#domianid').val(val[0]);
  resetfilter('domain');
}
//load unit wwith condition form list in autocomplete text box
$('#domainval').keyup(function (e) {
  console.log("inside domains")
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var unit_id = $('#unitid').val();
  var domain_list = [];

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id == unitList[i].business_group_id):false;
      var unit_check = unit_id>0?(unit_id == unitList[i].unit_id):false;
      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && (bg_check == true || bg_check == false) &&
        (unit_check == true || unit_check == false))
      {
        for(var j=0;j<domainsList.length;j++)
        {
          console.log("domain:"+domainsList[j].domain_id)
          if(jQuery.inArray(domainsList[j].domain_id, unitList[i].d_ids))
          {
            domain_list.push({
              "domain_id": domainsList[j].domain_id,
              "domain_name": domainsList[j].domain_name,
              "is_active":domainsList[j].is_active
            });
            break;
          }
        }
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domain_list, "domain_id", "domain_name", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    });
  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
});

//Organization type------------------------------------------------------------------------------------------------
function onOrgtypeSuccess(val) {
  $('#orgtypeval').val(val[1]);
  $('#orgtypeid').val(val[0]);
  resetfilter('orgtype');
}
//load unit wwith condition form list in autocomplete text box
$('#orgtypeval').keyup(function (e) {
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var unit_id = $('#unitid').val();
  var domain_id = $('#domainid').val();
  var org_list = [];

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id == unitList[i].business_group_id):false;
      var unit_check = unit_id>0?(unit_id == unitList[i].unit_id):false;
      var domain_check = domain_id>0?(jQuery.inArray(domain_id, unitList[i].d_ids)):false;
      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && (bg_check == true || bg_check == false) &&
        (unit_check == true || unit_check == false) && (domain_check == true || domain_check == false))
      {
        for(var j=0;j<industriesList.length;j++)
        {
          if(jQuery.inArray(industriesList[j].industry_id, unitList[i].i_ids))
          {
            org_list.push({
              "industry_id": industriesList[j].industry_id,
              "industry_name": industriesList[j].industry_name,
              "is_active":industriesList[j].is_active
            });
            break;
          }
        }
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACOrgtype, Orgtype, text_val,
      org_list, "industry_id", "industry_name", function (val) {
        onAutoCompleteSuccess(OrgtypeVal, Orgtype, val);
    });

  }
  else
  {
    if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legal_entity_required);
    }
  }
});

function resetAllfilter()
{
  $('#countryval').val('');
  $('#groupsval').val('');
  $('#businessgroupsval').val('');
  $('#legalentityval').val('');
  $('#unitval').val('');
  $('#domainval').val('');
  $('#orgtypeval').val('');
  $("select#elem").prop('selectedIndex', 0);
  $('#from-date').val('');
  $('#to-date').val('');
  $('#countryval').focus();
}
function resetfilter(evt)
{
  //alert("jhjh");'
  console.log(evt);
  if(evt == 'countries')
  {
    $('#groupsval').val('');
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
  }
  if(evt == 'clients')
  {
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
  }
  if(evt == 'bg')
  {
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
  }
  if(evt == 'le')
  {
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
  }
  if(evt == 'unit')
  {
    $('#domainval').val('');
    $('#orgtypeval').val('');
  }
  if(evt == 'domian')
  {
    $('#orgtypeval').val('');
  }

}

function renderControls(){
  initialize();

  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });
}

$(function () {
  $('.grid-table-rpt').hide();
  renderControls();
  loadItemsPerPage();
});