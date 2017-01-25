var MessageList;
var from_count = 0;
var page_count = 50;
// User List render process
function loadMessages() {
  var isEmpty = true;
  $('.tbody-message-list').find('tr').remove();
  $.each(MessageList, function(k, v) {
    isEmpty = false;
    var tableRow = $('#templates .table-message .table-row');
    var rowClone = tableRow.clone();
    $('.message-content', rowClone).text(v.message_heading + ' - ' + v.message_text);
    $('.message-time', rowClone).text(v.created_on);
    $('.message-user',rowClone).text('User: '+v.created_by);
    $('.tbody-message-list').append(rowClone);
  });

  if(isEmpty){
    var no_record_row = $("#templates .table-no-record tr");
    var clone = no_record_row.clone();
    $(".tbody-message-list").append(clone);
  }
  
}

// page load
function initialize() {
  mirror.getMessages(from_count, page_count, function (error, response) {
      if (error != null) {
        displayMessage(error);
      }
      else {
        MessageList = response.messages;
        loadMessages();
      }
    });
}

$(document).ready(function () {
  initialize();
});
