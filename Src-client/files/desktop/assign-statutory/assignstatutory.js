var assignedStatutoriesList;
var countriesList;
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


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}


//check & uncheck list data for single selection
  function activate(element, id, dispname, type){
    alert($(element).attr('class'))
    alert(type)
    $(type).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(element).addClass("active");

    var checkbox_status = $(element).attr('class');
    var clsval='';
    var clsval1='';
    var str='';

    if(checkbox_status == 'countrylist active'){
      assignStatutoryCountryId = id;
      assignStatutoryCountryValue = dispname;

      clsval='.grouplist';
      clsval1='grouplist';
      $('#group').empty();
      for(var group in groupcompaniesList){
        var groupid = groupcompaniesList[group]["client_id"];
        var dispgroupname = groupcompaniesList[group]["group_name"];
        if(groupcompaniesList[group]["is_active"] == true && $.inArray(id, groupcompaniesList[group]["country_ids"]) >= 0){
          str += '<li id="'+groupid+'" class="'+clsval1+'" onclick="activate(this,'+groupid+',\''+dispgroupname+'\',\''+clsval+'\')" ><span class="filter2_name">'+dispgroupname+'</span></li>';
        }
      }
      $('#group').append(str); 
    }

    if(checkbox_status == 'grouplist active'){
      assignStatutoryGroupId = id;
      assignStatutoryGroupValue = dispname;

      clsval='.businessgrouplist';
      clsval1='businessgrouplist';
      $('#businessgroup').empty();
      for(var businessgroup in businessgroupsList){
        var businessgroupid = businessgroupsList[businessgroup]["business_group_id"];
        var dispbusinessgroupname = businessgroupsList[businessgroup]["business_group_name"];
        if(businessgroupsList[businessgroup]["client_id"] == id){
          str += '<li id="'+businessgroupid+'" class="'+clsval1+'" onclick="activate(this,'+businessgroupid+',\''+dispbusinessgroupname+'\',\''+clsval+'\')" ><span class="filter2_name">'+dispbusinessgroupname+'</span></li>';
        }
      }
      $('#businessgroup').append(str); 
    }

      /*if(checkbox_status == 'domainlist active'){
        sm_domainid = id;
        sm_domainval = dispname;
      }

      if(checkbox_status == 'statutorynaturelist active'){
        sm_statutorynatureid = id;
        sm_statutorynatureval = dispname;
      }

      if(sm_countryid != '' && sm_domainid !=''){
        loadStatutoryLevels(sm_countryid,sm_domainid);
      }
      if(sm_countryid != ''){
        loadGeographyLevels(sm_countryid);
      }
      make_breadcrumbs();*/
  }

function load_firstwizard(){
  //load country details
  var clsval='.countrylist';
  var clsval1='countrylist';
  var str='';
  $('#country').empty();
    for(var country in countriesList){
      var countryid = countriesList[country]["country_id"];
      var dispcountryname = countriesList[country]["country_name"];
      if(countriesList[country]["is_active"] == true){
      str += '<li id="'+countryid+'" class="'+clsval1+'" onclick="activate(this,'+countryid+',\''+dispcountryname+'\',\''+clsval+'\')" ><span class="filter1_name">'+dispcountryname+'</span></li>';
    }
  }
  $('#country').append(str); 
}

$(".btn-assignstatutory-add").click(function(){
$("#assignstatutory-view").hide();
$("#assignstatutory-add").show();
$("#edit_assignstatutory_id").val('');
displayMessage('');
load_firstwizard();

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
    countriesList = data["countries"];
    groupcompaniesList = data["group_companies"];
    businessgroupsList = data["business_groups"];
    legalentitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    geographyLevelsList = data["geography_levels"];
    geographiesList = data["geographies"];
    industriesList = data["industries"];
    domainsList = data["domains"];
    unitsList = data["units"];

    loadAssignedStatutoriesList(assignedStatutoriesList);
  }
  function onFailure(error){
  }
  mirror.GetAssignedStatutoriesList(
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

    countriesList =  [
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