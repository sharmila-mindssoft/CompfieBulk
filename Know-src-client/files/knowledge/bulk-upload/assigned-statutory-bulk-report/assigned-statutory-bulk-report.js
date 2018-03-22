//variable declaration
var TOTAL_RECORD;
var ALL_USER_INFO;
var CLIENT_LIST = [];
var LEGEL_ENTITY_LIST = [];
var ASSIGNED_UNIT_LIST = [];
var MAPPED_USER_LIST = [];
var USER_MAPPING_LIST = [];
var CSV = false;
var DOMAIN_EXECUTIVES = [];
var USER_CATEGORY_ID;
var EXISTING_USER_ID = [];

//Input field variable declaration
var TO_DATE = $("#to_date");
var FROM_DATE = $("#from_date");
var SHOW_BTN = $('#show');
var EXPORT_BTN = $('#export');

//PAGINATION variable declaration
var ITEMS_PER_PAGE = $('#items_per_page');
var PAGINATION_VIEW = $('.pagination-view');
var PAGINATION = $('#pagination-rpt');
var ASS_STAT_COUNT = $('.assigned-statu-count');

var DE_NAME = $('#de_name');
var ON_CURRENT_PAGE = 1;
var SNO = 0;
var PAGE_LIMIT = 25;
var REPORT_VIEW = $('.grid-table-rpt');
var AC_GROUP = $('#ac-group');
var AC_LEGAL_ENTITY = $('#ac-legalentity');
var AC_UNIT = $('#ac-unit');
var GROUP_VAL = $('#groupsval');
var GROUP = $('#group_id');
var LEGAL_ENTITY_VAL = $('#legalentityval');
var LEGAL_ENTITY = $('#legalentityid');
var UNIT_VAL = $('#unitval');
var UNIT = $('#unitid');
var DOMAIN = $('#domain');

function AssignStatutoryBulkReport() {}

var asBulkReport = new AssignStatutoryBulkReport();

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

//load all the filters
function initialize() {
    function onSuccess(data) {
        DomainList = data.domains;
        allUserInfoList();
        resetAllFilter();
        resetFields();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

//load all the filters
function UserGroupDetails() {
    function onSuccess(data) {
        CLIENT_LIST = data.usermapping_groupdetails;
        LEGEL_ENTITY_LIST = data.usermapping_legal_entities;
        ASSIGNED_UNIT_LIST = data.statutory_unit;
        resetAllFilter();
        resetFields();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getUserMappingStatutoryFilters(function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

function resetAllFilter() {
    GROUP_VAL.val('');
    LEGAL_ENTITY_VAL.val('');
    UNIT_VAL.val('');
    $('.tbody-usermappingdetails-list').empty();
    REPORT_VIEW.hide();
    $('.details').hide();
}

function resetFilter(evt) {
    if (evt == 'clients') {
        LEGAL_ENTITY_VAL.val('');
        LEGAL_ENTITY.val('');

        DOMAIN.empty();
        DOMAIN.html();
        DOMAIN.multiselect('rebuild');

        UNIT_VAL.val('');
        UNIT.val('');

        FROM_DATE.val('');
        TO_DATE.val('');

        DE_NAME.multiselect("deselectAll", false);
        DE_NAME.multiselect('refresh');
    }
    if (evt == 'le') {
        DOMAIN.empty();
        DOMAIN.html();
        DOMAIN.multiselect('rebuild');

        UNIT_VAL.val('');
        UNIT_VAL.val('');

        FROM_DATE.val('');
        TO_DATE.val('');

        DE_NAME.multiselect("deselectAll", false);
        DE_NAME.multiselect('refresh');

    }
    if (evt == 'domains') {
        UNIT_VAL.val('');
        UNIT_VAL.val('');

        FROM_DATE.val('');
        TO_DATE.val('');
    }

    $('.tbody-usermappingdetails-list').empty();
    REPORT_VIEW.hide();
    $('.details').hide();
}

//Pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom  ;
    showText +=  ' to ' + showTo + ' of ' + total + ' entries ';
    ASS_STAT_COUNT.text(showText);
    PAGINATION_VIEW.show();
}

function hidePagePan() {
    ASS_STAT_COUNT.text('');
    PAGINATION_VIEW.hide();
}

function createPageView(totalRecords) {
    perPage = parseInt(ITEMS_PER_PAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');
    PAGINATION.twbsPAGINATION({
        totalPages: Math.ceil(totalRecords / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(ON_CURRENT_PAGE) != cPage) {
                ON_CURRENT_PAGE = cPage;
                $('#show-button').trigger("click");
                processSubmit();
            }
        }
    });
};

function processPaging() {
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    showFrom = SNO + 1;
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * PAGE_LIMIT;
    }
    SNO = SNO;
    if (TOTAL_RECORD == 0) {
        /*loadHeader();*/
        hideLoader();
        $('.tbody-usermappingdetails-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content '+
                          '.table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-usermappingdetails-list').append(clone4);
        //ExportButton.hide();
        PAGINATION_VIEW.hide();

    } else {
        if (SNO == 0) {
            //ExportButton.show();
            createPageView(TOTAL_RECORD);
        }
        PAGINATION_VIEW.show();
        //REPORT_VIEW.show();

        loadUserMappingDetailsList();
    }
}

function pageData(onCurrentPage) {
    var data = [];
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    var recordLength = (parseInt(onCurrentPage) * PAGE_LIMIT);
    var showFrom = SNO + 1;
    var isNull = true;
    var i;
    for (i = SNO; i < MAPPED_USER_LIST.length; i++) {
        isNull = false;
        data.push(MAPPED_USER_LIST[i]);
        if (i == (recordLength - 1)) {
            break;
        }
    }
    if (isNull == true) {
        hidePagePan();
    } else {
        if (recordLength < TOTAL_RECORD)
            showPagePan(showFrom, recordLength, TOTAL_RECORD);
        else
            showPagePan(showFrom, TOTAL_RECORD, TOTAL_RECORD);
    }
    return data;
}

function resetFields() {
    GROUP.val('');
    LEGAL_ENTITY.val('');
    UNIT.val('');
}

function loadUserMappingDetailsList() {
    var thCnt = 3;

    var isNull = true;
    $('.tbody-usermappingdetails-list').empty();
    $('.usermapping-header').empty();
    //$('.#datatable-responsive').empty();
    var domainsList = USER_MAPPING_LIST.usermapping_domain;
    /*loadHeader();*/

    //$('#datatable-responsive th').remove();

    var tableheading = $('#templates .tr-heading');
    var cloneheading = tableheading.clone();
    $('.usermapping-header').append(cloneheading);

    if (domainsList.length > 0) {
        var i = 0;
        for (i = 0; i < domainsList.length; i++) {
            isNull = false;
            var domName = domainsList[i].domain_name;
            console.log("Dom name- >>> " + domName);
            $('.usermapping-header th:last-child').each(function() {
                for (var j = 1; j <= 2; j++) {
                    var clone = $(this).clone().html('&nbsp;');
                    if (clone.is('th')) {
                        if (j == 1) {
                            clone.text('Domain Manager ' + domName);
                        } else {
                            clone.text('Domain User ' + domName);
                        }
                    }
                    $(this).parent().append(clone);
                    thCnt = thCnt + 1;
                }
            });
        }
    }
    //load details
    var technoDetails = USER_MAPPING_LIST.techno_details;
    var assignedDomVal = '';
    var assignedDomVal1 = '';
    var getDomainVal = '';
    var col = 4;
    for (var i = 0; i < technoDetails.length; i++) {
        isNull = false;
        //alert(technoDetails.length);
        assignedDomVal = '';
        var tableRow = $('#templates .table-row');
        var clone1 = tableRow.clone();
        SNO = SNO + 1;
        $('.SNO', clone1).text(SNO);
        //var unit_code_name = getUnitName(technoDetails[i].unit_id);
        $('.unit-name', clone1).text(technoDetails[i].unit_code_with_name);
        $('.techno-manager', clone1).text(technoDetails[i].techno_manager);
        $('.techno-user', clone1).text(technoDetails[i].techno_user);
        $('.tbody-usermappingdetails-list').append(clone1);
        for (var k = col; k <= thCnt; k++) {
            var headerObj = $('#datatable-responsive').find('th').eq(k);
            getDomainVal = getDomainAssigned(headerObj.text(), 
                            technoDetails[i].unit_id, USER_MAPPING_LIST);
            if (assignedDomVal == '') {
                assignedDomVal = getDomainVal;
            } else {
                assignedDomVal = assignedDomVal + "," + getDomainVal;
            }
        }
        if (assignedDomVal1 == '') {
            assignedDomVal1 = assignedDomVal;
        } else {
            assignedDomVal1 = assignedDomVal1 + ";" + assignedDomVal;
        }
    }
    var splitDomainWithColon = "";
    if (assignedDomVal1.indexOf(";") > 0)
        splitDomainWithColon = assignedDomVal1.split(";");
    else
        splitDomainWithColon = assignedDomVal1;
    var rowIndx = 0;
    $('.tbody-usermappingdetails-list tr :last-child').each(function() {
        var index = $(this).closest('td').index();
        if (index > 0 && assignedDomVal1.indexOf(";") < 0) {
            var splitDomainWithComma = splitDomainWithColon.split(",");
            for (var k = 0; k < splitDomainWithComma.length; k++) {
                var clone2 = $(this).clone().html('&nbsp;');
                if (clone2.is('td')) {
                    clone2.text(splitDomainWithComma[k]);
                }
                $(this).parent().append(clone2);
            }
        } else {
            if (index > 0) {
                for (var m = rowIndx; m < splitDomainWithColon.length; m++) {
                    var splitDomainWithComma = splitDomainWithColon[m].split(",");
                    for (var k = 0; k < splitDomainWithComma.length; k++) {
                        var clone2 = $(this).clone().html('&nbsp;');
                        if (clone2.is('td')) {
                            clone2.text(splitDomainWithComma[k]);
                        }
                        $(this).parent().append(clone2);
                    }
                    rowIndx = rowIndx + 1;
                    break;
                }
            }
        }
    });
    if (isNull == false)
        showPagePan(showFrom, SNO, TOTAL_RECORD);
}


//get statutory mapping bulk report filter details from api
function allUserInfoList() {
    function onSuccess(data) {
        ALL_USER_INFO = data.user_details;
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
    var loggedUserID = 0;

    if (ALL_USER_INFO) {
        $.each(ALL_USER_INFO, function(key, value) {
            if (user.user_id == value["user_id"]) {
                USER_CATEGORY_ID = value["user_category_id"];
                loggedUserID = value["user_id"];
            }
        });

        if (USER_CATEGORY_ID == 8) {
            // De-Name  : Domain-Executive
            $('.active-domain-executive').attr('style', 'display:block');
            $('.form-group-dename-dmanager')
                    .attr("style", "display:none !important");
            $('#domain-name')
                .text(
                user.employee_code + " - " + user.employee_name.toUpperCase());
            EXISTING_USER_ID.push(loggedUserID);
        } else if (USER_CATEGORY_ID == 7 && USER_CATEGORY_ID != 8
                                                    && loggedUserID > 0) {
            // DE-Name  : Domain-Manager
            getUserMappingsList(loggedUserID);
        }
    }

}

//get statutory mapping bulk report filter details from api
function getUserMappingsList(loggedUserID) {
    $('.form-group-dename-dmanager').attr("style", "display:block !important");
    $('#de_name').multiselect('rebuild');

    function onSuccess(loggedUserID, data) {
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value) {
            if (loggedUserID == value.parent_user_id) {
                DOMAIN_EXECUTIVES.push(value.child_user_id);
                childUsersDetails(ALL_USER_INFO, loggedUserID,
                                            value.child_user_id)
            }
        });
    }

    function childUsersDetails(ALL_USER_INFO, parent_user_id, child_user_id) {
        $.each(ALL_USER_INFO, function(key, value) {
            if ($.inArray(parseInt(child_user_id), EXISTING_USER_ID) == -1) {
                if (child_user_id == value["user_id"] &&
                    value["is_active"] == true) {
                    var option = $('<option></option>');
                    option.val(value["user_id"]);
                    option.text(value["employee_code"] + " - " +
                                value["employee_name"]);

                    $('#de_name').append(option);
                    EXISTING_USER_ID.push(parseInt(child_user_id));
                }
            }
        });
        $('#de_name').multiselect('rebuild');
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }

    mirror.getUserMappings(function(error, response) {
        if (error == null) {

            onSuccess(loggedUserID, response);
        } else {
            onFailure(error);
        }
    });
}

function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    var currentID = idElement[0].id;
    if (currentID == 'group_id') {
        resetFilter('clients');
    } else if (currentID == 'businessgroupid') {
        resetFilter('bg');
    } else if (currentID == 'legalentityid') {
        resetFilter('le');
    } else if (currentID == 'unitid') {
        resetFilter('unit');
    }
}

//Load group form list in autocomplete text box
GROUP_VAL.keyup(function(e) {
    resetFilter('clients');
    var textVal = $(this).val();
    var ctryGrps = [];
    /*if($('#country-id').val() > 0)
    {*/
    for (var i = 0; i < CLIENT_LIST.length; i++) {
        if (CLIENT_LIST[i].country_id) {
            var occur = -1
            for (var j = 0; j < ctryGrps.length; j++) {
                if (ctryGrps[j].client_id == CLIENT_LIST[i].client_id) {
                    occur = 1;
                    break;
                }
            }
            if (occur < 0) {
                ctryGrps.push({
                    "client_id": CLIENT_LIST[i].client_id,
                    "group_name": CLIENT_LIST[i].client_name,
                    "is_active": true
                });
            }
        }
    }
    commonAutoComplete(
        e, AC_GROUP, GROUP, textVal,
        ctryGrps, "group_name", "client_id",
        function(val) {
            onAutoCompleteSuccess(GROUP_VAL, GROUP, val);
        });

});

//load legalentity form list in autocomplete text box
LEGAL_ENTITY_VAL.keyup(function(e) {
    resetFilter('le');
    var textVal = $(this).val();
    var leList = [];
    var clientId = GROUP.val();
    var bgrpID = $('#businessgroupid').val();
    if (GROUP.val() > 0) {
        var conditionFields = [];
        var conditionValues = [];
        if (GROUP.val() != '') {
            conditionFields.push("client_id");
            conditionValues.push(GROUP.val());
        }
        for (var i = 0; i < CLIENT_LIST.length; i++) {
            var bgCheck = bgrpID > 0 ? 
                        (bgrpID === CLIENT_LIST[i].business_group_id) : false;
            if ((CLIENT_LIST[i].client_id == clientId) &&
                (bgCheck == true || bgCheck == false)) {
                for (var j = 0; j < LEGEL_ENTITY_LIST.length; j++) {
                    if (LEGEL_ENTITY_LIST[j].legal_entity_id == 
                                        CLIENT_LIST[i].legal_entity_id) {
                        leList.push({
                            "client_id": CLIENT_LIST[i].client_id,
                            "business_group_id": LEGEL_ENTITY_LIST[j]
                                                        .business_group_id,
                            "legal_entity_id": LEGEL_ENTITY_LIST[j]
                                                        .legal_entity_id,
                            "legal_entity_name": LEGEL_ENTITY_LIST[j]
                                                        .legal_entity_name
                        });
                    }
                }
            }
        }
        commonAutoComplete(
            e, AC_LEGAL_ENTITY, LEGAL_ENTITY, textVal,
            leList, "legal_entity_name", "legal_entity_id",
            function(val) {
                onAutoCompleteSuccess(LEGAL_ENTITY_VAL, LEGAL_ENTITY, val);
                loadDomains();
            }, conditionFields, conditionValues);
    }

});

DOMAIN.on('change', function(e) {
    resetFilter('domains');
});

//load legalentity form list in autocomplete text box
UNIT_VAL.keyup(function(e) {
    resetFilter('unit');
    var textVal = $(this).val();
    var unitList = [];
    var clientId = GROUP.val();
    var leID = LEGAL_ENTITY.val();
    var domain_ids = DOMAIN.val();
    var unit_code_name;

    var selectedDomain = [];
    $.each(domain_ids, function(key, value) {
        selectedDomain.push(parseInt(value));
    });

    if (clientId > 0 && leID > 0) {
        for (var i = 0; i < ASSIGNED_UNIT_LIST.length; i++) {
            if (ASSIGNED_UNIT_LIST[i].client_id == clientId &&
                ASSIGNED_UNIT_LIST[i].legal_entity_id == leID &&
                $.inArray(ASSIGNED_UNIT_LIST[i].d_id, selectedDomain) >= 0) {
                unit_code_name = ASSIGNED_UNIT_LIST[i].unit_code_name;
                unit_code = unit_code_name.split("-");
                unit_code = unit_code[0];

                unitList.push({
                    "unit_id": unit_code,
                    "unit_name": ASSIGNED_UNIT_LIST[i].unit_code_name
                });
            }
        }
        commonAutoComplete(
            e, AC_UNIT, UNIT, textVal,
            unitList, "unit_name", "unit_id",
            function(val) {
                onAutoCompleteSuccess(UNIT_VAL, UNIT, val);
            });
    }

});

// Fields Manadory validation
AssignStatutoryBulkReport.prototype.validateMandatory = function() {
    is_valid = true;

    if (GROUP.val().trim().length == 0) {
        displayMessage(message.clientgroup_required);
        is_valid = false;
    } else if (LEGAL_ENTITY.val().trim().length == 0) {
        displayMessage(message.legalentity_required);
        is_valid = false;
    } else if ($('#domain option:selected').text() == "") {
        displayMessage(message.domain_required);
        is_valid = false;
    } else if (FROM_DATE.val().trim() == "") {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (TO_DATE.val().trim() == "") {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};

AssignStatutoryBulkReport.prototype.pageControls = function() {

    SHOW_BTN.click(function() {
        is_valid = asBulkReport.validateMandatory();
        if (is_valid == true) {
            asBulkReport._ON_CURRENT_PAGE = 1;
            asBulkReport._total_record = 0;

            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                    $(this).removeClass();
                });

            ON_CURRENT_PAGE = 1;
            processSubmit();
        }
    });

    ITEMS_PER_PAGE.on('change', function(e) {
        perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        createPageView(TOTAL_RECORD);
        processSubmit();
    });

    EXPORT_BTN.click(function(e) {
        is_valid = asBulkReport.validateMandatory();
        if (is_valid == true) {
            CSV = true;
            asBulkReport.exportData();
        }
    });

}

function loadDomains() {

    /******** Load Domain Lists *********/

    var clientId = GROUP.val();
    var legal_id = LEGAL_ENTITY.val();
    var APIClientID;
    var APILegalEntityID;
    var countriesList = [];


    $.each(CLIENT_LIST, function(key, value) {
        APIClientID = parseInt(value["client_id"]);
        APILegalEntityID = parseInt(value["legal_entity_id"]);

        if (clientId == APIClientID && legal_id == APILegalEntityID) {
            countriesList.push(parseInt(value["country_id"]));

        }
    });
    getDomainByCountryID(countriesList);
}

function getDomainByCountryID(countriesList) {
    var sText = '';
    var str = '';
    $.each(countriesList, function(key, countryId) {
        var cId = countryId;
        var flag = true;

        $.each(DomainList, function(key1, v) {
            if (v.is_active == false) {
                return;
            }
            if ($.inArray(cId, v.country_ids) >= 0) {
                var dVal = v.domain_id;
                str += '<option value="' + dVal + '" ' + sText + '>' + v.domain_name + '</option>';
                flag = false;
            }
        });

    });
    $('#domain').append(str);
    $('#domain').multiselect('rebuild');
}
// get statutory mapping report data from api
function processSubmit() {
    var clientGroup = parseInt(GROUP.val());
    var legalEntityID = parseInt(LEGAL_ENTITY.val());
    var deIds = DE_NAME.val();
    var domain_ids = DOMAIN.val();
    var unitID = "";

    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();

    var selectedDEName = [];
    var splitValues;

    var selectedDomain = [];
    $.each(domain_ids, function(key, value) {
        selectedDomain.push(parseInt(value));
    });

    if (UNIT.val()) {
        unitID = UNIT.val();
    }


    /* multiple COUNTRY selection in to generate array */
    if ($('#de_name option:selected').text() == "") {
        selectedDEName = EXISTING_USER_ID; // When execute unselected the Field.
    } else {
        $.each(deIds, function(key, value) {
            selectedDEName.push(parseInt(value));
        });
    }

    displayLoader();
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());

    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * PAGE_LIMIT;
    }

    filterdata = {
        "bu_client_id": clientGroup,
        "bu_legal_entity_id": legalEntityID,
        "bu_unit_id": unitID,
        "domain_ids": selectedDomain,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": SNO,
        "p_count": PAGE_LIMIT,
        "child_ids": selectedDEName,
        "user_category_id": USER_CATEGORY_ID
    };

    function onSuccess(data) {

        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                $(this).removeClass();
                $(this).show();
            });


        SNO = SNO;
        assignStatutoryData = data.assign_statutory_data;
        TOTAL_RECORD = data.total;
        hideLoader();

        if (TOTAL_RECORD == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl_norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            PAGINATION_VIEW.hide();
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            if (SNO == 0) {
                createPageView(TOTAL_RECORD);
            }
            PAGINATION_VIEW.show();
            REPORT_VIEW.show();
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
    var showFrom = SNO + 1;
    var isNull = true;

    for (var entity in filterList) {

        isNull = false;
        SNO = parseInt(SNO) + 1;

        var domain = filterList[entity].domain;
        var csv_name = filterList[entity].csv_name;
        var tbl_no_of_tasks = filterList[entity].total_records;
        var uploaded_by = filterList[entity].uploaded_by;
        var uploaded_on = filterList[entity].uploaded_on;
        var total_rejected_records = filterList[entity].total_rejected_records;
        var rejected_on = filterList[entity].rejected_on;
        var rejected_by = filterList[entity].rejected_by;
        var reason_for_rejection = filterList[entity].is_fully_rejected;
        var total_approve_records = filterList[entity].total_approve_records;
        var rejected_reason = filterList[entity].rejected_reason;
        var domain_name = filterList[entity].domain_name;
        var approved_on = filterList[entity].approved_on;
        var approved_by = filterList[entity].approved_by;
        approved_rejected_on = '';
        approved_rejected_by = '';
        approved_rejected_tasks = '-';



        $(ALL_USER_INFO).each(function(key, value) {
            if (parseInt(uploaded_by) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                uploaded_by = EmpCode + " - " + EmpName.toUpperCase();
            } else if (parseInt(rejected_by) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                rejected_by = EmpCode + " - " + EmpName.toUpperCase();
            } else if (parseInt(approved_by) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                approved_by = EmpCode + " - " + EmpName.toUpperCase();
            }
        });

        if (parseInt(reason_for_rejection) == 1) {
            reason_for_rejection = rejected_reason;
        } else {
            reason_for_rejection = "";
            approved_rejected_tasks = total_approve_records;
            approved_rejected_tasks += " / ";
            approved_rejected_tasks += total_rejected_records;
        }

        if (String(approved_on) != null && String(approved_on) != '') {
            approved_rejected_on = approved_on;
            approved_rejected_by = approved_by;
        } else if (String(rejected_on) != null && String(rejected_on) != '') {
            approved_rejected_on = rejected_on;
            approved_rejected_by = rejected_by;
        }

        var occurance = '';
        var occuranceid;
        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_SNO', clone1).text(SNO);
        $('.tbl_uploaded_file_name', clone1).text(csv_name);
        $(".tbl_uploaded_by", clone1).text(uploaded_by);
        $('.tbl_uploaded_on', clone1).text(uploaded_on);
        $('.tbl_no_of_tasks', clone1).text(tbl_no_of_tasks);
        $('.tbl_approved_rejected_tasks', clone1).text(approved_rejected_tasks);
        $('.tbl_approved_rejected_on', clone1).text(approved_rejected_on);
        $('.tbl_approved_rejected_by', clone1).text(approved_rejected_by);
        $('.tbl_reason_for_rejection', clone1).text(reason_for_rejection);
        $('.tbl_domain', clone1).text(domain_name);
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }

    if (isNull == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, SNO, TOTAL_RECORD);
    }
    hideLoader();
}


$(function() {
    REPORT_VIEW.hide();
    asBulkReport.pageControls();
    initialize();
    UserGroupDetails();
    ITEMS_PER_PAGE.on('change', function(e) {
        perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        $('#show-button').trigger("click");
    });
    loadItemsPerPage();
});

//To export data
AssignStatutoryBulkReport.prototype.exportData = function() {

    var clientGroup = parseInt(GROUP.val());
    var clientGroupName = GROUP_VAL.val();
    var legalEntityID = parseInt(LEGAL_ENTITY.val());
    var legalEntityName = LEGAL_ENTITY_VAL.val();
    var deIds = DE_NAME.val();
    var domainIds = DOMAIN.val();
    var unitID = "";
    var unitName = UNIT_VAL.val();

    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();

    var selectedDEName = [];
    var splitValues;

    var selectedDomain = [];
    $.each(domain_ids, function(key, value) {
        selectedDomain.push(parseInt(value));
    });

    if (UNIT.val()) {
        unitID = UNIT.val();
    }


    /* multiple COUNTRY selection in to generate array */
    if ($('#de_name option:selected').text() == "") {
        selectedDEName = EXISTING_USER_ID; // When execute unselected the Field.
    } else {
        $.each(deIds, function(key, value) {
            selectedDEName.push(parseInt(value));
        });
    }

    var domainNames = $("#domain option:selected").map(function() {
        return $(this).text();
    }).get().join(',');

    displayLoader();

    filterdata = {
        "bu_client_id": clientGroup,
        "bu_group_name": clientGroupName,
        "bu_legal_entity_id": legalEntityID,
        "legal_entity_name": legalEntityName,
        "bu_unit_id": unitID,
        "unit_name": unitName,
        "domain_ids": selectedDomain,
        "d_names": domainNames,
        "from_date": fromDate,
        "to_date": toDate,
        "child_ids": selectedDEName,
        "user_category_id": USER_CATEGORY_ID,
        "csv": CSV
    };

    displayLoader();
    bu.exportASBulkReportData(filterdata,
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