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
  mirror.getAssignedStatutoryReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

$('#show-button').click(function () {
  on_current_page = 1;
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
    }
  } else {
    var statutoryid = 0;
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
    displayMessage(message.legal_entity_required);
    $('.grid-table-rpt').hide();
  } else {
    displayLoader();
    function onSuccess(data) {
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
      totalRecord = data.unit_groups.length;
      processPaging();
      //loadStatutorySettingReport(data)
    }
    function onFailure(error) {
      hideLoader();
      displayMessage(error);
    }
    console.log(parseInt(countries), domainsVal, groupid, businessgroupid, lentityid, statutoryid, unitid, complianceid);
    //countryId, domainId,  clientId, businessGroupId, legalEntityId, divisionId, unitId, level1StatutoryId, applicableStatus,
    mirror.getAssignedStatutoryReport(parseInt(countries), domainsVal, groupid, businessgroupid, lentityid, statutoryid, unitid, complianceid, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
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
  totalRecord = matchedStatutory.length;
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
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  console.log(totalRecord,_page_limit)
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<matchedStatutory.length;i++)
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
  return data;
}

function loadStatutorySettingReport(data)
{
  var sno = 0;
  $('.grid-table-rpt').show();
  $('#pagination').hide();
  var totalrecords = 0;
  $('.tbody-assigned-statutory-list tr').remove();
  unit_grp = data;
  main_unit_grp = assignedStatutoryList.unit_groups;
  act_grp = assignedStatutoryList.act_groups;
  compl_stat_List = assignedStatutoryList.compliance_statutories_list;

  //load header, search details
  var tablefilter = $('#statutory-list .tr-filter');

  $('.countryval').text($('#countryval').val());
  $('.groupsval').text($('#groupsval').val());
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

  for(var i=0;i<unit_grp.length;i++)
  {
    var tableRow = $('#unit-details-list .table-unit-details-list .tablerow');
    var clone = tableRow.clone();
    var unitNameAddress = unit_grp[i].unit_code+' - '+unit_grp[i].unit_name+' - '+unit_grp[i].address;
    $('.unit-name-address', clone).text(unitNameAddress);
    $('.tbody-assigned-statutory-list').append(clone);
    //act loop
    for(var j=0;j<act_grp.length;j++)
    {
      if(act_grp[j].unit_id == unit_grp[i].unit_id)
      {
        var tableRowAssigned = $('#act-heading .table-act-heading-list .tablerow');
        var cloneAssigned = tableRowAssigned.clone();
        var actheading = "Act : "+act_grp[j].statutory_name;
        $('.heading', cloneAssigned).text(actheading);
        $('.tbody-assigned-statutory-list').append(cloneAssigned);
        for(var k=0;k<compl_stat_List.length;k++)
        {
          if(unit_grp[i].unit_id == compl_stat_List[k].unit_id && act_grp[j].statutory_id == compl_stat_List[k].statutory_id)
          {
            sno++;
            var remarks = compl_stat_List[k].remarks;
            if (remarks == null) {
              remarks = 'Nil';
            }
            var appStatus = compl_stat_List[k].statutory_applicability_status;
            if (appStatus == true) {
              asImageName = '<img src=\'/knowledge/images/tick1bold.png\'>';
            } else {
              asImageName = '<img src=\'/knowledge/images/deletebold.png\' title='+remarks+'>';
            }
            var optedStatus = compl_stat_List[k].statutory_opted_status;
            if (optedStatus == true) {
              optedImageName = '<img src=\'/knowledge/images/tick-orange.png\'>';
            } else if (optedStatus == false) {
              optedImageName = '<img src=\'/knowledge/images/deletebold.png\' title='+remarks+'>';
            } else {
              optedImageName = 'Nil';
            }

            var tableRowAssignedRecord = $('#statutory-list .table-statutory-list .tablerow');
            var cloneAssignedRecord = tableRowAssignedRecord.clone();
            $('.sno', cloneAssignedRecord).text(sno);
            $('.statutory-provision', cloneAssignedRecord).text(compl_stat_List[k].statutory_provision);
            $('.compliance-task', cloneAssignedRecord).text(compl_stat_List[k].c_task+' - '+compl_stat_List[k].document_name);
            $('.statutory-nature', cloneAssignedRecord).text(compl_stat_List[k].statutory_nature_name);
            $('.applicability-status', cloneAssignedRecord).html(asImageName);
            $('.opted-status', cloneAssignedRecord).html(optedImageName);
            $('.compfiedmin', cloneAssignedRecord).text(compl_stat_List[k].compfie_admin+" "+compl_stat_List[k].admin_update);
            $('.clientadmin', cloneAssignedRecord).text(compl_stat_List[k].client_admin+" "+compl_stat_List[k].client_update);
            $('.tbody-assigned-statutory-list').append(cloneAssignedRecord);
          }
        }
      }
    }
  }
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
  var text_val = $(this).val();
  commonAutoComplete(
    e, ACCountry, Country, text_val,
    countriesList, "country_name", "country_id", function (val) {
      onAutoCompleteSuccess(CountryVal, Country, val);
  });
});

//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  var textval = $(this).val();
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
        e, ACGroup, Group, textval,
        ctry_grps, "group_name", "client_id", function (val) {
          onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  else
  {
    displayMessage(message.country_required);
  }
});


//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
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
        bg_grp.push({
            "client_id": businessgroupsList[i].client_id,
            "business_group_id": businessgroupsList[i].business_group_id,
            "business_group_name": businessgroupsList[i].business_group_name
        });
      }
    }
    console.log(bg_grp.length)
    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroupVal, textval,
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

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
  var textval = $(this).val();
  var le_list = [];
  if($('#group-id').val() > 0)
  {
    for(var i=0;i<businessgroupsList.length;i++)
    {
      var condition_fields = [];
      var condition_values = [];
      if(Group.val() != ''){
        condition_fields.push("client_id");
        condition_values.push(Group.val());
      }

      if($('#group-id').val() == businessgroupsList[i].client_id)
      {
        le_list.push({
          "client_id": businessgroupsList[i].client_id,
          "legal_entity_id": businessgroupsList[i].legal_entity_id,
          "legal_entity_name": businessgroupsList[i].legal_entity_name
        });
      }
    }
    commonAutoComplete(
      e, ACLegalEntity, LegalEntity, textval,
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


//load unit with conditionform list in autocomplete text box
$('#unitval').keyup(function (e) {
  var text_val = $(this).val();
  var unit_list = [];
  console.log(textval)
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<unitList.length;i++)
    {
      if(unitList[i].client_id == $('#group-id').val() &&
        unitList[i].legal_entity_id == $('#legalentityid').val())
      {
        unit_list.push({
          "unit_id": unitList[i].unit_id,
          "unit_name": unitList[i].unit_code+"-"+unitList[i].unit_name,
        });
      }
    }
    console.log("unit:"+unit_list)
    commonAutoComplete(
      e, ACUnit, Unit, text_val,
      unit_list, "unit_id", "unit_name", function (val) {
        onAutoCompleteSuccess(UnitVal, Unit, val);
    });
  }
  else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});


//load domain list in autocomplete textbox
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
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
              domain_list.push({
                "domain_id": domainsList[j].domain_id,
                "domain_name": domainsList[j].domain_name,
                "is_active": domainsList[j].is_active
              });
            }
          }
        }
        else
        {
          for(var j=0;j<domainsList.length;j++)
          {
            if(domainsList[j].domain_id == domain_compl_stat_List[i].domain_id)
            {
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
    commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domain_list, "domain_id", "domain_name", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    });
  }
  else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});


//load statutory list in autocomplete textbox
$('#statutoryval').keyup(function (e) {
  var textval = $(this).val();
  var act_list = [];
  if($('#group-id').val() > 0 && $('#legalentityid').val() > 0)
  {
    for(var i=0;i<domain_compl_stat_List.length;i++)
    {
      var unit_check = $('#unitid').val()>0?($('#unitid').val() == domain_compl_stat_List[i].unit_id):false;
      var domain_check = $('#domain').val()>0?($('#domain').val() === domain_compl_stat_List[i].domain_id):false;
      if($('#group-id').val() == domain_compl_stat_List[i].client_id &&
        $('#legalentityid').val() == domain_compl_stat_List[i].legal_entity_id &&
        (unit_check == true || unit_check == false) && (domain_check == true || domain_check == false))
      {
        console.log("inside act")
        act_list.push({
          "statutory_id": domain_compl_stat_List[i].statutory_id,
          "statutory_name": domain_compl_stat_List[i].statutory_name
        });
      }
    }
    commonAutoComplete(
    e, ACAct, Act, textval,
    act_list, "statutory_id", "statutory_name", function (val) {
        onAutoCompleteSuccess(ActVal, Act, val);
    });
  }
  else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
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
      var unit_check = $('#unitid').val()>0?($('#unitid').val() === domain_compl_stat_List[i].unit_id):false;
      console.log("unit check:"+unit_check)
      var domain_check = $('#domain').val()>0?($('#domain').val() === domain_compl_stat_List[i].domain_id):false;
      console.log("domain check:"+domain_check)

      if($('#group-id').val() == domain_compl_stat_List[i].client_id &&
        $('#legalentityid').val() == domain_compl_stat_List[i].legal_entity_id
        && (unit_check == true || unit_check == false) && (domain_check == true || domain_check == false))
      {
        compl_task_list.push({
          "compliance_id": domain_compl_stat_List[i].compliance_id,
          "compliance_name": domain_compl_stat_List[i].c_task+" - "+domain_compl_stat_List[i].document_name
        });
      }
    }
    console.log("list:"+compl_task_list)
    commonAutoComplete(
    e, ACCompltask, CTask, textval,
    compl_task_list, "compliance_id", "compliance_name", function (val) {
        onAutoCompleteSuccess(CTaskVal, CTask, val);
    });
  }
  else
  {
    if($('#legalentityid').val() == 0)
    {
     displayMessage(message.legal_entity_required);
    }
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
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
  $('#statutoryval').val('');
  $('#compliance-task').val('');
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
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'clients')
  {
    $('#businessgroupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'bg')
  {
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('#domainval').val('');
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'le')
  {
    $('#unitval').val('');
    $('#domainval').val('');
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'unit')
  {
    $('#domainval').val('');
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'domian')
  {
    $('#statutoryval').val('');
    $('#compliance-task').val('');
  }
  if(evt == 'act')
  {
    $('#compliance-task').val('');
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
      processPaging();
  });
  loadItemsPerPage();
});