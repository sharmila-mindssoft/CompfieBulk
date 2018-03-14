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

var singleRejectRemark = $('#single-reject-remark');
var passwordSingleRejectSubmit = $('#password-single-reject-submit');
var singleRejectId = $('#single-reject-id');


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

var viewDataFiltered = $(".view-data-filtered");
var domainFiltered = $(".domain-filtered");
var unitFiltered = $(".unit-filtered");
var primaryLegislationFiltered = $(".primary-legislation-filtered");
var secondaryLegislationFiltered = $(".secondary-legislation-filtered");
var statutoryProvisionFiltered = $(".statutory-provision-filtered");
var complianceTaskFiltered = $(".compliance-task-filtered");
var statutoryTaskFiltered = $(".statutory-task-filtered");
var complianceStatusFiltered = $(".compliance-status-filtered");
var domplianceDescriptionFiltered = $(".dompliance-description-filtered");
var clearFiltered = $(".clear-filtered");
var filtered = $(".filtered");

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

ApproveAssignStatutoryBulkUpload = function() {
    // JSON.parse('[{"client_group_name":"Group one","is_active":true,"client_id":1},{"client_group_name":"Group two","is_active":true,"client_id":2},{"client_group_name":"Group three","is_active":false,"client_id":3}]');
    this._client_group = []; 
    this._entities = [];
    this._data_list = [];
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
            // showAnimation(listView);
            REPORT.fetchStatutoryValues();
        }
    });

    downloadBtn.click(function() {
        // alert('ji');
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
        confirmationAction(0, 'single-reject');
      } else {
        $('.single-reject').removeAttr("checked");
        $('.single-approve').removeAttr("disabled");
        checkAllApprove.removeAttr("disabled");
      }
    });

    passwordSingleRejectSubmit.click(function() {
      var remark = singleRejectRemark.val().trim();
      if (remark.length == 0) {
          displayMessage(message.remarks_required);
          singleRejectRemark.focus();
          checkAllReject.removeAttr("checked");
          return false;
      } else if (validateMaxLength('remark', remark, "Remark") == false) {
          checkAllReject.removeAttr("checked");
          return false;
      } else {
        Custombox.close();
        if(checkAllReject.prop("checked") == true) {
          $('.single-reject').removeAttr("checked");
          $('.single-reject').trigger('click');
          $('.single-approve').attr("disabled","disabled");
          checkAllApprove.attr("disabled","disabled"); 
        } else {
          singleReject(singleRejectId.val(), true);
        }
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
          complianceDescriptionName.val(val[1]);
        });
    });

    search.click(function() {
      if($(".view-data:checked").val() == "1")
        viewDataFiltered.html("View Data : Verified");
      else if($(".view-data:checked").val() == "0")
        viewDataFiltered.html("View Data : Pending");
      else
        viewDataFiltered.html("");

      if(domain.val() != null)
        domainFiltered.html("Domain Name : "+domain.val().join());
      else
        domainFiltered.html("");

      if(unit.val() != null) {
        var unitText = "";
        $.each(unit.find('option:selected'), function() {
            (unitText != "") ? unitText = unitText+', '+$(this).text() : unitText = $(this).text();
        });
        unitFiltered.html("Unit Name : "+unitText);
      } else {
        unitFiltered.html("");
      }

      // unitFiltered.html();
      // primaryLegislationFiltered.html();
      // secondaryLegislationFiltered.html();
      // statutoryProvisionFiltered.html();
      // complianceTaskFiltered.html();
      // statutoryTaskFiltered.html();
      // complianceStatusFiltered.html();
      // domplianceDescriptionFiltered.html();
      // clearFiltered

      viewListDetailsPage(ASID.val());
    });
    
    clearFiltered.click(function() {
      filtered.empty();
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

/*showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
}*/

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
            // getDomainUserInfo(domain_user_id, group_id, entity_id, domain_id, callback)
            $('.no-of-records', clone).html(v.no_of_records);
            if (v.approved_count != 0 || v.rej_count != 0) {
                if (v.approved_count == 0) { v.approved_count = 0; }
                if (v.rej_count == 0) { v.rej_count = 0; }
                $('.approve-reject', clone).html(v.approved_count + '/' + v.rej_count);
                $('.view', clone).html('<a><i class="fa fa-pencil text-primary c-pointer"></i></a>')
                    .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
            } else {
                $('.view', clone).html('<button class="btn btn-primary text-center waves-effect waves-light" type="button"> View </button>')
                    .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
            }
            $('.download', clone).attr("onClick", "download('show-download" + v.csv_id + "')");

            /*$('.download .dowload-excel', clone).attr("onClick", "downloadFile('" + v.download_file + "', 'xlsx')");
            $('.download .dowload-csv', clone).attr("onClick", "downloadFile('" + v.download_file + "', 'csv')");
            $('.download .dowload-ods', clone).attr("onClick", "downloadFile('" + v.download_file + "', 'ods')");
            $('.download .dowload-text', clone).attr("onClick", "downloadFile('" + v.download_file + "', 'txt')");*/

            //bulkuploadcsv
            $('.download .dowload-excel', clone).attr("href", "/uploaded_file/xlsx/" + v.download_file.split('.')[0] + ".xlsx");
            $('.download .dowload-csv', clone).attr("href", "/uploaded_file/csv/" + v.download_file.split('.')[0] + ".csv");
            $('.download .dowload-ods', clone).attr("href", "/uploaded_file/ods/" + v.download_file.split('.')[0] + ".ods)");
            $('.download .dowload-text', clone).attr("href", "/uploaded_file/txt/" + v.download_file.split('.')[0] + ".txt");

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

downloadFile = function(name, ext) {
  fileName = name.split('.');
  var file_path = '';
  if(ext == "xlsx") {
    file_path = "/bulkuploadcsv/xlsx/" + InvalidFileName[0] + '.xlsx';
  } else if (ext == "csv") {
    file_path = "/bulkuploadcsv/csv/" + InvalidFileName[0] + '.csv';
  } else if (ext == "ods") {
    file_path = "/bulkuploadcsv/ods/" + InvalidFileName[0] + '.ods';
  } else if (ext == "txt") {
    file_path = "/bulkuploadcsv/txt/" + InvalidFileName[0] + '.txt';
  }
}

function confirmationAction(id, action) {
    approveId.val(id);
    rejectId.val(id);
    singleRejectRemark.val("");
    rejectRemark.val("");
    Custombox.open({
        target: '#custom-modal-'+action,
        effect: 'contentscale',
        complete: function() {
            approvePassword.focus();
        }
    });
}

function closeCustombox() {
  checkAllReject.removeAttr("checked");
  Custombox.close();
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
        action = 2;
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
    bu.assignStatutoryActionInList(parseInt(cl_id), parseInt(le_id), parseInt(id), parseInt(action), remark, password, function(error, response) {
        console.log(error, response);
        if (error == null) {
            hideLoader();
            Custombox.close();
            if(action == 1)
              displaySuccessMessage(message.assign_statutory_approved_success);
            else
              displaySuccessMessage(message.assign_statutory_rejected_success);
            REPORT.fetchStatutoryValues();
        } else {
            REPORT.possibleFailures(error);
            hideLoader();
        }
    });
}

goToDetailsPage = function(id) {
  $(".all-data").trigger('click');
  domain.find("option").remove();
  unit.find("option").remove();
  primaryLegislation.find("option").remove();
  secondaryLegislationName.val("");
  statutoryProvisionName.val("");
  complianceTaskName.val("");
  statutoryStatus.val("");
  complianceStatus.val("");
  complianceDescriptionName.val("");
  viewListDetailsPage(id);
}


viewListDetailsPage = function(id) {
    listPage.hide();
    dataListPage.show();

    pageLimits = parseInt(ItemsPerPage.val());
    if (currentPage == 1)
        sno = 0;
    else
        sno = (currentPage - 1) * pageLimits;

    REPORT.loadFilterPage(id);

    var view_data = $(".view-data:checked").val();
    REPORT.loadDetailsPageWithFilter(id, view_data, domain.val(), unit.val(), primaryLegislation.val(), secondaryLegislationName.val(), statutoryProvisionName.val(), complianceTaskName.val(), statutoryStatus.val(), complianceStatus.val(), complianceDescriptionName.val());
}

ApproveAssignStatutoryBulkUpload.prototype.displayDetailsPage = function() {
    t_this = this;
    is_null = true;
    var showFrom = sno + 1;
    dataDetailsTableTbody.empty();
    if (t_this._data_list_details.length > 0) {
        var no = 0;
        $.each(t_this._data_list_details, function(k, v) {
            is_null = false;
            sno = parseInt(sno) + 1;
            no++;
            var clone = $('#template #report-details-table tr').clone();
            $('.sno', clone).text(no);

            $('.single-approve', clone).val(v.as_id).attr({ id:"approve"+v.as_id, onClick:"singleApprove(" + v.as_id + ")" });
            $('.single-reject', clone).val(v.as_id).attr({ id:"reject"+v.as_id, onClick:"singleReject(" + v.as_id + ", false)" });

            if(v.bu_action == 1) {
              $('.single-approve', clone).prop('checked', true);
              $('.single-reject', clone).attr("disabled","disabled");
            } else if(v.bu_action == 2) {
              $('.single-reject', clone).prop('checked', true);
              $('.single-approve', clone).attr("disabled","disabled");
              if(v.remarks != "")
                $('.rejected-reason', clone).html('<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" data-toggle="tooltip" title="" data-original-title="'+v.remarks+'"></i>');
            }
            $('.domain-name', clone).html(v.d_name);
            $('.unit-name span', clone).html(v.u_name);
            $('.unit-name i', clone).attr("title", v.u_location);
            $('.primary-legislation', clone).html(v.p_leg);
            
            if(v.c_status == 1)
              $('.compliance-applicable i', clone).addClass("text-info");
            else if(v.c_status == 2)
              $('.compliance-not-applicable', clone).addClass("text-warning");
            else if(v.c_status == 3)
              $('.compliance-do-not-show', clone).addClass("text-warning");

            if(v.s_status == 1)
              $('.statutory-applicable i', clone).addClass("text-info");
            else if(v.s_status == 2)
              $('.statutory-not-applicable', clone).addClass("text-warning");
            else if(v.s_status == 3)
              $('.statutory-do-not-show', clone).addClass("text-warning");

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
      tempAction(id, 1);
    } else {
      $('#reject'+id).removeAttr("disabled");
    }
}

singleReject = function(id, flag) {
    if($('#reject'+id).prop("checked") == true) { 
      if(checkAllReject.prop("checked") == false) {
        if(flag == false) {
          singleRejectId.val(id);
          confirmationAction(0, 'single-reject');
        } else {
          $('#approve'+id).attr("disabled","disabled");
          tempAction(id, 2);
        }
      } else {
        $('#approve'+id).attr("disabled","disabled");
        tempAction(id, 2);
      }
    } else {
      $('#approve'+id).removeAttr("disabled");
    }
}

tempAction = function(id, action) {
  var csvid = ASID.val();
  var remarks = singleRejectRemark.val();
  displayLoader();
  bu.updateAssignStatutoryActionFromView(parseInt(csvid), parseInt(id), parseInt(action), remarks, function(error, response) {
      if (error == null) {
          viewListDetailsPage(csvid);
          hideLoader();
      } else {
          REPORT.possibleFailures(error);
          hideLoader();
      }
  });
}

ApproveAssignStatutoryBulkUpload.prototype.loadFilterPage = function(id) {
    t_this = this;
    displayLoader();
    bu.getAssignStatutoryFilters(parseInt(id), function(error, response) {
        // console.log("---------->"+response);
        // alert(response.toSource());
        if (error == null) {
            t_this._filter_domain = response.d_names;
            t_this._filter_unit = response.u_names;
            t_this._filter_primary_legislation = response.p_legis;
            t_this._filter_secondary_legislation = response.s_legis;
            t_this._filter_statutory_provision = response.s_provs;
            t_this._filter_compliance_task = response.c_tasks;
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
    
    if (t_this._filter_domain.length > 0 && domain.val() == null) {
      domain.find("option").remove();
      $.each(t_this._filter_domain, function(k, v) {
        domain.append('<option value="'+v+'">'+v+'</option>');
      });
      domain.multiselect();
    }

    if (t_this._filter_unit.length > 0 && unit.val() == null) {
      unit.find("option").remove();
      $.each(t_this._filter_unit, function(k, v) {
        unit.append('<option value="'+v.split("-")[0].trim()+'">'+v+'</option>');
      });
      unit.multiselect();
    }

    if (t_this._filter_primary_legislation.length > 0 && primaryLegislation.val() == null) {
      primaryLegislation.find("option").remove();
      $.each(t_this._filter_primary_legislation, function(k, v) {
        primaryLegislation.append('<option value="'+v+'">'+v+'</option>');
      });
      primaryLegislation.multiselect();
    }

    if (t_this._filter_statutory_status.length > 0 && statutoryStatus.val() == "") {
      $.each(t_this._filter_statutory_status, function(k, v) {
        statutoryStatus.append('<option value="'+v+'">'+v+'</option>');
      });
      statutoryStatus.multiselect();
    }

    if (t_this._filter_compliance_status.length > 0 && complianceStatus.val() == "") {
      $.each(t_this._filter_compliance_status, function(k, v) {
        complianceStatus.append('<option value="'+v+'">'+v+'</option>');
      });
      complianceStatus.multiselect();
    }

};

ApproveAssignStatutoryBulkUpload.prototype.loadDetailsPageWithFilter = function(id, v_data, d_names, u_names, p_leg, s_leg, s_pro, c_task, s_status, c_status, c_des) {
    t_this = this;
    if(d_names != null) { d_names = d_names.join(); }
    if(u_names != null) { u_names = u_names.join(); }
    if(p_leg != null) { p_leg = p_leg.join(); }
    if(s_leg == "") { s_leg = null; }
    if(s_pro == "") { s_pro = null; }
    if(c_task == "") { c_task = null; }
    if(c_des == "") { c_des = null; }
    if(s_status == "") { s_status = null; } else { s_status = parseInt(s_status); }
    if(c_status == "") { c_status = null; }  else { c_status = parseInt(c_status); }
    if(v_data == "") { v_data = null; }  else { v_data = parseInt(v_data); }
    displayLoader();
    bu.getViewAssignStatutoryDataFromFilter(parseInt(id), parseInt(sno), parseInt(pageLimits),  d_names, u_names, p_leg, s_leg, s_pro, c_task, c_des, v_data, s_status, c_status, function(error, response) {
        // console.log(error, response);
        alert(response.toSource());
        if (error == null) {
            t_this._data_list_details = response.assign_statutory_data_list;
            totalRecord = 3;
            t_this.displayDetailsPage();
            ASID.val(id);
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
  var csvid = ASID.val();
  var cl_id = clientGroupId.val();
  var le_id = legalEntityId.val();

  displayLoader();
  bu.confirmAssignStatutoryUpdateAction(parseInt(csvid), parseInt(cl_id), parseInt(le_id), function(error, response) {
      if (error == null) {
          displaySuccessMessage(message.assign_statutory_submit_success);
          REPORT.pageLoad();
          PageControls();
          hideLoader();
      } else {
          t_this.possibleFailures(error);
          hideLoader();
      }
  });

}

REPORT = new ApproveAssignStatutoryBulkUpload();

$(document).ready(function() {
    REPORT.pageLoad();
    PageControls();
    loadItemsPerPage();
    // viewListDetailsPage(3);
});