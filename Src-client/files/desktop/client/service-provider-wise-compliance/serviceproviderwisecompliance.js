var serviceProviderWiseComplianceList;
var countriesList;
var domainsList;
var levelOneStatutoriesList;
var unitsList;
var serviceProvidersList;


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function getServiceProviderReportFilters(){
  function onSuccess(data){
    countriesList = data["countries"];
    domainsList = data["domains"];
    levelOneStatutoriesList = data["level_1_statutories"];
    unitsList = data["units"];
    serviceProvidersList = data["service_providers"];
    loadCountries(countriesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  client_mirror.getServiceProviderReportFilters(
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
  var act = $("#actval").val();


  $(".tbody-serviceprovider").find("tbody").remove();
  var compliance_count=0;
  var sp_count=0;

  var tableRow=$('#serviceprovider-list-templates .table-serviceprovider-list .table-row-serviceprovider-list');
  var clone=tableRow.clone();
  $('.tbl_country', clone).text(country);
  $('.tbl_domain', clone).text(domain);
  $('.tbl_act', clone).text(act);
  $('.tbody-serviceprovider').append(clone);

  var tableRow5=$('#serviceprovider-head-templates .table-serviceprovider-head .table-row-serviceprovider-head');
    var clone5=tableRow5.clone();
    $('.tbody-serviceprovider').append(clone5);

  for(var entity in filterList){

    var sp_name = filterList[entity]["service_provider_name"];
    if(sp_name != null || sp_name != ''){

    var tableRow1=$('#serviceprovider-head-templates .table-serviceprovider-head .table-row-serviceprovider-headvalue');
    var clone1=tableRow1.clone();
    $('.tbl_sp_count', clone1).text(sp_count+1);
    $('.tbl_sp_name', clone1).text(sp_name);
    $('.tbl_sp_contactperson', clone1).text(filterList[entity]["contact_person"]);
    $('.tbl_sp_email', clone1).text("main");
    $('.tbl_sp_contactno', clone1).text(filterList[entity]["contact_no"]);
    $('.tbl_sp_address', clone1).text(filterList[entity]["address"]);
    $('.tbl_sp_period', clone1).text(filterList[entity]["contract_from"] +' to '+ filterList[entity]["contract_to"]);
    $('.tbody-serviceprovider').append(clone1);



   var tableRow6=$('#unit-head-templates .table-unit-head .table-row-unit-head');
    var clone6=tableRow6.clone();
    $('.tbody-serviceprovider').append(clone6);

    var compliancelists = filterList[entity]["unit_wise_compliance"];
    for(var compliancelist in compliancelists){
      var uAddress = '';
      if(compliancelists[compliancelist].length > 0)
        uAddress = compliancelists[compliancelist][0]["unit_address"]
      
      var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
      var clone2=tableRow2.clone();
      $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;"> <abbr class="page-load tipso_style" title="'+ uAddress +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliancelist+'</div>');
      $('.tbody-serviceprovider').append(clone2);
      
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
            
          triggerdate +=  tDays + " Days";
          statutorydate +=  sDay + ' - ' + sMonth;
        }
        var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone3=tableRow3.clone();
        var cDescription = compliancelists[compliancelist][i]["description"];
        $('.tbl_sno', clone3).text(compliance_count+1);
        $('.tbl_compliance', clone3).html(compliancelists[compliancelist][i]["compliance_name"]);
        $('.tbl_description', clone3).text(cDescription);
        $('.tbl_statutorydate', clone3).text(statutorydate);
        $('.tbl_triggerbefore', clone3).text(triggerdate);
        $('.tbl_duedate', clone3).text(compliancelists[compliancelist][i]["due_date"]);
        var vDate = '';
        if(compliancelists[compliancelist][i]["validity_date"] != null) vDate = compliancelists[compliancelist][i]["validity_date"];
        $('.tbl_validitydate', clone3).text(vDate);
        $('.tbody-serviceprovider').append(clone3);
        compliance_count++;
      }

      if(compliancelists[compliancelist].length == 0){
        var tableRow4=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone4=tableRow4.clone();
        $('.tbl_statutorydate', clone4).text("No Compliance Found");
        $('.tbody-serviceprovider').append(clone4);
      }
    } 
  }
  sp_count++;
    
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
}

$("#submit").click(function(){ 
  var country = $("#country").val();
  var domain = $("#domain").val();
  var act = $("#act").val().trim();
  var unit = null;
  var serviceprovider = null;

  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#serviceprovider").val() != '') serviceprovider = $("#serviceprovider").val();

  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");  
  }
  else if(act.length == 0){
    displayMessage("Act Required");  
  }
  else{
      var filterdata={};
      filterdata["country_id"]=parseInt(country);
      filterdata["domain_id"]=parseInt(domain);
      filterdata["statutory_id"]=act;
      filterdata["unit_id"]=parseInt(unit);
      filterdata["service_provider_id"]=parseInt(serviceprovider);

      function onSuccess(data){
        serviceProviderWiseComplianceList = data["compliance_list"];
        loadresult(serviceProviderWiseComplianceList);
      }
      function onFailure(error){
        onFailure(error);
      }
      client_mirror.getServiceProviderWiseCompliance( parseInt(country), parseInt(domain), act, parseInt(unit), parseInt(serviceprovider), 
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
  $("#autocomplete_act").hide();
  $("#autocomplete_unit").hide();
  $("#autocomplete_serviceprovider").hide();
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

//acts-----------------------------------------
$("#actval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_act").show();
  var acts = levelOneStatutoriesList;
  var suggestions = [];
  $('#ulist_act').empty();
  if(textval.length>0){
    for(var i in acts){
      if (~acts[i]["statutory"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([acts[i]["statutory"],acts[i]["statutory"]]); 
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
$("#serviceproviderval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_serviceprovider").show();
  
  var serviceprovider = serviceProvidersList;
  var suggestions = [];
 $('#ulist_serviceprovider').empty();
  if(textval.length>0){
    for(var i in serviceprovider){
      if (~serviceprovider[i]["service_provider_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([serviceprovider[i]["service_provider_id"],serviceprovider[i]["service_provider_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_serviceprovider(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_serviceprovider').append(str);
    $("#serviceprovider").val('');
    }else{
      $("#serviceprovider").val('');
      $("#autocomplete_serviceprovider").hide();
    }
});
//set selected autocomplte value to textbox
function activate_serviceprovider (element,checkval,checkname) {
  $("#serviceproviderval").val(checkname);
  $("#serviceprovider").val(checkval);
}
//Autocomplete Script ends

$(function() {
  $(".grid-table-rpt").hide();
  getServiceProviderReportFilters();
});