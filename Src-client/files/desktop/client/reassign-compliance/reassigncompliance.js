var compliancesList;
var usersList;
var unitsList;
var reassignUserId=null;
var cCount = 1;
var two_level_approve;


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
      var userId= usersList[user]["user_id"];
      userName = usersList[user]["user_name"];
      seatingUnitId = usersList[user]["seating_unit_id"];
    }
    for(var unit in unitsList){
      var userId= usersList[user]["user_id"];
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
    for(var i in usersList){ 
    if(givenUnitId == usersList[i]["seating_unit_id"]){ 
      var uId =  usersList[i]["user_id"];
      var uCompliances = compliancesList[uId];
      load_UserCompliances(uCompliances, uId);
    }
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
      var uId = userUnitwiseCompliance[entity]["unit_id"];
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
            var compliance_history_id = actList[actentity]["compliance_history_id"];
            
            var due_date =  $('#duedate'+statutoriesCount).val();

            reassignComplianceData = client_mirror.reassingComplianceDet(uId,
              compliance_id, compliance_history_id, due_date
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
  client_mirror.saveReassignCompliance(reassignUserId, assignComplianceAssigneeId, 
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
    unitsList = data["units"]; 
    //two_level_approve = data["two_level_approve"];
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
  var assignees = usersList;

  var suggestions = [];
  $('#ulist_user').empty();
  if(textval.length>0){
    for(var i in assignees){    
    if(sUnit == '' || sUnit == assignees[i]["seating_unit_id"]){
      if (~assignees[i]["user_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["user_name"]]); 
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

function getUserLevel(selectedUserId){
  var getuserLevel = null; 
  for(var user in usersList){
    var userId= usersList[user]["user_id"];
    if(userId == selectedUserId){
      getuserLevel = usersList[user]["user_level"];
    }
  }
  return getuserLevel;
}
function loadUser(userType){
  var selectedUnit;
  var userClass;
  var temp_assignee = null;
  var temp_concurrence = null;
  var temp_approval = null;
  var temp_id = null;

  if(userType == 'assignee'){
    selectedUnit = $("#assignee_unit").val();
    userClass = 'assigneelist';

    if($('.assigneelist.active').attr('id') != undefined)
      temp_id = parseInt($('.assigneelist.active').attr('id'));
  }
  else if(userType == 'concurrence'){
    selectedUnit = $("#concurrence_unit").val();
    userClass = 'concurrencelist';

    if($('.concurrencelist.active').attr('id') != undefined)
      temp_id = parseInt($('.concurrencelist.active').attr('id'));
  }
  else{
    selectedUnit = $("#approval_unit").val();
    userClass = 'approvallist';

    if($('.approvallist.active').attr('id') != undefined)
      temp_id = parseInt($('.approvallist.active').attr('id'));
  }
  var str='';
  $('#'+userType).empty();

  var assigneeUserId = null;
  if($('.assigneelist.active').attr('id') != undefined)
    assigneeUserId = parseInt($('.assigneelist.active').attr('id'));

  var concurrenceUserId = null;
  if($('.concurrencelist.active').attr('id') != undefined)
    concurrenceUserId = parseInt($('.concurrencelist.active').attr('id'));

  var approvalUserId = null;
  if($('.approvallist.active').attr('id') != undefined)
    approvalUserId = parseInt($('.approvallist.active').attr('id'));


  var conditionResult = true;
  var conditionResult1 = true;
  var userLevel = null;
  var userLevel1 = null;

  if(userType == 'assignee' && (concurrenceUserId != null || approvalUserId != null)){
    if(concurrenceUserId != null){
      userLevel = getUserLevel(concurrenceUserId);
    }else{
      userLevel = getUserLevel(approvalUserId);
    }
  }else if(userType == 'concurrence' && (assigneeUserId != null || approvalUserId != null)){
    if(assigneeUserId != null){
      userLevel = getUserLevel(assigneeUserId);
    }
    if(approvalUserId != null){
      userLevel1 = getUserLevel(approvalUserId);
    }
  }else if(userType == 'approval' && (concurrenceUserId != null || assigneeUserId != null)){
    if(concurrenceUserId != null){
      userLevel = getUserLevel(concurrenceUserId);
    }else{
      userLevel = getUserLevel(assigneeUserId);
    }
  }

  for(var user in usersList){
    var userUnits = usersList[user]["unit_ids"];
    if( selectedUnit == 'all' || $.inArray(parseInt(selectedUnit), userUnits) >= 0){
      var userId= usersList[user]["user_id"];
      var uLevel = usersList[user]["user_level"];
      var userName= usersList[user]["user_name"] + ' - Level ' + uLevel;
     
      if(userLevel != null){
        if(userType == 'assignee'){
          conditionResult = (uLevel >= userLevel);
        }
        else if(userType == 'concurrence'){
          conditionResult = (uLevel <= userLevel);
        }
        else if(userType == 'approval'){
          conditionResult = (uLevel <= userLevel);
        }
      }

      if(userType == 'concurrence' && userLevel1 != null){
          conditionResult1 = (uLevel >= userLevel1);
      }

      if(conditionResult && conditionResult1 && (assigneeUserId == null || assigneeUserId != userId)
        && (approvalUserId == null || approvalUserId != userId) 
        && (concurrenceUserId == null || concurrenceUserId != userId)){
        if(temp_id == userId){
          str += '<li id="'+userId+'" class="'+userClass+ ' active'+'" >'+userName+'</li>';
        }else{
          str += '<li id="'+userId+'" class="'+userClass+'" >'+userName+'</li>';
        }
      }
    }
  }
  $('#'+userType).append(str);
}

$("#assignee").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'assigneelist active'){
      $(event.target).removeClass("active");
    }else{
      $('.assigneelist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }

    loadUser('concurrence');
    loadUser('approval');
  }
});

$("#concurrence").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'concurrencelist active'){
      $(event.target).removeClass("active");
    }else{
      $('.concurrencelist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }

    loadUser('assignee');
    loadUser('approval');
  }
});

$("#approval").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'approvallist active'){
      $(event.target).removeClass("active");
    }else{
      $('.approvallist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }

    loadUser('assignee');
    loadUser('concurrence');
  }
});

$('#assignee_unit').change(function() {
    loadUser('assignee');
});

$('#concurrence_unit').change(function() {
    loadUser('concurrence');
});

$('#approval_unit').change(function() {
    loadUser('approval');
});


function validate_firsttab(){
  return true;
}

function validate_secondtab(){
  if($('.assigneelist.active').text() == ''){
    displayMessage("Assignee Required");
    return false;
  /*}else if ($('.concurrencelist.active').text() == '' && two_level_approve){
    displayMessage("Concurrence Required");
    return false;*/
  }else if ($('.approvallist.active').text() == ''){
    displayMessage("Approval Required");
    return false;
  }else if ($('#reason').val().trim() == ''){
    displayMessage("Reason Required");
    return false;
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