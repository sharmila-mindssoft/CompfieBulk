var compliancesList;
var sno = 0;
var totalRecord;
var lastUnit = '';
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//load compliances in view page
function load_compliances(compliancesList) {
  for (var entity in compliancesList) {
    if (lastUnit != entity) {
      var tableRow = $('#head-templates .tbl_heading');
      var clone = tableRow.clone();
      $('.heading', clone).html(entity);
      $('.tbody-compliances-list').append(clone);
      lastUnit = entity;
    }
    var compliances = compliancesList[entity];
    $.each(compliances, function (key, value) {
      sno = sno + 1;
      var complianceId = value.compliance_id;
      var unitId = value.unit_id;
      var completeDays = value.complete_within_days;
      var tableRow1 = $('#templates .table-compliances .table-row');
      var clone1 = tableRow1.clone();
      $('.sno', clone1).text(sno);
      $('.statutory', clone1).text(value.statutory_provision);
      $('.compliance-task', clone1).text(value.compliance_name);
      $('.description', clone1).text(value.description);
      $('.duration', clone1).text(completeDays);
      $('.startdate', clone1).attr('id', 'startdate' + sno);
      $('.btn-submit', clone1).attr('id', sno);
      $('.btn-submit', clone1).on('click', function () {
        submitOnOccurence(complianceId, this, unitId, completeDays);
      });
      /*$(clone1, '.action').on("click", function(e){
            submitOnOccurence(complianceId, j, unitId, completeDays);
        });*/
      $('.tbody-compliances-list').append(clone1);
      $('#startdate' + sno).datetimepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: 'dd-M-yy',
        monthNames: [
          'Jan',
          'Feb',
          'Mar',
          'Apr',
          'May',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Oct',
          'Nov',
          'Dec'
        ]
      });
    });
  }
  if (totalRecord == 0) {
    $('#pagination').hide();
    $('.compliance_count').text('');
  } else {
    $('.compliance_count').text('Total Compliances : ' + totalRecord);
    if (sno >= totalRecord) {
      $('#pagination').hide();
    } else {
      $('#pagination').show();
    }
  }
}
//convert string to date format
function convert_date(data) {
  var datetime = data.split(' ');
  var date = datetime[0].split('-');
  var months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  for (var j = 0; j < months.length; j++) {
    if (date[1] == months[j]) {
      date[1] = months.indexOf(months[j]) + 1;
    }
  }
  if (date[1] < 10) {
    date[1] = '0' + date[1];
  }
  return new Date(date[2], date[1] - 1, date[0]);
}
//start on occurance compliance
function submitOnOccurence(complianceId, thisval, unitId, complete_within_days) {
  var startdate = $('#startdate' + thisval.id).val();
  var d = new Date();
  var month = d.getMonth() + 1;
  var day = d.getDate();
  var output = d.getFullYear() + '/' + month + '/' + day;
  var currentDate = new Date(output);
  if (startdate != '') {
    var convertDueDate = convert_date(startdate);
    if (convertDueDate > currentDate) {
      displayMessage(message.startdate_greater_today);
      return false;
    }
    displayLoader();
    function onSuccess(data) {
      displayMessage(message.action_success);
      //getOnOccuranceCompliances ();
      $('#startdate' + thisval.id).val('');
      hideLoader();  //window.location.href='/compliance-task-details'
    }
    function onFailure(error) {
      displayMessage(error);
      hideLoader();
    }
    client_mirror.startOnOccurrenceCompliance(complianceId, startdate, unitId, complete_within_days, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  } else {
    displayMessage(message.startdate_required);
    return false;
  }
}
//get on occurance compliance list from api
function getOnOccuranceCompliances(sno) {
  //displayLoader();
  if (sno == 0) {
    $('.tbody-complainces-list').find('tr').remove();
    lastUnit = '';
  }
  function onSuccess(data) {
    compliancesList = data.compliances;
    totalRecord = data.total_count;
    load_compliances(compliancesList);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getOnOccurrenceCompliances(sno, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
$('#pagination').click(function () {
  endCount = sno;
  getOnOccuranceCompliances(sno);
});
//initialization
$(document).ready(function () {
  sno = 0;
  lastUnit = '';
  getOnOccuranceCompliances(sno);
});