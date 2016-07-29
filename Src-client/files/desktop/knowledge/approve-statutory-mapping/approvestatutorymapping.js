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


//get statutory mapping data from api
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
    displayMessage(error);
  }
  mirror.getApproveStatutoryMapings(
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

//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
  $("#countryval").focus();
}

//load country list in autocomplete text box
$("#countryval").keyup(function(e){
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, function(val){
    onCountrySuccess(val)
  })
});

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

//retrive industry autocomplete value
function onIndustrySuccess(val){
  $("#industryval").val(val[1]);
  $("#industry").val(val[0]);
  $("#industryval").focus();
}
//load industry list in autocomplete textbox
$("#industryval").keyup(function(e){
  var textval = $(this).val();
  getIndustryAutocomplete(e, textval, industriesList, function(val){
    onIndustrySuccess(val)
  })
});

//retrive statutorynature autocomplete value
function onStatutoryNatureSuccess(val){
  $("#statutorynatureval").val(val[1]);
  $("#statutorynature").val(val[0]);
  $("#statutorynatureval").focus();
}
//load statutorynature list in autocomplete textbox
$("#statutorynatureval").keyup(function(e){
  var textval = $(this).val();
  getStatutoryNatureAutocomplete(e, textval, statutoryNaturesList, function(val){
    onStatutoryNatureSuccess(val)
  })
});
//Autocomplete Script ends

//load statutories for approval
function loadApproveStatutory(){
  var country = $("#country").val().trim();
  var domain = $("#domain").val().trim();
  var industry = $("#industry").val();
  var statutorynature = $("#statutorynature").val();
  if(country.length == 0){
    displayMessage(message.country_required);
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);
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
      //displayMessage("");
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
        statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i]+ '<br>';
        statutoryprovision = statutoryprovision + statutoryMappingsList[entity]["statutory_mappings"][i];
      }
      statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/knowledge/images/right_arrow.png\'/> ');

      var applicableLocation = '';

      for(var i=0; i<statutoryMappingsList[entity]["geography_mappings"].length; i++){
        applicableLocation = applicableLocation + statutoryMappingsList[entity]["geography_mappings"][i] + '<br>';
      }
      applicableLocation = applicableLocation.replace(/>>/gi,' <img src=\'/knowledge/images/right_arrow.png\'/> ');

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
          complianceNames = complianceNames + '<a href="#popup1" class="new-link" onclick="disppopup('+statutorymappingId+','+i+',this)">'+(i+1)+'. '+statutoryMappingsList[entity]["compliance_names"][i]['compliance_name']+'</a> <br>';
        }
        $('.compliancetask', clone).html(complianceNames);
        $('.applicablelocation', clone).html(applicableLocation);
        $('.action', clone).html('<input type="hidden" id="mapping_id'+j+'" value="'+statutorymappingId+'" /> <input type="hidden" id="statutoryprovision'+j+'" value="'+statutoryprovision.replace(/"/gi,'##')+'" /> <select class="input-box" id="action'+j+'" onchange="dispreason('+j+')"></select>');
        $('.reason', clone).html('<textarea class="input-box userreason" maxlength="500" id="notifyreason'+j+'" placeholder="Enter notification text" style="height:50px;display:none;"></textarea><span style="font-size:0.75em;display:none;" id="notifynote'+j+'"> <br> (max 500 characters)</span> <input type="text" maxlength="500" style="display:none;" id="reason'+j+'" class="input-box userreason" placeholder="Enter reason" />');
        $('.tbody-statutorymapping-list').append(clone);

        for (var status in approvalStatusList) {
          var option = $("<option></option>");
          option.val(approvalStatusList[status]["approval_status_id"]);
          var approveStatus = approvalStatusList[status]["approval_status"];
          var updatedStatus = '';
          if( approveStatus == 'Pending' ){
            updatedStatus = approveStatus.replace("Pending", "Select");
          }else if( approveStatus == 'Approved' ){
            updatedStatus = approveStatus.replace("Approved", "Approve");
          }else if( approveStatus == 'Rejected' ){
            updatedStatus = approveStatus.replace("Rejected", "Reject");
          }else if( approveStatus == 'Approved & Notified' ){
            updatedStatus = approveStatus.replace("Approved & Notified", "Approve & Notify");
          }
          option.text( updatedStatus );
          $("#action"+j).append(option);
        }
        j = j + 1;
        $('.userreason').on('input', function (e) {
	      this.value = isCommon($(this));
	  	});
      }
      $('#saverecord').show();
    }
    if(j <= 1){
      $(".grid-table").show();
      var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
      var clone4=tableRow4.clone();
      $('.no_records', clone4).text('No Compliance Found');
      $('.tbody-statutorymapping-list').append(clone4);
      $('#saverecord').hide();
    }
  }
}
$("#submit").click(function(){
  loadApproveStatutory();
});

//display popup with details
function disppopup(sm_id,compliance_id,element){
  $("#popup1").show();
  $(element).removeClass("new-link");

  var sm = statutoryMappingsList[sm_id];
  var compliances = sm["compliances"];
  var statutoryMappings='';
  for(var i=0; i<sm["statutory_mappings"].length; i++){
    statutoryMappings = statutoryMappings + sm["statutory_mappings"][i];
  }
  var frequency = '';
  $.each(complianceFrequencyList, function(index, value) {
  if (value.frequency_id == compliances[compliance_id]["f_id"]) {
      frequency = value.frequency;
  }
  });

  var sdateDesc = '';
  var duration = compliances[compliance_id]["duration"];
  var duration_type_id = compliances[compliance_id]["d_type_id"];
  var repeats_every = compliances[compliance_id]["r_every"];
  var repeats_type_id = compliances[compliance_id]["r_type_id"];
  var statutory_date =  compliances[compliance_id]["statu_dates"];
  var statutorydate = '';
  var duration_type = '';
  var repeats_type = '';

  if(frequency == "On Occurrence"){
    if(duration_type_id == 1){
      duration_type = 'Day(s)';
    }else{
      duration_type = 'Hour(s)';
    }
    sdateDesc = 'To complete with in ' +duration + ' ' + duration_type;
  }
  else if(frequency == 'One Time'){
    sdateDesc = '';
  }
  else{
    if(repeats_type_id == 1){
      repeats_type = 'Day(s)';
    }else if(repeats_type_id == 2){
      repeats_type = 'Month(s)';
    }else{
      repeats_type = 'Year(s)';
    }
    sdateDesc = 'Repeats every ' + repeats_every + ' ' + repeats_type;
  }

  if(frequency != "On Occurrence"){
    for(z = 0; z < statutory_date.length; z++){
    var sDay = '';
    if(statutory_date[z]["statutory_date"] != null) sDay = statutory_date[z]["statutory_date"];
    var sMonth = '';
    if(statutory_date[z]["statutory_month"] != null) sMonth = statutory_date[z]["statutory_month"];

    if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);

    statutorydate +=  sMonth +' '+ sDay +' ';
    }
    if(sdateDesc != ''){
      if(statutorydate.trim() == ''){
        statutorydate = sdateDesc;
      }else{
        statutorydate = sdateDesc + ' ( '+statutorydate+' )';
      }
    }
  }else{
    statutorydate = sdateDesc;
  }

  $(".popup_statutory").html(compliances[compliance_id]["s_provision"]);
  $(".popup_statutorynature").text(sm["statutory_nature_name"]);
  $(".popup_compliancetask").html(sm["compliance_names"][compliance_id]["compliance_name"]);
  $(".popup_compliancedescription").text(compliances[compliance_id]["description"]);
  $(".popup_penalconsequences").text(compliances[compliance_id]["p_consequences"]);
  $(".popup_compliancefrequency").text(frequency);
  $(".popup_complianceoccurance").text(statutorydate);
  $(".popup_applicablelocation").text(sm["geography_mappings"]);
}

//display reason select box according to action selection
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

//reload statutories for approval after save process
function reloadStatutoryMapping(){
  function onSuccess(data){
      statutoryMappingsList = data["statutory_mappings"];
      loadApproveStatutory();
    }
      function onFailure(error){
        displayMessage(error);
    }
    mirror.getApproveStatutoryMapings(
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

//save statutory mapping approval
$("#saverecord").click(function(){
  approvelist = [];
  for(var i=1; i<j; i++){
    var statutory_mapping_id = parseInt($("#mapping_id"+i).val());
    var statutory_provision = $("#statutoryprovision"+i).val().replace(/##/gi,'"');
    var approval_status = parseInt($("#action"+i).val());
    var rejected_reason = $("#reason"+i).val().trim();
    var notification_text = $("#notifyreason"+i).val().trim();
    if(approval_status != '0'){
      var reason = '';
      if(approval_status == 2){
        reason = rejected_reason;
      }else if(approval_status == 3){
        reason = notification_text;
      }
      var checkLength = approveMappingValidate(reason);
      if(checkLength){
        if(approval_status == 2 && rejected_reason.length == 0){
          displayMessage(message.reason_required);
          return false;
        }else if(approval_status == 3 && notification_text.length == 0){
          displayMessage(message.reason_required);
          return false;
        }else{
          approveStatutoryList = mirror.approveStatutoryList(statutory_mapping_id, statutory_provision, approval_status, rejected_reason, notification_text);
          approvelist.push(approveStatutoryList);
        }
      }else{
        return false;
      }
    }
  }

  if(approvelist.length == 0){
    displayMessage(message.action_selection_required);
    return false;
  }
  function onSuccess(response) {
    $(".grid-table").hide();
    displayMessage(message.action_selection_success);
    reloadStatutoryMapping();
  }
  function onFailure(error, response){
    if (error == "TransactionFailed") {
      displayMessage(response["message"])
    }
    else {
      displayMessage(error);
    }
  }
  mirror.approveStatutoryMapping(approvelist,
    function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error, response);
        }
      });
});

//initialization
$(function() {
  getStatutoryMappings();
  $("#countryval").focus();
});