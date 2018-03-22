// control initialize
var ListContainer = $('.tbody-sm-approve-list1');
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');
var ListScreen = $("#sm-approve-list");
var ViewScreen = $("#sm-approve-view");
var ShowButton = $("#btn-list-show");
var GoButton = $("#go");
var PasswordSubmitButton = $('.password-submit');
var CancelButton = $("#btn-sm-view-cancel");
var ViewListContainer = $('#tbody-sm-approve-view');
var ViewListRowTemplate = $('#templates .table-sm-approve-info .clone-row');
var FinalSubmit = $('#btn-final-submit')
// auto complete - country
var country_val = $('#countryid');
var country_ac = $("#countryname");
var AcCountry = $('#ac-country');

// auto complete - domain
var domain_val = $('#domainid');
var domain_ac = $("#domainname");
var AcDomain = $('#ac-domain')

// auto complete - user
var user_val = $('#userid');
var user_ac = $("#username");
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

var ac_orgName = $('#orgname');
var ACOrg = $('#ac-orgname');
var ac_nature = $('#nature');
var ACNature = $('#ac-nature');
var ac_statutory = $('#statutory');
var ACStatutory = $('#ac-statutory');
var ac_geoLocation = $('#geolocation');
var ACGeoLocation = $('#ac-geolocation');
var ac_compTask = $('#comptask');
var ACCompTask = $('#ac-comptask');
var ac_taskID = $('#taskid');
var ACTaskId = $('#ac-taskid');
var ac_compDoc = $('#compdoc');
var ACCompDoc = $('#ac-compdoc');
var ac_compDesc = $('#compdesc');
var ACCompDesc = $('#ac-compdesc');
var ac_taskType = $('#tasktype');
var ACTaskType = $('#ac-tasktype');
var MultiSelect_Frequency = $('#frequency');


var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var _on_current_page = 1;
var STATU_TOTALS;
var j = 1;



var CurrentPassword = null;

var Msg_pan = $(".error-message");
var bu_approve_page = null;
var isAuthenticate;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var primary_key = id_element[0].id;
    if(primary_key == 'countryid'){
      domain_ac.val('');
      domain_val.val('');
      user_ac.val('');
      user_val.val('');
    }
}

function displayPopUp(TYPE, csv_id, smid){
    if (TYPE == "reject") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current-password-reject');
        $('.reject-reason-txt').val('')
    }
    else if (TYPE == "view-reject") {
        targetid = "#custom-modal-remarks";
        CurrentPassword = null;
        $('.view-reason').val('')
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
                        bu_approve_page.actionFromList(csv_id, 1, null, CurrentPassword.val());
                    }
                    else if (TYPE == "reject") {
                        bu_approve_page.actionFromList(csv_id, 2, $('.reject-reason-txt').val(), CurrentPassword.val());
                    }
                    else if (TYPE == "submit") {
                        bu_approve_page.finalSubmit(csv_id, CurrentPassword.val());
                    }
                    else if (TYPE == "view-reject") {
                        bu.updateActionFromView(csv_id, smid, 2, $('.view-reason').val(), function(err, res) {
                        if (err != null) {
                            t_this.possibleFailures(err);
                        }
                        hideLoader();
                    });
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
    }else if(isLengthMinMax(CurrentPassword, 1, 20, message.password_20_exists) == false){
        return false;
    } else {
        isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
}


function ApproveBulkMapping() {
    this._CountryList = [];
    this._DomainList = [];
    this._UserList = [];
    this._ApproveDataList = [];
    this._ViewDataList = [];

    this._OrgaNames = [];
    this._Natures = [];
    this._Statutories = [];
    this._Frequency = [];
    this._GeoLocation = [];
    this._CompTasks = [];
    this._CompDescs = [];
    this._CompDocs = [];
    this._TaskId = [];
    this._TaskType = [];
    this._CSV_ID = null;
    this.show_map_count = 0;
    this._Country_id = null;
    this._domain_id = null;
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
    t_this = this;
    displayLoader();
    cid = parseInt(country_val.val());
    did = parseInt(domain_val.val());
    uid = parseInt(user_val.val());
    bu.getApproveMappingCSVList(cid, did, uid, function(error, response) {
        if (error == null) {
            t_this._ApproveDataList = response.pending_csv_list;
            $.each(t_this._ApproveDataList, function(idx, data) {
                uploaded_name = null
                for (var i=0; i<t_this._UserList.length; i++) {
                    if (data.uploaded_by == t_this._UserList[i].user_id) {
                        uploaded_name = t_this._UserList[i].emp_code_name
                        break;
                    }
                }
                if (uploaded_name != null) {
                    data.uploaded_by = uploaded_name;
                }

            });
            t_this.renderList(t_this._ApproveDataList);
            hideLoader();
        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.renderList = function(list_data) {
    t_this = this;
    var j = 1;
    ListContainer.find('tr').remove();
    if(list_data.length == 0) {
        ListContainer.empty();
        var tr = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    }
    else {
        $.each(list_data, function(idx, data) {


            var cloneRow = ListRowTemplate.clone();
            cname_split = data.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cname);;
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(data.uploaded_by);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(
                data.approve_count + '/' + data.rej_count
            );
            $('.approve-checkbox', cloneRow).on('change', function(e){
                if (e.target.checked){
                    displayPopUp('approve', data.csv_id, null);
                }
            });
            $('.reject-checkbox', cloneRow).on('change', function(e){
                if(e.target.checked){
                    displayPopUp('reject', data.csv_id, null);
                }
            });
            $('.bu-view-mapping', cloneRow).on('click', function(){
                t_this._CSV_ID = data.csv_id;
                t_this._Country_id = data.c_id;
                t_this._domain_id = data.d_id;
                t_this.showViewScreen(data.csv_id, 0, 25);
            });
            flname = data.csv_name.split('.')
            flname = flname[0]
            $('.dl-xls-file',cloneRow).attr("href", "/uploaded_file/xlsx/"+flname+'.xlsx');
            $('.dl-csv-file',cloneRow).attr("href", "/uploaded_file/csv/"+flname+'.csv');
            $('.dl-ods-file',cloneRow).attr("href", "/uploaded_file/ods/"+flname+ '.ods');
            $('.dl-txt-file',cloneRow).attr("href", "/uploaded_file/txt/"+flname+'.txt');
            ListContainer.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};
ApproveBulkMapping.prototype.fetchDropDownData = function() {
    t_this = this;
    displayLoader();
    mirror.getDomainList(function (error, response) {
        if (error == null) {
            t_this._DomainList = response.domains;
            t_this._CountryList = response.countries
            mirror.getKnowledgeUserInfo(function (err, resp){
                if (err == null){
                    t_this._UserList = resp.k_executive_info;
                    hideLoader();
                }
                else {
                    hideLoader();
                    t_this.possibleFailures(err);
                }
            });

        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.confirmAction = function() {
    t_this = this;
    displayLoader();
    console.log("confirm action called")
    bu.confirmUpdateAction(t_this._CSV_ID, t_this._Country_id, t_this._domain_id, function(error, response) {
        if (error == null) {
            t_this.showList();
            t_this.fetchListData();
            displaySuccessMessage(message.confirm_success);
        }
        else {
            bu_approve_page.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.actionFromList = function(
    csv_id, action, remarks, pwd
) {
    t_this = this;
    c_id = parseInt(country_val.val());
    d_id = parseInt(domain_val.val());
    t_this._CSV_ID = csv_id;
    t_this._Country_id = c_id;
    t_this._domain_id = d_id;
    displayLoader();
    bu.updateActionFromList(
        csv_id, action, remarks, pwd, country_val.val(), domain_val.val(),
        function(error, response){
            if (error == null) {
                if (response.rej_count > 0) {
                    msg = response.rej_count + " compliance declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            t_this.confirmAction();
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

                    t_this.fetchListData()
                }


            }
            else {
                hideLoader();
                t_this.possibleFailures(error);
            }
        }
    );
};
ApproveBulkMapping.prototype.showViewScreen = function(csv_id, f_count, r_range) {
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
    j = 1;
    bu_approve_page.show_map_count = 0;
    bu_approve_page.fetchViewData(csv_id, f_count, r_range);


// alert();

// setTimeout(function(){  $.getScript("/knowledge/js/multifreezer.js");

// $.getScript("/knowledge/css/multifreezer.css");
 // hideLoader();}, 3000);

     if($("body").hasClass("freezer-active-bu")==false) {
displayLoader();
        setTimeout(function(){  $.getScript("/knowledge/js/multifreezer.js");  hideLoader();}, 3000);
    }

// $.getScript("/knowledge/js/multifreezer.js");
};
ApproveBulkMapping.prototype.fetchViewData = function(csv_id, f_count, r_range) {
    t_this = this;

    displayLoader();
    bu.getApproveMappingView(csv_id, f_count, r_range, function(error, response){
        if(error == null) {
            t_this._ViewDataList = response.mapping_data;
            if (t_this._ViewDataList.length > 0) {

                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploaded_name = null
                for (var i=0; i<t_this._UserList.length; i++) {
                    if (response.uploaded_by == t_this._UserList[i].user_id) {
                        uploaded_name = t_this._UserList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploaded_name);
                $('.view-uploaded-on').text(response.uploaded_on);
                cname_split = response.csv_name.split("_");
                cname_split.pop();
                cname = cname_split.join("_");
                $('.view-csv-name').text(cname);
                $('#view-csv-id').val(response.csv_id);
                STATU_TOTALS  = response.total;
                if(t_this._ViewDataList.length == 0) {
                    _t_this.hidePagePan();
                    PaginationView.hide();
                    t_this.hidePageView();
                }
                else {
                    t_this.createPageView();
                    PaginationView.show();
                }
            }
            t_this.renderViewScreen(t_this._ViewDataList);

            // var onetimejs = $("#tbody-sm-approve-view").html();
            // alert(onetimejs);


            hideLoader();
        }
    });

};
ApproveBulkMapping.prototype.renderViewScreen = function(view_data) {
    t_this = this;

    showFrom = t_this.show_map_count;
    showFrom += 1;

    ViewListContainer.find('tr').remove();
    if(view_data.length == 0) {
        ViewListContainer.empty();
        var tr = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tr.clone();
        $('.no_records', clone4).text('No Records Found');
        ViewListContainer.append(clone4);
    }
    else {
        $.each(view_data, function(idx, data) {


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
            $('.format', cloneRow).text(data.format_file);
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
            else {
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", true);
            }

            $('.view-approve-check', cloneRow).on('change', function(e){
                if (e.target.checked){
                    csvid = $('#view-csv-id').val();
                    bu.updateActionFromView(parseInt(csvid), data.sm_id, 1, null, function(err, res) {
                        if (err != null) {
                            t_this.possibleFailures(err);
                        }
                        else {
                            $('.view-reject-check',cloneRow).attr("checked", false);
                        }
                    });
                }
            });
            $('.view-reject-check', cloneRow).on('change', function(e){
                if(e.target.checked){
                    csvid = $('#view-csv-id').val();
                    displayPopUp('view-reject', parseInt(csvid), data.sm_id);
                    $('.view-approve-check',cloneRow).attr("checked", false);
                }
            });

            ViewListContainer.append(cloneRow);
            j += 1;
        });
    }

    t_this.show_map_count += view_data.length;
    $('[data-toggle="tooltip"]').tooltip();
    t_this.showPagePan(showFrom, t_this.show_map_count, STATU_TOTALS);
};

ApproveBulkMapping.prototype.fetchFilterDropDown = function(csvid) {
    t_this = this;
    displayLoader();
    bu.getApproveMappingViewFilter(parseInt(csvid), function(err, resp) {
        if (err == null) {
            t_this._OrgaNames = resp.orga_names;
            t_this._Natures = resp.s_natures;
            t_this._Statutories = resp.bu_statutories;
            t_this._Frequency = resp.frequencies;
            t_this._GeoLocation = resp.geo_locations;
            t_this._CompTasks = resp.c_tasks;
            t_this._CompDescs = resp.c_descs;
            t_this._CompDocs = resp.c_docs;
            t_this._TaskId = resp.task_ids;
            t_this._TaskType = resp.task_types
            if (t_this._Frequency.length > 0) {
                str = ''
                for (var i in t_this._Frequency){
                    val = t_this._Frequency[i]
                    str += '<option value="'+ val +'">'+ val +'</option>';
                }
                MultiSelect_Frequency.html(str).multiselect('rebuild');
            }
            hideLoader();
        }
    });
};

ApproveBulkMapping.prototype.renderViewFromFilter = function() {
    _page_limit = parseInt(ItemsPerPage.val());
    var showCount = 0;
    if (_on_current_page == 1) {
        showCount = 0;
        t_this.show_map_count = 0;
    } else {
        showCount = (_on_current_page - 1) * _page_limit;
        t_this.show_map_count = showCount;
    }
    f_types = [];
    $("#frequency option:selected").each(function () {
       var $this = $(this);
       if ($this.length) {
        f_types.push($this.text());
       }
    });
    args = {
        "csv_id": parseInt($('#view-csv-id').val()),
        "orga_name": ac_orgName.val(),
        "s_nature": ac_nature.val(),
        "f_types": f_types,
        "statutory": ac_statutory.val(),
        "geo_location": ac_geoLocation.val(),
        "c_task_name": ac_compTask.val(),
        "c_desc": ac_compDesc.val(),
        "c_doc": ac_compDoc.val(),
        "f_count": showCount,
        "r_range": _page_limit
    }
    bu.getApproveMappingViewFromFilter(args, function(err, response){
        displayLoader()
        if(err != null) {
            hideLoader();
            bu_approve_page.possibleFailures(err)
        }
        if(err == null) {
            t_this._ViewDataList = response.mapping_data;
            if (t_this._ViewDataList.length > 0) {
                $('.view-country-name').text(response.c_name);
                $('.view-domain-name').text(response.d_name)
                uploaded_name = null
                for (var i=0; i<t_this._UserList.length; i++) {
                    if (response.uploaded_by == t_this._UserList[i].user_id) {
                        uploaded_name = t_this._UserList[i].emp_code_name
                        break;
                    }
                }
                $('.view-uploaded-by').text(uploaded_name);
                $('.view-uploaded-on').text(response.uploaded_on);
                cname_split = response.csv_name.split("_");
                cname_split.pop();
                cname = cname_split.join("_");
                $('.view-csv-name').text(cname);
                $('#view-csv-id').val(response.csv_id);
                STATU_TOTALS  = response.total;
                if(t_this._ViewDataList.length == 0) {
                    _t_this.hidePagePan();
                    PaginationView.hide();
                    t_this.hidePageView();
                }
                else {
                    t_this.createPageView();
                    PaginationView.show();
                }
            }
            t_this.renderViewScreen(t_this._ViewDataList);
            hideLoader();
        }
    });
};


ApproveBulkMapping.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

ApproveBulkMapping.prototype.createPageView = function(page_type) {
    t_this = this;
    perPage = parseInt(ItemsPerPage.val());
    t_this.hidePageView();
    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(STATU_TOTALS / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cpage = parseInt(page);
            if (parseInt(_on_current_page) != cpage) {
                _on_current_page = cpage;
                _page_limit = parseInt(ItemsPerPage.val());
                var showCount = 0;
                if (_on_current_page == 1) {
                    showCount = 0;
                    t_this.show_map_count = 0;
                } else {
                    showCount = (_on_current_page - 1) * _page_limit;
                    t_this.show_map_count = showCount;
                }
                if(page_type == "show") {
                    t_this.fetchViewData(t_this._CSV_ID, showCount, _page_limit);
                }
                else {
                    t_this.renderViewFromFilter();

                }
            }
        }
    });
};

ApproveBulkMapping.prototype.hidePagePan = function() {
    $('compliance_count').text('');
    $('.pagination-view').hide();
};

ApproveBulkMapping.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' compliances ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};

ApproveBulkMapping.prototype.finalSubmit = function(csvid, pwd) {
    t_this = this;
    displayLoader();
    c_id = parseInt(country_val.val());
    d_id = parseInt(domain_val.val());
    t_this._CSV_ID = csvid;
    t_this._Country_id = c_id;
    t_this._domain_id = d_id;
    bu.submitMappingAction(csvid, c_id, d_id, pwd, function(err, res){
        if(err == null) {
            if (res.rej_count > 0) {
                msg = res.rej_count + " compliance declined, Do you want to continue ?";
                confirm_alert(msg, function(isConfirm) {
                    if (isConfirm) {
                        t_this.confirmAction();
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
                t_this.fetchListData()
            }

        }
        else {
            t_this.possibleFailures(err);
        }
    });

};

function key_search(mainList) {
    csv_key = searchFileName.val().toLowerCase();
    upload_by_key = searchUploadBy.val().toLowerCase();
    total = searchTotRecords.val();
    upload_on_key = searchUploadOn.val().toLowerCase();
    console.log(upload_on_key)

    var fList = [];
    for (var entity in mainList) {
        csvName = mainList[entity].csv_name;
        uploadby = mainList[entity].uploaded_by;
        total_records = mainList[entity].no_of_records;
        uploadon = mainList[entity].uploaded_on;
        console.log(uploadon)

        if (
            (~csvName.toLowerCase().indexOf(csv_key)) &&
            (~uploadon.toLowerCase().indexOf(upload_on_key)) &&
            (~uploadby.toLowerCase().indexOf(upload_by_key)) &&
            (~total_records.toString().indexOf(total))
        ){
            fList.push(mainList[entity]);
        }
    }
    return fList
}
function key_view_search(mainList) {
    console.log("key view search");
    key_statutory = searchStatutory.val().toLowerCase();
    key_organization = searchOrganization.val().toLowerCase();
    key_nature = searchNature.val().toLowerCase();
    key_provision = searchProvision.val().toLowerCase();
    key_c_task = searchCTask.val().toLowerCase();
    key_c_doc = searchCDoc.val().toLowerCase();
    key_taskid = searchTaskId.val().toLowerCase();
    key_c_desc = searchCDesc.val().toLowerCase();
    key_p_cons = searchPCons.val().toLowerCase();
    key_tasktype = searchTaskType.val().toLowerCase();
    key_refer = searchReferLink.val().toLowerCase();
    key_freq = searchFreq.val().toLowerCase();
    key_format = searchFormat.val().toLowerCase();
    key_geo = searchGeography.val().toLowerCase();

    var fList = [];
    for (var entity in mainList) {
        d = mainList[entity];

        if (
            (~d.statutory.toLowerCase().indexOf(key_statutory)) &&
            (~d.orga_name.toLowerCase().indexOf(key_organization)) &&
            (~d.s_nature.toLowerCase().indexOf(key_nature)) &&
            (~d.s_provision.toLowerCase().indexOf(key_provision)) &&
            (~d.c_task_name.toLowerCase().indexOf(key_c_task)) &&
            (~d.c_doc.toLowerCase().indexOf(key_c_doc)) &&
            (~d.task_id.toLowerCase().indexOf(key_taskid)) &&
            (~d.c_desc.toLowerCase().indexOf(key_c_desc)) &&
            (~d.p_cons.toLowerCase().indexOf(key_p_cons)) &&
            (~d.task_type.toLowerCase().indexOf(key_tasktype)) &&
            (~d.refer.toLowerCase().indexOf(key_refer)) &&
            (~d.frequency.toLowerCase().indexOf(key_freq)) &&
            (~d.format_file.toLowerCase().indexOf(key_format)) &&
            (~d.geo_location.toLowerCase().indexOf(key_geo))

        ){
            fList.push(d);
        }
    }
    return fList
}

function PageControls() {
    country_ac.keyup(function(e){
        var condition_fields = ["is_active"];
        var condition_values = [true];
        var text_val = $(this).val();
        commonAutoComplete(
            e, AcCountry, country_val, text_val,
            bu_approve_page._CountryList, "country_name", "country_id", function (val) {
                onAutoCompleteSuccess(country_ac, country_val, val);
            }, condition_fields, condition_values
        );

    });

    domain_ac.keyup(function(e){
        var domainList = bu_approve_page._DomainList;
        var text_val = $(this).val();
        var domain_list = [];
        var c_ids = null;
        var check_val = false;
        if(country_val.val() != ''){
          for(var i=0;i<domainList.length;i++){
            c_ids = domainList[i].country_ids;

            for(var j=0;j<c_ids.length;j++){
              if(c_ids[j] == country_val.val())
              {
                check_val = true;
              }
            }

            if(check_val == true && domainList[i].is_active == true){
              domain_list.push({
                "domain_id": domainList[i].domain_id,
                "domain_name": domainList[i].domain_name
              });
              check_val = false;
              //break;
            }
          }
          commonAutoComplete(
            e, AcDomain, domain_val, text_val,
            domain_list, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(domain_ac, domain_val, val);
         });
        }
        else{
          displayMessage(message.country_required);
        }
    });

    user_ac.keyup(function(e){
        var userList = bu_approve_page._UserList;
        var text_val = $(this).val();
        var user_list = [];
        if (country_val.val() != '' && domain_val.val() != '') {
            for (var i=0; i<userList.length; i++) {
                if(
                    (jQuery.inArray(parseInt(country_val.val()), userList[i].c_ids) !== -1) &&
                    (jQuery.inArray(parseInt(domain_val.val()), userList[i].d_ids) !== -1)
                ) {
                    console.log(userList[i])
                    user_list.push({
                        "emp_id": userList[i].user_id,
                        "emp_name": userList[i].emp_code_name
                    });
                }

            }
            commonAutoComplete(
                e, AcUser, user_val, text_val,
                user_list, "emp_name", "emp_id", function (val) {
                    onAutoCompleteSuccess(user_ac, user_val, val);
            });
        }
        else {
            if (country_val.val() == '') {
                displayMessage(message.country_required);
            }
            else if (domain_val.val() == '') {
                displayMessage(message.domain_required);
            }
        }
    });

    ShowButton.click(function(){
        if (country_val.val() == '') {
            displayMessage(message.country_required);
        }
        else if (domain_val.val() == '') {
            displayMessage(message.domain_required);
        }
        if (country_val.val() != '' && domain_val.val() != '') {
            bu_approve_page.fetchListData()
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
        bu_approve_page.showList();
    });


    searchFileName.keyup(function() {
        fList = key_search(bu_approve_page._ApproveDataList);
        bu_approve_page.renderList(fList);
    });

    searchTotRecords.keyup(function() {
        fList = key_search(bu_approve_page._ApproveDataList);
        bu_approve_page.renderList(fList);
    });

    searchUploadBy.keyup(function() {
        fList = key_search(bu_approve_page._ApproveDataList);
        bu_approve_page.renderList(fList);
    });
    searchUploadOn.keyup(function() {
        fList = key_search(bu_approve_page._ApproveDataList);
        bu_approve_page.renderList(fList);
    });

    searchStatutory.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchOrganization.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchNature.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchProvision.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchCTask.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchCDoc.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchTaskId.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchCDesc.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchPCons.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchTaskType.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchReferLink.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchFreq.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchFormat.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });
    searchGeography.keyup(function(){
        fList = key_view_search(bu_approve_page._ViewDataList);
        bu_approve_page.renderViewScreen(fList);
    });

    // filter events

    $('.right-bar-toggle').on('click', function(e) {
      $('#wrapper').toggleClass('right-bar-enabled');
      bu_approve_page.fetchFilterDropDown($('#view-csv-id').val());
    });

    ac_orgName.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACOrg, text_val,
            bu_approve_page._OrgaNames, function (val) {
                ac_orgName.val(val[0])
            }
        );

    });

    ac_nature.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACNature, text_val,
            bu_approve_page._Natures, function (val) {
                ac_nature.val(val[0])
            }
        );

    });

    ac_statutory.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACStatutory, text_val,
            bu_approve_page._Statutories, function (val) {
                ac_statutory.val(val[0])
            }
        );

    });

    ac_geoLocation.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACGeoLocation, text_val,
            bu_approve_page._GeoLocation, function (val) {
                ac_geoLocation.val(val[0])
            }
        );

    });

    ac_compTask.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACCompTask, text_val,
            bu_approve_page._CompTasks, function (val) {
                ac_compTask.val(val[0])
            }
        );
    });

    ac_taskID.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACTaskId, text_val,
            bu_approve_page._TaskId, function (val) {
                ac_taskID.val(val[0])
            }
        );
    });

    ac_compDoc.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACCompDoc, text_val,
            bu_approve_page._CompDocs, function (val) {
                ac_compDoc.val(val[0])
            }
        );
    });

    ac_compDesc.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACCompDesc, text_val,
            bu_approve_page._CompDescs, function (val) {
                ac_compDesc.val(val[0])
            }
        );
    });


    ac_taskType.keyup(function(e){
        var text_val = $(this).val();
        commonArrayAutoComplete(
            e, ACTaskType, text_val,
            bu_approve_page._TaskType, function (val) {
                ac_taskType.val(val[0])
            }
        );
    });

    GoButton.click(function(){
        var filtered = '';
        append_filter = function(val) {
            if (filtered == '') {
                filtered += val;
            }
            else {
                filtered += "|" + val;
            }
        }
        if(ac_orgName.val() != "") {
            orgs = "Organization : " + ac_orgName.val();
            append_filter(orgs);
        }
        if(ac_nature.val() != "") {
            natures = "Statutory Nature : " + ac_nature.val();
            append_filter(natures);
        }
        if (ac_statutory.val() != "") {
            statutories = "Statutory : " + ac_statutory.val();
            append_filter(statutories);
        }
        if(ac_geoLocation.val() != "") {
            geos = "Geography Location : " + ac_geoLocation.val();
            append_filter(geos);
        }
        if(ac_compTask.val() != "") {
            tasks = "Compliance Task : " + ac_compTask.val();
            append_filter(tasks);
        }
        if(ac_taskID.val() != "") {
            tid = "Task ID : " + ac_taskID.val();
            append_filter(tid);
        }
        if(ac_compDoc.val() != "") {
            doc = "Compliance Document : " + ac_compDoc.val();
            append_filter(doc);
        }
        if(ac_compDesc.val() != "") {
            desc = "Compliance Description : " + ac_compDesc.val();
            append_filter(desc);
        }
        if(ac_taskType.val() != "") {
            tt = "Task Type : " + ac_taskType.val();
            append_filter(tt);
        }
        f_types = [];
        $("#frequency option:selected").each(function () {
           var $this = $(this);
           if ($this.length) {
            f_types.push($this.text());
           }
        });
        if (f_types.length != 0) {
            tt = "Frequency : " + f_types.join(',');
            append_filter(tt);
        }

        $('.filtered-data').text(filtered);

        bu_approve_page.renderViewFromFilter();

    });

    FinalSubmit.click(function(){
        displayPopUp("submit", parseInt($('#view-csv-id').val()), null);
    });




}

bu_approve_page = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    bu_approve_page.showList()
});

$(".nicescroll").niceScroll();