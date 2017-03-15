var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
var UNITS = null;

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
var transactionList;
var sno = 0;
var totalRecord;
var lastUnit = '';


function displayPopup(statutoryProvision, unitName, complianceName, description, transactionList) {
    $('.popup-statutory').text(statutoryProvision);
    $('.popup-unit').text(unitName);
    $('.popup-task').text(complianceName);
    $('.popup-description').text(description);

    $(".tbody-popup-list").empty();

    $.each(transactionList, function(k1, v1) {
        var start_Date = transactionList[k1].start_date;
        var assignee = transactionList[k1].assignee_name;
        var completed_On = transactionList[k1].completion_date;
        var concurr = transactionList[k1].concurrer_name;
        var concurred_On = transactionList[k1].concurred_on;
        var approver = transactionList[k1].approver_name;
        var approved_On = transactionList[k1].approved_on;
        var status = transactionList[k1].on_compliance_status;

        var tableRow1 = $('#templates .table-pop-up .table-row');
        var clone1 = tableRow1.clone();

        $('.pop-start-date', clone1).text(start_Date);
        $('.pop-assignee', clone1).text(assignee);
        $('.pop-completed-on', clone1).text(completed_On);
        $('.pop-concur', clone1).text(concurr);
        $('.pop-concur-on', clone1).text(concurred_On);
        $('.pop-approver', clone1).text(approver);
        $('.pop-approver-on', clone1).text(approved_On);
        $('.pop-compliance-status', clone1).text(status);

        $('.tbody-popup-list').append(clone1);

    });

    Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
    });
}

//load compliances in view page
function load_compliances(compliancesList) {
    for (var entity in compliancesList) {
        if (lastUnit != entity) {
            var tableRow = $('#templates .tbl_heading .table-row');
            var clone = tableRow.clone();
            $('.heading-unit', clone).html(entity);
            $('.tbody-compliances-list').append(clone);
            lastUnit = entity;
        }
        var compliances = compliancesList[entity];
        $.each(compliances, function(key, value) {
            sno = sno + 1;
            var complianceId = value.compliance_id;
            var unitId = value.unit_id;
            var completeDays = value.complete_within_days;
            var tableRow1 = $('#templates .table-compliances .table-row');
            var clone1 = tableRow1.clone();
            $('.sno', clone1).text(sno);
            $('.statutory', clone1).text(value.statutory_provision);
            $('.compliance-task', clone1).find('a').text(value.compliance_name);
            $('.compliance-task', clone1).find('a').on('click', function(e) {
                loadLastTransaction(complianceId, unitId);
                displayPopup(value.statutory_provision, lastUnit, value.compliance_name, value.description, transactionList);
            });

            $('.description', clone1).text(value.description);
            $('.duration', clone1).text(completeDays);
            $('.startdate', clone1).attr('id', 'startdate' + sno);

            $('.remarks', clone1).attr('id', 'remarks' + sno);

            $('.btn-submit', clone1).attr('id', sno);
            $('.btn-submit', clone1).on('click', function() {
                submitOnOccurence(value.compliance_id, this, value.unit_id, value.complete_within_days);
            });

            $('.tbody-compliances-list').append(clone1);

            $('#startdate' + sno).datetimepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: 'dd-M-yy',
                monthNames: [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
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
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
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
    var remarks = $('#remarks' + thisval.id).val();
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
            $('#remarks' + thisval.id).val('');
            hideLoader(); //window.location.href='/compliance-task-details'
        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        client_mirror.startOnOccurrenceCompliance(parseInt(LegalEntityId.val()), complianceId, startdate, unitId, complete_within_days, function(error, response) {
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
        $('.tbody-compliances-list').empty();
        lastUnit = '';
    }

    function onSuccess(data) {
        compliancesList = data.onoccur_compliances;
        totalRecord = data.total_count;
        load_compliances(compliancesList);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    client_mirror.getOnOccurrenceCompliances(parseInt(LegalEntityId.val()), sno, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function loadLastTransaction(compliance_id, unit_id) {
    function onSuccess(data) {
        transactionList = data.onoccurrence_transactions;
        // load_Transaction(compliancesList);
        // hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        // hideLoader();
    }

    client_mirror.onOccurrenceLastTransaction(parseInt(LegalEntityId.val()), compliance_id, unit_id, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            // onFailure(error);
        }
    });
}


function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'legal_entity_id') {
        UnitName.val('');
        UnitId.val('');
    }
}

function pageControls() {

    ShowButton.click(function() {
        sno = 0;
        lastUnit = '';
        if (LegalEntityId.val().trim().length <= 0) {
            displayMessage(message.legalentity_required);
            return false;
        } else {
            getOnOccuranceCompliances(sno);
        }
    });

    ShowMore.click(function() {
        endCount = sno;
        getOnOccuranceCompliances(sno);
    });

    LegalEntityName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "le_name", "le_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            });
    });

    UnitName.keyup(function(e) {
        var condition_fields = ['is_closed'];
        var condition_values = [false];

        var text_val = $(this).val();
        commonAutoComplete(
            e, ACUnit, UnitId, text_val,
            UNITS, "unit_name", "unit_id",
            function(val) {
                onAutoCompleteSuccess(UnitName, UnitId, val);
            }, condition_fields, condition_values);


    });

}

function loadEntityDetails() {
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();

        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $('.tbody-compliances-list').append(clone);

    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        ShowButton.trigger("click");
        //callAPI(REASSIGN_FILTER);
    }
}

//initialization
$(function() {
    pageControls();
    loadEntityDetails();

    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
});