var categoryList;
var uglist;
function clearMessage() {
  $('.error-message').hide();
  $('.error-message').text('');
}
function displayMessage(message) {
  $('.error-message').text(message);
  $('.error-message').show();
}
$('#btnUserGroupCancel').click(function () {
  $('#userGroupAdd').hide();
  $('#userGroupView').show();
  $('#groupNameSearch').val('');
  $('#categoryNameSearch').val('');
  loadUserGroupdata(uglist);
});
$('#btnUserGroupAdd').click(function () {
  $('#userGroupView').hide();
  $('#userGroupAdd').show();
  $('#formList').hide();
  clearMessage();
  $('#groupName').val('');
  $('#groupId').val('');
  $('#categoryName').val('');
  $('#categoryName option:gt(0)').remove();
  $('.checkbox-full-check').prop('checked', false);
  loadFormCategories();
});
function loadFormCategories() {
  var categoryName = $('#categoryName');
  $.each(categoryList, function (key, value) {
    categoryName.append($('<option></option>').val(categoryList[key].form_category_id).html(categoryList[key].form_category));
  });
}
//get user group master details from api
function initialize() {
  clearMessage();
  $('.checkbox-full-check').prop('checked', false);
  $('.js-filter').val('');
  function onSuccess(data) {
    categoryList = data.form_categories;
    uglist = data.user_group_details;
    loadUserGroupdata(uglist);
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getAdminUserGroupList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//load user group details
function loadUserGroupdata(userGroupList) {
  $('.tbody-usergroups-list').find('tr').remove();
  var sno = 0;
  $.each(userGroupList, function (key, value) {
    var catgid = value.user_category_id;
    var userGroupName = value.user_group_name;
    var isActive = value.is_active;
    var userGroupId = value.user_group_id;
    var passStatus = null;
    var classValue = null;
    if (isActive == true) {
      passStatus = false;
      classValue = 'active-icon';
    } else {
      passStatus = true;
      classValue = 'inactive-icon';
    }
    function getCategoryName(catgId) {
      var catgname;
      $.each(categoryList, function (key, value) {
        if (categoryList[key].form_category_id == catgId) {
          catgname = categoryList[key].form_category;
          return false;
        }
      });
      return catgname;
    }
    var tableRow = $('#templates .table-usergroup-list .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.group-name', clone).text(userGroupName);
    $('.catg-name', clone).text(getCategoryName(catgid));
    $('.edit-icon').attr('title', 'Edit');
    $('.edit-icon', clone).on('click', function () {
      userGroupEdit(userGroupId, userGroupName, catgid);
    });
    $('.status', clone).addClass(classValue);
    $('.active-icon').attr('title', 'Deactivate');
    $('.inactive-icon').attr('title', 'Activate');
    $('.status', clone).on('click', function () {
      userGroupActive(userGroupId, userGroupName, passStatus);
    });
    $('.tbody-usergroups-list').append(clone);
  });
}
$('#categoryName').on('change', function () {
  // 	$("#btnUserGroupShow").trigger("click");
  // });
  // $("#btnUserGroupShow").click(function(){
  clearMessage();
  $('.checkbox-full-check').prop('checked', false);
  var groupNameVal = $('#groupName').val().trim();
  var categoryNameVal = $('#categoryName').val().trim();
  clearMessage();
  $('#formList').show();
  // $("#tempcatgid").val(categoryNameVal);
  function onSuccess(data) {
    loadFormList(data.forms, categoryNameVal);
  }
  function onFailure(error) {
    if (error == 'GroupNameAlreadyExists') {
      displayMessage(message.groupname_exists);
    } else {
      displayMessage(error);
    }
  }
  mirror.getAdminUserGroupList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
});
function loadFormList(formList, categoryNameVal) {
  clearMessage();
  $('.tableFormList').find('tr').remove();
  $('.checkedFormId').prop('checked', false);
  var i_incre;
  var list = formList[categoryNameVal].menus;
  $.each(list, function (key, value) {
    if (jQuery.isEmptyObject(key) == false) {
      var tableRowList = $('#templates-form-heading .table-form-heading .table-row-form-heading');
      var clone1 = tableRowList.clone();
      $('.formHeading', clone1).text(key);
      $('.tableFormList').append(clone1);
      $.each(value, function (i) {
        var formName = value[i].form_name;
        var formId = value[i].form_id;
        var tableRowForms = $('#templates-form-list .table-form-list .table-row-form');
        var clone2 = tableRowForms.clone();
        $('.checkbox-val', clone2).html('<input type="checkbox" class="checkedFormId" value="' + value[i].form_id + '">');
        $('.form-name', clone2).html(formName);
        $('.tableFormList').append(clone2);
      });
    }
  });
}
function loadFormListUpdate(formList, userGroupList, catgid, userGroupId) {
  $('.tableFormList').find('tr').remove();
  $('.checkedFormId').prop('checked', false);
  clearMessage();
  var i_incre;
  var list = formList[catgid].menus;
  $.each(list, function (key, value) {
    if (jQuery.isEmptyObject(key) == false) {
      var tableRowList = $('#templates-form-heading .table-form-heading .table-row-form-heading');
      var clone1 = tableRowList.clone();
      $('.formHeading', clone1).text(key);
      $('.tableFormList').append(clone1);
      $.each(value, function (i) {
        var formName = value[i].form_name;
        var formId = value[i].form_id;
        var tableRowForms = $('#templates-form-list .table-form-list .table-row-form');
        var clone2 = tableRowForms.clone();
        $('.checkbox-val', clone2).html('<input type="checkbox" class="checkedFormId" value="' + value[i].form_id + '">');
        $('.form-name', clone2).text(formName);
        $('.tableFormList').append(clone2);
      });
    }
  });
  for (var userGroupDetails in userGroupList) {
    if (userGroupList[userGroupDetails].user_group_id == userGroupId) {
      var formIds = userGroupList[userGroupDetails].form_ids;
      for (var i = 0; i < formIds.length; i++) {
        $('.checkedFormId[value = "' + formIds[i] + '"]').prop('checked', true);
      }
    }
  }
}
$('#btnUserGroupSubmit').click(function () {
  var groupIdVal = $('#groupId').val();
  var groupNameVal = $('#groupName').val().trim();
  var categoryNameVal = $('#categoryName').val().trim();
  // var tempcategoryidVal = $("#tempcatgid").val().trim();
  var chkArray = [];
  var chkArrayInt = [];
  var checkLength = userGroupValidate();
  if (checkLength) {
    if (groupNameVal == '') {
      displayMessage(message.group_required);
    } else if (categoryNameVal == '') {
      displayMessage(message.catgname_required);
    } else if (categoryNameVal.length > 50) {
      displayMessage(message.category_max50);
    }  // else if(tempcategoryidVal != categoryNameVal){
       // 	displayMessage(message.category_invalid);
       // }
    else if (groupIdVal == '') {
      $('.checkedFormId:checked').each(function () {
        chkArray.push($(this).val());
      });
      if (chkArray.length == 0) {
        displayMessage(message.add_one_form);
      } else {
        clearMessage();
        chkArrayInt = chkArray.map(function (item) {
          return parseInt(item, 10);
        });
        function onSuccess(response) {
          $('#userGroupAdd').hide();
          $('#userGroupView').show();
          initialize();
        }
        function onFailure(error) {
          if (error == 'GroupNameAlreadyExists') {
            displayMessage(message.groupname_exists);
          } else {
            displayMessage(error);
          }
        }
        var userGroupInsertDetails = mirror.getSaveAdminUserGroupDict(groupNameVal, parseInt(categoryNameVal), chkArrayInt);
        mirror.saveAdminUserGroup(userGroupInsertDetails, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      }
    } else if (groupIdVal != '') {
      clearMessage();
      $('.checkedFormId:checked').each(function () {
        chkArray.push($(this).val());
      });
      if (chkArray.length == 0) {
        displayMessage(message.add_one_form);
      } else {
        // $(".checkedFormId:checked").each(function() {
        // 	chkArray.push($(this).val());
        // });
        // /* join array separated by comma*/
        chkArrayInt = chkArray.map(function (item) {
          return parseInt(item, 10);
        });
        function onSuccess(status) {
          $('#userGroupAdd').hide();
          $('#userGroupView').show();
          initialize();
        }
        function onFailure(error) {
          if (error == 'GroupNameAlreadyExists') {
            displayMessage(message.groupname_exists);
          } else {
            displayMessage(error);
          }
        }
        var userGroupInsertDetails = mirror.getUpdateAdminUserGroupDict(parseInt(groupIdVal), groupNameVal, parseInt(categoryNameVal), chkArrayInt);
        mirror.updateAdminUserGroup(userGroupInsertDetails, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      }
    }
  }
});
function userGroupEdit(userGroupId, userGroupName, catgid) {
  clearMessage();
  $('#userGroupAdd').show();
  $('#userGroupView').hide();
  $('#groupId').val(userGroupId);
  $('#groupName').val(userGroupName);
  $('#categoryName').val('');
  $('#categoryName option:gt(0)').remove();
  loadFormCategories();
  $('#categoryName option[value = ' + catgid + ']').attr('selected', 'selected');
  //$("#tempcatgid").val(catgid);
  function onSuccess(data) {
    loadFormListUpdate(data.forms, data.user_group_details, catgid, userGroupId);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getAdminUserGroupList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
function userGroupActive(userGroupId, userGroupName, isActive) {
  $('#userGroupId').val(userGroupId);
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(response) {
          initialize();
        }
        function onFailure(error) {
          if (error == 'CannotDeactivateUserExists') {
            custom_alert(message.cannot_deactivate_usergroup);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeAdminUserGroupStatus(userGroupId, userGroupName, isActive, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
}
$('.checkbox-full-check').click(function (event) {
  if (this.checked) {
    $('.checkedFormId').each(function () {
      this.checked = true;
    });
  } else {
    $('.checkedFormId').each(function () {
      this.checked = false;
    });
  }
});
$(function () {
  initialize();
});
$(document).find('.js-filtertable').each(function () {
  $(this).filtertable().addFilter('.js-filter');
});
$('#groupName').on('input', function (e) {
  this.value = isCommon($(this));
});