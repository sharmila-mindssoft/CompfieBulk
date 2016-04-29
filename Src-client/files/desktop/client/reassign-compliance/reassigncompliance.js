var compliancesList;
var usersList;
var unitsList;
var reassignUserId=null;
var cCount;
var two_level_approve;
var client_admin;
var accordionstatus = true;
//var currentUser;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
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
  accordionstatus = false;
}

function compliancestatus(element){
  var sClass = $(element).attr('class');
  var actSelect = sClass.substr(sClass.lastIndexOf("s") + 1);
  var cStatus = false;
  $('.'+sClass).each(function() {
    if(this.checked){
      cStatus = true;
    }
  });
  if(cStatus){
    $('#act'+actSelect).prop("checked",true);
  }else{
    $('#act'+actSelect).prop("checked",false);
  }
}

//convert string to date format
function convert_date (data){
  var date = data.split("-");
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  for(var j=0;j<months.length;j++){
      if(date[1]==months[j]){
           date[1]=months.indexOf(months[j])+1;
       }
  }
  if(date[1]<10){
      date[1]='0'+date[1];
  }
  return new Date(date[2], date[1]-1, date[0]);
}

//load all compliances for selected user
function load_allcompliances(userId, userName){
  //currentUser = userId;
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
      $('.actname', clone).html('<input style="margin-top:5px" type="checkbox" id="act'+actCount+'" value="'+actCount+'" onclick="actstatus(this)"> <label for="act'+actCount+'">'+actname+'</label> <span><img src="/images/chevron_black_down.png"></span>');
      $('.tbody-assignstatutory').append(clone);
      $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      if(count==1){
        $('.accordion-content'+count).addClass("default");
      }

      var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
      var clone1=complianceHeadingtableRow.clone();
      $('.accordion-content'+count).append(clone1);

      var actList = statutoriesList[statutory];
      //$('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      for(var actentity in actList){
        var compliance_id = actList[actentity]["compliance_id"];
        var compliance_name = actList[actentity]["compliance_name"];
        var compliance_description = actList[actentity]["description"];
        var frequency =  actList[actentity]["compliance_frequency"];
        var statutory_date =  actList[actentity]["statutory_date"];
        var summary = actList[actentity]["summary"];
        var due_date =  actList[actentity]["due_date"];
        var validity_date =  actList[actentity]["validity_date"];
        var compliance_history_id = actList[actentity]["compliance_history_id"];
        if(validity_date == null) validity_date = '';
        var triggerdate = '';
        var statutorydate = '';
        var sdateDesc = '';

        for(j = 0; j < statutory_date.length; j++){
          var sDay = '';
          if(statutory_date[j]["statutory_date"] != null) sDay = statutory_date[j]["statutory_date"];
          var sMonth = '';
          if(statutory_date[j]["statutory_month"] != null) sMonth = statutory_date[j]["statutory_month"];
          var tDays = '';
          if(statutory_date[j]["trigger_before_days"] != null) tDays = statutory_date[j]["trigger_before_days"];

          if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);

          triggerdate +=  tDays + " Day(s) ";
          statutorydate +=  sMonth +' '+ sDay + ' ';
        }

        if(summary != null){
          if(statutorydate.trim() != ''){
            statutorydate = summary + ' ( '+statutorydate+' )';
          }else{
            statutorydate = summary;
          }
        }

        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        $('.ckbox', clone2).html('<input type="checkbox" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'" onclick="compliancestatus(this)">');

        $('.compliancetask', clone2).html('<abbr class="page-load" title="'+
          compliance_description+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliance_name);

        $('.compliancefrequency', clone2).text(frequency);

        $('.statutorydate', clone2).text(statutorydate);

        $('.triggerbefore', clone2).text(triggerdate);

        if(frequency != 'On Occurrence'){
          if(compliance_history_id != null){
            $('.duedate', clone2).html('<input type="text" value="'+due_date+'" class="input-box" readonly id="duedate'+statutoriesCount+'" />');
          }else{
            $('.duedate', clone2).html(due_date + '<input type="hidden" value="'+due_date+'" id="duedate'+statutoriesCount+'" />');
          }
        }else{
          $('.duedate', clone2).html(due_date);
        }

        $('.validitydate', clone2).text(validity_date);

        $('.accordion-content'+count).append(clone2);

        if(compliance_history_id != null){
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
        }
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
      if(accordionstatus){
        //Expand or collapse this panel
        $(this).next().slideToggle('fast');
        //Hide the other panels
        $(".accordion-content").not($(this).next()).slideUp('fast');
      }else{
        accordionstatus = true;
      }
    });
  });
}

//load list in view page
function load_UserCompliances(uCompliances, uId){
  for( compliance in uCompliances){
    var userName = "";
    var seatingUnitId = null;
    var seatingUnit = "";
    var noOfCompliances = uCompliances[compliance]["no_of_compliances"];

    for(var user in usersList){
      var userId= usersList[user]["user_id"];
      if(uId == userId){
        userName = usersList[user]["user_name"];
        seatingUnitId = usersList[user]["seating_unit_id"];
      }
    }
    for(var unit in unitsList){
      if(unitsList[unit]["unit_id"] == seatingUnitId){
        seatingUnit = unitsList[unit]["unit_name"];
      }
    }

    if(uId == 0){
      userName = "Client Admin";
      seatingUnit = "-";
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
  var givenUserId = $("#user").val();
  var givenUnitId = $("#seatingunit").val();;

  $(".tbody-reassign-compliances-list").find("tr").remove();
  cCount = 1;
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

  if(two_level_approve){
    $('.c-view').show();
  }else{
    $('.c-view').hide();
  }

}

//save reassign compliances 
function submitcompliance(){
  displayLoader();
  var assignComplianceAssigneeId = null;
  var assignComplianceConcurrenceId = null;
  var assignComplianceApprovalId = null;
  var assignComplianceAssigneeName = null;

  if($('.assigneelist.active').attr('id') != undefined){
    assignComplianceAssigneeId = parseInt($('.assigneelist.active').attr('id'));
    assignComplianceAssigneeName = $('.assigneelist.active').text().trim();
  }

  if($('.concurrencelist.active').attr('id') != undefined){
    assignComplianceConcurrenceId = parseInt($('.concurrencelist.active').attr('id'));
  }

  if($('.approvallist.active').attr('id') != undefined){
    assignComplianceApprovalId = parseInt($('.approvallist.active').attr('id'));
  }

  if(assignComplianceAssigneeName == 'Client Admin'){
    assignComplianceApprovalId = assignComplianceAssigneeId;
  }

  var reason = $('#reason').val();
  reassignCompliance = [];
  var statutoriesCount= 1;
  var userCompliances = compliancesList[reassignUserId];
  var d = new Date();
  var month = d.getMonth()+1;
  var day = d.getDate();
  var output = d.getFullYear() + '/' + month + '/' + day;
  var currentDate = new Date(output);
  var selectedStatus = false;

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
            selectedStatus = true;
          }
          if(complianceApplicable){
            var compliance_id = actList[actentity]["compliance_id"];
            var compliance_history_id = actList[actentity]["compliance_history_id"];
            var cfrequency = actList[actentity]["compliance_frequency"];
            var compliance_name = actList[actentity]["compliance_name"];
            var due_date = null;
            if(cfrequency != 'On Occurrence'){
              due_date =  $('#duedate'+statutoriesCount).val();
              if(due_date == '' || due_date == undefined){
                displayMessage(message.duedate_required_compliance + compliance_name);
                hideLoader();
                return false;
                /*var convertDueDate = convert_date(due_date);
                if (convertDueDate < currentDate) {
                  displayMessage("Due date is less than today's date for compliance '" + compliance_name + "'");
                  hideLoader();
                  return false;
                }*/
              }
            }
            reassignComplianceData = client_mirror.reassignComplianceDet(uId,
              compliance_id, compliance_name, compliance_history_id, due_date
            );
            reassignCompliance.push(reassignComplianceData);
          }
          statutoriesCount = statutoriesCount + 1;
        }
      }
    }
  }

  if(selectedStatus){
    function onSuccess(data){
      $('ul.setup-panel li:eq(0)').addClass('active');
      $('ul.setup-panel li:eq(1)').addClass('disabled');
      $('ul.setup-panel li a[href="#step-1"]').trigger('click');
      $(".tbody-reassign-compliances-list").find("tbody").remove();
      getReassignCompliances();
      hideLoader();
      $("#reassign-view").show();
      $("#reassign-detailview").hide();
      $("#currentassignee").text('');
      $('#assignee').empty();
      $('#concurrence').empty();
      $('#approval').empty();
      $('#reason').val('');
      reassignUserId = null;
    }
    function onFailure(error){
      displayMessage(error);
      hideLoader();
    }
    client_mirror.saveReassignCompliance(
      reassignUserId, assignComplianceAssigneeId,
      assignComplianceAssigneeName,
      assignComplianceConcurrenceId,
      assignComplianceApprovalId, reassignCompliance, reason,
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
    hideLoader();
    displayMessage(message.nocompliance_selected_forassign);
  }
}

//get reassign compliance details from api
function getReassignCompliances () {
  function onSuccess(data){
    compliancesList = data["user_wise_compliances"];
    usersList = data["users"];
    unitsList = data["units"];
    two_level_approve = data["two_level_approve"];
    client_admin = data["client_admin"];
    $("#compliance-list").show();
    load_compliances();
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

//retrive unit with condition form autocomplete value
function onUnitSuccess(val){
  $("#seatingunitval").val(val[1]);
  $("#seatingunit").val(val[0]);
}

//load unit with conditionform list in autocomplete text box  
$("#seatingunitval").keyup(function(){
    var textval = $(this).val();
    getUnitAutocomplete(textval, unitsList, function(val){
        onUnitSuccess(val)
    })
});

//retrive user autocomplete value
function onUserSuccess(val){
  $("#userval").val(val[1]);
  $("#user").val(val[0]);
}

//load user list in autocomplete text box  
$("#userval").keyup(function(){
  var textval = $(this).val();
  getReassignUserAutocomplete(textval, usersList, function(val){
    onUserSuccess(val)
  })
});


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

//load avaliable users list in assignee,concurrence and approval list
function loadUser(userType){
  var selectedUnit = null;
  var userClass;
  var temp_assignee = null;
  var temp_concurrence = null;
  var temp_approval = null;

  if(userType == 'assignee'){
    selectedUnit = $("#assignee_unit").val();
    userClass = 'assigneelist';

  }
  else if(userType == 'concurrence'){
    selectedUnit = $("#concurrence_unit").val();
    userClass = 'concurrencelist';

  }
  else{
    selectedUnit = $("#approval_unit").val();
    userClass = 'approvallist';

  }

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

  var str='';
  if(userType != 'concurrence' && selectedUnit != ''){
    if((assigneeUserId == null || assigneeUserId != client_admin)
    && (approvalUserId == null || approvalUserId != client_admin)
    && (concurrenceUserId == null || concurrenceUserId != client_admin)){

      str='<li id="'+client_admin+'" class="'+userClass+'" > Client Admin </li>';
    }
  }
  for(var user in usersList){
    var userUnits = usersList[user]["unit_ids"];
    if( selectedUnit == 'all' || $.inArray(parseInt(selectedUnit), userUnits) >= 0){
      var userId= usersList[user]["user_id"];
      var uLevel = usersList[user]["user_level"];
      var userName= usersList[user]["user_name"] + ' - Level ' + uLevel;
      var isAssignee = usersList[user]["is_assignee"];
      var isConcurrence = usersList[user]["is_concurrence"];
      var isApprover = usersList[user]["is_approver"];

      var userPermission;
      if(userType == 'assignee'){
        userPermission = isAssignee;
      }
      else if(userType == 'concurrence'){
        userPermission = isConcurrence;
      }
      else if(userType == 'approval'){
       userPermission = isApprover;
      }

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

      if(userPermission && conditionResult && conditionResult1 && (assigneeUserId == null || assigneeUserId != userId)
        && (approvalUserId == null || approvalUserId != userId)
        && (concurrenceUserId == null || concurrenceUserId != userId)){
        //&& (currentUser != userId || userType != 'assignee') - for same assignee not loaded in assignee list

        str += '<li id="'+userId+'" class="'+userClass+'" >'+userName+'</li>';
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
    var assigneeText = $(".assigneelist.active").text().trim();
    if(assigneeText != 'Client Admin'){
      loadUser('concurrence');
      loadUser('approval');
    }else{
      $('#concurrence').empty();
      $('#approval').empty();
    }
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
    //loadUser('assignee');
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

    //loadUser('assignee');
    //loadUser('concurrence');
  }
});


$("#filter_assignee").keyup( function() {
    var filter = $("#filter_assignee").val().toLowerCase();
    var lis = document.getElementsByClassName('assigneelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_concurrence").keyup( function() {
    var filter = $("#filter_concurrence").val().toLowerCase();
    var lis = document.getElementsByClassName('concurrencelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_approval").keyup( function() {
    var filter = $("#filter_approval").val().toLowerCase();
    var lis = document.getElementsByClassName('approvallist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
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

$('#reason').keyup(function(e)
  {
  var maxLength = 500;
  var textlength = this.value.length;
  if (textlength >= maxLength)
  {
  $('#counter').html('You cannot write more then ' + maxLength + ' characters!');
  this.value = this.value.substring(0, maxLength);
  e.preventDefault();
  }
  else
  {
  $('#counter').html((maxLength - textlength) + ' characters left.');
  }
  });
function validate_firsttab(){
  return true;
}

//validation in second tab
function validate_secondtab(){
  if($('.assigneelist.active').text() == ''){
    displayMessage(message.assignee_required);
    return false;
  }else if ($('.concurrencelist.active').text() == '' && two_level_approve && $(".assigneelist.active").text().trim() != 'Client Admin'){
    displayMessage(message.concurrence_required);
    return false;
  }else if ($('.approvallist.active').text() == '' && $(".assigneelist.active").text().trim() != 'Client Admin'){
    displayMessage(message.approval_required);
    return false;
  }else if ($('#reason').val().trim() == ''){
    displayMessage(message.reason_required);
    return false;
  }else{
    displayMessage("");
    return true;
  }
}

//create wizard
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

//initialization
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