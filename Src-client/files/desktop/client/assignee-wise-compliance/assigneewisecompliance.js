var assigneeWiseComplianceList;
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
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();
  $(".country").text(country);
  $(".domain").text(domain);

  $(".tbody-assignee").find("tbody").remove();
  var compliance_count=0;
  for(var entity in filterList){

      var tableRow=$('#assignee-list-templates .table-assignee-list .table-row-assignee-list');
      var clone=tableRow.clone();
      $('.tbl_country', clone).text(country);
      $('.tbl_domain', clone).text(domain);

      var bg = '-';
      if(filterList[entity]["business_group_name"] != null) bg = filterList[entity]["business_group_name"];
      $('.tbl_businessgroup', clone).text(bg);

      var dv = '-';
      if( filterList[entity]["division_name"] != null) dv = filterList[entity]["division_name"];
      $('.tbl_division', clone).text(dv);

      $('.tbl_businessgroup', clone).text(bg);
      $('.tbl_division', clone).text(dv);
      $('.tbl_legalentity', clone).text(filterList[entity]["legal_entity_name"]);
      $('.tbody-assignee').append(clone);

      var tableRow1=$('#assignee-head-templates .table-assignee-head .table-row-assignee-head');
      var clone1=tableRow1.clone();
      $('.tbody-assignee').append(clone1);

      var compliancelists = filterList[entity]["user_wise_compliance"];
      if(compliancelists.length > 0){
        for(var compliancelist in compliancelists){
          var assignee_ = compliancelists[compliancelist]["assignee"];
          var concurrence = compliancelists[compliancelist]["concurrence_person"];
          var approval_ = compliancelists[compliancelist]["approval_person"];

          if(assignee_ == null) assignee_ = 'Client Admin';
          if(concurrence == null) concurrence = 'Nil';
          if(approval_ == null) approval_ = 'Client Admin';

          var tableRow2=$('#assignee-name-templates .table-assignee-name .table-row-assignee-name');
          var clone2=tableRow2.clone();
          $('.tbl_assigneeheading', clone2).html('Assignee: ' + assignee_);
          $('.tbl_concurrenceheading', clone2).html('concurrence: ' + concurrence);
          $('.tbl_approvalheading', clone2).html('Approval: ' + approval_);

          $('.tbody-assignee').append(clone2);
          var compliances = compliancelists[compliancelist]["compliances"];
          for(i=0; i<compliances.length; i++){
            var triggerdate = '';
            var statutorydate = '';
            for(j=0; j<compliances[i]["statutory_dates"].length; j++){
              var sDay = '';
              if(compliances[i]["statutory_dates"][j]["statutory_date"] != null) sDay = compliances[i]["statutory_dates"][j]["statutory_date"];

              var sMonth = '';
              if(compliances[i]["statutory_dates"][j]["statutory_month"] != null) sMonth = compliances[i]["statutory_dates"][j]["statutory_month"];

              var tDays = '';
              if(compliances[i]["statutory_dates"][j]["trigger_before_days"] != null) tDays = compliances[i]["statutory_dates"][j]["trigger_before_days"];

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
                
              triggerdate +=  tDays + " Days" + ', ';
              statutorydate +=  sDay + ' - ' + sMonth +', ';
            }

            if(statutorydate.trim() != '') statutorydate = statutorydate.replace(/,\s*$/, "");
            if(triggerdate.trim() != '') triggerdate = triggerdate.replace(/,\s*$/, "");

            var summary = compliances[i]["summary"];
            if(summary != null){
              if(statutorydate.trim() != ''){
                statutorydate = summary + ' ( '+statutorydate+' )';
              }else{
                statutorydate = summary;
              }
            }

            var tableRow3=$('#assignee-content-templates .table-assignee-content .table-row-assignee-content');
            var clone3=tableRow3.clone();
            var cDescription = compliances[i]["description"];
            $('.tbl_sno', clone3).text(compliance_count+1);
            $('.tbl_compliance', clone3).html('<abbr class="page-load tipso_style" title="'+ cDescription +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliances[i]["compliance_name"]);
            $('.tbl_unit', clone3).text(compliances[i]["unit_address"]);
            $('.tbl_frequency', clone3).text(compliances[i]["compliance_frequency"]);
            $('.tbl_statutorydate', clone3).text(statutorydate);
            $('.tbl_triggerbefore', clone3).text(triggerdate);
            var dDays = '-';
            if(compliances[i]["due_date"] != null) dDays = compliances[i]["due_date"];
            $('.tbl_duedate', clone3).text(dDays);

            var vDays = '-';
            if(compliances[i]["validity_date"] != null) vDays = compliances[i]["validity_date"];
            $('.tbl_validitydate', clone3).text(vDays);
            $('.tbody-assignee').append(clone3);
            compliance_count++;
          }
        }   
      }else{
        var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
        var clone4=tableRow4.clone();
        $('.no_records', clone4).text('No Compliance Found');
        $('.tbody-assignee').append(clone4);
      }
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
  $(".grid-table-rpt").show();
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
        assigneeWiseComplianceList = data["compliance_list"];
        loadresult(assigneeWiseComplianceList);
      }
      function onFailure(error){
        onFailure(error);
      }
      client_mirror.getAssigneewisecomplianceReport( parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), parseInt(assignee), 
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
      var combineUnitName = units[i]['unit_code']+"-"+units[i]['unit_name'];
      if (~combineUnitName.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],combineUnitName]); 
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
      var combineUserName = assignees[i]['employee_code']+"-"+assignees[i]['employee_name'];
      if (~combineUserName.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["employee_id"],combineUserName]); 
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

$( document ).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function( position, feedback ) {
            $( this ).css( position );
            $( "<div>" )
                .addClass( "arrow" )
                .addClass( feedback.vertical )
                .addClass( feedback.horizontal )
                .appendTo( this );
        }
    }
});