var assignedStatutoriesList;
//var countriesList;
var groupcompaniesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var geographyLevelsList;
var geographiesList;
var industriesList;
var domainsList;
var unitsList;

var assignStatutoryCountryId = 0;
var assignStatutoryCountryValue = null;
var assignStatutoryGroupId = 0;
var assignStatutoryGroupValue = null;
var assignStatutoryBusinessGroupId = 0;
var assignStatutoryBusinessGroupValue = null;
var assignStatutoryLegalEntityId = 0;
var assignStatutoryLegalEntityValue = null;
var assignStatutoryDivisionId = 0;
var assignStatutoryDivisionValue = null;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];
var assignStatutoryDomainIds = [];
var assignStatutoryDomainId = 0;
var assignStatutoryDomainValue = null;
var assignStatutoryIndustryId = 0;
var assignStatutoryIndustryValue = null;
var assignStatutoryLocationId = 0;
var assignStatutoryLocationValue = null;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$("#geographylevel").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryGeographyLevelId = parseInt(event.target.id);
  assignStatutoryGeographyLevelValue = $(event.target).text();
  $('#location').empty();
  for(var geography in geographiesList[assignStatutoryCountryId]){
    if(geographiesList[assignStatutoryCountryId][geography]["is_active"] == true && geographiesList[assignStatutoryCountryId][geography]["level_id"] == assignStatutoryGeographyLevelId){
      str += '<li id="'+geographiesList[assignStatutoryCountryId][geography]["geography_id"]+'" class="locationlist"><span class="filter2_name">'+geographiesList[assignStatutoryCountryId][geography]["geography_name"]+'</span></li>';
    }
  }
  $('#location').append(str);
});

$("#group").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryGroupId = parseInt(event.target.id);
  assignStatutoryGroupValue = $(event.target).text();
  $('#businessgroup').empty();
  for(var businessgroup in businessgroupsList){
    if(businessgroupsList[businessgroup]["client_id"] == assignStatutoryGroupId){
      str += '<li id="'+businessgroupsList[businessgroup]["business_group_id"]+'" class="businessgrouplist" ><span class="filter2_name">'+businessgroupsList[businessgroup]["business_group_name"]+'</span></li>';
    }
  }
  $('#businessgroup').append(str); 

  var str1='';
  $('#legalentity').empty();
  for(var legalentity in legalentitiesList){
    if(legalentitiesList[legalentity]["client_id"] == assignStatutoryGroupId && legalentitiesList[legalentity]["business_group_id"] == null){
      str1 += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" ><span class="filter2_name">'+legalentitiesList[legalentity]["legal_entity_name"]+'</span></li>';
    }
  }
  $('#legalentity').append(str1);

});


$("#businessgroup").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryBusinessGroupId = parseInt(event.target.id);
  assignStatutoryBusinessGroupValue = $(event.target).text();
  $('#legalentity').empty();
  for(var legalentity in legalentitiesList){
    if(legalentitiesList[legalentity]["client_id"] == assignStatutoryGroupId && legalentitiesList[legalentity]["business_group_id"] == assignStatutoryBusinessGroupId){
      str += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" ><span class="filter2_name">'+legalentitiesList[legalentity]["legal_entity_name"]+'</span></li>';
    }
  }
  $('#legalentity').append(str);
});

$("#legalentity").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryLegalEntityId = parseInt(event.target.id);
  assignStatutoryLegalEntityValue = $(event.target).text();
  $('#division').empty();
  for(var division in divisionsList){
    if(divisionsList[division]["client_id"] == assignStatutoryGroupId && divisionsList[division]["legal_entity_id"] == assignStatutoryLegalEntityId){
      str += '<li id="'+divisionsList[division]["division_id"]+'" class="divisionlist" ><span class="filter2_name">'+divisionsList[division]["division_name"]+'</span></li>';
    }
  }
  $('#division').append(str);
});

$("#division").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryDivisionId = parseInt(event.target.id);
  assignStatutoryDivisionValue = $(event.target).text();
});

$("#location").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryLocationId = parseInt(event.target.id);
  assignStatutoryLocationValue = $(event.target).text();
});

$("#industry").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryIndustryId = parseInt(event.target.id);
  assignStatutoryIndustryValue = $(event.target).text();
  
  if(assignStatutoryDivisionId == 0){
    var str='';
    $('#unit').empty();
    for(var unit in unitsList){
      if(unitsList[unit]["division_id"] == null && unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && unitsList[unit]["client_id"] == assignStatutoryGroupId && unitsList[unit]["industry_id"] == assignStatutoryIndustryId && $.inArray(assignStatutoryLocationId, unitsList[unit]["geography_ids"]) >= 0){
        str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" ><span class="filter2_name">'+unitsList[unit]["unit_name"]+'</span></li>';
      }
    }
    $('#unit').append(str);
  }else{
    var str='';
    $('#unit').empty();
    for(var unit in unitsList){
      if(unitsList[unit]["division_id"] == assignStatutoryDivisionId && unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && unitsList[unit]["client_id"] == assignStatutoryGroupId && unitsList[unit]["industry_id"] == assignStatutoryIndustryId && $.inArray(assignStatutoryLocationId, unitsList[unit]["geography_ids"]) >= 0){
        str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" ><span class="filter2_name">'+unitsList[unit]["unit_name"]+'</span></li>';
      }
    }
    $('#unit').append(str);
  }
});


$("#unit").click(function(event){

  var chkstatus = $(event.target).attr('class');
  if(chkstatus == 'unitlist active'){
    $(event.target).removeClass("active");
    var removeid = assignStatutoryUnitIds.indexOf(event.target.id);
    assignStatutoryUnitIds.splice(removeid,1);
    var removename = assignStatutoryUnitValues.indexOf($(event.target).text());
    assignStatutoryUnitValues.splice(removename,1);
  }else{
    $(event.target).addClass("active");
    assignStatutoryUnitIds.push(parseInt(event.target.id));
    assignStatutoryUnitValues.push($(event.target).text());
  }
  
  var domainArray = [];
  for(var unit in unitsList){
    if($.inArray(unitsList[unit]["unit_id"], assignStatutoryUnitIds) >= 0){
      domainArray.push(unitsList[unit]["domain_ids"]);
    }
  }
  
  if(domainArray.length > 0){
    var applicableDomains = domainArray.shift().filter(function(v) {
    return domainArray.every(function(a) {
        return a.indexOf(v) !== -1;
    });
  });

  var str=''; 
  $('#domain').empty();
  for(var domain in domainsList){
    if(domainsList[domain]["is_active"] == true && $.inArray(domainsList[domain]["domain_id"], applicableDomains) >= 0){
      str += '<li id="'+domainsList[domain]["domain_id"]+'" class="domainlist" ><span class="filter2_name">'+domainsList[domain]["domain_name"]+'</span></li>';
    }
  }
  $('#domain').append(str);
  }else{
     $('#domain').empty();
  }
});

$("#domain").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryDomainId = parseInt(event.target.id);
  assignStatutoryDomainValue = $(event.target).text();
  
});

function load_firstwizard(){

  var str='';
  $('#group').empty();
  for(var group in groupcompaniesList){
    if(groupcompaniesList[group]["is_active"] == true && $.inArray(assignStatutoryCountryId, groupcompaniesList[group]["country_ids"]) >= 0){
      str += '<li id="'+groupcompaniesList[group]["client_id"]+'" class="grouplist"><span class="filter2_name">'+groupcompaniesList[group]["group_name"]+'</span></li>';
    }
  }
  $('#group').append(str);
   
  var str1='';
  $('#geographylevel').empty();
  for(var geographylevel in geographyLevelsList[assignStatutoryCountryId]){
    str1 += '<li id="'+geographyLevelsList[assignStatutoryCountryId][geographylevel]["level_id"]+'" class="geographylevellist"><span class="filter2_name">'+geographyLevelsList[assignStatutoryCountryId][geographylevel]["level_name"]+'</span></li>';
  }
  $('#geographylevel').append(str1);

  var str2='';
  $('#industry').empty();
  for(var industry in industriesList){
    if(industriesList[industry]["is_active"] == true){
      str2 += '<li id="'+industriesList[industry]["industry_id"]+'" class="industrylist"><span class="filter2_name">'+industriesList[industry]["industry_name"]+'</span></li>';
    }
  }
  $('#industry').append(str2);
}

$("#country").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryCountryId = parseInt(event.target.id);
  assignStatutoryCountryValue = $(event.target).text();

  function onSuccess(data){
  //countriesList = data["countries"];
  groupcompaniesList = data["group_companies"];
  businessgroupsList = data["business_groups"];
  legalentitiesList = data["legal_entities"];
  divisionsList = data["divisions"];
  geographyLevelsList = data["geography_levels"];
  geographiesList = data["geographies"];
  industriesList = data["industries"];
  domainsList = data["domains"];
  unitsList = data["units"];
  load_firstwizard();
}
function onFailure(error){
}
mirror.getAssignStatutoryWizardOne(assignStatutoryCountryId,
  function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
    }
);
});

/*
if(sm_countryid != '' && sm_domainid !=''){
  loadStatutoryLevels(sm_countryid,sm_domainid);
}
if(sm_countryid != ''){
  loadGeographyLevels(sm_countryid);
}
make_breadcrumbs();*/
  
function loadCountriesList(data){
  var countriesList = data["countries"];
  var str='';
  $('#country').empty();
    for(var country in countriesList){
      if(countriesList[country]["is_active"] == true){
      str += '<li id="'+countriesList[country]["country_id"]+'" class="countrylist"  ><span class="filter1_name">'+countriesList[country]["country_name"]+'</span></li>';
    }
  }
  $('#country').append(str);
}

$(".btn-assignstatutory-add").click(function(){
$("#assignstatutory-view").hide();
$("#assignstatutory-add").show();
$("#edit_assignstatutory_id").val('');
displayMessage('');

function onSuccess(data){
  loadCountriesList(data);
}
function onFailure(error){
  displayMessage(error);
}
mirror.getCountryList(
  function (error, response) {
          if (error == null){
              onSuccess(response);
          }
          else {
              onFailure(error);
          }
      }
);
/*sm_countryid='';
sm_domainid='';
sm_statutorynatureid='';
sm_countryval='';
sm_domainval='';
sm_statutorynatureval='';
sm_statutoryids=[];
compliances = [];
load_selectdomain_master();
$(".tbody-statutory-list").find("tr").remove();
$(".tbody-compliance-list").find("tr").remove();*/
/*$(".tbody-statutory-level").find("div").remove();
$(".tbody-geography-level").find("div").remove();*/
});

function validate_firsttab(){
  /*if(sm_countryid == ''){
    displayMessage("Country Required");
  }else if (sm_domainid == ''){
    displayMessage("Domain Required");
  }else if (sm_industryids.length == 0){
    displayMessage("Industry Required");
  }else if (sm_statutorynatureid == ''){
    displayMessage("Statutory Nature Required");
  }else{
    displayMessage("");
    return true;
  }*/
  return true;
}

var navListItems = $('ul.setup-panel li a'),
allWells = $('.setup-content');
allWells.hide();
navListItems.click(function(e)
{
e.preventDefault();
var $target = $($(this).attr('href')),
$item = $(this).closest('li');
if (!$item.hasClass('disabled')) {
navListItems.closest('li').removeClass('active');
$item.addClass('active');
allWells.hide();
$target.show();
}
});
$('ul.setup-panel li.active a').trigger('click');
$('#activate-step-2').on('click', function(e) {
if (validate_firsttab()){
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-2"]').trigger('click');
}
})
$('#backward-step-1').on('click', function(e) {
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-1"]').trigger('click');

})
$('#activate-step-finish').on('click', function(e) {
/*getGeographyResult();
if (validate_fourthtab()){
savestatutorymapping();
}*/
})

function loadAssignedStatutoriesList(assignedStatutoriesList){
  var j = 1;
  var client_saved_statutory_id = 0;
  var client_assigned_statutory_id = 0;
  $(".tbody-assignstatutory-list").find("tr").remove();
    for(var entity in assignedStatutoriesList) {
      client_saved_statutory_id = assignedStatutoriesList[entity]["client_saved_statutory_id"];
      client_assigned_statutory_id = assignedStatutoriesList[entity]["client_assigned_statutory_id"];
      
      var tableRow=$('#templates .table-assignstatutory .table-row');
      var clone=tableRow.clone();
      $('.tbl_sno', clone).text(j);
      $('.tbl_country', clone).text(assignedStatutoriesList[entity]["country_name"]);
      $('.tbl_group', clone).text(assignedStatutoriesList[entity]["group_name"]);
      $('.tbl_businessgroup', clone).text(assignedStatutoriesList[entity]["business_group_name"]);
      $('.tbl_legalentity', clone).text(assignedStatutoriesList[entity]["legal_entity_name"]);
      $('.tbl_division', clone).text(assignedStatutoriesList[entity]["division_name"]);
      $('.tbl_location', clone).text(assignedStatutoriesList[entity]["geography_name"]);
      $('.tbl_industry', clone).text(assignedStatutoriesList[entity]["industry_name"]);
      $('.tbl_unit', clone).text(assignedStatutoriesList[entity]["unit_name"]);
      $('.tbl_domain', clone).text(assignedStatutoriesList[entity]["domain_name"]);
      $('.tbl_status', clone).text(assignedStatutoriesList[entity]["submission_status"]);

      $('.tbl_edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+client_saved_statutory_id+')"/>');
      $('.tbl_view', clone).html('<img src=\'/images/icon-viewsubmit.png\' onclick="changeStatus('+client_saved_statutory_id+')"/>');
      $('.tbody-assignstatutory-list').append(clone);
      j = j + 1;
    }
}

function getAssignedStatutories () {

  /*function onSuccess(data){
  assignedStatutoriesList = data["assigned_statutories"];
  loadAssignedStatutoriesList(assignedStatutoriesList);
  }
  function onFailure(error){
  }
  mirror.getAssignedStatutoriesList(
    function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
  );*/


      assignedStatutoriesList = [
      {
        "submission_status": "Pending",
        "client_saved_statutory_id": 1,
        "client_assigned_statutory_id": 1,
        "country_name" : "India",
        "group_name" : "India Group",
        "business_group_name" : "India Business Group",
        "legal_entity_name" : "India Legal Entity",
        "industry_name" : "India Industry",
        "division_name" : "India Division",
        "unit_name": "IND - TN",
        "geography_name" : "Tamilnadu",
        "domain_name": "India Domain"
      }, 
      {
        "submission_status": "Submitted",
        "client_saved_statutory_id": 2,
        "client_assigned_statutory_id": 2,
        "country_name" : "Singapore",
        "group_name" : "Singapore Group",
        "business_group_name" : "Singapore Business Group",
        "legal_entity_name" : "Singapore Legal Entity",
        "industry_name" : "Singapore Industry",
        "division_name" : "Singapore Division",
        "unit_name": "IND - TN",
        "geography_name" : "Tamilnadu",
        "domain_name": "Singapore Domain"
      }
    ];

    /* countriesList =  [
      {
        "country_name": "India", 
        "is_active": true, 
        "country_id": 1
      }, 
      {
        "country_name": "United States", 
        "is_active": true, 
        "country_id": 2
      }, 
      {
        "country_name": "Sri Lanka", 
        "is_active": true, 
        "country_id": 3
      }, 
      {
        "country_name": "test country", 
        "is_active": true, 
        "country_id": 4
      }
    ];

    domainsList =  [
      {
        "is_active": true, 
        "domain_id": 1, 
        "domain_name": "Finance Law"
      }, 
      {
        "is_active": true, 
        "domain_id": 2, 
        "domain_name": "Industry Law"
      }, 
      {
        "is_active": true, 
        "domain_id": 4, 
        "domain_name": "test domain2"
      }
    ];


    groupcompaniesList = [
    {
        "country_ids":[1],
        "is_active":true,
        "domain_ids":"1",
        "client_id":2,
        "group_name":"Client Test Group 1"
    },
    {
        "country_ids":[1],
        "is_active":true,
        "domain_ids":"1",
        "client_id":7,
        "group_name":"Client Test Group 21 Update"
    },
    {
        "country_ids":[1,2],
        "is_active":true,
        "domain_ids":"1,2",
        "client_id":11,
        "group_name":"Test Client 1"
    },
    {
        "country_ids":[1,2],
        "is_active":true,
        "domain_ids":"1,2",
        "client_id":12,
        "group_name":"Test Client 2"
    },
    {
        "country_ids":[1,2],
        "is_active":true,
        "domain_ids":"1,2",
        "client_id":13,
        "group_name":"Test Client 21"
    }

];

businessgroupsList = [

    {
        "business_group_id":1,
        "client_id":2,
        "business_group_name":"Test Business Group 1"
    }

];

legalentitiesList = [

    {
        "legal_entity_id":1,
        "business_group_id":1,
        "legal_entity_name":"Test Legal entity",
        "client_id":2
    },
    {
        "legal_entity_id":2,
        "business_group_id":null,
        "legal_entity_name":"Test Legal entity without BG",
        "client_id":2
    }

];

divisionsList = [

    {
        "division_id":1,
        "division_name":"Test Division",
        "legal_entity_id":1,
        "business_group_id":1,
        "client_id":2
    }

];

unitsList = [

    {
        "division_id":1,
        "unit_name":"Test Unit 1",
        "business_group_id":1,
        "client_id":2,
        "unit_code":"TU001",
        "legal_entity_id":1,
        "unit_address":"Test Address 1",
        "is_active":true,
        "unit_id":1
    },
    {
        "division_id":null,
        "unit_name":"Test Unit 2",
        "business_group_id":1,
        "client_id":2,
        "unit_code":"TU002",
        "legal_entity_id":1,
        "unit_address":"Test Address 2",
        "is_active":true,
        "unit_id":2
    }

];*/

  loadAssignedStatutoriesList(assignedStatutoriesList);
}


$(".listfilter").keyup(function() {
  var filter1 = $("#filter1").val().toLowerCase();
  var filter2 = $("#filter2").val().toLowerCase();
  var filter3 = $("#filter3").val().toLowerCase();
  var filter4 = $("#filter4").val().toLowerCase();
  var filter5 = $("#filter5").val().toLowerCase();
  var filter6 = $("#filter6").val().toLowerCase();
  var filter7 = $("#filter7").val().toLowerCase();
  var filter8 = $("#filter8").val().toLowerCase();
  var filter9 = $("#filter9").val().toLowerCase();
  var filter10 = $("#filter10").val().toLowerCase();
 
  var filteredList=[];
  for(var entity in assignedStatutoriesList) {
    var filter1val = assignedStatutoriesList[entity]["country_name"];
    var filter2val = assignedStatutoriesList[entity]["group_name"];
    var filter3val = assignedStatutoriesList[entity]["business_group_name"];
    var filter4val = assignedStatutoriesList[entity]["legal_entity_name"];
    var filter5val = assignedStatutoriesList[entity]["division_name"];
    var filter6val = assignedStatutoriesList[entity]["geography_name"];
    var filter7val = assignedStatutoriesList[entity]["industry_name"];
    var filter8val = assignedStatutoriesList[entity]["unit_name"];
    var filter9val = assignedStatutoriesList[entity]["domain_name"];
    var filter10val = assignedStatutoriesList[entity]["submission_status"];
    
    if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6) && ~filter7val.toLowerCase().indexOf(filter7) && ~filter8val.toLowerCase().indexOf(filter8) && ~filter9val.toLowerCase().indexOf(filter9) && ~filter10val.toLowerCase().indexOf(filter10)) 
    {
      filteredList.push(assignedStatutoriesList[entity]);
    }   
  }
  loadAssignedStatutoriesList(filteredList);
  });

$(document).ready(function () {
  getAssignedStatutories ();
});