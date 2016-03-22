
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
function initialize(){

  function onSuccess(data){
    var profiles = data['profile_detail'];
    $('#assigneeval').val(data['assignee_reminder_days']);
    $('#concurrenceapprovalval').val(data['escalation_reminder_In_advance_days']);
    $('#allval').val(data['escalation_reminder_days']);

    var twolevelapproval = data['is_two_levels_of_approval'];
    if(twolevelapproval)
        $("input[name=2levels][value=yes]").prop('checked', true);
    else
        $("input[name=2levels][value=no]").prop('checked', true);

    loadClientProfileList(profiles)
  }
  function onFailure(error){
        console.log(error);
  }
  client_mirror.getSettings(
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }

    );
}
function loadClientProfileList(profiles){
    $(".tbody-clientprofile-list").find("tr").remove();
    var sno = 0;        
    var list=profiles;
    var contractFrom = list['contract_from'];
    var contractTo = list['contract_to'];
    var noLicence = list['no_of_user_licence'];
    var remaininglicence = list['remaining_licence'];
    var totaldiskspace = list["total_file_space"];
    var useddiskspace = list["used_space"];    
    $('.contract-start').html(contractFrom);
    $('.contract-expires').html(contractTo);    
    $('.space-summary').html(useddiskspace+" GB of "+totaldiskspace+" GB used");
    var calculate = ((useddiskspace/totaldiskspace)*100).toFixed(2);

    var balance = 100-calculate;
    if(calculate !='0.00'){
        $('.usedspace').css("width", calculate+"%");
        $('.totalspace').css("width", balance+"%");
        $('.totalspace').html(balance+"%");
        $('.usedspace').html(calculate+"%");
    }
    else{
        $('.usedspace').hide();
        $('.totalspace').css("width", balance+"%");
        $('.totalspace').html(balance+"%");
    }
    $('.remaining-licence').html(remaininglicence);

    var lists = list['licence_holders'];
    $.each(lists, function(key, val) { 
        var tableRow = $('#templates .table-clientprofile-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        var seating_unit = '-';
        if(lists[key]['seating_unit_name'] != null) seating_unit = lists[key]['seating_unit_name'];
        $('.sno', clone).text(sno);
        $('.employee', clone).text(lists[key]['user_name']);
        $('.email', clone).text(lists[key]['email_id']);
        if(lists[key]['contact_no'] == null){
          $('.mobile-number', clone).text("-");  
        }
        else{
          $('.mobile-number', clone).text(lists[key]['contact_no']);
        }     
        $('.seating-unit', clone).text(seating_unit);
        $('.unit-address', clone).text(lists[key]['address']);      
        $('.tbody-clientprofile-list').append(clone);
    });
        
}

function validate(){
  if($("input[name=2levels]:checked").val() == ''){
    displayMessage('Level of Approval is Required');
  }
  else if($("#assigneeval").val().trim().length==0){
    displayMessage('Reminder to Assignee is Required');
  }
  else if($("#concurrenceapprovalval").val().trim().length==0){
    displayMessage('Escalation Reminders to Concurrence & Approval Person is Required');
  }
  else if($("#allval").val().trim().length==0){
    displayMessage('Escalation Reminders to Assignee, Concurrence & Approval is person');
  }
  else{
    displayMessage('');
    return true
  }
}

$("#submit").click(function(){

  var twolevelapproval = false;
  if($("input[name=2levels]:checked").val() == 'yes') twolevelapproval = true;

  var assigneeReminderDays = $("#assigneeval").val();
  var eReminderAdvance = $("#concurrenceapprovalval").val();
  var eReminder = $("#allval").val();

if(validate()){
    function onSuccess(response){
        displayMessage('Record Updated Successfully');
      }
    function onFailure(error) {
        displayMessage = error
    }
    client_mirror.updateSettings(twolevelapproval, parseInt(assigneeReminderDays), parseInt(eReminderAdvance), parseInt(eReminder),
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

$("#search-employee").keyup(function() { 
  var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".employee").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-email").keyup(function() { 
  var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".email").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-mobile-number").keyup(function() { 
  var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".mobile-number").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-seating-unit").keyup(function() { 
  var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".seating-unit").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$(function() {
  initialize();

  $('#assigneeval').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9]/g, '');
  });
  
  $('#concurrenceapprovalval').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9]/g, '');
  });

  $('#allval').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9]/g, '');
  });

});