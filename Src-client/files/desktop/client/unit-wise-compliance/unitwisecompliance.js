var unitWiseComplianceList;
var countriesList;
var domainsList;
var businessGroupsList;
var legalEntitiesList;
var divisionsList
var unitsList;
var assigneesList;

var sno = 0;
var fullArrayList = [];

var s_endCount = 0;
var totalRecord;
var lastBG = '';
var lastLE = '';
var lastDV = '';
var lastUnit = '';

var country = null;
var domain = null;
var businessgroup = null;
var legalentity = null;
var division = null;
var unit = null;
var assignee = null;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//get report filter from api
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

//display businessgroup title
function bgList(data){
  var bg = '-';
  if(data["business_group_name"] != null) bg = data["business_group_name"];
  var dv = '-';
  if( data["division_name"] != null) dv = data["division_name"];
  var le = data["legal_entity_name"];

  if(lastBG != bg || lastLE != le || lastDv != dv){
    var country = $("#country").find('option:selected').text();
    var domain = $("#domainval").val();
    $(".country").text(country);
    $(".domain").text(domain);
    var tableRow=$('#unit-list-templates .table-unit-list .table-row-unit-list');
    var clone=tableRow.clone();
    $('.tbl_country', clone).text(country);
    $('.tbl_domain', clone).text(domain);  
    $('.tbl_businessgroup', clone).text(bg);
    $('.tbl_division', clone).text(dv);
    $('.tbl_legalentity', clone).text(le);
    $('.tbody-unit').append(clone);
    var tableRow1=$('#unit-head-templates .table-unit-head .table-row-unit-head');
    var clone1=tableRow1.clone();
    $('.tbody-unit').append(clone1);
    lastBG = bg;
    lastDv = dv;
    lastLE = le;
    lastUnit = '';
  }
}

//display unit name
function unitList(data){
  if(lastUnit != data){
    var uAddress = data;
    /*if(compliancelists[compliancelist].length > 0)
      uAddress = compliancelists[compliancelist][0]["unit_address"]*/
    var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
    var clone2=tableRow2.clone();
    $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;"> <abbr class="page-load tipso_style" title="'+ uAddress +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+data+'</div>');
    $('.tbody-unit').append(clone2);
    lastUnit = data;
  }
}

//display complaince details
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

    if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);
    
    triggerdate +=  tDays + " Day(s), ";
    statutorydate +=  sMonth +' '+ sDay + ', ';
  }

  if(data["statutory_dates"].length <= 1){
  	statutorydate = '';
  }

  var summary = data["summary"];
  if(statutorydate.trim() != ''){
    statutorydate = statutorydate.replace(/,\s*$/, "");
  }
  if(triggerdate.trim() != ''){
    triggerdate = triggerdate.replace(/,\s*$/, "");
  }
  if(summary != null){
    if(statutorydate.trim() != ''){
      statutorydate = summary + ' ('+statutorydate+')';
    }else{
      statutorydate = summary;
    }
  }

  var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
  var clone3=tableRow3.clone();
  var cDescription = data["description"];
  $('.tbl_sno', clone3).text(sno+1);
  $('.tbl_compliance', clone3).html('<abbr class="page-load tipso_style" title="'+ cDescription +'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+data["compliance_name"]);
  $('.tbl_frequency', clone3).text(data["compliance_frequency"]);
  $('.tbl_statutorydate', clone3).text(statutorydate);
  $('.tbl_triggerbefore', clone3).text(triggerdate);
  var dDate = '-';
  if(data["due_date"] != null) dDate = data["due_date"];
  $('.tbl_duedate', clone3).text(dDate);
  var vDate = '-';
  if(data["validity_date"] != null) vDate = data["validity_date"];
  $('.tbl_validitydate', clone3).text(vDate);
  $('.tbody-unit').append(clone3);
  sno++;
}


//split and save full list into array
function loadArray(complianceList) {   
  $.each(complianceList, function(i, val){
      var list = complianceList[i];
      var list_unit = val["unit_wise_compliances"]
      delete val["unit_wise_compliances"];         
      fullArrayList.push(list);

      $.each(list_unit, function(i1, val1){
        fullArrayList.push(i1);
        var list_c = list_unit[i1];
        $.each(list_c, function(i2, val2){
          fullArrayList.push(list_c[i2]);
        })   
      });
  });

 
  var sub_keys_list = fullArrayList;
  //filterList();
  for(var y = 0;  y < fullArrayList.length; y++){
    if(sub_keys_list[y] !=  undefined){
      if(Object.keys(sub_keys_list[y])[0] == "division_name"){
        bgList(sub_keys_list[y]);
      }    
      else if(Object.keys(sub_keys_list[y])[0] == "due_date"){
        complianceListArray(sub_keys_list[y]);
      }else{
        unitList(sub_keys_list[y]);
      } 
    } 
  }

  if(totalRecord == 0){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-unit').append(clone4);
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

//pagination process
$('#pagination').click(function(){
  displayLoader();
  s_endCount = sno;
  fullArrayList = [];
  clearMessage();

  function onSuccess(data){
    unitWiseComplianceList = data["compliance_list"];
    totalRecord = data["total_count"];
    loadArray(unitWiseComplianceList);
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getUnitwisecomplianceReport( parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), parseInt(assignee), s_endCount,
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    });
});


//get unitwise compliance report from api
$("#submit").click(function(){ 
  displayLoader();
  country = $("#country").val();
  domain = $("#domain").val();
  businessgroup = null;
  legalentity = null;
  division = null;
  unit = null;
  assignee = null;
  if($("#businessgroup").val() != '') businessgroup = $("#businessgroup").val();
  if($("#legalentity").val() != '') legalentity = $("#legalentity").val();
  if($("#division").val() != '') division = $("#division").val();
  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#assignee").val() != '') assignee = $("#assignee").val();
  $(".tbody-unit").find("tbody").remove();
  $('.compliance_count').text('');
  lastUnit = '';
  lastBG = '';
  lastLE = '';
  lastDv = '';
  sno = 0;
  s_endCount = 0;
  fullArrayList = [];
  clearMessage();

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
  else{
      function onSuccess(data){
        $(".grid-table-rpt").show();
        unitWiseComplianceList = data["compliance_list"];
        totalRecord = data["total_count"];
        loadArray(unitWiseComplianceList);
        hideLoader();
      }
      function onFailure(error){
        displayMessage(error);
        hideLoader();
      }
      client_mirror.getUnitwisecomplianceReport( parseInt(country), parseInt(domain), parseInt(businessgroup), parseInt(legalentity), parseInt(division), parseInt(unit), parseInt(assignee), s_endCount,
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
$("#domainval").keyup(function(e){
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});


//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val){
  $("#businessgroupval").val(val[1]);
  $("#businessgroup").val(val[0]);
   $("#businessgroupval").focus();
}

//load businessgroup form list in autocomplete text box  
$("#businessgroupval").keyup(function(e){
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(e, textval, businessGroupsList, function(val){
    onBusinessGroupSuccess(val)
  })
});

//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val){
  $("#legalentityval").val(val[1]);
  $("#legalentity").val(val[0]);
  $("#legalentityval").focus();
}

//load legalentity form list in autocomplete text box  
$("#legalentityval").keyup(function(e){
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(e, textval, legalEntitiesList, function(val){
    onLegalEntitySuccess(val)
  })
});

//retrive division form autocomplete value
function onDivisionSuccess(val){
  $("#divisionval").val(val[1]);
  $("#division").val(val[0]);
  $("#divisionval").focus();
}

//load division form list in autocomplete text box  
$("#divisionval").keyup(function(e){
  var textval = $(this).val();
  getClientDivisionAutocomplete(e, textval, divisionsList, function(val){
    onDivisionSuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unit").val(val[0]);
  $("#unitval").focus();
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(e){
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = $("#domain").val();
  getUnitAutocomplete(e, textval, unitsList, function(val){
    onUnitSuccess(val)
  })
});

//retrive user autocomplete value
function onUserSuccess(val){
  $("#assigneeval").val(val[1]);
  $("#assignee").val(val[0]);
  $("#assigneeval").focus();
}

//load user list in autocomplete text box  
$("#assigneeval").keyup(function(e){
  var textval = $(this).val();
  getUserAutocomplete(e, textval, assigneesList, function(val){
    onUserSuccess(val)
  })
});


//Autocomplete Script ends

//initialization
$(function() {
  $(".grid-table-rpt").hide();
  getClientReportFilters();
  $('#country').focus();
});

//tool tip
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