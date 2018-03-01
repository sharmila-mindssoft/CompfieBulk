// control initialize
var ListContainer = $('.tbody-sm-approve-list1');
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');
var ListScreen = $("#sm-approve-list");
var ViewScreen = $("#sm-csv-view");
var ShowButton = $("#btn-list-show");
var PasswordSubmitButton = $('.password-submit');

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
    this._ApproveDataList = []
}
ApproveBulkMapping.prototype.possibleFailures = function(error) {
    displayMessage(error);
};
ApproveBulkMapping.prototype.showList = function() {
    ListScreen.show();
    ViewScreen.hide();
    this.fetchDropDownData();
    this.fetchListData();
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
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    }
    else {
        $.each(list_data, function(idx, data) {

            var cloneRow = ListRowTemplate.clone();
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(data.csv_name);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.uploaded-by', cloneRow).text(data.uploaded_by);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.approve-reject', cloneRow).text(data.approve_count + '/' + data.rej_count);
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
ApproveBulkMapping.prototype.actionFromList = function(csv_id, action, remarks, pwd) {
    t_this = this;
    displayLoader();
    bu.updateActionFromList(csv_id, action, remarks, pwd, function(error, response){
        if (error == null) {
            t_this.fetchListData();
        }
        else {
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
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

    ShowButton.click(function(){
        if (country_val.val() != '' && domain_val.val() != '') {
            bu_approve_page.showList()
        }
    });

    PasswordSubmitButton.click(function(){
        validateAuthentication();
    });
}

bu_approve_page = new ApproveBulkMapping();

$(document).ready(function() {
    PageControls();
    bu_approve_page.fetchDropDownData()
});
