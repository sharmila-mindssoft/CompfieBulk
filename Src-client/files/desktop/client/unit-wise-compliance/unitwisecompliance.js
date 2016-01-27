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
  var country = $("#countryval").val();
  var domain = $("#domainval").val();
  $(".country").text(country);
  $(".domain").text(domain);

  $(".tbody-unit").find("tbody").remove();
  var count=1;
  var compliance_count=0;
  for(var entity in filterList){
    var unitname =  'UNIT NAME'/*filterList[entity][""]*/;

    var tableRow=$('#unit-list-templates');
    var clone=tableRow.clone();
    $('.tbl_country', clone).text(country);
    $('.tbody-unit').append(clone);
   
    

/*    for(var j=0; j<complianceFrequencyList.length; j++){             
      for(var i=0; i<filterList[entity].length; i++){
        for(var k=0; k<filterList[entity][i]["compliances"].length; k++){

          if((compliance_frequency == 'All' || compliance_frequency == filterList[entity][i]["compliances"][k]["frequency_id"]) ){
            var occurance = '';
            var occuranceid;
            $.each(complianceFrequencyList, function(index, value) {
            if (value.frequency_id == filterList[entity][i]["compliances"][k]["frequency_id"]) {
                occurance = value.frequency;
                occuranceid = value.frequency_id;
                checkNoCompliance = false;
            }
            });
            if(occuranceid == 1 && (j+1)==1){
              if(display_occurance1){
                var tableRow2=$('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance1 = false;}
            }
            if(occuranceid == 2 && (j+1)==2){
              if(display_occurance2){
                var tableRow2=$('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance2 = false;}
            }
            if(occuranceid == 3 && (j+1)==3){
              if(display_occurance3){
                var tableRow2=$('#head-templates  .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance3 = false;}
            }
            if(occuranceid == 4 && (j+1)==4){
              if(display_occurance4){
                var tableRow2=$('#head-templates  .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance4 = false;}
            }

            if(occuranceid == 1 && (j+1)==1 || occuranceid == 2 && (j+1)==2 || occuranceid == 3 && (j+1)==3 || occuranceid == 4 && (j+1)==4){
              var tableRow1=$('#compliance-templates .table-compliances-list .table-row');
              var clone1=tableRow1.clone();
              $('.tbody-compliance').append(clone1);
              $('.tbl_sno', clone1).text(compliance_count+1);
              $('.tbl_industrytype', clone1).text(filterList[entity][i]["industry_names"]);
              $('.tbl_statutorynature',   clone1).text(filterList[entity][i]["statutory_nature_name"]);
              $('.tbl_statutoryprovision', clone1).text(filterList[entity][i]["compliances"][k]["statutory_provision"]);
              $('.tbl_compliancetask', clone1).html('<a href="#">'+filterList[entity][i]["compliance_names"][k]+'</a>');
              $('.tbl_description', clone1).text(filterList[entity][i]["compliances"][k]["description"]);
              $('.tbl_penalconsequences', clone1).text(filterList[entity][i]["compliances"][k]["penal_consequences"]);
              $('.tbl_occurance', clone1).text(occurance);
              $('.tbl_applicablelocation', clone1).text(filterList[entity][i]["geography_mappings"]);
              $('.accordion-content'+count).append(clone1);
              compliance_count = compliance_count + 1;
            }
          }
        }
      }
    }*/
    
    count++;
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
      $("#autocomplete_businessgroups").hide();
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