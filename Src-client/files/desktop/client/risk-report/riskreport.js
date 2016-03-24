var riskComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList
var unitsList;
var actList;


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function getRiskReportFilters(){
  function onSuccess(data){
    countriesList = data["countries"];
    domainsList = data["domains"];
    businessGroupsList = data["business_groups"];
    legalEntitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    unitsList = data["units"];
    actList = data["level1_statutories"];
    loadCountries(countriesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  client_mirror.getRiskReportFilters(
    function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
  );
}

function loadresult(filterList){
  $(".grid-table-rpt").show();
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();

  $(".tbody-unit").find("tbody").remove();
  var compliance_count=0;
  for(var entity in filterList){

    var tableRow=$('#unit-list-templates .table-unit-list .table-row-unit-list');
    var clone=tableRow.clone();
    $('.tbl_country', clone).text(country);
    $('.tbl_domain', clone).text(domain);
    $('.tbl_businessgroup', clone).text(filterList[entity]["business_group_name"]);
    $('.tbl_division', clone).text(filterList[entity]["division_name"]);
    $('.tbl_legalentity', clone).text(filterList[entity]["legal_entity_name"]);
    $('.tbody-unit').append(clone);

    var statutoryUnits = filterList[entity]["level_1_statutory_wise_units"]
    for(var statutoryUnit in statutoryUnits){

      var tableRow5=$('#unit-head-templates .table-unit-head .table-row-act-name');
      var clone5=tableRow5.clone();
      $('.tbl_actname', clone5).html('<div class="heading" style="margin-top:5px;width:auto;">'+statutoryUnit+'</div>');
      $('.tbody-unit').append(clone5);

      var tableRow1=$('#unit-head-templates .table-unit-head .table-row-unit-head');
      var clone1=tableRow1.clone();
      $('.tbody-unit').append(clone1);

      for(var j=0; j<statutoryUnits[statutoryUnit].length; j++){
        var uName = statutoryUnits[statutoryUnit][j]["unit_name"];
        var uAddress = statutoryUnits[statutoryUnit][j]["address"];

        var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
        var clone2=tableRow2.clone();
        $('.tbl_unitheading', clone2).html('<abbr class="page-load tipso_style" title="'+ uAddress +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+uName);
        $('.tbody-unit').append(clone2);
      
      
      var uCompliences = statutoryUnits[statutoryUnit][j]["compliances"];

      for(i=0; i<uCompliences.length; i++){
        
        var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone3=tableRow3.clone();

        $('.tbl_sno', clone3).text(compliance_count+1);
        $('.tbl_statutoryprovision', clone3).text(uCompliences[i]["statutory_mapping"]);
        $('.tbl_compliance', clone3).text(uCompliences[i]["compliance_name"]);
        $('.tbl_description', clone3).text(uCompliences[i]["description"]);
        $('.tbl_penalconsequences', clone3).text(uCompliences[i]["penal_consequences"]);
        $('.tbl_frequency', clone3).text(uCompliences[i]["compliance_frequency"]);
        $('.tbl_repeats', clone3).text(uCompliences[i]["repeats"]);
        
        $('.tbody-unit').append(clone3);
        compliance_count++;
      }

      if(uCompliences.length == 0){
        var tableRow4=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone4=tableRow4.clone();
        $('.tbl_description', clone4).text("No Compliance Found");
        $('.tbody-unit').append(clone4);
      }
    }
    }   
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
 
}

function loadCompliance(reportType){
  var country = $("#country").val();
  var domain = $("#domain").val();
  var businessgroup = null;
  var legalentity = null;
  var division = null;
  var unit = null;
  var act = null;
  var statutory_status = null;

  if($("#businessgroup").val() != '') businessgroup = $("#businessgroup").val();
  if($("#legalentity").val() != '') legalentity = $("#legalentity").val();
  if($("#division").val() != '') division = $("#division").val();
  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#act").val() != '') act = $("#act").val().trim();
  if($("#statutory_status").val() != '') statutory_status = $("#statutory_status").val();

  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");  
  }
  else{
    var filterdata={};
    filterdata["country_id"] = country;
    filterdata["domain_id"] = domain;
    filterdata["businessgroup_id"] = businessgroup;
    filterdata["legalentity_id"] = legalentity;
    filterdata["division_id"] = division;
    filterdata["unit_id"] = unit;
    filterdata["statutory_id"] = act;
    filterdata["statutory_status"] = statutory_status;

    function onSuccess(data){
      riskComplianceList = data["delayed_compliance"];
      if(reportType == "show"){
        loadresult(riskComplianceList);
      }else{
        loadresult(riskComplianceList);
        client_mirror.exportToCSV(data, 
          function (error, response) {
            if (error == null){
              var download_url = response["link"];
              window.open(download_url, '_blank');
            }
            else {
              displayMessage(error);
            }
          });
      }
    }
    function onFailure(error){
      onFailure(error);
    }
    client_mirror.getRiskReport( parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), act, parseInt(statutory_status), 
      function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
  }
}

$("#submit").click(function(){ 
  loadCompliance("show")
});

$("#export").click(function(){ 
  loadCompliance("export")
});


//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocomplete_domain").hide();
  $("#autocomplete_businessgroup").hide();
  $("#autocomplete_legalentity").hide();
  $("#autocomplete_division").hide();
  $("#autocomplete_unit").hide();
  $("#autocomplete_act").hide();
});

//load country list
function loadCountries(countriesList){
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function(key, values){
    var countryId = countriesList[key]['country_id'];
    var countryName = countriesList[key]['country_name'];
    if(countriesList[key]['is_active'])
      $('#country').append($('<option value="'+countryId+'">'+countryName+'</option>'));
  });
}

//load domain list in autocomplete text box  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_domain").show();
  var domains = domainsList;
  var suggestions = [];
  $('#ulist_domain').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == true) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_domain(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_domain').append(str);
    $("#domain").val('');
    }else{
      $("#domain").val('');
      $("#autocomplete_domain").hide();
    }
});
//set selected autocomplte value to textbox
function activate_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}

//businessgroups-----------------------------------------
$("#businessgroupval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_businessgroup").show();
  var bgroups = businessGroupsList;
  var suggestions = [];
  $('#ulist_businessgroup').empty();
  if(textval.length>0){
    for(var i in bgroups){
      if (~bgroups[i]["business_group_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_businessgroups(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_businessgroup').append(str);
    $("#businessgroup").val('');
    }else{
      $("#businessgroup").val('');
      $("#autocomplete_businessgroup").hide();
    }
});
function activate_businessgroups (element,checkval,checkname) {
  $("#businessgroupval").val(checkname);
  $("#businessgroup").val(checkval);
}

//Legal Entity---------------------------------------------------------------------------------------------------------------
$("#legalentityval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_legalentity").show();
  
  var lentity = legalEntitiesList;
  var suggestions = [];
 $('#ulist_legalentity').empty();
  if(textval.length>0){
    for(var i in lentity){
      if (~lentity[i]["legal_entity_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_lentity(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_legalentity').append(str);
    $("#legalentity").val('');
    }else{
      $("#legalentity").val('');
      $("#autocomplete_legalentity").hide();
    }
});
//set selected autocomplte value to textbox
function activate_lentity (element,checkval,checkname) {
  $("#legalentityval").val(checkname);
  $("#legalentity").val(checkval);
}

//Division Entity---------------------------------------------------
$("#divisionval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_division").show();
  
  var divisions = divisionsList;
  var suggestions = [];
 $('#ulist_division').empty();
  if(textval.length>0){
    for(var i in divisions){
      if (~divisions[i]["division_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([divisions[i]["division_id"],divisions[i]["division_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_division(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_division').append(str);
    $("#division").val('');
    }else{
      $("#division").val('');
      $("#autocomplete_division").hide();
    }
});
//set selected autocomplte value to textbox
function activate_division (element,checkval,checkname) {
  $("#divisionval").val(checkname);
  $("#division").val(checkval);
}


//Division Entity---------------------------------------------------
$("#unitval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_unit").show();
  
  var units = unitsList;
  var suggestions = [];
 $('#ulist_unit').empty();
  if(textval.length>0){
    for(var i in units){
      if (~units[i]["unit_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],units[i]["unit_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_unit').append(str);
    $("#unit").val('');
    }else{
      $("#unit").val('');
      $("#autocomplete_unit").hide();
    }
});
//set selected autocomplte value to textbox
function activate_unit (element,checkval,checkname) {
  $("#unitval").val(checkname);
  $("#unit").val(checkval);
}

//acts-------------------------------------
$("#actval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_act").show();
  var acts = actList;
  var suggestions = [];
  $('#ulist_act').empty();
  if(textval.length>0){
    for(var i in acts){
      if (~acts[i].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([acts[i],acts[i]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_acts(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_act').append(str);
    $("#act").val('');
    }else{
      $("#act").val('');
      $("#autocomplete_act").hide();
    }
});
function activate_acts (element,checkval,checkname) {
  $("#actval").val(checkname);
  $("#act").val(checkval);
}
//Autocomplete Script ends

$(function() {
  $(".grid-table-rpt").hide();
  getRiskReportFilters();
});