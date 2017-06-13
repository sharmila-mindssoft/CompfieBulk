var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal-entity");
var LegalEntityId = $("#legal-entity-id");
var ACLegalEntity = $("#ac-legal-entity");

var users = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");

var FormName = $("#form");
var FormId = $("#form-id");
var ACForm = $("#ac-form");

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

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function PageControls() {
    $(".from-date, .to-date").datepicker({
        showButtonPanel: true,
        closeText: 'Clear',
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
        onSelect: function(selectedDate) {
            if ($(this).hasClass("from-date") == true) {
                var dateMin = $('.from-date').datepicker("getDate");
                var rMin = new Date(dateMin.getFullYear(), dateMin.getMonth(), dateMin.getDate()); // +1
                $('.to-date').datepicker("option", "minDate", rMin);
                var event = arguments.callee.caller.caller.arguments[0];
                if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
                    $(this).val('');
                }
            }
            if ($(this).hasClass("to-date") == true) {
                var dateMin = $('.to-date').datepicker("getDate");
            }
        }
    });

    /*current_date(function (c_date) {
        toDate.val(c_date);
    });

    current_date_ymd(function (c_date) {
        var dateMax = date_format(new Date(c_date.getFullYear(), c_date.getMonth() , c_date.getDate() - 7));
        fromDate.val(dateMax);
    });*/

    LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        });
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        commonAutoComplete(e, acUser, userId, text_val, userList, "user_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        });
    });

    FormName.keyup(function(e) {
        var text_val = FormName.val().trim();
        var formList = REPORT._forms;
        var condition_fields = ["u_g_id"];
        var condition_values = [u_g_id];
        commonAutoComplete(e, ACForm, FormId, text_val, formList, "form_name", "form_id", function(val) {
            onFormAutoCompleteSuccess(REPORT, val);
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
        createPageView(t_this._total_record);
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

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([users, userId, FormId, FormName]);
    reportView.hide();
    REPORT.fetchUserList(val[0]);
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    for (var i=0;i<REPORT._users.length;i++){
    	if (REPORT._users[i].user_id == val[0]){
    		u_g_id = REPORT._users[i].u_g_id;
    		break;
    	}
    }
    users.focus();
    clearElement([FormId, FormName]);
}

onFormAutoCompleteSuccess = function(REPORT, val) {
    FormName.val(val[1]);
    FormId.val(val[0]);
    FormName.focus();
}

AuditTrailReport = function() {
    this._entities = [];
    this._users = [];
    this._forms = [];
    this._report_data = [];
    this._AuditTrailList = [];
}

AuditTrailReport.prototype.loadSearch = function() {
    reportView.hide();
    LegalEntityName.val('');
    LegalEntityId.val('');
    users.val('');
    userId.val('');
    FormName.val('');
    FormId.val('');
    this.fetchSearchList();
};

AuditTrailReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

AuditTrailReport.prototype.loadEntityDetails = function(){
    t_this = this;
    if(t_this._entities.length > 1){
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
    }else{
        le_name = t_this._entities[0]["le_name"];
        le_id = t_this._entities[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(le_name);
        LegalEntityName.val(le_name);
        LegalEntityId.val(le_id);
        REPORT.fetchUserList(le_id);
    }
    hideLoader();
};

AuditTrailReport.prototype.fetchUserList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getAuditTrailReportFilters(parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._users = response.audit_users_list;
            t_this._forms = response.audit_forms_list;
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

AuditTrailReport.prototype.validate = function() {
    if (LegalEntityName) {
        if (isNotEmpty(LegalEntityName, message.legalentity_required) == false)
            return false;
        else if (isLengthMinMax(LegalEntityName, 1, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(LegalEntityName, message.legalentity_str) == false)
            return false;
    }
    if (users) {
        if (isLengthMinMax(users, 0, 100, message.user_max) == false)
            return false;
        else if (isCommonName(users, message.user_str) == false)
            return false;
    }
    if (FormName) {
        if (isLengthMinMax(FormName, 0, 50, message.form_max) == false)
            return false;
        else if (isCommonName(FormName, message.form_str) == false)
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

AuditTrailReport.prototype.fetchReportValues = function() {
    t_this = this;
    le_id = LegalEntityId.val();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    form_id = FormId.val();
    if (form_id == "")
        form_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    check_count = false;

    _page_limit = parseInt(ItemsPerPage.val());
    if (_on_current_page == 1) {
        _sno = 0;
        check_count = true;
    }
    else {
        _sno = (_on_current_page - 1) *  _page_limit;
        check_count = false;
    }
    displayLoader();
    client_mirror.getAuditTrailReportData(
        parseInt(le_id), parseInt(user_id), parseInt(form_id), f_date, t_date, csv, _sno, _page_limit, check_count,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._AuditTrailList = response.audit_activities;
            if (check_count == true)
                t_this._total_record = response.total_count;
            if (response.audit_activities.length == 0) {
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
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

AuditTrailReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._AuditTrailList;
    $('.le-header').text(LegalEntityName.val());
    $('.from-header').text(fromDate.val());
    $('.to-header').text(toDate.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var is_null = true;
    showFrom = _sno + 1;
    $.each(data, function(k, v) {
        console.log(data.length);
        is_null = false;
        $('.client-logo').attr("src", v.logo_url);

        var clonethree = $('#template #report-table .row-three').clone();
        _sno += 1;
        $('.sno', clonethree).text(_sno);
        $('.user-name', clonethree).text(v.user_name);
        if (v.activity_date != "")
            $('.activity-date', clonethree).text(v.created_on);
        else
            $('.activity-date', clonethree).text('-');
        var form_name = null;
        for (var i=0;i<REPORT._forms.length;i++){
        	if(REPORT._forms[i].form_id == v.form_id){
        		form_name = REPORT._forms[i].form_name;
        		break;
        	}
        }
        $('.form-name', clonethree).text(form_name);
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

AuditTrailReport.prototype.exportReportValues = function() {
    t_this = this;
    le_id = LegalEntityId.val();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    form_id = FormId.val();
    if (form_id == "")
        form_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();

    displayLoader();
    client_mirror.getAuditTrailReportData(
        parseInt(le_id), parseInt(user_id), parseInt(form_id), f_date, t_date, csv, 0, 0, false,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            if(csv){
                document_url = response.link;
                //window.open(document_url, '_blank');
                $(location).attr('href', document_url);
            }
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

AuditTrailReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage(message.domainname_exists);
    } else if (error == "ExportToCSVEmpty") {
        displayMessage(message.empty_export);
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

REPORT = new AuditTrailReport();

$(document).ready(function() {
    displayLoader();
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
