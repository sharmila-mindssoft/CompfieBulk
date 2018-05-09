// control initialize
var LIST_CONTAINER = $('.tbody-sm-approve-list1');
var LIST_ROW_TEMPLATE = $('#templates .table-sm-csv-info .table-row');
var LIST_SCREEN = $("#sm-approve-list");
var VIEW_SCREEN = $("#sm-approve-view");
var SHOW_BUTTON = $("#btn-list-show");
var GO_BUTTON = $("#go");
var PASSWORD_SUBMIT_BUTTON = $('.password-submit');
var CANCEL_BUTTON = $("#btn-sm-view-cancel");
var VIEW_LIST_CONTAINER = $('.tbody-sm-approve-view');
var VIEW_LIST_ROW_TEMPLATE = $('#templates .table-sm-approve-info tr');
var FINAL_SUBMIT = $('#btn-final-submit');
var FILTERED_DATA = $('.filtered-data');
var CLEAR_FILTERED = $(".clear-filtered");

var ITEMS_PER_PAGE = $('#items_per_page');
var PAGINATION_VIEW = $('.pagination-view');
var STATU_TOTALS;
var j = 1;
var PAGE_TYPE = "show";
var CURRENT_PASSWORD = null;
var BU_APPROVE_PAGE = null;
var IS_AUTHENTICATE = '';

// auto complete - country
var COUNTRY_VAL = $('#countryid');
var COUNTRY_AC = $("#countryname");
var AC_COUNTRY = $('#ac-country');

// auto complete - domain
var DOMAIN_VAL = $('#domainid');
var DOMAIN_AC = $("#domainname");
var AC_DOMAIN = $('#ac-domain')

// auto complete - user
var USER_VAL = $('#userid');
var USER_AC = $("#username");
var AC_USER = $('#ac-user');

var SEARCH_FILENAME = $('.search-file-name');
var SEARCH_UPLOAD_BY = $('.search-upload-by');
var SEARCH_TOT_RECORDS = $('.search-tot-records');
var SEARCH_UPLOAD_ON = $('.search-upload-on');

var SEARCH_STATUTORY = $('#search-statutory');
var SEARCH_ORGANIZATION = $('#search-organization');
var SEARCH_NATURE = $('#search-nature');
var SEARCH_PROVISION = $('#search-provision');
var SEARCH_CTASK = $('#search-c-task');
var SEARCH_CDOC = $('#search-c-doc');
var SEARCH_TASK_ID = $('#search-task-id');
var SEARCH_CDESC = $('#search-c-desc');
var SEARCH_PCONS = $('#search-p-cons');
var SEARCH_TASK_TYPE = $('#search-task-type');
var SEARCH_REFER_LINK = $('#search-refer-link');
var SEARCH_FREQ = $('#search-frequency');
var SEARCH_FORMAT = $('#search-format');
var SEARCH_GEOGRAPHY = $('#search-geo');

// filter controls

var ORG_NAME = $('#orgname');
var AC_ORG = $('#ac-orgname');
var NATURE = $('#nature');
var AC_NATURE = $('#ac-nature');
var STATUTORY = $('#statutory');
var AC_STATUTORY = $('#ac-statutory');
var GEOLOCATION = $('#geolocation');
var AC_GEO_LOCATION = $('#ac-geolocation');
var COMPTASK = $('#comptask');
var AC_COMPTASK = $('#ac-comptask');
var TASK_ID = $('#taskid');
var AC_TASK_ID = $('#ac-taskid');
var COMP_DOC = $('#compdoc');
var AC_COMP_DOC = $('#ac-compdoc');
var COMP_DESC = $('#compdesc');
var AC_COMP_DESC = $('#ac-compdesc');
var TASK_TYPE = $('#tasktype');
var AC_TASK_TYPE = $('#ac-tasktype');
var AC_VIEW_DATA = $('.view-data');
var MULTI_SELECT_FREQUENCY = $('#frequency');

var APPROVE_SELECT_ALL = $(".approve-all");
var REJECT_SELECT_ALL = $(".reject-all");
var CURRENT_PAGE_SMID = [];

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function onAutoCompleteSuccess(valueElement, idElement, val) {
    var primaryKey = '';
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    primaryKey = idElement[0].id;
    if(primaryKey == 'countryid') {
      DOMAIN_AC.val('');
      DOMAIN_VAL.val('');
      USER_AC.val('');
      USER_VAL.val('');
    }
}
function resetFilter(evt) {
    if (evt == "country") {
        DOMAIN_AC.val('');
        DOMAIN_VAL.val('');
        USER_VAL.val('');
        USER_AC.val('');
    }
    if (evt == "domain") {
        USER_VAL.val('');
        USER_AC.val('');
    }
    LIST_CONTAINER.empty();
}

function displayPopUp(TYPE, csvId, smId, callback) {
    var targetId ='';
    if (TYPE == "reject") {
        targetId = "#custom-modal";
        CURRENT_PASSWORD = $('#current-password-reject');
        $('.reject-reason-txt').val('')
    }
    else if (TYPE == "view-reject") {
        targetId = "#custom-modal-remarks";
        CURRENT_PASSWORD = null;
        $('.view-reason').val('');
    }
    else {
        targetId = "#custom-modal-approve"
        CURRENT_PASSWORD = $('#current-password');
    }
    Custombox.open({
        target: targetId,
        effect: 'contentscale',
        complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            IS_AUTHENTICATE = false;
        },
        close: function() {
            if (IS_AUTHENTICATE) {
                displayLoader();
                setTimeout(function() {
                    if (TYPE == "approve") {
                        csvId["TYPE"] = "approve";
                        BU_APPROVE_PAGE.actionFromList(
                            csvId, 1, null, CURRENT_PASSWORD.val()
                        );
                    }
                    else if (TYPE == "reject") {
                        if ($('.reject-reason-txt').val() == '') {
                            displayMessage(message.reason_required)
                        }
                        else {
                            BU_APPROVE_PAGE.actionFromList(
                                csvId, 2, $('.reject-reason-txt').val(),
                                CURRENT_PASSWORD.val()
                            );
                        }
                    }
                    else if (TYPE == "submit") {
                        BU_APPROVE_PAGE.finalSubmit(
                            csvId, CURRENT_PASSWORD.val()
                        );
                    }
                    else if (TYPE == "view-reject") {
                        if ($('.view-reason').val()== '') {
                            displayMessage(message.reason_required)
                        }
                        else {
                            bu.updateActionFromView(
                                csvId, smId, 2, $('.view-reason').val(),
                                function(err, res) {
                                    if (err != null) {
                                        tThis.possibleFailures(err);
                                    }
                                    hideLoader();
                            });
                            callback($('.view-reason').val());
                        }
                    }
                }, 500);
            }
        },
    });
}

function displayViewRejectAllPopUp(callback) {
    targetId = "#custom-modal-remarks";
    CURRENT_PASSWORD = null;
    $('.view-reason').val('');

    Custombox.open({
        target: targetId,
        effect: 'contentscale',
        complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            IS_AUTHENTICATE = false;
        },
        close: function() {
            if (IS_AUTHENTICATE) {
                displayLoader();
                setTimeout(function() {
                    if ($('.view-reason').val() == '') {
                        displayMessage(message.reason_required)
                    }
                    else {
                        callback($('.view-reason').val());
                    }

                }, 500);
            }
        },
    });
}

function validateAuthentication() {
    var password = CURRENT_PASSWORD.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASSWORD.focus();
        return false;
    }else if(isLengthMinMax(
        CURRENT_PASSWORD, 1, 20, message.password_20_exists) == false
    ) {
        return false;
    } else {
        IS_AUTHENTICATE = true;
        Custombox.close();
    }
    displayLoader();
}


function ApproveBulkMapping() {
    this.countryList = [];
    this.domainList = [];
    this.userList = [];
    this.approveDataList = [];
    this.viewDataList = [];
    this.orgNames = [];
    this.natures = [];
    this.statutories = [];
    this.frequency = [];
    this.geoLocation = [];
    this.compTasks = [];
    this.compDescs = [];
    this.compDocs = [];
    this.taskId = [];
    this.taskType = [];
    this.CSVID = null;
    this.showMapCount = 0;
    this.countryId = null;
    this.domainId = null;
}
ApproveBulkMapping.prototype.possibleFailures = function(error) {
    displayMessage(error);
    hideLoader();
};
ApproveBulkMapping.prototype.showList = function() {
    LIST_SCREEN.show();
    VIEW_SCREEN.hide();
    SEARCH_FILENAME.val('');
    SEARCH_UPLOAD_BY.val('');
    SEARCH_TOT_RECORDS.val('');
    SEARCH_UPLOAD_ON.val('');
    this.fetchDropDownData();

};
ApproveBulkMapping.prototype.fetchListData = function() {
    var i = 0;
    tThis = this;
    displayLoader();
    cId = parseInt(COUNTRY_VAL.val());
    dId = parseInt(DOMAIN_VAL.val());
    uId = parseInt(USER_VAL.val());
    bu.getApproveMappingCSVList(cId, dId, uId, function(error, response) {
        if (error == null) {
            tThis.approveDataList = response.pending_csv_list;
            $.each(tThis.approveDataList, function(idx, data) {
                uploadedName = null;
                for (i=0; i<tThis.userList.length; i++) {
                    if (data.uploaded_by == tThis.userList[i].user_id) {
                        uploadedName = tThis.userList[i].emp_code_name
                        break;
                    }
                    else {
                        uploadedName = '';
                    }
                }
                if (uploadedName != null) {
                    data.uploaded_by = uploadedName;
                }
            });
            tThis.renderList(tThis.approveDataList);
            hideLoader();
        }
        else{
            hideLoader();
            tThis.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.renderList = function(listData) {
    var j = 1;
    var tr = '', clone4 = '', cloneRow = '';
    var approveRejCount = {};
    tThis = this;    
    LIST_CONTAINER.find('tr').remove();
    if(listData.length == 0) {
        LIST_CONTAINER.empty();
        tr = $('#no-record-templates .table-no-content .table-row-no-content');
        clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        LIST_CONTAINER.append(clone4);
    }
    else {
        $.each(listData, function(idx, data) {
            cloneRow = LIST_ROW_TEMPLATE.clone();
            cNameSplit = data.csv_name.split("_");
            cNameSplit.pop();
            cName = cNameSplit.join("_");
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cName);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(data.uploaded_by);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(
                data.approve_count + ' / ' + data.rej_count
            );
            $('.approve-checkbox', cloneRow).on('change', function(e) {
                if (e.target.checked) {
                    if(data.rej_count > 0) {
                        approveRejCount['approve_count'] = data.approve_count;
                        approveRejCount['rej_count'] = data.rej_count;
                        approveRejCount['csv_id'] = data.csv_id;
                        displayPopUp('approve', approveRejCount, null);
                    }
                    else{
                        displayPopUp('approve', data.csv_id, null);
                    }
                }
            });
            $('.reject-checkbox', cloneRow).on('change', function(e) {
                if(e.target.checked) {
                    displayPopUp('reject', data.csv_id, null);
                }
            });
            fileName = data.csv_name.split('.')
            fileName = fileName[0]

            $('.dropbtn',cloneRow).on('click', function() {
                if($(".dropdown-content", cloneRow).hasClass("show")==false) {
                    $(".dropdown-content", cloneRow).show();
                    $(".dropdown-content", cloneRow).addClass("show");
                }
                else{
                    $(".dropdown-content", cloneRow).hide();
                    $(".dropdown-content", cloneRow).removeClass("show");
                }
            });

            $(".dl-xls-file, .dl-csv-file, .dl-ods-file,"+
                " .dl-txt-file", cloneRow).on("click", function() {
                $(".dropdown-content", cloneRow).hide();
                $(".dropdown-content", cloneRow).removeClass("show");
            });

            $('.dl-xls-file',cloneRow).attr(
                "href", "/uploaded_file/xlsx/"+fileName+'.xlsx'
            );
            $('.dl-csv-file',cloneRow).attr(
                "href", "/uploaded_file/csv/"+fileName+'.csv'
            );
            $('.dl-ods-file',cloneRow).attr(
                "href", "/uploaded_file/ods/"+fileName+ '.ods'
            );
            $('.dl-txt-file',cloneRow).attr(
                "href", "/uploaded_file/txt/"+fileName+'.txt'
            );
            if(data.approve_count > 0 || data.rej_count > 0 
                || data.declined_count > 0) {

                $('.bu-view-mapping', cloneRow).hide();
                $('.editbtn', cloneRow).show();
                $('.editbtn', cloneRow).on('click', function() {
                    tThis.CSVID = data.csv_id;
                    tThis.countryId = data.c_id;
                    tThis.domainId = data.d_id;
                    pageLimit = parseInt(ITEMS_PER_PAGE.val());
                    tThis.showViewScreen(data.csv_id, 0, pageLimit);
                });

            } else {
                $('.bu-view-mapping', cloneRow).show();
                $('.editbtn', cloneRow).hide();
                $('.bu-view-mapping', cloneRow).on('click', function() {
                    tThis.CSVID = data.csv_id;
                    tThis.countryId = data.c_id;
                    tThis.domainId = data.d_id;
                    pageLimit = parseInt(ITEMS_PER_PAGE.val());
                    tThis.showViewScreen(data.csv_id, 0, pageLimit);
                });
            }
            LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};
ApproveBulkMapping.prototype.fetchDropDownData = function() {
    tThis = this;
    displayLoader();
    bu.getDomainList(function (error, response) {
        if (error == null) {
            tThis.domainList = response.bsm_domains;
            tThis.countryList = response.bsm_countries
            bu.getKnowledgeUserInfo(function (err, resp) {
                if (err == null) {
                    tThis.userList = resp.k_executive_info;
                    hideLoader();
                }
                else {
                    hideLoader();
                    tThis.possibleFailures(err);
                }
            });

        }
        else{
            hideLoader();
            tThis.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.confirmAction = function() {
    tThis = this;
    displayLoader();
    console.log("confirm action called")
    bu.confirmUpdateAction(
        tThis.CSVID, tThis.countryId, tThis.domainId,
        function(error, response) {
        if (error == null) {
            tThis.showList();
            tThis.fetchListData();
            displaySuccessMessage(message.confirm_success);
        }
        else {
            BU_APPROVE_PAGE.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.actionFromList = function(
    csvId, action, remarks, pwd
) {
    var showPopup = false;;
    displayLoader();
    tThis = this;
    tThis.countryId = parseInt(COUNTRY_VAL.val());
    tThis.domainId = parseInt(DOMAIN_VAL.val());

    if(typeof csvId != "number") {
        if(csvId["TYPE"].length > 0 && csvId["TYPE"] == "approve") {
            if(csvId["rej_count"] > 0) {
                tThis.CSVID = csvId["csv_id"];
                csvId = tThis.CSVID;
                swal({
                    title: "Are you sure",
                    text: "Some manual rejections are inside, "+
                          "Do you want to continue?",
                    type: "success",
                    showCancelButton: true,
                    confirmButtonClass: 'btn-success waves-effect waves-light',
                    confirmButtonText: 'Yes'
                }, function(isConfirm) {
                    if (isConfirm) {
                            bu.updateActionFromList(
                                csvId, action, remarks, pwd, COUNTRY_VAL.val(),
                                DOMAIN_VAL.val(),
                                function(error, response) {
                                    if (error == null) {
                                        if (response.rej_count > 0) {
                                            msg = response.rej_count
                                            + " compliance declined, "
                                            +"Do you want to continue ?";
                                            confirm_alert(msg, 
                                                function(isConfirm) {
                                                if (isConfirm) {
                                                    tThis.confirmAction();
                                                }
                                                else {
                                                    hideLoader();
                                                }
                                            });
                                        }else {
                                            if (action == 1) {
                                                displaySuccessMessage(
                                                    message.approve_success
                                                );
                                            }
                                            else {
                                                displaySuccessMessage(
                                                    message.reject_success
                                                );
                                            }
                                            tThis.fetchListData()
                                        }
                                    }
                                    else {
                                        hideLoader();
                                        tThis.possibleFailures(error);
                                    }
                                }
                                );
                        }
                        else {
                            hideLoader();
                            return false;
                        }
                    })
            }
        }
    }
    else {
        tThis.CSVID = csvId;
        bu.updateActionFromList(
        csvId, action, remarks, pwd, COUNTRY_VAL.val(),
        DOMAIN_VAL.val(),
        function(error, response) {
            if (error == null) {
                if (response.rej_count > 0) {
                    msg = response.rej_count
                    + " compliance declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            tThis.confirmAction();
                        }
                        else {
                            hideLoader();
                        }
                    });
                }
                else {
                    if (action == 1) {
                        displaySuccessMessage(message.approve_success);
                    }
                    else {
                        displaySuccessMessage(message.reject_success);
                    }
                    tThis.fetchListData()
                }
            }
            else {
                hideLoader();
                tThis.possibleFailures(error);
            }
        }
        );
    }
};
ApproveBulkMapping.prototype.showViewScreen = function(
    csvId, fCount, rRange
) {
    LIST_SCREEN.hide();
    VIEW_SCREEN.show();

    SEARCH_STATUTORY.val('');
    SEARCH_ORGANIZATION.val('');
    SEARCH_NATURE.val('');
    SEARCH_PROVISION.val('');
    SEARCH_CTASK.val('');
    SEARCH_CDOC.val('');
    SEARCH_TASK_ID.val('');
    SEARCH_CDESC.val('');
    SEARCH_PCONS.val('');
    SEARCH_TASK_TYPE.val('');
    SEARCH_REFER_LINK.val('');
    SEARCH_FREQ.val('');
    SEARCH_FORMAT.val('');
    SEARCH_GEOGRAPHY.val('');

    ORG_NAME.val('');
    NATURE.val('');
    STATUTORY.val('');
    GEOLOCATION.val('');
    COMPTASK.val('');
    TASK_ID.val('');
    COMP_DOC.val('');
    COMP_DESC.val('');
    TASK_TYPE.val('');
    MULTI_SELECT_FREQUENCY.val('');
    MULTI_SELECT_FREQUENCY.multiselect('rebuild');

    $('input[id="verified-data"]').removeAttr("checked");
    $('input[id="pending-data"]').removeAttr("checked");
    $('input[id="all-data"]').prop("checked", true);

    CLEAR_FILTERED.hide();
    FILTERED_DATA.empty();

    onCurrentPage = 1;
    j = 1;
    $('.filtered-data').text('');
    BU_APPROVE_PAGE.showMapCount = 0;
    BU_APPROVE_PAGE.fetchViewData(csvId, fCount, rRange);
};
ApproveBulkMapping.prototype.fetchViewData = function(
    csvId, fCount, rRange
) {
    var i = 0;
    tThis = this;
    displayLoader();
    bu.getApproveMappingView(csvId, fCount, rRange, function(
        error, response
    ) {
        if(error == null) {
            tThis.viewDataList = response.mapping_data;
            if (tThis.viewDataList.length > 0) {

                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploadedName = null
                for (i=0; i<tThis.userList.length; i++) {
                    if (response.uploaded_by == tThis.userList[i].user_id) {
                        uploadedName = tThis.userList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploadedName);
                $('.view-uploaded-on').text(response.uploaded_on);
                cNameSplit = response.csv_name.split("_");
                cNameSplit.pop();
                cName = cNameSplit.join("_");
                $('.view-csv-name').text(cName);
                $('#view-csv-id').val(response.csv_id);
                STATU_TOTALS  = response.total;
                if(tThis.viewDataList.length == 0) {
                    _tThis.hidePagePan();
                    PAGINATION_VIEW.hide();
                    tThis.hidePageView();
                }
                else {
                    if (onCurrentPage == 1) {
                        tThis.createPageView();
                        PAGINATION_VIEW.show();
                    }
                    PAGE_TYPE = "show";

                }
            }
            tThis.renderViewScreen(tThis.viewDataList);
            hideLoader();
        }
    });

};
ApproveBulkMapping.prototype.renderViewScreen = function(viewData) {
    var tr = '', clone4 = '', formatDownloadUrl = '';
    var isChecked = '', actionStatus = '', cloneRow = '';
    tThis = this;
    showFrom = tThis.showMapCount;
    showFrom += 1;

    VIEW_LIST_CONTAINER.find('tr').remove();
    if(viewData.length == 0) {
        VIEW_LIST_CONTAINER.empty();
        tr = $('#no-record-templates .table-no-content .table-row-no-content');
        clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        VIEW_LIST_CONTAINER.append(clone4);
        hideLoader();
    }
    else {
        $.each(viewData, function(idx, data) {

            formatDownloadUrl = "/uploadedformat/" +
                $('#view-csv-id').val() + "/" + data.format_file;

            cloneRow = VIEW_LIST_ROW_TEMPLATE.clone();
            $('.sno', cloneRow).text(j);
            $('.statutory', cloneRow).text(data.statutory);
            $('.organization', cloneRow).text(data.orga_name);
            $('.nature', cloneRow).text(data.s_nature);
            $('.provision', cloneRow).text(data.s_provision);
            $('.task', cloneRow).text(data.c_task_name);
            $('.doc-name', cloneRow).text(data.c_doc);
            $('.task-id', cloneRow).text(data.task_id);
            $('.task-type', cloneRow).text(data.task_type);
            $('.refer-link', cloneRow).text(data.refer);
            $('.freq', cloneRow).text(data.frequency);
            $('.statu-month', cloneRow).text(data.statu_month);
            $('.statu-date', cloneRow).text(data.statu_date);
            $('.trigger-before', cloneRow).text(data.trigger_before);
            $('.repeats-every', cloneRow).text(data.r_every);
            $('.repeats-type', cloneRow).text(data.r_type);
            $('.duration', cloneRow).text(data.dur);
            $('.duration-type', cloneRow).text(data.dur_type);
            $('.multiple', cloneRow).text(data.multiple_input);
            $('.format a', cloneRow).text(data.format_file).attr(
                "href", formatDownloadUrl
            );
            $('.geography', cloneRow).text(data.geo_location);
            $('.comp-desc', cloneRow).text(data.c_desc);
            $('.penal', cloneRow).text(data.p_cons);
            if (parseInt(data.bu_action) == 1) {
                $('.view-approve-check',cloneRow).attr("checked", true);
                $('.view-reject-check',cloneRow).attr("checked", false);
            }
            else if (data.bu_action == null) {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", false);
            }
            else if (data.bu_action == 2) {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", true);
                if(parseInt(data.bu_action)==2 && data.bu_remarks != null) {
                    $('.reject-reason .fa-info-circle',cloneRow).
                    removeClass("default-display-none");
                    $('.reject-reason .fa-info-circle',cloneRow).
                    attr("data-original-title", data.bu_remarks);
                }
                else {
                    $('.reject-reason .fa-info-circle',cloneRow).
                    addClass("default-display-none");
                }

            }
            else {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", false);
                $('.reject-reason .fa-info-circle',cloneRow).each(function() {

                    $(this).addClass("default-display-none");
                });
            }

            $('.view-approve-check', cloneRow).on('change', function(e) {
                if (e.target.checked) {
                    isChecked = false;
                    actionStatus = 1;
                    $('.reject-all').attr("checked", false);
                }
                else {
                    isChecked = true;
                    actionStatus = 0;
                }
                csvId = $('#view-csv-id').val();
                bu.updateActionFromView(
                    parseInt(csvId), data.sm_id, actionStatus, null,
                    function(err, res) {
                    if (err != null) {
                        tThis.possibleFailures(err);
                    }
                    else {
                        $('.view-reject-check',cloneRow).attr(
                            "checked", isChecked
                        );
                        $('.reject-reason .fa-info-circle', cloneRow)
                        .addClass("default-display-none");
                    }
                });
            });
            $(".view-reject-check", cloneRow).on('change', function(e) {
                if(e.target.checked) {
                    csvId = $('#view-csv-id').val();
                    $('.view-approve-check',cloneRow).attr("checked", false);
                    $('.approve-all').attr("checked", false);
                    displayPopUp('view-reject', parseInt(csvId), data.sm_id,
                        function(viewReason) {
                            $('.reject-reason .fa-info-circle', cloneRow).
                            removeClass("default-display-none");
                            $('.reject-reason .fa-info-circle', cloneRow).
                            attr("data-original-title", viewReason);
                    });
                }
                else
                {
                    csvId = $('#view-csv-id').val();
                    $('.view-reject-check',cloneRow).attr("checked", false);
                    bu.updateActionFromView(
                        parseInt(csvId), data.sm_id, 0, null,
                        function(err, res) {
                        if (err != null) {
                            tThis.possibleFailures(err);
                        }
                        else{
                            $('.view-reject-check',cloneRow).attr(
                                "checked", false);

                            $('.reject-reason .fa-info-circle', cloneRow)
                            .addClass("default-display-none");

                            $('.reject-reason .fa-info-circle', cloneRow)
                            .attr("data-original-title", '');
                        }
                    });
                }

            });
            VIEW_LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
        hideLoader();
    }

    setTimeout(function() {
        $(".tbody-sm-approve-view tr").removeAttr("style");
    }, 500);

    $('.js-filtertable-action-sm').each(function() {
        $(this).filtertable().addFilter('.js-filter-sm');
    });

    tThis.showMapCount += viewData.length;
    $('[data-toggle="tooltip"]').tooltip();
    tThis.showPagePan(showFrom, tThis.showMapCount, STATU_TOTALS);
};

ApproveBulkMapping.prototype.fetchFilterDropDown = function(csvId) {
    var i = 0, str = '';
    tThis = this;
    displayLoader();
    bu.getApproveMappingViewFilter(parseInt(csvId), function(err, resp) {
        if (err == null) {
            tThis.orgNames = resp.orga_names;
            tThis.natures = resp.s_natures;
            tThis.statutories = resp.bu_statutories;
            tThis.frequency = resp.frequencies;
            tThis.geoLocation = resp.geo_locations;
            tThis.compTasks = resp.c_tasks;
            tThis.compDescs = resp.c_descs;
            tThis.compDocs = resp.c_docs;
            tThis.taskId = resp.task_ids;
            tThis.taskType = resp.task_types;
            if (tThis.frequency.length > 0) {
                str = '';
                for (i in tThis.frequency) {
                    val = tThis.frequency[i]
                    str += '<option value="'+ val +'">'+ val +'</option>';
                }
                MULTI_SELECT_FREQUENCY.html(str).multiselect('rebuild');
            }
            hideLoader();
        }
    });
};

ApproveBulkMapping.prototype.renderViewFromFilter = function() {
    var view_data = 3;
    var showCount = 0;
    var pageLimit = parseInt(ITEMS_PER_PAGE.val());
    displayLoader();
    if (onCurrentPage == 1) {
        showCount = 0;
        tThis.showMapCount = 0;
        j = 1;
        showFrom = 1;
    } else {
        showCount = (onCurrentPage - 1) * pageLimit;
        tThis.showMapCount = showCount;
    }
    fTypes = [];
    $("#frequency option:selected").each(function () {
       var $this = $(this);
       if ($this.length) {
        fTypes.push($this.text());
       }
    });
    if ($('input[id="verified-data"]:checked').length == 1)
        view_data = 1;

    if ($('input[id="pending-data"]:checked').length == 1)
        view_data = 2;
    if ($('input[id="all-data"]:checked').length == 1)
        view_data = 3;

    args = {
        "csv_id": parseInt($('#view-csv-id').val()),
        "orga_name": ORG_NAME.val(),
        "s_nature": NATURE.val(),
        "f_types": fTypes,
        "statutory": STATUTORY.val(),
        "geo_location": GEOLOCATION.val(),
        "c_task_name": COMPTASK.val(),
        "c_desc": COMP_DESC.val(),
        "c_doc": COMP_DOC.val(),
        "f_count": showCount,
        "r_range": pageLimit,
        "tsk_id": TASK_ID.val(),
        "tsk_type": TASK_TYPE.val(),
        "filter_view_data" : view_data
    }

    bu.getApproveMappingViewFromFilter(args, function(err, response) {
        var i = 0;
        displayLoader();
        if(err != null) {
            hideLoader();
            BU_APPROVE_PAGE.possibleFailures(err)
        }
        if(err == null) {
            tThis.viewDataList = response.mapping_data;
            if (tThis.viewDataList.length > 0) {
                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploadedName = null
                for (i=0; i<tThis.userList.length; i++) {
                    if (response.uploaded_by == tThis.userList[i].user_id) {
                        uploadedName = tThis.userList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploadedName);
                $('.view-uploaded-on').text(response.uploaded_on);
                cNameSplit = response.csv_name.split("_");
                cNameSplit.pop();
                cName = cNameSplit.join("_");
                $('.view-csv-name').text(cName);
                $('#view-csv-id').val(response.csv_id);
                STATU_TOTALS  = response.total;
                if(tThis.viewDataList.length == 0) {
                    _tThis.hidePagePan();
                    PAGINATION_VIEW.hide();
                    tThis.hidePageView();
                }
                else {
                    PAGE_TYPE = "filter";
                    if (onCurrentPage == 1) {
                        tThis.createPageView();
                        PAGINATION_VIEW.show();
                    }

                }
            }
            tThis.renderViewScreen(tThis.viewDataList);
            hideLoader();
        }
    });
};


ApproveBulkMapping.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

ApproveBulkMapping.prototype.createPageView = function() {
    tThis = this;
    perPage = parseInt(ITEMS_PER_PAGE.val());
    tThis.hidePageView();
    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(STATU_TOTALS / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            var showCount = 0;

            cpage = parseInt(page);
            if (parseInt(onCurrentPage) != cpage) {
                onCurrentPage = cpage;
                if(PAGE_TYPE == "show") {
                    pageLimit = parseInt(ITEMS_PER_PAGE.val());
                    if (onCurrentPage == 1) {
                        showCount = 0;
                        j = 1;
                        tThis.showMapCount = 0;
                    } else {
                        showCount = (onCurrentPage - 1) * pageLimit;
                        tThis.showMapCount = showCount;
                    }
                    tThis.fetchViewData(tThis.CSVID, showCount, pageLimit);
                }
                else {
                    tThis.renderViewFromFilter();
                }
            }
            console.log(onCurrentPage);
        }
    });
};

ApproveBulkMapping.prototype.hidePagePan = function() {
    $('compliance_count').text('');
    $('.pagination-view').hide();
};

ApproveBulkMapping.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' +
    showTo + ' of ' + total + ' compliances ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};

ApproveBulkMapping.prototype.finalSubmit = function(csvId, pwd) {
    tThis = this;
    displayLoader();
    tThis.CSVID = csvId;
    tThis.countryId = parseInt(COUNTRY_VAL.val());
    tThis.domainId = parseInt(DOMAIN_VAL.val());
    bu.submitMappingAction(
        csvId, parseInt(COUNTRY_VAL.val()), parseInt(DOMAIN_VAL.val()), pwd,
        function(err, res) {
        if(err == null) {
            if (res.rej_count > 0) {
                msg = res.rej_count + " compliance declined, " 
                + "Do you want to continue ?";
                confirm_alert(msg, function(isConfirm) {
                    if (isConfirm) {
                        tThis.confirmAction();
                    }
                });
            }else {
                displaySuccessMessage(message.submit_success);
                LIST_SCREEN.show();
                VIEW_SCREEN.hide();
                SEARCH_FILENAME.val('');
                SEARCH_UPLOAD_BY.val('');
                SEARCH_TOT_RECORDS.val('');
                SEARCH_UPLOAD_ON.val('');
                tThis.fetchListData();
            }
        }
        else {
            tThis.possibleFailures(err);
        }
    });

};

function key_search(mainList) {
    var csvKey = SEARCH_FILENAME.val().toLowerCase();
    var uploadByKey = SEARCH_UPLOAD_BY.val().toLowerCase();
    var total = SEARCH_TOT_RECORDS.val();
    var uploadOnKey = SEARCH_UPLOAD_ON.val().toLowerCase();
    var csvName, uploadBy, totalRecords, uploadon;
    var fList = [];
    var entity = '';
    for (entity in mainList) {
        csvName = mainList[entity].csv_name;
        uploadBy = mainList[entity].uploaded_by;
        totalRecords = mainList[entity].no_of_records;
        uploadon = mainList[entity].uploaded_on;

        if (
            (~csvName.toLowerCase().indexOf(csvKey)) &&
            (~uploadon.toLowerCase().indexOf(uploadOnKey)) &&
            (~uploadBy.toLowerCase().indexOf(uploadByKey)) &&
            (~totalRecords.toString().indexOf(total))
        ) {
            fList.push(mainList[entity]);
        }
    }
    return fList
}
function key_view_search(mainList) {

    keyStatutory = $('#search-statutory').val().toLowerCase();
    keyOrganization = SEARCH_ORGANIZATION.val().toLowerCase();
    keyNature = SEARCH_NATURE.val().toLowerCase();
    keyProvision = SEARCH_PROVISION.val().toLowerCase();
    keyCTask = SEARCH_CTASK.val().toLowerCase();
    keyCDoc = SEARCH_CDOC.val().toLowerCase();
    keyTaskId = SEARCH_TASK_ID.val().toLowerCase();
    keyCDesc = SEARCH_CDESC.val().toLowerCase();
    keyPCons = SEARCH_PCONS.val().toLowerCase();
    keyTaskType = SEARCH_TASK_TYPE.val().toLowerCase();
    keyRefer = SEARCH_REFER_LINK.val().toLowerCase();
    keyFreq = SEARCH_FREQ.val().toLowerCase();
    keyFormat = SEARCH_FORMAT.val().toLowerCase();
    keyGeo = SEARCH_GEOGRAPHY.val().toLowerCase();
    var fList = [];
    var entity = '';
    for (entity in mainList) {
        d = mainList[entity];
        if (
            (~d.statutory.toLowerCase().indexOf(keyStatutory)) &&
            (~d.task_id.toLowerCase().indexOf(keyTaskId)) &&
            (~d.orga_name.toLowerCase().indexOf(keyOrganization)) &&
            (~d.s_nature.toLowerCase().indexOf(keyNature)) &&
            (~d.s_provision.toLowerCase().indexOf(keyProvision)) &&
            (~d.c_task_name.toLowerCase().indexOf(keyCTask)) &&
            (~d.c_doc.toLowerCase().indexOf(keyCDoc)) &&
            (~d.task_id.toLowerCase().indexOf(keyTaskId)) &&
            (~d.c_desc.toLowerCase().indexOf(keyCDesc)) &&
            (~d.p_cons.toLowerCase().indexOf(keyPCons)) &&
            (~d.task_type.toLowerCase().indexOf(keyTaskType)) &&
            (~d.refer.toLowerCase().indexOf(keyRefer)) &&
            (~d.frequency.toLowerCase().indexOf(keyFreq)) &&
            (~d.format_file.toLowerCase().indexOf(keyFormat)) &&
            (~d.geo_location.toLowerCase().indexOf(keyGeo))) {

            fList.push(mainList[entity]);
        }
    }
    j = 1;
    BU_APPROVE_PAGE.showMapCount = 0;
    return fList
}

function PageControls() {
    COUNTRY_AC.keyup(function(e) {
        var conditionFields = ["is_active"];
        var conditionValues = [true];
        var textVal = $(this).val();
        commonAutoComplete(
            e, AC_COUNTRY, COUNTRY_VAL, textVal,
            BU_APPROVE_PAGE.countryList, "country_name", "country_id",
            function (val) {
                onAutoCompleteSuccess(COUNTRY_AC, COUNTRY_VAL, val);
            }, conditionFields, conditionValues
        );
        resetFilter('country');

    });

    DOMAIN_AC.keyup(function(e) {
        var mainDomainList = BU_APPROVE_PAGE.domainList;
        var textVal = $(this).val();
        var domainList = [];
        var cIds = null;
        var checkVal = false;
        var i = 0, j = 0;
        if(COUNTRY_VAL.val() != '') {
          for(i=0;i<mainDomainList.length;i++) {
            cIds = mainDomainList[i].country_ids;

            for(j=0;j<cIds.length;j++) {
              if(cIds[j] == COUNTRY_VAL.val())
              {
                checkVal = true;
              }
            }
            if(checkVal == true && mainDomainList[i].is_active == true) {
              domainList.push({
                "domain_id": mainDomainList[i].domain_id,
                "domain_name": mainDomainList[i].domain_name
              });
              checkVal = false;
            }
          }
          commonAutoComplete(
            e, AC_DOMAIN, DOMAIN_VAL, textVal,
            domainList, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(DOMAIN_AC, DOMAIN_VAL, val);
         });
        }
        else{
          displayMessage(message.country_required);
        }
        resetFilter('domain');
    });

    USER_AC.keyup(function(e) {
        var mainUserList = BU_APPROVE_PAGE.userList;
        var textVal = $(this).val();
        var userList = [];
        var i;
        if (COUNTRY_VAL.val() != '' && DOMAIN_VAL.val() != '') {
            for (i=0; i<mainUserList.length; i++) {
                if(
                    (jQuery.inArray(
                        parseInt(COUNTRY_VAL.val()), mainUserList[i].c_ids
                        ) !== -1) &&
                    (jQuery.inArray(
                        parseInt(DOMAIN_VAL.val()), mainUserList[i].d_ids
                        ) !== -1)
                ) {
                    userList.push({
                        "emp_id": mainUserList[i].user_id,
                        "emp_name": mainUserList[i].emp_code_name
                    });
                }

            }
            commonAutoComplete(
                e, AC_USER, USER_VAL, textVal,
                userList, "emp_name", "emp_id", function (val) {
                    onAutoCompleteSuccess(USER_AC, USER_VAL, val);
            });
        }
        else {
            if (COUNTRY_VAL.val() == '') {
                displayMessage(message.country_required);
            }
            else if (DOMAIN_VAL.val() == '') {
                displayMessage(message.domain_required);
            }
        }
        resetFilter('user');
    });

    SHOW_BUTTON.click(function() {
        if (COUNTRY_VAL.val() == '') {
            displayMessage(message.country_required);
        }
        else if (DOMAIN_VAL.val() == '') {
            displayMessage(message.domain_required);
        }
        if (COUNTRY_VAL.val() != '' && DOMAIN_VAL.val() != '') {
            BU_APPROVE_PAGE.fetchListData()
        }
    });

    PASSWORD_SUBMIT_BUTTON.click(function() {
        if (CURRENT_PASSWORD != null) {
            validateAuthentication();
        }
        else {
            IS_AUTHENTICATE = true;
            Custombox.close();
            displayLoader();
        }
    });

    CANCEL_BUTTON.click(function() {
        BU_APPROVE_PAGE.showList();
        BU_APPROVE_PAGE.fetchListData();
    });

    SEARCH_FILENAME.keyup(function() {
        fList = key_search(BU_APPROVE_PAGE.approveDataList);
        BU_APPROVE_PAGE.renderList(fList);
    });

    SEARCH_TOT_RECORDS.keyup(function() {
        fList = key_search(BU_APPROVE_PAGE.approveDataList);
        BU_APPROVE_PAGE.renderList(fList);
    });

    SEARCH_UPLOAD_BY.keyup(function() {
        fList = key_search(BU_APPROVE_PAGE.approveDataList);
        BU_APPROVE_PAGE.renderList(fList);
    });
    SEARCH_UPLOAD_ON.keyup(function() {
        fList = key_search(BU_APPROVE_PAGE.approveDataList);
        BU_APPROVE_PAGE.renderList(fList);
    });

    SEARCH_STATUTORY.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_ORGANIZATION.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_NATURE.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_PROVISION.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_CTASK.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_CDOC.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_TASK_ID.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_CDESC.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_PCONS.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_TASK_TYPE.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_REFER_LINK.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_FREQ.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_FORMAT.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });
    SEARCH_GEOGRAPHY.keyup(function() {
        displayLoader();
        fList = key_view_search(BU_APPROVE_PAGE.viewDataList);
        BU_APPROVE_PAGE.renderViewScreen(fList);
    });

    // filter events

    $('.right-bar-toggle').on('click', function(e) {
      $('#wrapper').toggleClass('right-bar-enabled');
      BU_APPROVE_PAGE.fetchFilterDropDown($('#view-csv-id').val());
    });

    ORG_NAME.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_ORG, textVal,
            BU_APPROVE_PAGE.orgNames, function (val) {
                ORG_NAME.val(val[0])
            }
        );

    });

    NATURE.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_NATURE, textVal,
            BU_APPROVE_PAGE.natures, function (val) {
                NATURE.val(val[0])
            }
        );

    });

    STATUTORY.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_STATUTORY, textVal,
            BU_APPROVE_PAGE.statutories, function (val) {
                STATUTORY.val(val[0])
            }
        );

    });

    GEOLOCATION.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_GEO_LOCATION, textVal,
            BU_APPROVE_PAGE.geoLocation, function (val) {
                GEOLOCATION.val(val[0])
            }
        );

    });

    COMPTASK.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_COMPTASK, textVal,
            BU_APPROVE_PAGE.compTasks, function (val) {
                COMPTASK.val(val[0])
            }
        );
    });

    TASK_ID.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_TASK_ID, textVal,
            BU_APPROVE_PAGE.taskId, function (val) {
                TASK_ID.val(val[0])
            }
        );
    });

    COMP_DOC.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_COMP_DOC, textVal,
            BU_APPROVE_PAGE.compDocs, function (val) {
                COMP_DOC.val(val[0])
            }
        );
    });

    COMP_DESC.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_COMP_DESC, textVal,
            BU_APPROVE_PAGE.compDescs, function (val) {
                COMP_DESC.val(val[0])
            }
        );
    });


    TASK_TYPE.keyup(function(e) {
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, AC_TASK_TYPE, textVal,
            BU_APPROVE_PAGE.taskType, function (val) {
                TASK_TYPE.val(val[0])
            }
        );
    });

    GO_BUTTON.click(function() {
        var filtered = '';
        FILTERED_DATA.empty();
        CLEAR_FILTERED.hide();
        
        appendFilter = function(val) {
            if (filtered == '') {
                filtered += val;
            }
            else {
                filtered += "|" + val;
            }
        }
        if ($('input[id="verified-data"]:checked').length == 1)
        {
            verified = "View Data : Verified";
            appendFilter(verified);
        }
        if ($('input[id="pending-data"]:checked').length == 1)
        {
            pending = "View Data : Pending";
            appendFilter(pending);
        }
        if(ORG_NAME.val() != "") {
            orgs = "Organization : " + ORG_NAME.val();
            appendFilter(orgs);
        }
        if(NATURE.val() != "") {
            natures = "Statutory Nature : " + NATURE.val();
            appendFilter(natures);
        }
        if (STATUTORY.val() != "") {
            statutories = "Statutory : " + STATUTORY.val();
            appendFilter(statutories);
        }
        if(GEOLOCATION.val() != "") {
            geos = "Geography Location : " + GEOLOCATION.val();
            appendFilter(geos);
        }
        if(COMPTASK.val() != "") {
            tasks = "Compliance Task : " + COMPTASK.val();
            appendFilter(tasks);
        }
        if(TASK_ID.val() != "") {
            tid = "Task ID : " + TASK_ID.val();
            appendFilter(tid);
        }
        if(COMP_DOC.val() != "") {
            doc = "Compliance Document : " + COMP_DOC.val();
            appendFilter(doc);
        }
        if(COMP_DESC.val() != "") {
            desc = "Compliance Description : " + COMP_DESC.val();
            appendFilter(desc);
        }
        if(TASK_TYPE.val() != "") {
            tt = "Task Type : " + TASK_TYPE.val();
            appendFilter(tt);
        }
        fTypes = [];
        $("#frequency option:selected").each(function () {
           var $this = $(this);
           if ($this.length) {
            fTypes.push($this.text());
           }
        });
        if (fTypes.length != 0) {
            tt = "Frequency : " + fTypes.join(',');
            appendFilter(tt);
        }

        FILTERED_DATA.text(filtered);
        if(filtered.split("|").length >= 1)
        {
            CLEAR_FILTERED.show();
        }
        else
        {
            FILTERED_DATA.empty();
            CLEAR_FILTERED.hide();
        }
        onCurrentPage = 1;
        BU_APPROVE_PAGE.renderViewFromFilter();

    });
    CLEAR_FILTERED.click(function() {
        SEARCH_STATUTORY.val('');
        SEARCH_ORGANIZATION.val('');
        SEARCH_NATURE.val('');
        SEARCH_PROVISION.val('');
        SEARCH_CTASK.val('');
        SEARCH_CDOC.val('');
        SEARCH_TASK_ID.val('');
        SEARCH_CDESC.val('');
        SEARCH_PCONS.val('');
        SEARCH_TASK_TYPE.val('');
        SEARCH_REFER_LINK.val('');
        SEARCH_FREQ.val('');
        SEARCH_FORMAT.val('');
        SEARCH_GEOGRAPHY.val('');

        ORG_NAME.val('');
        NATURE.val('');
        STATUTORY.val('');
        GEOLOCATION.val('');
        COMPTASK.val('');
        TASK_ID.val('');
        COMP_DOC.val('');
        COMP_DESC.val('');
        TASK_TYPE.val('');
        MULTI_SELECT_FREQUENCY.val('');
        MULTI_SELECT_FREQUENCY.multiselect('rebuild');

        $('input[id="verified-data"]').removeAttr("checked");
        $('input[id="pending-data"]').removeAttr("checked");
        $('input[id="all-data"]').prop("checked", true);
        CLEAR_FILTERED.hide();
        FILTERED_DATA.empty();
        BU_APPROVE_PAGE.renderViewFromFilter();
    });

    FINAL_SUBMIT.click(function() {
        displayPopUp("submit", parseInt($('#view-csv-id').val()), null);
    });


    APPROVE_SELECT_ALL.on("change", function(e) {
        if (BU_APPROVE_PAGE.viewDataList.length > 0) {
            $(".tbody-sm-approve-view "+
            ".view-approve-check").prop('checked', false);
            $(".tbody-sm-approve-view "+
            ".view-reject-check").prop('checked', false);
            $('.reject-reason '
                +'.fa-info-circle').addClass("default-display-none");

            $('.tbody-sm-approve-view .view-approve-check').each(
                function(index, el) {
                var data = BU_APPROVE_PAGE.viewDataList[index];
                var csvId = 0;
                if (e.target.checked) {
                    $(this).prop("checked", true);
                    if (data) {
                        csvId = $('#view-csv-id').val();
                        bu.updateActionFromView(
                            parseInt(csvId), data.sm_id, 1, null,
                            function(err, res) {
                                if (err != null) {
                                    BU_APPROVE_PAGE.possibleFailures(err);
                                }
                        });
                    }
                }
                else {
                    $(this).prop("checked", false);
                }
            });

        }
    });


    REJECT_SELECT_ALL.on("change", function(e) {
        CURRENT_PAGE_SMID = [];
        if (BU_APPROVE_PAGE.viewDataList.length > 0
            && REJECT_SELECT_ALL.prop('checked') == true) {
            displayViewRejectAllPopUp(function(reason) {
                var viewReason = $('.view-reason').val();
                var i = 0;
                $(".tbody-sm-approve-view "+
                ".view-approve-check").prop('checked', false);
                $(".tbody-sm-approve-view"+
                    " .view-reject-check").prop('checked', false);

                $('.tbody-sm-approve-view .view-reject-check').each(
                    function(index, el) {
                    var data = BU_APPROVE_PAGE.viewDataList[index];
                    var csvId = 0;

                    if (e.target.checked) {
                        $(this).prop("checked", true);
                        $(".tbody-sm-approve-view th.reject-reason")
                        .find("*").removeClass("default-display-none");

                        $(".tbody-sm-approve-view th.reject-reason")
                        .find("*").attr("data-original-title", viewReason);
                        //$(".reject-reason").find(*)
                        if (data) {
                            csvId = $('#view-csv-id').val();
                            bu.updateActionFromView(
                                parseInt(csvId), data.sm_id, 2, viewReason,
                                function(err, res) {
                                    if (err != null) {
                                        BU_APPROVE_PAGE.possibleFailures(err);
                                    }
                            });
                        }
                    }
                    else {
                        $(this).find("*").prop("checked", false);
                        $(".tbody-sm-approve-view th.reject-reason")
                        .find("*").addClass("default-display-none");

                        $(".tbody-sm-approve-view th.reject-reason")
                        .find("*").attr("data-original-title","");

                        $('.tbody-sm-approve-view .view-reject-check').each(
                            function() {
                            $(this).prop("checked",false);
                        });
                    }
                    i++;
                });
                hideLoader();
            });
        }
        else {
        $(this).find("*").prop("checked", false);
        }
    });

    ITEMS_PER_PAGE.on("change", function(e) {
        pageLimit = parseInt(ITEMS_PER_PAGE.val());
        tThis.showViewScreen(tThis.CSVID, 0, pageLimit);
    });
}

BU_APPROVE_PAGE = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    BU_APPROVE_PAGE.showList();
});
$(".nicescroll").niceScroll();