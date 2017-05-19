var AddScreen = $("#add-screen");
var ViewScreen = $("#list-screen");
var AddButton = $("#btn-add");
var CancelScreen = $("#cancel-screen");
var SubmitButton = $("#btn-submit");

var ListContainer = $('#tbody-list');

var FilterUserGroupName = $('#filter-user-group-name');
var FilterCategoryName = $('#filter-category-name');
var FilterStatus = $('#filter-status');

var CurrentPassword = $('#current-password');
var PasswordSubmitButton = $('#password-submit');

var UserGroupName = $('#user-group-name');
var UserGroupId = $('#user-group-id');
var Category = $('#category');
var FormList = $('#form-list');
var FormRowList = $('#tbody-form-list');
var CheckAll = $('#checkAll');

var isAuthenticate;
var u_p_page = null;

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var uId = null;
var status = null;

var statusmsgsuccess = "";

UserPrivilegesPage = function() {
    this._FormsList = [];
    this._UserGroupsList = [];
    this._UserCategoryList = [];
}

UserPrivilegesPage.prototype.showList = function() {
    AddScreen.hide();
    ViewScreen.show();
    FilterUserGroupName.val('');
    FilterCategoryName.val('');
    FormList.hide();
    this.fetchUserPrivileges();
    Search_status.removeClass();
    Search_status.addClass('fa');
    Search_status.text('All');
};

UserPrivilegesPage.prototype.fetchUserPrivileges = function() {
    t_this = this;
    displayLoader();
    client_mirror.getClientUserGroups(function(error, response) {
        if (error == null) {
            t_this._FormsList = response.forms;
            t_this._UserGroupsList = response.user_groups
            t_this._UserCategoryList = response.user_category
            t_this.renderList(t_this._UserGroupsList);
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};

UserPrivilegesPage.prototype.possibleFailures = function(error) {
    if (error == "UserGroupNameAlreadyExists") {
        displayMessage(message.usergroupname_exists);
    } else if (error == 'InvalidUserGroupId') {
        displayMessage(message.invalid_usergroupid);
    } else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else if (error == 'CannotDeactivateUserExists') {
        displayMessage(message.user_privileges_cannot_deactivate);
    } else {
        displayMessage(error);
    }
};

UserPrivilegesPage.prototype.renderList = function(u_g_data) {
    t_this = this;
    var j = 1;
    ListContainer.find('tr').remove();
    if(u_g_data.length > 0) {
        $.each(u_g_data, function(k, v) {
            var cloneRow = $('#template .table-user-privileges .table-row').clone();
            $('.sno', cloneRow).text(j);

            $('.user-group-name', cloneRow).text(v.u_g_name);
            $('.category-name', cloneRow).text(v.u_c_name);

            $('.edit i').attr('title', 'Click Here to Edit');
            /*$('.edit i', cloneRow).on('click', function() {
                t_this.showEdit(v.u_g_id, v.u_g_name, v.u_c_id, v.f_ids);
            });*/
            $('.edit i', cloneRow).attr("onClick", "showEdit(" + v.u_g_id +", '"+ v.u_g_name +"', '"+ v.u_c_id +"' , ["+ v.f_ids + "])");
            if (v.is_active == true) {
                $('.status i', cloneRow).removeClass('fa-times text-danger');
                $('.status i', cloneRow).addClass('fa-check text-success');
                $('.status i', cloneRow).attr('title', 'Click here to Deactivate');
            } else {
                $('.status i', cloneRow).removeClass('fa-check text-success');
                $('.status i', cloneRow).addClass('fa-times text-danger');
                $('.status i', cloneRow).attr('title', 'Click here to Activate');
            }
            // $('.status i', cloneRow).on('click', function(e) {
            //     t_this.showModalDialog(e, v.u_g_id, v.is_active);
            // });
            $('.status i', cloneRow).attr("onClick", "showModalDialog("+ v.u_g_id +", "+ v.is_active +")");

            ListContainer.append(cloneRow);
            j = j + 1;
        });
    } else {
        ListContainer.append('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
    }
    $('[data-toggle="tooltip"]').tooltip();
};

UserPrivilegesPage.prototype.showAddScreen = function() {
    t_this = this;
    ViewScreen.hide();
    AddScreen.show();
    UserGroupName.val('');
    Category.val('');
    FormList.hide();
    UserGroupId.val('');
    this.renderCategoryList(t_this._FormsList);
};

UserPrivilegesPage.prototype.renderCategoryList = function(f_data) {
    t_this = this;
    var cat_ids = t_this._UserCategoryList;
    Category.empty();
    var select = '<option value="">Select Category</option>';
    $.each(f_data, function(k1, v1) {
        $.each(cat_ids, function(k2, v2) {
            if (parseInt(k1) === parseInt(v2.u_c_id)) {
                select = select + '<option value="' + k1 + '"> ' + v2.u_c_name + ' </option>';
            }
        });
    });
    Category.html(select);
};

UserPrivilegesPage.prototype.renderFormList = function(cat_id, arr) {
    t_this = this;
    if (cat_id != '') {
        var f_data = t_this._FormsList;
        var j = 1;
        FormList.show();
        FormRowList.find('tr').remove();
        $.each(f_data, function(k, v) {
            if (k == parseInt(cat_id)) {
                $.each(v.menus, function(key, menu) {
                    var cloneRowOne = $('#template .table-form-list .table-row-form-type').clone();
                    $('.form-type', cloneRowOne).text(key);
                    FormRowList.append(cloneRowOne);
                    $.each(menu, function(i, val) {
                        var cloneRow = $('#template .table-form-list .table-row-form-list').clone();
                        $('.form-name', cloneRow).text(val.form_name);
                        $('.u-f-id', cloneRow).val(val.form_id).addClass('form-id');
                        if (jQuery.inArray(val.form_id, arr) !== -1)
                            $('.u-f-id', cloneRow).val(val.form_id).addClass('form-id').attr("checked", "checked");
                        else
                            $('.u-f-id', cloneRow).val(val.form_id).addClass('form-id');
                        FormRowList.append(cloneRow);
                    });
                });
                select_checkbox();
            }
        });
    } else {
        FormList.hide();
    }
};

select_checkbox = function() {
    if ($('.form-id:checked').length == $('.form-id').length) {
        CheckAll.prop('checked', true);
    } else {
        CheckAll.prop('checked', false);
    }
}

UserPrivilegesPage.prototype.validate = function() {
    if (UserGroupName) {
        if (isNotEmpty(UserGroupName, message.usergroupname_required) == false)
            return false;
        else if (isLengthMinMax(UserGroupName, 1, 50, message.usergroupname_max) == false)
            return false;
        else if (isCommonName(UserGroupName, message.usergroupname_str) == false)
            return false;
    }
    if (Category) {
        if (isNotEmpty(Category, message.category_required) == false)
            return false;
    }
    if ($('.form-id')) {
        if ($('.form-id:checked').length == 0) {
            displayMessage(message.form_name_required);
            return false;
        }
    }
    return true;
};


UserPrivilegesPage.prototype.submitProcess = function() {
    var u_g_id = UserGroupId.val();
    u_g_name = UserGroupName.val();
    f_cat_id = parseInt(Category.val());
    var f_ids = [];
    $('.form-id:checked').each(function() {
        f_ids.push(parseInt($(this).val()));
    });
    t_this = this;
    displayLoader();
    if (u_g_id == '') {
        client_mirror.saveClientUserGroup(u_g_name, f_cat_id, f_ids, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.user_privileges_save_success);
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
            hideLoader();
        });
    } else {
        client_mirror.updateClientUserGroup(parseInt(u_g_id), u_g_name, f_cat_id, f_ids, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.user_privileges_updated_success);
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
            hideLoader();
        });
    }
};

showModalDialog = function(userGroupId, isActive) {
    t_this = u_p_page;
    if (isActive == true) {
        status = false;
        var statusmsg = message.user_privileges_deactive_status_confim;
        statusmsgsuccess = message.user_privileges_deactive_status_success;
    } else {
        status = true;
        var statusmsg = message.user_privileges_active_status_confim;
        statusmsgsuccess = message.user_privileges_active_status_success;
    }
    CurrentPassword.val('');
    confirm_alert(statusmsg, function(isConfirm) {
        if (isConfirm) {
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete: function() {
                    CurrentPassword.focus();
                    uId = userGroupId;
                },
            });
            // e.preventDefault();
        }
    });
}

UserPrivilegesPage.prototype.changeStatus = function(userGroupId, status) {
    t_this = this;
    if (isNotEmpty(CurrentPassword, message.password_required) == false) {
        return false;
    } else {
        var password = CurrentPassword.val();
        if (status == "false") { status = false; }
        if (status == "true") { status = true; }
        client_mirror.changeClientUserGroupStatus(userGroupId, status, password, function(error, response) {
            console.log(error, response)
            if (error == null) {
                Custombox.close();
                displaySuccessMessage(statusmsgsuccess);
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    }
};

// UserPrivilegesPage.prototype.showEdit = function(u_g_id, u_g_name, u_c_id, f_ids) {
//     t_this = this;
//     t_this.showAddScreen();
//     UserGroupName.val(u_g_name);
//     UserGroupId.val(u_g_id);
//     Category.val(u_c_id);
//     FormList.show();
//     alert(f_ids.toSource());
//     t_this.renderFormList(u_c_id, f_ids);
// };


showEdit = function(u_g_id, u_g_name, u_c_id, f_ids) {
    t_this = u_p_page;
    t_this.showAddScreen();
    UserGroupName.val(u_g_name);
    UserGroupId.val(u_g_id);
    Category.val(u_c_id);
    FormList.show();
    t_this.renderFormList(u_c_id, f_ids);
};

key_search = function(mainList) {
    key_one = FilterUserGroupName.val().toLowerCase();
    key_two = FilterCategoryName.val().toLowerCase();
    d_status = Search_status_ul.find('li.active').attr('value');
    var fList = [];
    for (var entity in mainList) {
        uGName = mainList[entity].u_g_name;
        cNames = mainList[entity].u_c_name;
        dStatus = mainList[entity].is_active;
        if ((~uGName.toLowerCase().indexOf(key_one)) && (~cNames.toLowerCase().indexOf(key_two))) {
            if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)) {
                fList.push(mainList[entity]);
            }
        }
    }
    return fList
}

PageControls = function() {

    Category.change(function() {
        var val = $(this).val().trim()
        u_p_page.renderFormList(val, []);
    });

    AddButton.click(function() {
        u_p_page.showAddScreen();
    });

    CancelScreen.click(function() {
        u_p_page.showList();
    });

    CheckAll.click(function() {
        $('.form-id').not(this).prop('checked', this.checked);
    });

    SubmitButton.click(function() {
        if (u_p_page.validate()) {
            u_p_page.submitProcess();
        }
    });

    PasswordSubmitButton.click(function() {
        t_this.changeStatus(uId, status);
    });

    FilterUserGroupName.keyup(function() {
        fList = key_search(u_p_page._UserGroupsList);
        u_p_page.renderList(fList);
    });

    FilterCategoryName.keyup(function() {
        fList = key_search(u_p_page._UserGroupsList);
        u_p_page.renderList(fList);
    });

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
        fList = key_search(u_p_page._UserGroupsList);
        u_p_page.renderList(fList);
    });
}
u_p_page = new UserPrivilegesPage();

$(document).ready(function() {
    PageControls();
    u_p_page.showList();
});
