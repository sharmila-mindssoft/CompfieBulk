var listPage = $(".list-page");
var dataListPage = $(".data-list-page");

var clientGroupName = $("#client-group");
var clientGroupId = $("#client-group-id");
var acClientGroup = $("#ac-client-group");

var legalEntityName = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

var showButton = $("#show-button");
var listView = $("#list-view");

var dataTableTbody = $("#data-table-tbody");
var dataFilterHeader = $("#data-filter-header");

var downloadBtn = $(".download");
var passwordApproveSubmit = $('#password-approve-submit');
var approvePassword = $('#approve-password');

var passwordRejectSubmit = $('#password-reject-submit');
var rejectPassword = $('#reject-password');
var rejectRemark = $('#remark');


var dataDetailsTableTbody = $("#data-details-table-tbody");
var checkAllApprove = $("#check-all-approve");
var checkAllReject = $("#check-all-reject");

var verifieddata = $("#verified-data");
var pendingData = $("#pending-data");
var allData = $("#all-data");
var domain = $("#domain");
var unit = $("#unit");
var act = $("#act");
var unit = $("#unit");
var statutoryStatus = $("#statutory-status");
var complianceStatus = $("#compliance-status");
var search = $("#search");

var secondaryLegislationName = $("#secondary-legislation");
var secondaryLegislationId = $("#secondary-legislation-id");
var acSecondaryLegislation = $("#ac-secondary-legislation");

var statutoryProvisionName = $("#statutory-provision");
var statutoryProvisionId = $("#statutory-provision-id");
var acStatutoryProvision = $("#ac-statutory-provision");

var complianceTaskName = $("#compliance-task");
var complianceTaskId = $("#compliance-task-id");
var acComplianceTask = $("#ac-compliance-task");

var complianceStatusName = $("#compliance-status");
var complianceStatusId = $("#compliance-status-id");
var acComplianceStatus = $("#ac-compliance-status");



function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

ApproveAssignStatutoryBulkUpload = function() {
    this._client_group = []; // JSON.parse('[{"client_group_name":"Group one","is_active":true,"client_id":1},{"client_group_name":"Group two","is_active":true,"client_id":2},{"client_group_name":"Group three","is_active":false,"client_id":3}]');
    this._entities = []; // JSON.parse('[{"client_id":1,"legal_entity_id":1,"legal_entity_name":"LEGAL ENTITY 1"},{"client_id":1,"legal_entity_id":1,"legal_entity_name":"LEGAL ENTITY 2"},{"client_id":3,"legal_entity_id":1,"legal_entity_name":"LEGAL ENTITY 3"}]');
    this._data_list = []; // JSON.parse('[{"uploaded_file_name":"GroupRG-LE-General Act1947","uploaded_on":"04-Dec-2017 10:15","uploaded_by":"EM001 - Ram Kumar","no_of_records":1500,"approved_records":null,"rejected_records":null,"id":1},{"uploaded_file_name":"Ind-LL-Administrator Act1947 ","uploaded_on":"04-Dec-2017 11:45","uploaded_by":"EM002 - Muthu Kumar","no_of_records":1750,"approved_records":500,"rejected_records":50,"id":2},{"uploaded_file_name":"Ind-FL-General Act1947 ","uploaded_on":"03-Dec-2017 12:15","uploaded_by":"EM002 - Muthu Kumar","no_of_records":1200,"approved_records":null,"rejected_records":30,"id":3}]');
    this._data_list_details = [];
    /*this._domains = [];
    this._units = [];
    this._acts = [];
    this._frequencies = [];
    this._user_type = [];
    this._users = [];
    this._compliance_task_status = [];
    this._service_providers = [];
    this._report_data = [];
    on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._UserCompliances = [];*/
}

ApproveAssignStatutoryBulkUpload.prototype.pageLoad = function() {
    t_this = this;
    listPage.show();
    dataListPage.hide();

    listView.hide();
    clientGroupName.val('');
    clientGroupId.val('');
    legalEntityName.val('');
    legalEntityId.val('');

    t_this.initialize();
};

ApproveAssignStatutoryBulkUpload.prototype.initialize = function() {
    t_this = this;
    displayLoader();
    bu.getClientInfo(function(error, response) {
        if (error == null) {
            t_this._client_group = response.bu_clients;
            t_this._entities = response.bu_legalentites;
            hideLoader();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

ApproveAssignStatutoryBulkUpload.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage(message.domainname_exists);
    } else if (error == "ExportToCSVEmpty") {
        displayMessage(message.empty_export);
    } else {
        displayMessage(error);
    }
};

/*REPORT.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getREPORTFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.units;
            t_this._acts = response.acts;
            // t_this._compliance_task = response.compliances;
            t_this._users = response.legal_entity_users;
            t_this._frequencies = response.compliance_frequency;
            t_this.renderComplianceFrequencyList(t_this._frequencies);

        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};*/

function PageControls() {

    clientGroupName.keyup(function(e) {
        var text_val = clientGroupName.val().trim();
        var clientGroupList = REPORT._client_group;
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acClientGroup, clientGroupId, text_val, clientGroupList, "cl_name", "cl_id", function(val) {
            onClientGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntityName.keyup(function(e) {
        var text_val = legalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        var condition_fields = ["cl_id"];
        var condition_values = [clientGroupId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (validate()) {
            listView.show();
            showAnimation(listView);
            REPORT.fetchStatutoryValues();
        }
    });

    downloadBtn.click(function() {
        alert('ji');
        this.find('.dropdown-content').show();
    });

    passwordApproveSubmit.click(function() {
        validateAuthentication(approvePassword, null);
    });

    passwordRejectSubmit.click(function() {
        validateAuthentication(rejectPassword, rejectRemark);
    });

    checkAllApprove.click(function() {
      if($(this).prop("checked") == true) {
        $('.single-approve').removeAttr("checked");
        $('.single-approve').trigger('click');
        $('.single-reject').attr("disabled","disabled");
        checkAllReject.attr("disabled","disabled");
      } else {
        $('.single-approve').removeAttr("checked");
        $('.single-reject').removeAttr("disabled");
        checkAllReject.removeAttr("disabled");
      }
    });

    checkAllReject.click(function() {
      if($(this).prop("checked") == true) {
        $('.single-reject').removeAttr("checked");
        $('.single-reject').trigger('click');
        $('.single-approve').attr("disabled","disabled");
        checkAllApprove.attr("disabled","disabled");
      } else {
        $('.single-reject').removeAttr("checked");
        $('.single-approve').removeAttr("disabled");
        checkAllApprove.removeAttr("disabled");
      }
    });

    $('.right-bar-toggle').on('click', function(e) {
        $('#wrapper').toggleClass('right-bar-enabled');
    });
}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onClientGroupAutoCompleteSuccess = function(REPORT, val) {
    clientGroupName.val(val[1]);
    clientGroupId.val(val[0]);
    clientGroupName.focus();
    clearElement([legalEntityName, legalEntityId]);
    // REPORT.fetchLegalEntityList(val[0]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntityName.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntityName.focus();
}

validate = function() {
    is_valid = true;
    if (clientGroupName.val().trim().length == 0) {
        displayMessage(message.group_required);
        is_valid = false;
    } else if (clientGroupName.val().trim().length > 50) {
        displayMessage(message.group_50);
        is_valid = false;
    } else if (legalEntityName.val().trim().length == 0) {
        displayMessage(message.legalentity_required);
        is_valid = false;
    } else if (legalEntityName.val().trim().length > 50) {
        displayMessage(message.le_50);
        is_valid = false;
    }
    return is_valid;
};

showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
}

download = function(element) {
    if ($("." + element).is(':visible') == false) {
        $(".dropdown-content").hide();
        $("." + element).toggle();
    } else {
        $("." + element).toggle();
    }
}

viewListPage = function() {
    REPORT.pageLoad();
}

ApproveAssignStatutoryBulkUpload.prototype.fetchStatutoryValues = function() {
    t_this = this;
    c_id = clientGroupId.val();
    le_id = legalEntityId.val();
    displayLoader();
    bu.getAssignStatutoryForApprove(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response);
        if (error == null) {
            t_this._data_list = response.pending_csv_list_as;
            t_this.displayListPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ApproveAssignStatutoryBulkUpload.prototype.displayListPage = function() {
    t_this = this;
    if (t_this._data_list.length > 0) {
        dataTableTbody.empty();
        var sno = 0;
        $.each(t_this._data_list, function(k, v) {
            sno++;
            var clone = $('#template #report-table tr').clone();
            $('.sno', clone).text(sno);
            $('.uploaded-file-name', clone).html(v.csv_name);
            $('.uploaded-on', clone).html(v.uploaded_on);
            $('.uploaded-by', clone).html(v.uploaded_by);
            $('.no-of-records', clone).html(v.no_of_records);
            if (v.approved_count != 0 || v.rej_count != 0) {
                if (v.approved_count == 0) { v.approved_count = 0; }
                if (v.rej_count == 0) { v.rej_count = 0; }
                $('.approve-reject', clone).html(v.approved_count + '/' + v.rej_count);
                $('.view', clone).html('<a><i class="fa fa-pencil text-primary c-pointer"></i></a>')
                    .attr("onClick", "viewListDetailsPage(" + v.csv_id + ")");
            } else {
                $('.view', clone).html('<button class="btn btn-primary text-center waves-effect waves-light" type="button"> View </button>')
                    .attr("onClick", "viewListDetailsPage(" + v.csv_id + ")");
            }
            $('.download', clone).attr("onClick", "download('show-download" + sno + "')");
            $('.dropdown-content', clone).addClass("show-download" + sno);
            $('.approve a', clone).attr("onClick", "confirm_all_approve(" + sno + ")");
            $('.reject a', clone).attr("onClick", "confirm_all_reject(" + sno + ")");
            dataTableTbody.append(clone);
        });
    } else {
        $('.pagination-view').show();
        showAnimation(reportView);
        REPORT.showReportValues(ReportData);
    }
};

function confirm_all_approve(id) {
    Custombox.open({
        target: '#custom-modal-approve',
        effect: 'contentscale',
        complete: function() {
            approvePassword.focus();
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                allStatutoryApprove(id);
            }
        }
    });
}

allStatutoryApprove = function(id) {
    alert(id)
    /*displayLoader();
    bu.getAssignStatutoryForApprove(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response);
        if (error == null) {
            t_this._data_list = response.pending_csv_list_as;
            t_this.displayListPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });*/
};

function confirm_all_reject(id) {
    Custombox.open({
        target: '#custom-modal-reject',
        effect: 'contentscale',
        complete: function() {
            rejectPassword.focus();
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                allStatutoryReject(id, rejectReason);
            }
        }
    });
}

allStatutoryReject = function(id, rejectReason) {
    alert(id + ' - ' + rejectReason);
    /*displayLoader();
    bu.getAssignStatutoryForApprove(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response);
        if (error == null) {
            t_this._data_list = response.pending_csv_list_as;
            t_this.displayListPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });*/
};

function validateAuthentication(passwordField, remarkField) {
    var password = passwordField.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        passwordField.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    if (remarkField != null) {
        var remark = remarkField.val().trim();
        if (remark.length == 0) {
            displayMessage(message.remarks_required);
            remarkField.focus();
            return false;
        } else if (validateMaxLength('remark', remark, "Remark") == false) {
            return false;
        }
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            hideLoader();
            isAuthenticate = true;
            Custombox.close();
            displaySuccessMessage(message.password_authentication_success);
        } else {
            hideLoader();
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}


viewListDetailsPage = function(id) {
    listPage.hide();
    dataListPage.show();
    REPORT.loadDetailsPage(id);
    REPORT.loadFilterPage(id);
}

ApproveAssignStatutoryBulkUpload.prototype.loadDetailsPage = function(id) {
    t_this = this;
    var f_count = 0;
    var r_range = 10;
    displayLoader();
    bu.getViewAssignStatutoryData(parseInt(id), parseInt(f_count), parseInt(r_range), function(error, response) {
        console.log(error, response);
        if (error == null) {
            $('#client-group-name').text(response.cl_name);
            $('#legal-entity-name').text(response.le_name);
            $('#uploaded-file-name').text(response.csv_name);
            $('#uploaded-on').text(response.uploaded_on);
            $('#uploaded-by').text(response.uploaded_by);
            t_this._data_list_details = response.assign_statutory_data_list;
            t_this.displayDetailsPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ApproveAssignStatutoryBulkUpload.prototype.displayDetailsPage = function() {
    t_this = this;
    if (t_this._data_list_details.length > 0) {
        dataDetailsTableTbody.empty();
        var sno = 0;
        //   "d_name": "Finance Law",
        //   "u_code": "ZE00001",
        //   "bu_action": null,
        //   "c_task": "- Sample compliance Review",
        //   "u_name": "CBE UNIT",
        //   "s_prov": "Sample compliance Review",
        //   "c_desc": "Sample compliance Review",
        //   "s_status": 1,
        //   "as_id": 1,
        //   "p_leg": "Battries Act",
        //   "c_status": 1,
        //   "u_location": "Coimbatore",
        //   "remarks": null,
        //   "org_name": "Factory",
        //   "s_remarks": "",
        //   "s_leg": ""
        $.each(t_this._data_list_details, function(k, v) {
            sno++;
            var clone = $('#template #report-details-table tr').clone();
            $('.sno', clone).text(sno);

            $('.single-approve', clone).val(v.as_id).attr({ id:"approve"+v.as_id, onClick:"singleApprove(" + v.as_id + ")" });
            $('.single-reject', clone).val(v.as_id).attr({ id:"reject"+v.as_id, onClick:"singleReject(" + v.as_id + ")" });

            $('.rejected-reason', clone).html(v.s_remarks);
            $('.domain-name', clone).html(v.d_name);
            $('.unit-name span', clone).html(v.u_name);
            $('.unit-name i', clone).attr("title", v.u_location);
            $('.primary-legislation', clone).html(v.p_leg);
            // $('.primary-applicable', clone).html(v.p_leg);
            // $('.primary-not-applicable', clone).html(v.p_leg);
            // $('.primary-do-not-show', clone).html(v.p_leg);
            $('.statutory-remarks', clone).html(v.s_remarks);
            $('.secondary-legislation', clone).html(v.s_leg);
            $('.statutory-provision', clone).html(v.s_prov);
            $('.compliance-task-name span', clone).html(v.c_task);
            $('.compliance-task-name i', clone).attr("title", v.org_name);
            $('.compliance-description', clone).html(v.c_desc);
            dataDetailsTableTbody.append(clone);
        });
    } else {
        $('.pagination-view').show();
        showAnimation(reportView);
        REPORT.showReportValues(ReportData);
    }
};

singleApprove = function(id) {
    if($('#approve'+id).prop("checked") == true) {
      $('#reject'+id).attr("disabled","disabled");
    } else {
      $('#reject'+id).removeAttr("disabled");
    }
    multipleApprove([id]);
}

singleReject = function(id) {
    if($('#reject'+id).prop("checked") == true) {
      $('#approve'+id).attr("disabled","disabled");
    } else {
      $('#approve'+id).removeAttr("disabled");
    }
    multipleReject([id]);
}

multipleApprove = function(arr) {

}

multipleReject = function(arr) {

}

ApproveAssignStatutoryBulkUpload.prototype.loadFilterPage = function(id) {
    t_this = this;
    displayLoader();
    bu.getAssignStatutoryFilters(parseInt(id), function(error, response) {
        console.log("---------->"+response);
        // alert(response.toSource());
        if (error == null) {
            t_this._data_list_details = response.assign_statutory_data_list;
            t_this.displayDetailsPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};


REPORT = new ApproveAssignStatutoryBulkUpload();

$(document).ready(function() {
    REPORT.pageLoad();
    PageControls();
    viewListDetailsPage(1);
    $('#country').multiselect();
    $('#domain').multiselect();
    $('#unitname').multiselect();
    $('#actname').multiselect();
});