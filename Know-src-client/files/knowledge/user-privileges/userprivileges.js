var categoryList;
var uglist;
var CurrentPassword = $('#current-password');
var PasswordSubmitButton = $('#password-submit');

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterGroupname = $('#groupNameSearch');
var FilterCategorname = $('#categoryNameSearch');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

function displayLoader() {
    $('.loading-indicator-spin').show();
}

function hideLoader() {
    $('.loading-indicator-spin').hide();
}

$('#btnUserGroupCancel').click(function() {
    $('#userGroupAdd').hide();
    $('#userGroupView').show();
    $('#groupNameSearch').val('');
    $('#categoryNameSearch').val('');
    loadUserGroupdata(uglist);
});
$('#btnUserGroupAdd').click(function() {
    $('#userGroupView').hide();
    $('#userGroupAdd').show();
    $('#formList').hide();
    clearMessage();
    $('#groupName').val('');
    $('#groupId').val('');
    $('#categoryName').val('');
    $('#categoryName option:gt(0)').remove();
    $('.checkbox-full-check').prop('checked', false);
    $('#groupName').focus();
    loadFormCategories();
});

function loadFormCategories() {
    var categoryName = $('#categoryName');
    $.each(categoryList, function(key, value) {
        categoryName.append($('<option></option>').val(categoryList[key].form_category_id).html(categoryList[key].form_category));
    });
}
//get user group master details from api
function initialize() {
    clearMessage();
    $('#userGroupView').show();
    $('#userGroupAdd').hide();
    $('#formList').hide();
    $('.checkbox-full-check').prop('checked', false);
    $('.filter-text-box').val('');

    function onSuccess(data) {
        categoryList = data.form_categories;
        uglist = data.user_group_details;
        loadUserGroupdata(uglist);
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getAdminUserGroupList(function(error, response) {
        if (error == null) {
            hideLoader();
            onSuccess(response);
        } else {
            hideLoader();
            onFailure(error);
        }
    });
}

function processGroupSearch() {
    g_name = FilterGroupname.val().toLowerCase();
    c_g_name = FilterCategorname.val().toLowerCase();

    user_status = $('.search-status-li.active').attr('value');
    searchList = []

    for (var i in uglist) {
        data = uglist[i];

        data_g_name = data.user_group_name.toLowerCase();
        data_c_g_name = getCategoryName(data.user_category_id);
        data_c_g_name = data_c_g_name.toLowerCase();
        data_is_active = data.is_active;

        if ((~data_g_name.indexOf(g_name)) && (~data_c_g_name.indexOf(c_g_name))) {
            if ((user_status == 'all' || Boolean(parseInt(user_status)) == data_is_active)) {
                searchList.push(data);
            }
        }
    }
    loadUserGroupdata(searchList);
}

function getCategoryName(catgId) {
    var catgname;
    $.each(categoryList, function(key, value) {
        if (categoryList[key].form_category_id == catgId) {
            catgname = categoryList[key].form_category;
            return false;
        }
    });
    return catgname;
}

//load user group details
function loadUserGroupdata(userGroupList) {
    $('.tbody-usergroups-list').find('tr').remove();
    var sno = 0;
    if (userGroupList.length == 0) {
        $('.tbody-usergroups-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-usergroups-list').append(clone4);
    }
    $.each(userGroupList, function(key, value) {
        var catgid = value.user_category_id;
        var userGroupName = value.user_group_name;
        var isActive = value.is_active;
        var userGroupId = value.user_group_id;
        var passStatus = null;
        var classValue = null;


        var tableRow = $('#templates .table-usergroup-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.group-name', clone).text(userGroupName);
        $('.catg-name', clone).text(getCategoryName(catgid));

        //edit icon
        $('.edit').attr('title', 'Click Here to Edit');
        $('.edit', clone).addClass('fa-pencil text-primary');
        // $('.edit', clone).on('click', function() {
        //     userGroupEdit(userGroupId, userGroupName, catgid);
        // });
        $('.edit', clone).attr("onClick", "userGroupEdit(" + userGroupId + ", '" + userGroupName + "', " + catgid + ")");

        if (isActive == true) {
            $('.status').attr('title', 'Click Here to Deactivate');
            $('.status', clone).removeClass('fa-times text-danger');
            $('.status', clone).addClass('fa-check text-success');
        } else {
            $('.status').attr('title', 'Click Here to Activate');
            $('.status', clone).removeClass('fa-check text-success');
            $('.status', clone).addClass('fa-times text-danger');
        }

        // $('.status', clone).on('click', function(e) {
        //     showModalDialog(e, userGroupId, userGroupName, isActive);
        // });
        $('.status', clone).attr("onClick", "showModalDialog(" + userGroupId + ", '" + userGroupName + "', " + isActive + ")");

        $('.status').hover(function() {
            showTitle(this);
        });

        $('.tbody-usergroups-list').append(clone);
    });
}
$('#categoryName').on('change', function() {
    clearMessage();
    if ($('#categoryName').val().trim() > 0) {
        $('.checkbox-full-check').prop('checked', false);
        var groupNameVal = $('#groupName').val().trim();
        var categoryNameVal = $('#categoryName').val().trim();
        clearMessage();
        $('#formList').show();
        getFormsList(categoryNameVal)
    } else {
        clearMessage();
        $('#formList').hide();
    }
    // $("#tempcatgid").val(categoryNameVal);
});

//load form list
function getFormsList(categoryNameVal) {
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
    displayLoader();
    mirror.getAdminUserGroupList(function(error, response) {
        if (error == null) {
            hideLoader();
            onSuccess(response);
        } else {
            hideLoader();
            onFailure(error);
        }
    });
}

//Status Title
function showTitle(e) {
    if (e.className == "fa c-pointer status fa-times text-danger") {
        e.title = 'Click Here to Activate';
    } else if (e.className == "fa c-pointer status fa-check text-success") {
        e.title = 'Click Here to Deactivate';
    }
}

//open password dialog
function showModalDialog(userGroupId, userGroupName, isActive) {
    var passStatus = null;
    if (isActive == true) {
        passStatus = false;
        statusmsg = message.deactive_message;
    } else {
        passStatus = true;
        statusmsg = message.active_message;
    }
    CurrentPassword.val('');
    confirm_alert(statusmsg, function(isConfirm) {
        if (isConfirm) {
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete: function() {
                    CurrentPassword.focus();
                    isAuthenticate = false;
                },
                close: function() {
                    if (isAuthenticate) {
                        userGroupActive(userGroupId, userGroupName, passStatus);
                    }
                },
            });
            // e.preventDefault();
        }
    });
}

//validate password
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } else {
        if (validateMaxLength('password', password, "Password") == false) {
            return false;
        }
    }
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        } else {
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}

//length validation
function validateMaxLength(key_name, value, show_name) {
    e_n_msg = validateLength(key_name, value.trim())
    if (e_n_msg != true) {
        displayMessage(show_name + e_n_msg);
        return false;
    }
    return true;
}

function loadFormList(formList, categoryNameVal) {
    clearMessage();
    $('.tableFormList').find('tr').remove();
    $('.checkedFormId').prop('checked', false);
    var i_incre;
    var list = formList[categoryNameVal].menus;
    $.each(list, function(key, value) {
        if (jQuery.isEmptyObject(key) == false) {
            var tableRowList = $('#templates-form-heading .table-form-heading .table-row-form-heading');
            var clone1 = tableRowList.clone();
            $('.formHeading', clone1).text(key);
            $('.tableFormList').append(clone1);
            $.each(value, function(i) {
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
    $('#templates-form-list').show();
    $('#formList').show();
    $('.checkedFormId').prop('checked', false);
    clearMessage();
    var i_incre;
    var list = formList[catgid].menus;
    $.each(list, function(key, value) {
        if (jQuery.isEmptyObject(key) == false) {
            var tableRowList = $('#templates-form-heading .table-form-heading .table-row-form-heading');

            var clone1 = tableRowList.clone();
            $('.formHeading', clone1).text(key);
            $('.tableFormList').append(clone1);
            $.each(value, function(i) {
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
$('#btnUserGroupSubmit').click(function() {
    var groupIdVal = $('#groupId').val();
    var groupNameVal = $('#groupName').val().trim();
    var categoryNameVal = $('#categoryName').val().trim();
    var chkArray = [];
    var chkArrayInt = [];

    if (groupNameVal.length == 0) {
        displayMessage(message.usergroup_required);
        $('#groupName').focus();
        return false;
    } else {

        if (!validateMaxLength('usergroupname', groupNameVal, "User Group Name")) {
            return false;
        }
    }

    if (categoryNameVal == 0) {
        displayMessage(message.catgname_required);
        $('#categoryName').focus();
        return false;
    }

    if (groupIdVal == '') {
        $('.checkedFormId:checked').each(function() {
            chkArray.push($(this).val());
        });
        if (chkArray.length == 0) {
            displayMessage(message.add_one_form);
        } else {
            clearMessage();
            chkArrayInt = chkArray.map(function(item) {
                return parseInt(item, 10);
            });

            function onSuccess(response) {
                $('#userGroupAdd').hide();
                $('#userGroupView').show();
                displaySuccessMessage(message.user_group_save_success);
                initialize();
            }

            function onFailure(error) {
                if (error == 'GroupNameAlreadyExists') {
                    displayMessage(message.groupname_exists);
                } else if (error == 'CannotDeactivateUserExists') {
                    displayMessage(message.cannot_deactivate_usergroup);
                } else {
                    displayMessage(error);
                }
            }
            var userGroupInsertDetails = mirror.getSaveAdminUserGroupDict(groupNameVal, parseInt(categoryNameVal), chkArrayInt);
            displayLoader();
            mirror.saveAdminUserGroup(userGroupInsertDetails, function(error, response) {
                if (error == null) {
                    hideLoader();
                    onSuccess(response);
                } else {
                    hideLoader();
                    onFailure(error);
                }
            });
        }
    } else if (groupIdVal != '') {
        clearMessage();
        $('.checkedFormId:checked').each(function() {
            chkArray.push($(this).val());
        });
        if (chkArray.length == 0) {
            displayMessage(message.add_one_form);
        } else {
            chkArrayInt = chkArray.map(function(item) {
                return parseInt(item, 10);
            });

            function onSuccess(status) {
                $('#userGroupAdd').hide();
                $('#userGroupView').show();
                displaySuccessMessage(message.user_group_edit_success);
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
            displayLoader();
            mirror.updateAdminUserGroup(userGroupInsertDetails, function(error, response) {
                if (error == null) {
                    hideLoader();
                    onSuccess(response);
                } else {
                    hideLoader();
                    onFailure(error);
                }
            });
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
    displayLoader();
    mirror.getAdminUserGroupList(function(error, response) {
        if (error == null) {
            hideLoader();
            onSuccess(response);
        } else {
            hideLoader();
            onFailure(error);
        }
    });
}

function userGroupActive(userGroupId, userGroupName, isActive) {
    $('#userGroupId').val(userGroupId);

    function onSuccess(data) {
        initialize();
    }

    function onFailure(error) {
        if (error == 'CannotDeactivateUserExists') {
            displayMessage(message.cannot_deactivate_usergroup);
        } else {
            displayMessage(error);
        }
    }
    displayLoader();
    mirror.changeAdminUserGroupStatus(userGroupId, userGroupName, isActive, function(error, response) {
        if (error == null) {
            hideLoader();
            if (isActive) {
                displaySuccessMessage(message.record_active);
            } else {
                displaySuccessMessage(message.record_deactive);
            }
            onSuccess(response);
        } else {
            hideLoader();
            onFailure(error);
        }
    });
}
$('.checkbox-full-check').click(function(event) {
    if (this.checked) {
        $('.checkedFormId').each(function() {
            this.checked = true;
        });
    } else {
        $('.checkedFormId').each(function() {
            this.checked = false;
        });
    }
});

function renderControls() {
    //status of the list
    Search_status_ul.click(function(event) {
        Search_status_li.each(function(index, el) {
            $(el).removeClass('active');
        });
        $(event.target).parent().addClass('active');

        var currentClass = $(event.target).find('i').attr('class');
        Search_status.removeClass();
        if (currentClass != undefined) {
            Search_status.addClass(currentClass);
            Search_status.text('');
        } else {
            Search_status.addClass('fa');
            Search_status.text('All');
        }
        processGroupSearch();
    });
}
$(function() {
    renderControls();
    initialize();
});
/*$(document).find('.js-filtertable').each(function () {
  $(this).filtertable().addFilter('.js-filter');
});*/
FilterBox.keyup(function() {
    processGroupSearch();
});
$('#groupName').on('input', function(e) {
    //this.value = isCommon($(this));
    isCommon(this);
});
PasswordSubmitButton.click(function() {
    validateAuthentication();
});
Search_status.change(function() {
    processGroupSearch();
});
