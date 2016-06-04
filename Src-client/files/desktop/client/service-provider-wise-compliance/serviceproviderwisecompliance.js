var serviceProviderWiseComplianceList;
var countriesList;
var domainsList;
var levelOneStatutoriesList;
var unitsList;
var serviceProvidersList;
var sno = 0;
var service_sno = 0;
var totalRecord;
var lastSP = '';
var lastUnit = '';

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//get report filter data
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

//display compliance details in view page
function loadresult(filterList){
  for(var entity in filterList){
    var sp_name = filterList[entity]["service_provider_name"];
    if(sp_name != null || sp_name != ''){
      if(lastSP != sp_name){
        var tableRow1=$('#serviceprovider-head-templates .table-serviceprovider-head .table-row-serviceprovider-headvalue');
        var clone1=tableRow1.clone();
        service_sno = service_sno + 1;
        $('.tbl_sp_count', clone1).text(service_sno);
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

        lastSP = sp_name;
        lastUnit = '';
      }
    
      var compliancelists = filterList[entity]["unit_wise_compliance"];
      for(var compliancelist in compliancelists){
        var uAddress = '';
        if(compliancelists[compliancelist].length > 0)
          uAddress = compliancelists[compliancelist][0]["unit_address"];

        if(lastUnit != compliancelist){
          var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
          var clone2=tableRow2.clone();
          $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;"> <abbr class="page-load tipso_style" title="'+ uAddress +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliancelist+'</div>');
          $('.tbody-serviceprovider').append(clone2);
          lastUnit = compliancelist
        }
      
        
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

            if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);

            triggerdate +=  tDays + " Days" + ', ';
            statutorydate +=  sDay + ' - ' + sMonth +', ';
          }

          if(statutorydate.trim() != '') statutorydate = statutorydate.replace(/,\s*$/, "");
          if(triggerdate.trim() != '') triggerdate = triggerdate.replace(/,\s*$/, "");

          var summary = compliancelists[compliancelist][i]["summary"];
          if(summary != null){
            if(statutorydate.trim() != ''){
              statutorydate = summary + ' ('+statutorydate+')';
            }else{
              statutorydate = summary;
            }
          }
          
          var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
          var clone3=tableRow3.clone();
          var cDescription = compliancelists[compliancelist][i]["description"];
          sno = sno+1;
          $('.tbl_sno', clone3).text(sno);
          $('.tbl_compliance', clone3).html(compliancelists[compliancelist][i]["compliance_name"]);
          $('.tbl_description', clone3).text(cDescription);
          $('.tbl_statutorydate', clone3).text(statutorydate);
          $('.tbl_triggerbefore', clone3).text(triggerdate);
          var dDate = '-';
          if(compliancelists[compliancelist][i]["due_date"] != null) dDate = compliancelists[compliancelist][i]["due_date"];
          $('.tbl_duedate', clone3).text(dDate);
          
          var vDate = '-';
          if(compliancelists[compliancelist][i]["validity_date"] != null) vDate = compliancelists[compliancelist][i]["validity_date"];
          $('.tbl_validitydate', clone3).text(vDate);
          $('.tbody-serviceprovider').append(clone3);
        }
      } 
    }    
  }  

  if(totalRecord == 0){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-serviceprovider').append(clone4);
    $('#pagination').hide();
    $('.compliance_count').text('');
  }else{
    $('.compliance_count').text("Showing " + 1 + " to " + sno + " of " + totalRecord);
    if(sno >= totalRecord){
      $('#pagination').hide();
    }else{
      $('#pagination').show();
    }
  }
}

//get report data from api
function loadCompliance(reportType){ 
  displayLoader();
  var country = $("#country").val();
  var domain = $("#domain").val();
  var act = $("#act").val().trim();
  var unit = null;
  var serviceprovider = null;

  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#serviceprovider").val() != '') serviceprovider = $("#serviceprovider").val();

  if(country.length == 0){
    displayMessage(message.country_required);
    $(".grid-table-rpt").hide();
    hideLoader();
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);
    $(".grid-table-rpt").hide();  
    hideLoader();
  }
  else if(act.length == 0){
    displayMessage(message.act_required);
    $(".grid-table-rpt").hide();  
    hideLoader();
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
        totalRecord = data["total_count"];
        $(".grid-table-rpt").show();
        if(sno == 0){
          var country = $("#country").find('option:selected').text();
          var domain = $("#domainval").val();
          var act = $("#actval").val();
          var tableRow=$('#serviceprovider-list-templates .table-serviceprovider-list .table-row-serviceprovider-list');
          var clone=tableRow.clone();
          $('.tbl_country', clone).text(country);
          $('.tbl_domain', clone).text(domain);
          $('.tbl_act', clone).text(act);
          $('.tbody-serviceprovider').append(clone);
          var tableRow5=$('#serviceprovider-head-templates .table-serviceprovider-head .table-row-serviceprovider-head');
          var clone5=tableRow5.clone();
          $('.tbody-serviceprovider').append(clone5);
        }
        
        loadresult(serviceProviderWiseComplianceList);

        if(reportType == "export"){
          var download_url = data["link"];
          window.open(download_url, '_blank');
          // client_mirror.exportToCSV(data, 
          // function (error, response) {
          //   if (error == null){
          //     var download_url = response["link"];
          //     window.open(download_url, '_blank');
          //   }
          //   else {
          //     displayMessage(error);
          //   }
          // });
        }
        hideLoader();
      }
      function onFailure(error){
        onFailure(error);
        hideLoader();
      }

      var csv = true
      if(reportType == "show"){
        csv = false
      }

      client_mirror.getServiceProviderWiseCompliance( parseInt(country), parseInt(domain), act, parseInt(unit), parseInt(serviceprovider), sno, csv,
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
  sno = 0;
  service_sno = 0;
  lastSP = '';
  lastUnit = '';
  $(".tbody-serviceprovider").find("tbody").remove();

  loadCompliance("show")
});

$("#export").click(function(){ 
  loadCompliance("export")
});

//pagination process
$('#pagination').click(function(){
  displayLoader();
  loadCompliance("show")
});

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
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

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
  $("#domainval").focus();
}
//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#actval").val(val[1]);
  $("#act").val(val[0].replace(/##/gi,'"'));
  $("#actval").focus();
}
//load statutory list in autocomplete textbox  
$("#actval").keyup(function(){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(textval, levelOneStatutoriesList, function(val){
    onStatutorySuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unit").val(val[0]);
  $("#unitval").focus();
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  var cId = $("#country").val();
  var dId = $("#domain").val();
  getUnitAutocomplete(textval, unitsList, cId, dId, function(val){
    onUnitSuccess(val)
  })
});


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
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_serviceprovider(this)">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_serviceprovider').append(str);
    //$("#serviceprovider").val('');
    }else{
      $("#serviceprovider").val('');
      $("#autocomplete_serviceprovider").hide();
    }
});
//set selected autocomplte value to textbox
function activate_serviceprovider (element) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $("#serviceproviderval").val(checkname);
  $("#serviceprovider").val(checkval);
  $("#serviceproviderval").focus();
}
//Autocomplete Script ends

//initialization
$(function() {
  $(".grid-table-rpt").hide();
  getServiceProviderReportFilters();
  $("#country").focus();
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