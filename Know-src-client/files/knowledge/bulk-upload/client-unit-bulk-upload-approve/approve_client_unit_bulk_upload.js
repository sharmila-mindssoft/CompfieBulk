// Variable Declaration
var CLIENTGROUPLIST = [];
var TECHNOUSERLIST = [];
var CLIENTUNITCSVFILESLIST = [];
var VIEWCLIENTUNITLIST = [];
var LEGALENTITYLIST = [];
var DIVISIONLIST = [];
var CATEGORYLIST = [];
var UNITLOCATIONLIST = [];
var UNITCODELIST = [];
var DOMAINLIST = [];
var ORGANIZATIONLIST = [];
var USERCATEGORYID = 5;
var DOWNLOADFILE = null;

// Initialization of controls
var BTN_UPLOADED_FILELIST = $('.showbtn');
var PASSWORD_SUBMIT_BUTTON = $('.password-submit');
var CANCEL_BUTTON = $("#btn_cu_view_cancel");
var BTN_FILTER_GO = $('#btn_go');
var BTN_SUBMIT = $('.submitbtn');
var BULK_CLIENTUNIT_UPLOADED_FILELIST_VIEWPAGE = $(
    '#bulk_client_unit_uploaded_list_view'
);
var TBL_CLIENTUNIT_BULK_UPLOADED_LIST = $(
    '.tbody-bulk-client-unit-uploaded-file-list'
);
var BULK_CLIENTUNIT_UPLOADED_APPROVAL_LISTPAGE = $(
    '#bulk_clientunit_view_approve'
);
var TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST = $(
    '.tbody-bulk-client-unit-file-details'
);

var LBL_GROUP_NAME = $('.approve-group-name');
var LBL_CSV_FILENAME = $('.approve-file-name');
var LBL_CSV_FILEDATE = $('.approve-file-date');
var LBL_CSV_FILEUSER = $('.approve-file-user');

// Client Group auto complete controls
var SEARCH_GROUP_NAME = $('#search_group_name');
var SEARCH_GROUP_ID = $('#group_id');
var GROUP_LIST_BOX = $('#ac_group');
var GROUP_ULIST_CTRL = $('#ac-group ul');

// Filter Controls
var FILTER_LEGAL_ENTITY = $('#search_le_name');
var FILTER_LEGAL_ENTITY_NAME = $('#ac_legal_entity');
var FILTER_DIVISION = $('#search_division');
var FILTER_DIVISION_NAME = $('#ac_division');
var FILTER_CATEGORY = $('#search_category');
var FILTER_CATEGORY_NAME = $('#ac_category');
var FILTER_GEO_LOCATION = $('#search_geo_location');
var FILTER_GEO_NAME = $('#ac_geography');
var FILTER_UNIT_CODE = $('#search_unit_code');
var FILTER_UNIT_CODE_NAME = $('#ac_unit_code');
var FILTER_DOMAIN = $('#search_domain');
var FILTER_DOMAIN_NAME = $('#ac_domain');
var FILTER_ORGANIZATION = $('#search_organization');
var FILTER_ORGANIZATION_NAME = $('#ac_organization');
var APPROVE_ALL_UNITS = $('.select_all_approve');
var REJECT_ALL_UNITS = $('.select_all_reject');

var CURRENT_PASSWORD = null;
var REJECT_REASON = null;
var IS_AUTHENTICATE = false;
var CSVID = null;

var ITEMS_PER_PAGE = $('#items_per_page');
var PAGINATION_VIEW = $('.pagination-view');
var _ON_CURRENT_PAGE = 1;
var TOTAL_RECORD = 0;
var _PAGE_LIMIT = 25;
var _SHOW_FROM = 0;
var _SHOW_CLICKED = true;
var _FILTER_CLICKED = true;

// To load the client groups under logged techno executive
function initialize(type_of_initialization) {
    displayPage(type_of_initialization);
    if (type_of_initialization == "list") {
        displayLoader();
        bu.getClientGroupsList(function(error, response) {
            if (error == null) {
                CLIENTGROUPLIST = response.client_group_list;
                bu.getTechnoUserDetails(
                    parseInt(USERCATEGORYID), function(error, response)
                {
                    if(error == null) {
                        TECHNOUSERLIST = response.techno_info;
                        hideLoader();
                    }
                    else {
                        displayMessage(error);
                        hideLoader();
                    }
                });
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    }
}

// Displays the client unit bulk uploaded files list
BTN_UPLOADED_FILELIST.click(function() {
    var ClientId = null, GroupName = null;
    if (SEARCH_GROUP_ID.val() != '') {
        ClientId = parseInt(SEARCH_GROUP_ID.val().trim());
        GroupName = SEARCH_GROUP_NAME.val().trim();
        displayLoader();
        function onSuccess(data) {
            CLIENTUNITCSVFILESLIST = data.bu_cu_csv_files_list;
            loadClientUnitCSVFilesList(CLIENTUNITCSVFILESLIST);
        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        bu.getClientGroupsClientUnitFilesList(
            ClientId, GroupName, function(error, response)
        {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    } else {
        displayMessage(message.cg_required);
    }
});


// To display the uploaded CSV files list
function loadClientUnitCSVFilesList(data) {
    var sno = 0;
    var TableRow = null, clone = null, SplitFileName = null;
    var App_Rej = 0;
    var NoRecordRow = null;
    if(data.length > 0) {
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.empty();
        $.each(data, function(key, value) {
            TableRow = $(
                '#templates .table-bulk-client-unit-uploaded-file-list ' +
                '.table-row'
            );
            clone = TableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            cname_split = value.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            $('.uploaded-file-name', clone).text(cname);
            $('#csvUnitID', clone).val(value.csv_id);
            $('.uploaded-on', clone).text(value.uploaded_on);
            $('.uploaded-by', clone).text(fetchTechnoManager(value.uploaded_by));
            $('.no-of-units', clone).text(value.no_of_records);
            TOTAL_RECORD = value.no_of_records;
            App_Rej = value.approved_count + " / " + value.rej_count;
            $('.approved-rejected', clone).text(App_Rej);

            $('.download-invalidfile', clone).html(
                '<i class="fa fa-download text-primary c-pointer dropbtn" ' +
                'onClick="showFormats('+value.csv_id+')" title="Click here to download" />'
            );
            $('.download-invalidfile', clone).append
            (
                $('<div/>')
                .addClass("dropdown-content default-display-none")
                .attr("id","myDropdown-"+value.csv_id)
            );
            SplitFileName = value.csv_name.split(".")[0];
            $('.download-invalidfile #myDropdown-'+value.csv_id, clone).append
            (
                $('<a/>')
                .text("Download Excel")
                .addClass("dl-xls-file-"+value.csv_id)
                .attr("href","/uploaded_file/xlsx/"+SplitFileName+'.xlsx'),
                $('<a/>')
                .text("Download CSV")
                .addClass("dl-csv-file-"+value.csv_id)
                .attr("href","/uploaded_file/csv/"+SplitFileName+'.csv'),
                $('<a/>')
                .text("Download ODS")
                .addClass("dl-ods-file-"+value.csv_id)
                .attr("href","/uploaded_file/ods/"+SplitFileName+'.ods'),
                $('<a/>')
                .text("Download Text")
                .addClass("dl-txt-file-"+value.csv_id)
                .on("click",function(){
                    $.get(
                        "/uploaded_file/txt/" + SplitFileName+".txt",
                        function(data)
                        {
                           download(SplitFileName+".txt", "text/plain", data);
                        },
                    'text');
                })
            );

            //approve all
            $('.approve-checkbox', clone).on('change', function(e){
                if (e.target.checked){
                    displayPopUp('approve_all', value.csv_id, null, e);
                }
            });

            //reject all
            $('.reject-checkbox', clone).on('change', function(e){
                if(e.target.checked){
                    displayPopUp('reject_all', value.csv_id, null, e);
                }
            });

            if(
                value.approved_count > 0 ||
                value.rej_count > 0 ||
                value.declined_count > 0
            ){
                $('.viewbtn', clone).hide();
                $('.editbtn', clone).show();
                _SHOW_CLICKED = true;
                _FILTER_CLICKED = false;
                APPROVE_ALL_UNITS.prop("checked", false);
                REJECT_ALL_UNITS.prop("checked", false);
                $('.editbtn', clone).on('click', function(){
                    displayViewScreen(value.csv_id, 0, 25);
                });
            } else {
                $('.viewbtn', clone).show();
                $('.editbtn', clone).hide();
                _SHOW_CLICKED = true;
                _FILTER_CLICKED = false;
                APPROVE_ALL_UNITS.prop("checked", false);
                REJECT_ALL_UNITS.prop("checked", false);
                $('.viewbtn', clone).on('click', function(){
                    displayViewScreen(value.csv_id, 0, 25);
                });
            }
            TBL_CLIENTUNIT_BULK_UPLOADED_LIST.append(clone);
        });
    } else {
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.empty();
        NoRecordRow = $("#templates .table-no-record tr");
        clone = NoRecordRow.clone();
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.append(clone);
    }
    /*$('.js-filtertable-view').each(function() {
        $(this).filtertable().addFilter('.js-filter-main');
    });*/
    hideLoader();
}

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:' + mime_type + ';' +
        'charset=utf-8,' + encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

// Fetch the employee code and name from the datalist for the uploaded user
function fetchTechnoManager(executiveId) {
    data = TECHNOUSERLIST;
    var Executive_Name_Code = null;
    $.each(data, function(key, value) {
        if(value.user_id == executiveId){
            Executive_Name_Code = value.emp_code_name;
        }
    });
    return Executive_Name_Code;
}

// To display invalid files download formats
function showFormats(arg) {
    document.getElementById("myDropdown-"+arg).classList.toggle("show");
}

function keySearchUnitsFilesList(data) {
    keyFileName = $('#uploaded_file_name').val().toLowerCase();
    keyUplOn = $('#uploaded_on').val().toLowerCase();
    keyUplBy = $('#uploaded_by').val().toLowerCase();
    keyTotalUnits = $('#total_units').val().toLowerCase();
    var mList = [];
    var d;
    for (d in data) {
        var valueFileName = data[d].csv_name.toLowerCase();
        var valueUplOn = data[d].uploaded_on.toLowerCase();
        var valueUplBy = fetchTechnoManager(data[d].uploaded_by).toString().toLowerCase();
        var valueTotalUnits = data[d].no_of_records.toString();
        if ((~valueFileName.indexOf(keyFileName)) &&
            (~valueUplOn.indexOf(keyUplOn)) &&
            (~valueUplBy.indexOf(keyUplBy)) &&
            (~valueTotalUnits.indexOf(keyTotalUnits))
        ) {
            mList.push(data[d]);
        }
    }
    return mList;
}

function displayPopUp(TYPE, csv_id, b_u_id, evt){
    if (TYPE == "reject_all") {
        targetid = "#custom-modal";
        CURRENT_PASSWORD = $('#current_password_reject');
        REJECT_REASON = $('.rej-all-reason');
        CURRENT_PASSWORD.val('');
        REJECT_REASON.val('');
        REJECT_REASON.keyup(function(e){
            if (e.keyCode== 13)
                validateAuthentication();
        });
    }
    else if (TYPE == "approve_all" || TYPE =="submit") {
        targetid = "#custom-modal-approve"
        CURRENT_PASSWORD = $('#current_password');
        CURRENT_PASSWORD.val('');
        REJECT_REASON = null;
        CURRENT_PASSWORD.keyup(function(e){
            if (e.keyCode == 13)
                validateAuthentication();
        });
    }
    else if (TYPE == "view-reject") {
        targetid = "#custom-modal-remarks";
        CURRENT_PASSWORD = null;
        REJECT_REASON = $('.view-reason');
        REJECT_REASON.focus();
        REJECT_REASON.val('');
        REJECT_REASON.keyup(function(e){
            if (e.keyCode == 13)
                validateAuthentication();
        });
    }

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            if (REJECT_REASON != null) {
                REJECT_REASON.val('');
            }
            IS_AUTHENTICATE = false;
        },
        close: function() {
            if (IS_AUTHENTICATE) {
                displayLoader();
                setTimeout(function() {
                    if (TYPE == "approve_all") {
                        performApproveRejectAction(
                            csv_id, 1, CURRENT_PASSWORD.val(), null
                        );
                    }
                    else if (TYPE == "reject_all") {
                        performApproveRejectAction(
                            csv_id, 2, CURRENT_PASSWORD.val(),
                            $('.rej-all-reason').val()
                        );
                    }
                    else if (TYPE == "view-reject") {
                        bu.updateClientUnitActionFromView(
                            csv_id, b_u_id, 2, $('.view-reason').val(),
                            function(err, res)
                        {
                            if (err != null) {
                                displayMessage(err);
                            }
                            else {
                                //$('.view-approve-check-' + b_u_id).prop("checked", false);
                                loadRemarksOnView(
                                    b_u_id, $('.view-reason').val()
                                );
                            }
                            hideLoader();
                        });
                    }
                    else if (TYPE == "submit") {
                        submitAction(csv_id, 4, CURRENT_PASSWORD.val(), null)
                    }
                }, 500);
            }
            else {
                evt.target.checked = false;
            }
        },
    });
}

// Reject all check box in view units list screen
function displayViewRejectAllPopUp(callback){
    targetid = "#custom-modal-remarks";
    CURRENT_PASSWORD = null;
    REJECT_REASON = $('.view-reason');
    REJECT_REASON.focus();
    REJECT_REASON.val('');
    REJECT_REASON.keyup(function(e){
        if (e.keyCode == 13)
            validateAuthentication();
    });

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            else if (REJECT_REASON != null) {
                REJECT_REASON.val('');
            }
            IS_AUTHENTICATE = false;
        },
        close: function() {
            if (IS_AUTHENTICATE) {
                displayLoader();
                setTimeout(function() {
                    var rejectReason = REJECT_REASON.val()
                    if (REJECT_REASON.val() == '') {
                        displayMessage(message.reason_required);
                        hideLoader();
                    }
                    else {
                        callback($('.view-reason').val());
                    }
                }, 500);
            } else {
                REJECT_ALL_UNITS.prop("checked", false);
                hideLoader();
                //callback($('.view-reason').val());
            }
        },
    });
}

// To perform approve all or reject all action from main list
function performApproveRejectAction(csv_id, actionType, pwd, remarksText){
    displayLoader();
    bu.performClientUnitApproveReject(
        csv_id, actionType, remarksText, pwd,
        parseInt(SEARCH_GROUP_ID.val().trim()),
        function(error, response) {
        if (error == null) {
            if (actionType == 1) {
                displaySuccessMessage(message.approve_success);
                initialize('list');
            }
            else {
                displaySuccessMessage(message.reject_success);
            }
            initialize('list');
        }
        else
        {
            hideLoader();
            if(error == "ReturnDeclinedCount")
            {
                var declinedCount = response.declined_count;
                if(response.rejected_count > 0) {
                    setTimeout(function() {
                        msg = message.manuval_rejected_confirm;
                        confirm_alert(msg, function(isConfirm) {
                            if (isConfirm) {
                                performApproveRejectDeclination(
                                    csv_id, actionType, pwd,
                                    remarksText, declinedCount
                                );
                            }
                        });
                    }, 500);
                }
                else if(declinedCount > 0) {
                    performApproveRejectDeclination(
                        csv_id, actionType, pwd,
                        remarksText, declinedCount
                    );
                }
            } else {
                displayMessage(error);
            }
        }
    });
}

function performApproveRejectDeclination(
    csv_id, actionType, pwd, remarksText, declined_count
) {
    if (declined_count > 0) {
        setTimeout(function() {
            msg_decl = declined_count +
                " units declined, Do you want to continue ?";
            confirm_alert(msg_decl, function(isConfirm) {
                if (isConfirm) {
                    bu.confirmClientUnitDeclination(
                        csv_id, parseInt(SEARCH_GROUP_ID.val().trim()),
                    function(error, response)
                    {
                        if (error == null) {
                            displaySuccessMessage(message.approve_success);
                            initialize('list');
                        } else {
                            displayMessage(error)
                        }
                    });
                }
            });
        }, 500);
    } else {
        bu.confirmClientUnitDeclination(
            csv_id, parseInt(SEARCH_GROUP_ID.val().trim()),
        function(error, response)
        {
            if (error == null) {
                displaySuccessMessage(message.approve_success);
                initialize('list');
            }
            else {
                displayMessage(error)
            }
        });
    }
}

// To handle submit action of total view
BTN_SUBMIT.click(function(){
    csvid = $('#view_csv_unit_id').val();
    displayPopUp('submit', parseInt(csvid), 0, null);
});

function submitAction(csv_id, actionType, pwd, remarksText) {
    displayLoader();
    bu.submitClientUnitActionFromView(
        csv_id, actionType, remarksText, pwd,
        parseInt(SEARCH_GROUP_ID.val().trim()),
    function(error, response){
        if (error == null) {
            if (actionType == 4) {
                displaySuccessMessage(message.action_selection_success);
                BULK_CLIENTUNIT_UPLOADED_FILELIST_VIEWPAGE.show();
                BULK_CLIENTUNIT_UPLOADED_APPROVAL_LISTPAGE.hide();
                initialize('list');
            }
        }
        else{
            hideLoader();
            if(error == "InvalidPassword"){
                displayMessage(
                    "Invalid Password"
                );
            }
            if(error == "ReturnDeclinedCount") {
                if(response.declined_count > 0){
                    msg = response.declined_count +
                        " units declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            bu.confirmSubmitClientUnitFromView(
                                csv_id, parseInt(SEARCH_GROUP_ID.val().trim()),
                                function(error, response)
                                {
                                    if (error == null) {
                                        displaySuccessMessage(
                                            message.action_selection_success
                                        );
                                        BULK_CLIENTUNIT_UPLOADED_FILELIST_VIEWPAGE.show();
                                        BULK_CLIENTUNIT_UPLOADED_APPROVAL_LISTPAGE.hide();
                                        initialize('list');
                                    }
                                }
                            );
                        }
                    });
                }
            }
            else if (error == "SubmitClientUnitActionFromListFailure"){
                displayMessage(
                    "All the units should be selected before Submit."
                );
            }
        }
    });
}

// To validate the password inputted in custom box
function validateAuthentication() {
    var Password = null, Rej_Reason = null;
    if (CURRENT_PASSWORD != null) {
        Password = CURRENT_PASSWORD.val().trim();
    }
    if (REJECT_REASON != null){
        Rej_Reason = REJECT_REASON.val().trim();
    }
    if (CURRENT_PASSWORD != null && Password.length == 0) {
        displayMessage(message.password_required);
        CURRENT_PASSWORD.focus();
        return false;
    }else if((CURRENT_PASSWORD != null) && (
        isLengthMinMax(
            CURRENT_PASSWORD, 1, 20,
            message.password_20_exists
        )) == false
    ){
        return false;
    } else if(REJECT_REASON != null && Rej_Reason.length == 0) {
        displayMessage(message.reason_required);
        REJECT_REASON.focus();
        return false;
    }else if((REJECT_REASON != null) && (
        isLengthMinMax(
            REJECT_REASON, 1, 500,
            "Reason should not exceed 500 characters"
        )) == false
    ){
        return false;
    }
    else {
        if(Password != null){
            mirror.verifyPassword(Password, function(error, response) {
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
        else
        {
            IS_AUTHENTICATE = true;
            Custombox.close();
        }
    }
    displayLoader();
}

// To navigate to the approval list page of a selected csv file
function displayViewScreen(csv_id, start_count, _PAGE_LIMIT) {
    BULK_CLIENTUNIT_UPLOADED_FILELIST_VIEWPAGE.hide();
    BULK_CLIENTUNIT_UPLOADED_APPROVAL_LISTPAGE.show();
    _PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    if (_ON_CURRENT_PAGE == 1) {
        _SHOW_FROM = 0
    } else {
        _SHOW_FROM = (_ON_CURRENT_PAGE - 1) * _PAGE_LIMIT;
    }
    getCSVFileApprovalList(csv_id, _SHOW_FROM, _PAGE_LIMIT);
}

//To display the approval units list
function getCSVFileApprovalList(csv_id, start_count, _PAGE_LIMIT) {
    displayLoader();
    var cname_split = "", cname = "";
    bu.getBulkClientUnitApproveRejectList(
        csv_id, start_count, _PAGE_LIMIT, function(error, response){
        if (error == null) {
            VIEWCLIENTUNITLIST = response.client_unit_data;
            LEGALENTITYLIST = response.le_names;
            DIVISIONLIST = response.div_names;
            CATEGORYLIST = response.cg_names;
            UNITLOCATIONLIST = response.unit_locations;
            UNITCODELIST = response.unit_codes;
            DOMAINLIST = response.bu_domain_names;
            ORGANIZATIONLIST = response.orga_names;
            LBL_GROUP_NAME.text(response.bu_group_name);
            cname_split = response.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            LBL_CSV_FILENAME.text(cname);
            LBL_CSV_FILEDATE.text(response.uploaded_on);
            LBL_CSV_FILEUSER.text(fetchTechnoManager(response.uploaded_by));
            TOTAL_RECORD = response.total_records;
            $('#view_csv_unit_id').val(response.csv_id);
            CSVID = response.csv_id;
            if(TOTAL_RECORD == 0) {
                hidePagePan();
                PAGINATION_VIEW.hide();
                hidePageView();
            }
            else {
                if (_ON_CURRENT_PAGE == 1) {
                    createPageView();
                    PAGINATION_VIEW.show();
                }
            }
            bindClientUnitList(VIEWCLIENTUNITLIST);
            hideLoader();
        }
        else {
            if(error != null) {
                if (error == "EmptyFilteredData") {
                    TOTAL_RECORD = 0;
                    hidePagePan();
                    PAGINATION_VIEW.hide();
                    hidePageView();
                    bindClientUnitList([]);
                } else {
                    displayMessage(error);
                }
                hideLoader();
            }
        }
    });
}

// To load the remarks after successful rejection
function loadRemarksOnView(b_u_id, remarksText) {
    var ViewList = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
        find('tr').length;
    var ReasonIconCtrl = null, RejectTool = null, ViewApproveCtrl = null;
    var i = 0;
    for (i=0; i<ViewList; i++) {
        ReasonIconCtrl = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('tr')[i].cells[3];
        if (ReasonIconCtrl.className.indexOf(b_u_id) != -1) {
            if(remarksText != null){
                RejectTool = (
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 ' +
                    'text-primary c-pointer "' +
                    'data-original-title="' + remarksText + '" ' +
                    'data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
                ReasonIconCtrl.innerHTML = RejectTool;
            }
        }
        ViewApproveCtrl = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('tr')[i].cells[1].getElementsByTagName('input')[0];
        if (ViewApproveCtrl.className.indexOf(b_u_id) != -1) {
            ViewApproveCtrl.checked = false;
        }
    }
}

// To load the remarks after successful rejection
function loadRemarksOnViewRejectAll(remarksText) {
    var ViewList = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
        find('tr').length;
    var i = 0;
    var ReasonIconCtrl = null, RejectTool = null;
    for (i=0; i<ViewList; i++) {
        value = VIEWCLIENTUNITLIST[i];
        b_u_id = value.bulk_unit_id;
        ReasonIconCtrl = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('tr')[i].cells[3];
        if (ReasonIconCtrl.className.indexOf(b_u_id) != -1) {
            if(remarksText != null){
                RejectTool = (
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 ' +
                    'text-primary c-pointer "'+
                    'data-original-title="' + remarksText + '" ' +
                    'data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
                ReasonIconCtrl.innerHTML = RejectTool;
            }
        }
    }
}

// Bind data to view data list
function bindClientUnitList(data){
    var sno = 0;
    sno = _SHOW_FROM;
    var TableRow = null, CloneRow = null, Clone = null, NoRecordRow = null;
    if(data.length > 0) {
        APPROVE_ALL_UNITS.prop("checked", false);
        REJECT_ALL_UNITS.prop("checked", false);
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.empty();
        $.each(data, function(key, value) {
            sno += 1;
            TableRow = $(
                '#templates .table-bulk-client-unit-file-details .table-row'
            );
            CloneRow = TableRow.clone();

            $('.sno', CloneRow).text(sno);
            $('.reject-reason', CloneRow).addClass("-"+value.bulk_unit_id);
            $('.view-approve-check', CloneRow).addClass("-"+value.bulk_unit_id);
            $('.view-reject-check', CloneRow).addClass("-"+value.bulk_unit_id);
            if(value.bu_remarks != null && value.bu_remarks != ''){
                $('.reject-reason', CloneRow).append(
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 ' +
                    'text-primary c-pointer "' +
                    'data-original-title="' + value.bu_remarks + '" ' +
                    'data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
            }
            // $('.legal-entity-name', CloneRow).text(value.bu_le_name);
            $('.legal-entity-name', CloneRow).append(
                '&nbsp;&nbsp;<i class="fa fa-info-circle fa-1-2x l-h-51 ' +
                'text-primary c-pointer "' +
                'data-original-title="Country : ' + value.country_name + '" ' +
                'data-toggle="tooltip"></i>' + value.bu_le_name
            );
            $('[data-toggle="tooltip"]').tooltip();
            $('.division-name', CloneRow).text(value.bu_division_name);
            $('.category-name', CloneRow).text(value.bu_category_name);
            $('.geography-level', CloneRow).text(value.bu_geography_level);
            $('.unit-location', CloneRow).text(value.bu_unit_location);
            $('.unit-code', CloneRow).text(value.bu_unit_code);
            $('.unit-name', CloneRow).text(value.bu_unit_name);
            $('.unit-address', CloneRow).text(value.bu_address);
            $('.city-name', CloneRow).text(value.bu_city);
            $('.state-name', CloneRow).text(value.bu_state);
            $('.postal-code', CloneRow).text(value.bu_postal_code);
            var dn = null, org = null;
            var d_names = null;
            var o_names = null;
            if (value.bu_domain.indexOf("|;|") >= 0) {
                dn = value.bu_domain.split('|;|');
                org = value.bu_orgn.split('|;|');

                for(var i=0;i<dn.length;i++) {
                    if (i == 0)
                        d_names = dn[i] + "<br />";
                    else {
                        d_names = d_names + dn[i] + "<br />";
                    }
                    if (o_names == null)
                        o_names = "<strong>"+dn[i]+"</strong><br />";
                    else
                        o_names = o_names +
                        "<br /><strong>"+dn[i]+"</strong><br />";

                    for(var j=0;j<org.length;j++) {
                        d_o = org[j].split(">>");
                        if(dn[i].trim() == d_o[0].trim()) {
                            o_names = o_names + d_o[1].trim() + ",";
                        }

                    }
                }
            } else {
                dn = value.bu_domain;
                org = value.bu_orgn.split('|;|');
                d_names = dn;
                o_names = "<strong>"+dn+"</strong><br />";
                for(var i=0;i<org.length;i++) {
                    if (dn == org[i].split('>>')[0].trim()) {
                        o_names = o_names + org[i].split(">>")[1].trim()+","
                    }
                }
            }
            $('.domain', CloneRow).html(d_names);
            $('.organization', CloneRow).html(
                o_names.substring(0,o_names.length -1)
            );

            if (parseInt(value.bu_action) == 1) {
                $('.view-approve-check.-'+value.bulk_unit_id,CloneRow).attr("checked", true);
                $('.view-reject-check.-'+value.bulk_unit_id,CloneRow).attr("checked", false);
            }
            else if (parseInt(value.bu_action) == 2){
                $('.view-approve-check.-'+value.bulk_unit_id,CloneRow).attr("checked", false);
                $('.view-reject-check.-'+value.bulk_unit_id,CloneRow).attr("checked", true);
            }
            else if (parseInt(value.bu_action) == 0){
                $('.view-approve-check.-'+value.bulk_unit_id,CloneRow).attr("checked", false);
                $('.view-reject-check.-'+value.bulk_unit_id,CloneRow).attr("checked", false);
            }

            $('.view-approve-check', CloneRow).on('change', function(e){
                if (e.target.checked){
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id, 1,
                        null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                '.view-reject-check.-'+value.bulk_unit_id
                            ).attr("checked", false);
                        }
                    });
                }
                else {
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id,
                        0, null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                '.view-reject-check.-'+value.bulk_unit_id
                            ).attr("checked", false);
                        }
                    });
                }
            });
            $('.view-reject-check', CloneRow).on('change', function(e){
                if(e.target.checked){
                    csvid = $('#view_csv_unit_id').val();
                    displayPopUp(
                        'view-reject', parseInt(csvid), value.bulk_unit_id, e
                    );
                }
                else {
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id, 0,
                        null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                                '.view-approve-check.-'+value.bulk_unit_id
                            ).attr("checked", false);
                        }
                    });
                }
            });

            TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.append(CloneRow);
        });
        showPagePan((_SHOW_FROM + 1), sno, TOTAL_RECORD);
    } else {
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.empty();
        NoRecordRow = $("#templates .approval-table-no-record tr");
        Clone = NoRecordRow.clone();
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.append(Clone);
        hidePagePan();
    }
}


function keySearchUnitsDetailsList(data) {
    keyLE = $('#filter_legal_entity').val().toLowerCase();
    keyDivision = $('#filter_division').val().toLowerCase();
    keyCategory = $('#filter_category').val().toLowerCase();
    keyGeography = $('#filter_geo_level').val().toLowerCase();
    keyUnitLocation = $('#filter_location').val().toLowerCase();
    keyUnitCode = $('#filter_unit_code').val().toLowerCase();
    keyUnitName = $('#filter_unit_name').val().toLowerCase();
    keyAddress = $('#filter_address').val().toLowerCase();
    keyCity = $('#filter_city').val().toLowerCase();
    keyState = $('#filter_state').val().toLowerCase();
    keyPostCode = $('#filter_post_code').val().toLowerCase();
    keyDomain = $('#filter_domain').val().toLowerCase();
    keyOrgn = $('#filter_orgn').val().toLowerCase();
    var fList = [];
    var d;
    for (d in data) {
        console.log("2:"+data[d].bu_geography_level.toLowerCase());
        var valueLE = data[d].bu_le_name.toLowerCase();
        var valueDivision = data[d].bu_division_name.toLowerCase();
        var valueCategory = data[d].bu_category_name.toLowerCase();
        var valueGeography = data[d].bu_geography_level.toLowerCase();
        var valueUnitLocation = data[d].bu_unit_location.toLowerCase();
        var valueUnitCode = data[d].bu_unit_code.toLowerCase();
        var valueUnitName = data[d].bu_unit_name.toLowerCase();
        var valueAddress = data[d].bu_address.toLowerCase();
        var valueCity = data[d].bu_city.toLowerCase();
        var valueState = data[d].bu_state.toLowerCase();
        var valuePostCode = data[d].bu_postal_code.toLowerCase();
        var valueDomain = data[d].bu_domain.toLowerCase();
        var valueOrgn = data[d].bu_orgn.toLowerCase();
        if ((~valueLE.indexOf(keyLE)) &&
            (~valueDivision.indexOf(keyDivision)) &&
            (~valueCategory.indexOf(keyCategory)) &&
            (~valueGeography.indexOf(keyGeography))
            && (~valueUnitLocation.indexOf(keyUnitLocation))
            && (~valueUnitCode.indexOf(keyUnitCode))
            && (~valueUnitName.indexOf(keyUnitName))
            && (~valueAddress.indexOf(keyAddress))
            && (~valueCity.indexOf(keyCity))
            && (~valueState.indexOf(keyState))
            && (~valuePostCode.indexOf(keyPostCode))
            && (~valueDomain.indexOf(keyDomain))
            && (~valueOrgn.indexOf(keyOrgn))
        ) {
            fList.push(data[d]);
            console.log("3");
        }
    }
    console.log("4:"+fList.length);
    return fList;
}

// To display the page as per request
function displayPage(page_mode) {
    var NoRecordRow = null, Clone = null;
    if (page_mode == "list") {
        SEARCH_GROUP_ID.val('');
        SEARCH_GROUP_NAME.val('');
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.empty();
        NoRecordRow = $("#templates .table-no-record tr");
        Clone = NoRecordRow.clone();
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.append(Clone);
    }
}

// To invoke loading of client groups list
SEARCH_GROUP_NAME.keyup(function(e){
    var text_val = $(this).val();
    var NoRecordRow = null, Clone = null;
    if (text_val != '') {
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
          e, GROUP_LIST_BOX, SEARCH_GROUP_ID, text_val,
          CLIENTGROUPLIST, "group_name", "client_id", function (val) {
              onAutoCompleteSuccess(SEARCH_GROUP_NAME, SEARCH_GROUP_ID, val);
        }, condition_fields, condition_values);
    } else {
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.empty();
        NoRecordRow = $("#templates .table-no-record tr");
        Clone = NoRecordRow.clone();
        TBL_CLIENTUNIT_BULK_UPLOADED_LIST.append(Clone);
    }

});

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

PASSWORD_SUBMIT_BUTTON.click(function(){
    if (CURRENT_PASSWORD != null) {
        validateAuthentication();
    }
    else if (REJECT_REASON != null) {
        validateAuthentication();
    }
    else {
        IS_AUTHENTICATE = true;
        Custombox.close();
        displayLoader();
    }
});

CANCEL_BUTTON.click(function() {
    BULK_CLIENTUNIT_UPLOADED_FILELIST_VIEWPAGE.show();
    BULK_CLIENTUNIT_UPLOADED_APPROVAL_LISTPAGE.hide();
    $('.clear-filtered').hide();
    $('.filtered_items').text('');
    filterHead = null;
    _SHOW_CLICKED = false;
    _FILTER_CLICKED = false;
    actionVal = 0;
    $('.all-data').prop('checked', true);
    FILTER_LEGAL_ENTITY.val('');
    FILTER_DIVISION.val('');
    FILTER_CATEGORY.val('');
    FILTER_UNIT_CODE.val('');
    FILTER_GEO_LOCATION.val('');
    FILTER_DOMAIN.val('');
    FILTER_ORGANIZATION.val('');
    $('#filter_legal_entity').val('');
    $('#filter_division').val('');
    $('#filter_category').val('');
    $('#filter_geo_level').val('');
    $('#filter_location').val('');
    $('#filter_unit_code').val('');
    $('#filter_unit_name').val('');
    $('#filter_address').val('');
    $('#filter_city').val('');
    $('#filter_state').val('');
    $('#filter_post_code').val('');
    $('#filter_domain').val('');
    $('#filter_orgn').val('');
    _PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    _ON_CURRENT_PAGE = 1;
    _SHOW_FROM = 0;
    BTN_UPLOADED_FILELIST.trigger('click');
});

// filter display

$('.right-bar-toggle').on('click', function(e) {
  $('#wrapper').toggleClass('right-bar-enabled');
});

FILTER_LEGAL_ENTITY.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_LEGAL_ENTITY_NAME, text_val,
        LEGALENTITYLIST, function (val) {
            FILTER_LEGAL_ENTITY.val(val[0].trim())
        }
    );
});

FILTER_DIVISION.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_DIVISION_NAME, text_val,
        DIVISIONLIST, function (val) {
            FILTER_DIVISION.val(val[0])
        }
    );
});

FILTER_CATEGORY.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_CATEGORY_NAME, text_val,
        CATEGORYLIST, function (val) {
            FILTER_CATEGORY.val(val[0])
        }
    );
});

FILTER_GEO_LOCATION.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_GEO_NAME, text_val,
        UNITLOCATIONLIST, function (val) {
            FILTER_GEO_LOCATION.val(val[0])
        }
    );
});

FILTER_UNIT_CODE.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_UNIT_CODE_NAME, text_val,
        UNITCODELIST, function (val) {
            FILTER_UNIT_CODE.val(val[0])
        }
    );
});

FILTER_DOMAIN.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_DOMAIN_NAME, text_val,
        DOMAINLIST, function (val) {
            FILTER_DOMAIN.val(val[0])
        }
    );
});

FILTER_ORGANIZATION.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, FILTER_ORGANIZATION_NAME, text_val,
        ORGANIZATIONLIST, function (val) {
            FILTER_ORGANIZATION.val(val[0])
        }
    );
});

BTN_FILTER_GO.click(function(){
    var filterHead = null;
    _SHOW_CLICKED = false;
    _FILTER_CLICKED = true;
    actionVal = 0;
    if ($('.verified-data').prop('checked')) {
        actionVal = 2;
        if (filterHead == null)
            filterHead = "View Data : Verified" + " | ";
        else
            filterHead = filterHead + "View Data : Verified" + " | ";
    }
    if ($('.pending-data').prop('checked')) {
        actionVal = 1;
        if (filterHead == null)
            filterHead = "View Data : Pending" + " | ";
        else
            filterHead = filterHead + "View Data : Pending" + " | ";
    }
    if ($('.all-data').prop('checked')) {
        if (filterHead == null)
            filterHead = "View Data : All" + " | ";
        else
            filterHead = filterHead + "View Data : All" + " | ";
    }
    if (FILTER_LEGAL_ENTITY.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Legal Entity : " +
            FILTER_LEGAL_ENTITY.val().trim() + " ";
        else
            filterHead = filterHead + "Legal Entity : " +
            FILTER_LEGAL_ENTITY.val().trim() + " | ";
    }

    if (FILTER_DIVISION.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Division : " + FILTER_DIVISION.val().trim() + " ";
        else
            filterHead = filterHead + "Division : " +
            FILTER_DIVISION.val().trim() + " | ";
    }

    if (FILTER_CATEGORY.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Category : " + FILTER_CATEGORY.val().trim() + " ";
        else
            filterHead = filterHead + "Category : " +
            FILTER_CATEGORY.val().trim() + " | ";
    }

    if (FILTER_GEO_LOCATION.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Location : " +
            FILTER_GEO_LOCATION.val().trim() + " ";
        else
            filterHead = filterHead + "Unit Location : " +
            FILTER_GEO_LOCATION.val().trim() + " | ";
    }

    if (FILTER_UNIT_CODE.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Code : " + FILTER_UNIT_CODE.val().trim() + " ";
        else
            filterHead = filterHead + "Unit Code : " +
            FILTER_UNIT_CODE.val().trim() + " | ";
    }

    if (FILTER_DOMAIN.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Domain : " + FILTER_DOMAIN.val().trim() + " ";
        else
            filterHead = filterHead + "Domain : " +
            FILTER_DOMAIN.val().trim() + " | ";
    }

    if (FILTER_ORGANIZATION.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Organization : " +
            FILTER_ORGANIZATION.val().trim() + " ";
        else
            filterHead = filterHead + "Organization : " +
            FILTER_ORGANIZATION.val().trim() + " | ";
    }
    $('.filtered_items').text("Filtered By - " + filterHead);
    if(filterHead.length > 0){
        $('.clear-filtered').show();
    } else {
        $('.clear-filtered').hide();
        $('.filtered_items').text('');
    }
    _PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    _ON_CURRENT_PAGE = 1;
    _SHOW_FROM = 0;
    bu.getBulkClientUnitListForFilterView(
        parseInt($('#view_csv_unit_id').val()), _SHOW_FROM, _PAGE_LIMIT,
        FILTER_LEGAL_ENTITY.val().trim(), FILTER_DIVISION.val().trim(),
        FILTER_CATEGORY.val().trim(), FILTER_GEO_LOCATION.val().trim(),
        FILTER_UNIT_CODE.val().trim(), FILTER_DOMAIN.val().trim(),
        FILTER_ORGANIZATION.val().trim(), actionVal,
        function(err, response)
        {
        displayLoader();
        if(err != null) {
            if (err == "EmptyFilteredData") {
                TOTAL_RECORD = 0;
                hidePagePan();
                PAGINATION_VIEW.hide();
                hidePageView();
                bindClientUnitList([]);
            } else {
                displayMessage(err);
            }
            hideLoader();
        }
        if(err == null) {
            VIEWCLIENTUNITLIST = response.client_unit_data;
            LBL_GROUP_NAME.text(response.bu_group_name);
            var cname_split = "", cname = "";
            cname_split = response.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            LBL_CSV_FILENAME.text(cname);
            LBL_CSV_FILEDATE.text(response.uploaded_on);
            LBL_CSV_FILEUSER.text(fetchTechnoManager(response.uploaded_by));
            $('#view_csv_unit_id').val(response.csv_id);
            CSVID = response.csv_id;
            TOTAL_RECORD = response.total_records;
            if(TOTAL_RECORD == 0) {
                hidePagePan();
                PAGINATION_VIEW.hide();
                hidePageView();
            }
            else {
                if (_ON_CURRENT_PAGE == 1) {
                    createPageView();
                    PAGINATION_VIEW.show();
                }
            }
            bindClientUnitList(VIEWCLIENTUNITLIST);
            hideLoader();
        }
    });
});

$('.clear-filtered').click(function() {
    $('.clear-filtered').hide();
    $('.filtered_items').text('');
    filterHead = null;
    _SHOW_CLICKED = true;
    _FILTER_CLICKED = false;
    actionVal = 0;
    $('.all-data').prop('checked', true);
    FILTER_LEGAL_ENTITY.val('');
    FILTER_DIVISION.val('');
    FILTER_CATEGORY.val('');
    FILTER_UNIT_CODE.val('');
    FILTER_GEO_LOCATION.val('');
    FILTER_DOMAIN.val('');
    FILTER_ORGANIZATION.val('');
    getCSVFileApprovalList(CSVID, _SHOW_FROM, _PAGE_LIMIT);
});

// pagination

function hidePageView() {
    $('#pagination_rpt').empty();
    $('#pagination_rpt').removeData('twbs-pagination');
    $('#pagination_rpt').unbind('page');
}

function createPageView(page_type) {
    perPage = parseInt(ITEMS_PER_PAGE.val());
    hidePageView();
    $('#pagination_rpt').twbsPagination({
        totalPages: Math.ceil(TOTAL_RECORD / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(_ON_CURRENT_PAGE) != cPage) {
                if(_SHOW_CLICKED == true && _FILTER_CLICKED == false) {
                    _ON_CURRENT_PAGE = cPage;
                    _PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
                    if (_ON_CURRENT_PAGE == 1) {
                        _SHOW_FROM = 0;
                    } else {
                        _SHOW_FROM = (_ON_CURRENT_PAGE - 1) * _PAGE_LIMIT;
                    }
                    getCSVFileApprovalList(CSVID, _SHOW_FROM, _PAGE_LIMIT);
                }
                else if(_SHOW_CLICKED == false && _FILTER_CLICKED == true){
                    BTN_FILTER_GO.click();
                }
            }
        }
    });
};

function hidePagePan() {
    $('.compliance-count').text('');
    $('.pagination-view').hide();
};

function showPagePan(_SHOW_FROM, showTo, total) {
    var showText = 'Showing ' + _SHOW_FROM + ' to ' + showTo +
        ' of ' + total + ' units ';
    $('.compliance-count').text(showText);
    $('.pagination-view').show();
};

ITEMS_PER_PAGE.on('change', function(e) {
    _PAGE_LIMIT = parseInt($(this).val());
    _ON_CURRENT_PAGE = 1;
    _SHOW_FROM = 0;
    createPageView(TOTAL_RECORD);
    displayViewScreen(CSVID, _SHOW_FROM, _PAGE_LIMIT);
});


// Approve all check box event in view screen
APPROVE_ALL_UNITS.on("change", function(e) {
    REJECT_ALL_UNITS.prop("checked", false);
    var UnitsList = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
        find('tr').length;
    var value = null;
    if (UnitsList > 0) {
        displayLoader();
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('.view-approve-check').
            prop('checked', false);
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('.view-reject-check').
            prop('checked', false);
        var i = 0;
        for(i = 0; i < UnitsList; i++) {
            value = VIEWCLIENTUNITLIST[i];
            if(e.target.checked && value != null) {
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
                    find('.view-approve-check').
                    prop('checked', true);
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                    'td.reject-reason.-'+value.bulk_unit_id
                ).html('');
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id, 1,
                    null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                });
            }
            else if(!e.target.checked && value != null) {
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
                    find('.view-approve-check').
                    prop('checked', false);
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                    'td.reject-reason.-'+value.bulk_unit_id
                ).html('');
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id, 0,
                    null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                });
            }
        }
        hideLoader();
    }
});

// Reject all event in view screen
REJECT_ALL_UNITS.on("change", function(e) {
    APPROVE_ALL_UNITS.prop("checked", false);
    var UnitsList = TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
        find('tr').length;
    var value = null;
    if (UnitsList > 0 && e.target.checked) {
        displayLoader();
        displayViewRejectAllPopUp(function(reason) {
            if(reason != '' && reason != null) {
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
                    find('.view-approve-check').
                    prop('checked', false);
                TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
                    find('.view-reject-check').
                    prop('checked', false);
                var i = 0;
                for(i = 0; i < UnitsList; i++) {
                    value = VIEWCLIENTUNITLIST[i];
                    if(e.target.checked && value != null) {
                        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
                            find('.view-reject-check').
                            prop('checked', true);
                        csvid = $('#view_csv_unit_id').val();
                        bu.updateClientUnitActionFromView(
                            parseInt(csvid), value.bulk_unit_id,
                            2, $('.view-reason').val(),
                            function(err, res)
                            {
                                if (err != null) {
                                    displayMessage(err);
                                }
                                else {
                                    loadRemarksOnViewRejectAll(
                                        $('.view-reason').val()
                                    );
                                }
                            }
                        );
                    }
                }
            }
            hideLoader();
        });
    } else if(!e.target.checked && UnitsList > 0) {
        displayLoader();
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('.view-approve-check').
            prop('checked', false);
        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.
            find('.view-reject-check').
            prop('checked', false);
        var i = 0;
        for(i = 0; i < UnitsList; i++) {
            value = VIEWCLIENTUNITLIST[i];
            if (value != null) {
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id,
                    0, null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                    else {
                        TBL_CLIENTUNIT_BULK_UPLOADED_APPROVAL_LIST.find(
                            'td.reject-reason.-'+value.bulk_unit_id
                        ).html('');
                    }
                });
            }
        }
        hideLoader();
    }
});

$('#uploaded_file_name').keyup(function() {
    mList = keySearchUnitsFilesList(CLIENTUNITCSVFILESLIST);
    loadClientUnitCSVFilesList(mList);
});
$('#uploaded_on').keyup(function() {
    mList = keySearchUnitsFilesList(CLIENTUNITCSVFILESLIST);
    loadClientUnitCSVFilesList(mList);
});
$('#uploaded_by').keyup(function() {
    mList = keySearchUnitsFilesList(CLIENTUNITCSVFILESLIST);
    loadClientUnitCSVFilesList(mList);
});
$('#total_units').keyup(function() {
    mList = keySearchUnitsFilesList(CLIENTUNITCSVFILESLIST);
    loadClientUnitCSVFilesList(mList);
});
$('#filter_legal_entity').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_division').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_category').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_geo_level').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_location').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_unit_code').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_unit_name').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_address').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_city').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_state').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_post_code').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_domain').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});
$('#filter_orgn').keyup(function() {
    fList = keySearchUnitsDetailsList(VIEWCLIENTUNITLIST);
    bindClientUnitList(fList);
});

// Document initialization process
$(document).ready(function() {
    initialize('list');
    $(".nicescroll").niceScroll();
});

$('#exampleInputReason').on('input', function (e) {
      IsCommonInputBulkUpload(this);
});

$('#exampleInputReason1').on('input', function (e) {
      IsCommonInputBulkUpload(this);
});