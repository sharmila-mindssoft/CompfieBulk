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
var CurrentPassword = $('#current-password');
var btnPasswordSubmit = $('#btnPasswordSubmit');

var ShowButton = $(".btn-show");
var ShowMore = $(".btn-showmore");

var compliancesList;
var transactionList;
var sno = 0;
var totalRecord;
var lastUnit = '';

var complianceId = null;
var thisval = null;
var unitId = null;
var complete_within_days = null;
var password = null;
var remarks = null;
var currentDate;


function displayPopup(statutoryProvision, unitName, complianceName, description, transactionList) {
    $('.popup-statutory').text(statutoryProvision);
    $('.popup-task').text(complianceName);
    $('.popup-description').text(description);

    $(".tbody-popup-list").empty();

    if (transactionList.length == 0) {
        displayMessage(message.onoccurrence_history);
    } else {
        $.each(transactionList, function(k1, v1) {
            var start_Date = transactionList[k1].start_date;
            var assignee = transactionList[k1].assignee_name;
            var completed_On = transactionList[k1].completion_date;
            var concurr = transactionList[k1].concurrer_name;
            var concurred_On = transactionList[k1].concurred_on;
            var approver = transactionList[k1].approver_name;
            var approved_On = transactionList[k1].approved_on;
            var status = transactionList[k1].on_compliance_status;
            var unitName = transactionList[k1].on_unit;
            var tableRow1 = $('#templates .table-pop-up .table-row');
            var clone1 = tableRow1.clone();
            $('.popup-unit').text(unitName);
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
            // var complianceId = value.compliance_id;
            // var unitId = value.unit_id;
            // var completeDays = value.complete_within_days;
            var tableRow1 = $('#templates .table-compliances .table-row');
            var clone1 = tableRow1.clone();
            $('.sno', clone1).text(sno);
            //$('.sno', clone1).attr('id', 'sn-' + sno)
            $('.statutory', clone1).text(value.statutory_provision);
            $('.compliance-task', clone1).find('a').text(value.compliance_name);
            $('.compliance-task', clone1).find('a').on('click', function(e) {
                loadLastTransaction(value.compliance_id, value.unit_id, function(last_transac_data) {
                    displayPopup(value.statutory_provision, lastUnit, value.compliance_name, value.description, last_transac_data);
                });
            });

            $('.description', clone1).text(value.description);
            $('.duration', clone1).text(value.complete_within_days);
            $('.startdate', clone1).attr('id', 'startdate' + sno);

            $('.remarks', clone1).attr('id', 'remarks' + sno);

            $('.btn-submit', clone1).attr('id', sno);
            $('.btn-submit', clone1).on('click', function() {
                if ($('.startdate', clone1).val().trim() == "") {
                    displayMessage(message.startdate_required);
                    return false;
                } else if ($('.remarks', clone1).val().trim() == "") {
                    displayMessage(message.remarks_required);
                    return false;
                } else if (validateMaxLength('remark', $('.remarks', clone1).val(), "Remarks") == false) {
                    $('.remarks', clone1).focus();
                    return false;
                } else {
                    CurrentPassword.val('');
                    complianceId = value.compliance_id;
                    thisval = $(this, clone1).closest('tr').find('.sno').html();
                    unitId = value.unit_id;
                    complete_within_days = value.complete_within_days;

                    confirm_alert(message.onoccurrence_start.replace('COMP_NAME', value.compliance_name), function(isConfirm) {
                        if (isConfirm) {
                            Custombox.open({
                                target: '#custom-modal-start',
                                effect: 'contentscale',
                            });
                        }
                    });
                }
            });



            $('.tbody-compliances-list').append(clone1);

            if ((value.complete_within_days).indexOf("Hour(s)") > -1) {
                $('#startdate' + sno).datetimepicker({
                    changeMonth: true,
                    changeYear: true,
                    numberOfMonths: 1,
                    dateFormat: 'dd-M-yy',
                    minDate: currentDate,
                    maxDate: currentDate,
                    monthNames: [
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                });
            } else {
                $('#startdate' + sno).datepicker({
                    changeMonth: true,
                    changeYear: true,
                    numberOfMonths: 1,
                    dateFormat: 'dd-M-yy',
                    minDate: currentDate,
                    maxDate: currentDate,
                    monthNames: [
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                });
            }
        });
    }

    if (sno == 0) {
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $('.tbody-compliances-list').append(clone);
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
    var time = datetime[1].split(':');
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
    return new Date(date[2], date[1] - 1, date[0], time[0], time[1]);
}

//start on occurrence compliance
function submitOnOccurence(complianceId, thisval, unitId, complete_within_days, password) {
    var startdate = $('#startdate' + thisval).val();
    var remarks = $('#remarks' + thisval).val();
    // var d = new Date();
    var d, currentDate;

    current_date_time(function(c_date) {
        currentDate = c_date;

        if (startdate != '') {
            if ((complete_within_days).indexOf("Hour(s)") == -1) {
                startdate = startdate + " 00:00";
            }
            var convertDueDate = convert_date(startdate);
            if (convertDueDate > currentDate) {
                displayMessage(message.startdate_greater_today);
                return false;
            }
            displayLoader();

            function onSuccess(data) {
                displaySuccessMessage(message.onoccurrence_submit);
                //getOnOccuranceCompliances ();
                $('#startdate' + thisval).val('');
                $('#remarks' + thisval).val('');
                hideLoader(); //window.location.href='/compliance-task-details'
            }

            function onFailure(error) {
                displayMessage(error);
                hideLoader();
            }
            client_mirror.startOnOccurrenceCompliance(parseInt(LegalEntityId.val()), complianceId, startdate, unitId, complete_within_days, remarks, password,
                function(error, response) {
                    Custombox.close();
                    CurrentPassword.val('');
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
    })
}

//get on occurence compliance list from api
function getOnOccuranceCompliances(sno) {
    displayLoader();
    if (sno == 0) {
        $('.tbody-compliances-list').empty();
        lastUnit = '';
    }

    function onSuccess(data) {
        compliancesList = data.onoccur_compliances;
        totalRecord = data.total_count;

        current_date_ymd(function(c_date) {
            currentDate = c_date;
            load_compliances(compliancesList);
        });

        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    if (UnitId.val().trim() != "")
        var u_id = parseInt(UnitId.val());
    else
        var u_id = null;
    client_mirror.getOnOccurrenceCompliances(parseInt(LegalEntityId.val()), u_id, sno, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function loadLastTransaction(compliance_id, unit_id, callback) {
    function onSuccess(data) {
        transactionList = data.onoccurrence_transactions;
        callback(transactionList);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    client_mirror.onOccurrenceLastTransaction(parseInt(LegalEntityId.val()), compliance_id, unit_id, function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            // onFailure(error);
            hideLoader();
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
        $('.tbody-compliances-list').empty();
        client_mirror.complianceFilters(parseInt(val[0]), function(error, response) {
            if (error == null) {
                UNITS = response.user_units;
            } else {
                onFailure(error);
            }
        });

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
        commonAutoComplete(e, ACUnit, UnitId, text_val,
            UNITS, "unit_name", "unit_id",
            function(val) {
                onAutoCompleteSuccess(UnitName, UnitId, val);
            }, condition_fields, condition_values);
    });

    btnPasswordSubmit.click(function() {
        if (CurrentPassword.val().trim() == "") {
            displayMessage(message.password_required);
            return false;
        } else if (validateMaxLength('password', CurrentPassword.val(), "Password") == false) {
            CurrentPassword.focus();
            return false;
        } else {
            submitOnOccurence(complianceId, thisval, unitId, complete_within_days, CurrentPassword.val().trim());
        }
    });
}

function loadEntityDetails() {
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        ShowButton.trigger("click");
        client_mirror.complianceFilters(parseInt(LE_ID), function(error, response) {
            if (error == null) {
                UNITS = response.user_units;
            } else {
                onFailure(error);
            }
        });
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