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
  function onSuccess(data){
    industriesList = data["industries"];
    statutoryLevelsList = data["statutory_levels"];
    statutoriesList = data["statutories"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    geographyLevelsList = data["geography_levels"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    statutoryMappingsList = data["statutory_mappings"];
    tempstatutoryMappingsList = data["statutory_mappings"];
    complianceFrequencyList = data["compliance_frequency"];
    approvalStatusList = data["compliance_approval_status"]
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
    }
});
//set selected autocomplte value to textbox
function activate_statutorynature (element,checkval,checkname) {
  $("#statutorynatureval").val(checkname);
  $("#statutorynature").val(checkval);
}

//Autocomplete Script ends
$("#submit").click(function(){
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
    $(".grid-table").show();
    j = 1;
    var statutorymappingId = 0;
    var industryName = '';
    var statutoryNatureName = '';
    var approvalStatus = '';
    var applicableLocation = '';
    var isActive = 0;
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
      var statutoryMappings='';
      var statutoryprovision = '';
      for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
        statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
        statutoryprovision = statutoryprovision + statutoryMappingsList[entity]["statutory_mappings"][i];
      }
      statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
      applicableLocation = statutoryMappingsList[entity]["geography_mappings"];
      isActive = statutoryMappingsList[entity]["is_active"];
      approvalStatus = statutoryMappingsList[entity]["approval_status"];
      conditionResult = (approvalStatus == '0' && isActive == '1' && countryId == country && domainId == domain);
      if(statutorynature != ""){
        conditionResult = conditionResult && (statutorynature == statutoryNatureId);
      }
      if(industry != ""){
        conditionResult = conditionResult && ($.inArray(parseInt(industry), industryIds) >= 0);
      }
      if(conditionResult){
      var tableRow=$('#templates .table-statutorymapping .table-row');
      var clone=tableRow.clone();
      $('.industry', clone).text(industryName);
      $('.statutorynature', clone).text(statutoryNatureName);
      $('.statutory', clone).html(statutoryMappings);
      var complianceNames='';
      for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
        complianceNames = complianceNames + '<a href="#popup1" onclick="disppopup('+statutorymappingId+','+i+')">'+(i+1)+'. '+statutoryMappingsList[entity]["compliance_names"][i]+'</a>' + " <br>";
      }
      $('.compliancetask', clone).html(complianceNames);
      $('.applicablelocation', clone).text(applicableLocation);
      $('.action', clone).html('<input type="hidden" id="mapping_id'+j+'" value="'+statutorymappingId+'" /> <input type="hidden" id="statutoryprovision'+j+'" value="'+statutoryprovision+'" /> <select class="input-box" id="action'+j+'" onchange="dispreason('+j+')"></select>');
      $('.reason', clone).html('<textarea class="input-box" id="notifyreason'+j+'" placeholder="Enter notification text" style="height:50px;display:none;"></textarea><br><span style="font-size:0.75em;display:none;" id="notifynote'+j+'">(max 500 characters)</span> <input type="text" style="display:none;" id="reason'+j+'" class="input-box" placeholder="Enter reason" />');
      $('.tbody-statutorymapping-list').append(clone);
      //load compliance frequency selectbox

      for (var status in approvalStatusList) {
      var option = $("<option></option>");
      option.val(approvalStatusList[status]["approval_status_id"]);
      option.text(approvalStatusList[status]["approval_status"]);
      $("#action"+j).append(option);
      }
      j = j + 1;
    }
  }
}
});

function disppopup(sm_id,compliance_id){
  $("#popup1").show();
  var compliances = statutoryMappingsList[sm_id]["compliances"];
  var statutoryMappings='';
  for(var i=0; i<statutoryMappingsList[sm_id]["statutory_mappings"].length; i++){
    statutoryMappings = statutoryMappings + statutoryMappingsList[sm_id]["statutory_mappings"][i] + " <br>";
  }
  var frequency = '';
  $.each(complianceFrequencyList, function(index, value) {
  if (value.frequency_id == compliances[compliance_id]["frequency_id"]) {
      frequency = value.frequency;
  }
  });
  $(".popup_statutory").html(statutoryMappings);
  $(".popup_statutorynature").text(statutoryMappingsList[sm_id]["statutory_nature_name"]);
  $(".popup_compliancetask").html(statutoryMappingsList[sm_id]["compliance_names"][compliance_id]);
  $(".popup_compliancedescription").text(compliances[compliance_id]["description"]);
  $(".popup_penalconsequences").text(compliances[compliance_id]["penal_consequences"]);
  $(".popup_compliancefrequency").text(frequency);
  $(".popup_complianceoccurance").text("");
  $(".popup_applicablelocation").text(statutoryMappingsList[sm_id]["geography_mappings"]);
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

  function onSuccess(response) {
    getStatutoryMappings();
    jQuery('#submit').focus().click();
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