var compliancesList;
var usersList;
var unitsList;
var reassignUserId=null;
var cCount = 1;

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
});

function actstatus(element){
  var changestatusStatutories = '.statutoryclass'+$(element).val();
  if ($(element).is(":checked"))
  {
    $(changestatusStatutories).each(function() { 
      this.checked = true;           
    });
  }else{
    $(changestatusStatutories).each(function() {
      this.checked = false;                     
    });  
  }
}

function load_allcompliances(userId, userName){
  $("#reassign-view").hide();
  $("#reassign-detailview").show();
  $("#currentassignee").text(userName);
  reassignUserId = userId;
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tbody").remove();

  var userCompliances = compliancesList[reassignUserId];
  for(ucompliance in userCompliances){
    var userUnitwiseCompliance = userCompliances[ucompliance]["units"];
    for(var entity in userUnitwiseCompliance){
    var actname = '';
    var statutoriesList = userUnitwiseCompliance[entity]["statutories"];
    var uName = userUnitwiseCompliance[entity]["unit_name"];

    var tableRow3 = $('#head-templates .tbl_heading');
    var clone3 = tableRow3.clone();
    $('.heading', clone3).html(uName);
    $('.tbody-assignstatutory').append(clone3);

    for(var statutory in statutoriesList){
      actname = statutory;
      var acttableRow=$('#act-templates .font1 .tbody-heading');
      var clone=acttableRow.clone();
      $('.actname', clone).html('<input style="margin-top:5px" type="checkbox" checked="checked" id="act'+actCount+'" value="'+actCount+'" onclick="actstatus(this)"> <label for="act'+actCount+'">'+actname+'</label> <span><img src="/images/chevron_black_down.png"></span>');
      $('.tbody-assignstatutory').append(clone);
      $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      if(count==1){
        $('.accordion-content'+count).addClass("default");
      }
      
      var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
      var clone1=complianceHeadingtableRow.clone();
      $('.accordion-content'+count).append(clone1);

      var actList = statutoriesList[statutory];
      $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      for(var actentity in actList){    
        var compliance_id = actList[actentity]["compliance_id"];
        var compliance_name = actList[actentity]["compliance_name"];
        var compliance_description = actList[actentity]["description"];
        var frequency =  actList[actentity]["compliance_frequency"];
        var statutory_date =  actList[actentity]["statutory_date"];
        var due_date =  actList[actentity]["due_date"];
        var validity_date =  actList[actentity]["validity_date"];
        if(validity_date == null) validity_date = '';
        var triggerdate = '';
        var statutorydate = '';
        var sdateDesc = '';
        
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
            
          triggerdate +=  tDays + " Day(s)";
          statutorydate +=  sdateDesc + ' ' +sMonth +' '+ sDay;

        }
        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        $('.ckbox', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'">');
        
        $('.compliancetask', clone2).html('<abbr class="page-load" title="'+
          compliance_description+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliance_name);
        
        $('.compliancefrequency', clone2).text(frequency);
        
        $('.statutorydate', clone2).text(statutorydate);

        $('.triggerbefore', clone2).text(triggerdate);
        
        $('.duedate', clone2).html('<input type="text" value="'+due_date+'" class="input-box" readonly id="duedate'+statutoriesCount+'" />');
        
        $('.validitydate', clone2).text(validity_date);
      
        $('.accordion-content'+count).append(clone2);

        $("#duedate"+statutoriesCount).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            onClose: function( selectedDate ) {
            $( "#duedate"+statutoriesCount ).datepicker( "option", "minDate", selectedDate );
          }
        });
        statutoriesCount = statutoriesCount + 1;
      }  
      actCount = actCount + 1;
      count++;
    }
  }
}
  if(count <= 1){
    var norecordtableRow=$('#no-record-templates .font1');
    var noclone=norecordtableRow.clone();
    $('.tbody-assignstatutory').append(noclone);
    $('#activate-step-3').hide();
  }

  $(document).ready(function($) {
    $('#accordion').find('.accordion-toggle').click(function(){
      //Expand or collapse this panel
      $(this).next().slideToggle('fast');
      //Hide the other panels
      $(".accordion-content").not($(this).next()).slideUp('fast');
    });
  });
}


function load_UserCompliances(uCompliances, uId){
  for( compliance in uCompliances){
    var userName = "";
    var seatingUnitId = null;
    var seatingUnit = "";
    var noOfCompliances = uCompliances[compliance]["no_of_compliances"];

    for(var user in usersList){
      var unitusers = usersList[user];
      for(var user in unitusers){
        var userId= unitusers[user]["user_id"];
        if(userId == uId){
          userName = unitusers[user]["user_name"];
          seatingUnitId = unitusers[user]["seating_unit_id"]
        }
      }
    }
    for(var unit in unitsList){
        var userId= unitusers[user]["user_id"];
        if(unitsList[unit]["unit_id"] == seatingUnitId){
          seatingUnit = unitsList[unit]["unit_name"];
        }
    }

    var tableRow1=$('#templates .table-compliances .table-row');
    var clone1=tableRow1.clone();
    $('.sno', clone1).text(cCount);
    $('.assigneename', clone1).text(userName);
    $('.seatingunit', clone1).text(seatingUnit);
    $('.noofcompliance', clone1).text(noOfCompliances);
    $('.action', clone1).html('<input type="submit" value="Reassign" class="btn-save" style="width:auto;" onclick="load_allcompliances('+uId+ ',\''+userName+'\')"/>');
    $('.tbody-reassign-compliances-list').append(clone1);
    cCount = cCount + 1;
  }
}


function load_compliances () {
  var givenUserId = givenUserId = $("#assignee").val();
  var givenUnitId = givenUnitId = $("#seatingunit").val();;

  $(".tbody-reassign-compliances-list").find("tr").remove();

  if(givenUserId == '' && givenUnitId == ''){
    for(var entity in compliancesList) {
      var uCompliances = compliancesList[entity];
      load_UserCompliances(uCompliances, entity);
    }
  }
  else if(givenUserId != ''){
    var uCompliances = compliancesList[givenUserId];
    load_UserCompliances(uCompliances, givenUserId);
  }else if(givenUnitId != ''){
    var unitUsers = usersList[givenUnitId];
    for(var i in unitUsers){  
      var uId =  unitUsers[i]["user_id"];
      var uCompliances = compliancesList[uId];
      load_UserCompliances(uCompliances, uId);
    }
  }

  $('#assignee_unit').empty();
  $("#assignee_unit").append('<option value=""> Select </option>');
  $("#assignee_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#assignee_unit").append(option);
  }

  $('#concurrence_unit').empty();
  $("#concurrence_unit").append('<option value=""> Select </option>');
  $("#concurrence_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#concurrence_unit").append(option);
  }

  $('#approval_unit').empty();
  $("#approval_unit").append('<option value=""> Select </option>');
  $("#approval_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#approval_unit").append(option);
  }
}


function submitcompliance(){

  var assignComplianceAssigneeId = parseInt($('.assigneelist.active').attr('id'));
  var assignComplianceConcurrenceId = parseInt($('.concurrencelist.active').attr('id'));
  var assignComplianceApprovalId = parseInt($('.approvallist.active').attr('id'));
  var reason = $('#reason').val();
  reassignCompliance = [];
  var statutoriesCount= 1;
  var userCompliances = compliancesList[reassignUserId];

  for(ucompliance in userCompliances){
    var userUnitwiseCompliance = userCompliances[ucompliance]["units"];
    for(var entity in userUnitwiseCompliance){
    var statutoriesList = userUnitwiseCompliance[entity]["statutories"];
    for(var statutory in statutoriesList){
      var actList = statutoriesList[statutory];
      for(var actentity in actList){
        var complianceApplicable = false;
        if($('#statutory'+statutoriesCount).is(":checked")){
          complianceApplicable = true;
        }
        if(complianceApplicable){
          var compliance_id = actList[actentity]["compliance_id"];
          var due_date =  $('#duedate'+statutoriesCount).val();

          reassignComplianceData = client_mirror.assignCompliances(
            compliance_id, due_date
          );
          reassignCompliance.push(reassignComplianceData);
        }  
        statutoriesCount = statutoriesCount + 1;
      }  
    }
  }
}

  function onSuccess(data){
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-reassign-compliances-list").find("tbody").remove();
    getReassignCompliances();
    $("#reassign-view").show();
    $("#reassign-detailview").hide();
    $("#currentassignee").text('');
    reassignUserId = null;
  }
  function onFailure(error){
    displayMessage(error)
  }
  client_mirror.reassignCompliance(reassignUserId, assignComplianceAssigneeId, 
    assignComplianceConcurrenceId, assignComplianceApprovalId, reassignCompliance, reason, 
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
  
function getReassignCompliances () {
  function onSuccess(data){
    compliancesList = data["user_wise_compliances"];
    usersList = data["users"];
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
  
}

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocomplete_seatingunit").hide();
  $("#autocomplete_user").hide();
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

//Assignee----------------------------------------------
$("#userval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_user").show();
  
  var sUnit = $("#seatingunit").val();
  var assignees = null;

  var suggestions = [];
  $('#ulist_user').empty();
  if(textval.length>0){
    if(sUnit != ''){
      assignees = usersList[sUnit];
      for(var i in assignees){      
        if (~assignees[i]["user_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["user_name"]]); 
      }
    }else{
      for( user in usersList){
        assignees = usersList[user];
        for(var i in assignees){
          if (~assignees[i]["user_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["user_name"]]); 
        }
      }
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_user(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
              
    }
    $('#ulist_user').append(str);
    $("#user").val('');
    }else{
      $("#user").val('');
      $("#autocomplete_user").hide();
    }
});
//set selected autocomplte value to textbox
function activate_user (element,checkval,checkname) {
  $("#userval").val(checkname);
  $("#user").val(checkval);
}


$("#assignee").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'assigneelist active'){
      $(event.target).removeClass("active");
    }else{
      $(event.target).addClass("active");
    }

    var concurrenceUnit =  $("#concurrence_unit").val();
    var approvalUnit =  $("#approval_unit").val();

    loadUser(concurrenceUnit, 'concurrencelist', 'concurrence');
    loadUser(approvalUnit, 'approvallist', 'approval');
  }
});

$("#concurrence").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'concurrencelist active'){
      $(event.target).removeClass("active");
    }else{
      $(event.target).addClass("active");
    }

    var assigneeUnit =  $("#assignee_unit").val();
    var approvalUnit =  $("#approval_unit").val();

    loadUser(assigneeUnit, 'assigneelist', 'assignee');
    loadUser(approvalUnit, 'approvallist', 'approval');
  }
});

$("#approval").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'approvallist active'){
      $(event.target).removeClass("active");
    }else{
      $(event.target).addClass("active");
    }

    var assigneeUnit =  $("#assignee_unit").val();
    var concurrenceUnit =  $("#concurrence_unit").val();

    loadUser(assigneeUnit, 'assigneelist', 'assignee');
    loadUser(concurrenceUnit, 'concurrencelist', 'concurrence');
  }
});

function loadUser(selectedUnit, userClass, userType){
  var str='';

  var assigneeUserId = null;
  if($('.assigneelist.active').attr('id') != undefined)
    assigneeUserId = parseInt($('.assigneelist.active').attr('id'));

  var concurrenceUserId = null;
  if($('.concurrencelist.active').attr('id') != undefined)
    concurrenceUserId = parseInt($('.concurrencelist.active').attr('id'));

  var approvalUserId = null;
  if($('.approvallist.active').attr('id') != undefined)
    approvalUserId = parseInt($('.approvallist.active').attr('id'));

  $('#'+userType).empty();

  for(var user in usersList){
      if( selectedUnit == 'all' || selectedUnit == user ){
        var unitusers = usersList[user];
        for(var user in unitusers){
          var userId= unitusers[user]["user_id"];
          if(assigneeUserId != userId && concurrenceUserId !=userId && approvalUserId != userId){
            str += '<li id="'+userId+'" class="'+userClass+'" >'+unitusers[user]["user_name"]+'</li>';
          }
        }
      }
    }
  $('#'+userType).append(str);
}

$('#assignee_unit').change(function() {
    var assigneeUnit =  $("#assignee_unit").val();
    loadUser(assigneeUnit, 'assigneelist', 'assignee');
});

$('#concurrence_unit').change(function() {
    var concurrenceUnit =  $("#concurrence_unit").val();
    loadUser(concurrenceUnit, 'concurrencelist', 'concurrence');
});

$('#approval_unit').change(function() {
    var approvalUnit =  $("#approval_unit").val();
    loadUser(approvalUnit, 'approvallist', 'approval');
});

function validate_firsttab(){
  return true;
}

function validate_secondtab(){
  if($('.assigneelist.active').text() == ''){
    displayMessage("Assignee Required");
    return false;
  /*}else if ($('.approvallist.active').text() == ''){
    displayMessage("Approval Required");
    return false;
  }else if ($('#reason').val().trim() == ''){
    displayMessage("Reason Required");
    return false;*/
  }else{
    displayMessage("");
    return true;
  }    
}

var navListItems = $('ul.setup-panel li a'),
allWells = $('.setup-content');
allWells.hide();
navListItems.click(function(e)
{
e.preventDefault();
var $target = $($(this).attr('href')),
$item = $(this).closest('li');
if (!$item.hasClass('disabled')) {
navListItems.closest('li').removeClass('active');
$item.addClass('active');
allWells.hide();
$target.show();
}
});
$('ul.setup-panel li.active a').trigger('click');
$('#activate-step-2').on('click', function(e) {
if (validate_firsttab()){
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-2"]').trigger('click');
}
})

$('#backward-step-1').on('click', function(e) {
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-1"]').trigger('click');

})

$('#activate-step-finish').on('click', function(e) {
  if (validate_secondtab()){
  submitcompliance();
  }
})

$(document).ready(function () {
  getReassignCompliances ();
});