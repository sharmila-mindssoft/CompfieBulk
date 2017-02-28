var currentCompliances;
var file_list = [];
var currentDate;
var c_endCount = 0;
var u_endCount = 0;
var c_totalRecord1;
var c_totalRecord2;
var u_totalRecord;
var snoOverdue = 1;
var snoInprogress = 1;
var countOverdue = 0;
var countInprogress = 0;
var sno = 0;
var uploaded_file_list = [];

function displayLoader() {
    $(".loading-indicator-spin").show()
}

function hideLoader() {
    $(".loading-indicator-spin").hide()
}

function initialize() {
    displayLoader();
    c_endCount = 0;
    $(".tbody-compliances-task-list-overdue tr").remove();
    $(".tbody-compliances-task-list-inprogress tr").remove();
    $(".uploaded-filename").empty();
    snoOverdue = 1;
    snoInprogress = 1;
    countOverdue = 0;
    countInprogress = 0;
    closeicon();

    function b(c) {
        closeicon();
        currentCompliances = c.current_compliances;
        c_totalRecord1 = c.inprogress_count;
        c_totalRecord2 = c.overdue_count;
        currentDate = c.current_date;
        loadComplianceTaskDetails(currentCompliances)
    }

    function a(c) {
        displayMessage(c);
        hideLoader()
    }
    client_mirror.getCurrentComplianceDetail(2, c_endCount, function(d, c) {
        if (d == null) {
            b(c)
        } else {
            a(d)
        }
    })
}

function loadComplianceTaskDetails(c) {
    $.each(c, function(f, h) {
        if (c[f].compliance_status == "Not Complied" && countOverdue == 0) {
            var g = $("#templates .table-compliances-task-list .headingRow");
            var m = g.clone();
            $(".compliance-types", m).html("Over due Compliances");
            $(".tbody-compliances-task-list-overdue").append(m);
            countOverdue++
        }
        if (c[f].compliance_status == "Inprogress" && countInprogress == 0) {
            var g = $("#templates .table-compliances-task-list .headingRow");
            var m = g.clone();
            $(".compliance-types", m).html("Inprogress Compliances");
            $(".tbody-compliances-task-list-inprogress").append(m);
            countInprogress++
        }
        var e = $("#templates .table-compliances-task-list .table-row-list");
        var j = e.clone();
        $(".compliance-task span", j).html(c[f].compliance_name);
        $(".compliance-task", j).attr("title", c[f].compliance_description);
        $(".domain", j).html(c[f].domain_name);
        $(".startdate", j).html(c[f].start_date);
        $(".duedate", j).html(c[f].due_date);
        $(".days-text", j).html(c[f].ageing);
        if (c[f].compliance_status == "Not Complied") {
            $(".days-text", j).attr("style", "color:#f00;")
        }
        if (c[f].remarks != null) {
            $(".sno", j).attr("style", "color:#f00;");
            $(".compliance-task", j).attr("style", "color:#f00;");
            $(".domain", j).attr("style", "color:#f00;");
            $(".startdate", j).attr("style", "color:#f00;");
            $(".duedate", j).attr("style", "color:#f00;");
            $(".days-text", j).attr("style", "color:#f00;");
            $(".status", j).attr("style", "color:#f00;")
        }
        $(".status", j).html(c[f].compliance_status);
        if (c[f].format_file_name != null) {
            $(".format-file", j).attr("href", c[f].format_file_name)
        } else {
            $(".format-file", j).hide()
        }
        var l = c[f].compliance_history_id;
        $(j, ".expand_inprogress").on("click", function() {
            $(".table-row-list").removeClass("active1");
            $(j, ".table-row-list").addClass("active1");
            showSideBar(l, c)
        });
        if (c[f].compliance_status == "Not Complied") {
            $(".sno", j).text(snoOverdue);
            $(".tbody-compliances-task-list-overdue").append(j);
            snoOverdue = snoOverdue + 1
        }
        if (c[f].compliance_status == "Inprogress" || c[f].compliance_status == "Inprogress(Rejected)") {
            $(".sno", j).text(snoInprogress);
            $(".tbody-compliances-task-list-inprogress").append(j);
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
        $("#pagination").hide()
    } else {
        $("#pagination").show()
    }
    hideLoader()
}

// function remove_uploaded_temp_file(a) {
//     $(".uploaded" + a).remove();
//     uploaded_file_list.splice(parseInt(a), 1)
// }
// $(".expand_inprogress ").click(function() {
//     $('.expand_inprogress').removeClass('info');
//     $(".td_inprogress ").show();
//     $(this).addClass('info');
//     if ($(this).attr("id ") == "2 ")
//         $(".val-date ").show();
//     else
//         $(".val-date ").hide();
// });

function showSideBar(c, a) {
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
    $.each(a, function(g, m) {
        if (a[g].compliance_history_id == c) {
            var l = [];
            $(".validity1_label").show();
            $(".duedate1_label").show();
            $(".validity1_textbox").hide();
            $(".duedate1_textbox").hide();
            var f = $("#templates .sideview-div");
            var e = f.clone();
            var h = a[g].compliance_status;
            var d = a[g].remarks;
            $(".sideview-compliance-unit span", e).html(a[g].unit_name);
            // $(".sideview-compliance-unit abbr", e).attr("title", a[g].address);
            $(".sideview-compliance-task .ct", e).html(a[g].compliance_name);
            // $(".sideview-compliance-task abbr", e).attr("title", a[g].compliance_description);
            $(".sideview-compliance-frequency", e).html(a[g].compliance_task_frequency);
            $(".sideview-startdate", e).val(a[g].start_date);
            $(".sideview-completion-date-td", e).html("<input  type='text' class='input-box datepick sideview-completion-date' id='completion-date' readonly='readonly'>");
            $(".sideview-compliance-status", e).html(h);
            if (d != null) {
                $("#rejected-reason-header", e).show();
                $(".sideview-compliance-reason", e).html(d)
            } else {
                $("#rejected-reason-header", e).hide()
            }
            $(".sideview-upload-date", e).html(currentDate.substring(0, 11));
            $(".sideview-remarks-td", e).html("<textarea class='input-box sideview-remarks' maxlength='500'></textarea>");
            $("#upload_file", e).on("change", function(k) {
                // if (k.originalEvent.defaultPrevented) {
                //     return
                // }
                // uploadedfile(k)
            });
            uploaded_file_list = a[g].file_names;
            l = a[g].download_url;
            if (uploaded_file_list != null && uploaded_file_list.length > 0) {
                // $("#uploaded-documents-header", e).show();
                // for (var j = 0; j < uploaded_file_list.length; j++) {
                //     if (uploaded_file_list[j] != "") {
                //         $(".sidebar-uploaded-documents", e).append("<span class='uploaded" + j + "'><abbr class='sidebardocview'>" + uploaded_file_list[j] + "</abbr><a href='" + l[j] + "' download='" + l[j] + "' class='download-file' ><img src='/images/download.png' style='width:16px;height:16px' title='Download' /></a> <img src='/images/deletebold.png' style='width:16px;height:16px;' title='Remove' onclick='remove_uploaded_temp_file(\"" + j + "\")'/></span>");
                //         $(".tr-sidebar-uploaded-date", e).show()
                //     }
                // }
            } else {
                $("#uploaded-documents-header", e).hide()
            }
            if (a[g].compliance_frequency == "One Time" || a[g].compliance_frequency == "On Occurrence") {
                $(".validityAndDueDate", e).hide()
            } else {
                if (a[g].compliance_frequency != "One Time") {
                    $(".validityAndDueDate", e).show();
                    $(".validity1_icon", e).on("click", function(n, k) {
                        showTextbox(k)
                    });
                    $(".validity1_label abbr", e).html(a[g].validity_date);
                    $(".duedate1_label abbr", e).html(a[g].next_due_date);
                    $(".validity1-textbox-input", e).val(a[g].validity_date);
                    $(".duedate1-textbox-input", e).val(a[g].next_due_date)
                }
            }
            $(".btn-submit", e).on("click", function(s) {
                var o;
                var n;
                var v = [];
                var p = [];
                var q;
                var w;
                var r;
                n = a[g].compliance_history_id;

                // function u(x) {
                //     return new Date(x.replace(/^(\d+)\W+(\w+)\W+/, "$2 $1 "))
                // }
                v = file_list;
                if (v.length == 0) {
                    v = null
                }
                p = uploaded_file_list;
                if (p.length == 0) {
                    p = null
                }
                o = $(".sideview-completion-date").val();
                q = $(".validity1-textbox-input").val();
                if (q == "") {
                    q = $(".validity1_label abbr").html();
                    if (q == "") {
                        q = null
                    }
                }
                w = $(".duedate1-textbox-input").val();
                if (w == "") {
                    w = $(".duedate1_label").val();
                    if (w == "") {
                        w = null
                    }
                }
                remarks = $(".sideview-remarks").val();
                r = $(".sideview-startdate").val().split(" ")[0];
                if (remarks == "") {
                    remarks = null
                }
                if ($(".sideview-remarks").val().trim().length > 500) {
                    displayMessage("Remarks" + message.should_not_exceed + " 500 characters");
                    return false
                }
                if (o == "") {
                    displayMessage(message.completiondate_required);
                    return
                }
                if (q == "") {
                    displayMessage(message.validitydate_required);
                    return
                }
                if (a[g].compliance_frequency == "Periodical") {
                    if (q == "" || q == null) {
                        displayMessage(message.validitydate_required);
                        return
                    }
                }
                // if (u(r) > u(o)) {
                //     displayMessage(message.complietion_gt_start);
                //     return
                // }
                if (q != null) {
                    if (u(r) > u(q)) {
                        displayMessage(message.validity_gt_start);
                        return
                    }
                }
                if (w != null) {
                    // if (u(r) > u(w)) {
                    //     displayMessage(message.duedate_gt_start);
                    //     return
                    // }
                }
                // if (u(o) > u(currentDate)) {
                //     displayMessage(message.completion_lt_current);
                //     return
                // }
                if (currentDate != null && w != null) {
                    // if (u(currentDate) > u(w)) {
                    //     displayMessage(message.nextduedate_gt_current);
                    //     return
                    // }
                }
                if (q != null && w != null) {
                    // if (u(q) < u(w)) {
                    //     displayMessage(message.validity_gt_nextduedate);
                    //     return
                    // }
                }

                function t(x) {
                    initialize();
                    hideLoader();
                    custom_alert(message.compliance_uploaded_success)
                }

                function k(x) {
                    hideLoader();
                    if (x == "NotEnoughSpaceAvailable") {
                        displayMessage(message.error)
                    } else {
                        if (x == "FileSizeExceedsLimit") {
                            displayMessage(message.filesize_exceeds_limit)
                        } else {
                            if (x == "ComplianceUpdateFailed") {
                                displayMessage(message.compliance_update_failed)
                            } else {
                                displayMessage(x)
                            }
                        }
                    }
                }
                displayLoader();
                if (v != null) {
                    $(".upload-progress-count").html("");
                    $(".upload-progress-count").show()
                }
                var le_id = 2;
                client_mirror.updateComplianceDetail(le_id, n, v, p, o, q, w, remarks,
                    function(error, response) {
                        if (error == null) {
                            // onSuccess(response);
                        } else {
                            // onFailure(error);
                        }
                    }
                );

                // client_mirror.updateComplianceDetail(compliance_history_id, documents,
                //     completion_date, validity_date, next_due_date, remarks,

                //     function (error, response){
                //         if(error == null){
                //             onSuccess(response);
                //         }
                //         else{
                //             onFailure(error);
                //         }
                //     }
                // );

            });
            $(".half-width-task-details").append(e);
            $(".datepick").datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            });
            $(".validity1-textbox-input", e).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            });
            $(".duedate1-textbox-input", e).datepicker({
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

function showTextbox(a) {
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
    $("input.duedate1-textbox-input").datepicker("destroy")
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
$(function() {
    initialize()
});
$(document).find(".js-filtertable").each(function() {
    $(this).filtertable().addFilter(".js-filter")
});
$(document).find(".js-filtertable-upcoming").each(function() {
    $(this).filtertable().addFilter(".js-filter-upcoming")
});
$(document).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function(a, b) {
            $(this).css(a);
            $("<div>").addClass("arrow").addClass(b.vertical).addClass(b.horizontal).appendTo(this)
        }
    }
});
$(document).ready(function() {
    $(".current-tab").click(function() {
        $(".current-tab").addClass("active");
        $(".upcoming-tab").removeClass("active");
        $(".main-tab-content").show();
        $(".upcoming-tab-content").hide()
    });
    $(".upcoming-tab").click(function() {
        $(".upcoming-tab").addClass("active");
        $(".current-tab").removeClass("active");
        $(".main-tab-content").hide();
        $(".upcoming-tab-content").show()
    });
    $(".close").click(function() {
        $(".current-tab-content").hide();
        $(".main-tab-content").show()
    })
});