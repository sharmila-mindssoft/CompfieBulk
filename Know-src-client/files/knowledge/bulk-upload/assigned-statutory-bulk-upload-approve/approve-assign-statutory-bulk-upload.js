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
var approveId = $('#approve-id');
var approvePassword = $('#approve-password');

var passwordRejectSubmit = $('#password-reject-submit');
var rejectId = $('#reject-id');
var rejectPassword = $('#reject-password');
var rejectRemark = $('#remark');

var ASID = $("#assigned-statutory-id");

var dataDetailsTableTbody = $("#data-details-table-tbody");
var checkAllApprove = $("#check-all-approve");
var checkAllReject = $("#check-all-reject");

var domain = $("#domain");
var unit = $("#unit");
var primaryLegislation = $("#primary-legislation");

var secondaryLegislationName = $("#secondary-legislation");
// var secondaryLegislationId = $("#secondary-legislation-id");
var acSecondaryLegislation = $("#ac-secondary-legislation");

var statutoryProvisionName = $("#statutory-provision");
// var statutoryProvisionId = $("#statutory-provision-id");
var acStatutoryProvision = $("#ac-statutory-provision");

var complianceTaskName = $("#compliance-task");
var complianceTaskId = $("#compliance-task-id");
var acComplianceTask = $("#ac-compliance-task");

var statutoryStatus = $("#statutory-status");
var complianceStatus = $("#compliance-status");

var complianceDescriptionName = $("#compliance-description");
var complianceDescriptionId = $("#compliance-description-id");
var acComplianceDescription = $("#ac-compliance-description");

var search = $("#search");

var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var statutoryCount = $('.statutory_count');
var currentPage = 1;
var sno = 0;
var totalRecord;
var pageLimits;
var ItemsPerPage = $('#items_per_page');
var submit = $('#submit');

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
    this._filter_domain = [];
    this._filter_unit = [];
    this._filter_primary_legislation = []; 
    this._filter_secondary_legislation = [];
    this._filter_statutory_provision = [];
    this._filter_compliance_task = [];
    this._filter_statutory_status = [];
    this._filter_compliance_status = [];
    this._filter_compliance_description = [];
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

function PageControls() {

    clientGroupName.keyup(function(e) {
        var textVal = clientGroupName.val().trim();
        var clientGroupList = REPORT._client_group;
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acClientGroup, clientGroupId, textVal, clientGroupList, "cl_name", "cl_id", function(val) {
            onClientGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntityName.keyup(function(e) {
        var textVal = legalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        var condition_fields = ["cl_id"];
        var condition_values = [clientGroupId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, textVal, legalEntityList, "le_name", "le_id", function(val) {
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
        validateAuthentication(approveId.val(), approvePassword, null);
    });

    passwordRejectSubmit.click(function() {
        validateAuthentication(rejectId.val(), rejectPassword, rejectRemark);
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

    statutoryProvisionName.keyup(function(e) {
        var textVal = statutoryProvisionName.val().trim();
        var statutoryProvisionList = REPORT._filter_statutory_provision;
        arrayListSearch(e, textVal, statutoryProvisionList, acStatutoryProvision, function (val) {
          // onLegalEntitySuccess(val);
          statutoryProvisionName.val(val[1]);
        });
    });

    secondaryLegislationName.keyup(function(e) {
        var textVal = secondaryLegislationName.val().trim();
        var secondaryLegislationList = REPORT._filter_secondary_legislation;
        arrayListSearch(e, textVal, secondaryLegislationList, acSecondaryLegislation, function (val) {
          // onLegalEntitySuccess(val);
          secondaryLegislationName.val(val[1]);
        });
    });

    complianceTaskName.keyup(function(e) {
        var textVal = complianceTaskName.val().trim();
        var complianceTaskList = REPORT._filter_compliance_task;
        arrayListSearch(e, textVal, complianceTaskList, acComplianceTask, function (val) {
          // onLegalEntitySuccess(val);
          complianceTaskName.val(val[1]);
        });
    });

    complianceDescriptionName.keyup(function(e) {
        var textVal = complianceDescriptionName.val().trim();
        var complianceDescriptionList = REPORT._filter_compliance_description;
        arrayListSearch(e, textVal, complianceDescriptionList, acComplianceDescription, function (val) {
          // onLegalEntitySuccess(val);
          complianceDescriptionName.val(val[1]);
        });
    });

    search.click(function() {
        // radioInline
        // domain
        // unit
        // primaryLegislation
        // secondaryLegislationName
        // statutoryProvisionName
        // complianceTaskName
        // statutoryStatus
        // complianceStatus
        // complianceDescriptionName
        // alert(ASID.val()+' - '+domain.val()+' - '+unit.val()+' - '+primaryLegislation.val()+' - '+secondaryLegislationName.val()+' - '+statutoryProvisionName.val()+' - '+complianceTaskName.val()+' - '+statutoryStatus.val()+' - '+complianceDescriptionName.val());

        pageLimits = parseInt(ItemsPerPage.val());
        if (currentPage == 1)
            sno = 0;
        else
            sno = (currentPage - 1) * pageLimits;

        var view_data = $(".view-data:checked").val();
        REPORT.loadDetailsPageWithFilter(ASID.val(), view_data, domain.val(), unit.val(), primaryLegislation.val(), secondaryLegislationName.val(), statutoryProvisionName.val(), complianceTaskName.val(), statutoryStatus.val(), complianceStatus.val(), complianceDescriptionName.val());
    });

    submit.click(function() {
      REPORT.submitProcess();
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        currentPage = 1;
        createPageView(totalRecord);
        viewListDetailsPage(ASID.val());
    });
}

function arrayListSearch(e, textval, listval, acStatutoryProvision, callback) {
    var checkKey = [16, 17, 18, 19, 20, 27, 33, 34, 42, 91, 92, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144, 145];
    if (textval && textval.trim() != '' && listval.length > 0 && $.inArray(e.keyCode, checkKey) == -1) {
      let totalvalue = listval.filter((data) => {
        console.log((data.toLowerCase().indexOf(textval.toLowerCase()) > -1));
        return (data.toLowerCase().indexOf(textval.toLowerCase()) > -1);
      });
      let str = '';
      acStatutoryProvision.find('li').remove();
      if(totalvalue.length > 0) {
        for (var i = 0; i < totalvalue.length; ++i) {
          if(10 >= (i+1))
            str += '<li id="' + totalvalue[i] + '" onclick="activate_text(this,' + callback + ')">' + totalvalue[i] + '</li>';
        }
      }
      acStatutoryProvision.find('ul').append(str);
      acStatutoryProvision.show();
    } else {
      $('.ac-textbox').hide();
    }
    onArrowKey(e, acStatutoryProvision, callback);
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
    dataTableTbody.empty();
    if (t_this._data_list.length > 0) {
        var no = 0;
        $.each(t_this._data_list, function(k, v) {
            no++;
            var clone = $('#template #report-table tr').clone();
            $('.sno', clone).text(no);
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
            $('.download', clone).attr("onClick", "download('show-download" + v.csv_id + "')");
            $('.dropdown-content', clone).addClass("show-download" + v.csv_id);
            $('.approve a', clone).attr("onClick", "confirmationAction(" + v.csv_id + ", 'approve')");
            $('.reject a', clone).attr("onClick", "confirmationAction(" + v.csv_id + ", 'reject')");
            dataTableTbody.append(clone);
        });
    } else {
        hideLoader();
        var clone = $('#template #record-not-found tr').clone();
        dataTableTbody.append(clone);
        dataFilterHeader.hide();
    }
};

function confirmationAction(id, action) {
    approveId.val(id);
    rejectId.val(id);
    Custombox.open({
        target: '#custom-modal-'+action,
        effect: 'contentscale',
        complete: function() {
            approvePassword.focus();
            isAuthenticate = false;
        }
    });
}

function validateAuthentication(id, passwordField, remarkField) {
    var cl_id = clientGroupId.val();
    var le_id = legalEntityId.val();
    var password = passwordField.val().trim();
    var action = 1;
    if (password.length == 0) {
        displayMessage(message.password_required);
        passwordField.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    var remark = null;
    if (remarkField != null) {
        action = 0;
        remark = remarkField.val().trim();
        if (remark.length == 0) {
            displayMessage(message.remarks_required);
            remarkField.focus();
            return false;
        } else if (validateMaxLength('remark', remark, "Remark") == false) {
            return false;
        }
    }
    displayLoader();
    alert(parseInt(cl_id)+' - '+parseInt(le_id)+' - '+parseInt(id)+' - '+parseInt(action)+' - '+remark+' - '+password);
    bu.assignStatutoryActionInList(parseInt(cl_id), parseInt(le_id), parseInt(id), parseInt(action), remark, password, function(error, response) {
        console.log(error, response);
        if (error == null) {
            hideLoader();
            isAuthenticate = true;
            Custombox.close();
            if(action == 1)
              displaySuccessMessage(message.assign_statutory_approved_success);
            else
              displaySuccessMessage(message.assign_statutory_rejected_success);
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
}


viewListDetailsPage = function(id) {
    listPage.hide();
    dataListPage.show();

    $('#pending-data').trigger('click');

    /*domain
    unit
    primaryLegislation
    secondaryLegislationName
    acSecondaryLegislation
    statutoryProvisionName
    acStatutoryProvision
    complianceTaskName
    complianceTaskId
    statutoryStatus
    complianceStatus
    search
    complianceDescriptionName
    complianceDescriptionId
    acComplianceDescription*/

    pageLimits = parseInt(ItemsPerPage.val());
    if (currentPage == 1)
        sno = 0;
    else
        sno = (currentPage - 1) * pageLimits;

    REPORT.loadDetailsPage(id);
    REPORT.loadFilterPage(id);
}

ApproveAssignStatutoryBulkUpload.prototype.loadDetailsPage = function(id) {
    t_this = this;
    displayLoader();
    bu.getViewAssignStatutoryData(parseInt(id), parseInt(sno), parseInt(pageLimits), function(error, response) {
        console.log(error, response);
        if (error == null) {
            $('#client-group-name').text(response.cl_name);
            $('#legal-entity-name').text(response.le_name);
            $('#uploaded-file-name').text(response.csv_name);
            $('#uploaded-on').text(response.uploaded_on);
            $('#uploaded-by').text(response.uploaded_by);
            ASID.val(response.csv_id);
            totalRecord = 3;
            if (sno == 0) {
                createPageView(totalRecord);
            }
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
    is_null = true;
    var showFrom = sno + 1;
    if (t_this._data_list_details.length > 0) {
        dataDetailsTableTbody.empty();
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
        
        var no = 0;
        $.each(t_this._data_list_details, function(k, v) {
            is_null = false;
            sno = parseInt(sno) + 1;
            no++;
            var clone = $('#template #report-details-table tr').clone();
            $('.sno', clone).text(no);

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
        PaginationView.show();
    } else {
        PaginationView.hide();
    }

    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
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
        alert(response.toSource());
        if (error == null) {
            t_this._filter_domain = response.d_names;
            t_this._filter_unit = response.u_names;
            t_this._filter_primary_legislation = response.p_legis;
            t_this._filter_secondary_legislation = response.s_legis;
            // t_this._filter_statutory_provision = response.s_provs;
            t_this._filter_compliance_task = response.c_tasks;
            // t_this._filter_statutory_status = 
            // t_this._filter_compliance_status = 
            t_this._filter_compliance_description = response.c_descs;

            t_this.displayFilterList();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ApproveAssignStatutoryBulkUpload.prototype.displayFilterList = function() {
    t_this = this;

    domain.find("option").remove();
    unit.find("option").remove();
    primaryLegislation.find("option").remove();
    if (t_this._filter_domain.length > 0) {
      $.each(t_this._filter_domain, function(k, v) {
        domain.append('<option value="'+v+'">'+v+'</option>');
      });
      domain.multiselect();
    }

    if (t_this._filter_unit.length > 0) {
      $.each(t_this._filter_unit, function(k, v) {
        unit.append('<option value="'+v+'">'+v+'</option>');
      });
      unit.multiselect();
    }

    if (t_this._filter_primary_legislation.length > 0) {
      $.each(t_this._filter_primary_legislation, function(k, v) {
        primaryLegislation.append('<option value="'+v+'">'+v+'</option>');
      });
      primaryLegislation.multiselect();
    }

    if (t_this._filter_statutory_status.length > 0) {
      $.each(t_this._filter_statutory_status, function(k, v) {
        statutoryStatus.append('<option value="'+v+'">'+v+'</option>');
      });
      statutoryStatus.multiselect();
    }

    if (t_this._filter_compliance_status.length > 0) {
      $.each(t_this._filter_compliance_status, function(k, v) {
        complianceStatus.append('<option value="'+v+'">'+v+'</option>');
      });
      complianceStatus.multiselect();
    }

};

ApproveAssignStatutoryBulkUpload.prototype.loadDetailsPageWithFilter = function(id, v_data, d_names, u_names, p_leg, s_leg, s_pro, c_task, s_status, c_status, c_des) {
    t_this = this;
    // v_data
    if(d_names != null) { d_names = d_names.join(); }
    if(u_names != null) { u_names = u_names.join(); }
    if(p_leg != null) { p_leg = p_leg.join(); }
    if(s_leg == "") { s_leg = null; }
    if(s_pro == "") { s_pro = null; }
    if(c_task == "") { c_task = null; }
    if(s_status == "") { s_status = null; }
    if(c_status == "") { c_status = null; }
    if(c_des == "") { c_des = null; }

    displayLoader();
    bu.getViewAssignStatutoryDataFromFilter(parseInt(id), parseInt(sno), parseInt(pageLimits),  d_names, u_names, p_leg, s_leg, s_pro, c_task, c_des, function(error, response) {
        console.log(error, response);
        if (error == null) {
            t_this._data_list_details = response.assign_statutory_data_list;
            totalRecord = 3;
            t_this.displayDetailsPage();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    statutoryCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    statutoryCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(currentPage) != cPage) {
                currentPage = cPage;
                viewListDetailsPage(ASID.val());
            }
        }
    });
};

ApproveAssignStatutoryBulkUpload.prototype.submitProcess = function() {
  alert('ko');

}

REPORT = new ApproveAssignStatutoryBulkUpload();

$(document).ready(function() {
    REPORT.pageLoad();
    PageControls();
    loadItemsPerPage();
    viewListDetailsPage(1);
});