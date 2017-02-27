var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var UnitName = $("#unit_name");
var UnitId = $("#unit_id");
var ACUnit = $("#ac-unit");

var ShowButton = $(".btn-show");
var ShowMore = $(".btn-showmore");

var compliancesList;
var sno = 0;
var totalRecord;
var lastUnit = '';

//load compliances in view page
function load_compliances(compliancesList) {
  for (var entity in compliancesList) {
    if (lastUnit != entity) {
      var tableRow = $('#templates .tbl_heading');
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
      
      $('.tbody-compliances-list').append(clone1);
      $('#startdate' + sno).datetimepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: 'dd-M-yy',
        monthNames: [
          'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
        ]
      });
    });
  }
  if (totalRecord == 0) {
    ShowMore.hide();
    $('.total_count_view').text('');
  } else {
    $('.total_count_view').text('Total Compliances : ' + totalRecord);
    if (sno >= totalRecord) {
      ShowMore.hide();
    } else {
      ShowMore.show();
    }
  }
}
//convert string to date format
function convert_date(data) {
  var datetime = data.split(' ');
  var date = datetime[0].split('-');
  var months = [
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
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

ShowMore.click(function () {
  endCount = sno;
  getOnOccuranceCompliances(sno);
});


function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'legal_entity_id') {
        UnitName.val('');
        UnitId.val('');
    }
}

LegalEntityName.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLegalEntity, LegalEntityId, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
        });
    
});

ShowButton.click(function() {
    val_legal_entity_id = LegalEntityId.val();
    val_unit_id = UnitId.val();
    
    if (val_legal_entity_id.trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else {
        getOnOccuranceCompliances(sno);
    }
});

function loadEntityDetails(){
    if(LEGAL_ENTITIES.length > 1){
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();

        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $('.tbody-compliances-list').append(clone);

    }else{
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        ShowButton.trigger( "click" );
        //callAPI(REASSIGN_FILTER);
    }
}

//initialization
$(function() {
    sno = 0;
    lastUnit = '';
    loadEntityDetails();
});