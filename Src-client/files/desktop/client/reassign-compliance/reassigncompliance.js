var compliancesList;
var usersList;
var unitsList;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$(".btn-submit").click(function(){
  $("#compliance-list").show();
  load_compliances();
  /*$("#domain-add").show();
  $("#domainname").val('');
  $("#domainid").val('');
  $(".error-message").html('');*/
});

function load_compliances () {
  var j = 1;
  $(".tbody-reassign-compliances-list").find("tr").remove();
    for(var entity in compliancesList) {
        
        var givenUserId = null;
        var givenUnitId = null;

        if($("#assignee").val() != ''){
          givenUserId = $("#assignee").val();
        }
        
        if($("#seatingunit").val() != ''){
          givenUnitId = $("#seatingunit").val();
        }

      
        var userId = compliancesList[entity]["user_id"];
        var seatingUnit = compliancesList[entity]["seating_unit"];

        //if( (userId == givenUserId || givenUserId = null) && (seatingUnit == givenUnitId || givenUnitId = null)){
          var userName = compliancesList[entity]["user_name"];
          var noOfCompliances = compliancesList[entity]["no_of_compliances"];

          var tableRow1=$('#templates .table-compliances .table-row');
          var clone1=tableRow1.clone();
          $('.sno', clone1).text(j);
          $('.assigneename', clone1).text(userName);
          $('.seatingunit', clone1).text(seatingUnit);
          $('.noofcompliance', clone1).text(noOfCompliances);
          //$('.action', clone1).html('<input type="button" class="btn-submit" value="Start" onclick="submitOnOccurence('+complianceId+','+j+','+unitId+',\''+completeDays+'\')"/>');
          $('.action', clone1).html('<input type="submit" value="Reassign" class="btn-save" style="width:auto;" onclick=""/>');
          $('.tbody-reassign-compliances-list').append(clone1);
          j = j + 1;
        }
   // }
}

/* function submitOnOccurence(complianceId, count, unitId, complete_within_days){
  /*var startdate = $('#startdate'+count).val();
  if(startdate != ''){
    function onSuccess(data){
      //displayMessage("Task started successfully");
      //getOnOccuranceCompliances ();
      $('#startdate'+count).val('');
      window.location.href='/compliance-task-details'
    }
    function onFailure(error){
      displayMessage(error)
    }
    client_mirror.startOnOccurrenceCompliance(complianceId, startdate, unitId, complete_within_days, 
      function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    }
    );
  }else{
    displayMessage("Start date is required");
    return false;
  }*/
  



function getReassignCompliances () {
  function onSuccess(data){
    compliancesList = data["compliances"];
    //load_compliances(compliancesList);
  }
  function onFailure(error){
  }
  client_mirror.getUserwiseCompliances(
    function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
  );
  compliancesList = [
            {
                "user_id": 1,
                "user_name": "EMPLOYEE_CODE-EMPLOYEE",
                "seating_unit": "UNIT_CODE - UNIT_NAME",
                "address": "ADDRESS",
                "no_of_compliances": 9,
                "units":[
                    {
                        "unit_id": 1,
                        "unit_name": "UNIT_CODE - UNIT_NAME",
                        "address": "ADDRESS",
                        "statutories":[
                            {
                                "level_1_statutory_name": "LEVEL_1_STATUTORY_NAME",
                                "compliances": [
                                    {
                                        "compliance_history_id":1 ,
                                        "compliance_id": 1,
                                        "compliance_name":"DOCUMENT_NAME - COMPLIANCE_TASK_NAME",
                                        "description": "Description",
                                        "compliance_frequency": "COMPLIANCE_FREQUENCY",
                                        "statutory_date": [
                                            {
                                                "statutory_date": 1,
                                                "statutory_month": 12,
                                                "trigger_before_days": 7
                                            }
                                        ],
                                        "due_date": "01-09-2016"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ];
        

      usersList = [
      {
        "employee_code": "E1001", 
        "employee_id": 1, 
        "employee_name": "VijayKumar"
      }, 
      {
        "employee_code": "E009", 
        "employee_id": 2, 
        "employee_name": "usha"
      }, 
      {
        "employee_code": "Emp-123", 
        "employee_id": 3, 
        "employee_name": "Siva"
      }
    ];

    unitsList = [
      {
        "division_id": 1, 
        "unit_name": "Factory Unit I", 
        "business_group_id": 1, 
        "unit_code": "Tvs001", 
        "legal_entity_id": 1, 
        "unit_address": "address address", 
        "is_active": true, 
        "unit_id": 1
      }, 
      {
        "division_id": 1, 
        "unit_name": "TVS MADURAI", 
        "business_group_id": 2, 
        "unit_code": "UCODE-123", 
        "legal_entity_id": 1, 
        "unit_address": "345, Vinayaga Nagar, Anna Bus Stand, Madurai", 
        "is_active": true, 
        "unit_id": 2
      }
    ];
  
}

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocomplete_seatingunit").hide();
  $("#autocomplete_assignee").hide();
});


//Units-------------------------------------------------------------------------------------------
$("#seatingunitval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_seatingunit").show();
  var units = unitsList;
  var suggestions = [];
 $('#ulist_seatingunit').empty();
  if(textval.length>0){
    for(var i in units){
      if (~units[i]["unit_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],units[i]["unit_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_units(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_seatingunit').append(str);
    $("#seatingunit").val('');
    }else{
      $("#seatingunit").val('');
      $("#autocomplete_seatingunit").hide();
    }
});
//set selected autocomplte value to textbox
function activate_units (element,checkval,checkname) {
  $("#seatingunitval").val(checkname);
  $("#seatingunit").val(checkval);
}

//Assignee---------------------------------------------------
$("#assigneeval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_assignee").show();
  
  var assignees = usersList;
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

$(document).ready(function () {
  getReassignCompliances ();
});