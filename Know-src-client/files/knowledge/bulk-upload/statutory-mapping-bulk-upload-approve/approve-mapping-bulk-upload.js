// control initialize
var ListContainer = $('.tbody-sm-approve-list1');
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');
var ListScreen = $("#sm-approve-list");
var ViewScreen = $("#sm-approve-view");
var ShowButton = $("#btn-list-show");
var PasswordSubmitButton = $('.password-submit');

var ViewListContainer = $('.tbody-sm-approve-view');
var ViewListRowTemplate = $('#templates .table-sm-approve-info .table-row');

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
var AcUser = $('#ac-user')

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

function displayPopUp(TYPE, csv_id){
    if (TYPE == "reject") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current-password-reject');
    }
    else {
        targetid = "#custom-modal-approve"
        CurrentPassword = $('#current-password');
    }
    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            CurrentPassword.focus();
            CurrentPassword.val('');
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
                        bu_approve_page.actionFromList(csv_id, 2, null, CurrentPassword.val());
                    }
                    else if (TYPE == "submit") {

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
    }else if(isLengthMinMax($('#current-password'), 1, 20, message.password_should_not_exceed_20) == false){
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
}
ApproveBulkMapping.prototype.possibleFailures = function(error) {
    displayMessage(error);
};
ApproveBulkMapping.prototype.showList = function() {
    ListScreen.show();
    ViewScreen.hide();
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
            uploaded_name = null
            for (var i=0; i<t_this._UserList.length; i++) {
                if (data.uploaded_by == t_this._UserList[i].user_id) {
                    uploaded_name = t_this._UserList[i].emp_code_name
                    break;
                }
            }

            var cloneRow = ListRowTemplate.clone();
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(data.csv_name);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(uploaded_name);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(
                data.approve_count + '/' + data.rej_count
            );
            $('.approve-checkbox', cloneRow).on('change', function(e){
                if (e.target.checked){
                    displayPopUp('approve', data.csv_id);
                }
            });
            $('.reject-checkbox', cloneRow).on('change', function(e){
                if(e.target.checked){
                    displayPopUp('reject', data.csv_id);
                }
            });
            $('.bu-view-mapping', cloneRow).on('click', function(){
                t_this.showViewScreen(data.csv_id, 0, 25);
            });
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
    bu.confirmUpdateAction(csv_id, country_val.val(), domain_val.val(), function(error, response) {
        if (error == null) {
            t_this.showList();

        }
    });
};
ApproveBulkMapping.prototype.actionFromList = function(
    csv_id, action, remarks, pwd
) {
    t_this = this;
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
                        t_this.fetchListData();
                    }
                });
            }else {
                t_this.showList();
            }
        }
        else {
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
ApproveBulkMapping.prototype.showViewScreen = function(csv_id, f_count, r_range) {
    ListScreen.hide();
    ViewScreen.show();
    bu_approve_page.fetchViewData(csv_id, f_count, r_range);
};
ApproveBulkMapping.prototype.fetchViewData = function(csv_id, f_count, r_range) {
    t_this = this;
    displayLoader();
    bu.getApproveMappingView(csv_id, f_count, r_range, function(error, response){
        if(error == null) {
            t_this._ViewDataList = response.mapping_data;
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
            $('.view-csv-name').text(response.csv_name);
            t_this.renderViewScreen(t_this._ViewDataList);
            hideLoader();
        }
    });

};
ApproveBulkMapping.prototype.renderViewScreen = function(view_data) {
    t_this = this;
    var j = 1;
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
            if (data.action == 1) {
                $('.view-approve-check',cloneRow).checked = true;
                $('.view-reject-check',cloneRow).checked = false;
            }
            else {
                $('.view-approve-check',cloneRow).checked = false;
                $('.view-reject-check',cloneRow).checked = true;
            }

            $('.view-approve-check', cloneRow).on('change', function(e){
                if (e.target.checked){

                }
            });
            $('.view-reject-check', cloneRow).on('change', function(e){
                if(e.target.checked){

                }
            });

            ViewListContainer.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

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
        validateAuthentication();
    });
}

bu_approve_page = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    bu_approve_page.showList()
});
