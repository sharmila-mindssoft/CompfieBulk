//variable declaration
var totalRecord;
var allUserInfo;
var userDetails;
var clientList;
var assignedUnitList;
var mappedUserList;
var userMappingList;
var csv = false;

var UserAccessCountriesIds = [];
var DomainExecutives = [];
var UserCategoryID;

var ExistingUserId = [];

//Input field variable declaration

var ToDate = $("#to-date");
var FromDate = $("#from-date");

var Show_btn = $('#show');
var ExportButton = $('#export');


//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var compliance_count = 0;

var DeName = $('#dename-dmanager');
var on_current_page = 1;
var sno = 0;
var _page_limit = 25;


var ReportView = $('.grid-table-rpt');
var ACGroup = $('#ac-group');
var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UnitVal = $('#unitval');
var Unit = $('#unitid');

s_page = new ApproveAssignedStatutory();

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

//load all the filters
function initialize() {
    function onSuccess(data) {
      console.log("+++++++++++++++++++++++>"+data);
        clientList = data.usermapping_groupdetails;
        legelEntityList = data.usermapping_legal_entities;
        assignedUnitList = data.usermapping_unit;
        allUserInfoList();
        resetAllfilter();
        resetFields();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    bu.getClientInfo(function(error, response) {
        if (error == null) {

            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

function resetAllfilter() {
    $('#groupsval').val('');
    $('#legalentityval').val('');
    $('#unitval').val('');
    $('.tbody-usermappingdetails-list').empty();
    $('.grid-table-rpt').hide();
    $('.details').hide();
    //$('#countryval').focus();
}

function resetfilter(evt) {

    if (evt == 'clients') {

        $('#legalentityval').val('');
        $('#unitval').val('');
    }
    if (evt == 'le') {
        $('#divisionval').val('');
        $('#categoryval').val('');
        $('#unitval').val('');
    }
    $('.tbody-usermappingdetails-list').empty();
    $('.grid-table-rpt').hide();
    $('.details').hide();
}


//pagination - functions
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
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-usermappingdetails-list').append(clone4);
        //ExportButton.hide();
        PaginationView.hide();

    } else {
        if (sno == 0) {
            //ExportButton.show();
            createPageView(totalRecord);
        }
        PaginationView.show();
        //ReportView.show();

        loadUserMappingDetailsList();
    }
}

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

function resetFields() {
    $('#group-id').val('');
    $('#legalentityid').val('');
    $('#unitid').val('');
}

function loadUserMappingDetailsList() {
    var th_cnt = 3;

    var is_null = true;
    $('.tbody-usermappingdetails-list').empty();
    $('.usermapping-header').empty();
    //$('.#datatable-responsive').empty();
    domainsList = userMappingList.usermapping_domain;
    /*loadHeader();*/

    //$('#datatable-responsive th').remove();

    var tableheading = $('#templates .tr-heading');
    var cloneheading = tableheading.clone();
    $('.usermapping-header').append(cloneheading);

    if (domainsList.length > 0) {
        for (var i = 0; i < domainsList.length; i++) {
            is_null = false;
            $('.usermapping-header th:last-child').each(function() {
                for (var j = 1; j <= 2; j++) {
                    var clone = $(this).clone().html('&nbsp;');
                    if (clone.is('th')) {
                        if (j == 1) {
                            clone.text('Domain Manager ' + domainsList[i].domain_name);
                        } else {
                            clone.text('Domain User ' + domainsList[i].domain_name);
                        }
                    }
                    $(this).parent().append(clone);
                    th_cnt = th_cnt + 1;
                }
            });
        }
    }
    //load details
    technoDetails = userMappingList.techno_details;
    var assignedDomainVal = '';
    var assignedDomainVal_1 = '';
    var getDomainVal = '';
    var col = 4;
    for (var i = 0; i < technoDetails.length; i++) {
        is_null = false;
        //alert(technoDetails.length);
        assignedDomainVal = '';
        var tableRow = $('#templates .table-row');
        var clone1 = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone1).text(sno);
        //var unit_code_name = getUnitName(technoDetails[i].unit_id);
        $('.unit-name', clone1).text(technoDetails[i].unit_code_with_name);
        $('.techno-manager', clone1).text(technoDetails[i].techno_manager);
        $('.techno-user', clone1).text(technoDetails[i].techno_user);
        $('.tbody-usermappingdetails-list').append(clone1);
        for (var k = col; k <= th_cnt; k++) {
            var headerObj = $('#datatable-responsive').find('th').eq(k);
            getDomainVal = getDomainAssigned(headerObj.text(), technoDetails[i].unit_id, userMappingList);
            if (assignedDomainVal == '') {
                assignedDomainVal = getDomainVal;
            } else {
                assignedDomainVal = assignedDomainVal + "," + getDomainVal;
            }
        }
        if (assignedDomainVal_1 == '') {
            assignedDomainVal_1 = assignedDomainVal;
        } else {
            assignedDomainVal_1 = assignedDomainVal_1 + ";" + assignedDomainVal;
        }
    }
    var split_domain_with_colon = "";
    if (assignedDomainVal_1.indexOf(";") > 0)
        split_domain_with_colon = assignedDomainVal_1.split(";");
    else
        split_domain_with_colon = assignedDomainVal_1;
    var row_indx = 0;
    $('.tbody-usermappingdetails-list tr :last-child').each(function() {
        var index = $(this).closest('td').index();
        if (index > 0 && assignedDomainVal_1.indexOf(";") < 0) {
            var split_domain_with_comma = split_domain_with_colon.split(",");
            for (var k = 0; k < split_domain_with_comma.length; k++) {
                var clone2 = $(this).clone().html('&nbsp;');
                if (clone2.is('td')) {
                    clone2.text(split_domain_with_comma[k]);
                }
                $(this).parent().append(clone2);
            }
        } else {
            if (index > 0) {
                for (var m = row_indx; m < split_domain_with_colon.length; m++) {
                    var split_domain_with_comma = split_domain_with_colon[m].split(",");
                    for (var k = 0; k < split_domain_with_comma.length; k++) {
                        var clone2 = $(this).clone().html('&nbsp;');
                        if (clone2.is('td')) {
                            clone2.text(split_domain_with_comma[k]);
                        }
                        $(this).parent().append(clone2);
                    }
                    row_indx = row_indx + 1;
                    break;
                }
            }
        }
    });
    if (is_null == false)
        showPagePan(showFrom, sno, totalRecord);
}

//get statutory mapping bulk report filter details from api
function allUserInfoList() {
    function onSuccess(data) {
        allUserInfo = data.user_details;
        loadCurrentUserDetails();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

// Check If Current User Is Domain Manager Or Executives
function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var logged_user_id = 0;

    if (allUserInfo) {
        $.each(allUserInfo, function(key, value) {
            if (user.user_id == value["user_id"]) {
                UserCategoryID = value["user_category_id"];
                logged_user_id = value["user_id"];

            }
        });

        if (UserCategoryID == 8) {
            // De-Name  : Domain-Executive 
            $('.active-domain-executive').attr('style', 'display:block');
            $('.form-group-dename-dmanager').attr("style", "display:none !important");
            $('#domain-name').text(user.employee_code + " - " + user.employee_name.toUpperCase());
            ExistingUserId.push(logged_user_id);
        } else if (UserCategoryID == 7 && UserCategoryID != 8 && logged_user_id > 0) {
            // DE-Name  : Domain-Manager 
            getUserMappingsList(logged_user_id);
        }
    }

}

//get statutory mapping bulk report filter details from api
function getUserMappingsList(logged_user_id) {

    $('.form-group-dename-dmanager').attr("style", "display:block !important");
    $('#dename-dmanager').multiselect('rebuild');

    function onSuccess(logged_user_id, data) {

        var userMappingData = data;
        var d;

        $.each(userMappingData.user_mappings, function(key, value) {
            if (logged_user_id == value.parent_user_id) {
                DomainExecutives.push(value.child_user_id);
                childUsersDetails(allUserInfo, logged_user_id, value.child_user_id)
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

                    $('#dename-dmanager').append(option);
                    ExistingUserId.push(parseInt(child_user_id));
                }
            }
        });
        $('#dename-dmanager').multiselect('rebuild');
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

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if (current_id == 'group-id') {
        resetfilter('clients');
    } else if (current_id == 'businessgroupid') {
        resetfilter('bg');
    } else if (current_id == 'legalentityid') {
        resetfilter('le');
    } else if (current_id == 'unitid') {
        resetfilter('unit');
    }
}

//load group form list in autocomplete text box
$('#groupsval').keyup(function(e) {
    resetfilter('clients');
    var textval = $(this).val();
    var ctry_grps = [];
    /*if($('#country-id').val() > 0)
    {*/
    for (var i = 0; i < clientList.length; i++) {
        if (clientList[i].country_id) {
            var occur = -1
            for (var j = 0; j < ctry_grps.length; j++) {
                if (ctry_grps[j].client_id == clientList[i].client_id) {
                    occur = 1;
                    break;
                }
            }
            if (occur < 0) {
                ctry_grps.push({
                    "client_id": clientList[i].client_id,
                    "group_name": clientList[i].client_name,
                    "is_active": true
                });
            }

        }
    }
    commonAutoComplete(
        e, ACGroup, Group, textval,
        ctry_grps, "group_name", "client_id",
        function(val) {
            onAutoCompleteSuccess(GroupVal, Group, val);
        });

});


//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function(e) {
    resetfilter('le');
    var textval = $(this).val();
    var le_list = [];
    var client_id = $('#group-id').val();
    var bgrp_id = $('#businessgroupid').val();
    if ($('#group-id').val() > 0) {
        var condition_fields = [];
        var condition_values = [];
        if (Group.val() != '') {
            condition_fields.push("client_id");
            condition_values.push(Group.val());
        }
        for (var i = 0; i < clientList.length; i++) {
            var bg_check = bgrp_id > 0 ? (bgrp_id === clientList[i].business_group_id) : false;
            if ((clientList[i].client_id == client_id) &&
                (bg_check == true || bg_check == false)) {
                for (var j = 0; j < legelEntityList.length; j++) {
                    if (legelEntityList[j].legal_entity_id == clientList[i].legal_entity_id) {
                        le_list.push({
                            "client_id": clientList[i].client_id,
                            "business_group_id": legelEntityList[j].business_group_id,
                            "legal_entity_id": legelEntityList[j].legal_entity_id,
                            "legal_entity_name": legelEntityList[j].legal_entity_name
                        });
                    }
                }
            }
        }
        commonAutoComplete(
            e, ACLegalEntity, LegalEntity, textval,
            le_list, "legal_entity_name", "legal_entity_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
            }, condition_fields, condition_values);
    }

});


//load legalentity form list in autocomplete text box
$('#unitval').keyup(function(e) {
    resetfilter('unit');
    var textval = $(this).val();
    var unit_list = [];
    var client_id = $('#group-id').val();
    var le_id = $('#legalentityid').val();
    var unit_code_name;
    if (client_id > 0 && le_id > 0) {
        for (var i = 0; i < assignedUnitList.length; i++) {
            if (assignedUnitList[i].client_id == client_id && assignedUnitList[i].legal_entity_id == le_id) {
                unit_code_name = assignedUnitList[i].unit_code_name;
                unit_code = unit_code_name.split("-");
                unit_code = unit_code[0];

                unit_list.push({
                    "unit_id": unit_code,
                    "unit_name": assignedUnitList[i].unit_code_name
                });
            }
        }
        commonAutoComplete(
            e, ACUnit, Unit, textval,
            unit_list, "unit_name", "unit_id",
            function(val) {
                onAutoCompleteSuccess(UnitVal, Unit, val);
            });
    }

});

function ApproveAssignedStatutory() {}

// Fields Manadory validation 
ApproveAssignedStatutory.prototype.validateMandatory = function() {
    is_valid = true;

    if (Group.val().trim().length == 0) {
        displayMessage(message.usergroup_required);
        is_valid = false;
    } else if (LegalEntity.val().trim().length == 0) {
        displayMessage(message.legalentity_required);
        is_valid = false;
    } else if (FromDate.val().trim() == "") {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (ToDate.val().trim() == "") {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};

ApproveAssignedStatutory.prototype.pageControls = function() {

    Show_btn.click(function() {
        is_valid = s_page.validateMandatory();
        if (is_valid == true) {
            s_page._on_current_page = 1;
            s_page._total_record = 0;

            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                    $(this).removeClass();
                });

            on_current_page = 1;
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
}

// get statutory mapping report data from api
function processSubmit() {
    var clientGroup = parseInt(Group.val());
    var legalEntityID = parseInt(LegalEntity.val());
    var deIds = DeName.val();
    var unitID = "";

    var fromDate = $('#from-date').val();
    var toDate = $('#to-date').val();

    var selectedDEName = [];
    var splitValues;

    if (Unit.val()) {
        unitID = Unit.val();
    }

    /* multiple COUNTRY selection in to generate array */
    if ($('#dename-dmanager option:selected').text() == "") {
        selectedDEName = ExistingUserId; // When execute unselected the Field.
    } else {
        $.each(deIds, function(key, value) {
            selectedDEName.push(parseInt(value));
        });
    }

    displayLoader();
    _page_limit = parseInt(ItemsPerPage.val());

    if (on_current_page == 1) {
        sno = 0
    } else {
        sno = (on_current_page - 1) * _page_limit;
    }

    filterdata = {
        "bu_client_id": clientGroup,
        "bu_legal_entity_id": legalEntityID,
        "bu_unit_id": unitID,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": sno,
        "p_count": _page_limit,
        "child_ids": selectedDEName,
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
        assignStatutoryData = data.assign_statutory_data;
        totalRecord = data.total;
        hideLoader();

        if (totalRecord == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
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
            loadCountwiseResult(assignStatutoryData);
        }

    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    bu.getAssignedStatutoryBulkReportData(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    //temp_act = act;
    //}
}
//display statutory mapping details accoring to count
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
        //lastActName = country_name;
    }

    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}


$(function() {
    //list-page
    $('.grid-table-rpt').hide();
    s_page.pageControls();
    initialize();
    return false;
    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        $('#show-button').trigger("click");
    });
    loadItemsPerPage();
});