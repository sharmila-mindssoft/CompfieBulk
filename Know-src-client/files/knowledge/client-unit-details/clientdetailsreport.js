var countriesList;
var businessgroupsList;
var industriesList;
var domainsList;
var groupList;
var legalEntityList;
var unitList;
var unitReport;
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
var m_names = new Array('Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', "Dec");

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
var BusinessGroupVal = $('#businessgroupsval');
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
var _page_limit = 25;
var csv = false;

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
    domainsList = data.domains_organization_list;
    groupList = data.statutory_groups;
    unitList = data.units_report;
    industriesList = data.industry_name_id;
    resetAllfilter();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getClientDetailsReportFilters(function (error, response) {
    console.log(response);
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}
ExportButton.click(function () {
  //if($('.tbody-clientdetails-list').find('tr').length > 0){
    csv = true;
    var countries = $('#country-id').val();
    var groupid = $('#group-id').val();
    var bgroups = $('#businessgroupid').val();
    if (bgroups != '') {
      var businessgroupid = bgroups;
    } else {
      var businessgroupid = '%';
    }

    var legalentity = $('#legalentityid').val();
    if (legalentity != '') {
      var lentityid = parseInt(legalentity);
    } else {
      var lentityid = 0;
    }

    var units = $('#unitid').val();
    if (units != '') {
      var unitid = units;
    } else {
      var unitid = '%';
    }

    var domains = $('#domainid').val();
    if (domains != '') {
      var domainid = domains;
    } else {
      var domainid = '%';
    }

    var orgtype = $('#orgtypeid').val();
    if (orgtype != '') {
      var orgtypeid = orgtype;
    } else {
      var orgtypeid = '%'
    }

    if($('#from-date').val() == ''){
      var from_date = '%';
    }else{
      var from_date = $('#from-date').val();
    }

    if($('#to-date').val() == ''){
      var to_date = '%';
    }else{
      var to_date = $('#to-date').val();
    }

    var status = $('#unit-status').val();
    var unit_status  = '%';
    if(status == -1){
      unit_status = '%';
    }
    else {
      unit_status = status;
    }
    if (countries != '' && groupid != '' && lentityid > 0){
      var u_m_none = businessgroupid + ","+unitid+","+domainid+","+orgtypeid+","+from_date+","+to_date+","+unit_status;
      function onSuccess(data) {
        if (csv) {
          var download_url = data.link;
          $(location).attr('href', download_url);
        }
      }
      function onFailure(error) {
        if (error == "ExportToCSVEmpty") {
          displayMessage(message.empty_export);
        }else {
          displayMessage(error);
        }
      }
      displayLoader();
      mirror.exportClientDetailsReportData(parseInt(countries), parseInt(groupid), lentityid, csv, u_m_none, function (error, response) {
        if (error == null) {
          onSuccess(response);
          hideLoader();
        } else {
          onFailure(error);
          hideLoader();
        }
      });
    }
    else {
      if(countries == '')
      {
        displayMessage(message.country_required);
      }
      else if(groupid == '')
      {
        displayMessage(message.group_required);
      }
      else if(lentityid  == 0 || lentityid == '')
      {
        displayMessage(message.legalentity_required);
      }
    }
 // }
  /*else{
    displayMessage(message.export_empty);
  }*/
});

$('#show-button').click(function () {
  sno = 0;
  csv = false;
  on_current_page = 1;
  lastBG = '';
  lastLE = '';
  lastDv = '';
  $('.tbody-clientdetails-list').empty();
  loadunitdetailsreport();
});

function loadunitdetailsreport() {
  clearMessage();
  var unit_details = [];
  var countries = $('#country-id').val();
  var groupid = $('#group-id').val();
  var bgroups = $('#businessgroupid').val();
  if (bgroups != '') {
    var businessgroupid = bgroups;
  } else {
    var businessgroupid = '%';
  }

  var legalentity = $('#legalentityid').val();
  if (legalentity != '') {
    var lentityid = parseInt(legalentity);
  } else {
    var lentityid = 0;
  }

  var units = $('#unitid').val();
  if (units != '') {
    var unitid = units;
  } else {
    var unitid = '%';
  }

  var domains = $('#domainid').val();
  if (domains != '') {
    var domainid = domains;
  } else {
    var domainid = '%';
  }

  var orgtype = $('#orgtypeid').val();
  if (orgtype != '') {
    var orgtypeid = orgtype;
  } else {
    var orgtypeid = '%'
  }

  if($('#from-date').val() == ''){
    var from_date = '%';
  }else{
    var from_date = $('#from-date').val();
  }

  if($('#to-date').val() == ''){
    var to_date = '%';
  }else{
    var to_date = $('#to-date').val();
  }

  var status = $('#unit-status').val();
  var unit_status  = '%';
  if(status == -1){
    unit_status = '%';
  }
  else {
    unit_status = status;
  }

  if (countries != '' && groupid != '' && lentityid > 0){
    var u_m_none = businessgroupid + ","+unitid+","+domainid+","+orgtypeid+","+from_date+","+to_date+","+unit_status;
    function onSuccess(data) {
      unitReport = data.units_list;
      processPaging();
    }
    function onFailure(error) {
      displayMessage(error);
    }
    displayLoader();
    mirror.getClientDetailsReportData(parseInt(countries), parseInt(groupid), lentityid, u_m_none, function (error, response) {
      console.log(response)
      if (error == null) {
        onSuccess(response);
        hideLoader();
      } else {
        onFailure(error);
        hideLoader();
      }
    });
  }
  else {
    if(countries == '')
    {
      displayMessage(message.country_required);
    }
    else if(groupid == '')
    {
      displayMessage(message.group_required);
    }
    else if(lentityid  == 0 || lentityid == '')
    {
      displayMessage(message.legalentity_required);
    }
  }
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
    sno = 0;
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  totalRecord = unitReport.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.details').show();
    $('#compliance_animation')
      .removeClass().addClass('bounceInLeft animated')
      .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
      $(this).removeClass();
    });
    $('.grid-table-rpt').show();
    $('.countrynameval').text($('#countryval').val());
    $('.groupval').text($('#groupsval').val());
    if($('#businessgroupsval').val() != '')
    {
      $('.bgroupsval').text($('#businessgroupsval').val());
    }
    else
    {
      $('.bgroupsval').text("--");
    }
    $('.lentityval').text($('#legalentityval').val());
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
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<unitReport.length;i++)
  {
    is_null = false;
    data.push(unitReport[i]);
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
  $('.details').show();
  $('#compliance_animation')
    .removeClass().addClass('bounceInLeft animated')
    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
    $(this).removeClass();
  });
  $('.tbody-clientdetails-list').find('tr').remove();
  var status = $('#unit-status').val();
  //totalRecord = data.length;
  $('.grid-table-rpt').show();

  $('.countrynameval').text($('#countryval').val());
  $('.groupval').text($('#groupsval').val());
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
  sno = sno + 1;

  for(var i=0;i<data.length;i++)
  {
    var domainsNames = '';
    var orgnames = '';
    val = data[i];
    var tableRow = $('#templates .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(sno);
    $('.unit-code', clone).text(val.unit_code);
    $('.unit-name', clone).html(val.unit_name);
    if (val.division_name == '' || val.division_name == null)
      $('.division', clone).text("-Nil-");
    else
      $('.division', clone).text(val.division_name);

    if(val.category_name == null){
      $('.category', clone).text("-Nil-");
    }
    else{
      $('.category', clone).text(val.category_name);
    }

    $('.domain', clone).html(val.d_o_names);
    $('.unit-address', clone).text(val.address + ', ' + val.postal_code);
    $('.createdby', clone).text(val.emp_code_name);
    $('.createdon', clone).html(val.check_date);
    if(val.is_active == 0)
    {
      $('.status', clone).html("Active");
    }
    else if(val.is_active == 1)
    {
        if (status == "1"){
          if (val.closed_on == "null")
            $('.status', clone).html("Closed"+'<br>'+'-Nil-');
          else
            $('.status', clone).html("Closed"+'<br>'+val.closed_on);
        }else {
          if (val.closed_on == "null")
            $('.status', clone).html("Inactive"+'<br>'+'-Nil-');
          else
            $('.status', clone).html("Inactive"+'<br>'+val.closed_on);
        }

    }
    else
    {
      $('.status', clone).html("-Nil-")
    }
    $('.tbody-clientdetails-list').append(clone);
    sno = sno + 1;
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
  resetfilter('countries');
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    countriesList, "country_name", "country_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
  });
});


//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  resetfilter('clients');
  var text_val = $(this).val();
  var ctry_grps=[];
  if($('#country-id').val() > 0)
  {
    for(var i=0;i<groupList.length;i++)
    {
      if(groupList[i].country_id == $('#country-id').val())
      {
        var occur = -1;
        for(var k=0;k<ctry_grps.length;k++){
          if(ctry_grps[k].client_id == groupList[i].client_id){
            occur = 1;
          }
        }
        if(occur < 0){
          ctry_grps.push({
            "client_id": groupList[i].client_id,
            "group_name": groupList[i].short_name,
            "is_active": groupList[i].is_active
          });
        }
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
  resetfilter('bg');
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
        var occur = -1;
        for(var k=0;k<bg_grp.length;k++){
          if(bg_grp[k].business_group_id==businessgroupsList[i].business_group_id){
            occur = 1;
          }
        }
        if(occur < 1 && businessgroupsList[i].business_group_name != null){
          bg_grp.push({
            "client_id": businessgroupsList[i].client_id,
            "business_group_id": businessgroupsList[i].business_group_id,
            "business_group_name": businessgroupsList[i].business_group_name
          });
        }
      }
    }
    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroup, text_val,
      bg_grp, "business_group_name", "business_group_id", function (val) {
        onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
    }, condition_fields, condition_values);
  }
  else
  {
    /*if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }*/

  }
});
//retrive legelentity form autocomplete value

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
  resetfilter('le');
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
        var occur = -1;
        for(var k=0;k<le_list.length;k++){
          if(le_list[k].legal_entity_id == businessgroupsList[i].legal_entity_id){
            occur = 1;
          }
        }
        if(occur < 0){
          le_list.push({
            "client_id": businessgroupsList[i].client_id,
            "business_group_id": businessgroupsList[i].business_group_id,
            "legal_entity_id": businessgroupsList[i].legal_entity_id,
            "legal_entity_name": businessgroupsList[i].legal_entity_name
          });
        }
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
    /*if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }*/

  }
});

//retrive unit with condition form autocomplete value

//load unit wwith condition form list in autocomplete text box
$('#unitval').keyup(function (e) {
  resetfilter('unit');
  var unit_list = [];
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bg_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = true;
      if(businessgroupid>0 && (businessgroupid != unitList[i].business_group_id)){
        bg_check =false;
      }
      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && bg_check == true)
      {
        var occur = -1;
        for(var k=0;k<unit_list.length;k++)
        {
          if(unit_list[k].unit_id == unitList[i].unit_id){
            occur = 1;
          }
        }
        if(occur < 0){
          unit_list.push({
            "unit_id": unitList[i].unit_id,
            "unit_name": unitList[i].unit_code+"-"+unitList[i].unit_name
          });
        }
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
    e, ACUnit, Unit, text_val,
    unit_list, "unit_name", "unit_id", function (val) {
        onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }
  else
  {
    /*if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }*/
  }
});
//Domains------------------------------------------------------------------------------------------------
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domianid').val(val[0]);
  resetfilter('domain');
}
//load unit wwith condition form list in autocomplete text box
$('#domainval').keyup(function (e) {
  var country_id = $('#country-id').val();
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var unit_id = $('#unitid').val();
  resetfilter('domain');
  var domain_list = [];

  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = true;
      if(businessgroupid>0 && (businessgroupid != unitList[i].business_group_id)){
        bg_check =false;
      }
      var unit_check = true;
      if(unitid>0 &&(unitid != unitList[i].unit_id)){
        unit_check = false;
      }

      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && bg_check == true && unit_check == true)

      {
        var domain_ids = unitList[i].d_ids;
        for(var j=0;j<domain_ids.length;j++)
        {
          for(var k=0;k<domainsList.length;k++){
            if(domainsList[k].domain_id == domain_ids[j])
            {

              if(domain_list.length > 0)
              {
                  var arr_domain = [];
                  element = domain_ids[j];
                  arr_domain = domain_list.reduce(function(arr, e, i) {
                      if (e.domain_id === element)
                          arr.push(i);
                      return arr;
                  }, []);


                  if(arr_domain.length == 0){
                      domain_list.push({
                        "domain_id": domainsList[k].domain_id,
                        "domain_name": domainsList[k].domain_name,
                        "is_active":domainsList[k].is_active
                      });
                  }
              }
              else
              {
                  domain_list.push({
                    "domain_id": domainsList[k].domain_id,
                    "domain_name": domainsList[k].domain_name,
                    "is_active":domainsList[k].is_active
                  });
              }
            }
          }
        }
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domain_list, "domain_name", "domain_id", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    });
  }
  else
  {
    /*if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }*/
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
  console.log(domainsList)
  if(country_id > 0 && client_id > 0 && le_id > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      var bg_check = true;
      if(businessgroupid>0 && (businessgroupid != unitList[i].business_group_id)){
        bg_check =false;
      }
      var unit_check = true;
      if(unitid>0 &&(unitid != unitList[i].unit_id)){
        unit_check = false;
      }
      var domain_check = true;
      if(domainid>0 && (jQuery.inArray(domainid, unitList[i].d_ids) == -1)){
        domain_check = false;
      }


      if((unitList[i].country_id == country_id && unitList[i].client_id == client_id &&
        unitList[i].legal_entity_id == le_id) && bg_check == true && unit_check == true)
      {

        var org_ids = unitList[i].i_ids;
        console.log("1:"+domain_id)
        if(parseInt(domain_id )> 0){
            for(var j=0;j<org_ids.length;j++)
            {
              for(var k=0;k<domainsList.length;k++){
                if(domainsList[k].industry_id == org_ids[j] && domainsList[k].domain_id == domain_id)
                {
                  var occur = -1;
                  for (var org=0;org<org_list.length;org++){
                    if(org_list[org].industry_id == domainsList[k].industry_id && org_list[org].domain_id == domainsList[k].domain_id){
                      occur = 1;
                      break;
                    }
                  }
                  if (occur < 0){
                    org_list.push({
                      "domain_id": domainsList[k].domain_id,
                      "industry_id": domainsList[k].industry_id,
                      "industry_name": domainsList[k].industry_name
                      //"is_active":industriesList[k].is_active
                    });
                  }
                }
              }
            }
        }else{
            for(var j=0;j<org_ids.length;j++)
            {
              for(var k=0;k<industriesList.length;k++){
                if(industriesList[k].industry_id == org_ids[j])
                {
                  var occur = -1;
                  for (var org=0;org<org_list.length;org++){
                    if(org_list[org].industry_id == industriesList[k].industry_id && org_list[org].domain_id == industriesList[k].domain_id){
                      occur = 1;
                      break;
                    }
                  }
                  if (occur < 0){
                    org_list.push({
                      "domain_id": industriesList[k].domain_id,
                      "industry_id": industriesList[k].industry_id,
                      "industry_name": industriesList[k].industry_name
                      //"is_active":industriesList[k].is_active
                    });
                  }
                }
              }
            }
        }
      }
    }
    console.log(org_list)
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACOrgtype, Orgtype, text_val,
      org_list, "industry_name", "industry_id", function (val) {
        onAutoCompleteSuccess(OrgtypeVal, Orgtype, val);
    });

  }
  else
  {
    /*if(country_id == 0 || country_id == '')
    {
      displayMessage(message.country_required);
    }
    else if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    else if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }*/
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
  $("#unit-status").prop('selectedIndex', 0);
  $('#from-date').val('');
  $('#to-date').val('');
  $('#country-id').val('');
  $('#group-id').val('');
  $('#businessgroupid').val('');
  $('#legalentityid').val('');
  $('#unitid').val('');
  $('#domainid').val('');
  $('#orgtypeid').val('');
  $('#countryval').focus();
}
function resetfilter(evt)
{
  //alert("jhjh");'
  if(evt == 'countries')
  {
    $('#groupsval').val('');
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  if(evt == 'clients')
  {
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  if(evt == 'bg')
  {
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  if(evt == 'le')
  {
    $('#unitval').val('');
    $('#domainval').val('');
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  if(evt == 'unit')
  {
    $('#domainval').val('');
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  if(evt == 'domian')
  {
    $('#orgtypeval').val('');
    $('#from-date').val('');
    $('#to-date').val('');
  }
  $('.tbody-clientdetails-list').empty();
  $('.details').hide();
}
$('#from-date').on('keypress', function (e) {
    var k = e.which;
      var ok = k == 127;

      if (!ok){
          e.preventDefault();
      }
      else{
        $('#from-date').val('');
      }
  });

$('#to-date').on('keypress', function (e) {
    var k = e.which;
      var ok = k == 127;

      if (!ok){
          e.preventDefault();
      }
      else{
        $('#to-date').val('');
      }
  });

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