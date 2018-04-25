// control initialize
var ListContainer = $('.tbody-sm-approve-list1');
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');
var ListScreen = $("#sm-approve-list");
var ViewScreen = $("#sm-approve-view");
var ShowButton = $("#btn-list-show");
var GoButton = $("#go");
var PasswordSubmitButton = $('.password-submit');
var CancelButton = $("#btn-sm-view-cancel");
var ViewListContainer = $('.tbody-sm-approve-view');
var ViewListRowTemplate = $('#templates .table-sm-approve-info tr');
var FinalSubmit = $('#btn-final-submit');
var FILTERED_DATA = $('.filtered-data');
var CLEAR_FILTERED = $(".clear-filtered");

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var OnCurrentPage = 1;
var STATUTOTALS;
var j = 1;

var pageType = "show";

var CurrentPassword = null;

var MsgPan = $(".error-message");
var buApprovePage = null;
var isAuthenticate;


// auto complete - country
var countryVal = $('#countryid');
var countryAc = $("#countryname");
var AcCountry = $('#ac-country');

// auto complete - domain
var domainVal = $('#domainid');
var domainAc = $("#domainname");
var AcDomain = $('#ac-domain')

// auto complete - user
var userVal = $('#userid');
var userAc = $("#username");
var AcUser = $('#ac-user');

var searchFileName = $('.search-file-name');
var searchUploadBy = $('.search-upload-by');
var searchTotRecords = $('.search-tot-records');
var searchUploadOn = $('.search-upload-on');

var searchStatutory = $('#search-statutory');
var searchOrganization = $('#search-organization');
var searchNature = $('#search-nature');
var searchProvision = $('#search-provision');
var searchCTask = $('#search-c-task');
var searchCDoc = $('#search-c-doc');
var searchTaskId = $('#search-task-id');
var searchCDesc = $('#search-c-desc');
var searchPCons = $('#search-p-cons');
var searchTaskType = $('#search-task-type');
var searchReferLink = $('#search-refer-link');
var searchFreq = $('#search-frequency');
var searchFormat = $('#search-format');
var searchGeography = $('#search-geo');

// filter controls

var acOrgName = $('#orgname');
var ACOrg = $('#ac-orgname');
var acNature = $('#nature');
var ACNature = $('#ac-nature');
var acStatutory = $('#statutory');
var ACStatutory = $('#ac-statutory');
var acGeoLocation = $('#geolocation');
var ACGeoLocation = $('#ac-geolocation');
var acCompTask = $('#comptask');
var ACCompTask = $('#ac-comptask');
var acTaskId = $('#taskid');
var ACTaskId = $('#ac-taskid');
var acCompDoc = $('#compdoc');
var ACCompDoc = $('#ac-compdoc');
var acCompDesc = $('#compdesc');
var ACCompDesc = $('#ac-compdesc');
var acTaskType = $('#tasktype');
var ACTaskType = $('#ac-tasktype');
var acViewData = $('.view-data');
var MultiSelectFrequency = $('#frequency');

var ApproveSelectAll = $(".approve-all");
var RejectSelectAll = $(".reject-all");
var CurrentPageSmId = [];


function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    var primaryKey = idElement[0].id;
    if(primaryKey == 'countryid'){
      domainAc.val('');
      domainVal.val('');
      userAc.val('');
      userVal.val('');
    }
}
function resetFilter(evt) {
    if (evt == "country") {
        domainAc.val('');
        domainVal.val('');
        userVal.val('');
        userAc.val('');
    }
    if (evt == "domain") {
        userVal.val('');
        userAc.val('');
    }
    ListContainer.empty();
}

function RejectSelectAllFilter(evt) {

    if (evt == "country") {
        domainAc.val('');
        domainVal.val('');
        userVal.val('');
        userAc.val('');
    }
    if (evt == "domain") {
        userVal.val('');
        userAc.val('');
    }
    ListContainer.empty();
}

function displayPopUp(TYPE, csvId, smid, callback){
    console.log("TYPE ->>>>>> "+ TYPE);
    if (TYPE == "reject") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current-password-reject');
        $('.reject-reason-txt').val('')
    }
    else if (TYPE == "view-reject") {
        targetid = "#custom-modal-remarks";
        CurrentPassword = null;
        $('.view-reason').val('');
    }
    else {
        targetid = "#custom-modal-approve"
        CurrentPassword = $('#current-password');
    }
    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CurrentPassword != null) {
                CurrentPassword.focus();
                CurrentPassword.val('');
            }
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                displayLoader();
                setTimeout(function() {
                    if (TYPE == "approve") {
                        csvId["TYPE"] = "approve";
                        console.log(csvId);
                        buApprovePage.actionFromList(
                            csvId, 1, null, CurrentPassword.val()
                        );
                    }
                    else if (TYPE == "reject") {
                        if ($('.reject-reason-txt').val() == '') {
                            displayMessage(message.reason_required)
                        }
                        else {

                            buApprovePage.actionFromList(
                                csvId, 2, $('.reject-reason-txt').val(),
                                CurrentPassword.val()
                            );
                        }
                    }
                    else if (TYPE == "submit") {
                        buApprovePage.finalSubmit(
                            csvId, CurrentPassword.val()
                        );
                    }
                    else if (TYPE == "view-reject") {
                        if ($('.view-reason').val()== '') {
                            displayMessage(message.reason_required)
                        }
                        else {
                            bu.updateActionFromView(
                                csvId, smid, 2, $('.view-reason').val(),
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

function displayViewRejectAllPopUp(callback){
    targetid = "#custom-modal-remarks";
    CurrentPassword = null;
    $('.view-reason').val('')

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CurrentPassword != null) {
                CurrentPassword.focus();
                CurrentPassword.val('');
            }
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
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

    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    }else if(isLengthMinMax(
        CurrentPassword, 1, 20, message.password_20_exists) == false
    ){
        return false;
    } else {
        isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
}


function ApproveBulkMapping() {
    this.CountryList = [];
    this.DomainList = [];
    this.UserList = [];
    this.ApproveDataList = [];
    this.ViewDataList = [];
    this.OrgaNames = [];
    this.Natures = [];
    this.Statutories = [];
    this.Frequency = [];
    this.GeoLocation = [];
    this.CompTasks = [];
    this.CompDescs = [];
    this.CompDocs = [];
    this.TaskId = [];
    this.TaskType = [];
    this.CSVID = null;
    this.showMapCount = 0;
    this.CountryId = null;
    this.DomainId = null;
}
ApproveBulkMapping.prototype.possibleFailures = function(error) {
    displayMessage(error);
    hideLoader();
};
ApproveBulkMapping.prototype.showList = function() {
    ListScreen.show();
    ViewScreen.hide();
    searchFileName.val('');
    searchUploadBy.val('');
    searchTotRecords.val('');
    searchUploadOn.val('');
    this.fetchDropDownData();

};
ApproveBulkMapping.prototype.fetchListData = function() {
    tThis = this;
    displayLoader();
    cid = parseInt(countryVal.val());
    did = parseInt(domainVal.val());
    uid = parseInt(userVal.val());
    bu.getApproveMappingCSVList(cid, did, uid, function(error, response) {
        if (error == null) {
            tThis.ApproveDataList = response.pending_csv_list;
            $.each(tThis.ApproveDataList, function(idx, data) {
                uploadedName = null
                for (var i=0; i<tThis.UserList.length; i++) {
                    if (data.uploaded_by == tThis.UserList[i].user_id) {
                        uploadedName = tThis.UserList[i].emp_code_name
                        break;
                    }
                    else
                    {
                        uploadedName = '';
                    }
                }
                if (uploadedName != null) {
                    data.uploaded_by = uploadedName;
                }

            });
            tThis.renderList(tThis.ApproveDataList);
            hideLoader();
        }
        else{
            hideLoader();
            tThis.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.renderList = function(listData) {
    tThis = this;
    var j = 1;

    ListContainer.find('tr').remove();
    if(listData.length == 0) {
        ListContainer.empty();
        var tr = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    }
    else {
        $.each(listData, function(idx, data) {
            var cloneRow = ListRowTemplate.clone();
            var approve_reject_count = {};
            cnameSplit = data.csv_name.split("_");
            cnameSplit.pop();
            cname = cnameSplit.join("_");
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cname);;
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(data.uploaded_by);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(
                data.approve_count + ' / ' + data.rej_count
            );
            $('.approve-checkbox', cloneRow).on('change', function(e){

                if (e.target.checked){

                    if(data.rej_count > 0){
                        approve_reject_count['approve_count'] = data.approve_count
                        approve_reject_count['rej_count'] = data.rej_count
                        approve_reject_count['csv_id'] = data.csv_id
                        displayPopUp('approve', approve_reject_count, null);
                    }
                    else{
                        displayPopUp('approve', data.csv_id, null);
                    }
                }
            });
            $('.reject-checkbox', cloneRow).on('change', function(e){
                if(e.target.checked){
                    displayPopUp('reject', data.csv_id, null);
                }
            });
            /*$('.bu-view-mapping', cloneRow).on('click', function(){
                tThis.CSVID = data.csv_id;
                tThis.CountryId = data.c_id;
                tThis.DomainId = data.d_id;
                pageLimit = parseInt(ItemsPerPage.val());
                tThis.showViewScreen(data.csv_id, 0, pageLimit);
            });*/
            flname = data.csv_name.split('.')
            flname = flname[0]

            $('.dropbtn',cloneRow).on('click', function(){
                if($(".dropdown-content", cloneRow).hasClass("show")==false){
                    $(".dropdown-content", cloneRow).show();
                    $(".dropdown-content", cloneRow).addClass("show");
                }
                else{
                    $(".dropdown-content", cloneRow).hide();
                    $(".dropdown-content", cloneRow).removeClass("show");
                }
            });

            $(".dl-xls-file, .dl-csv-file, .dl-ods-file,"+
                " .dl-txt-file", cloneRow).on("click", function(){
                $(".dropdown-content", cloneRow).hide();
                $(".dropdown-content", cloneRow).removeClass("show");
            });

            $('.dl-xls-file',cloneRow).attr(
                "href", "/uploaded_file/xlsx/"+flname+'.xlsx'
            );
            $('.dl-csv-file',cloneRow).attr(
                "href", "/uploaded_file/csv/"+flname+'.csv'
            );
            $('.dl-ods-file',cloneRow).attr(
                "href", "/uploaded_file/ods/"+flname+ '.ods'
            );
            $('.dl-txt-file',cloneRow).attr(
                "href", "/uploaded_file/txt/"+flname+'.txt'
            );
            if(data.approve_count > 0 || data.rej_count > 0 || data.declined_count > 0){
                $('.bu-view-mapping', cloneRow).hide();
                $('.editbtn', cloneRow).show();

                $('.editbtn', cloneRow).on('click', function(){
                    tThis.CSVID = data.csv_id;
                    tThis.CountryId = data.c_id;
                    tThis.DomainId = data.d_id;
                    pageLimit = parseInt(ItemsPerPage.val());
                    tThis.showViewScreen(data.csv_id, 0, pageLimit);
                });

            } else {
                $('.bu-view-mapping', cloneRow).show();
                $('.editbtn', cloneRow).hide();
                $('.bu-view-mapping', cloneRow).on('click', function(){
                    tThis.CSVID = data.csv_id;
                    tThis.CountryId = data.c_id;
                    tThis.DomainId = data.d_id;
                    pageLimit = parseInt(ItemsPerPage.val());
                    tThis.showViewScreen(data.csv_id, 0, pageLimit);
                });
            }
            ListContainer.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};
ApproveBulkMapping.prototype.fetchDropDownData = function() {
    tThis = this;
    displayLoader();
    bu.getDomainList(function (error, response) {
        console.log("error " + error);
        console.log('response'+ response)
        if (error == null) {
            tThis.DomainList = response.bsm_domains;
            tThis.CountryList = response.bsm_countries
            bu.getKnowledgeUserInfo(function (err, resp){
                console.log(JSON.stringify(resp));
                if (err == null){
                    tThis.UserList = resp.k_executive_info;
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
        tThis.CSVID, tThis.CountryId, tThis.DomainId,
        function(error, response) {
        if (error == null) {
            tThis.showList();
            tThis.fetchListData();
            displaySuccessMessage(message.confirm_success);
        }
        else {
            buApprovePage.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.actionFromList = function(
    csvId, action, remarks, pwd
) {
    displayLoader();
    tThis = this;
    tThis.CountryId = parseInt(countryVal.val());
    tThis.DomainId = parseInt(domainVal.val());
    var showPopup = false;
    console.log("csvId"+ JSON.stringify(csvId));
    if(typeof csvId != "number"){
        if(csvId["TYPE"].length > 0 && csvId["TYPE"] == "approve"){
            if(csvId["rej_count"] > 0){
                tThis.CSVID = csvId["csv_id"];
                csvId = tThis.CSVID;
                swal({
                    title: "Are you sure",
                    text: "Some manual rejections are inside, Do you want to continue?",
                    type: "success",
                    showCancelButton: true,
                    confirmButtonClass: 'btn-success waves-effect waves-light',
                    confirmButtonText: 'Yes'
                }, function(isConfirm) {
                    if (isConfirm) {
                            bu.updateActionFromList(
                                csvId, action, remarks, pwd, countryVal.val(),
                                domainVal.val(),
                                function(error, response){
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
                                        }else {
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
                        else{
                            hideLoader();
                            return false;
                        }
                    })
            }
        }
    }
    else{
        console.log("else---> " + csvId);
        tThis.CSVID = csvId;
        bu.updateActionFromList(
        csvId, action, remarks, pwd, countryVal.val(),
        domainVal.val(),
        function(error, response){
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
                }else {
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
    ListScreen.hide();
    ViewScreen.show();

    searchStatutory.val('');
    searchOrganization.val('');
    searchNature.val('');
    searchProvision.val('');
    searchCTask.val('');
    searchCDoc.val('');
    searchTaskId.val('');
    searchCDesc.val('');
    searchPCons.val('');
    searchTaskType.val('');
    searchReferLink.val('');
    searchFreq.val('');
    searchFormat.val('');
    searchGeography.val('');

    acOrgName.val('');
    acNature.val('');
    acStatutory.val('');
    acGeoLocation.val('');
    acCompTask.val('');
    acTaskId.val('');
    acCompDoc.val('');
    acCompDesc.val('');
    acTaskType.val('');
    MultiSelectFrequency.find("option").remove();
    MultiSelectFrequency.multiselect('destroy');

    $('input[id="verified-data"]').removeAttr("checked");
    $('input[id="pending-data"]').removeAttr("checked");
    $('input[id="all-data"]').prop("checked", true);

    CLEAR_FILTERED.hide();
    FILTERED_DATA.empty();

    onCurrentPage = 1;
    j = 1;
    $('.filtered-data').text('');
    buApprovePage.showMapCount = 0;
    buApprovePage.fetchViewData(csvId, fCount, rRange);


// setTimeout(function(){  $.getScript("/knowledge/js/multifreezer.js");

// $.getScript("/knowledge/css/multifreezer.css");
 // hideLoader();}, 3000);

    if($("body").hasClass("freezer-active-bu")==false) {
        displayLoader();
/*        setTimeout(function(){  $.getScript(
            "/knowledge/js/multifreezer.js");  hideLoader();}, 3000
        );*/
    }

// $.getScript("/knowledge/js/multifreezer.js");
};
ApproveBulkMapping.prototype.fetchViewData = function(
    csvId, fCount, rRange
) {
    tThis = this;

    displayLoader();
    bu.getApproveMappingView(csvId, fCount, rRange, function(
        error, response
    ){
        if(error == null) {
            tThis.ViewDataList = response.mapping_data;
            if (tThis.ViewDataList.length > 0) {

                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploadedName = null
                for (var i=0; i<tThis.UserList.length; i++) {
                    if (response.uploaded_by == tThis.UserList[i].user_id) {
                        uploadedName = tThis.UserList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploadedName);
                $('.view-uploaded-on').text(response.uploaded_on);
                cnameSplit = response.csv_name.split("_");
                cnameSplit.pop();
                cname = cnameSplit.join("_");
                $('.view-csv-name').text(cname);
                $('#view-csv-id').val(response.csv_id);
                STATUTOTALS  = response.total;
                if(tThis.ViewDataList.length == 0) {
                    _tThis.hidePagePan();
                    PaginationView.hide();
                    tThis.hidePageView();
                }
                else {
                    if (onCurrentPage == 1) {
                        tThis.createPageView();
                        PaginationView.show();
                    }
                    pageType = "show";

                }
            }
            tThis.renderViewScreen(tThis.ViewDataList);

            // var onetimejs = $(".tbody-sm-approve-view").html();
            // alert(onetimejs);


            hideLoader();
        }
    });

};
ApproveBulkMapping.prototype.renderViewScreen = function(viewData) {
    tThis = this;
    showFrom = tThis.showMapCount;
    showFrom += 1;

    ViewListContainer.find('tr').remove();
    if(viewData.length == 0) {
        ViewListContainer.empty();
        var tr = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        ViewListContainer.append(clone4);
        hideLoader();
    }
    else {
        $.each(viewData, function(idx, data) {

            var formatDownloadUrl = "/uploadedformat/" +
                $('#view-csv-id').val() + "/" + data.format_file;
            var isChecked;
            var actionStatus;

            var cloneRow = ViewListRowTemplate.clone();
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
                if(parseInt(data.bu_action)==2 && data.bu_remarks != null){
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

            $('.view-approve-check', cloneRow).on('change', function(e){
                if (e.target.checked){
                    isChecked = false;
                    actionStatus = 1;
                    $('.reject-all').attr("checked", false);
                }
                else{
                    isChecked = true;
                    actionStatus = 0;
                }
                csvid = $('#view-csv-id').val();
                bu.updateActionFromView(
                    parseInt(csvid), data.sm_id, actionStatus, null,
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
            $(".view-reject-check", cloneRow).on('change', function(e){
                if(e.target.checked){
                    csvid = $('#view-csv-id').val();
                    $('.view-approve-check',cloneRow).attr("checked", false);
                    $('.approve-all').attr("checked", false);
                    displayPopUp('view-reject', parseInt(csvid), data.sm_id,
                        function(viewReason){
                            $('.reject-reason .fa-info-circle', cloneRow).
                            removeClass("default-display-none");
                            $('.reject-reason .fa-info-circle', cloneRow).
                            attr("data-original-title", viewReason);
                    });
                }
                else
                {
                    csvid = $('#view-csv-id').val();
                    $('.view-reject-check',cloneRow).attr("checked", false);
                    bu.updateActionFromView(
                        parseInt(csvid), data.sm_id, 0, null,
                        function(err, res) {
                        if (err != null) {
                            tThis.possibleFailures(err);
                        }
                        else{
                            $('.view-reject-check',cloneRow).attr("checked", false);
                            $('.reject-reason .fa-info-circle', cloneRow).addClass("default-display-none");
                            $('.reject-reason .fa-info-circle', cloneRow).attr("data-original-title", '');
                        }
                    });
                }

            });
            ViewListContainer.append(cloneRow);
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
    tThis.showPagePan(showFrom, tThis.showMapCount, STATUTOTALS);
};
/*ApproveBulkMapping.prototype.refreshFreezer = function() {
            setTimeout(function() {
                var freezerHtml = ".freeze-multi-scroll-left-body-inner"
                                  +" #datatable-responsive";
                $(freezerHtml).empty();
                tBodyClone = $(".freeze-multi-scroll-table-body"+
                    " .tbody-sm-approve-view");
                clone1 = tBodyClone.clone();
                $(freezerHtml).append(clone1);
                $(freezerHtml).show();
        }, 2000);

}*/
ApproveBulkMapping.prototype.fetchFilterDropDown = function(csvid) {
    tThis = this;
    displayLoader();
    bu.getApproveMappingViewFilter(parseInt(csvid), function(err, resp) {
        if (err == null) {
            tThis.OrgaNames = resp.orga_names;
            tThis.Natures = resp.s_natures;
            tThis.Statutories = resp.bu_statutories;
            tThis.Frequency = resp.frequencies;
            tThis.GeoLocation = resp.geo_locations;
            tThis.CompTasks = resp.c_tasks;
            tThis.CompDescs = resp.c_descs;
            tThis.CompDocs = resp.c_docs;
            tThis.TaskId = resp.task_ids;
            tThis.TaskType = resp.task_types
            if (tThis.Frequency.length > 0) {
                str = ''
                for (var i in tThis.Frequency){
                    val = tThis.Frequency[i]
                    str += '<option value="'+ val +'">'+ val +'</option>';
                }
                MultiSelectFrequency.html(str).multiselect('rebuild');
            }
            hideLoader();
        }
    });
};

ApproveBulkMapping.prototype.renderViewFromFilter = function() {
    displayLoader();
    pageLimit = parseInt(ItemsPerPage.val());
    var view_data = 3;
    var showCount = 0;
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
        "orga_name": acOrgName.val(),
        "s_nature": acNature.val(),
        "f_types": fTypes,
        "statutory": acStatutory.val(),
        "geo_location": acGeoLocation.val(),
        "c_task_name": acCompTask.val(),
        "c_desc": acCompDesc.val(),
        "c_doc": acCompDoc.val(),
        "f_count": showCount,
        "r_range": pageLimit,
        "tsk_id": acTaskId.val(),
        "tsk_type": acTaskType.val(),
        "filter_view_data" : view_data
    }

    bu.getApproveMappingViewFromFilter(args, function(err, response){
        displayLoader();
        if(err != null) {
            hideLoader();
            buApprovePage.possibleFailures(err)
        }
        if(err == null) {
            tThis.ViewDataList = response.mapping_data;
            if (tThis.ViewDataList.length > 0) {
                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploadedName = null
                for (var i=0; i<tThis.UserList.length; i++) {
                    if (response.uploaded_by == tThis.UserList[i].user_id) {
                        uploadedName = tThis.UserList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploadedName);
                $('.view-uploaded-on').text(response.uploaded_on);
                cnameSplit = response.csv_name.split("_");
                cnameSplit.pop();
                cname = cnameSplit.join("_");
                $('.view-csv-name').text(cname);
                $('#view-csv-id').val(response.csv_id);
                STATUTOTALS  = response.total;
                if(tThis.ViewDataList.length == 0) {
                    _tThis.hidePagePan();
                    PaginationView.hide();
                    tThis.hidePageView();
                }
                else {
                    pageType = "filter";
                    if (onCurrentPage == 1) {
                        tThis.createPageView();
                        PaginationView.show();
                    }

                }
            }
            tThis.renderViewScreen(tThis.ViewDataList);
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
    perPage = parseInt(ItemsPerPage.val());
    tThis.hidePageView();
    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(STATUTOTALS / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            console.log(page);
            cpage = parseInt(page);
            if (parseInt(onCurrentPage) != cpage) {
                onCurrentPage = cpage;
                console.log(onCurrentPage)
                if(pageType == "show") {
                    pageLimit = parseInt(ItemsPerPage.val());
                    var showCount = 0;
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

ApproveBulkMapping.prototype.finalSubmit = function(csvid, pwd) {
    tThis = this;
    displayLoader();
    tThis.CSVID = csvid;
    tThis.CountryId = parseInt(countryVal.val());
    tThis.DomainId = parseInt(domainVal.val());
    bu.submitMappingAction(
        csvid, parseInt(countryVal.val()), parseInt(domainVal.val()), pwd,
        function(err, res){
        if(err == null) {
            if (res.rej_count > 0) {
                msg = res.rej_count + " compliance declined, Do you want to continue ?";
                confirm_alert(msg, function(isConfirm) {
                    if (isConfirm) {
                        tThis.confirmAction();
                    }
                });
            }else {
                displaySuccessMessage(message.submit_success);
                ListScreen.show();
                ViewScreen.hide();
                searchFileName.val('');
                searchUploadBy.val('');
                searchTotRecords.val('');
                searchUploadOn.val('');
                tThis.fetchListData()
            }

        }
        else {
            tThis.possibleFailures(err);
        }
    });

};

function key_search(mainList) {
    var csvKey = searchFileName.val().toLowerCase();
    var uploadByKey = searchUploadBy.val().toLowerCase();
    var total = searchTotRecords.val();
    var uploadOnKey = searchUploadOn.val().toLowerCase();
    var csvName, uploadby, totalrecords, uploadon;

    var fList = [];
    for (var entity in mainList) {
        csvName = mainList[entity].csv_name;
        uploadby = mainList[entity].uploaded_by;
        totalrecords = mainList[entity].no_of_records;
        uploadon = mainList[entity].uploaded_on;

        if (
            (~csvName.toLowerCase().indexOf(csvKey)) &&
            (~uploadon.toLowerCase().indexOf(uploadOnKey)) &&
            (~uploadby.toLowerCase().indexOf(uploadByKey)) &&
            (~totalrecords.toString().indexOf(total))
        ){
            fList.push(mainList[entity]);
        }
    }
    return fList
}
function key_view_search(mainList) {

    keyStatutory = $('#search-statutory').val().toLowerCase();
    keyOrganization = searchOrganization.val().toLowerCase();
    keyNature = searchNature.val().toLowerCase();
    keyProvision = searchProvision.val().toLowerCase();
    keyCTask = searchCTask.val().toLowerCase();
    keyCDoc = searchCDoc.val().toLowerCase();
    keyTaskId = searchTaskId.val().toLowerCase();
    keyCDesc = searchCDesc.val().toLowerCase();
    keyPCons = searchPCons.val().toLowerCase();
    keyTaskType = searchTaskType.val().toLowerCase();
    keyRefer = searchReferLink.val().toLowerCase();
    keyFreq = searchFreq.val().toLowerCase();
    keyFormat = searchFormat.val().toLowerCase();
    keyGeo = searchGeography.val().toLowerCase();

    var fList = [];
    for (var entity in mainList) {
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
            (~d.geo_location.toLowerCase().indexOf(keyGeo))){

            fList.push(mainList[entity]);
        }
    }
    j = 1;
    buApprovePage.showMapCount = 0;
    return fList
}

function PageControls() {
    countryAc.keyup(function(e){
        var conditionFields = ["is_active"];
        var conditionValues = [true];
        var textVal = $(this).val();
        commonAutoComplete(
            e, AcCountry, countryVal, textVal,
            buApprovePage.CountryList, "country_name", "country_id",
            function (val) {
                onAutoCompleteSuccess(countryAc, countryVal, val);
            }, conditionFields, conditionValues
        );
        resetFilter('country');

    });

    domainAc.keyup(function(e){
        var mainDomainList = buApprovePage.DomainList;
        var textVal = $(this).val();
        var domainList = [];
        var cIds = null;
        var checkVal = false;
        if(countryVal.val() != ''){
          for(var i=0;i<mainDomainList.length;i++){
            cIds = mainDomainList[i].country_ids;

            for(var j=0;j<cIds.length;j++){
              if(cIds[j] == countryVal.val())
              {
                checkVal = true;
              }
            }

            if(checkVal == true && mainDomainList[i].is_active == true){
              domainList.push({
                "domain_id": mainDomainList[i].domain_id,
                "domain_name": mainDomainList[i].domain_name
              });
              checkVal = false;
              //break;
            }
          }
          commonAutoComplete(
            e, AcDomain, domainVal, textVal,
            domainList, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(domainAc, domainVal, val);
         });
        }
        else{
          displayMessage(message.country_required);
        }
        resetFilter('domain');
    });

    userAc.keyup(function(e){
        var mainUserList = buApprovePage.UserList;
        var textVal = $(this).val();
        var userList = [];
        if (countryVal.val() != '' && domainVal.val() != '') {
            for (var i=0; i<mainUserList.length; i++) {
                if(
                    (jQuery.inArray(
                        parseInt(countryVal.val()), mainUserList[i].c_ids
                        ) !== -1) &&
                    (jQuery.inArray(
                        parseInt(domainVal.val()), mainUserList[i].d_ids
                        ) !== -1)
                ) {

                    userList.push({
                        "emp_id": mainUserList[i].user_id,
                        "emp_name": mainUserList[i].emp_code_name
                    });
                }

            }
            commonAutoComplete(
                e, AcUser, userVal, textVal,
                userList, "emp_name", "emp_id", function (val) {
                    onAutoCompleteSuccess(userAc, userVal, val);
            });
        }
        else {
            if (countryVal.val() == '') {
                displayMessage(message.country_required);
            }
            else if (domainVal.val() == '') {
                displayMessage(message.domain_required);
            }
        }
        resetFilter('user');
    });

    ShowButton.click(function(){
        if (countryVal.val() == '') {
            displayMessage(message.country_required);
        }
        else if (domainVal.val() == '') {
            displayMessage(message.domain_required);
        }
        if (countryVal.val() != '' && domainVal.val() != '') {
            buApprovePage.fetchListData()
        }
    });

    PasswordSubmitButton.click(function(){
        if (CurrentPassword != null) {
            validateAuthentication();
        }
        else {
            isAuthenticate = true;
            Custombox.close();
            displayLoader();
        }
    });

    CancelButton.click(function() {
        buApprovePage.showList();
        buApprovePage.fetchListData();
    });

    searchFileName.keyup(function() {
        fList = key_search(buApprovePage.ApproveDataList);
        buApprovePage.renderList(fList);
    });

    searchTotRecords.keyup(function() {
        fList = key_search(buApprovePage.ApproveDataList);
        buApprovePage.renderList(fList);
    });

    searchUploadBy.keyup(function() {
        fList = key_search(buApprovePage.ApproveDataList);
        buApprovePage.renderList(fList);
    });
    searchUploadOn.keyup(function() {
        fList = key_search(buApprovePage.ApproveDataList);
        buApprovePage.renderList(fList);
    });

    searchStatutory.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchOrganization.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchNature.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchProvision.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchCTask.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchCDoc.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchTaskId.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchCDesc.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchPCons.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchTaskType.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchReferLink.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchFreq.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchFormat.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });
    searchGeography.keyup(function(){
        displayLoader();
        fList = key_view_search(buApprovePage.ViewDataList);
        buApprovePage.renderViewScreen(fList);
    });

    // filter events

    $('.right-bar-toggle').on('click', function(e) {
      $('#wrapper').toggleClass('right-bar-enabled');
      buApprovePage.fetchFilterDropDown($('#view-csv-id').val());
    });

    acOrgName.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACOrg, textVal,
            buApprovePage.OrgaNames, function (val) {
                acOrgName.val(val[0])
            }
        );

    });

    acNature.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACNature, textVal,
            buApprovePage.Natures, function (val) {
                acNature.val(val[0])
            }
        );

    });

    acStatutory.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACStatutory, textVal,
            buApprovePage.Statutories, function (val) {
                acStatutory.val(val[0])
            }
        );

    });

    acGeoLocation.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACGeoLocation, textVal,
            buApprovePage.GeoLocation, function (val) {
                acGeoLocation.val(val[0])
            }
        );

    });

    acCompTask.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACCompTask, textVal,
            buApprovePage.CompTasks, function (val) {
                acCompTask.val(val[0])
            }
        );
    });

    acTaskId.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACTaskId, textVal,
            buApprovePage.TaskId, function (val) {
                acTaskId.val(val[0])
            }
        );
    });

    acCompDoc.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACCompDoc, textVal,
            buApprovePage.CompDocs, function (val) {
                acCompDoc.val(val[0])
            }
        );
    });

    acCompDesc.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACCompDesc, textVal,
            buApprovePage.CompDescs, function (val) {
                acCompDesc.val(val[0])
            }
        );
    });


    acTaskType.keyup(function(e){
        var textVal = $(this).val();
        commonArrayAutoComplete(
            e, ACTaskType, textVal,
            buApprovePage.TaskType, function (val) {
                acTaskType.val(val[0])
            }
        );
    });

    GoButton.click(function(){
        FILTERED_DATA.empty();
        CLEAR_FILTERED.hide();
        var filtered = '';
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
        if(acOrgName.val() != "") {
            orgs = "Organization : " + acOrgName.val();
            appendFilter(orgs);
        }
        if(acNature.val() != "") {
            natures = "Statutory Nature : " + acNature.val();
            appendFilter(natures);
        }
        if (acStatutory.val() != "") {
            statutories = "Statutory : " + acStatutory.val();
            appendFilter(statutories);
        }
        if(acGeoLocation.val() != "") {
            geos = "Geography Location : " + acGeoLocation.val();
            appendFilter(geos);
        }
        if(acCompTask.val() != "") {
            tasks = "Compliance Task : " + acCompTask.val();
            appendFilter(tasks);
        }
        if(acTaskId.val() != "") {
            tid = "Task ID : " + acTaskId.val();
            appendFilter(tid);
        }
        if(acCompDoc.val() != "") {
            doc = "Compliance Document : " + acCompDoc.val();
            appendFilter(doc);
        }
        if(acCompDesc.val() != "") {
            desc = "Compliance Description : " + acCompDesc.val();
            appendFilter(desc);
        }
        if(acTaskType.val() != "") {
            tt = "Task Type : " + acTaskType.val();
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
            CLEAR_FILTERED.hide()
        }

        onCurrentPage = 1;
        buApprovePage.renderViewFromFilter();

    });
    CLEAR_FILTERED.click(function() {
        searchStatutory.val('');
        searchOrganization.val('');
        searchNature.val('');
        searchProvision.val('');
        searchCTask.val('');
        searchCDoc.val('');
        searchTaskId.val('');
        searchCDesc.val('');
        searchPCons.val('');
        searchTaskType.val('');
        searchReferLink.val('');
        searchFreq.val('');
        searchFormat.val('');
        searchGeography.val('');

        acOrgName.val('');
        acNature.val('');
        acStatutory.val('');
        acGeoLocation.val('');
        acCompTask.val('');
        acTaskId.val('');
        acCompDoc.val('');
        acCompDesc.val('');
        acTaskType.val('');
        MultiSelectFrequency.find("option").remove();
        MultiSelectFrequency.multiselect('destroy');

        $('input[id="verified-data"]').removeAttr("checked");
        $('input[id="pending-data"]').removeAttr("checked");
        $('input[id="all-data"]').prop("checked", true);
        CLEAR_FILTERED.hide();
        FILTERED_DATA.empty();
        buApprovePage.renderViewFromFilter();
    });

    FinalSubmit.click(function(){
        displayPopUp("submit", parseInt($('#view-csv-id').val()), null);
    });


    ApproveSelectAll.on("change", function(e) {
        if (buApprovePage.ViewDataList.length > 0) {
            $(".tbody-sm-approve-view .view-approve-check").prop('checked', false);
            $(".tbody-sm-approve-view .view-reject-check").prop('checked', false);
            $('.reject-reason .fa-info-circle').addClass("default-display-none");
            $('.tbody-sm-approve-view .view-approve-check').each(function(index, el) {
                var data = buApprovePage.ViewDataList[index];
                if (e.target.checked) {
                    $(this).prop("checked", true);
                    if (data) {
                        var csvid = $('#view-csv-id').val();
                        bu.updateActionFromView(
                            parseInt(csvid), data.sm_id, 1, null,
                            function(err, res) {
                                if (err != null) {
                                    buApprovePage.possibleFailures(err);
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


    RejectSelectAll.on("change", function(e) {
        CurrentPageSmId = [];
        if (buApprovePage.ViewDataList.length > 0
            && RejectSelectAll.prop('checked') == true) {

            displayViewRejectAllPopUp(function(reason) {
                console.log(reason);
                var viewReason = $('.view-reason').val();
                var i=0;
                $(".tbody-sm-approve-view .view-approve-check").prop('checked', false);
                $(".tbody-sm-approve-view .view-reject-check").prop('checked', false);

                $('.tbody-sm-approve-view .view-reject-check').each(function(index, el) {
                    var data = buApprovePage.ViewDataList[index];

                    if (e.target.checked) {
                        $(this).prop("checked", true);
                        $(".tbody-sm-approve-view th.reject-reason").find("*").removeClass("default-display-none");
                        $(".tbody-sm-approve-view th.reject-reason").find("*").attr("data-original-title", viewReason);
                        //$(".reject-reason").find(*)
                        if (data) {
                            var csvid = $('#view-csv-id').val();
                            bu.updateActionFromView(
                                parseInt(csvid), data.sm_id, 2, viewReason,
                                function(err, res) {
                                    if (err != null) {
                                        buApprovePage.possibleFailures(err);
                                    }
                            });
                        }
                    }
                    else {
                        $(this).find("*").prop("checked", false);
                        $(".tbody-sm-approve-view th.reject-reason").find("*").addClass("default-display-none");
                        $(".tbody-sm-approve-view th.reject-reason").find("*").attr("data-original-title","");
                        $('.tbody-sm-approve-view .view-reject-check').each(function(){
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
        /*$(".tbody-sm-approve-view th.reject-reason").find("*").addClass("default-display-none");
        $(".tbody-sm-approve-view th.reject-reason").find("*").attr("data-original-title","");*/

        }
    });

    ItemsPerPage.on("change", function(e) {
        pageLimit = parseInt(ItemsPerPage.val());
        tThis.showViewScreen(tThis.CSVID, 0, pageLimit);
    });
}

var buApprovePage = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    // $(".nicescroll").niceScroll();
    buApprovePage.showList()
});

$(".nicescroll").niceScroll();