var ServiceProvider = $("#service-provider");
var ServiceProviderId = $("#service-provider-id");
var ACServiceProvider = $("#ac-service-provider");

var users = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");

var ServiceProviderStatus = $("#sp-status");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;

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
    ServiceProvider.keyup(function(e) {
        var text_val = ServiceProvider.val().trim();
        var spList = REPORT._sp_list;
        commonAutoComplete(e, ACServiceProvider, ServiceProviderId, text_val, spList, "sp_name", "sp_id", function(val) {
            onServiceProviderAutoCompleteSuccess(REPORT, val);
        });
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        if (ServiceProviderId.val() != ""){
        	var condition_fields = ["sp_id_optional"];
        	var condition_values = [ServiceProviderId.val()];
        }
        commonAutoComplete(e, acUser, userId, text_val, userList, "user_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            this._on_current_page = 1;
            this._sno = 0;
            this._total_record = 0;
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
            REPORT.renderPageControls();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            csv = true;
            REPORT.exportReportValues();
        }
    });

}

clearElement = function(arr) {
    if(arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onServiceProviderAutoCompleteSuccess = function(REPORT, val) {
    ServiceProvider.val(val[1]);
    ServiceProviderId.val(val[0]);
    ServiceProvider.focus();
    clearElement([users, userId]);
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    users.focus();
}

ServiceProviderDetails = function() {
    this._sp_list = [];
    this._users = [];
    this._sp_status = [];
    this._report_data = [];
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._ServiceProviderUsers = [];
}

ServiceProviderDetails.prototype.loadSearch = function() {
    reportView.hide();
    ServiceProvider.val('');
    ServiceProviderId.val('');
    users.val('');
    userId.val('');
    ServiceProviderStatus.empty();
    this.renderPageControls();
    this.fetchSearchList();
};

ServiceProviderDetails.prototype.fetchSearchList = function() {
    t_this = this;
    client_mirror.getServiceProviderDetailsReportFilters(function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._sp_list = response.sp_list;
            t_this._sp_status = response.sp_status_list;
            REPORT.renderServiceProviderStatusList(t_this._sp_status);
            t_this._users = response.sp_user_list;
        } else {
            t_this.possibleFailures(error);
        }
    });
};

ServiceProviderDetails.prototype.renderServiceProviderStatusList = function(data) {
    t_this = this;
    ServiceProviderStatus.empty();
    var spStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        spStatusList = spStatusList + '<option value="' + e.s_p_status_id + '"> ' + e.s_p_status + ' </option>';
    });
    ServiceProviderStatus.html(spStatusList);
};

ServiceProviderDetails.prototype.validate = function() {
    if (ServiceProvider) {
        if (isLengthMinMax(ServiceProvider, 0, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(ServiceProvider, message.legalentity_str) == false)
            return false;
    }
    if (users) {
        if (isLengthMinMax(users, 0, 50, message.user_max) == false)
            return false;
        else if (isCommonName(users, message.user_str) == false)
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

ServiceProviderDetails.prototype.fetchReportValues = function() {
    t_this = this;
    sp_id = ServiceProviderId.val();
    if (sp_id == "")
        sp_id = 0;
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    sp_s = $('#sp-status option:selected').text().trim();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0
    }
    else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
    }

    client_mirror.getServiceProviderDetailsReport(
        parseInt(sp_id), parseInt(user_id), sp_s, this._sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._ServiceProviderUsers = response.sp_details_list;
            if (response.sp_details_list.length == 0) {
                t_this.hidePageView();
                t_this.hidePagePan();
                //Export_btn.hide();
                PaginationView.hide();
                t_this.showReportValues();
            }
            else{
                t_this._total_record = response.sp_details_list.length;
                if (t_this._sno == 0) {
                    t_this.createPageView(t_this, t_this._total_record);
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

ServiceProviderDetails.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._ServiceProviderUsers;
    reportTableTbody.find('tr').remove();
    var spid = "";
    var is_null = true;
    showFrom = t_this._sno + 1;
    t_this._total_record = data.length;
    $.each(data, function(k, v) {
        console.log(data.length)
        is_null = false;
        //$('.client-logo').attr("src", v.logo_url);

        if (spid != v.sp_id) {
            var clonethree = $('#template #report-table .row-three').clone();
            t_this._sno += 1;
            $('.sno', clonethree).text(t_this._sno);
            $('.sp-name', clonethree).text(v.sp_name);
            $('.unit-count', clonethree).text(v.unit_count);
            $('.contact-no', clonethree).text(v.con_no);
            $('.email-id', clonethree).text(v.email_id);
            $('.address', clonethree).text(v.address);
            $('.contract-period', clonethree).text(v.contract_period);
            $('.status', clonethree).text(v.s_p_status);

            if (v.sp_status_date != "")
                $('.action-date', clonethree).text(v.sp_status_date);
            else
                $('.action-date', clonethree).text('-');
            reportTableTbody.append(clonethree);
            spid = v.sp_id;
        } else {
            var clonefour = $('#template #report-table .row-four').clone();
            $('.user-name-new', clonefour).text(v.sp_name);
            $('.contact-no-new', clonefour).text(v.con_no);
            $('.email-id-new', clonethree).text(v.email_id);
            $('.status-new', clonethree).text(v.s_p_status);

            if (v.sp_status_date != "")
                $('.action-date-new', clonethree).text(v.sp_status_date);
            else
                $('.action-date-new', clonethree).text('-');

            reportTableTbody.append(clonefour);
            spid = v.sp_id;
        }
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
        t_this.showPagePan(showFrom, t_this._sno, t_this._total_record);
    }
};

ServiceProviderDetails.prototype.possibleFailures = function(error) {
    t_this = this;
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

// Pagination Functions - begins
ServiceProviderDetails.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

ServiceProviderDetails.prototype.createPageView = function(a_obj, total_records) {
    perPage = parseInt(ItemsPerPage.val());
    a_obj.hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(a_obj._on_current_page) != cPage) {
                a_obj._on_current_page = cPage;
                a_obj.fetchReportValues();
            }
        }
    });
};
ServiceProviderDetails.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
ServiceProviderDetails.prototype.hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

ServiceProviderDetails.prototype.renderPageControls = function(e) {
    var t_this = this;
    ItemsPerPage.on('change', function(e) {
        t_this.perPage = parseInt($(this).val());
        t_this._sno = 0;
        t_this._on_current_page = 1;
        t_this.createPageView(t_this, t_this._total_record);
        t_this.fetchReportValues();
    });
    t_this._perPage = parseInt(ItemsPerPage.val());

};
// Pagination Ends

REPORT = new ServiceProviderDetails();

$(document).ready(function() {
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
});