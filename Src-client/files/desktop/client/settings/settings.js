
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
        displayMessage(error);
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
    var free_space = (totaldiskspace - useddiskspace).toFixed(2);
    $('.contract-start').html(contractFrom);
    $('.contract-expires').html(contractTo);
    $('.space-summary').html(free_space + " GB free of "+totaldiskspace+" GB ");
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
        var address = '';
        if(lists[key]['seating_unit_name'] != null){
          seating_unit = lists[key]['seating_unit_name'];
          address = lists[key]['address'];
        }
        $('.sno', clone).text(sno);
        $('.employee', clone).text(lists[key]['user_name']);
        $('.email', clone).text(lists[key]['email_id']);
        if(lists[key]['contact_no'] == null){
          $('.mobile-number', clone).text("-");
        }
        else{
          $('.mobile-number', clone).text(lists[key]['contact_no']);
        }
        $('.seating-unit span', clone).html(seating_unit);
        if(seating_unit != '-'){
          $('.seating-unit abbr', clone).attr("title", lists[key]['address']);
        }else{
          $('.seating-unit abbr', clone).text('');
        }
        $('.unit-address', clone).text(address);
        $('.tbody-clientprofile-list').append(clone);
    });

}

function validate(){
  if($("input[name=2levels]:checked").val() == ''){
    displayMessage(message.approval_level);
  }
  else if($("#assigneeval").val().trim().length==0 || $("#assigneeval").val().trim() == 0){
    displayMessage(message.reminder_assignee_required);
  }
  else if($("#concurrenceapprovalval").val().trim().length==0 || $("#concurrenceapprovalval").val().trim() == 0){
    displayMessage(message.escalationreminder_concurrence_approval_required);
  }
  else if($("#allval").val().trim().length==0 || $("#allval").val().trim() == 0){
    displayMessage(message.escalationreminder_all);
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
        displayMessage(message.record_updated);
      }
    function onFailure(error) {
        displayMessage(error);
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

$(function() {
  initialize();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
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

$('#assigneeval').on('input', function (e) {
    this.value = isNumbers($(this));
});
  $('#concurrenceapprovalval').on('input', function (e) {
    this.value = isNumbers($(this));
});
$('#allval').on('input', function (e) {
    this.value = isNumbers($(this));
});