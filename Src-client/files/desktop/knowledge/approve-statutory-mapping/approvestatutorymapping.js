var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var complianceFrequencyList;
var approvalStatusList;
var approvelist = [];
var j;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function getStatutoryMappings(){
  function onSuccessMaster(data){
    industriesList = data["industries"];
    statutoryLevelsList = data["statutory_levels"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    geographyLevelsList = data["geography_levels"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    statutoriesList = data["statutories"];
    complianceFrequencyList = data["compliance_frequency"];
    approvalStatusList = data["compliance_approval_status"]
  }
  function onFailureMaster(error){
  }
  mirror.getStatutoryMappingsMaster(
    function (error, response) {
      if (error == null){
        onSuccessMaster(response);
      }
      else {
        onFailureMaster(error);
      }
    }
  );

  function onSuccess(data){
    statutoryMappingsList = data["statutory_mappings"];
    tempstatutoryMappingsList = data["statutory_mappings"];
    
  }
  function onFailure(error){
  }
  mirror.getStatutoryMappings(
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

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide(); 
  $("#autocomplete_domain").hide();
  $("#autocomplete_industry").hide();
  $("#autocomplete_statutorynature").hide();
});

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  $("#autocompleteview").show();
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
    }else{
      $("#country").val('');
      $("#autocompleteview").hide();
    }
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);
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
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == 1) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
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

//load domain list in autocomplete text box  
$("#industryval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_industry").show();
  var industries = industriesList;
  var suggestions = [];
  $('#ulist_industry').empty();
  if(textval.length>0){
    for(var i in industries){
      if (~industries[i]["industry_name"].toLowerCase().indexOf(textval.toLowerCase()) && industries[i]["is_active"] == 1) suggestions.push([industries[i]["industry_id"],industries[i]["industry_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_industry(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_industry').append(str);
    $("#industry").val('');
    }else{
      $("#industry").val('');
      $("#autocomplete_industry").hide();
    }
});
//set selected autocomplte value to textbox
function activate_industry (element,checkval,checkname) {
  $("#industryval").val(checkname);
  $("#industry").val(checkval);
}


//load statutorynature list in autocomplete text box  
$("#statutorynatureval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_statutorynature").show();
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ulist_statutorynature').empty();
  if(textval.length>0){
    for(var i in statutorynatures){
      if (~statutorynatures[i]["statutory_nature_name"].toLowerCase().indexOf(textval.toLowerCase()) && statutorynatures[i]["is_active"] == 1) suggestions.push([statutorynatures[i]["statutory_nature_id"],statutorynatures[i]["statutory_nature_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_statutorynature(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_statutorynature').append(str);
    $("#statutorynature").val('');
    }else{
      $("#statutorynature").val('');
      $("#autocomplete_statutorynature").hide();
    }
});
//set selected autocomplte value to textbox
function activate_statutorynature (element,checkval,checkname) {
  $("#statutorynatureval").val(checkname);
  $("#statutorynature").val(checkval);
}

//Autocomplete Script ends

function loadApproveStatutory(){
  var country = $("#country").val().trim();
  var domain = $("#domain").val().trim();
  var industry = $("#industry").val();
  var statutorynature = $("#statutorynature").val();
  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");  
  }
  else{
    j = 1;
    var statutorymappingId = 0;
    var industryName = '';
    var statutoryNatureName = '';
    var approvalStatus = '';
    
    var isActive = false;
    var countryId = '';
    var domainId = '';
    var statutoryNatureId = '';
    var industryIds = [];
    $(".tbody-statutorymapping-list").find("tr").remove();
    for(var entity in statutoryMappingsList) {
      statutorymappingId = entity;
      countryId = statutoryMappingsList[entity]["country_id"];
      domainId = statutoryMappingsList[entity]["domain_id"];
      industryIds = statutoryMappingsList[entity]["industry_ids"];
      industryName = statutoryMappingsList[entity]["industry_names"];
      statutoryNatureName = statutoryMappingsList[entity]["statutory_nature_name"];
      statutoryNatureId = statutoryMappingsList[entity]["statutory_nature_id"];        
      var statutoryMappings='';
      var statutoryprovision = '';
      for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
        statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i];
        statutoryprovision = statutoryprovision + statutoryMappingsList[entity]["statutory_mappings"][i];
      }
      statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
      
      var applicableLocation = '';

      for(var i=0; i<statutoryMappingsList[entity]["geography_mappings"].length; i++){
        applicableLocation = applicableLocation + statutoryMappingsList[entity]["geography_mappings"][i];
      }
      applicableLocation = applicableLocation.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');

      isActive = statutoryMappingsList[entity]["is_active"];
      approvalStatus = statutoryMappingsList[entity]["approval_status"];
      conditionResult = (approvalStatus == '0' && isActive == true && countryId == country && domainId == domain);
      if(statutorynature != ""){
        conditionResult = conditionResult && (statutorynature == statutoryNatureId);
      }
      if(industry != ""){
        conditionResult = conditionResult && ($.inArray(parseInt(industry), industryIds) >= 0);
      }
      if(conditionResult){
        $(".grid-table").show();
        var tableRow=$('#templates .table-statutorymapping .table-row');
        var clone=tableRow.clone();
        $('.industry', clone).text(industryName);
        $('.statutorynature', clone).text(statutoryNatureName);
        $('.statutory', clone).html(statutoryMappings);
        var complianceNames='';
        for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
          complianceNames = complianceNames + '<a href="#popup1" onclick="disppopup('+statutorymappingId+','+i+')">'+(i+1)+'. '+statutoryMappingsList[entity]["compliance_names"][i]['compliance_name']+'</a> <br>';
        }
        $('.compliancetask', clone).html(complianceNames);
        $('.applicablelocation', clone).html(applicableLocation);
        $('.action', clone).html('<input type="hidden" id="mapping_id'+j+'" value="'+statutorymappingId+'" /> <input type="hidden" id="statutoryprovision'+j+'" value="'+statutoryprovision+'" /> <select class="input-box" id="action'+j+'" onchange="dispreason('+j+')"></select>');
        $('.reason', clone).html('<textarea class="input-box" id="notifyreason'+j+'" placeholder="Enter notification text" style="height:50px;display:none;"></textarea><span style="font-size:0.75em;display:none;" id="notifynote'+j+'"> <br> (max 500 characters)</span> <input type="text" maxlength="500" style="display:none;" id="reason'+j+'" class="input-box" placeholder="Enter reason" />');
        $('.tbody-statutorymapping-list').append(clone);

        for (var status in approvalStatusList) {
          var option = $("<option></option>");
          option.val(approvalStatusList[status]["approval_status_id"]);
          option.text(   approvalStatusList[status]["approval_status"].replace("Pending", "Select") );
          $("#action"+j).append(option);
        }
        j = j + 1;
      }
      $('#saverecord').show();
    }

    if(j <= 1){
    var norecordtableRow=$('#no-record-templates .font1 .norecord-table-row');
    var noclone=norecordtableRow.clone();
    $('.tbody-statutorymapping-list').append(noclone);
    $('#saverecord').hide();
    }

  }
}
$("#submit").click(function(){
  loadApproveStatutory();
});

function disppopup(sm_id,compliance_id){
  $("#popup1").show();
  var sm = statutoryMappingsList[sm_id];

  var compliances = sm["compliances"];
  var statutoryMappings='';
  for(var i=0; i<sm["statutory_mappings"].length; i++){
    statutoryMappings = statutoryMappings + sm["statutory_mappings"][i];
  }
  var frequency = '';
  $.each(complianceFrequencyList, function(index, value) {
  if (value.frequency_id == compliances[compliance_id]["frequency_id"]) {
      frequency = value.frequency;
  }
  });
  
  var sdateDesc = '';
  var statutorydate = '';
  var statutory_date =  compliances[compliance_id]["statutory_dates"];

  if(frequency == 'Periodical' || frequency == 'Review') sdateDesc = 'Every';
    for(j = 0; j < statutory_date.length; j++){
      var sDay = '';
      if(statutory_date[j]["statutory_date"] != null) sDay = statutory_date[j]["statutory_date"];

      var sMonth = '';
      if(statutory_date[j]["statutory_month"] != null) sMonth = statutory_date[j]["statutory_month"];

      var tDays = '';
      if(statutory_date[j]["trigger_before_days"] != null) tDays = statutory_date[j]["trigger_before_days"];

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
        
      //triggerdate +=  tDays + " Day(s)";
      statutorydate +=  sdateDesc + ' ' +sMonth +' '+ sDay;
    }

  
  $(".popup_statutory").html(statutoryMappings);
  $(".popup_statutorynature").text(sm["statutory_nature_name"]);
  $(".popup_compliancetask").html(sm["compliance_names"][compliance_id]["compliance_name"]);
  $(".popup_compliancedescription").text(compliances[compliance_id]["description"]);
  $(".popup_penalconsequences").text(compliances[compliance_id]["penal_consequences"]);
  $(".popup_compliancefrequency").text(frequency);
  $(".popup_complianceoccurance").text(statutorydate);
  $(".popup_applicablelocation").text(sm["geography_mappings"]);
}

function dispreason(j){
  if($("#action"+j).val() == '2'){
    $("#notifyreason"+j).hide();
    $("#notifynote"+j).hide();
    $("#reason"+j).show();
    $("#notifyreason"+j).val('');
    $("#notifynote"+j).val('');
  }else if($("#action"+j).val() == '3'){
    $("#notifyreason"+j).show();
    $("#notifynote"+j).show();
    $("#reason"+j).hide();
    $("#reason"+j).val('');
  }else{
    $("#notifyreason"+j).hide();
    $("#notifynote"+j).hide();
    $("#reason"+j).hide();
    $("#notifyreason"+j).val('');
    $("#notifynote"+j).val('');
    $("#reason"+j).val('');
  }
}

function reloadStatutoryMapping(){
  function onSuccess(data){
      statutoryMappingsList = data["statutory_mappings"];
      loadApproveStatutory();
    }
      function onFailure(error){
    }
    mirror.getStatutoryMappings(
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

$("#saverecord").click(function(){
  approvelist = [];
  for(var i=1; i<j; i++){
    var statutory_mapping_id = parseInt($("#mapping_id"+i).val()); 
    var statutory_provision = $("#statutoryprovision"+i).val();
    var approval_status = parseInt($("#action"+i).val()); 
    var rejected_reason = $("#reason"+i).val(); 
    var notification_text = $("#notifyreason"+i).val(); 
    if(approval_status != '0'){
      approveStatutoryList = mirror.approveStatutoryList(statutory_mapping_id, statutory_provision, approval_status, rejected_reason, notification_text);
      approvelist.push(approveStatutoryList);
    }
  }

  if(approvelist.length == 0){
    displayMessage("Atleast one action should be select");
    return false;
  }
  function onSuccess(response) {
    $(".grid-table").hide();
    displayMessage("Statutory Mapping successfully approved");
    reloadStatutoryMapping();
  }
  function onFailure(error){
    displayMessage(error);
  }
  mirror.approveStatutoryMapping(approvelist,
    function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
});

$(function() {
  getStatutoryMappings();
});