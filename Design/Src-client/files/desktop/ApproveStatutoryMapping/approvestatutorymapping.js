var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var j;

$(function() {
	getStatutoryMappings();
});
function getStatutoryMappings(){
  function success(status,data){
    industriesList = data["industries"];
    statutoryLevelsList = data["statutory_levels"];
    statutoriesList = data["statutories"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    geographyLevelsList = data["geography_levels"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    statutoryMappingsList = data["statutory_mappings"];
    tempstatutoryMappingsList = data["statutory_mappings"];
  }
  function failure(data){
  }
  mirror.getStatutoryMappings(success, failure);
}

//Autocomplete Script Starts
//Hide list items after select
function hidemenu() {
  document.getElementById('autocompleteview').style.display = 'none';
  document.getElementById('autocomplete_domain').style.display = 'none';
  document.getElementById('autocomplete_industry').style.display = 'none';
  document.getElementById('autocomplete_statutorynature').style.display = 'none';
}

//load country list in autocomplete text box  
function loadauto_text (textval) {
  document.getElementById('autocompleteview').style.display = 'block';
  var countries = countriesList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == 1) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text').append(str);
    $("#country").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);
}

//load domain list in autocomplete text box  
function loadauto_domain (textval) {
  document.getElementById('autocomplete_domain').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == 1) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_domain(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_domain').append(str);
    $("#domain").val('');
    }
}
//set selected autocomplte value to textbox
function activate_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}

//load domain list in autocomplete text box  
function loadauto_industry (textval) {
  document.getElementById('autocomplete_industry').style.display = 'block';
  var industries = industriesList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in industries){
      if (~industries[i]["industry_name"].toLowerCase().indexOf(textval.toLowerCase()) && industries[i]["is_active"] == 1) suggestions.push([industries[i]["industry_id"],industries[i]["industry_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_industry(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_industry').append(str);
    $("#industry").val('');
    }
}
//set selected autocomplte value to textbox
function activate_industry (element,checkval,checkname) {
  $("#industryval").val(checkname);
  $("#industry").val(checkval);
}


//load statutorynature list in autocomplete text box  
function loadauto_statutorynature (textval) {
  document.getElementById('autocomplete_statutorynature').style.display = 'block';
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ulist_statutorynature').empty();
  if(textval.length>0){
    for(var i in statutorynatures){
      if (~statutorynatures[i]["statutory_nature_name"].toLowerCase().indexOf(textval.toLowerCase()) && statutorynatures[i]["is_active"] == 1) suggestions.push([statutorynatures[i]["statutory_nature_id"],statutorynatures[i]["statutory_nature_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_statutorynature(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_statutorynature').append(str);
    $("#statutorynature").val('');
    }
}
//set selected autocomplte value to textbox
function activate_statutorynature (element,checkval,checkname) {
  $("#statutorynatureval").val(checkname);
  $("#statutorynature").val(checkval);
}

//Autocomplete Script ends
function loadresult(){
  var country = $("#country").val();
  var domain = $("#domain").val();
  var industry = $("#industry").val();
  var statutorynature = $("#statutorynature").val();

  j = 1;
  var statutorymappingId = 0;
  var industryName = '';
  var statutoryNatureName = '';
  var approvalStatus = '';
  var applicableLocation = '';
  var isActive = 0;
  var countryId = '';
  var domainId = '';
  var statutoryNatureId = '';
  var industryIds = [];
  $(".tbody-statutorymapping-list").find("tr").remove();
  for(var entity in statutoryMappingsList) {
        statutorymappingId = entity;

        countryId = statutoryMappingsList[entity]["country_id"];
        domainId = statutoryMappingsList[entity]["domain_id"];
        industryIds = statutoryMappingsList[entity]["industry_ids"];

        industryName = statutoryMappingsList[entity]["industry_names"];
        statutoryNatureName = statutoryMappingsList[entity]["statutory_nature_name"];        
        var statutoryMappings='';
        for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
          statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
        }
        var complianceNames='';
        for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
          complianceNames = complianceNames + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
        }
        statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
        applicableLocation = statutoryMappingsList[entity]["geography_mappings"];
        isActive = statutoryMappingsList[entity]["is_active"];
        approvalStatus = statutoryMappingsList[entity]["approval_status"];

        conditionResult = (approvalStatus == '0' && isActive == '1' && countryId == country && domainId == domain);
        if(statutorynature != ""){
          conditionResult = conditionResult && (statutorynature == statutoryNatureId);
        }
        if(industry != ""){
          conditionResult = conditionResult && ($.inArray(parseInt(industry), industryIds) >= 0);
        }
        if(conditionResult){
        var tableRow=$('#templates .table-statutorymapping .table-row');
        var clone=tableRow.clone();
        $('.industry', clone).text(industryName);
        $('.statutorynature', clone).text(statutoryNatureName);
        $('.statutory', clone).html(statutoryMappings);
        $('.compliancetask', clone).html('<a href="#popup1" onclick="disppopup('+j+')">'+complianceNames+'</a>');
        $('.applicablelocation', clone).text(applicableLocation);
        $('.action', clone).html('<input type="hidden" id="mapping_id'+j+'" value="'+statutorymappingId+'" /> <select class="input-box" id="action'+j+'" onchange="dispreason('+j+')"><option value="">Select</option><option value="approve">Approve</option><option value="reject">Reject</option><option value="notify">Approve & Notify</option></select>');
        $('.reason', clone).html('<textarea class="input-box" id="notifyreason'+j+'" placeholder="Enter notification text" style="height:50px;display:none;"></textarea><br><span style="font-size:0.75em;display:none;" id="notifynote'+j+'">(max 500 characters)</span> <input type="text" style="display:none;" id="reason'+j+'" class="input-box" placeholder="Enter reason" />');
        $('.tbody-statutorymapping-list').append(clone);
        j = j + 1;
      }
    }
}

function disppopup(j){


var statutoryMappings='';
for(var i=0; i<statutoryMappingsList[j]["statutory_mappings"].length; i++){
  statutoryMappings = statutoryMappings + statutoryMappingsList[j]["statutory_mappings"][i] + " <br>";
}

var complianceNames='';
for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
  complianceNames = complianceNames + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
}
        

$(".popup_statutory").html(statutoryMappings);
$(".popup_statutorynature").text(statutoryMappingsList[i]["statutory_nature_name"]);
$(".popup_compliancetask").html(complianceNames);
$(".popup_compliancedescription").html(statutoryMappings);
$(".popup_penalconsequences").html(statutoryMappings);
$(".popup_compliancefrequency").html(statutoryMappings);
$(".popup_complianceoccurance").html(statutoryMappings);
$(".popup_applicablelocation").html(statutoryMappings);


}

function dispreason(j){
  if($("#action"+j).val() == 'reject'){
    $("#notifyreason"+j).hide();
    $("#notifynote"+j).hide();
    $("#reason"+j).show();
  }else if($("#action"+j).val() == 'notify'){
    $("#notifyreason"+j).show();
    $("#notifynote"+j).show();
    $("#reason"+j).hide();
  }else{
    $("#notifyreason"+j).hide();
    $("#notifynote"+j).hide();
    $("#reason"+j).hide();
  }
}

function saveRecord(){
  
  for(var i=1; i<j; i++){
    var statutory_mapping_id = parseInt($("#mapping_id"+i).val()); 
    var approval_status = $("#action"+i).val(); 
    var rejected_reason = $("#reason"+i).val(); 
    var notification_text = $("#notifyreason"+i).val(); 
    if(approval_status != ''){
      function success(status,data){
      if(status == "success"){
          //getStatutoryMappings();
          //alert(status);
      }else{
          $("#error").text(status)
      }
      }
      function failure(data){
      }
      
    mirror.approveStatutoryMapping(statutory_mapping_id, approval_status, rejected_reason, notification_text, success, failure);
    }
    
  }
  
}
