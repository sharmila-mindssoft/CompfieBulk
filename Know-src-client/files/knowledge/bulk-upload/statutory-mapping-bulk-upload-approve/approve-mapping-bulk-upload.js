// control initialize
var LIST_CONTAINER = $('.tbody-sm-approve-list1');
var LIST_ROW_TEMPLATE = $('#templates .table-sm-csv-info .table-row');
var LIST_SCREEN = $("#sm_approve_list");
var VIEW_SCREEN = $("#sm_approve_view");
var SHOW_BUTTON = $("#btn_list_show");
var GO_BUTTON = $("#go");
var PASSWORD_SUBMIT_BUTTON = $('.password-submit');
var CANCEL_BUTTON = $("#btn_sm_view_cancel");
var VIEW_LIST_CONTAINER = $('.tbody-sm-approve-view');
var VIEW_LIST_ROW_TEMPLATE = $('#templates .table-sm-approve-info tr');
var FINAL_SUBMIT = $('#btn_final_submit');
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
var TIMEOUT_MLS = 5000;

// auto complete - country
var COUNTRY_VAL = $('#countryid');
var COUNTRY_AC = $("#countryname");
var AC_COUNTRY = $('#ac_country');

// auto complete - domain
var DOMAIN_VAL = $('#domainid');
var DOMAIN_AC = $("#domainname");
var AC_DOMAIN = $('#ac_domain')

// auto complete - user
var USER_VAL = $('#userid');
var USER_AC = $("#username");
var AC_USER = $('#ac_user');

var SEARCH_FILENAME = $('.search-file-name');
var SEARCH_UPLOAD_BY = $('.search-upload-by');
var SEARCH_TOT_RECORDS = $('.search-tot-records');
var SEARCH_UPLOAD_ON = $('.search-upload-on');

var SEARCH_STATUTORY = $('#search_statutory');
var SEARCH_ORGANIZATION = $('#search_organization');
var SEARCH_NATURE = $('#search_nature');
var SEARCH_PROVISION = $('#search_provision');
var SEARCH_CTASK = $('#search_c_task');
var SEARCH_CDOC = $('#search_c_doc');
var SEARCH_TASK_ID = $('#search_task_id');
var SEARCH_CDESC = $('#search_c_desc');
var SEARCH_PCONS = $('#search_p_cons');
var SEARCH_TASK_TYPE = $('#search_task_type');
var SEARCH_REFER_LINK = $('#search_refer_link');
var SEARCH_FREQ = $('#search_frequency');
var SEARCH_FORMAT = $('#search_format');
var SEARCH_GEOGRAPHY = $('#search_geo');

// filter controls

var ORG_NAME = $('#orgname');
var AC_ORG = $('#ac_orgname');
var NATURE = $('#nature');
var AC_NATURE = $('#ac_nature');
var STATUTORY = $('#statutory');
var AC_STATUTORY = $('#ac_statutory');
var GEOLOCATION = $('#geolocation');
var AC_GEO_LOCATION = $('#ac_geolocation');
var COMPTASK = $('#comptask');
var AC_COMPTASK = $('#ac_comptask');
var TASK_ID = $('#taskid');
var AC_TASK_ID = $('#ac_taskid');
var COMP_DOC = $('#compdoc');
var AC_COMP_DOC = $('#ac-compdoc');
var COMP_DESC = $('#compdesc');
var AC_COMP_DESC = $('#ac_compdesc');
var TASK_TYPE = $('#tasktype');
var AC_TASK_TYPE = $('#ac_tasktype');
var AC_VIEW_DATA = $('.view-data');
var MULTI_SELECT_FREQUENCY = $('#frequency');

var APPROVE_SELECT_ALL = $(".approve-all");
var REJECT_SELECT_ALL = $(".reject-all");
var CURRENT_PAGE_SMID = [];
var TOTAL_VIEW_ITEMS = 0;
var TOTAL_VIEW_APPROVE_ITEMS = 0;
var TOTAL_VIEW_REJECT_ITEMS = 0;
var VIEW_REJECTED_REASON = $('.view-reason').val();

var FREEZER_TABLE = $("#multi_col_freezer .table-responsive table");
var FREEZER_TBODY = $("#multi_col_freezer .table-responsive tbody");
var FREEZER_THEAD = $('#multi_col_freezer .table-responsive thead');
var FREEZER_TH = $('#multi_col_freezer .table-responsive thead tr th');

var FREEZER_TH_CHILD_1 = $('#multi_col_freezer .table-responsive thead th:nth-child(1)');
var FREEZER_TH_CHILD_2 = $('#multi_col_freezer .table-responsive thead th:nth-child(2)');
var FREEZER_TH_CHILD_3 = $('#multi_col_freezer .table-responsive thead th:nth-child(3)');
var FREEZER_TH_CHILD_4 = $('#multi_col_freezer .table-responsive thead th:nth-child(4)');
var FREEZER_TH_CHILD_5 = $('#multi_col_freezer .table-responsive thead th:nth-child(5)');
var FREEZER_TH_CHILD_6 = $('#multi_col_freezer .table-responsive thead th:nth-child(6)');

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
    var reject_reason = '';
    var viewReason = '';
    if (TYPE == "reject") {
        targetId = "#custom_modal";
        CURRENT_PASSWORD = $('#current_password_reject');
        $('.reject-reason-txt').val('')
    }
    else if (TYPE == "view-reject") {
        targetId = "#custom_modal_remarks";
        CURRENT_PASSWORD = null;
        $('.view-reason').val('');
    }
    else {
        targetId = "#custom_modal_approve"
        CURRENT_PASSWORD = $('#current_password');
    }
    Custombox.open({
        target: targetId,
        effect: 'contentscale',
        complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            else
            {
                $('.view-reason').focus();
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
                        reject_reason = $('.reject-reason-txt').val()
                        if (reject_reason == '') {
                            displayMessage(message.reason_required);
                            hideLoader();
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
                        viewReason = $('.view-reason').val()
                        if (viewReason == '') {
                            displayMessage(message.reason_required)
                            hideLoader();
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
    targetId = "#custom_modal_remarks";
    CURRENT_PASSWORD = null;
    var viewReason = '';
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
                    viewReason = $('.view-reason').val()
                    if (viewReason == '') {
                        displayMessage(message.reason_required);
                        hideLoader();
                    }
                    else {
                        callback(viewReason);
                    }

                }, 500);
            }
            else
            {
                $('.reject-all').attr("checked", false);
            }
        },
    });
}

function validateAuthentication() {
    
    var password = CURRENT_PASSWORD.val().trim();
    var rejectReason = $('.reject-reason-txt').val();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASSWORD.focus();
        return false;
    }
    else if(isLengthMinMax(
        CURRENT_PASSWORD, 1, 20, message.password_20_exists) == false
    ){
        return false;
    }
    else {
        mirror.verifyPassword(password, function(error, response) {
            if (error == null) {
                hideLoader();
                IS_AUTHENTICATE = true;
                Custombox.close();
            } else {
                hideLoader();
                if (error == 'InvalidPassword') {
                    displayMessage(message.invalid_password);
                }
            }
        });
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
    this.totRecords = null;
}
ApproveBulkMapping.prototype.possibleFailures = function(error) {

    if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    }
    else{
        displayMessage(error);    
    }
    
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
    var fileSubStats = '';
    tThis = this;    
    LIST_CONTAINER.find('tr').remove();
    if(listData.length == 0) {
        LIST_CONTAINER.empty();
        tr = $('#no_record_templates .table-no-content .table-row-no-content');
        clone4 = tr.clone();
        $('.no-records', clone4).text('No Records Found');
        LIST_CONTAINER.append(clone4);
    }
    else {
        $.each(listData, function(idx, data) {
            cloneRow = LIST_ROW_TEMPLATE.clone();
            cNameSplit = data.csv_name.split("_");
            cNameSplit.pop();
            cName = cNameSplit.join("_");

            fileSubStats = data.file_submit_status;

            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cName);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(data.uploaded_by);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(    
                data.approve_count + ' / ' + data.rej_count
            );
            $('.queued-task i', cloneRow).hide();
             console.log("fileSubStats = "+fileSubStats);
            if(fileSubStats == 2){
                $('.queued-task i', cloneRow).show();
                $('.queued-task i', cloneRow).on('click', function() {
                   tThis.processQueuedTasks(data.csv_id);
                });
                $('.show-approve-check', cloneRow).remove();
                $('.show-reject-check', cloneRow).remove();
                $('.bu-view-mapping', cloneRow).remove();
            }
            else if(fileSubStats == 3 && fileSubStats != 2){
                $('.queued-task', cloneRow).show();
                $('.queued-task', cloneRow).text("In Progress");
                $('.show-approve-check', cloneRow).remove();
                $('.show-reject-check', cloneRow).remove();
                $('.bu-view-mapping', cloneRow).remove();
                
            }
            else
            {
                $('.approve-checkbox', cloneRow).on('click', function(e) {
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
                $('.reject-checkbox', cloneRow).on('click', function(e) {
                    if(e.target.checked) {
                        displayPopUp('reject', data.csv_id, null);
                    }
                });
            }


            fileName = data.csv_name.split('.')
            fileName = fileName[0]

            $(".dropdown-content", cloneRow).attr("id", "myDropdown_"+j);
            $(".dropbtn", cloneRow).attr("data-dropdown-id", j);

            $('.dropbtn',cloneRow).on('click', function() {
                var dropDownID = $(this).attr("data-dropdown-id");
                if($("#myDropdown_"+dropDownID).hasClass("show") == false) {
                    $("#myDropdown_"+dropDownID).show();
                    $("#myDropdown_"+dropDownID).addClass("show");
                }
                else{
                    $("#myDropdown_"+dropDownID).hide();
                    $("#myDropdown_"+dropDownID).removeClass("show");
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
                    TOTAL_VIEW_REJECT_ITEMS = 0;
                    TOTAL_VIEW_APPROVE_ITEMS = 0;
                    TOTAL_VIEW_ITEMS = 0;
                    $('.reject-all').attr("checked", false);
                    $('.approve-all').attr("checked", false);
                    tThis.CSVID = data.csv_id;
                    tThis.countryId = data.c_id;
                    tThis.domainId = data.d_id;
                    tThis.totRecords = data.no_of_records;
                    pageLimit = parseInt(ITEMS_PER_PAGE.val());
                    tThis.showViewScreen(data.csv_id, 0, pageLimit);
                });

            } else {
                $('.bu-view-mapping', cloneRow).show();
                $('.editbtn', cloneRow).hide();
                $('.bu-view-mapping', cloneRow).on('click', function() {
                    TOTAL_VIEW_REJECT_ITEMS = 0;
                    TOTAL_VIEW_APPROVE_ITEMS = 0;
                    TOTAL_VIEW_ITEMS = 0;
                    $('.reject-all').attr("checked", false);
                    $('.approve-all').attr("checked", false);
                    tThis.CSVID = data.csv_id;
                    tThis.countryId = data.c_id;
                    tThis.domainId = data.d_id;
                    tThis.totRecords = data.no_of_records;
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

ApproveBulkMapping.prototype.processQueuedTasks = function(csvId) {
    tThis = this;
    displayLoader();
    tThis.CSVID = csvId;
        bu.documentUploadQueueProcess(
        csvId, 1, COUNTRY_VAL.val(),
        DOMAIN_VAL.val(),
        function(error, response) {   
            if(error == null){
                if(response.rejected_reason == "error"){
                    /*displaySuccessMessage(message.process_queued_temp_error);*/
                    BU_APPROVE_PAGE.possibleFailures(message.process_queued_temp_error);
                }
                else{
                    displaySuccessMessage(message.process_queued_doc_success);
                }
                if(BU_APPROVE_PAGE.fetchListData()){
                       hideLoader();
                }
                
            }
            else{
                hideLoader();
                tThis.possibleFailures(error);

            }
        }
        );

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
    function apiCall(csv_name, callback){
        console.log("Rejecttion API CALL");
        bu.getApproveMappingStatus(csv_name, callback);
    }

    function call_bck_fn(error, response){

        console.log("call_bck_fn --"+error+"-=----"+response);
        if (error == "Alive"){
            setTimeout(apiCall, TIMEOUT_MLS, csv_name, call_bck_fn);
        }
        else if (error == null && error != "Alive") {
            tThis.showList();
            tThis.fetchListData();
            displaySuccessMessage(message.approve_reject_submit_success);
        }
        else {
            if (error != "Alive"){
                BU_APPROVE_PAGE.possibleFailures(error);    
            }            
        }
    }

    bu.confirmUpdateAction(
        tThis.CSVID, tThis.countryId, tThis.domainId,
        function(error, response) {
            if(error == "Done" || response == "Done"){
                csv_name = response.csv_name;
                apiCall(csv_name, call_bck_fn);
            }
            else{
                hideLoader();
                tThis.possibleFailures(error);
            }
    });
};
ApproveBulkMapping.prototype.actionFromList = function(
    csvId, action, remarks, pwd
) {
    var showPopup = false;
    displayLoader();
    tThis = this;
    tThis.countryId = parseInt(COUNTRY_VAL.val());
    tThis.domainId = parseInt(DOMAIN_VAL.val());
    var count = 0;
    function apiCall(csv_name, callback){
        bu.getApproveMappingStatus(csv_name, callback);
    }
    function call_bck_fn(error, response){
        console.log("action : "+action);
        console.log("error : "+error);
        if (error == "Alive"){
            setTimeout(apiCall, TIMEOUT_MLS, csv_name, call_bck_fn);
        }
        else if (error == null && error != "Alive") {
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
                    hideLoader();

                }
                else {
                    displaySuccessMessage(message.reject_success);
                    hideLoader();
                }
                tThis.fetchListData();
                hideLoader();
            }
        }
        else {
            //hideLoader();
            tThis.possibleFailures(error);
        }
    }

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
            
            if(error == "Done" || response == "Done"){
                csv_name = response.csv_name;
                apiCall(csv_name, call_bck_fn);
            }
            else{
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

    $('input[id="verified_data"]').removeAttr("checked");
    $('input[id="pending_data"]').removeAttr("checked");
    $('input[id="all_data"]').prop("checked", true);
    $('.approve-all').attr("checked", false);

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
            $('.approve-all').prop("checked", false);
            $('.reject-all').prop("checked", false);
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
                $('#view_csv_id').val(response.csv_id);
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
    var tr = '';
    var clone4 = '';
    var formatDownloadUrl = '';
    var isChecked = '';
    var actionStatus = '';
    var cloneRow = '';
    var approveCheckCount;
    
    tThis = this;
    showFrom = tThis.showMapCount;
    showFrom += 1;
    VIEW_LIST_CONTAINER.find('tr').remove();
    
    if(viewData.length == 0) {
        VIEW_LIST_CONTAINER.empty();
        tr = $('#no_record_templates .table-no-content .table-row-no-content');
        clone4 = tr.clone();
        $('.no-records', clone4).text('No Records Found');
        VIEW_LIST_CONTAINER.append(clone4);
        hideLoader();
    }
    else {
        
        $.each(viewData, function(idx, data) {

            formatDownloadUrl = "/uploadedformat/";
            formatDownloadUrl += $('#view_csv_id').val();
            formatDownloadUrl += "/" + data.format_file;

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
            $('.format a', cloneRow).text(data.format_file).attr("href", formatDownloadUrl);
            $('.geography', cloneRow).text(data.geo_location);
            $('.comp-desc', cloneRow).text(data.c_desc);
            $('.penal', cloneRow).text(data.p_cons);
            
            $('.view-approve-check',cloneRow).attr("id", "view-approve-"+j);
            $('.view-approve-check',cloneRow).attr("data-sno", j);
            $('.view-reject-check',cloneRow).attr("id", "view-reject-"+j);
            $('.view-reject-check',cloneRow).attr("data-sno", j);
            $('.reject-reason .fa-info-circle',cloneRow).attr("id","fa-info-circle-"+j);

            if (parseInt(data.bu_action) == 1) {
                $('.view-approve-check',cloneRow).attr("checked", true);
                $('.view-reject-check',cloneRow).attr("checked", false);
                TOTAL_VIEW_APPROVE_ITEMS++;
            }
            else if (data.bu_action == null) {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", false);
            }
            else if (data.bu_action == 2) {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", true);
                if(parseInt(data.bu_action)==2 && data.bu_remarks != null) {
                    $('.reject-reason .fa-info-circle',cloneRow
                        ).removeClass("default-display-none");
                    $('.reject-reason .fa-info-circle',cloneRow
                        ).attr("data-original-title", data.bu_remarks);
                }
                else {
                    $('.reject-reason .fa-info-circle',cloneRow
                        ).addClass("default-display-none");
                }
                TOTAL_VIEW_REJECT_ITEMS++;
              
            }
            else {
                $('.view-approve-check', cloneRow).attr("checked", false);
                $('.view-reject-check', cloneRow).attr("checked", false);
                $('.reject-reason .fa-info-circle', cloneRow).each(function() {
                    $(this).addClass("default-display-none");
                });
            }            

            $('.view-approve-check', cloneRow).on('change', function(e) {
                var currentElement = $(this).attr("data-sno");
                if (e.target.checked) {
                    actionStatus = 1;
                    $('.reject-all').prop("checked", false);
                }
                else {
                    actionStatus = 0;
                }
                csvId = $('#view_csv_id').val();
                bu.updateActionFromView(
                    parseInt(csvId), data.sm_id, actionStatus, null,
                    function(err, res) {
                    if (err != null) {
                        tThis.possibleFailures(err);
                    }
                    else {
                        $('#fa-info-circle-'+currentElement).addClass(
                            "default-display-none");
                    }
                });
                $('#view-reject-'+currentElement).prop("checked", false);
                $('.approve-all').prop("checked", false);
                $('.reject-all').prop("checked", false);
            });


            $(".view-reject-check", cloneRow).on('change', function(e) {
                var currentElement = $(this).attr("data-sno");
                if(e.target.checked) {
                    csvId = $('#view_csv_id').val();                    
                    $('#view-approve-'+currentElement).prop("checked", false);
                    $('.approve-all').prop("checked", false);
                    displayPopUp('view-reject', parseInt(csvId), data.sm_id,
                        function(viewReason) {
                            $('#fa-info-circle-'+currentElement).removeClass(
                                "default-display-none");
                            $('#fa-info-circle-'+currentElement).attr(
                                "data-original-title", viewReason);
                    });
                }
                else
                {
                    csvId = $('#view_csv_id').val();
                    $('#view-reject-'+currentElement).prop("checked", false);
                    bu.updateActionFromView(
                        parseInt(csvId), data.sm_id, 0, null,
                        function(err, res) {
                        if (err != null) {
                            tThis.possibleFailures(err);
                        }
                        else{
                            $('#view-reject-'+currentElement).prop("checked", false);
                            $('#fa-info-circle-'+currentElement).addClass("default-display-none");
                            $('#fa-info-circle-'+currentElement).attr("data-original-title", '');
                        }
                    });
                }
                $(".zmdi-close").click(function(){
                    //$('#view-approve-'+currentElement).prop("checked", false);
                    //$('#view-reject-'+currentElement).prop("checked", false);
                });

            });
            VIEW_LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
        hideLoader();
    }

    setTimeout(function() {
        $(".tbody-sm-approve-view tr").each(function(){
            $(this).removeAttr("style");
        });
        BU_APPROVE_PAGE.approveRejectAllCheck();

    }, 500);

    $('.js-filtertable-action-sm').each(function() {
        $(this).filtertable().addFilter('.js-filter-sm');
    });

    tThis.showMapCount += viewData.length;
    $('[data-toggle="tooltip"]').tooltip();
    tThis.showPagePan(showFrom, tThis.showMapCount, STATU_TOTALS);
};

ApproveBulkMapping.prototype.approveRejectAllCheck = function(){
 if(parseInt(TOTAL_VIEW_APPROVE_ITEMS) == parseInt(TOTAL_VIEW_ITEMS) &&
            parseInt(TOTAL_VIEW_REJECT_ITEMS) == 0){
            $('.approve-all').prop("checked", true);
            $('.reject-all').prop("checked", false);
    }
    else if(TOTAL_VIEW_REJECT_ITEMS == TOTAL_VIEW_ITEMS &&
        TOTAL_VIEW_APPROVE_ITEMS == 0){
        $('.reject-all').prop("checked", true);
        $('.approve-all').prop("checked", false);
    }
    else{
        $('.reject-all').prop("checked", false);
        $('.approve-all').prop("checked", false);

    }
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
    if ($('input[id="verified_data"]:checked').length == 1)
        view_data = 1;

    if ($('input[id="pending_data"]:checked').length == 1)
        view_data = 2;
    if ($('input[id="all_data"]:checked').length == 1)
        view_data = 3;

    args = {
        "csv_id": parseInt($('#view_csv_id').val()),
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
                $('#view_csv_id').val(response.csv_id);
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
    $('#pagination_rpt').empty();
    $('#pagination_rpt').removeData('twbs-pagination');
    $('#pagination_rpt').unbind('page');
};

ApproveBulkMapping.prototype.createPageView = function() {
    tThis = this;
    perPage = parseInt(ITEMS_PER_PAGE.val());
    tThis.hidePageView();
    $('#pagination_rpt').twbsPagination({
        totalPages: Math.ceil(STATU_TOTALS / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            var showCount = 0;
            TOTAL_VIEW_APPROVE_ITEMS = 0;
            TOTAL_VIEW_REJECT_ITEMS = 0;
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
    $('compliance-count').text('');
    $('.pagination-view').hide();
};

ApproveBulkMapping.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' +
    showTo + ' of ' + total + ' compliances ';
    var pageLimit = parseInt(ITEMS_PER_PAGE.val())
    console.log("showPagePan TOTAL_VIEW_ITEMS >>>>>>>>>>"+TOTAL_VIEW_ITEMS);
    TOTAL_VIEW_ITEMS = (TOTAL_VIEW_ITEMS != 0 &&
        showTo != pageLimit)?showTo - TOTAL_VIEW_ITEMS:showTo;
    console.log(showTo + "showPagePan TOTAL_VIEW_ITEMS >>>>>>>>>>"+TOTAL_VIEW_ITEMS);

    $('.compliance-count').text(showText);
    $('.pagination-view').show();
};

ApproveBulkMapping.prototype.finalSubmit = function(csvId, pwd) {
    tThis = this;
    displayLoader();
    tThis.CSVID = csvId;
    tThis.countryId = parseInt(COUNTRY_VAL.val());
    tThis.domainId = parseInt(DOMAIN_VAL.val());

    function apiCall(csv_name, callback){
        bu.getApproveMappingStatus(csv_name, callback);
    }

    function call_bck_fn(error, response){
        if (error == "Alive"){
            setTimeout(apiCall, TIMEOUT_MLS, csv_name, call_bck_fn);
        }
        if(error == null && error != "Alive") {
            if (response.rej_count > 0) {
                msg = response.rej_count + " compliance declined, " 
                + "Do you want to continue ?";
                confirm_alert(msg, function(isConfirm) {
                    if (isConfirm) {
                        tThis.confirmAction();
                    }
                    else{
                        hideLoader();
                    }
                });
            }else {
                displaySuccessMessage(message.approve_reject_submit_success);
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
            if (error != "Alive"){
                tThis.possibleFailures(error);
            }
        }
    }
    bu.submitMappingAction(
        csvId, parseInt(COUNTRY_VAL.val()), parseInt(DOMAIN_VAL.val()), pwd,
        function(error, response) {
            if(error == "Done" || response == "Done"){
                csv_name = response.csv_name;
                apiCall(csv_name, call_bck_fn);
            }
            else if(error == "Failure"){
                hideLoader();
                tThis.possibleFailures(message.select_all_compliance_required);
            }
            else{
                hideLoader();
                tThis.possibleFailures(error);
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

    keyStatutory = $('#search_statutory').val().toLowerCase();
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
            (~d.refer_bu.toLowerCase().indexOf(keyRefer)) &&
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
      BU_APPROVE_PAGE.fetchFilterDropDown($('#view_csv_id').val());
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
        $('.approve-all').prop("checked", false);
        $('.reject-all').prop("checked", false);
        appendFilter = function(val) {
            if (filtered == '') {
                filtered += val;
            }
            else {
                filtered += "|" + val;
            }
        }
        if ($('input[id="verified_data"]:checked').length == 1)
        {
            verified = "View Data : Verified";
            appendFilter(verified);
        }
        if ($('input[id="pending_data"]:checked').length == 1)
        {
            pending = "View Data : Pending";
            appendFilter(pending);
        }
        if ($('input[id="all_data"]:checked').length == 1)
        {
            viewalldata = "View Data : All";
            appendFilter(viewalldata);
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

        $('input[id="verified_data"]').removeAttr("checked");
        $('input[id="pending_data"]').removeAttr("checked");
        $('input[id="all_data"]').prop("checked", true);
        CLEAR_FILTERED.hide();
        FILTERED_DATA.empty();
        BU_APPROVE_PAGE.renderViewFromFilter();
    });

    FINAL_SUBMIT.click(function() {
        displayPopUp("submit", parseInt($('#view_csv_id').val()), null);
    });


    APPROVE_SELECT_ALL.on("change", function(e) {
        if (BU_APPROVE_PAGE.viewDataList.length > 0 &&
            APPROVE_SELECT_ALL.prop('checked') == true) {
            $(".tbody-sm-approve-view "+
            ".view-approve-check").prop('checked', false);
            $(".tbody-sm-approve-view "+
            ".view-reject-check").prop('checked', false);
            $('.reject-reason '
                +'.fa-info-circle').addClass("default-display-none");
            $('.reject-all').attr("checked", false);
            $('.tbody-sm-approve-view .view-approve-check').each(
                function(index, el) {
                var data = BU_APPROVE_PAGE.viewDataList[index];
                var csvId = 0;
                if (e.target.checked) {
                    $(this).prop("checked", true);
                    if (data) {
                        csvId = $('#view_csv_id').val();
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
        else {
            $(this).find("*").prop("checked", false);
            $('.tbody-sm-approve-view .view-approve-check').each(
            function(index, el) {
                var data = BU_APPROVE_PAGE.viewDataList[index];
                $(this).prop("checked", false);
                $(".tbody-sm-approve-view th.reject-reason")
                .find("*").addClass("default-display-none");

                $(".tbody-sm-approve-view th.reject-reason")
                .find("*").attr("data-original-title","");
                
                if (data) {
                    csvId = $('#view_csv_id').val();
                    bu.updateActionFromView(
                    parseInt(csvId), data.sm_id, 0, '',
                    function(err, res) {
                        if (err != null) {
                        BU_APPROVE_PAGE.possibleFailures(err);
                        }
                    });
                }

            });
        }
    });


    REJECT_SELECT_ALL.on("change", function(e) {
        CURRENT_PAGE_SMID = [];
        console.log(BU_APPROVE_PAGE.viewDataList.length > 0);
        console.log(REJECT_SELECT_ALL.prop('checked') == true);
        if (BU_APPROVE_PAGE.viewDataList.length > 0 && REJECT_SELECT_ALL.prop('checked') == true) {
            displayViewRejectAllPopUp(function(reason) {
                var viewReason = $('.view-reason').val();
                var i = 0;

                $('.approve-all').attr("checked", false);
                $(".tbody-sm-approve-view "+
                ".view-approve-check").prop('checked', false);
                $(".tbody-sm-approve-view"+
                    " .view-reject-check").prop('checked', false);

                $('.tbody-sm-approve-view .view-reject-check').each(
                    function(index, el) {
                    var data = BU_APPROVE_PAGE.viewDataList[index];
                    var csvId = 0;
                    var sno;
                    sno = $(this).attr("data-sno");
                    if (e.target.checked) {
                        $(this).prop("checked", true);
                        $('#fa-info-circle-'+sno).removeClass(
                            "default-display-none");
                        $('#fa-info-circle-'+sno).attr(
                            "data-original-title", viewReason);

                        if (data) {
                            csvId = $('#view_csv_id').val();
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
                        console.log('#fa-info-circle-'+sno);
                        $('#fa-info-circle-'+sno).addClass(
                            "default-display-none");
                        $('#fa-info-circle-'+sno).attr(
                            "data-original-title", "");

                        $(this).find("*").prop("checked", false);

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
            $('.tbody-sm-approve-view .view-reject-check').each(
            function(index, el) {
                var sno;
                var data = BU_APPROVE_PAGE.viewDataList[index];
                sno = $(this).attr("data-sno");
                $(this).prop("checked", false);
                        console.log('#fa-info-circle-'+sno);
                $('#fa-info-circle-'+sno).addClass(
                    "default-display-none");
                $('#fa-info-circle-'+sno).attr(
                    "data-original-title", "");
                
                if (data) {
                    csvId = $('#view_csv_id').val();
                    bu.updateActionFromView(
                    parseInt(csvId), data.sm_id, 0, '',
                    function(err, res) {
                        if (err != null) {
                        BU_APPROVE_PAGE.possibleFailures(err);
                        }
                    });
                }

            });
       }
    });

    ITEMS_PER_PAGE.on("change", function(e) {
        pageLimit = parseInt(ITEMS_PER_PAGE.val());
        tThis.showViewScreen(tThis.CSVID, 0, pageLimit);
    });

    
    FREEZER_TABLE.scroll(function(e) {

        FREEZER_THEAD.css("left", -FREEZER_TBODY.scrollLeft());
        FREEZER_TH_CHILD_1.css("left", FREEZER_TABLE.scrollLeft() -0 );
        FREEZER_TH_CHILD_2.css("left", FREEZER_TABLE.scrollLeft() -0 );
        FREEZER_TH_CHILD_3.css("left", FREEZER_TABLE.scrollLeft() -0 );
        FREEZER_TH_CHILD_4.css("left", FREEZER_TABLE.scrollLeft() -0 );
        FREEZER_TH_CHILD_5.css("left", FREEZER_TABLE.scrollLeft() -0 );
        FREEZER_TH_CHILD_6.css("left", FREEZER_TABLE.scrollLeft() -0 );


        $('#multi_col_freezer .table-responsive tbody td:nth-child(1)'
            ).css("left", FREEZER_TABLE.scrollLeft());        
        $('#multi_col_freezer .table-responsive tbody td:nth-child(2)'
            ).css("left", FREEZER_TABLE.scrollLeft());        
        $('#multi_col_freezer .table-responsive tbody td:nth-child(3)'
            ).css("left", FREEZER_TABLE.scrollLeft());        
        $('#multi_col_freezer .table-responsive tbody td:nth-child(4)'
            ).css("left", FREEZER_TABLE.scrollLeft());        
        $('#multi_col_freezer .table-responsive tbody td:nth-child(5)'
            ).css("left", FREEZER_TABLE.scrollLeft());

        FREEZER_THEAD.css("top", -FREEZER_TBODY.scrollTop());
        FREEZER_TH.css("top", FREEZER_TABLE.scrollTop());
    });
}

BU_APPROVE_PAGE = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    BU_APPROVE_PAGE.showList();
});
$(".nicescroll").niceScroll();

$('.reject-reason-txt').on('input', function (e) {
      isCommon_input(this);
});

$('#view_reason_id').on('input', function (e) {
      isCommon_input(this);
});