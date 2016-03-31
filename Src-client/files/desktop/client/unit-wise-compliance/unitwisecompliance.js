var unitWiseComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList
var unitsList;
var assigneesList;


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function getClientReportFilters(){
  function onSuccess(data){
    countriesList = data["countries"];
    domainsList = data["domains"];
    businessGroupsList = data["business_groups"];
    legalEntitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    unitsList = data["units"];
    assigneesList = data["users"];
    loadCountries(countriesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  client_mirror.getClientReportFilters(
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
  $(".country").text(country);
  $(".domain").text(domain);

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

    var tableRow1=$('#unit-head-templates .table-unit-head .table-row-unit-head');
    var clone1=tableRow1.clone();
    $('.tbody-unit').append(clone1);

    var compliancelists = filterList[entity]["unit_wise_compliances"]
    for(var compliancelist in compliancelists){
      var uAddress = '';
      if(compliancelists[compliancelist].length > 0)
        uAddress = compliancelists[compliancelist][0]["unit_address"]
      var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
      var clone2=tableRow2.clone();
      $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;"> <abbr class="page-load tipso_style" title="'+ uAddress +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliancelist+'</div>');
      $('.tbody-unit').append(clone2);
      
      for(i=0; i<compliancelists[compliancelist].length; i++){
        var triggerdate = '';
        var statutorydate = '';
        for(j=0; j<compliancelists[compliancelist][i]["statutory_dates"].length; j++){

          var sDay = '';
          if(compliancelists[compliancelist][i]["statutory_dates"][j]["statutory_date"] != null) sDay = compliancelists[compliancelist][i]["statutory_dates"][j]["statutory_date"];

          var sMonth = '';
          if(compliancelists[compliancelist][i]["statutory_dates"][j]["statutory_month"] != null) sMonth = compliancelists[compliancelist][i]["statutory_dates"][j]["statutory_month"];

          var tDays = '';
          if(compliancelists[compliancelist][i]["statutory_dates"][j]["trigger_before_days"] != null) tDays = compliancelists[compliancelist][i]["statutory_dates"][j]["trigger_before_days"];

          if(sMonth == 1) sMonth = "January"
          else if(sMonth == 2) sMonth = "February"
          else if(sMonth == 3) sMonth = "March"
          else if(sMonth == 4) sMonth = "April"  
          else if(sMonth == 5) sMonth = "May"
          else if(sMonth == 6) sMonth = "June"
          else if(sMonth == 7) sMonth = "July"
          else if(sMonth == 8) sMonth = "Auguest"
          else if(sMonth == 9) sMonth = "September"
          else if(sMonth == 10) sMonth = "October"
          else if(sMonth == 11) sMonth = "November"
          else if(sMonth == 12) sMonth = "December"
          triggerdate +=  tDays + " Day(s), ";
          statutorydate +=  sMonth +' '+ sDay + ', ';
        }

        var summary = compliancelists[compliancelist][i]["summary"];
        if(statutorydate.trim() != ''){
          statutorydate = statutorydate.replace(/,\s*$/, "");
        }
        if(triggerdate.trim() != ''){
          triggerdate = triggerdate.replace(/,\s*$/, "");
        }
        if(summary != null){
          if(statutorydate.trim() != ''){
            statutorydate = summary + ' ( '+statutorydate+' )';
          }else{
            statutorydate = summary;
          }
        }

        var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone3=tableRow3.clone();
        var cDescription = compliancelists[compliancelist][i]["description"];
        $('.tbl_sno', clone3).text(compliance_count+1);
        $('.tbl_compliance', clone3).html('<abbr class="page-load tipso_style" title="'+ cDescription +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliancelists[compliancelist][i]["compliance_name"]);
        $('.tbl_frequency', clone3).text(compliancelists[compliancelist][i]["compliance_frequency"]);
        $('.tbl_statutorydate', clone3).text(statutorydate);
        $('.tbl_triggerbefore', clone3).text(triggerdate);
        $('.tbl_duedate', clone3).text(compliancelists[compliancelist][i]["due_date"]);
        var vDate = '';
        if(compliancelists[compliancelist][i]["validity_date"] != null) vDate = compliancelists[compliancelist][i]["validity_date"];
        $('.tbl_validitydate', clone3).text(vDate);
        $('.tbody-unit').append(clone3);
        compliance_count++;
      }

      if(compliancelists[compliancelist].length == 0){
        var tableRow4=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone4=tableRow4.clone();
        $('.tbl_statutorydate', clone4).text("No Compliance Found");
        $('.tbody-unit').append(clone4);
      }
    }   
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
 
}


$("#submit").click(function(){ 
  var country = $("#country").val();
  var domain = $("#domain").val();
  var businessgroup = null;
  var legalentity = null;
  var division = null;
  var unit = null;
  var assignee = null;

  if($("#businessgroup").val() != '') businessgroup = $("#businessgroup").val();
  if($("#legalentity").val() != '') legalentity = $("#legalentity").val();
  if($("#division").val() != '') division = $("#division").val();
  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#assignee").val() != '') assignee = $("#assignee").val();

  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");  
  }
  else{
      var filterdata={};
      filterdata["country_id"]=parseInt(country);
      filterdata["domain_id"]=parseInt(domain);
      filterdata["businessgroup_id"]=parseInt(businessgroup);
      filterdata["legalentity_id"]=parseInt(legalentity);
      filterdata["division_id"]=parseInt(division);
      filterdata["unit_id"]=parseInt(unit);
      filterdata["user_id"]=parseInt(assignee);

      function onSuccess(data){
        unitWiseComplianceList = data["compliance_list"];
        loadresult(unitWiseComplianceList);
      }
      function onFailure(error){
        onFailure(error);
      }
      client_mirror.getUnitwisecomplianceReport( parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), parseInt(assignee), 
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
        });
  }
});


//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocomplete_domain").hide();
  $("#autocomplete_businessgroup").hide();
  $("#autocomplete_legalentity").hide();
  $("#autocomplete_division").hide();
  $("#autocomplete_unit").hide();
  $("#autocomplete_assignee").hide();
});

//load country list
function loadCountries(countriesList){
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function(key, values){
    var countryId = countriesList[key]['country_id'];
    var countryName = countriesList[key]['country_name'];
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


//Assignee---------------------------------------------------
$("#assigneeval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_assignee").show();
  
  var assignees = assigneesList;
  var suggestions = [];
 $('#ulist_assignee').empty();
  if(textval.length>0){
    for(var i in assignees){
      if (~assignees[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["employee_id"],assignees[i]["employee_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_assignee(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_assignee').append(str);
    $("#assignee").val('');
    }else{
      $("#assignee").val('');
      $("#autocomplete_assignee").hide();
    }
});
//set selected autocomplte value to textbox
function activate_assignee (element,checkval,checkname) {
  $("#assigneeval").val(checkname);
  $("#assignee").val(checkval);
}
//Autocomplete Script ends

$(function() {
  $(".grid-table-rpt").hide();
  getClientReportFilters();
});