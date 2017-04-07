var users = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");

var fromDate = $("#from_date");
var toDate = $("#to_date");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;
var u_g_id = null;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var _page_limit = 25;
var csv = false;

function PageControls() {
    $(".from-date, .to-date").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
        onSelect: function(selectedDate) {
            if ($(this).hasClass("from-date") == true) {
                var fromDate = $('.from-date').datepicker('getDate');
                var dateMax = new Date(fromDate.getFullYear(), fromDate.getMonth(), fromDate.getDate());
                var dateMin = new Date(fromDate.getFullYear(), fromDate.getMonth(), fromDate.getDate());
                $('.to-date').datepicker('setDate', dateMax);
                $('.to-date').datepicker("option", "minDate", dateMin);
                $('.to-date').datepicker("option", "maxDate", dateMax);
            }
            if ($(this).hasClass("to-date") == true) {
                var dateMin = $('.to-date').datepicker('getDate');
            }
        }
    });

    toDate.val(current_date());
    fromDate.val(past_days(7));

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        commonAutoComplete(e, acUser, userId, text_val, userList, "user_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        });
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            _on_current_page = 1;
            _sno = 0;
            _total_record = 0;
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            csv = true;
            REPORT.exportReportValues();
        }
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        _on_current_page = 1;
        _sno = 0;
        createPageView(_total_record);
        csv = false;
        REPORT.fetchReportValues();
    });
}

clearElement = function(arr) {
    if(arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    users.focus();
}

LoginTraceReport = function() {
    this._users = [];
    this._report_data = [];
    /*this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;*/
    this._LoginTraceList = [];
}

LoginTraceReport.prototype.loadSearch = function() {
    reportView.hide();
    users.val('');
    userId.val('');
    this.fetchUserList();
};

LoginTraceReport.prototype.fetchUserList = function() {
    t_this = this;
    client_mirror.getLoginTraceReportFilters(function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._users = response.audit_users_list;
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LoginTraceReport.prototype.validate = function() {
    if (users) {
        if (isLengthMinMax(users, 0, 100, message.user_max) == false)
            return false;
        else if (isCommonName(users, message.user_str) == false)
            return false;
    }
    if (fromDate) {
        if (isNotEmpty(fromDate, message.fromdate_required) == false)
            return false;
    }
    if (toDate) {
        if (isNotEmpty(toDate, message.todate_required) == false)
            return false;
    }
    return true;
};

showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
}

LoginTraceReport.prototype.fetchReportValues = function() {
    t_this = this;
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;

    f_date = fromDate.val();
    t_date = toDate.val();

    _page_limit = parseInt(ItemsPerPage.val());
    if (_on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (_on_current_page - 1) *  _page_limit;
    }
    console.log(_sno, _on_current_page)
    client_mirror.getLoginTraceReportData(
        parseInt(user_id), f_date, t_date, csv, _sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._LoginTraceList = response.log_trace_activities;
            t_this._total_record = response.total_count;
            if (response.total_count == 0) {
                hidePageView();
                hidePagePan();
                //Export_btn.hide();
                PaginationView.hide();
                t_this.showReportValues();
            }
            else{
                if (_sno == 0) {
                    createPageView(t_this._total_record);
                }
                //Export_btn.show();
                PaginationView.show();
                t_this.showReportValues();
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LoginTraceReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._LoginTraceList;
    $('.from-header').text(fromDate.val());
    $('.to-header').text(toDate.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var is_null = true;
    showFrom = _sno + 1;
    $.each(data, function(k, v) {
        console.log(data.length)
        is_null = false;
        $('.client-logo').attr("src", v.logo_url);

        var clonethree = $('#template #report-table .row-three').clone();
        _sno += 1;
        $('.sno', clonethree).text(_sno);
        if (v.activity_date != "")
            $('.activity-date', clonethree).text(v.created_on);
        else
            $('.activity-date', clonethree).text('-');
        $('.form-name', clonethree).text(v.form_name);
        $('.form-action', clonethree).text(v.action);

        reportTableTbody.append(clonethree);

    });

    if (is_null == true) {
        //a_page.hidePagePan();
        reportTableTbody.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        reportTableTbody.append(clone4);
    }
    else {
        showPagePan(showFrom, _sno, t_this._total_record);
    }
};

LoginTraceReport.prototype.exportReportValues = function() {
    t_this = this;
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;

    f_date = fromDate.val();
    t_date = toDate.val();



    client_mirror.getLoginTraceReportData(
        parseInt(user_id), f_date, t_date, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            if(csv){
                document_url = response.link;
                window.open(document_url, '_blank');
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LoginTraceReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

// Pagination Functions - begins
hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

createPageView = function(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            console.log(cPage, _on_current_page)
            if (parseInt(_on_current_page) != cPage) {
                _on_current_page = cPage;
                REPORT.fetchReportValues();
            }
        }
    });
};
showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}
// Pagination Ends

REPORT = new LoginTraceReport();

$(document).ready(function() {
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
});