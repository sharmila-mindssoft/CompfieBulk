var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var CountryId = $("#country_id");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var txtUnit = $('#txtUnit');
var hdnUnit = $('#hdnUnit');
var divUnit = $('#divUnit');

var ShowButton = $(".btn-show");
var ShowMoreButton = $(".btn-show-more");
var basicwizard = $("#basicwizard");
var currentCompliances;
var file_list = [];
var temp_file_list = [];
var currentDate;
var c_endCount = 0;
var u_endCount = 0;
var c_totalRecord1;
var c_totalRecord2;
var u_totalRecord;
var snoOverdue = 1;
var snoInprogress = 1;
var countOverdue = 0;
var countUpcoming = 0;
var countInprogress = 0;
var sno = 0;
var uploaded_file_list = [];
var unitList = [];
var curDate = "";
var minDate = "";
var calDate = "";
var maxDate = "";


function initialize() {
    displayLoader();
    c_endCount = 0;
    $(".tbody-compliances-task-list-overdue").empty();
    $(".tbody-compliances-task-list-inprogress").empty();
    $(".uploaded-filename").empty();
    snoOverdue = 1;
    snoInprogress = 1;
    countOverdue = 0;
    countInprogress = 0;
    closeicon();
    loadCalendar(null);
    hideLoader();

    // function onSuccess(data) {
    //     closeicon();
    //     currentCompliances = data['current_compliances'];
    //     c_totalRecord1 = data['inprogress_count'];
    //     c_totalRecord2 = data['overdue_count'];
    //     currentDate = data['current_date'];
    //     loadComplianceTaskDetails(currentCompliances);
    //     hideLoader();
    // }

    // function onFailure(error) {
    //     hideLoader()
    // }
    // if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    // client_mirror.getCurrentComplianceDetail(parseInt(LegalEntityId.val()), unit_id, c_endCount, null, null,
    // function(error, response) {
    //     if (error == null) {
    //         onSuccess(response);
    //     } else {
    //         onFailure(error);
    //     }
    // })
}

function loadComplianceTaskDetails(data) {
    $(".tbody-compliances-task-list-overdue").empty();
    $(".tbody-compliances-task-list-inprogress").empty();
    snoOverdue = 1;
    snoInprogress = 1;
    countOverdue = 0;
    countInprogress = 0;

    $.each(data, function(key, value) {
        if (data[key].compliance_status == "Not Complied" && countOverdue == 0) {
            var tableRowHeading = $("#templates .table-compliances-task-list .headingRow");
            var clone = tableRowHeading.clone();
            $(".compliance-types mark", clone).html("Over due Compliances");
            $(".tbody-compliances-task-list-overdue").append(clone);
            countOverdue++
        }
        if (data[key].compliance_status == "Inprogress" && countInprogress == 0) {
            var tableRowHeading = $("#templates .table-compliances-task-list .headingRow");
            var clone = tableRowHeading.clone();
            $(".compliance-types mark", clone).html("Inprogress Compliances");
            $(".tbody-compliances-task-list-inprogress").append(clone);
            countInprogress++
        }
        if (data[key].compliance_status == "Rectify" && countOverdue == 0) {
            var tableRowHeading = $("#templates .table-compliances-task-list .headingRow");
            var clone = tableRowHeading.clone();
            $(".compliance-types mark", clone).html("Over due Compliances");
            $(".tbody-compliances-task-list-overdue").append(clone);
            countOverdue++
        }
        // $("#templates .table-compliances-task-list").empty();
        var tableRowvalues = $("#templates .table-compliances-task-list .table-row-list");
        var cloneval = tableRowvalues.clone();
        $(".compliance-task span", cloneval).html(data[key].compliance_name);
        $(".compliance-task small", cloneval).html('Assigned on: ' + data[key].assigned_on);
        $(".compliance-task i", cloneval).attr("title", data[key].compliance_description);
        $(".domain", cloneval).html(data[key].domain_name);
        $(".startdate", cloneval).html(data[key].start_date);
        $(".duedate", cloneval).html(data[key].due_date);
        $(".days-text", cloneval).html(data[key].ageing);
        if (data[key].compliance_status == "Not Complied") {
            $(".days-text", cloneval).attr("style", "color:#f00;");
        }
        if (data[key].remarks != null) {
            $(".sno", cloneval).attr("style", "color:#f00;");
            $(".compliance-task", cloneval).attr("style", "color:#f00;");
            $(".domain", cloneval).attr("style", "color:#f00;");
            $(".startdate", cloneval).attr("style", "color:#f00;");
            $(".duedate", cloneval).attr("style", "color:#f00;");
            $(".days-text", cloneval).attr("style", "color:#f00;");
            $(".status", cloneval).attr("style", "color:#f00;");
        }
        $(".status", cloneval).html(data[key].compliance_status);
        // if (data[key].format_file_name != null) {
        if (data[key].compliance_file_name != null) {
            $(".format-file", cloneval).on("click", function(e, val) {
                $('.format-file', cloneval).attr('href', data[key].compliance_file_name[0]);
            });
        } else {
            $(".format-file", cloneval).hide();
        }
        var compliance_history_id = data[key].compliance_history_id;
        $(cloneval, ".expand_inprogress").on("click", function() {
            $(".table-row-list").removeClass("active1");
            $(cloneval, ".table-row-list").addClass("active1");
            showSideBar(compliance_history_id, data);
        });
        if (data[key].compliance_status == "Not Complied" || data[key].compliance_status == "Rectify") {
            $(".sno", cloneval).text(snoOverdue);
            $(".tbody-compliances-task-list-overdue").append(cloneval);
            snoOverdue = snoOverdue + 1
        }
        if (data[key].compliance_status == "Inprogress" || data[key].compliance_status == "Inprogress(Rejected)") {
            $(".sno", cloneval).text(snoInprogress);
            $(".tbody-compliances-task-list-inprogress").append(cloneval);
            snoInprogress = snoInprogress + 1
        }
    });

    var b = snoOverdue - 1 + (snoInprogress - 1);
    if (c_totalRecord1 == 0 && c_totalRecord2 == 0) {
        var d = $("#no-record-templates .table-no-content .table-row-no-content");
        var a = d.clone();
        $(".no_records", a).text("No Compliance Available");
        $(".tbody-compliances-task-list-inprogress").append(a)
    }
    if (c_totalRecord2 == 0) {
        $(".compliance_count1").text("")
    } else {
        $(".compliance_count1").text("Total Over Due Compliances : " + c_totalRecord2)
    }
    if (c_totalRecord1 == 0) {
        $(".compliance_count2").text("")
    } else {
        $(".compliance_count2").text("Total Inprogress Compliances : " + c_totalRecord1)
    }
    if (b >= c_totalRecord1 + c_totalRecord2) {
        // $("#pagination").hide()
        ShowMoreButton.hide();
    } else {
        ShowMoreButton.show();
        // $("#pagination").show()
    }
    hideLoader()

    $('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
    $('[data-toggle="tooltip"]').tooltip();
}

$('.upcoming-tab').click(function() {
    if (sno == 0) {
        displayLoader();
        u_endCount = 0;
        $('.tbody-upcoming-compliances-list tr').remove();
        sno = 0;

        function onSuccess(data) {
            clearMessage();
            closeicon();
            u_totalRecord = data['total_count'];
            loadUpcomingCompliancesDetails(data['upcoming_compliances']);
            hideLoader();
        }

        function onFailure(error) {
            hideLoader();
        }
        if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
        client_mirror.getUpcomingComplianceDetail(parseInt(LegalEntityId.val()), unit_id, u_endCount, null, null,
            function(error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            }
        );
    }
});

function loadUpcomingCompliancesDetails(data) {
    $(".tbody-upcoming-compliances-list").empty();
    sno = 0;
    $.each(data, function(k, value) {
        if (countUpcoming == 0) {
            var tableRowHeading = $("#templates .table-upcoming-compliances-list .headingRow");
            var clone = tableRowHeading.clone();
            $(".uc-unit span", clone).html(data[k]['unit_name']);
            $(".uc-unit span", clone).attr("title", data[k].address);
            $(".tbody-upcoming-compliances-list").append(clone);
            countUpcoming++
        }

        var tableRowvalues = $('#templates .table-upcoming-compliances-list .table-row-list');
        var cloneval = tableRowvalues.clone();
        sno = sno + 1;
        $('.uc-sno', cloneval).text(sno);
        $('.uc-compliance-task span', cloneval).html(data[k]['compliance_name']);
        $(".uc-compliance-task i", cloneval).attr("title", data[k].compliance_description);
        $('.uc-compliance-task small', cloneval).html('Assigned on: ' + data[k].assigned_on);

        $('.uc-domain', cloneval).html(data[k]['domain_name']);
        $('.uc-startdate', cloneval).html(data[k]['start_date']);
        $('.uc-duedate', cloneval).html(data[k]['due_date']);

        if (data[k]['upcoming_format_file_name'] == null) {
            $('.uc-download', cloneval).empty();
        } else {
            $('.uc-download a', cloneval).attr("href", data[k]['upcoming_format_file_name']);
        }

        $('.tbody-upcoming-compliances-list').append(cloneval);

    });

    if (u_totalRecord == 0) {
        $('#pagination-upcoming').hide();
        $('.compliance_count_upcoming').text('');
    } else {
        $('.compliance_count_upcoming').text("Total Upcoming Compliances : " + u_totalRecord);
        if (sno >= u_totalRecord) {
            $('#pagination-upcoming').hide();
        } else {
            $('#pagination-upcoming').show();
        }
    }
}

function remove_uploaded_temp_file(a) {
    $(".uploaded" + a).remove();
    uploaded_file_list.splice(parseInt(a), 1);
}

function getCountryId(le_id) {
    var c_id = null;
    $.each(LEGAL_ENTITIES, function(k, v) {
        if (v.le_id == parseInt(le_id)) {
            c_id = v.c_id;
        }
    });
    return c_id;
}

function showSideBar(idval, data) {
    $(".half-width-task-details").empty();
    file_list = [];
    uploaded_file_list = [];
    $(".uploaded-filename").html("");
    var b = new Date().toLocaleDateString("en-GB", {
        year: "numeric",
        month: "short",
        day: "numeric"
    }).split(" ").join("-");
    $(".half-width-task-details").show();
    $(".full-width-list").attr("width", "60%");
    $(".half-width-task-details").attr("width", "40%");
    $(".half-width-task-details").css("display", "table");
    $(".attached-data").html("");
    //SideView append ---------------------------------------------------------------------
    $.each(data, function(key1, value) {
        if (data[key1].compliance_history_id == idval) {
            var l = [];
            $(".validity1_label").show();
            $(".duedate1_label").show();
            $(".validity1_textbox").hide();
            $(".duedate1_textbox").hide();

            var tableRowSide = $("#templates .sideview-div");
            var cloneValSide = tableRowSide.clone();
            var complianceStatus = data[key1]['compliance_status'];
            var rejected_reason = data[key1]['remarks'];

            $(".sideview-compliance-unit span", cloneValSide).html(data[key1]['unit_name']);
            $('.sideview-compliance-unit i', cloneValSide).attr('data-original-title', data[key1]['address']);

            $(".sideview-compliance-task span", cloneValSide).html(data[key1]['compliance_name']);
            $('.sideview-compliance-task i', cloneValSide).attr('data-original-title', data[key1]['compliance_description']);
            $(".sideview-compliance-frequency", cloneValSide).html(data[key1]['compliance_task_frequency']);
            $(".sideview-startdate", cloneValSide).val(data[key1]['start_date']);
            $(".sideview-completion-date-td", cloneValSide).html("<input  type='text' class='input-box datepick sideview-completion-date' id='completion-date' readonly='readonly'>");
            $(".sideview-compliance-status span", cloneValSide).html(complianceStatus);
            if (rejected_reason != null) {
                $("#rejected-reason-header", cloneValSide).show();
                $(".sideview-compliance-reason span", cloneValSide).html(rejected_reason)
            } else {
                $("#rejected-reason-header", cloneValSide).hide();
            }
            $(".sideview-upload-date", cloneValSide).html(currentDate.substring(0, 11));
            $(".sideview-remarks-td", cloneValSide).html("<textarea class='input-box sideview-remarks' maxlength='500'></textarea>");
            $("#upload_file", cloneValSide).on("change", function(e) {
                if (e.originalEvent.defaultPrevented) {
                    return
                }
                uploadedfile(e)
            });
            uploaded_file_list = data[key1].file_names;
            l = data[key1].download_url;
            if (uploaded_file_list != null && uploaded_file_list.length > 0) {
                $("#uploaded-documents-header", cloneValSide).show();
                for (var j = 0; j < uploaded_file_list.length; j++) {
                    if (uploaded_file_list[j] != "") {
                        // $(".sidebar-uploaded-documents", cloneValSide).append("<span clascs='uploaded" + j + "'><abbr class='sidebardocview'>" + uploaded_file_list[j] + "</abbr><a href='" + l[j] + "' download='" + l[j] + "' class='download-file' ><img src='/images/download.png' style='width:16px;height:16px' title='Download' /></a> <img src='/images/deletebold.png' style='width:16px;height:16px;' title='Remove' onclick='remove_uploaded_temp_file(\"" + j + "\")'/></span>");
                        // $(".tr-sidebar-uploaded-date", cloneValSide).show()

                        var tableDown = $('#templates .temp-download');
                        var cloneDown = tableDown.clone();
                        $(".uploaded", cloneDown).addClass("uploaded" + j);
                        $(".remove-file", cloneDown).attr("title", uploaded_file_list[j]);
                        // $(".download-file", cloneDown).attr("title", uploaded_file_list[j]);
                        $(".remove-file", cloneDown).attr("id", j);
                        $(".sidebardocview", cloneDown).html(uploaded_file_list[j]);
                        $(".remove-file", cloneDown).on("click", function() {
                            remove_uploaded_temp_file($(this).attr("id"));
                            // var getfilename = $(this).attr("title");
                            // console.log(getfilename);
                            // client_mirror.downloadTaskFile(LE_ID, getCountryId(LE_ID), data['domain_id'], data['unit_id'], data['start_date'], getfilename); // data.file_names[i]);
                        });
                        // $(".download-file", cloneDown).on("click", function() {
                        //     var getfilename = $(this).attr("title");
                        //     client_mirror.downloadTaskFile(LE_ID, getCountryId(LE_ID), data[key1]['domain_id'], data[key1]['unit_id'], data[key1]['start_date'], getfilename); //data.file_names[i]);
                        // });
                        $('.uploaded-filename', cloneValSide).html(cloneDown);
                        $('.tr-sidebar-uploaded-date', cloneValSide).show();

                    }
                }
            } else {
                $("#uploaded-documents-header", cloneValSide).hide()
            }
            if (data[key1].compliance_task_frequency == "One Time" || data[key1]['compliance_task_frequency'] == "On Occurrence") {
                $(".validityAndDueDate", cloneValSide).hide()
            } else {
                if (data[key1].compliance_task_frequency != "One Time") {
                    $(".validityAndDueDate", cloneValSide).show();
                    $(".validity1_icon", cloneValSide).on("click", function(e, complianceStatus) {
                        showTextbox(complianceStatus)
                    });
                    $('.validity1_label abbr', cloneValSide).html(data[key1]['validity_date']);
                    $('.duedate1_label abbr', cloneValSide).html(data[key1]['next_due_date']);
                    $('.validity1-textbox-input', cloneValSide).val(data[key1]['validity_date']);
                    $('.duedate1-textbox-input', cloneValSide).val(data[key1]['next_due_date']);
                }
            }

            $(".btn-submit", cloneValSide).on("click", function(s) {
                var completion_date;
                var compliance_history_id;
                var validity_date;
                var next_due_date;
                var start_date;

                compliance_history_id = data[key1]['compliance_history_id'];
                validity_settings_days = data[key1]['validity_settings_days'];

                function parseMyDate(s) {
                    return new Date(s.replace(/^(\d+)\W+(\w+)\W+/, '$2 $1 '));
                }

                var temp_documents = temp_file_list;
                var documents = file_list;

                if (documents.length == 0) {
                    documents = null;
                }

                uploaded_documents = uploaded_file_list;
                if (uploaded_documents.length == 0) {
                    uploaded_documents = null;
                }

                // validity_date = uploaded_file_list;
                // if (validity_date.length == 0) {
                //     validity_date = null
                // }


                // next_due_date = $('.duedate1_label').val();
                next_due_date = $('.duedate1-textbox-input').val();

                completion_date = $(".sideview-completion-date").val();
                // validity_date = $(".validity1-textbox-input").val();
                validity_date = $('.validity1_label abbr').html();
                if (validity_date == "") {
                    validity_date = $('.validity1-textbox-input').val();
                    if (validity_date == "") {
                        validity_date = null
                    } else {
                        if (validity_settings_days != 0) {
                            var convertDue = convert_date(next_due_date);
                            var convertValidity = convert_date(validity_date);

                            if (Math.abs(daydiff(convertDue, convertValidity)) <= validity_settings_days) {} else {
                                displayMessage(message.validity_date_before_after.replace('V_DAYS', validity_settings_days));
                                hideLoader();
                                return false;
                            }
                        }
                    }
                }

                if (next_due_date == '') {
                    next_due_date = $('.duedate1-textbox-input').val();
                    if (next_due_date == '') {
                        next_due_date = null;
                    }
                }
                remarks = $(".sideview-remarks").val();
                start_date = $('.sideview-startdate').val();

                if (remarks == "") {
                    remarks = null
                }
                if ($(".sideview-remarks").val().trim().length > 500) {
                    displayMessage("Remarks" + message.should_not_exceed + " 500 characters");
                    return false
                }
                if (completion_date == "") {
                    displayMessage(message.completiondate_required);
                    return
                }
                if (parseMyDate(start_date) > parseMyDate(completion_date)) {
                    displayMessage(message.complietion_gt_start);
                    return;
                }
                if (next_due_date != null) {
                    if (parseMyDate(start_date) > parseMyDate(next_due_date)) {
                        displayMessage(message.duedate_gt_start);
                        return;
                    }
                }

                if (parseMyDate(completion_date) > parseMyDate(currentDate)) {
                    displayMessage(message.completion_lt_current);
                    return;
                }
                if (currentDate != null && next_due_date != null) {
                    if (parseMyDate(currentDate) > parseMyDate(next_due_date)) {
                        displayMessage(message.nextduedate_gt_current);
                        return;
                    }
                }

                function onSuccess(data) {
                    initialize();
                    hideLoader();
                    custom_alert(message.compliance_uploaded_success)
                }

                function onFailure(error) {
                    hideLoader();
                    if (error == "NotEnoughSpaceAvailable") {
                        displayMessage(message.error)
                    } else {
                        if (error == "FileSizeExceedsLimit") {
                            displayMessage(message.filesize_exceeds_limit);
                        } else {
                            if (error == "ComplianceUpdateFailed") {
                                displayMessage(message.compliance_update_failed);
                            } else {
                                displayMessage(error)
                            }
                        }
                    }
                }
                displayLoader();
                client_mirror.updateComplianceDetail(parseInt(LegalEntityId.val()), compliance_history_id, documents, uploaded_documents, completion_date, validity_date, next_due_date, remarks,
                    function(error, response) {
                        if (error == null) {
                            saveUploadedFile();
                            onSuccess(response);
                            displaySuccessMessage(message.compliance_submit_success);
                        } else {
                            onFailure(error);
                        }
                    }
                );

                function saveUploadedFile() {
                    if ($(".attached-data").html() != "") {
                        var up_file = JSON.parse($(".attached-data").html());
                        if (up_file != null) {
                            client_mirror.uploadComplianceTaskFile(parseInt(LegalEntityId.val()), getCountryId(LegalEntityId.val()), data[key1]['domain_id'], data[key1]['unit_id'], data[key1]['start_date'], up_file,
                                function(error, response) {
                                    if (error == null) {
                                        $(".attached-data").html("");
                                        hideLoader();
                                    } else {
                                        console.log(error);
                                        hideLoader();
                                    }
                                });
                        }
                    }
                }
            });
            $(".half-width-task-details").append(cloneValSide);
            if (data[key1].compliance_task_frequency == "On Occurrence" && data[key1].duration_type == "2") {
                $('.datepick').datetimepicker({
                    changeMonth: true,
                    changeYear: true,
                    numberOfMonths: 1,
                    dateFormat: 'dd-M-yy',
                    monthNames: [
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                });

            } else {
                $(".datepick").datepicker({
                    changeMonth: true,
                    changeYear: true,
                    numberOfMonths: 1,
                    dateFormat: "dd-M-yy",
                    monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                });
            }


            $(".validity1-textbox-input", cloneValSide).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            });
            $(".duedate1-textbox-input", cloneValSide).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            });
            $(".sideview-remarks").on("input", function(k) {
                this.value = isCommon($(this))
            })
        }
    })
}

function addDays(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;
}

function loadCalendar(cal_date) {
    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getCalenderView(parseInt(LegalEntityId.val()), unit_id, cal_date, function(error, response) {
        if (error == null) {
            loadCalendarData(response);
        } else {
            onFailure(error);
        }
    });
}



function loadCalendarData(data) {
    $(".comp-calendar").empty();

    var wid_data = data.widget_data;
    var current_date = new Date(wid_data[0]['CurrentMonth']);
    var date = current_date;
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var month_value = current_date.getMonth();
    var year_value = current_date.getFullYear();
    var week_day = current_date.getDay();
    var html = '';
    var ct = $("#templates .calender-templates .cal");
    var ctclone = ct.clone();

    var previous = "<a href='##' class='prev'><i class='ti-angle-double-left text-info '></i></a>";
    var next = "<a href='##' class='next'><i class='ti-angle-double-right text-info '></i></a>";

    calDate = wid_data[0]['CurrentMonth'];

    if (curDate == "") {
        curDate = calDate;
    }
    if (minDate == "") {
        minDate = calDate;
    }
    if (maxDate == "") {
        var f = new Date(calDate);
        f.setMonth(f.getMonth() + 1);
        maxDate = f.getFullYear() + '-' + (('0' + (f.getMonth() + 5)).slice(-2)) + '-' + ('0' + (f.getDate())).slice(-2)
    }
    if (minDate == calDate) {
        previous = "";
    }
    if (maxDate == calDate) {
        next = "";
    }

    $(".cal-caption", ctclone).html(previous + (months[month_value] + " - " + year_value) + next);
    $(".comp-calendar").append(ctclone);

    day = date.getDate();
    month = date.getMonth();
    year = date.getFullYear();

    months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
    this_month = new Date(year, month, 1);
    next_month = new Date(year, month + 1, 1);
    // Find out when this month starts and ends.
    first_week_day = this_month.getDay();
    days_in_this_month = Math.round((next_month.getTime() - this_month.getTime()) / (1000 * 60 * 60 * 24));

    calendar_html = '';
    calendar_html += '<tr>';
    for (week_day = 0; week_day < first_week_day; week_day++) {
        calendar_html += '<td class="cal-off"> </td>';
    }
    week_day = first_week_day;
    for (day_counter = 1; day_counter <= days_in_this_month; day_counter++) {
        week_day %= 7;
        if (week_day == 0)
            calendar_html += '</tr><tr>';
        if (day == day_counter)
            calendar_html += '<td class="dateid' + day_counter + '"><div class="date">' + day_counter + '</div></td>';
        else
            calendar_html += '<td class="dateid' + day_counter + '"><div class="date">' + day_counter + '</div></td>';
        week_day++;
    }

    calendar_html += '</tr>';

    $(".comp-calendar .cal-body").append(calendar_html);

    var getdata = wid_data[0]['data'];
    $.each(getdata, function(k, v) {
        if (v.inprogress > 0) {
            $(".dateid" + v.date).append('<div class="count-round inprogress" data-toggle="tooltip" data-original-title="' + v.inprogress + ' Inprogress Compliances"> ' + v.inprogress + ' </div>');
            $('.dateid' + v.date + ' .inprogress').on('click', function() {
                var clickDate = new Date(year_value, ('0' + month_value).slice(-2), ('0' + v.date).slice(-2));
                var clickDate1 = date_format(clickDate);
                showCurrentTab("INPROGRESS", clickDate1);
            });
        }
        if (v.duedate > 0) {
            $(".dateid" + v.date).append('<div class="count-round due-date" data-toggle="tooltip" data-original-title="' + v.duedate + ' Due Date Compliances"> ' + v.duedate + '</div>');
            $('.dateid' + v.date + ' .due-date').on('click', function() {
                var clickDate = new Date(year_value, ('0' + month_value).slice(-2), ('0' + v.date).slice(-2));
                var clickDate1 = date_format(clickDate);
                showCurrentTab("DUEDATE", clickDate1);
            });
        }
        if (v.upcoming > 0) {
            $(".dateid" + v.date).append('<div class="count-round upcomming" data-toggle="tooltip" data-original-title="' + v.upcoming + ' Upcoming Compliances">' + v.upcoming + '</div>');
            $('.dateid' + v.date + ' .upcomming').on('click', function() {
                var clickDate = new Date(year_value, ('0' + month_value).slice(-2), ('0' + v.date).slice(-2));
                var clickDate1 = date_format(clickDate);
                showUpcomingTab("UPCOMING", clickDate1);
            });
        }
        if (v.overdue > 0) {
            $(".dateid" + v.date).append('<div class="count-round over-due" data-toggle="tooltip" data-original-title="' + v.overdue + ' Over Due">' + v.overdue + '</div>');
            $('.dateid' + v.date + ' .over-due').on('click', function() {
                var clickDate = new Date(year_value, ('0' + month_value).slice(-2), ('0' + v.date).slice(-2));
                var clickDate1 = date_format(clickDate);
                showCurrentTab("OVERDUE", clickDate1);
            });
        }
    });
}

function showTextbox(complianceStatus) {
    $(".duedate1_textbox").show();
    $(".duedate1_label").hide();
    $(".validity1_textbox").show();
    $(".validity1_label").hide()
}

function closeicon() {
    $(".uploaded-filename").html("");
    $(".half-width-task-details").hide();
    $(".full-width-list").attr("width", "100%");
    $(".half-width-task-details").attr("width", "0%");
    $("input.validity1-textbox-input").datepicker("destroy");
    $("input.duedate1-textbox-input").datepicker("destroy");
    $(".tbody-compliances-task-list-overdue tr").removeClass("active1");
}

function uploadedfile(e) {
    client_mirror.uploadFile(e, function result_data(data) {

        if (data == "File max limit exceeded") {
            displayMessage(message.file_maxlimit_exceed);
            $(".uploaded_filename").html('');
            $("#upload_file").val("");
            return;
        } else if (data != 'File max limit exceeded' || data != 'File content is empty') {
            uploadFile = data;
            file_list = data
            temp_file_list = data
            $(".attached-data").html(JSON.stringify(data));
            var result = "";
            for (i = 0; i < data.length; i++) {
                var fileclassname;
                var filename = data[i]['file_name'];
                fileclassname = filename.replace(/[^\w\s]/gi, "");
                fileclassname = fileclassname.replace(/\s/g, "");
                // var fN = filename.substring(0, filename.indexOf('.'));
                // var fE = filename.substring(filename.lastIndexOf('.') + 1);
                // var uniqueId = Math.floor(Math.random() * 90000) + 10000;
                // var f_Name = fN + '-' + uniqueId + '.' + fE;

                result += "<span class='" + fileclassname + "'>" + filename + "<i class='fa fa-times text-primary removeicon' onclick='remove_temp_file(\"" + fileclassname + "\")' ></i></span>";
            }
            $(".uploaded-filename").html(result);
        }
    });
}

function remove_temp_file(b, a) {
    $("." + b).remove();
    for (var c = 0; c < file_list.length; c++) {
        if (file_list[c].file_name == a) {
            file_list.splice(c, 1)
        }
    }
    $("#upload_file").val("")
}

ShowButton.click(function() {
    if (LegalEntityId.val().trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else {
        basicwizard.show();
        initialize();
        showCalendarTab();
    }
});

ShowMoreButton.click(function() {
    c_endCount = snoOverdue + snoInprogress - 2;

    function onSuccess(data) {
        closeicon();
        currentCompliances = data['current_compliances'];
        c_totalRecord1 = data['inprogress_count'];
        c_totalRecord2 = data['overdue_count'];
        currentDate = data['current_date'];
        loadComplianceTaskDetails(currentCompliances);
        hideLoader();
    }

    function onFailure(error) {
        hideLoader()
    }
    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getCurrentComplianceDetail(parseInt(LegalEntityId.val()), unit_id, c_endCount, null, null, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    })
});

function loadUnits(le_id, unit_id) {
    client_mirror.complianceFilters(le_id, function(error, response) {
        if (error == null) {
            unitList = response.user_units;
        }
    });
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    if (id_element[0].id == 'legal_entity_id') {
        loadUnits(parseInt(LegalEntityId.val()));
    }
}

//Unit Auto Complete
txtUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(
        e, divUnit, hdnUnit, text_val,
        unitList, "unit_name", "unit_id",
        function(val) {
            onAutoCompleteSuccess(txtUnit, hdnUnit, val);
        }, condition_fields, condition_values);
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
        loadUnits(parseInt(LegalEntityId.val()));
        ShowButton.trigger("click");
    }
}

function showCalendarTab() {
    $(".calendar-tab").addClass("active");
    $(".calendar-tab-content").addClass("active in");

    $(".current-tab").removeClass("active");
    $(".current-tab-content").removeClass("active in");

    $(".upcoming-tab").removeClass("active");
    $(".upcoming-tab-content").removeClass("active in");

    $(".calendar-tab-content").show();
    $(".upcoming-tab-content").hide();
    $(".current-tab-content").hide();
}

function showCurrentTab(countName, clickDate) {
    $(".current-tab").addClass("active");
    $(".current-tab-content").addClass("active in");

    $(".upcoming-tab").removeClass("active");
    $(".upcoming-tab-content").removeClass("active in");

    $(".calendar-tab").removeClass("active");
    $(".calendar-tab-content").removeClass("active in");

    $(".current-tab-content").show();
    $(".upcoming-tab-content").hide();
    $(".calendar-tab-content").hide();


    function onSuccess(data) {
        closeicon();
        currentCompliances = data['current_compliances'];
        if (countName == null) {
            c_totalRecord1 = data['inprogress_count'];
            c_totalRecord2 = data['overdue_count'];

        } else {
            c_totalRecord1 = 0;
            c_totalRecord2 = 0;
            $.each(currentCompliances, function(key, value) {
                if (currentCompliances[key].compliance_status == "Not Complied") {
                    c_totalRecord2++;
                }
                if (currentCompliances[key].compliance_status == "Inprogress") {
                    c_totalRecord1++;
                }
            });
        }
        currentDate = data['current_date'];
        loadComplianceTaskDetails(currentCompliances);
        hideLoader();
    }

    function onFailure(error) {
        hideLoader()
    }
    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getCurrentComplianceDetail(parseInt(LegalEntityId.val()), unit_id, c_endCount, countName, clickDate, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    })

}

function showUpcomingTab(countName, clickDate) {
    $(".upcoming-tab").addClass("active");
    $(".upcoming-tab-content").addClass("active in");

    $(".current-tab").removeClass("active");
    $(".current-tab-content").removeClass("active in");

    $(".calendar-tab").removeClass("active");
    $(".calendar-tab-content").removeClass("active in");

    $(".upcoming-tab-content").show();
    $(".current-tab-content").hide();
    $(".calendar-tab-content").hide();

    function onSuccess(data) {
        clearMessage();
        closeicon();
        u_totalRecord = data['total_count'];
        loadUpcomingCompliancesDetails(data['upcoming_compliances']);
        hideLoader();
    }

    function onFailure(error) {
        console.log(error);
        hideLoader();
    }
    if (hdnUnit.val() != "") { var unit_id = parseInt(hdnUnit.val()); } else { var unit_id = null }
    client_mirror.getUpcomingComplianceDetail(parseInt(LegalEntityId.val()), unit_id, u_endCount, countName, clickDate,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

$(function() {
    loadEntityDetails();
});

$('.js-filtertable').each(function() {
    $(this).filtertable().addFilter('.js-filter');
});

$(document).find(".js-filtertable-upcoming").each(function() {
    $(this).filtertable().addFilter(".js-filter-upcoming");
});

$(document).ready(function() {
    $(".calendar-tab").click(function() {
        showCalendarTab();
    });

    $(".current-tab").click(function() {
        showCurrentTab(null, null);
    });

    $(".upcoming-tab").click(function() {
        showUpcomingTab(null, null);
    });

    $(document).on('click', '.next', function() {
        var nextDate = new Date(calDate);
        nextDate.setMonth(nextDate.getMonth() + 1);
        loadCalendar(date_format(nextDate));
    });

    $(document).on('click', '.prev', function() {
        var prevDate = new Date(calDate);
        prevDate.setMonth(prevDate.getMonth() - 1);
        var passDate = prevDate.getFullYear() + '-' + (('0' + (prevDate.getMonth() + 1)).slice(-2)) + '-' + ('0' + (prevDate.getDate())).slice(-2)
        if (curDate == passDate)
            loadCalendar(null);
        else
            loadCalendar(date_format(prevDate));
    });

});