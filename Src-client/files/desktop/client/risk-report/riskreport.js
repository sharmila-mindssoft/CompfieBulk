var riskComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList
var unitsList;
var actList;
var totalRecord;


//get risk report filters from api
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

//load report data
function loadresult(complianceList){
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();
  var compliance_count=0;

  /*var tableRowStatus=$('#statutory-status-templates .table-unit-name .table-row-unit-name');
  var cloneStatus=tableRowStatus.clone();
  $('.tbl_statutory_status', cloneStatus).text('');
  $('.tbody-unit').append(cloneStatus);
  console.log(complianceList)*/

  for(var entity in complianceList){
    var tableRow=$('#unit-list-templates .table-unit-list .table-row-unit-list');
    var clone=tableRow.clone();
    $('.tbl_country', clone).text(country);
    $('.tbl_domain', clone).text(domain);
    $('.tbl_businessgroup', clone).text(complianceList[entity]["business_group_name"]);
    $('.tbl_division', clone).text(complianceList[entity]["division_name"]);
    $('.tbl_legalentity', clone).text(complianceList[entity]["legal_entity_name"]);
    $('.tbody-unit').append(clone);

    var statutoryUnits = complianceList[entity]["level_1_statutory_wise_units"]
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
      }
    }
  }

  if(compliance_count == 0){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-unit').append(clone4);
  }

  if(compliance_count >= 1){
    var tableRowCount=$('#compliance-count-templates .table-unit-name .table-row-unit-name');
    var cloneCount=tableRowCount.clone();
    $('.compliance_count', cloneCount).text("Total : "+ (compliance_count) +" records");
    $('.tbody-unit').append(cloneCount);
  }
  //$('.compliance_count').text("Total : "+ (compliance_count) +" records");

}

//get risk report data from api
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
  statutory_status = $("#statutory_status").val();

  if(country.length == 0){
    displayMessage(message.country_required);
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);
  }
  else{
   
    function onSuccess(data){
      riskComplianceList = data['compliance_list'];
      totalRecord = data['total_record'];
      $(".grid-table-rpt").show();
      $(".tbody-unit").find("tbody").remove();
      loadresult(riskComplianceList);

      if(reportType == "export"){
        var download_url = data["link"];
        window.open(download_url, '_blank');
      }
    }
    function onFailure(error){
      onFailure(error);
    }
    var csv = true
    if(reportType == "show"){
      csv = false
    }
    client_mirror.getRiskReport(
      parseInt(country), parseInt(domain), parseInt(businessgroup),
      parseInt(legalentity), parseInt(division), parseInt(unit),
      act, parseInt(statutory_status), csv,
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

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val){
  $("#businessgroupval").val(val[1]);
  $("#businessgroup").val(val[0]);
}

//load businessgroup form list in autocomplete text box  
$("#businessgroupval").keyup(function(){
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(textval, businessGroupsList, function(val){
    onBusinessGroupSuccess(val)
  })
});

//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val){
  $("#legalentityval").val(val[1]);
  $("#legalentity").val(val[0]);
}

//load legalentity form list in autocomplete text box  
$("#legalentityval").keyup(function(){
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(textval, legalEntitiesList, function(val){
    onLegalEntitySuccess(val)
  })
});

//retrive division form autocomplete value
function onDivisionSuccess(val){
  $("#divisionval").val(val[1]);
  $("#division").val(val[0]);
}

//load division form list in autocomplete text box  
$("#divisionval").keyup(function(){
  var textval = $(this).val();
  getClientDivisionAutocomplete(textval, divisionsList, function(val){
    onDivisionSuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unit").val(val[0]);
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  getUnitAutocomplete(textval, unitsList, function(val){
    onUnitSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#actval").val(val[1]);
  $("#act").val(val[0].replace(/##/gi,'"'));
}
//load statutory list in autocomplete textbox  
$("#actval").keyup(function(){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(textval, actList, function(val){
    onStatutorySuccess(val)
  })
});

//Autocomplete Script ends

//initialization
$(function() {
  $(".grid-table-rpt").hide();
  getRiskReportFilters();
});