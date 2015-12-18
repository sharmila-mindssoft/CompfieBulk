var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;

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
    
    loadStatutoryMappingList(statutoryMappingsList);
  }
  function failure(data){
  }
  mirror.getStatutoryMappings(success, failure);
}

function loadStatutoryMappingList(statutoryMappingsList) {
  /*var j = 1;
  var imgName = '';
  var passStatus = '';
  var statutorymappingId = 0;
  var isActive = 0;
  var industryName = '';
  var statutoryNatureName = '';
  var countryName = '';
  var domainName = '';
  var approvalStatus = '';

  $(".tbody-statutorymapping-list").find("tr").remove();
  for(var entity in statutoryMappingsList) {
        statutorymappingId = entity;
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
        countryName = statutoryMappingsList[entity]["country_name"];
        domainName = statutoryMappingsList[entity]["domain_name"];
        isActive = statutoryMappingsList[entity]["is_active"];
        approvalStatus = statutoryMappingsList[entity]["approval_status"];
        if(isActive == 1) {
          passStatus="0";
          imgName="icon-active.png"
        }
        else {
          passStatus="1";
          imgName="icon-inactive.png"
         }
         if(approvalStatus == '0'){
          approvalStatus = "Pending";
         }
        var tableRow=$('#templates .table-statutorymapping .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(j);
        $('.country', clone).text(countryName);
        $('.domain', clone).text(domainName);
        $('.industry', clone).text(industryName);
        $('.statutorynature', clone).text(statutoryNatureName);
        $('.statutory', clone).html(statutoryMappings);
        $('.compliancetask', clone).html(complianceNames);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+statutorymappingId+')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+statutorymappingId+','+passStatus+')"/>');
        $('.approvalstatus', clone).text(approvalStatus);
        $('.tbody-statutorymapping-list').append(clone);
        j = j + 1;
        }*/
      }

//Autocomplete Script Starts
//Hide list items after select
function hidemenu() {
  document.getElementById('autocompleteview').style.display = 'none';
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

//load country list in autocomplete text box  
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
  $("#countryval").val(checkname);
  $("#country").val(checkval);
}
//Autocomplete Script ends