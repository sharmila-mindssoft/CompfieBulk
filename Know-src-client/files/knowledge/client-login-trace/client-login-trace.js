var GroupName = $("#groupsval");
var GroupId = $("#group-id");
var ACGroup = $("#ac-group");

var users = $("#user");
var userId = $("#userid");
var acUser = $("#ac-user");

var fromDate = $("#from-date");
var toDate = $("#to-date");

var showButton = $("#show");
var exportButton = $("#export");

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
    GroupName.keyup(function(e) {
        var textval = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, textval,
            _clients, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            });

    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var newUserList = [];
        for (var i = 0; i < _clientUsers.length; i++) {
            var occur = -1;
            for (var j = 0; j < newUserList.length; j++) {
                if (newUserList[j].user_id == _clientUsers[i].user_id) {
                    occur = 1;
                }
            }
            if (occur < 0) {
                newUserList.push({
                    "user_id": _clientUsers[i].user_id,
                    "employee_name": _clientUsers[i].employee_name
                });
            }
        }
        commonAutoComplete(
            e, acUser, userId, text_val,
            newUserList, "employee_name", "user_id",
            function(val) {
                onAutoCompleteSuccess(users, userId, val);
            });
    });

    showButton.click(function() {
        if (validateMandatory()) {
            csv = false;
            _on_current_page = 1;
            _sno = 0;
            _total_record = 0;
            fetchData();
        }
    });

    exportButton.click(function() {
        if (validateMandatory()) {
            csv = true;
            exportData();
        }
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        _on_current_page = 1;
        _sno = 0;
        createPageView(_total_record);
        csv = false;
        fetchData();
    });
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    console.log(id_element)
    var current_id = id_element[0].id;
    if (current_id == "group-id") {
        clearElement([users, userId]);
    }
}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

function fetchFiltersData() {
    mirror.getClientLoginTraceFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                this.displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
            }
        }
    );
}


// Resets the filter fields
function resetFields() {
    $('.tbody-audittrail-list').find('tr').remove();
    $('.grid-table').hide();
    _sno = 0;
    users.val('');
    userId.val('');
    GroupName.val('');
    GroupId.val('');
    fromDate.val('');
    toDate.val('');
    _sno = 0;
    _clientUsers = {};
    _auditData = {};
    _clients = {};
    _on_current_page = 1;
    _total_record = 0;
    _csv = false;
    GroupName.focus();
}

function validateMandatory() {
    is_valid = true;
    if (GroupId.val().trim() == '' || GroupId.val().trim() == null) {
        displayMessage(message.group_required);
        is_valid = false;
    } else if (fromDate.val().trim() == '' || fromDate.val().trim() == null) {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (toDate.val().trim() == '' || toDate.val().trim() == null) {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};

// To get the audit log data from DB - by passing user type, user name, form name and dates, country
function fetchData() {
    _from_date = fromDate.val().trim();
    _to_date = toDate.val().trim();
    _user_id = userId.val().trim();
    _client_id = GroupId.val().trim();

    _page_limit = parseInt(ItemsPerPage.val());
    if (_on_current_page == 1) {
        _sno = 0
    } else {
        _sno = (_on_current_page - 1) * _page_limit;
    }
    displayLoader();
    console.log(_from_date, _to_date, _user_id, _client_id)
    mirror.getClientLoginTrace(
        _from_date, _to_date, parseInt(_user_id), parseInt(_client_id), _sno, _page_limit,
        function(error, response) {
        	console.log(error, response)
            if (error != null) {
                hideLoader();
                if (error == "DatabaseConnectionFailure")
                    displayMessage(message.db_connect_failed);
                else
                    displayMessage(error)
            } else {
                hideLoader();
                _sno = _sno;
                _auditData = response.client_audit_trail_details;
                if (response.client_audit_trail_details.length == 0) {
                    hidePageView();
                    hidePagePan();
                    //Export_btn.hide();
                    PaginationView.hide();
                    renderAuditData(_auditData);

                } else {
                    if (_sno == 0) {
                    	_total_record = response.total_records;
                        createPageView(_total_record);
                    }
                    //Export_btn.show();
                    PaginationView.show();
                    renderAuditData(_auditData);
                }
            }
        }
    );
};

// To get the audit log data from DB - by passing user type, user name, form name and dates, country
function exportData() {
    _from_date = fromDate.val().trim();
    _to_date = toDate.val().trim();
    _user_id = userId.val().trim();
    _client_id = GroupId.val().trim();

    displayLoader();
    console.log(_from_date, _to_date, _user_id, _client_id)
    mirror.getExportClientLoginTrace(
        _from_date, _to_date, parseInt(_user_id), parseInt(_client_id), true,
        function(error, response) {
            hideLoader();
            if (error == null) {
                hideLoader();
                if (csv) {
                    var download_url = response.link;
                    $(location).attr('href', download_url);
                }
            }
            else {
                hideLoader();
                if (error == "ExportToCSVEmpty") {
                    displayMessage(message.empty_export);
                }else {
                    displayMessage(error);
                }
            }
        }
    );
};

// Binds the data from DB
function renderAuditData(audit_data) {
    $('.details').show();
    $('#compliance_animation')
        .removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
    $('.grid-table').show();
    $('.tbody-audittrail-list').find('tr').remove();
    showFrom = _sno + 1;
    var is_null = true;
    $('.grp-header').text(GroupName.val().trim());
    $('.from-header').text(fromDate.val());
    $('.to-header').text(toDate.val());
    $.each(audit_data, function(k, v) {
        if (typeof v.action != 'undefined') {
            is_null = false;
            _sno += 1;
            var tableRow = $('#templates .table-audittrail-list .client-tableRow');
            var rowClone = tableRow.clone();

            f_name = 'Login';
            if (v.action.indexOf('Login') >= 0) {
                f_name = 'Login';
            }
            else if (v.action.indexOf('Logout') >= 0) {
                f_name = 'Logout';
            }

            $('.snumber', rowClone).text(parseInt(_sno));
            $('.username', rowClone).text(v.user_name);
            $('.usertype', rowClone).text(v.user_category_name);
            //$('.usertype', rowClone).text("categoryName");
            $('.formname', rowClone).text(f_name);
            $('.action', rowClone).text(v.action);
            $('.datetime', rowClone).text(v.created_on);
            $('.tbody-audittrail-list').append(rowClone);
        }
    });

    if (is_null == true) {
        //a_page.hidePagePan();
        $('.tbody-audittrail-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-audittrail-list').append(clone4);
    } else {
        showPagePan(showFrom, _sno, _total_record);
    }
    hideLoader();
};

function getValue(f_id) {
	frm_name = null;
    $.each(_clientForms, function(k, v) {
        if (v.form_id == f_id) {
            frm_name = v.form_name;
            return frm_name;
        }
    });
    return frm_name;
}

// Pagination Functions - begins
function hidePageView() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
}

function createPageView(total_records) {
	alert(total_records)
    perPage = parseInt(ItemsPerPage.val());
    hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(_on_current_page) != cPage) {
                _on_current_page = cPage;
                fetchData();
            }
        }
    });
}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
}

function hidePagePan() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

// Form Initalize
$(function() {
    resetFields();
    loadItemsPerPage();
    PageControls();
    fetchFiltersData();
});