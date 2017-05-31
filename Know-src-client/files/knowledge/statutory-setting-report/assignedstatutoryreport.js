var countriesList;
var businessgroupsList;
var divisionsList;
var domainsList;
var groupList;
var legalEntityList;
var unitList;
var countriesText;
var groupsval;
var businessgroupsval;
//var legalentityval;
var divisionval;
var unitval;
var level1val;
var applicableStatus;
var assignedStatutoryList;
var finalList;
var pageSize = 500;
var startCount = 0;
var endCount;
var unitcountid = null;
var fullArrayList = [];
var matchedStatutory;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
var ACOrgtype = $('#ac-industry');
var ACDomain = $('#ac-domain');
var ACAct = $('#ac-statutory');
var ACCompltask = $('#ac-compliancetask');

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
var ActVal = $('#statutoryval');
var Act = $('#statutoryid');
var CTaskVal = $('#compliance-task');
var CTask = $('#complianceid');
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
var page_limit = 25;
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
    domainsList = data.domains;
    businessgroupsList = data.statutory_business_groups;
    groupList = data.statutory_groups;
    unitList = data.statutory_units;
    domain_compl_stat_List = data.statutory_compliances;
    //loadCountries(countriesList);
    console.log(data)
    resetAllfilter();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getAssignedStatutoryReportFilters(function (error, response) {
    if (error == null) {
      hideLoader();
      onSuccess(response);
    } else {
      hideLoader();
      onFailure(error);
    }
  });
}

$('#show-button').click(function () {
  csv = false;
  on_current_page = 1;
  sno = 0;
  total_record = 0;
  processSubmit();
});

function processSubmit(){
    page_limit = parseInt(ItemsPerPage.val());
    if (on_current_page == 1) {
        sno = 0
    }
    else {
        sno = (on_current_page - 1) *  page_limit;
    }

  //country selection
  var countries = $('#country-id').val();
  //countriesText = $('#countries  option:selected').text();
  //Domain
  var domain = $('#domain').val();
  if (domain != '') {
    var domainsVal = parseInt(domain);
  } else {
    var domainsVal = 0;
  }
  var domainName = $('#domainval').val();
  //Groups
  var groups = $('#group-id').val();
  if (groups != '') {
    var groupid = parseInt(groups);
  } else {
    var groupid = null;
  }
  groupsval = $('#groupsval').val();
  //Business Groups
  var bgroups = $('#businessgroupid').val();
  businessgroupsval = $('#businessgroupsval').val().trim();
  if (bgroups != '') {
    if (businessgroupsval != '') {
      var businessgroupid = parseInt(bgroups);
    } else {
      var businessgroupid = 0;
    }
  } else {
    var businessgroupid = 0;
  }
  //Legal Entity
  var legalentity = $('#legalentityid').val();
  legalentityval = $('#legalentityval').val().trim();
  if (legalentity != '') {
    if (legalentityval != '') {
      var lentityid = parseInt(legalentity);
    } else {
      var lentityid = null;
    }
  } else {
    var lentityid = null;
  }

  //Units
  var units = $('#unitid').val();
  unitval = $('#unitval').val().trim();
  if (units != '') {
    if (unitval != '') {
      var unitid = parseInt(units);
    } else {
      var unitid = 0;
    }
  } else {
    var unitid = 0;
  }

  //Act
  var statutory = $('#statutoryid').val();
  statutoryval = $('#statutoryval').val().trim();
  if (statutory != '') {
    if (statutoryval != '') {
      var statutoryid = parseInt(statutory);
    } else {
      var statutoryid = 0;
      statutoryval = '%';
    }
  } else {
    var statutoryid = 0;
    statutoryval = '%';
  }

  //Level1Statutory
  var compliance = $('#complianceid').val();
  console.log(compliance)
  var compliancetask = $('#compliance-task').val().trim();
  console.log(compliancetask)
  if (compliance != '') {
    if (compliancetask != '') {
      var complianceid = parseInt(compliance);
    } else {
      var complianceid = 0;
    }
  } else {
    var complianceid = 0;
  }

  if (countries == '') {
    displayMessage(message.country_required);
    $('.grid-table-rpt').hide();
  } else if (groups == '') {
    displayMessage(message.group_required);
    $('.grid-table-rpt').hide();
  } else if (legalentity == '') {
    displayMessage(message.legalentity_required);
    $('.grid-table-rpt').hide();
  } else {
    displayLoader();
    function onSuccess(data) {
        if (csv) {
          hideLoader();
          clearMessage();
          var download_url = data.link;
          $(location).attr('href', download_url);
        }else{
        $('.details').show();
        $('#compliance_animation')
          .removeClass().addClass('bounceInLeft animated')
          .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
          $(this).removeClass();
        });
        fullArrayList = [];
        hideLoader();
        clearMessage();
        sno = 0;
        startCount = 0;
        endCount = 0;
        $('.grid-table-rpt').show();
        $('.countryval').text(countryval);
        $('.groupsval').text(groupsval);
        $('.domainval').text(domainName);
        $('.bgroupsval').text(businessgroupsval);
        $('.lentityval').text(legalentityval);
        //loadAssignedStatutoryList(data.unit_wise_assigned_statutories);
        console.log(data)
        assignedStatutoryList = data;
        matchedStatutory = data.unit_groups;
        totalRecord = data.total_count;
        processPaging();
        //loadStatutorySettingReport(data)
      }
    }
    function onFailure(error) {
      hideLoader();
      if (error == "ExportToCSVEmpty") {
          displayMessage(message.empty_export);
      }else {
        displayMessage(error);
      }
    }
    console.log(parseInt(countries), domainsVal, groupid, businessgroupid, lentityid, statutoryid, unitid, complianceid, sno, page_limit);
    mirror.getAssignedStatutoryReport(parseInt(countries), domainsVal, groupid, businessgroupid, lentityid, statutoryval, unitid, complianceid, csv, sno, page_limit, function (error, response) {
      console.log(error, response)
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}

$('#export-button').click(function () {
  csv = true;
  on_current_page = 1;
  sno = 0;
  total_record = 0;
  processSubmit();
});

//pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
}

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
                processSubmit();
            }
        }
    });
};

function processPaging(){
  page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  page_limit;
  }
  sno  = sno;
  //totalRecord = matchedStatutory.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.tbody-assigned-statutory-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-assigned-statutory-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadStatutorySettingReport(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * page_limit);
  console.log(totalRecord,page_limit,recordLength)
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<totalRecord;i++)
  {
    is_null = false;
    data.push(matchedStatutory[i]);
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
  console.log("l:"+data.length)
  return data;
}
function getIdName(id_val, data, mode){
  var idName = null;
  if (mode == "unit"){
    for(var k=0;k<data.length;k++)
    {
      if(id_val == data[k].unit_id)
      {
        idName = data[k].unit_code+' - '+data[k].unit_name+' - '+data[k].address;
      }
    }
  }else{
    for(var k=0;k<data.length;k++)
    {
      if(id_val == data[k].statutory_id)
      {
        idName = data[k].map_text;
      }
    }
  }
  return idName;
}

function loadStatutorySettingReport(data)
{
  $('.grid-table-rpt').show();
  $('#pagination').hide();
  var totalrecords = 0;
  $('.tbody-assigned-statutory-list tr').remove();
  // unit_grp = data;
  unit_grp = assignedStatutoryList.unit_groups;
  act_grp = assignedStatutoryList.act_groups;
  compl_stat_List = assignedStatutoryList.compliance_statutories_list;

  //load header, search details
  var tablefilter = $('#statutory-list .tr-filter');

  $('.countrynameval').text(CountryVal.val());
  $('.groupsval').text(GroupVal.val());
  businessGroup = $('#businessgroupsval').val();
  if (businessGroup == null)
    businessGroup = 'Nil';
  $('.bgroupsval').text(businessGroup);
  $('.lentityval').text($('#legalentityval').val());
  domainName = $('#domainval').val();
  if (domainName == null)
    domainName = 'Nil';
  $('.domainval').text(domainName);

  var tableheading = $('#statutory-list .tr-heading');
  var cloneheading = tableheading.clone();
  $('.tbody-assigned-statutory-list').append(cloneheading);

  unit_names = [];
  act_names = [];
  for (var i=0;i<compl_stat_List.length;i++){
      var occur = -1;
      for(var j=0;j<unit_names.length;j++){
          if(compl_stat_List[i].unit_id == unit_names[j]){
              occur = 1;
              break;
          }
      }
      if(occur < 0){
          unit_names.push(compl_stat_List[i].unit_id);
      }
  }
  for (var i=0;i<compl_stat_List.length;i++){
      var occur = -1;
      for(var j=0;j<act_names.length;j++){
          if(compl_stat_List[i].statutory_mapping_id == act_names[j]){
              occur = 1;
              break;
          }
      }
      if(occur < 0){
          act_names.push(compl_stat_List[i].statutory_mapping_id);
      }
  }
  console.log("1:"+act_names)
  var u_count = 1;
  var sub_cnt = 0;
  for(var i=0;i<unit_names.length;i++){
    var tableRow = $('#unit-details-list .table-unit-details-list .tablerow');
    var clone = tableRow.clone();
    var unitNameAddress = getIdName(unit_names[i], unit_grp, "unit")
    $('.unit-name-address', clone).text(unitNameAddress);
    $('.tbody-assigned-statutory-list').append(clone);
    for (var sm=0;sm<act_names.length;sm++){
      s_count = 1;
      actname = act_names[sm];
      if(getActCount(actname, unit_names[i]) == true){
        var tableRowAssigned = $('#act-heading .tablerow');
        var cloneAssigned = tableRowAssigned.clone();
        var actheading = getIdName(actname, act_grp, "act");
        if (actheading == null){
          console.log("null act:"+actname)
        }
        if(actheading != null && actheading.indexOf("-") >= 0){
          $('.act-name', cloneAssigned).text("Act : "+actheading.split("-")[0]);
        }
        else if(actheading != null){
          $('.act-name', cloneAssigned).text("Act : "+actheading);
        }
        else {
          $('.act-name', cloneAssigned).text("Act : -");
        }
        $('.tbody-assigned-statutory-list').append(cloneAssigned);
        for(var k=0;k<compl_stat_List.length;k++)
        {
          if(unit_names[i] == compl_stat_List[k].unit_id && actname == compl_stat_List[k].statutory_mapping_id)
          {
              sno++;

              var remarks = compl_stat_List[k].remarks;
              if (remarks == null) {
                remarks = 'Nil';
              }
              console.log(sno, remarks)
              var appStatus = compl_stat_List[k].statutory_applicability_status;
              if (appStatus == true) {
                asImageName = '<img src=\'/knowledge/images/tick1bold.png\'>';
              } else {
                asImageName = '<img src=\'/knowledge/images/deletebold.png\' title="'+remarks+'">';
              }

              var optedStatus = compl_stat_List[k].statutory_opted_status;
              if (optedStatus == true) {
                optedImageName = '<img src=\'/knowledge/images/tick-orange.png\'>';
              } else if (optedStatus == false) {
                optedImageName = '<img src=\'/knowledge/images/deletebold.png\' title="'+remarks+'">';
              } else {
                optedImageName = 'Nil';
              }

              var tableRowAssignedRecord = $('#statutory-list .table-statutory-list .tablerow');
              var cloneAssignedRecord = tableRowAssignedRecord.clone();

              $('.sno', cloneAssignedRecord).text(sno);

              var s_provision = "";

              if(actheading != null && actheading.indexOf("-") >= 0){
                s_provision = actheading.split("-")[1] + " - " + compl_stat_List[k].statutory_provision;
              } else if(actheading != null) {
                s_provision = compl_stat_List[k].statutory_provision;
              }
              $('.statutory-provision', cloneAssignedRecord).text(s_provision);

              $('.compliance-task', cloneAssignedRecord).text(compl_stat_List[k].c_task+' - '+compl_stat_List[k].document_name);
              $('.statutory-nature', cloneAssignedRecord).text(compl_stat_List[k].statutory_nature_name);
              $('.applicability-status', cloneAssignedRecord).html(asImageName);
              $('.opted-status', cloneAssignedRecord).html(optedImageName);

              var comp_admin = "";
              var admin_upd = "";
              var cl_admin = "";
              var cl_upd = "";

              console.log(compl_stat_List[k].admin_update)
              if (compl_stat_List[k].compfie_admin != null)
                comp_admin = compl_stat_List[k].compfie_admin;

              if (compl_stat_List[k].admin_update != null)
                  admin_upd = compl_stat_List[k].admin_update;

              $('.compfiedmin', cloneAssignedRecord).text(comp_admin+" "+admin_upd);

              if (compl_stat_List[k].client_admin != null)
                cl_admin = compl_stat_List[k].client_admin;

              if (compl_stat_List[k].client_update != null)
                  cl_upd = compl_stat_List[k].client_update;

              $('.clientadmin', cloneAssignedRecord).text(cl_admin+" "+cl_upd);

              $('.tbody-assigned-statutory-list').append(cloneAssignedRecord);
          }
        }
      }
    }
  }
}

function getActCount(actId, unitId) {
  compl_stat_List = assignedStatutoryList.compliance_statutories_list;
  for (var i=0;i<compl_stat_List.length;i++){
    if(compl_stat_List[i].statutory_mapping_id == actId && compl_stat_List[i].unit_id == unitId) {
      return true;
    }
  }
  return false;
}

function onAutoCompleteSuccess(value_element, id_element, val) {
  console.log(value_element)
  console.log(id_element)
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'country-id'){
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
    else if(current_id == 'statutoryid'){
      resetfilter('act');
    }
}

//Countries---------------------------------------------------------------------------------------------------------------

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
  var textval = $(this).val();
  var ctry_grps=[];
  if($('#country-id').val() > 0)
  {
    for(var i=0;i<groupList.length;i++)
    {
      if(groupList[i].country_id == $('#country-id').val())
      {
        var occur = -1
        for(var j=0;j<ctry_grps.length;j++){
          if(ctry_grps[j].client_id == groupList[i].client_id){
            occur = 1;
            break;
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
      e, ACGroup, Group, textval,
      ctry_grps, "group_name", "client_id", function (val) {
        onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  /*else
  {
    displayMessage(message.country_required);
  }*/
});


//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
  resetfilter('bg');
  var textval = $(this).val();
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
        if(occur < 0){
          bg_grp.push({
            "client_id": businessgroupsList[i].client_id,
            "business_group_id": businessgroupsList[i].business_group_id,
            "business_group_name": businessgroupsList[i].business_group_name
          });
        }
      }
    }
    console.log(bg_grp.length)
    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroup, textval,
      bg_grp, "business_group_name", "business_group_id", function (val) {
        onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
    }, condition_fields, condition_values);
  }
  /*else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/

});

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
  resetfilter('le');
  var textval = $(this).val();
  var le_list = [];
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
      if($('#group-id').val() == businessgroupsList[i].client_id)
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
            "legal_entity_id": businessgroupsList[i].legal_entity_id,
            "legal_entity_name": businessgroupsList[i].legal_entity_name
          });
        }
      }
    }
    commonAutoComplete(
      e, ACLegalEntity, LegalEntity, textval,
      le_list, "legal_entity_name", "legal_entity_id", function (val) {
          onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
      }, condition_fields, condition_values);
  }
  /*else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/
});


//load unit with conditionform list in autocomplete text box
$('#unitval').keyup(function (e) {
  resetfilter('unit');
  var text_val = $(this).val();
  var unit_list = [];
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      if(unitList[i].client_id == $('#group-id').val() &&
        unitList[i].legal_entity_id == $('#legalentityid').val())
      {
        var occur = -1;
        for(var u=0;u<unit_list.length;u++){
          if(unit_list[u].unit_id == unitList[i].unit_id){
            occur = 1;
            break;
          }
        }
        if(occur < 0){
          unit_list.push({
            "unit_id": unitList[i].unit_id,
            "unit_name": unitList[i].unit_code+"-"+unitList[i].unit_name,
          });
        }
      }
    }
    console.log("unit:"+unit_list)
    commonAutoComplete(
      e, ACUnit, Unit, text_val,
      unit_list, "unit_name", "unit_id", function (val) {
        onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }
  /*else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/
});


//load domain list in autocomplete textbox
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
  resetfilter('domian');
  var text_val = $(this).val();
  var domain_list = [];
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<domain_compl_stat_List.length;i++)
    {
      if($('#group-id').val() == domain_compl_stat_List[i].client_id &&
        $('#legalentityid').val() == domain_compl_stat_List[i].legal_entity_id)
      {
        if($('#unitid').val() > 0 && domain_compl_stat_List[i].unit_id == $('#unitid').val())
        {
          for(var j=0;j<domainsList.length;j++)
          {
            if(domainsList[j].domain_id == domain_compl_stat_List[i].domain_id)
            {
              var occur = -1;
              for(var d=0;d<domain_list.length;d++){
                if(domainsList[j].domain_id == domain_list[d].domain_id){
                  occur = 1;
                  break;
                }
              }
              if(occur < 0){
                domain_list.push({
                  "domain_id": domainsList[j].domain_id,
                  "domain_name": domainsList[j].domain_name,
                  "is_active": domainsList[j].is_active
                });
              }
            }
          }
        }
        else
        {
          for(var j=0;j<domainsList.length;j++)
          {
            if(domainsList[j].domain_id == domain_compl_stat_List[i].domain_id)
            {
              var occur = -1;
              for(var d=0;d<domain_list.length;d++){
                if(domainsList[j].domain_id == domain_list[d].domain_id){
                  occur = 1;
                  break;
                }
              }
              if(occur < 0){
                domain_list.push({
                  "domain_id": domainsList[j].domain_id,
                  "domain_name": domainsList[j].domain_name,
                  "is_active": domainsList[j].is_active
                });
              }
            }
          }
        }
      }
    }
    commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domain_list, "domain_name", "domain_id", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    });
  }
  /*else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/
});


//load statutory list in autocomplete textbox
$('#statutoryval').keyup(function (e) {
  resetfilter('act');
  var textval = $(this).val();
  var act_list = [];
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<domain_compl_stat_List.length;i++)
    {
      var unit_check = true;
      if($('#unitid').val()>0 && ($('#unitid').val() != domain_compl_stat_List[i].unit_id)){
        unit_check =false;
      }
      var domain_check = true;
      if($('#domain').val()>0 && ($('#domain').val() != domain_compl_stat_List[i].domain_id)){
        domain_check =false;
      }
      if($('#group-id').val() == domain_compl_stat_List[i].client_id &&
        $('#legalentityid').val() == domain_compl_stat_List[i].legal_entity_id &&
        unit_check == true && domain_check == true)
      {
        console.log("inside act")
        var occur = -1;
        for(var s=0;s<act_list.length;s++){
          if(act_list[s].statutory_id == domain_compl_stat_List[i].statutory_id){
            occur = 1;
            break;
          }
        }
        if(occur < 0){
          act_list.push({
            "statutory_id": domain_compl_stat_List[i].statutory_id,
            "statutory_name": domain_compl_stat_List[i].statutory_name
          });
        }
      }
    }
    commonAutoComplete(
    e, ACAct, Act, textval,
    act_list, "statutory_name", "statutory_id", function (val) {
        onAutoCompleteSuccess(ActVal, Act, val);
    });
  }
  /*else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/
});


//load division form list in autocomplete text box
$('#compliance-task').keyup(function (e) {
  console.log("inside compl task")
  var textval = $(this).val();
  var compl_task_list = [];
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<domain_compl_stat_List.length;i++)
    {
      var unit_check = true;
      if($('#unitid').val()>0 && ($('#unitid').val() != domain_compl_stat_List[i].unit_id)){
        unit_check =false;
      }
      var domain_check = true;
      if($('#domain').val()>0 && ($('#domain').val() != domain_compl_stat_List[i].domain_id)){
        domain_check =false;
      }
      if($('#group-id').val() == domain_compl_stat_List[i].client_id &&
        $('#legalentityid').val() == domain_compl_stat_List[i].legal_entity_id
        && unit_check == true && domain_check == true)
      {
        var occur = -1;
        for(var c=0;c<compl_task_list.length;c++){
          if(compl_task_list[c].compliance_id == domain_compl_stat_List[i].compliance_id){
            occur = 1;
            break;
          }
        }
        if(occur < 0){
          compl_task_list.push({
            "compliance_id": domain_compl_stat_List[i].compliance_id,
            "compliance_name": domain_compl_stat_List[i].c_task+" - "+domain_compl_stat_List[i].document_name
          });
        }
      }
    }
    console.log("list:"+compl_task_list)
    commonAutoComplete(
    e, ACCompltask, CTask, textval,
    compl_task_list, "compliance_name", "compliance_id", function (val) {
        onAutoCompleteSuccess(CTaskVal, CTask, val);
    });
  }
  /*else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }*/
});


function resetAllfilter()
{
  $('#countryval').val('');
  $('#country-id').val('');
  $('#groupsval').val('');
  $('#group-id').val('')
  $('#businessgroupsval').val('');
  $('#businessgroupid').val('');
  $('#legalentityval').val('');
  $('#legalentityid').val('');
  $('#unitval').val('');
  $('#unitid').val('');
  $('#domainval').val('');
  $('#domainid').val('');
  $('#statutoryval').val('');
  $('#statutoryid').val('');
  $('#compliance-task').val('');
  $('#complianceid').val('');
  $('#countryval').focus();
}
function resetfilter(evt)
{
  //alert("jhjh");'
  console.log(evt);
  if(evt == 'countries')
  {
    $('#groupsval').val('');
    $('#group-id').val('')
    $('#businessgroupsval').val('');
    $('#businessgroupid').val('');
    $('#legalentityval').val('');
    $('#legalentityid').val('');
    $('#unitval').val('');
    $('#unitid').val('');
    $('#domainval').val('');
    $('#domainid').val('');
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'clients')
  {
    $('#businessgroupsval').val('');
    $('#businessgroupid').val('');
    $('#legalentityval').val('');
    $('#legalentityid').val('');
    $('#unitval').val('');
    $('#unitid').val('');
    $('#domainval').val('');
    $('#domainid').val('');
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'bg')
  {
    $('#legalentityval').val('');
    $('#legalentityid').val('');
    $('#unitval').val('');
    $('#unitid').val('');
    $('#domainval').val('');
    $('#domainid').val('');
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'le')
  {
    $('#unitval').val('');
    $('#unitid').val('');
    $('#domainval').val('');
    $('#domainid').val('');
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'unit')
  {
    $('#domainval').val('');
    $('#domainid').val('');
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'domian')
  {
    $('#statutoryval').val('');
    $('#statutoryid').val('');
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
  if(evt == 'act')
  {
    $('#compliance-task').val('');
    $('#complianceid').val('');
  }
}

$(function () {
  // $( "#accordion" ).accordion({
  //  heightStyle: "content"
  // });
  initialize();
   ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processSubmit();
  });
  loadItemsPerPage();
});


