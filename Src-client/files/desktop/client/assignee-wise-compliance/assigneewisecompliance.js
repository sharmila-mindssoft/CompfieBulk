var assigneeWiseComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList
var unitsList;
var assigneesList;
var finalList;
var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var fullArrayList = [];

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


function bgList(data){
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();
  $(".country").text(country);
  $(".domain").text(domain);
  var tableRow=$('#assignee-list-templates .table-assignee-list .table-row-assignee-list');
  var clone=tableRow.clone();
  $('.tbl_country', clone).text(country);
  $('.tbl_domain', clone).text(domain);
  var bg = '-';
  if(data["business_group_name"] != null) bg = data["business_group_name"];
  $('.tbl_businessgroup', clone).text(bg);
  var dv = '-';
  if( data["division_name"] != null) dv = data["division_name"];
  $('.tbl_division', clone).text(dv);
  $('.tbl_businessgroup', clone).text(bg);
  $('.tbl_division', clone).text(dv);
  $('.tbl_legalentity', clone).text(data["legal_entity_name"]);
  $('.tbody-assignee').append(clone);
  var tableRow1=$('#assignee-head-templates .table-assignee-head .table-row-assignee-head');
  var clone1=tableRow1.clone();
  $('.tbody-assignee').append(clone1);
}

function assigneeList(data){
  var assignee_ = data["assignee"];
  var concurrence = data["concurrence_person"];
  var approval_ = data["approval_person"];
  if(assignee_ == null) assignee_ = 'Client Admin';
  if(concurrence == null) concurrence = 'Nil';
  if(approval_ == null) approval_ = 'Client Admin';
  var tableRow2=$('#assignee-name-templates .table-assignee-name .table-row-assignee-name');
  var clone2=tableRow2.clone();
  $('.tbl_assigneeheading', clone2).html('Assignee: ' + assignee_);
  $('.tbl_concurrenceheading', clone2).html('concurrence: ' + concurrence);
  $('.tbl_approvalheading', clone2).html('Approval: ' + approval_);
  $('.tbody-assignee').append(clone2);
}

function complianceListArray(data){

  var triggerdate = '';
  var statutorydate = '';
  for(j=0; j<data["statutory_dates"].length; j++){
    var sDay = '';
    if(data["statutory_dates"][j]["statutory_date"] != null) sDay = data["statutory_dates"][j]["statutory_date"];
    var sMonth = '';
    if(data["statutory_dates"][j]["statutory_month"] != null) sMonth = data["statutory_dates"][j]["statutory_month"];
    var tDays = '';
    if(data["statutory_dates"][j]["trigger_before_days"] != null) tDays = data["statutory_dates"][j]["trigger_before_days"];
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
  var summary = data["summary"];
  if(summary != null){
    if(statutorydate.trim() != ''){
      statutorydate = summary + ' ( '+statutorydate+' )';
    }else{
      statutorydate = summary;
    }
  }

  var tableRow3=$('#assignee-content-templates .table-assignee-content .table-row-assignee-content');
  var clone3=tableRow3.clone();
  var cDescription = data["description"];
  $('.tbl_sno', clone3).text(sno+1);
  $('.tbl_compliance', clone3).html('<abbr class="page-load tipso_style" title="'+ cDescription +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+data["compliance_name"]);
  $('.tbl_unit', clone3).text(data["unit_address"]);
  $('.tbl_frequency', clone3).text(data["compliance_frequency"]);
  $('.tbl_statutorydate', clone3).text(statutorydate);
  $('.tbl_triggerbefore', clone3).text(triggerdate);
  var dDays = '-';
  if(data["due_date"] != null) dDays = data["due_date"];
  $('.tbl_duedate', clone3).text(dDays);
  var vDays = '-';
  if(data["validity_date"] != null) vDays = data["validity_date"];
  $('.tbl_validitydate', clone3).text(vDays);
  $('.tbody-assignee').append(clone3);
  sno++;
}

function get_sub_array(object, start, end){
  if(!end){ end = -1;}
  return object.slice(start, end);
}

function showloadrecord() {
  startCount = endCount;
  endCount = startCount + pageSize;
  var sub_keys_list = get_sub_array(fullArrayList, startCount, endCount);
  if(sub_keys_list.length < pageSize){
      $('#pagination').hide();
  }
  for(var y = 0;  y < pageSize; y++){
    if(sub_keys_list[y] !=  undefined){
      if(Object.keys(sub_keys_list[y])[0] == "division_name"){
        bgList(sub_keys_list[y]);
      }    
      else if(Object.keys(sub_keys_list[y])[0] == "assignee"){
        assigneeList(sub_keys_list[y]);
      }
      else if(Object.keys(sub_keys_list[y])[0] == "due_date"){
        complianceListArray(sub_keys_list[y]);
      } 
    } 
  }
}

$(function() {
    $('#pagination').click(function(e){
        $(".loading-indicator-spin").show();
        if($('.loading-indicator-spin').css('display') != 'none')
        {
          setTimeout(function(){  
              showloadrecord();
          }, 500);
        }
        setTimeout(function(){  
            $(".loading-indicator-spin").hide();
        }, 500);
    });
});

function loadArray(complianceList) {   
  endCount = pageSize;
  $.each(complianceList, function(i, val){
      var list = complianceList[i];
      var list_unit = val["user_wise_compliance"]
      delete val["unit_wise_compliances"];         
      fullArrayList.push(list);

      $.each(list_unit, function(i1, val1){
        var list_c = list_unit[i1];
        var list_compliances = val1['compliances'];
        delete list_c["compliances"];  
        fullArrayList.push(list_c);
   
        $.each(list_compliances, function(i2, val2){
            var list_comp = list_compliances[i2]; 
            fullArrayList.push(list_comp);
        }); 
    });
  });

  var totallist = fullArrayList.length;
  if(totallist > pageSize){
    $('#pagination').show();
  }
  else{
    $('#pagination').hide();
  }
  var sub_keys_list = get_sub_array(fullArrayList, startCount, endCount);
  //filterList();
  for(var y = 0;  y < pageSize; y++){
    if(sub_keys_list[y] !=  undefined){
      if(Object.keys(sub_keys_list[y])[0] == "division_name"){
        bgList(sub_keys_list[y]);
      }    
      else if(Object.keys(sub_keys_list[y])[0] == "assignee"){
        assigneeList(sub_keys_list[y]);
      }
      else if(Object.keys(sub_keys_list[y])[0] == "due_date"){
        complianceListArray(sub_keys_list[y]);
      } 
    } 
  }
}


function loadTotalCount(complianceList){
  $("#pagination").hide();
  var totalrecords = 0;
  $(".tbody-assignee").find("tbody").remove();

  $.each(complianceList, function(i, val){
    var ucList = val['user_wise_compliance'];
    $.each(ucList, function(i1, val1){
        var complianceCount =val1['compliances'].length;
        totalrecords = totalrecords + complianceCount;    
    });       
  }); 

  loadArray(complianceList);    
  $('.compliance_count').text("Total : "+ totalrecords +" records");

  if(totalrecords == 0){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-assignee').append(clone4);
  }
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
    displayMessage(message.country_required);
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);  
  }
  else{
      function onSuccess(data){
        assigneeWiseComplianceList = data["compliance_list"];

        fullArrayList = [];
        clearMessage();
        sno = 0;
        startCount = 0;
        endCount = 0;
        $(".grid-table-rpt").show();
        loadTotalCount(assigneeWiseComplianceList);
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