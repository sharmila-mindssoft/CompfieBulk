var clientUnitData;
var allUserInfo;
var userDetails;
var GroupName = $("#groupsval");
var GroupId = $("#group-id");
var ACGroup = $("#ac-group");
var Show_btn = $('#show');
var Export_btn = $('#export');
var fromDate = $("#from-date");
var toDate = $("#to-date");
var TeName = $('#tename-tmanager');
var ExistingUserId = [];
var CSV = false;
s_page = null;
var UserCategoryID = 0;
var TechnoExecutives = [];
var ItemsPerPage = $('#items_per_page');
var Show_btn = $('#show');
var Export_btn = $('#export');
var _page_limit = 25;
var count = 1;
//Pagination variable declaration
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportView = $('.grid-table-rpt');
var compliance_count = 0;
var ItemsPerPage = $('#items_per_page');

function pageData(on_current_page) {
    data = [];
    _page_limit = parseInt(ItemsPerPage.val());
    recordLength = (parseInt(on_current_page) * _page_limit);
    var showFrom = sno + 1;
    var is_null = true;
    for (i = sno; i < mappedUserList.length; i++) {
        is_null = false;
        data.push(mappedUserList[i]);
        if (i == (recordLength - 1)) {
            break;
        }
    }
    if (is_null == true) {
        hidePagePan();
    } else {
        if (recordLength < totalRecord)
            showPagePan(showFrom, recordLength, totalRecord);
        else
            showPagePan(showFrom, totalRecord, totalRecord);
    }
    return data;
}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
}

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');
    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                $('#show-button').trigger("click");
                processSubmit();
            }
        }
    });
};

function resetFields() {
    $('#group-id').val('');
    $('#legalentityid').val('');
    $('#unitid').val('');
}

function processPaging() {
    _page_limit = parseInt(ItemsPerPage.val());
    showFrom = sno + 1;
    if (on_current_page == 1) {
        sno = 0
    } else {
        sno = (on_current_page - 1) * _page_limit;
    }
    sno = sno;
    if (totalRecord == 0) {
        /*loadHeader();*/
        hideLoader();
        $('.tbody-usermappingdetails-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.tbl-norecords', clone4).text('No Records Found');
        $('.tbody-usermappingdetails-list').append(clone4);
        //ExportButton.hide();
        PaginationView.hide();
        ReportView.show();
        hideLoader();
    } else {
        hideLoader();
        if (sno == 0) {
            //ExportButton.show();
            createPageView(totalRecord);
        }
        PaginationView.show();
        ReportView.show();
        loadUserMappingDetailsList();
    }
}
// get statutory mapping report data from api
function processSubmit() {
    var clientGroup = parseInt(GroupId.val());
    var teIds = TeName.val();
    var unitID = "";
    var fromDate = $('#from-date').val();
    var toDate = $('#to-date').val();
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ItemsPerPage.val())) {
        _page_limit = parseInt(ItemsPerPage.val());
    }
    if (on_current_page == 1) {
        sno = 0
    } else {
        sno = (on_current_page - 1) * _page_limit;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename-tmanager option:selected').text() == "") {
        selectedTEName = ExistingUserId; // When execute unselected the Field.
    } else {
        $.each(teIds, function(key, value) {
            selectedTEName.push(parseInt(value));
        });
    }
    // if($('#tename-tmanager option:selected').text() == ""){
    //     selectedTEName = ExistingUserId;
    //     console.log("in if selectedTEName-> "+ selectedTEName);
    // }else{
    //     $('#tename-tmanager > option:selected').each(function() {
    //         console.log(this.value);
    //         selectedTEName.push(parseInt(this.value));
    //         console.log("in else selectedTEName-> "+ selectedTEName);
    //     });
    // }
    console.log("selectedTEName-> " + selectedTEName);
    displayLoader();
    filterdata = {
        "bu_client_id": clientGroup,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": sno,
        "p_count": _page_limit,
        "child_ids": selectedTEName,
        "user_category_id": UserCategoryID
    };

    function onSuccess(data) {
        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                $(this).removeClass();
                $(this).show();
            });
        sno = sno;
        clientUnitData = data.clientdata;
        totalRecord = data.total;
        hideLoader();
        if (totalRecord == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl-norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            PaginationView.hide();
            ReportView.show();
            hideLoader();
        } else {
            hideLoader();
            if (sno == 0) {
                createPageView(totalRecord);
            }
            PaginationView.show();
            ReportView.show();
            loadCountwiseResult(clientUnitData);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    bu.getClientUnitBulkReportData(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    //temp_act = act;
    //}
}

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
    Show_btn.click(function() {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            s_page._on_current_page = 1;
            s_page._total_record = 0;
            /*     s_page.fetchData();
                 s_page.renderPageControls();*/
            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                    $(this).removeClass();
                });
            on_current_page = 1;
            /*$('.country').text("Country: " + Country.val());
            $('.domain').text("Domain: " + Domain.val());*/
            processSubmit();
        }
    });
    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        createPageView(totalRecord);
        processSubmit();
    });
    Export_btn.click(function(e) {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            CSV = true;
            s_page.exportData();
        }
    });
}

function fetchFiltersData() {
    displayLoader();
    mirror.getClientLoginTraceFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
                loadCurrentUserDetails();
                hideLoader();
            }
        }
    );
}

function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var logged_user_id = 0;
    $.each(allUserInfo, function(key, value) {
        if (user.user_id == value["user_id"]) {
            UserCategoryID = value["user_category_id"];
            logged_user_id = value["user_id"];
            console.log(UserCategoryID);
        }
    });
    if (UserCategoryID == 6) {
        // TE-Name  : Techno-Executive 
        $('.active-techno-executive').attr('style', 'display:block');
        $('#techno-name').text(user.employee_code + " - " + user.employee_name.toUpperCase());
        ExistingUserId.push(logged_user_id);
    } else if (UserCategoryID == 5 && UserCategoryID != 6 && logged_user_id > 0) {
        // TE-Name  : Techno-Manager 
        getUserMappingsList(logged_user_id);
    }
}
//get client unit bulk upload report filter details from api
function getUserMappingsList(logged_user_id) {
    $('.form-group-tename-tmanager').attr("style", "display:block !important");
    $('#tename-tmanager').multiselect('rebuild');

    function onSuccess(logged_user_id, data) {
        console.log("logged_user_id->" + logged_user_id);
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value) {
            if (logged_user_id == value.parent_user_id) {
                console.log("value.child_user_id-> " + value.child_user_id);
                console.log("inaary-> " + jQuery.inArray(value.child_user_id, TechnoExecutives));
                if (jQuery.inArray(value.child_user_id, TechnoExecutives) == -1) {
                    console.log("inif");
                    TechnoExecutives.push(value.child_user_id);
                    childUsersDetails(allUserInfo, logged_user_id, value.child_user_id)
                }
            }
        });
    }

    function childUsersDetails(allUserInfo, parent_user_id, child_user_id) {
        $.each(allUserInfo, function(key, value) {
            if ($.inArray(parseInt(child_user_id), ExistingUserId) == -1) {
                if (child_user_id == value["user_id"] &&
                    value["is_active"] == true) {
                    var option = $('<option></option>');
                    option.val(value["user_id"]);
                    option.text(value["employee_code"] + " - " + value["employee_name"]);
                    console.log(option)
                    $('#tename-tmanager').append(option);
                    ExistingUserId.push(parseInt(child_user_id));
                }
            }
        });
        $('#tename-tmanager').multiselect('rebuild');
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getUserMappings(function(error, response) {
        if (error == null) {
            onSuccess(logged_user_id, response);
        } else {
            onFailure(error);
        }
    });
}
//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    console.log(id_element)
    var current_id = id_element[0].id;
    // if (current_id == "group-id") {
    //     clearElement([users, userId]);
    // }
}
//get client unit bulk report filter details from api
function getClientUnits() {
    function onSuccess(data) {
        allUserInfo = data.user_details;
        userDetails = data.user_details[0];
        loadCurrentUserDetails();
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function Client_unit_bulk_report_page() {}
// Fields Manadory validation 
Client_unit_bulk_report_page.prototype.validateMandatory = function() {
    is_valid = true;
    if (GroupId.val().trim() == '' || GroupId.val().trim() == null) {
        displayMessage(message.group_required);
        is_valid = false;
    } else if (this.getValue("from-date") == "") {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (this.getValue("to-date") == "") {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};
// To get the corresponding value
Client_unit_bulk_report_page.prototype.getValue = function(field_name, f_id) {
    if (field_name == "from-date") {
        f_date = fromDate.val().trim();
        return f_date;
    } else if (field_name == "to-date") {
        f_date = toDate.val().trim();
        return f_date;
    }
};
//display client unit bulk upload details according to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = sno + 1;
    var is_null = true;
    for (var entity in filterList) {
        is_null = false;
        sno = parseInt(sno) + 1;
        var csv_name = filterList[entity].csv_name;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var uploaded_by = filterList[entity].uploaded_by;
        var uploaded_on = filterList[entity].uploaded_on;
        var total_rejected_records = filterList[entity].total_rejected_records;
        var rejected_on = filterList[entity].rejected_on;
        var rejected_by = filterList[entity].rejected_by;
        var reason_for_rejection = filterList[entity].is_fully_rejected;
        var approve_status = filterList[entity].approve_status;
        $(allUserInfo).each(function(key, value) {
            if (parseInt(uploaded_by) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                uploaded_by = EmpCode + " - " + EmpName.toUpperCase();
            } else if (parseInt(rejected_by) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                rejected_by = EmpCode + " - " + EmpName.toUpperCase();
            }
        });
        if (parseInt(reason_for_rejection) == 1) {
            reason_for_rejection = "Fully Rejected";
        } else {
            reason_for_rejection = "- -";
        }
        var occurance = '';
        var occuranceid;
        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();
        $('.tbl_sno', clone1).text(sno);
        $('.tbl_uploaded_file_name', clone1).text(csv_name);
        $(".tbl_uploaded_by", clone1).text(uploaded_by);
        $('.tbl_uploaded_on', clone1).text(uploaded_on);
        $('.tbl_no_of_tasks', clone1).text(tbl_no_of_tasks);
        $('.tbl_approved_rejected_tasks', clone1).text(approve_status + " / " + total_rejected_records);
        $('.tbl_approved_rejected_on', clone1).text(rejected_on);
        $('.tbl_approved_rejected_by', clone1).text(rejected_by);
        $('.tbl_reason_for_rejection', clone1).text(reason_for_rejection);
        $('#datatable-responsive .tbody-compliance').append(clone1);
        compliance_count = compliance_count + 1;
        // lastActName = country_name;
    }
    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}
//To export data
Client_unit_bulk_report_page.prototype.exportData = function() {
    var clientGroup = parseInt(GroupId.val());
    var clientGroupName = GroupName.val();
    var teIds = TeName.val();
    var unitID = "";
    var fromDate = $('#from-date').val();
    var toDate = $('#to-date').val();
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ItemsPerPage.val())) {
        _page_limit = parseInt(ItemsPerPage.val());
    }
    if (on_current_page == 1) {
        sno = 0
    } else {
        sno = (on_current_page - 1) * _page_limit;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename-tmanager option:selected').text() == "") {
        selectedTEName = ExistingUserId; // When execute unselected the Field.
    } else {
        $.each(teIds, function(key, value) {
            selectedTEName.push(parseInt(value));
        });
    }
    filterdata = {
        "bu_client_id": clientGroup,
        "bu_group_name": clientGroupName,
        "from_date": fromDate,
        "to_date": toDate,
        "child_ids": selectedTEName,
        "user_category_id": UserCategoryID,
        "csv": CSV
    };
    displayLoader();
    bu.exportCUBulkReportData(filterdata,
        function(error, response) {
            if (error == null) {
                hideLoader();
                if (CSV) {
                    var download_url = response.link;
                    $(location).attr('href', download_url);
                }
            } else {
                hideLoader();
                if (error == "ExportToCSVEmpty") {
                    displayMessage(message.empty_export);
                } else {
                    displayMessage(error);
                }
            }
        });
};
// Instance Creation of the page class
s_page = new Client_unit_bulk_report_page();
// Form Initalize
$(function() {
    //resetFields();
    loadItemsPerPage();
    getClientUnits();
    PageControls();
    fetchFiltersData();
});