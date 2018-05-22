var LIST_PAGE = $(".list-page");
var DATA_LIST_PAGE = $(".data-list-page");
var CLIENT_GROUP = $("#client_group");
var CLIENT_GROUP_ID = $("#client_group_id");
var AC_CLIENT_GROUP = $("#ac_client_group");
var LEGAL_ENTITY = $("#legal_entity");
var LEGAL_ENTITY_ID = $("#legal_entity_id");
var AC_LEGAL_ENTITY = $("#ac_legal_entity");
var SHOW_BUTTON = $("#show_button");
var LIST_VIEW = $("#list_view");
var DATA_TABLE_TBODY = $("#data_table_tbody");
var DOWNLOAD_BTN = $(".download");
var PASSWORD_APPROVE_SUBMIT = $('#password_approve_submit');
var APPROVE_ID = $('#approve_id');
var APPROVE_PASSWORD = $('#approve_password');
var PASSWORD_REJECT_SUBMIT = $('#password_reject_submit');
var REJECT_ID = $('#reject_id');
var REJECT_PASSWORD = $('#reject_password');
var REJECT_REASON = $('#remark');
var SINGLE_REJECT_REASON = $('#single_reject_remark');
var PASSWORD_SINGLE_REJECT_SUBMIT = $('#password_single_reject_submit');
var SINGLE_REJECT_ID = $('#single_reject_id');
var FILTER_UPLOADED_FILE_NAME = $('#filter_uploaded_file_name');
var FILTER_UPLOADED_ON = $('#filter_uploaded_on');
var FILTER_UPLOADED_BY = $('#filter_uploaded_by');
var FILTER_NO_OF_RECORDS = $('#filter_no_of_records');
var ASID = $("#assigned_statutory_id");
var DETAILS_TBODY = $("#data_details_table_tbody");
var CHECK_ALL_APPROVE = $("#check_all_approve");
var CHECK_ALL_REJECT = $("#check_all_reject");
var DOMAIN = $("#domain");
var UNIT = $("#unit");
var PRIMARY_LEGISLATION = $("#primary_legislation");
var SECONDARY_LEGISLATION = $("#secondary_legislation");
var AC_SECONDARY_LEGISLATION = $("#ac_secondary_legislation");
var STATUTORY_PROVISION_NAME = $("#statutory_provision");
var AC_STATUTORY_PROVISION = $("#ac_statutory_provision");
var COMPLIANCE_TASK_NAME = $("#compliance_task");
var AC_COMPLIANCE_TASK = $("#ac_compliance_task");
var STATUTORY_STATUS = $("#statutory_status");
var COMPLIANCE_STATUS = $("#compliance_status");
var COMPLIANCE_DESCRIPTION_NAME = $("#compliance_description");
var AC_COMPLIANCE_DESCRIPTION = $("#ac_compliance_description");
var SEARCH = $("#search");
var PAGINATION_VIEW = $('.pagination-view');
var PAGINATION = $('#pagination_rpt');
var SHOW_COUNT = $('.show-count');
var CURRENT_PAGE = 1;
var SNO = 0;
var TOTAL_RECORD;
var PAGE_LIMIT;
var ITEMS_PER_PAGE = $('#items_per_page');
var SUBMIT = $('#submit');
var CLIENT_GROUP_NAME = $('#client_group_name');
var LEGAL_ENTITY_NAME = $('#legal_entity_name');
var COUNTRY_NAME = $('#country_name');
var UPLOADED_FILE_NAME = $('#uploaded_file_name');
var UPLOADED_ON = $('#uploaded_on');
var UPLOADED_BY = $('#uploaded_by');
var FILTERED_DATA = $(".filtered-data");
var CLEAR_FILTERED = $(".clear-filtered");
var FILTER_DOMAIN = $("#filter_domain");
var FILTER_UNIT = $("#filter_unit");
var FILTER_PRIMARY_LEGISLATION = $("#filter_primary_legislation");
var FILTER_SECONDARY_LEGISLATION = $("#filter_secondary_legislation");
var FILTER_STATUTORY_PROVISION = $("#filter_statutory_provision");
var FILTER_COMPLIANCE_TASK = $("#filter_compliance_task");
var FILTER_COMPLIANCE_DESCRIPTION = $("#filter_compliance_description");
var ACTION_PASSWORD_SUBMIT = $("#action_password_submit");
var SUBMIT_PASSWORD = $("#submit_password");
var STATUTORY_APPLICABLE = $("#statutory_applicable");
var STATUTORY_NOT_APPLICABLE = $("#statutory_not_applicable");
var STATUTORY_DO_NOT_SHOW = $("#statutory_do_not_show");
var COMPLIANCE_APPLICABLE = $("#compliance_applicable");
var COMPLIANCE_NOT_APPLICABLE = $("#compliance_not_applicable");
var COMPLIANCE_DO_NOT_SHOW = $("#compliance_do_not_show");
var PER_PAGE = 0;

// Display spinner icon in page
displayLoader = function() {
    $('.loading-indicator-spin').show();
}

// Hiding spinner icon in page
hideLoader = function() {
    $('.loading-indicator-spin').hide();
}

// Created Class variables
ApproveAssignStatutoryBU = function() {
    this.clientGroup = [];
    this.legalEntities = [];
    this.userList = [];
    this.dataList = [];
    this.dataListDetails = [];
    this.filterDomain = [];
    this.filterUnits = [];
    this.filterPrimaryLegislation = [];
    this.filterSecondaryLegislation = [];
    this.filterStatutoryProvision = [];
    this.filterComplianceTask = [];
    this.filterStatutoryStatus = [];
    this.filterComplianceStatus = [];
    this.filterComplianceDescription = [];
}

// Page loading clear the element default value
ApproveAssignStatutoryBU.prototype.pageLoad = function() {
    statute = this;
    LIST_PAGE.show();
    DATA_LIST_PAGE.hide();
    LIST_VIEW.hide();
    CLIENT_GROUP.val('');
    CLIENT_GROUP_ID.val('');
    LEGAL_ENTITY.val('');
    LEGAL_ENTITY_ID.val('');
    FILTER_UPLOADED_FILE_NAME.val('');
    FILTER_UPLOADED_ON.val('');
    FILTER_UPLOADED_BY.val('');
    FILTER_NO_OF_RECORDS.val('');
    statute.initialize();
};

// Initial function to fetch client and legal entity data to server
ApproveAssignStatutoryBU.prototype.initialize = function() {
    statute = this;
    displayLoader();
    bu.getClientInfo(function(error, response) {
        if (error == null) {
            statute.clientGroup = response.bu_clients;
            statute.legalEntities = response.bu_legalentites;
            hideLoader();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

// To display any failure message to display
ApproveAssignStatutoryBU.prototype.failuresMessage = function(error) {
    if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else {
        displayMessage(error);
    }
};

// HTML page element event control function
PageControls = function() {
    CLIENT_GROUP.keyup(function(e) {
        var textVal = CLIENT_GROUP.val().trim();
        var clientGroupList = STATUTE.clientGroup;
        var conditionFields = [];
        var condition_values = [];
        commonAutoComplete(e, AC_CLIENT_GROUP, CLIENT_GROUP_ID, textVal,
            clientGroupList, "cl_name", "cl_id",
            function(val) {
                onClientGroupAutoCompleteSuccess(STATUTE, val);
            }, conditionFields, condition_values);
    });
    LEGAL_ENTITY.keyup(function(e) {
        var textVal = LEGAL_ENTITY.val().trim();
        var legalEntityList = STATUTE.legalEntities;
        var conditionFields = ["cl_id"];
        var condition_values = [CLIENT_GROUP_ID.val()];
        commonAutoComplete(e, AC_LEGAL_ENTITY, LEGAL_ENTITY_ID, textVal,
            legalEntityList, "le_name", "le_id",
            function(val) {
                onLegalEntityAutoCompleteSuccess(STATUTE, val);
            }, conditionFields, condition_values);
    });
    SHOW_BUTTON.click(function() {
        if (validate()) {
            LIST_VIEW.show();
            STATUTE.fetchValues();
        }
    });
    DOWNLOAD_BTN.click(function() {
        this.find('.dropdown-content').show();
    });
    PASSWORD_APPROVE_SUBMIT.click(function() {
        validateAuthentication(APPROVE_ID.val(), APPROVE_PASSWORD, null);
    });
    PASSWORD_REJECT_SUBMIT.click(function() {
        validateAuthentication(
            REJECT_ID.val(), REJECT_PASSWORD, REJECT_REASON
        );
    });
    FILTER_UPLOADED_FILE_NAME.keyup(function() {

        fList = keySearchList(STATUTE.dataList);
        STATUTE.displayListPage(fList);
    });
    FILTER_UPLOADED_ON.keyup(function() {
        fList = keySearchList(STATUTE.dataList);
        STATUTE.displayListPage(fList);
    });
    FILTER_UPLOADED_BY.keyup(function() {
        fList = keySearchList(STATUTE.dataList);
        STATUTE.displayListPage(fList);
    });
    FILTER_NO_OF_RECORDS.keyup(function() {
        fList = keySearchList(STATUTE.dataList);
        STATUTE.displayListPage(fList);
    });
    CHECK_ALL_APPROVE.click(function() {
        if ($(this).prop("checked") == true) {
            DETAILS_TBODY.find('.single-approve').removeAttr("checked");
            DETAILS_TBODY.find('.single-approve').trigger('click');
        } else{
            DETAILS_TBODY.find('.single-approve').removeAttr("checked");
            DETAILS_TBODY.find(".single-approve").each(function(){
               $(this).prop('checked', false).triggerHandler('click');
            });
        }
    });
    CHECK_ALL_REJECT.click(function() {
        if ($(this).prop("checked") == true) {
            confirmationAction(0, 'single-reject');
        } else {
            DETAILS_TBODY.find('.single-reject').removeAttr("checked");
            DETAILS_TBODY.find('.rejected-reason').html('')
            DETAILS_TBODY.find(".single-reject").each(function(){
               $(this).prop('checked', false).triggerHandler('click');
            });
        }
    });
    PASSWORD_SINGLE_REJECT_SUBMIT.click(function() {
        var reason = SINGLE_REJECT_REASON.val().trim();
        if (reason.length == 0) {
            displayMessage(message.reason_required);
            SINGLE_REJECT_REASON.focus();
            CHECK_ALL_REJECT.removeAttr("checked");
            return false;
        } else if (reason.match(/^[ A-Za-z0-9_.,-]*$/) === null) {
            displayMessage(message.reason_invalid);
            SINGLE_REJECT_REASON.focus();
            CHECK_ALL_REJECT.removeAttr("checked");
            return false;
        } else if (validateMaxLength('reason', reason, "Reason") == false) {
            CHECK_ALL_REJECT.removeAttr("checked");
            return false;
        } else {
            Custombox.close();
            if (CHECK_ALL_REJECT.prop("checked") == true) {
                DETAILS_TBODY.find('.single-reject').removeAttr("checked");
                DETAILS_TBODY.find('.single-reject').trigger('click');
            } else {
                singleReject(SINGLE_REJECT_ID.val(), true);
            }
        }
    });
    $('.right-bar-toggle').on('click', function(e) {
        $('#wrapper').toggleClass('right-bar-enabled');
    });
    STATUTORY_PROVISION_NAME.keyup(function(e) {
        var textVal = STATUTORY_PROVISION_NAME.val().trim();
        var statutoryProvisionList = STATUTE.filterStatutoryProvision;
        arrayListSearch(e, textVal, statutoryProvisionList,
            AC_STATUTORY_PROVISION,
            function(val) {
                STATUTORY_PROVISION_NAME.val(val[1]);
            });
    });
    SECONDARY_LEGISLATION.keyup(function(e) {
        var textVal = SECONDARY_LEGISLATION.val().trim();
        var secondaryLegislationList = STATUTE.filterSecondaryLegislation;
        arrayListSearch(e, textVal, secondaryLegislationList,
            AC_SECONDARY_LEGISLATION,
            function(val) {
                SECONDARY_LEGISLATION.val(val[1]);
            });
    });
    COMPLIANCE_TASK_NAME.keyup(function(e) {
        var textVal = COMPLIANCE_TASK_NAME.val().trim();
        var complianceTaskList = STATUTE.filterComplianceTask;
        arrayListSearch(e, textVal, complianceTaskList, AC_COMPLIANCE_TASK,
            function(val) {
                COMPLIANCE_TASK_NAME.val(val[1]);
            });
    });
    COMPLIANCE_DESCRIPTION_NAME.keyup(function(e) {
        var textVal = COMPLIANCE_DESCRIPTION_NAME.val().trim();
        var complianceDescriptionList = STATUTE.filterComplianceDescription;
        arrayListSearch(e, textVal, complianceDescriptionList,
            AC_COMPLIANCE_DESCRIPTION,
            function(val) {
                COMPLIANCE_DESCRIPTION_NAME.val(val[1]);
            });
    });
    SEARCH.click(function() {
        var tempArr = [];
        var u = "";
        var pLeg = "Primary Legislation : ";
        var sLeg = "Secondary Legislation : ";
        var sPro = "Statutory Provision : ";
        var cTask = "Compliance Task Name : ";
        var sS = "Statutory Status : ";
        var cS = "Compliance Status : ";
        var cDescription = "Compliance Description : ";

        if ($(".view-data:checked").val() == "1")
            tempArr.push("View Data : Verified");
        else if ($(".view-data:checked").val() == "0")
            tempArr.push("View Data : Pending");
        if (DOMAIN.val() != null)
            tempArr.push("Domain Name : " + DOMAIN.val().join());
        if (UNIT.val() != null) {
            u = "";
            $.each(UNIT.find('option:selected'), function() {
                (u != "") ? u = u + ', ' + $(this).text(): u = $(this).text();
            });
            tempArr.push("Unit Name : " + u);
        }
        if (PRIMARY_LEGISLATION.val() != null)
            tempArr.push(pLeg + PRIMARY_LEGISLATION.val().join());
        if (SECONDARY_LEGISLATION.val() != "")
            tempArr.push(sLeg + SECONDARY_LEGISLATION.val());
        if (STATUTORY_PROVISION_NAME.val() != "")
            tempArr.push(sPro + STATUTORY_PROVISION_NAME.val());
        if (COMPLIANCE_TASK_NAME.val() != "")
            tempArr.push(cTask + COMPLIANCE_TASK_NAME.val());
        if (STATUTORY_STATUS.val() != "")
            tempArr.push(sS + STATUTORY_STATUS.find('option:selected').text());
        if (COMPLIANCE_STATUS.val() != "")
            tempArr.push(
                cS + COMPLIANCE_STATUS.find('option:selected').text()
            );
        if (COMPLIANCE_DESCRIPTION_NAME.val() != "")
            tempArr.push(cDescription + COMPLIANCE_DESCRIPTION_NAME.val());
        tex = "";
        if (tempArr.length > 0) {
            CLEAR_FILTERED.show();
            for (var i = 0; i < tempArr.length; i++) {
                (tex != "") ? tex = tex + ' | ' + tempArr[i]: tex = tempArr[i];
            }
            FILTERED_DATA.html("Filtered By - " + tex);
        } else {
            FILTERED_DATA.empty();
            CLEAR_FILTERED.hide();
        }
        if (AC_SECONDARY_LEGISLATION.is(':visible') == true) {
            displayMessage(message.secondary_legislation_required);
            return false;
        } else if (AC_STATUTORY_PROVISION.is(':visible') == true) {
            displayMessage(message.statutory_provision_required);
            return false;
        } else if (AC_COMPLIANCE_TASK.is(':visible') == true) {
            displayMessage(message.compliance_task_required);
            return false;
        } else if (AC_COMPLIANCE_DESCRIPTION.is(':visible') == true) {
            displayMessage(message.compliance_description_required);
            return false;
        } else {
            SNO = 0;
            CURRENT_PAGE = 1;
            viewListDetailsPage(ASID.val());
        }
    });
    CLEAR_FILTERED.click(function() {
        goToDetailsPage(ASID.val());
    });
    SUBMIT.click(function() {
        confirmationAction(0, 'submit');
    });
    ACTION_PASSWORD_SUBMIT.click(function() {
        STATUTE.submitProcess();
    });
    ITEMS_PER_PAGE.on('change', function(e) {
        PER_PAGE = parseInt($(this).val());
        SNO = 0;
        CURRENT_PAGE = 1;
        createPageView(TOTAL_RECORD);
        viewListDetailsPage(ASID.val());
    });
    FILTER_DOMAIN.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_UNIT.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_PRIMARY_LEGISLATION.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_SECONDARY_LEGISLATION.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_STATUTORY_PROVISION.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_COMPLIANCE_TASK.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    FILTER_COMPLIANCE_DESCRIPTION.keyup(function() {
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    STATUTORY_APPLICABLE.click(function() {
        if ($(this).hasClass("text-info")) {
            $(this).removeClass("text-info");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-info");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    STATUTORY_NOT_APPLICABLE.click(function() {
        if ($(this).hasClass("text-warning")) {
            $(this).removeClass("text-warning");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-warning");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    STATUTORY_DO_NOT_SHOW.click(function() {
        if ($(this).hasClass("text-danger")) {
            $(this).removeClass("text-danger");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-danger");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    COMPLIANCE_APPLICABLE.click(function() {
        if ($(this).hasClass("text-info")) {
            $(this).removeClass("text-info");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-info");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    COMPLIANCE_NOT_APPLICABLE.click(function() {
        if ($(this).hasClass("text-warning")) {
            $(this).removeClass("text-warning");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-warning");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
    COMPLIANCE_DO_NOT_SHOW.click(function() {
        if ($(this).hasClass("text-danger")) {
            $(this).removeClass("text-danger");
            $(this).addClass("text-muted");
        } else {
            $(this).removeClass("text-muted");
            $(this).addClass("text-danger");
        }
        fList = keySearchDetailsList(STATUTE.dataListDetails);
        STATUTE.displayDetailsPage(fList, true);
    });
}

// Search key from array list. to display list tag
arrayListSearch = function(e, textval, listval, acDiv, callback) {
    var checkKey = [16, 17, 18, 19, 20, 27, 33, 34, 42, 91, 92, 112, 113,
        114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144, 145
    ];
    if (textval && textval.trim() != '' && listval.length > 0 &&
        $.inArray(e.keyCode, checkKey) == -1) {
        let tot = listval.filter((data) => {
            return (data.toLowerCase().indexOf(textval.toLowerCase()) > -1);
        });
        let s = '';
        acDiv.find('li').remove();
        if (tot.length > 0) {
            for (var i = 0; i < tot.length; ++i) {
                if (10 >= (i + 1))
                    s += '<li onclick="activate_text(this,' + callback + ')"' +
                    'id="' + tot[i] + '">' + tot[i] + '</li>';
            }
        }
        acDiv.find('ul').append(s);
        acDiv.show();
    } else {
        $('.ac-textbox').hide();
    }
    onArrowKey(e, acDiv, callback);
}

// Clear element default value to pass value array list
clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

// After Selected Client Group set values
onClientGroupAutoCompleteSuccess = function(STATUTE, val) {
    CLIENT_GROUP.val(val[1]);
    CLIENT_GROUP_ID.val(val[0]);
    CLIENT_GROUP.focus();
    clearElement([LEGAL_ENTITY, LEGAL_ENTITY_ID]);
}

// After Selected Legal Entity set values
onLegalEntityAutoCompleteSuccess = function(STATUTE, val) {
    LEGAL_ENTITY.val(val[1]);
    LEGAL_ENTITY_ID.val(val[0]);
    LEGAL_ENTITY.focus();
}

// Show click after to validate filter value
validate = function() {
    var isValid = true;
    if (CLIENT_GROUP_ID.val().trim().length == 0) {
        displayMessage(message.client_group_required);
        isValid = false;
    } else if (CLIENT_GROUP.val().trim().length > 50) {
        displayMessage(message.client_group_50);
        isValid = false;
    } else if (LEGAL_ENTITY_ID.val().trim().length == 0) {
        displayMessage(message.legalentity_required);
        isValid = false;
    } else if (LEGAL_ENTITY.val().trim().length > 50) {
        displayMessage(message.le_50);
        isValid = false;
    }
    return isValid;
};

// Grid view filter search to pass array list value
keySearchList = function(d) {
    var fList = [];
    var valueOne = '';
    var valueTwo = '';
    var valueThree = '';
    var valueFour = '';
    var e;
    keyOne = FILTER_UPLOADED_FILE_NAME.val().toLowerCase();
    keyTwo = FILTER_UPLOADED_ON.val().toLowerCase();
    keyThree = FILTER_UPLOADED_BY.val().toLowerCase();
    keyFour = FILTER_NO_OF_RECORDS.val();
    for (e in d) {
        valueOne = d[e].csv_name.toLowerCase();
        valueTwo = d[e].uploaded_on.toLowerCase();
        valueThree = d[e].uploaded_by.toString().toLowerCase();
        valueFour = d[e].no_of_records.toString();
        if ((~valueOne.indexOf(keyOne)) && (~valueTwo.indexOf(keyTwo)) &&
            (~valueThree.indexOf(keyThree)) && (~valueFour.indexOf(keyFour))) {
            fList.push(d[e]);
        }
    }
    return fList
}

// Grid detailed view filter search value to pass array list value
keySearchDetailsList = function(d) {
    var sKeys = cKeys = [];
    var fList = [];
    var valueOne = '';
    var valueTwo = '';
    var valueThree = '';
    var valueFour = '';
    var valueFive = '';
    var valueSix = '';
    var valueSeven = '';
    var sStatus = '';
    var cStatus = '';
    var e;

    keyOne = FILTER_DOMAIN.val().toLowerCase();
    keyTwo = FILTER_UNIT.val().toLowerCase();
    keyThree = FILTER_PRIMARY_LEGISLATION.val().toLowerCase();
    keyFour = FILTER_SECONDARY_LEGISLATION.val().toLowerCase();
    keyFive = FILTER_STATUTORY_PROVISION.val().toLowerCase();
    keySix = FILTER_COMPLIANCE_TASK.val().toLowerCase();
    keySeven = FILTER_COMPLIANCE_DESCRIPTION.val().toLowerCase();

    if (STATUTORY_APPLICABLE.hasClass("text-muted") &&
        STATUTORY_NOT_APPLICABLE.hasClass("text-muted") &&
        STATUTORY_DO_NOT_SHOW.hasClass("text-muted")) {
        sKeys = [1, 2, 3];
    }
    if (STATUTORY_APPLICABLE.hasClass("text-info"))
        sKeys.push(1);
    if (STATUTORY_NOT_APPLICABLE.hasClass("text-warning"))
        sKeys.push(2);
    if (STATUTORY_DO_NOT_SHOW.hasClass("text-danger"))
        sKeys.push(3);
    if (COMPLIANCE_APPLICABLE.hasClass("text-muted") &&
        COMPLIANCE_NOT_APPLICABLE.hasClass("text-muted") &&
        COMPLIANCE_DO_NOT_SHOW.hasClass("text-muted")) {
        cKeys = [1, 2, 3];
    }
    if (COMPLIANCE_APPLICABLE.hasClass("text-info"))
        cKeys.push(1);
    if (COMPLIANCE_NOT_APPLICABLE.hasClass("text-warning"))
        cKeys.push(2);
    if (COMPLIANCE_DO_NOT_SHOW.hasClass("text-danger"))
        cKeys.push(3);

    for (e in d) {
        valueOne = d[e].d_name.toLowerCase();
        valueTwo = (d[e].u_code + ' - ' +d[e].u_name).toLowerCase();
        valueThree = d[e].p_leg.toLowerCase();
        valueFour = d[e].s_leg.toLowerCase();
        valueFive = d[e].s_prov.toLowerCase();
        valueSix = d[e].c_task.toLowerCase();
        valueSeven = d[e].c_desc.toLowerCase();
        sStatus = d[e].s_status;
        cStatus = d[e].c_status;
        if ((~valueOne.indexOf(keyOne)) && (~valueTwo.indexOf(keyTwo)) &&
            (~valueThree.indexOf(keyThree)) && (~valueFour.indexOf(keyFour)) &&
            (~valueFive.indexOf(keyFive)) && (~valueSix.indexOf(keySix)) &&
            (~valueSeven.indexOf(keySeven))) {
            if ((~sKeys.indexOf(sStatus)) && (~cKeys.indexOf(cStatus))) {
                fList.push(d[e]);
            }
        }
    }
    return fList
}

// download click show hide download list
download = function(element) {
    if ($("." + element).is(':visible') == false) {
        $(".dropdown-content").hide();
        $("." + element).toggle();
    } else {
        $("." + element).toggle();
    }
}

viewListPage = function() {
    LIST_PAGE.show();
    DATA_LIST_PAGE.hide();
    LIST_VIEW.show();
    FILTER_UPLOADED_FILE_NAME.val('');
    FILTER_UPLOADED_ON.val('');
    FILTER_UPLOADED_BY.val('');
    FILTER_NO_OF_RECORDS.val('');
    STATUTE.fetchValues();
}

// To get value Grid view data to search values
ApproveAssignStatutoryBU.prototype.fetchValues = function() {
    statute = this;
    var clId = CLIENT_GROUP_ID.val();
    var leId = LEGAL_ENTITY_ID.val();
    var data = null;
   
    displayLoader();
    bu.getAssignStatutoryForApprove(parseInt(clId),
        parseInt(leId),
        function(error, response) {
            if (error == null) {
                statute.dataList = response.pending_csv_list_as;
                data = statute.dataList;
                bu.getDomainUserInfo(function(err, resp) {
                    if (err == null) {
                        statute.userList = resp.domain_executive_info;
                        var i;
                        for (i = 0; i < data.length; i++) {
                            var j;
                            for (j = 0; j < statute.userList.length; j++) {
                                if (data[i].uploaded_by == statute.userList[j].user_id) {
                                    data[i].uploaded_by = statute.userList[j].emp_code_name;
                                    break;
                                }
                            }
                        }
                        statute.displayListPage(data);
                        hideLoader();
                    } else {
                        hideLoader();
                        statute.failuresMessage(err);
                    }
                });
            } else {
                statute.failuresMessage(error);
                hideLoader();
            }
        });
};

// To display value in grid view html element.
ApproveAssignStatutoryBU.prototype.displayListPage = function(data) {
    var no = 0;
    var clone = null;
    var path = "/uploaded_file/";
    statute = this;
    DATA_TABLE_TBODY.empty();
    if (data.length == 0) {
        hideLoader();
        clone = $('#template #record_not_found tr').clone();
        $('.no-records', clone).attr("colspan", "10");
        DATA_TABLE_TBODY.append(clone);
        return false;
    }
    
    $.each(data, function(k, v) {
        no++;
        clone = $('#template #report_table tr').clone();
        $('.sno', clone).text(no);
        $('.uploaded-file-name', clone).html(v.csv_name);
        $('.uploaded-on', clone).html(v.uploaded_on);
        $('.uploaded-by', clone).html(v.uploaded_by);
        $('.no-of-records', clone).html(v.no_of_records);
        if (v.approved_count != 0 || v.rej_count != 0) {
            if (v.approved_count == 0) { v.approved_count = 0; }
            if (v.rej_count == 0) { v.rej_count = 0; }
            $('.approve-reject', clone)
                .html(v.approved_count + '/' + v.rej_count);
            $('.view', clone)
                .html('<i class="fa fa-pencil text-primary c-pointer"></i>')
                .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
        } else {
            $('.view', clone)
                .html('<button class="btn btn-primary text-center ' +
                    ' waves-effect waves-light" type="button"> View </button>')
                .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
        }
        $('.fa-download', clone)
            .attr("onClick", "download('show-download" + v.csv_id + "')");
        
        $('.download .dowload-excel', clone).attr({
            href: path + "xlsx/" + v.download_file.split('.')[0] + ".xlsx",
            download: "download"
        });
        $('.download .dowload-csv', clone).attr({
            href: path + "csv/" + v.download_file.split('.')[0] + ".csv",
            download: "download"
        });
        $('.download .dowload-ods', clone).attr({
            href: path + "ods/" + v.download_file.split('.')[0] + ".ods",
            download: "download"
        });
        $('.download .dowload-text', clone).attr({
            href: path + "txt/" + v.download_file.split('.')[0] + ".txt",
            download: "download"
        });
        $('.dropdown-content', clone).addClass("show-download" + v.csv_id);
        $('.approve span', clone)
            .attr(
                "onClick", "confirmationAction(" + v.csv_id + ", 'approve')"
            );
        $('.reject span', clone)
            .attr("onClick", "confirmationAction(" + v.csv_id + ", 'reject')");
        DATA_TABLE_TBODY.append(clone);
    });
};

// Approve & Reject confirmation to display pop-up
confirmationAction = function(id, action) {
    APPROVE_ID.val(id);
    REJECT_ID.val(id);
    SINGLE_REJECT_REASON.val("");
    REJECT_REASON.val("");
    APPROVE_PASSWORD.val("");
    REJECT_PASSWORD.val("");
    SUBMIT_PASSWORD.val("");
    Custombox.open({
        target: '#custom_modal_' + action,
        effect: 'contentscale',
        complete: function() {
            SUBMIT_PASSWORD.focus();
            APPROVE_PASSWORD.focus();
            REJECT_PASSWORD.focus();
        }
    });
}

// Event click close pop-up
closeCustombox = function() {
    CHECK_ALL_REJECT.removeAttr("checked");
    Custombox.close();
    if ($("#reject" + SINGLE_REJECT_ID.val()))
        $("#reject" + SINGLE_REJECT_ID.val()).removeAttr("checked");
}

// validate to approve or reject and server side.
validateAuthentication = function(id, passwordField, reasonField) {
    var clId = CLIENT_GROUP_ID.val();
    var leId = LEGAL_ENTITY_ID.val();
    var password = passwordField.val().trim();
    var action = 1;
    var reason = null;
    var statusmsg = message.manuval_rejected_confirm;

    if (password.length == 0) {
        displayMessage(message.password_required);
        passwordField.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    if (reasonField != null) {
        action = 2;
        reason = reasonField.val().trim();
        if (reason.length == 0) {
            displayMessage(message.reason_required);
            reasonField.focus();
            return false;
        } else if (reason.match(/^[ A-Za-z0-9_.,-]*$/) === null) {
            displayMessage(message.reason_invalid);
            reasonField.focus();
            return false;
        } else if (validateMaxLength('reason', reason, "Reason") == false) {
            return false;
        }
    }
    displayLoader();
    bu.validateAssignStatutory(parseInt(id), function(error, res1) {
        hideLoader();
        Custombox.close();
        if (res1.rej_count == 0) {
            approveOrRejectAction(id, clId, leId, action, reason, password);
        } else {
            setTimeout(function() {
                confirm_alert(statusmsg, function(isConfirm) {
                    if (isConfirm) {
                        approveOrRejectAction(id, clId, leId,
                            action, reason, password);
                    }
                });
            }, 500);
        }
    });
}

// Server to approve & Reject send status. To check system rejected status
approveOrRejectAction = function(id, clId, leId, action, reason, password) {
    displayLoader();
    bu.assignStatutoryActionInList(parseInt(clId), parseInt(leId),
        parseInt(id), parseInt(action), reason, password,
        function(err1, res2) {
            console.log(err1, res2);
            if (err1 == null) {
                if (res2.hasOwnProperty("rej_count")) {
                    setTimeout(function() {
                        hideLoader();
                        var statusmsg = res2.rej_count + ' ' + 
                            message.sys_rejected_confirm;
                        confirm_alert(statusmsg, function(isConfirm) {
                            if (isConfirm) {
                                displayLoader();
                                bu.confirmAssignStatutoryUpdateAction(
                                    parseInt(id),
                                    parseInt(clId), parseInt(leId),
                                    function(error, res3) {
                                        if (error == null) {
                                            displayMsg(action);
                                            STATUTE.fetchValues();
                                        } else {
                                            STATUTE.failuresMessage(error);
                                            hideLoader();
                                        }
                                    });
                            }
                        });
                    }, 500);
                } else {
                    displayMsg(action);
                    STATUTE.fetchValues();
                }
            } else {
                STATUTE.failuresMessage(err1);
                hideLoader();
            }
        });
}

// Display message to info message
displayMsg = function(action) {
    if (action == 1)
        displaySuccessMessage(message.assign_statutory_approved_success);
    else
        displaySuccessMessage(message.assign_statutory_rejected_success);
}

// Grid detailed view page Filter element set default value
goToDetailsPage = function(id) {
    FILTERED_DATA.empty();
    CLEAR_FILTERED.hide();
    $(".all-data").trigger('click');
    DOMAIN.find("option").remove();
    DOMAIN.multiselect('destroy');
    UNIT.find("option").remove();
    UNIT.multiselect('destroy');
    PRIMARY_LEGISLATION.find("option").remove();
    PRIMARY_LEGISLATION.multiselect('destroy');
    SECONDARY_LEGISLATION.val("");
    STATUTORY_PROVISION_NAME.val("");
    COMPLIANCE_TASK_NAME.val("");
    STATUTORY_STATUS.val("");
    COMPLIANCE_STATUS.val("");
    COMPLIANCE_DESCRIPTION_NAME.val("");
    SNO = 0;
    CURRENT_PAGE = 1;
    viewListDetailsPage(id);
}

// Grid detailed view page load to all the element set default value
viewListDetailsPage = function(id) {
    var view_data = $(".view-data:checked").val();
    LIST_PAGE.hide();
    DATA_LIST_PAGE.show();
    FILTER_DOMAIN.val('');
    FILTER_UNIT.val('');
    FILTER_PRIMARY_LEGISLATION.val('');
    FILTER_SECONDARY_LEGISLATION.val('');
    FILTER_STATUTORY_PROVISION.val('');
    FILTER_COMPLIANCE_TASK.val('');
    FILTER_COMPLIANCE_DESCRIPTION.val('');
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    if (CURRENT_PAGE == 1)
        SNO = 0;
    else
        SNO = (CURRENT_PAGE - 1) * PAGE_LIMIT;
    STATUTE.loadFilterPage(id);
    
    STATUTE.loadDetailsPageWithFilter(id, view_data, DOMAIN.val(), UNIT.val(),
        PRIMARY_LEGISLATION.val(), SECONDARY_LEGISLATION.val(),
        STATUTORY_PROVISION_NAME.val(), COMPLIANCE_TASK_NAME.val(),
        STATUTORY_STATUS.val(), COMPLIANCE_STATUS.val(),
        COMPLIANCE_DESCRIPTION_NAME.val());
}

// To load the Grid detailed view page values
ApproveAssignStatutoryBU.prototype.displayDetailsPage = function(data, flag) {
    var clone = null;
    var no = 0;
    var showFrom = 1;

    if (flag == false)
        showFrom = SNO + 1;

    DETAILS_TBODY.empty();
    if (data.length > 0) {
        $.each(data, function(k, v) {
            if (flag == false) {
                SNO = parseInt(SNO) + 1;
                no = SNO;
            } else {
                no++;
            }
            clone = $('#template #report_details_table tr').clone();
            $('.sno', clone).text(no);
            $('.single-approve', clone).val(v.as_id).attr({
                id: "approve" + v.as_id,
                onClick: "singleApprove(" + v.as_id + ")",
                name: "action" + v.as_id
            });
            $('.single-reject', clone).val(v.as_id).attr({
                id: "reject" + v.as_id,
                onClick: "singleReject(" + v.as_id + ", false)",
                name: "action" + v.as_id
            });
            $('.rejected-reason', clone)
                .attr("id", "rejected_reason" + v.as_id);
            if (v.bu_action == 1) {
                $('.single-approve', clone).prop('checked', true);
                $('.single-reject', clone).prop('checked', false);
            } else if (v.bu_action == 2) {
                $('.single-reject', clone).prop('checked', true);
                $('.single-approve', clone).prop('checked', false);
                if (v.remarks != "") {
                    $('.rejected-reason', clone)
                        .html('<i class="fa fa-info-circle fa-1-2x l-h-51 ' +
                            'text-primary c-pointer" data-toggle="tooltip" ' +
                            'data-original-title="' + v.remarks + '"></i>');
                }
            } else {
                $('.single-approve', clone).prop('checked', false);
                $('.single-reject', clone).prop('checked', false);
            }
            $('.domain-name', clone).html(v.d_name);
            $('.unit-name span', clone).html(v.u_code + ' - ' +v.u_name);
            $('.unit-name i', clone).attr(
                "title", "Location: " + v.u_location
            );
            $('.primary-legislation', clone).html(v.p_leg);
            if (v.c_status == 1) {
                $('.compliance-applicable i', clone).addClass("text-info");
                $('.compliance-not-applicable i', clone).addClass(
                    "text-muted"
                );
                $('.compliance-do-not-show i', clone).addClass("text-muted");
            } else if (v.c_status == 2) {
                $('.compliance-applicable i', clone).addClass("text-muted");
                $('.compliance-not-applicable i', clone)
                    .addClass("text-warning");
                $('.compliance-do-not-show i', clone).addClass("text-muted");
            } else if (v.c_status == 3) {
                $('.compliance-applicable i', clone).addClass("text-muted");
                $('.compliance-not-applicable i', clone).addClass(
                    "text-muted"
                );
                $('.compliance-do-not-show i', clone).addClass("text-danger");
            } else {
                $('.compliance-applicable i', clone).addClass("text-muted");
                $('.compliance-not-applicable i', clone).addClass(
                    "text-muted"
                );
                $('.compliance-do-not-show i', clone).addClass("text-muted");
            }
            if (v.s_status == 1) {
                $('.statutory-applicable i', clone).addClass("text-info");
                $('.statutory-not-applicable i', clone).addClass("text-muted");
                $('.statutory-do-not-show i', clone).addClass("text-muted");
            } else if (v.s_status == 2) {
                $('.statutory-applicable i', clone).addClass("text-muted");
                $('.statutory-not-applicable i', clone)
                    .addClass("text-warning");
                $('.statutory-do-not-show i', clone).addClass("text-muted");
            } else if (v.s_status == 3) {
                $('.statutory-applicable i', clone).addClass("text-muted");
                $('.statutory-not-applicable i', clone).addClass("text-muted");
                $('.statutory-do-not-show i', clone).addClass("text-danger");
            } else {
                $('.statutory-applicable i', clone).addClass("text-muted");
                $('.statutory-not-applicable i', clone).addClass("text-muted");
                $('.statutory-do-not-show i', clone).addClass("text-muted");
            }
            if (v.s_remarks != "") {
                $('.statutory-remarks', clone).html(v.s_remarks);
            }
            $('.secondary-legislation', clone).html(v.s_leg);
            $('.statutory-provision', clone).html(v.s_prov);
            $('.compliance-task-name span', clone).html(v.c_task);
            $('.compliance-task-name i', clone)
                .attr("title", "Organization: " + v.org_names.join());
            $('.compliance-description', clone).html(v.c_desc);
            DETAILS_TBODY.append(clone);
        });
        checkAllEnableDisable();
        PAGINATION_VIEW.show();
        if(showFrom == undefined) showFrom = 1;
        showPagePan(showFrom, SNO, TOTAL_RECORD);
    } else {
        PAGINATION_VIEW.hide();
        hideLoader();
        clone = $('#template #record_not_found tr').clone();
        $('.no-records', clone).attr("colspan", "18");
        DETAILS_TBODY.append(clone);
        hidePagePan();
    }
};

// Single approve to click check box
singleApprove = function(id) {
    if ($('#approve' + id).prop("checked") == true) {
        $('#reject' + id).removeAttr("checked");
        $('#rejected_reason' + id + ' i').remove();
        tempAction(id, 1);
        checkAllEnableDisable();
    } else {
        tempAction(id, 0);
        checkAllEnableDisable();
    }
}

// Single Reject to click check box
singleReject = function(id, flag) {
    if ($('#reject' + id).prop("checked") == true) {
        if (CHECK_ALL_REJECT.prop("checked") == false) {
            if (flag == false) {
                SINGLE_REJECT_ID.val(id);
                confirmationAction(0, 'single-reject');
            } else {
                $('#approve' + id).removeAttr("checked");
                $('#rejected_reason' + id).html(
                    '<i class="fa fa-info-circle ' +
                    ' fa-1-2x l-h-51 text-primary c-pointer" ' +
                    'data-toggle="tooltip" data-original-title=' +
                    '"' + SINGLE_REJECT_REASON.val() + '"></i>'
                );
                tempAction(id, 2);
                checkAllEnableDisable();
            }
        } else {
            $('#approve' + id).removeAttr("checked");
            $('#rejected_reason' + id)
            .html(
                '<i data-toggle="tooltip" class="fa fa-info-circle fa-1-2x ' +
                'l-h-51 text-primary c-pointer" ' + 
                'data-original-title="' + SINGLE_REJECT_REASON.val() + '" ' +
                '></i>'
            );
            tempAction(id, 2);
            CHECK_ALL_APPROVE.removeAttr("checked");
        }
    } else {
        tempAction(id, 0);
        checkAllEnableDisable();
        $('#rejected_reason' + id + ' i').remove();
    }
}

// To update approve & reject to sent server
tempAction = function(id, action) {
    console.log(id);
    var csvid = ASID.val();
    var reason = SINGLE_REJECT_REASON.val();
    displayLoader();
    bu.updateAssignStatutoryActionFromView(parseInt(csvid), parseInt(id),
        parseInt(action), reason,
        function(error, response) {
            if (error == null) {
                hideLoader();
            } else {
                STATUTE.failuresMessage(error);
                hideLoader();
            }
        });
}

// To validate approve all and reject all check box
checkAllEnableDisable = function(id, action) {
    var approveTotalCount = DETAILS_TBODY.find('.single-approve').length;
    var rejectTotalCount = DETAILS_TBODY.find('.single-reject').length;
    var approve = DETAILS_TBODY.find('.single-approve:checked').length;
    var reject = DETAILS_TBODY.find('.single-reject:checked').length;
    if (approve == approveTotalCount) {
        CHECK_ALL_APPROVE.prop('checked', true);
        CHECK_ALL_REJECT.removeAttr("checked");
    } else if (reject == rejectTotalCount) {
        CHECK_ALL_APPROVE.removeAttr("checked");
        CHECK_ALL_REJECT.prop('checked', true);
    } else {
        CHECK_ALL_APPROVE.removeAttr("checked");
        CHECK_ALL_REJECT.removeAttr("checked");
    }
}

// To get grid detailed view page filters value to server.
ApproveAssignStatutoryBU.prototype.loadFilterPage = function(id) {
    statute = this;
    displayLoader();
    bu.getAssignStatutoryFilters(parseInt(id), function(error, response) {
        if (error == null) {
            statute.filterDomain = response.d_names;
            statute.filterUnits = response.u_names;
            statute.filterPrimaryLegislation = response.p_legis;
            statute.filterSecondaryLegislation = response.s_legis;
            statute.filterStatutoryProvision = response.s_provs;
            statute.filterComplianceTask = response.c_tasks;
            statute.filterComplianceDescription = response.c_descs;
            statute.displayFilterList();
            hideLoader();
        } else {
            statute.failuresMessage(error);
            hideLoader();
        }
    });
};

// To load the grid detailed view page filters.
ApproveAssignStatutoryBU.prototype.displayFilterList = function() {
    statute = this;
    if (statute.filterDomain.length > 0 && DOMAIN.val() == null) {
        DOMAIN.find("option").remove();
        $.each(statute.filterDomain, function(k, v) {
            DOMAIN.append('<option value="' + v + '">' + v + '</option>');
        });
        DOMAIN.multiselect();
    }
    if (statute.filterUnits.length > 0 && UNIT.val() == null) {
        UNIT.find("option").remove();
        $.each(statute.filterUnits, function(k, v) {
            var unitCode = v.split("-")[0].trim();
            UNIT.append('<option value="' + unitCode + '">' + v + '</option>');
        });
        UNIT.multiselect();
    }
    if (statute.filterPrimaryLegislation.length > 0 &&
        PRIMARY_LEGISLATION.val() == null) {
        PRIMARY_LEGISLATION.find("option").remove();
        $.each(statute.filterPrimaryLegislation, function(k, v) {
            var str = '<option value="' + v + '">' + v + '</option>';
            PRIMARY_LEGISLATION.append(str);
        });
        PRIMARY_LEGISLATION.multiselect();
    }
    if (statute.filterStatutoryStatus.length > 0 &&
        STATUTORY_STATUS.val() == "") {
        $.each(statute.filterStatutoryStatus, function(k, v) {
            STATUTORY_STATUS
                .append('<option value="' + v + '">' + v + '</option>');
        });
        STATUTORY_STATUS.multiselect();
    }
    if (statute.filterComplianceStatus.length > 0 &&
        COMPLIANCE_STATUS.val() == "") {
        $.each(statute.filterComplianceStatus, function(k, v) {
            COMPLIANCE_STATUS
                .append('<option value="' + v + '">' + v + '</option>');
        });
        COMPLIANCE_STATUS.multiselect();
    }
}

// To get filter values pass and get value to server
ApproveAssignStatutoryBU.prototype.loadDetailsPageWithFilter = function(
    id, vData, dNames, uNames, pLeg, sLeg,
    sPro, cTask, sStatus, cStatus, cDes) {
    statute = this;
    if (dNames != null)
        dNames = dNames.join();
    if (uNames != null)
        uNames = uNames.join();
    if (pLeg != null){
        for(var i=0;i<pLeg.length;i++){
            pLeg[i] = pLeg[i].replace(',', '|')
        }
        pLeg = pLeg.join();
    }
    if (sLeg == "")
        sLeg = null;
    if (sPro == "")
        sPro = null;
    if (cTask == "")
        cTask = null;
    if (cDes == "")
        cDes = null;
    if (sStatus == "")
        sStatus = null;
    else
        sStatus = parseInt(sStatus);
    if (cStatus == "")
        cStatus = null;
    else
        cStatus = parseInt(cStatus);
    if (vData == "")
        vData = null;
    else
        vData = parseInt(vData);
    displayLoader();
    bu.getViewAssignStatutoryDataFromFilter(parseInt(id), parseInt(SNO),
        parseInt(PAGE_LIMIT), dNames, uNames, pLeg, sLeg, sPro, cTask,
        cDes, vData, sStatus, cStatus,
        function(error, response) {
            CLIENT_GROUP_NAME.html(response.cl_name);
            LEGAL_ENTITY_NAME.html(response.le_name);
            COUNTRY_NAME.html(response.c_name);
            UPLOADED_FILE_NAME.html(response.csv_name);
            UPLOADED_ON.html(response.uploaded_on);
            var j;
            for (j = 0; j < statute.userList.length; j++) {
                if (response.uploaded_by == statute.userList[j].user_id) {
                    UPLOADED_BY.html(statute.userList[j].emp_code_name);
                }
            }
            if (error == null) {
                statute.dataListDetails = response.assign_statutory_data_list;
                TOTAL_RECORD = response.count;
                if (SNO == 0 && TOTAL_RECORD > 0)
                    createPageView(TOTAL_RECORD);
                statute.displayDetailsPage(statute.dataListDetails, false);
                ASID.val(id);
                hideLoader();
            } else {
                statute.failuresMessage(error);
                hideLoader();
            }
        });
};

// Pagination Show values display
showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' +
        showTo + ' of ' + total + ' entries ';
    SHOW_COUNT.text(showText);
    PAGINATION_VIEW.show();
};

// Pagination hide values display
hidePagePan = function() {
    SHOW_COUNT.text('');
    PAGINATION_VIEW.hide();
}

// To create pagination no of page list
createPageView = function(total_records) {
    PER_PAGE = parseInt(ITEMS_PER_PAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');
    PAGINATION.twbsPagination({
        totalPages: Math.ceil(total_records / PER_PAGE),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(CURRENT_PAGE) != cPage) {
                CURRENT_PAGE = cPage;
                viewListDetailsPage(ASID.val());
            }
        }
    });
};

// To validate and send action status server using submit button action
ApproveAssignStatutoryBU.prototype.submitProcess = function() {
    var password = SUBMIT_PASSWORD.val();
    var csvid = ASID.val();
    var clId = CLIENT_GROUP_ID.val();
    var leId = LEGAL_ENTITY_ID.val();
    if (password.length == 0) {
        displayMessage(message.password_required);
        SUBMIT_PASSWORD.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }

    displayLoader();
    bu.validateAssignStatutory(parseInt(csvid), function(error, response) {
        if (response.un_saved_count > 0) {
            displayMessage(message.un_saved_compliance);
            hideLoader();
        } else {
            bu.submitAssignStatutoryAction(parseInt(csvid), parseInt(clId),
                parseInt(leId), password,
                function(error, response) {
                    if (error == null) {
                        hideLoader();
                        Custombox.close();
                        var dispMsg = message.assign_statutory_submit_success;
                        if (response.hasOwnProperty("rej_count")) {
                            setTimeout(function() {
                                var msg = response.rej_count + ' ' + 
                                    message.sys_rejected_confirm;
                                confirm_alert(msg, function(isConfirm) {
                                    if (isConfirm) {
                                        displayLoader();
                                        bu.confirmAssignStatutoryUpdateAction(
                                            parseInt(csvid),
                                            parseInt(clId), parseInt(leId),
                                            function(error, res3) {
                                                if (error == null) {
                                                    displaySuccessMessage(
                                                        dispMsg
                                                    );
                                                    STATUTE.pageLoad();
                                                } else {
                                                    STATUTE.failuresMessage(
                                                        error
                                                    );
                                                    hideLoader();
                                                }
                                            });
                                    }
                                });
                            }, 500);
                        } else {
                            displaySuccessMessage(
                                message.assign_statutory_submit_success
                            );
                            STATUTE.pageLoad();
                        }
                    } else {
                        statute.failuresMessage(error);
                        hideLoader();
                    }
                });
        }
    });
}

// Create class
STATUTE = new ApproveAssignStatutoryBU();

// To start ready function
$(document).ready(function() {
    STATUTE.pageLoad();
    PageControls();
    bulkLoadItemsPerPage();
    $(".nicescroll").niceScroll();
});