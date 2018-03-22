var listPage = $(".list-page");
var dataListPage = $(".data-list-page");

var clientGroup = $("#client-group");
var clientGroupId = $("#client-group-id");
var acClientGroup = $("#ac-client-group");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

var showButton = $("#show-button");
var listView = $("#list-view");

var dataTableTbody = $("#data-table-tbody");

var downloadBtn = $(".download");
var passwordApproveSubmit = $('#password-approve-submit');
var approveId = $('#approve-id');
var approvePassword = $('#approve-password');

var passwordRejectSubmit = $('#password-reject-submit');
var rejectId = $('#reject-id');
var rejectPassword = $('#reject-password');
var rejectReason = $('#remark');

var singleRejectReason = $('#single-reject-remark');
var passwordSingleRejectSubmit = $('#password-single-reject-submit');
var singleRejectId = $('#single-reject-id');

var filterUploadedFileName = $('#filter-uploaded-file-name');
var filterUploadedOn = $('#filter-uploaded-on');
var filterUploadedBy = $('#filter-uploaded-by');
var filterNoOfRecords = $('#filter-no-of-records');

var ASID = $("#assigned-statutory-id");

var dataDetailsTableTbody = $("#data-details-table-tbody");
var checkAllApprove = $("#check-all-approve");
var checkAllReject = $("#check-all-reject");

var domain = $("#domain");
var unit = $("#unit");
var primaryLegislation = $("#primary-legislation");

var secondaryLegislationName = $("#secondary-legislation");
var acSecondaryLegislation = $("#ac-secondary-legislation");

var statutoryProvisionName = $("#statutory-provision");
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
var showCount = $('.show-count');
var currentPage = 1;
var sno = 0;
var totalRecord;
var pageLimits;
var ItemsPerPage = $('#items_per_page');
var submit = $('#submit');

var clientGroupName = $('#client-group-name');
var legalEntityName = $('#legal-entity-name');
var uploadedFileName = $('#uploaded-file-name');
var uploadedOn = $('#uploaded-on');
var uploadedBy = $('#uploaded-by');

var filteredData = $(".filtered-data");
var clearFiltered = $(".clear-filtered");

var filterDomain = $("#filter-domain");
var filterUnit = $("#filter-unit");
var filterPrimaryLegislation = $("#filter-primary-legislation");
var filterSecondaryLegislation = $("#filter-secondary-legislation");
var filterStatutoryProvision = $("#filter-statutory-provision");
var filterComplianceTask = $("#filter-compliance-task");
var filterComplianceDescription = $("#filter-compliance-description");

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
  this._UserList = [];
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
  clientGroup.val('');
  clientGroupId.val('');
  legalEntity.val('');
  legalEntityId.val('');
  filterUploadedFileName.val('');
  filterUploadedOn.val('');
  filterUploadedBy.val('');
  filterNoOfRecords.val('');
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

ApproveAssignStatutoryBulkUpload.prototype.failuresMessage = function(error) {
  if (error == 'InvalidPassword') {
    displayMessage(message.invalid_password);
  } else {
    displayMessage(error);
  }
};

function PageControls() {

  clientGroup.keyup(function(e) {
    var textVal = clientGroup.val().trim();
    var clientGroupList = REPORT._client_group;
    var condition_fields = [];
    var condition_values = [];
    commonAutoComplete(e, acClientGroup, clientGroupId, textVal,
      clientGroupList, "cl_name", "cl_id",
      function(val) {
        onClientGroupAutoCompleteSuccess(REPORT, val);
      }, condition_fields, condition_values);
  });

  legalEntity.keyup(function(e) {
    var textVal = legalEntity.val().trim();
    var legalEntityList = REPORT._entities;
    var condition_fields = ["cl_id"];
    var condition_values = [clientGroupId.val()];
    commonAutoComplete(e, acLegalEntity, legalEntityId, textVal,
      legalEntityList, "le_name", "le_id",
      function(val) {
        onLegalEntityAutoCompleteSuccess(REPORT, val);
      }, condition_fields, condition_values);
  });

  showButton.click(function() {
    if (validate()) {
      listView.show();
      REPORT.fetchStatutoryValues(clientGroupId.val(), legalEntityId.val());
    }
  });

  downloadBtn.click(function() {
    this.find('.dropdown-content').show();
  });

  passwordApproveSubmit.click(function() {
    validateAuthentication(approveId.val(), approvePassword, null);
  });

  passwordRejectSubmit.click(function() {
    validateAuthentication(rejectId.val(), rejectPassword, rejectReason);
  });

  filterUploadedFileName.keyup(function() {
    fList = key_search_list(REPORT._data_list);
    REPORT.displayListPage(fList);
  });

  filterUploadedOn.keyup(function() {
    fList = key_search_list(REPORT._data_list);
    REPORT.displayListPage(fList);
  });

  filterUploadedBy.keyup(function() {
    fList = key_search_list(REPORT._data_list);
    REPORT.displayListPage(fList);
  });

  filterNoOfRecords.keyup(function() {
    fList = key_search_list(REPORT._data_list);
    REPORT.displayListPage(fList);
  });

  checkAllApprove.click(function() {
    if ($(this).prop("checked") == true) {
      dataDetailsTableTbody.find('.single-approve').removeAttr("checked");
      dataDetailsTableTbody.find('.single-approve').trigger('click');
    } else {
      dataDetailsTableTbody.find('.single-approve').removeAttr("checked");
      // dataDetailsTableTbody.find('.single-reject').removeAttr("disabled");
      // checkAllReject.removeAttr("disabled");
    }
  });

  checkAllReject.click(function() {
    if ($(this).prop("checked") == true) {
      confirmationAction(0, 'single-reject');
    } else {
      dataDetailsTableTbody.find('.single-reject').removeAttr("checked");
      // dataDetailsTableTbody.find('.single-approve').removeAttr("disabled");
      // checkAllApprove.removeAttr("disabled");
    }
  });

  passwordSingleRejectSubmit.click(function() {
    var reason = singleRejectReason.val().trim();
    if (reason.length == 0) {
      displayMessage(message.reason_required);
      singleRejectReason.focus();
      checkAllReject.removeAttr("checked");
      return false;
    } else if (validateMaxLength('reason', reason, "Reason") == false) {
      checkAllReject.removeAttr("checked");
      return false;
    } else {
      Custombox.close();
      if (checkAllReject.prop("checked") == true) {
        dataDetailsTableTbody.find('.single-reject').removeAttr("checked");
        dataDetailsTableTbody.find('.single-reject').trigger('click');
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
    arrayListSearch(e, textVal, statutoryProvisionList,
      acStatutoryProvision,
      function(val) {
        statutoryProvisionName.val(val[1]);
      });
  });

  secondaryLegislationName.keyup(function(e) {
    var textVal = secondaryLegislationName.val().trim();
    var secondaryLegislationList = REPORT._filter_secondary_legislation;
    arrayListSearch(e, textVal, secondaryLegislationList,
      acSecondaryLegislation,
      function(val) {
        secondaryLegislationName.val(val[1]);
      });
  });

  complianceTaskName.keyup(function(e) {
    var textVal = complianceTaskName.val().trim();
    var complianceTaskList = REPORT._filter_compliance_task;
    arrayListSearch(e, textVal, complianceTaskList,
      acComplianceTask,
      function(val) {
        complianceTaskName.val(val[1]);
      });
  });

  complianceDescriptionName.keyup(function(e) {
    var textVal = complianceDescriptionName.val().trim();
    var complianceDescriptionList = REPORT._filter_compliance_description;
    arrayListSearch(e, textVal, complianceDescriptionList,
      acComplianceDescription,
      function(val) {
        complianceDescriptionName.val(val[1]);
      });
  });

  search.click(function() {
    var tempArr = [];

    if ($(".view-data:checked").val() == "1")
      tempArr.push("View Data : Verified");
    else if ($(".view-data:checked").val() == "0")
      tempArr.push("View Data : Pending");

    if (domain.val() != null)
      tempArr.push("Domain Name : " + domain.val().join());

    if (unit.val() != null) {
      var u = "";
      $.each(unit.find('option:selected'), function() {
        (u != "") ? u = u + ', ' + $(this).text(): u = $(this).text();
      });
      tempArr.push("Unit Name : " + u);
    }

    if (primaryLegislation.val() != null)
      tempArr.push("Primary Legislation : " + primaryLegislation.val().join());

    if (secondaryLegislationName.val() != "")
      tempArr.push("Secondary Legislation : " + secondaryLegislationName.val());

    if (statutoryProvisionName.val() != "")
      tempArr.push("Statutory Provision : " + statutoryProvisionName.val());

    if (complianceTaskName.val() != "")
      tempArr.push("Compliance Task Name : " + complianceTaskName.val());

    if (statutoryStatus.val() != "")
      tempArr.push("Statutory Status : " + statutoryStatus.find('option:selected').text());

    if (complianceStatus.val() != "")
      tempArr.push("Compliance Status : " + complianceStatus.find('option:selected').text());

    if (complianceDescriptionName.val() != "")
      tempArr.push("Compliance Description : " + complianceDescriptionName.val());

    tex = "";
    if (tempArr.length > 0) {
      clearFiltered.show();
      for (var i = 0; i < tempArr.length; i++) {
        (tex != "") ? tex = tex + ' | ' + tempArr[i]: tex = tempArr[i];
      }
      filteredData.html("Filtered By - " + tex);
    } else {
      filteredData.empty();
      clearFiltered.hide();
    }
    if (acSecondaryLegislation.is(':visible') == true) {
      displayMessage(message.secondary_legislation_required);
      return false;
    } else if (acStatutoryProvision.is(':visible') == true) {
      displayMessage(message.statutory_provision_required);
      return false;
    } else if (acComplianceTask.is(':visible') == true) {
      displayMessage(message.compliance_task_required);
      return false;
    } else if (acComplianceDescription.is(':visible') == true) {
      displayMessage(message.compliance_description_required);
      return false;
    } else {
      sno = 0;
      currentPage = 1;
      viewListDetailsPage(ASID.val());
    }
  });

  clearFiltered.click(function() {
    goToDetailsPage(ASID.val());
  });

  submit.click(function() {
    var approveCount = dataDetailsTableTbody.find('.single-approve:checked').length;
    var rejectCount = dataDetailsTableTbody.find('.single-reject:checked').length;
    if (approveCount == 0 || rejectCount) {
      displayMessage(message.action_selection_required);
    } else {
      // to check the record checked all the action need to check temp db
      REPORT.submitProcess();
    }
    // REPORT.submitProcess();
  });

  ItemsPerPage.on('change', function(e) {
    perPage = parseInt($(this).val());
    sno = 0;
    currentPage = 1;
    createPageView(totalRecord);
    viewListDetailsPage(ASID.val());
  });

  filterDomain.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterUnit.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterPrimaryLegislation.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterSecondaryLegislation.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterStatutoryProvision.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterComplianceTask.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });

  filterComplianceDescription.keyup(function() {
    fList = key_search_details_list(REPORT._data_list_details);
    REPORT.displayDetailsPage(fList, true);
  });
}

function arrayListSearch(e, textval, listval, acDiv, callback) {
  var checkKey = [16, 17, 18, 19, 20, 27, 33, 34, 42, 91, 92, 112, 113,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144, 145
  ];
  if (textval && textval.trim() != '' && listval.length > 0 &&
    $.inArray(e.keyCode, checkKey) == -1) {
    let tot = listval.filter((data) => {
      console.log((data.toLowerCase().indexOf(textval.toLowerCase()) > -1));
      return (data.toLowerCase().indexOf(textval.toLowerCase()) > -1);
    });
    let str = '';
    acDiv.find('li').remove();
    if (tot.length > 0) {
      for (var i = 0; i < tot.length; ++i) {
        if (10 >= (i + 1))
          str += '<li id="' + tot[i] + '" ' +
          'onclick="activate_text(this,' + callback + ')">' + tot[i] + '</li>';
      }
    }
    acDiv.find('ul').append(str);
    acDiv.show();
  } else {
    $('.ac-textbox').hide();
  }
  onArrowKey(e, acDiv, callback);
}

clearElement = function(arr) {
  if (arr.length > 0) {
    $.each(arr, function(i, element) {
      element.val('');
    });
  }
}

onClientGroupAutoCompleteSuccess = function(REPORT, val) {
  clientGroup.val(val[1]);
  clientGroupId.val(val[0]);
  clientGroup.focus();
  clearElement([legalEntity, legalEntityId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
  legalEntity.val(val[1]);
  legalEntityId.val(val[0]);
  legalEntity.focus();
}

validate = function() {
  is_valid = true;
  if (clientGroup.val().trim().length == 0) {
    displayMessage(message.client_group_required);
    is_valid = false;
  } else if (clientGroup.val().trim().length > 50) {
    displayMessage(message.client_group_50);
    is_valid = false;
  } else if (legalEntity.val().trim().length == 0) {
    displayMessage(message.legalentity_required);
    is_valid = false;
  } else if (legalEntity.val().trim().length > 50) {
    displayMessage(message.le_50);
    is_valid = false;
  }
  return is_valid;
};

key_search_list = function(d) {
  key_one = filterUploadedFileName.val().toLowerCase();
  key_two = filterUploadedOn.val().toLowerCase();
  key_three = filterUploadedBy.val().toLowerCase();
  key_four = filterNoOfRecords.val();
  var fList = [];
  for (var e in d) {
    var value_one = d[e].csv_name.toLowerCase();
    var value_two = d[e].uploaded_on.toLowerCase();
    var value_three = d[e].uploaded_by.toString().toLowerCase();
    var value_four = d[e].no_of_records.toString();
    if ((~value_one.indexOf(key_one)) && (~value_two.indexOf(key_two)) &&
      (~value_three.indexOf(key_three)) && (~value_four.indexOf(key_four))) {
      fList.push(d[e]);
    }
  }
  return fList
}

key_search_details_list = function(d) {
  key_one = filterDomain.val().toLowerCase();
  key_two = filterUnit.val().toLowerCase();
  key_three = filterPrimaryLegislation.val();
  key_four = filterSecondaryLegislation.val();
  key_five = filterStatutoryProvision.val();
  key_six = filterComplianceTask.val();
  key_seven = filterComplianceDescription.val();
  var fList = [];
  for (var e in d) {
    var value_one = d[e].d_name.toLowerCase();
    var value_two = d[e].u_name.toLowerCase();
    var value_three = d[e].p_leg.toLowerCase();
    var value_four = d[e].s_leg.toLowerCase();
    var value_five = d[e].s_prov.toLowerCase();
    var value_six = d[e].c_task.toLowerCase();
    var value_seven = d[e].c_desc.toLowerCase();
    if ((~value_one.indexOf(key_one)) && (~value_two.indexOf(key_two)) &&
      (~value_three.indexOf(key_three)) && (~value_four.indexOf(key_four)) &&
      (~value_five.indexOf(key_five)) && (~value_six.indexOf(key_six)) &&
      (~value_seven.indexOf(key_seven))) {
      fList.push(d[e]);
    }
  }
  return fList
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


ApproveAssignStatutoryBulkUpload.prototype.fetchStatutoryValues = function(c_id, le_id) {
  t_this = this;
  /*c_id = clientGroupId.val();
  le_id = legalEntityId.val();*/
  displayLoader();
  bu.getAssignStatutoryForApprove(parseInt(c_id),
    parseInt(le_id),
    function(error, response) {
      // console.log(error, response);
      if (error == null) {
        t_this._data_list = response.pending_csv_list_as;
        mirror.getDomainUserInfo(function(err, resp) {
          if (err == null) {
            t_this._UserList = resp.domain_executive_info;
            for (var i = 0; i < t_this._data_list.length; i++) {
              for (var j = 0; j < t_this._UserList.length; j++) {
                if (t_this._data_list[i].uploaded_by == t_this._UserList[j].user_id) {
                  t_this._data_list[i].uploaded_by = t_this._UserList[j].emp_code_name;
                  break;
                }
              }
            }
            t_this.displayListPage(t_this._data_list);
            hideLoader();
          } else {
            hideLoader();
            t_this.failuresMessage(err);
          }
        });
      } else {
        t_this.failuresMessage(error);
        hideLoader();
      }
    });
};

ApproveAssignStatutoryBulkUpload.prototype.displayListPage = function(data) {
  t_this = this;
  dataTableTbody.empty();
  if (data.length > 0) {
    var no = 0;
    $.each(data, function(k, v) {
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
        $('.view', clone)
          .html('<a><i class="fa fa-pencil text-primary c-pointer"></i></a>')
          .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
      } else {
        $('.view', clone)
          .html('<button class="btn btn-primary ' +
            'text-center waves-effect waves-light" type="button"> View </button>')
          .attr("onClick", "goToDetailsPage(" + v.csv_id + ")");
      }
      $('.fa-download', clone)
        .attr("onClick", "download('show-download" + v.csv_id + "')");
      $('.download .dowload-excel', clone)
        .attr("href", "/uploaded_file/xlsx/" + v.download_file.split('.')[0] + ".xlsx");
      $('.download .dowload-csv', clone)
        .attr("href", "/uploaded_file/csv/" + v.download_file.split('.')[0] + ".csv");
      $('.download .dowload-ods', clone)
        .attr("href", "/uploaded_file/ods/" + v.download_file.split('.')[0] + ".ods)");
      $('.download .dowload-text', clone)
        .attr("href", "/uploaded_file/txt/" + v.download_file.split('.')[0] + ".txt");
      $('.dropdown-content', clone).addClass("show-download" + v.csv_id);
      $('.approve a', clone)
        .attr("onClick", "confirmationAction(" + v.csv_id + ", 'approve')");
      $('.reject a', clone)
        .attr("onClick", "confirmationAction(" + v.csv_id + ", 'reject')");
      dataTableTbody.append(clone);
    });
  } else {
    hideLoader();
    var clone = $('#template #record-not-found tr').clone();
    dataTableTbody.append(clone);
  }
};

/*downloadFile = function(name, ext) {
  fileName = name.split('.');
  var file_path = '';
  if (ext == "xlsx") {
    file_path = "/bulkuploadcsv/xlsx/" + InvalidFileName[0] + '.xlsx';
  } else if (ext == "csv") {
    file_path = "/bulkuploadcsv/csv/" + InvalidFileName[0] + '.csv';
  } else if (ext == "ods") {
    file_path = "/bulkuploadcsv/ods/" + InvalidFileName[0] + '.ods';
  } else if (ext == "txt") {
    file_path = "/bulkuploadcsv/txt/" + InvalidFileName[0] + '.txt';
  }
}*/

function confirmationAction(id, action) {
  approveId.val(id);
  rejectId.val(id);
  singleRejectReason.val("");
  rejectReason.val("");
  approvePassword.val("");
  rejectPassword.val("");
  Custombox.open({
    target: '#custom-modal-' + action,
    effect: 'contentscale',
    complete: function() {
      approvePassword.focus();
    }
  });
}

function closeCustombox() {
  checkAllReject.removeAttr("checked");
  Custombox.close();
  if ($("#reject" + singleRejectId.val()))
    $("#reject" + singleRejectId.val()).removeAttr("checked");
}

function validateAuthentication(id, passwordField, reasonField) {
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
  var reason = null;
  if (reasonField != null) {
    action = 2;
    reason = reasonField.val().trim();
    if (reason.length == 0) {
      displayMessage(message.reason_required);
      reasonField.focus();
      return false;
    } else if (validateMaxLength('reason', reason, "Reason") == false) {
      return false;
    }
  }
  displayLoader();
  bu.validateAssignStatutory(parseInt(id), function(error, res1) {
    hideLoader();
    Custombox.close();
    if (res1.rej_count == 0) {
      approveOrRejectAction(id, cl_id, le_id, action, reason, password);
    } else {
      var statusmsg = message.manuval_rejected_confirm;
      confirm_alert(statusmsg, function(isConfirm) {
        if (isConfirm) {
          approveOrRejectAction(id, cl_id, le_id, action, reason, password);
        }
      });
    }
  });
}

approveOrRejectAction = function(id, cl_id, le_id, action, reason, password) {
  bu.assignStatutoryActionInList(parseInt(cl_id), parseInt(le_id), parseInt(id),
    parseInt(action), reason, password, function(err1, res2) {
      console.log(err1, res2);
      if (err1 == null) {
        if (res2.hasOwnProperty("rej_count")) {
          var statusmsg = res2.rej_count+' '+message.sys_rejected_confirm;
          confirm_alert(statusmsg, function(isConfirm) {
            if (isConfirm) {
              alert("Status change");
              bu.confirmAssignStatutoryUpdateAction(parseInt(id), parseInt(cl_id), 
                parseInt(le_id), function(error, res3) {
                  if (error == null) {
                    if (action == 1)
                      displaySuccessMessage(message.assign_statutory_approved_success);
                    else
                      displaySuccessMessage(message.assign_statutory_rejected_success);
                    REPORT.fetchStatutoryValues(clientGroupId.val(), legalEntityId.val());
                  } else {
                    REPORT.failuresMessage(error);
                    hideLoader();
                  }
              });
            }
          });
        } else {
          if (action == 1)
            displaySuccessMessage(message.assign_statutory_approved_success);
          else
            displaySuccessMessage(message.assign_statutory_rejected_success);
          REPORT.fetchStatutoryValues(clientGroupId.val(), legalEntityId.val());
        }
      } else {
        REPORT.failuresMessage(err1);
        hideLoader();
      }
    });
}

/*//open password dialog
function showModalDialog(domainId, isActive){
    t_this = this;
    var passStatus = null;
    if (isActive == true) {
        passStatus = false;
        statusmsg = message.deactive_message;
    } else {
        passStatus = true;
        statusmsg = message.active_message;
    }
    confirm_alert(statusmsg, function(isConfirm) {
    if(isConfirm) {
        Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete:   function() {
          isAuthenticate = false;
        },
        close:   function() {
          if(isAuthenticate) {
            t_this.changeStatus(domainId, passStatus);
          }
        },
      });
    }
  });
}*/

goToDetailsPage = function(id) {
  filteredData.empty();
  clearFiltered.hide();
  $(".all-data").trigger('click');
  domain.find("option").remove();
  domain.multiselect('destroy');
  unit.find("option").remove();
  unit.multiselect('destroy');
  primaryLegislation.find("option").remove();
  primaryLegislation.multiselect('destroy');
  secondaryLegislationName.val("");
  statutoryProvisionName.val("");
  complianceTaskName.val("");
  statutoryStatus.val("");
  complianceStatus.val("");
  complianceDescriptionName.val("");
  sno = 0;
  currentPage = 1;
  viewListDetailsPage(id);
}


viewListDetailsPage = function(id) {
  console.log(id);
  listPage.hide();
  dataListPage.show();
  filterDomain.val('');
  filterUnit.val('');
  filterPrimaryLegislation.val('');
  filterSecondaryLegislation.val('');
  filterStatutoryProvision.val('');
  filterComplianceTask.val('');
  filterComplianceDescription.val('');
  pageLimits = parseInt(ItemsPerPage.val());
  if (currentPage == 1)
    sno = 0;
  else
    sno = (currentPage - 1) * pageLimits;
  REPORT.loadFilterPage(id);
  var view_data = $(".view-data:checked").val();
  REPORT.loadDetailsPageWithFilter(id, view_data, domain.val(), unit.val(),
    primaryLegislation.val(), secondaryLegislationName.val(),
    statutoryProvisionName.val(), complianceTaskName.val(),
    statutoryStatus.val(), complianceStatus.val(),
    complianceDescriptionName.val());
}

ApproveAssignStatutoryBulkUpload.prototype.displayDetailsPage = function(data, pageFlag) {
  if (pageFlag == false)
    var showFrom = sno + 1;
  dataDetailsTableTbody.empty();
  if (data.length > 0) {
    $.each(data, function(k, v) {
      if (pageFlag == false)
        sno = parseInt(sno) + 1;
      var clone = $('#template #report-details-table tr').clone();
      $('.sno', clone).text(sno);
      $('.single-approve', clone).val(v.as_id).attr({
        id: "approve" + v.as_id,
        onClick: "singleApprove(" + v.as_id + ")",
        name: "action" + v.as_id
      });
      $('.single-reject', clone).val(v.as_id).attr({
        id: "reject" + v.as_id,
        onClick: "singleReject(" + v.as_id + ", false)",
        name: "action" + v.as_id
      });
      $('.rejected-reason', clone).attr("id", "rejected-reason" + v.as_id);
      if (v.bu_action == 1) {
        $('.single-approve', clone).prop('checked', true);
        $('.single-reject', clone).prop('checked', false);
      } else if (v.bu_action == 2) {
        $('.single-reject', clone).prop('checked', true);
        $('.single-approve', clone).prop('checked', false);
        if (v.remarks != "") {
          $('.rejected-reason', clone)
            .html('<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" ' +
              'data-toggle="tooltip" data-original-title="' + v.remarks + '"></i>');
        }
      } else {
        $('.single-approve', clone).prop('checked', false);
        $('.single-reject', clone).prop('checked', false);
      }
      $('.domain-name', clone).html(v.d_name);
      $('.unit-name span', clone).html(v.u_name);
      $('.unit-name i', clone).attr("title", "Location: " + v.u_location);
      $('.primary-legislation', clone).html(v.p_leg);

      if (v.c_status == 1) {
        $('.compliance-applicable i', clone).addClass("text-info");
        $('.compliance-not-applicable i', clone).addClass("text-muted");
        $('.compliance-do-not-show i', clone).addClass("text-muted");
      } else if (v.c_status == 2) {
        $('.compliance-applicable i', clone).addClass("text-muted");
        $('.compliance-not-applicable i', clone).addClass("text-warning");
        $('.compliance-do-not-show i', clone).addClass("text-muted");
      } else if (v.c_status == 3) {
        $('.compliance-applicable i', clone).addClass("text-muted");
        $('.compliance-not-applicable i', clone).addClass("text-muted");
        $('.compliance-do-not-show i', clone).addClass("text-danger");
      } else {
        $('.compliance-applicable i', clone).addClass("text-muted");
        $('.compliance-not-applicable i', clone).addClass("text-muted");
        $('.compliance-do-not-show i', clone).addClass("text-muted");
      }

      if (v.s_status == 1) {
        $('.statutory-applicable i', clone).addClass("text-info");
        $('.statutory-not-applicable i', clone).addClass("text-muted");
        $('.statutory-do-not-show i', clone).addClass("text-muted");
      } else if (v.s_status == 2) {
        $('.statutory-applicable i', clone).addClass("text-muted");
        $('.statutory-not-applicable i', clone).addClass("text-warning");
        $('.statutory-do-not-show i', clone).addClass("text-muted");
      } else if (v.s_status == 3) {
        $('.statutory-applicable i', clone).addClass("text-muted");
        $('.statutory-not-applicable i', clone).addClass("text-muted");
        $('.statutory-do-not-show i', clone).addClass("text-danger");
      } else {
        $('.statutory-applicable i', clone).addClass("text-muted");
        $('.statutory-not-applicable i', clone).addClass("text-muted");
        $('.statutory-do-not-show i', clone).addClass("text-muted");
      }
      if (v.s_remarks != "") {
        $('.statutory-remarks', clone).html(v.s_remarks);
      }
      $('.secondary-legislation', clone).html(v.s_leg);
      $('.statutory-provision', clone).html(v.s_prov);
      $('.compliance-task-name span', clone).html(v.c_task);
      $('.compliance-task-name i', clone)
        .attr("title", "Organization: " + v.org_names.join());
      $('.compliance-description', clone).html(v.c_desc);
      dataDetailsTableTbody.append(clone);
    });
    checkAllEnableDisable();
    PaginationView.show();
    if (pageFlag == false)
      showPagePan(showFrom, sno, totalRecord);
  } else {
    PaginationView.hide();
    hideLoader();
    var clone = $('#template #record-not-found tr').clone();
    dataDetailsTableTbody.append(clone);
    hidePagePan();
  }
};

singleApprove = function(id) {
  if ($('#approve' + id).prop("checked") == true) {
    $('#reject' + id).removeAttr("checked");
    $('#rejected-reason' + id + ' i').remove();
    tempAction(id, 1);
    checkAllEnableDisable();
  } else {
    checkAllEnableDisable();
  }
}

singleReject = function(id, flag) {
  if ($('#reject' + id).prop("checked") == true) {
    if (checkAllReject.prop("checked") == false) {
      if (flag == false) {
        singleRejectId.val(id);
        confirmationAction(0, 'single-reject');
      } else {
        $('#approve' + id).removeAttr("checked");
        $('#rejected-reason' + id).html('<i class="fa fa-info-circle ' +
          ' fa-1-2x l-h-51 text-primary c-pointer" data-toggle="tooltip" ' +
          ' data-original-title="' + singleRejectReason.val() + '"></i>');
        tempAction(id, 2);
        checkAllEnableDisable();
      }
    } else {
      $('#approve' + id).removeAttr("checked");
      $('#rejected-reason' + id).html('<i class="fa fa-info-circle ' +
        ' fa-1-2x l-h-51 text-primary c-pointer" data-toggle="tooltip" ' +
        ' data-original-title="' + singleRejectReason.val() + '"></i>');
      tempAction(id, 2);
      // checkAllEnableDisable();
      checkAllApprove.removeAttr("checked");
    }
  } else {
    checkAllEnableDisable();
    $('#rejected-reason' + id + ' i').remove();
  }
}

tempAction = function(id, action) {
  console.log(id);
  var csvid = ASID.val();
  var reason = singleRejectReason.val();
  displayLoader();
  bu.updateAssignStatutoryActionFromView(parseInt(csvid), parseInt(id),
    parseInt(action), reason,
    function(error, response) {
      if (error == null) {
        hideLoader();
      } else {
        REPORT.failuresMessage(error);
        hideLoader();
      }
    });
}

checkAllEnableDisable = function(id, action) {
  var approveTotalCount = dataDetailsTableTbody.find('.single-approve').length;
  var rejectTotalCount = dataDetailsTableTbody.find('.single-reject').length;
  var approveCount = dataDetailsTableTbody.find('.single-approve:checked').length;
  var rejectCount = dataDetailsTableTbody.find('.single-reject:checked').length;
  // alert(rejectTotalCount+' - '+rejectCount);
  if (approveCount == approveTotalCount) {
    checkAllApprove.prop('checked', true);
    checkAllReject.removeAttr("checked");
  } else if (rejectCount == rejectTotalCount) {
    checkAllApprove.removeAttr("checked");
    checkAllReject.prop('checked', true);
  } else {
    checkAllApprove.removeAttr("checked");
    checkAllReject.removeAttr("checked");
  }
}

ApproveAssignStatutoryBulkUpload.prototype.loadFilterPage = function(id) {
  t_this = this;
  displayLoader();
  bu.getAssignStatutoryFilters(parseInt(id), function(error, response) {
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
      t_this.failuresMessage(error);
      hideLoader();
    }
  });
};

ApproveAssignStatutoryBulkUpload.prototype.displayFilterList = function() {
  t_this = this;

  if (t_this._filter_domain.length > 0 && domain.val() == null) {
    domain.find("option").remove();
    $.each(t_this._filter_domain, function(k, v) {
      domain.append('<option value="' + v + '">' + v + '</option>');
    });
    domain.multiselect();
  }

  if (t_this._filter_unit.length > 0 && unit.val() == null) {
    unit.find("option").remove();
    $.each(t_this._filter_unit, function(k, v) {
      unit.append('<option value="' + v.split("-")[0].trim() + '">' + v + '</option>');
    });
    unit.multiselect();
  }

  if (t_this._filter_primary_legislation.length > 0 &&
    primaryLegislation.val() == null) {
    primaryLegislation.find("option").remove();
    $.each(t_this._filter_primary_legislation, function(k, v) {
      primaryLegislation.append('<option value="' + v + '">' + v + '</option>');
    });
    primaryLegislation.multiselect();
  }

  if (t_this._filter_statutory_status.length > 0 && statutoryStatus.val() == "") {
    $.each(t_this._filter_statutory_status, function(k, v) {
      statutoryStatus.append('<option value="' + v + '">' + v + '</option>');
    });
    statutoryStatus.multiselect();
  }

  if (t_this._filter_compliance_status.length > 0 &&
    complianceStatus.val() == "") {
    $.each(t_this._filter_compliance_status, function(k, v) {
      complianceStatus.append('<option value="' + v + '">' + v + '</option>');
    });
    complianceStatus.multiselect();
  }

};

ApproveAssignStatutoryBulkUpload.prototype.loadDetailsPageWithFilter = function(
  id, v_data, d_names, u_names, p_leg, s_leg,
  s_pro, c_task, s_status, c_status, c_des) {
  t_this = this;
  if (d_names != null) { d_names = d_names.join(); }
  if (u_names != null) { u_names = u_names.join(); }
  if (p_leg != null) { p_leg = p_leg.join(); }
  if (s_leg == "") { s_leg = null; }
  if (s_pro == "") { s_pro = null; }
  if (c_task == "") { c_task = null; }
  if (c_des == "") { c_des = null; }
  if (s_status == "") { s_status = null; } else { s_status = parseInt(s_status); }
  if (c_status == "") { c_status = null; } else { c_status = parseInt(c_status); }
  if (v_data == "") { v_data = null; } else { v_data = parseInt(v_data); }
  displayLoader();
  bu.getViewAssignStatutoryDataFromFilter(parseInt(id), parseInt(sno),
    parseInt(pageLimits), d_names, u_names, p_leg, s_leg, s_pro, c_task,
    c_des, v_data, s_status, c_status,
    function(error, response) {
      clientGroupName.html(response.cl_name);
      legalEntityName.html(response.le_name);
      uploadedFileName.html(response.csv_name);
      uploadedOn.html(response.uploaded_on);
      for (var j = 0; j < t_this._UserList.length; j++) {
        if (response.uploaded_by == t_this._UserList[j].user_id) {
          uploadedBy.html(t_this._UserList[j].emp_code_name);
        }
      }
      if (error == null) {
        t_this._data_list_details = response.assign_statutory_data_list;
        // totalRecord = 32;
        totalRecord = response.count;
        // alert(response.count);
        if (sno == 0)
          createPageView(totalRecord);
        t_this.displayDetailsPage(t_this._data_list_details, false);
        ASID.val(id);
        hideLoader();
      } else {
        t_this.failuresMessage(error);
        hideLoader();
      }
    });
};

function showPagePan(showFrom, showTo, total) {
  var showText = 'Showing ' + showFrom + ' to ' +
    showTo + ' of ' + total + ' entries ';
  showCount.text(showText);
  PaginationView.show();
};

function hidePagePan() {
  showCount.text('');
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
  bu.validateAssignStatutory(parseInt(csvid), function(error, response) {
    if (response.un_saved_count > 0) {
      displayMessage(message.un_saved_compliance);
      hideLoader();
    } else {

      bu.submitAssignStatutoryAction(parseInt(csvid), 1, 1, "pass@123",
        function(error, response) {
          if (error == null) {
            if (response.hasOwnProperty("rej_count")) {
              var statusmsg = response.rej_count+' '+message.sys_rejected_confirm;
              confirm_alert(statusmsg, function(isConfirm) {
                if (isConfirm) {
                  bu.confirmAssignStatutoryUpdateAction(parseInt(csvid), parseInt(cl_id), 
                    parseInt(le_id), function(error, res3) {
                      if (error == null) {
                        displaySuccessMessage(message.assign_statutory_submit_success);
                        // REPORT.fetchStatutoryValues(clientGroupId.val(), legalEntityId.val());
                        REPORT.pageLoad();
                      } else {
                        REPORT.failuresMessage(error);
                        hideLoader();
                      }
                  });
                }
              });
            } else {
              displaySuccessMessage(message.assign_statutory_submit_success);
              REPORT.pageLoad();
            }
          } else {
            t_this.failuresMessage(error);
            hideLoader();
          }
        });

    }
  });
}

REPORT = new ApproveAssignStatutoryBulkUpload();

$(document).ready(function() {
  REPORT.pageLoad();
  PageControls();
  loadItemsPerPage();
  // goToDetailsPage(38);
  // listView.show();
  // REPORT.fetchStatutoryValues(1,1);

  $(".nicescroll").niceScroll();
});