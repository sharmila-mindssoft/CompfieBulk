var categoryList;
var userGroupList;
var businessGroupList;
var legalEntityList;
var divisionList;
var categoryList;
var domainList;
var unitArray;
var spList;
var listLegalEntity;
var listUsers;
var listLegalEntity_edit;
var listUser_edit;
var listDomains_edit;
var listUnits_edit;

var listContainer = $("#listContainer");

var addScreen = $("#add-screen");
var viewScreen = $("#list-screen");
var addButton = $("#btn-add");
var cancelButton = $("#cancelButton");
var btnSubmit = $('#btnSubmit');
var btnNext = $('#btnNext');
var btnPrevious = $('#btnPrevious');

var hdnUserId = $('#hdnUserId');
var ddlUserCategory = $('#ddlUserCategory');
var hdnUserGroup = $('#hdnUserGroup');
var txtUserGroup = $('#txtUserGroup');
var divUserGroup = $('#divUserGroup');
var txtSeatingUnit = $('#txtSeatingUnit');
var hdnSeatingUnit = $('#hdnSeatingUnit');
var divSeatingUnit = $('#divSeatingUnit');

var txtServiceProvider = $('#txtServiceProvider');
var hdnServiceProvider = $('#hdnServiceProvider');
var divServiceProvider = $('#divServiceProvider');
var txtEmployeeName = $('#txtEmployeeName');
var txtEmployeeId = $('#txtEmployeeId');
var ddlUserLevel = $('#ddlUserLevel');
var txtEmailID = $('#txtEmailID');
var txtContactNo1 = $('#txtContactNo1');
var txtContactNo2 = $('#txtContactNo2');
var txtContactNo3 = $('#txtContactNo3');
var txtMobileNo1 = $('#txtMobileNo1');
var txtMobileNo2 = $('#txtMobileNo2');

var ddlBusinessGroup = $('#ddlBusinessGroup');
var ddlLegalEntity = $('#ddlLegalEntity');
var ddlDivision = $('#ddlDivision');
var ddlCategory = $('#ddlCategory');
var ddlDomain = $('#ddlDomain');

var CurrentPassword = $('#current-password');
var btnPasswordSubmit_Status = $('#btnPasswordSubmit_Status');
var btnPasswordSubmit_Block = $('#btnPasswordSubmit_Block');
var divRemarks = $('#divRemarks');
var txtRemarks = $('#txtRemarks');

var UnitRow = $("#template .unit-row li");
var UnitList = $(".unit-list");
var SelectedUnitCount = $(".selected_checkbox_count");
var chkSelectAll = $('.select_all');

var legalEntityRow = $("#template .legal-entity-row");

var CURRENT_TAB = 1;

var businessGroup_ids = [];
var legalEntity_ids = [];
var ACTIVE_UNITS = [];
var unit_ids_edit = [];

var userId = null;
var user_status = null;
var blocked_status = null
var remarks = "";
var empName = null;
var legal_entity_id = null;

var um_page = null;

var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");
var filterCountryName = $(".filter-country-name");

var businessGroup = $("#business-group");
var businessGroupId = $("#business-group-id");
var acBusinessGroup = $("#ac-business-group");
var filterBusinessGroupName = $(".filter-business-group-name");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");
var filterLegalEntityName = $(".filter-legal-entity-name");
var btnShow = $('#btnShow');

var selected_domain = {};
var unitFilter = $('#unit-filter');

userManagementPage = function() {
        this._userCategory = [];
        this._userGroup = [];
    }
    // Load User List
userManagementPage.prototype.showList = function() {
    addScreen.hide();
    viewScreen.show();
    this.fetchUserManagement();
};

//Load User List
userManagementPage.prototype.fetchUserManagement = function() {
    t_this = this;
    client_mirror.getUserManagement_List(function(error, response) {
        if (error == null) {
            listLegalEntity = response.ul_legal_entity;
            listUsers = response.ul_users;
            t_this.renderList(listLegalEntity, listUsers, null, null, null);
        } else {
            t_this.possibleFailures(error);
        }
    });

    // Add Button Click
    userManagementPage.prototype.showAddScreen = function() {
        t_this = this;
        viewScreen.hide();
        addScreen.show();
        ddlUserCategory.attr('disabled', false);
    };

    // Load Prerequisiste
    client_mirror.getUserManagement_Prerequisite(function(error, response) {
        if (error == null) {
            t_this._userCategory = response.um_user_category;
            userGroupList = response.um_user_group;
            businessGroupList = response.um_business_group;
            legalEntityList = response.um_legal_entity;
            divisionList = response.um_group_division;
            categoryList = response.um_group_category;
            domainList = response.um_legal_domain;
            unitArray = response.um_legal_units;
            spList = response.um_service_providers;

            loadUserCategories(t_this._userCategory)
            loadBusinessGroup(businessGroupList);

        } else {
            t_this.possibleFailures(error);
        }
    });
};

//User List
userManagementPage.prototype.renderList = function(ul_legal, ul_users, c_name, bg_name, le_name) {
    t_this = this;
    listContainer.empty();
    if (ul_legal.length != 0) {
        var le_list = client_mirror.getUserLegalEntity();
        var leids = [];
        $.each(le_list, function(k, v) {
            leids.push(v.le_id);
        });
        $.each(ul_legal, function(k, v) {
            if ($.inArray(v.le_id, leids) >= 0) {
                if (((c_name == v.c_name) || (c_name == null)) && ((bg_name == v.b_g_name) || (bg_name == null)) && ((le_name == v.le_name) || (le_name == null))) {
                    var cloneRow = $('#template .legal-entity-row').clone();

                    var total_licences = parseInt(v.total_licences);
                    var used_licences = parseInt(v.used_licences);
                    var remaining_licences = parseInt(total_licences - used_licences);

                    $('.um-country', cloneRow).text(v.c_name);
                    $('.um-business-group', cloneRow).text(v.b_g_name);
                    $('.um-legal-entity', cloneRow).text(v.le_name);
                    $('.um-contract-from', cloneRow).text(v.cont_from);
                    $('.um-contract-to', cloneRow).text(v.cont_to);
                    $('.um-total-licence', cloneRow).text(v.total_licences);
                    $('.um-used-licence', cloneRow).text(v.used_licences);
                    $('.um-remaining-licence', cloneRow).text(remaining_licences);

                    $('.filter-users', cloneRow).on('keyup', function(e) {
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    $('.filter-user-id', cloneRow).on('keyup', function(e) {
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    $('.filter-email', cloneRow).on('keyup', function(e) {
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    $('.filter-mobile', cloneRow).on('keyup', function(e) {
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    $('.search-status-list', cloneRow).click(function(event) {
                        $('.search-status-li', cloneRow).each(function(index, el) {
                            $(el).removeClass('active');
                        });
                        $(event.target).parent().addClass('active');

                        var currentClass = $(event.target).find('i').attr('class');

                        $('#search-status', cloneRow).removeClass();
                        if (currentClass != undefined) {
                            $('#search-status', cloneRow).addClass(currentClass);
                            $('#search-status', cloneRow).text('');
                        } else {
                            $('#search-status', cloneRow).addClass('fa');
                            $('#search-status', cloneRow).text('All');
                        }
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    $('.search-category-list', cloneRow).click(function(event) {
                        $('.search-category-li', cloneRow).each(function(index, el) {
                            $(el).removeClass('active');
                        });
                        $(event.target).parent().addClass('active');

                        var currentClass = $(event.target).find('i').attr('class');

                        $('#search-category', cloneRow).removeClass();
                        if (currentClass != undefined) {
                            $('#search-category', cloneRow).addClass(currentClass);
                            $('#search-category', cloneRow).text('');
                        } else {
                            $('#search-category', cloneRow).addClass('fa');
                            $('#search-category', cloneRow).text('All');
                        }
                        fList = key_search(cloneRow, v.le_id, ul_users);
                        t_this.renderUserList(v.le_id, cloneRow, fList);
                    });

                    t_this.renderUserList(v.le_id, cloneRow, ul_users);
                    listContainer.append(cloneRow);
                }
            }
        });
    }
    // $('[data-toggle="tooltip"]').tooltip();
};


userManagementPage.prototype.renderUserList = function(le_id, cloneRow, ul_users) {
    t_this = this;
    $('.user-row-body', cloneRow).empty();
    var j = 1;
    var id = "";
    $.each(ul_users, function(k1, v1) {
        if (le_id == v1.le_id) {
            var cloneUserRow = $('#template .user-row-table tr').clone();
            var user_name = v1.user_name;
            $('.sno', cloneUserRow).text(j);
            $('.um-employee-name', cloneUserRow).text(v1.emp_name);
            $('.um-user-name span', cloneUserRow).text(user_name);
            if (user_name == null || user_name == "") {
                $('.um-user-name', cloneUserRow).empty();
            } else {
                $('.um-user-name i', cloneUserRow).attr("data-original-title", v1.seating_unit);
            }

            $('.um-user-email', cloneUserRow).text(v1.email_id);
            $('.um-user-mobile', cloneUserRow).text(v1.mob_no);

            var cat_class = "";
            if (v1.u_cat_id == 2) {
                cat_class = "text-muted";
            } else if (v1.u_cat_id == 3) {
                cat_class = "text-warning";
            } else if (v1.u_cat_id == 4) {
                cat_class = "text-info";
            } else if (v1.u_cat_id == 5) {
                cat_class = "text-danger";
            }

            if (user_name == null) {
                $('.um-email-resend a', cloneUserRow).html("Resend");
                $('.um-email-resend a', cloneUserRow).attr("data-original-title", "Click here to resend email");
                $('.um-email-resend a', cloneUserRow).on('click', function(e) {
                    t_this.resendemail(v1.user_id);
                });
            }

            if (v1.is_disable != true) {
                $('.edit i', cloneUserRow).attr('title', 'Click Here to Edit');
                $('.edit i', cloneUserRow).attr("onClick", "showEdit('" + v1.user_id + "')");
                if (v1.is_active == true) {
                    $('.status i', cloneUserRow).removeClass('fa-times text-danger');
                    $('.status i', cloneUserRow).addClass('fa-check text-success');
                    $('.status i', cloneUserRow).attr('title', 'Click here to Deactivate');
                } else {
                    $('.status i', cloneUserRow).removeClass('fa-check text-success');
                    $('.status i', cloneUserRow).addClass('fa-times text-danger');
                    $('.status i', cloneUserRow).attr('title', 'Click here to Activate');
                }
                $('.status i', cloneUserRow).attr("onClick", "showModalDialog(" + v1.user_id + ", '" + v1.emp_name + "', " + v1.is_active + ", " + v1.unblock_days + ", " + v1.is_disable + "," + v1.le_id + ", 'STATUS')");
            }

            

            if (v1.is_disable == true) {
                $('.blocked i', cloneUserRow).addClass('text-danger');
                $('.blocked i', cloneUserRow).removeClass('text-muted');
                if (v1.unblock_days == 0) {
                    $('.blocked i', cloneUserRow).hide();
                } else {
                    $('.blocked i', cloneUserRow).attr('title', 'Days left ' + v1.unblock_days + ' day(s)');
                }
            } else {
                $('.blocked i', cloneUserRow).removeClass('text-danger');
                $('.blocked i', cloneUserRow).addClass('text-muted');
                $('.blocked i', cloneUserRow).attr('title', 'Click here to Block');
            }

            
            $('.blocked i', cloneUserRow).attr("onClick", "showModalDialog(" + v1.user_id + ", '" + v1.emp_name + "', " + v1.is_active + ", " + v1.unblock_days + ", " + v1.is_disable + "," + v1.le_id + ", 'BLOCK')");

            $('.um-category i', cloneUserRow).addClass(cat_class);
            $('.user-row-body', cloneRow).append(cloneUserRow);

            j = j + 1;
        }


    });
    // $('[data-toggle="tooltip"]').tooltip();
};

showEdit = function(user_id) {
    client_mirror.userManagementEditView(parseInt(user_id), function(error, response) {
        if (error == null) {
            listUser_edit = response.ul_userDetails;
            listLegalEntity_edit = response.ul_legal_entities;
            listDomains_edit = response.ul_user_domains;
            listUnits_edit = response.ul_user_units;
            t_this.showEditView(listUser_edit, listLegalEntity_edit, listDomains_edit, listUnits_edit);
        } else {
            t_this.possibleFailures(error);
        }
    });
}

userManagementPage.prototype.showEditView = function(listUser_edit, listLegalEntity_edit, listDomains_edit, listUnits_edit) {
    t_this = this;
    t_this.showAddScreen();
    CURRENT_TAB = 1;
    showTab();
    if (listUser_edit.length != 0) {
        $.each(listUser_edit, function(k1, v1) {
            hdnUserId.val(v1.user_id);
            txtEmployeeId.val(v1.emp_code);
            txtEmployeeName.val(v1.emp_name);
            txtEmailID.val(v1.email_id);

            ddlUserCategory.val(v1.u_cat_id);
            um_page.onChangeUserCategory();
            ddlUserCategory.attr('disabled', true);

            hdnUserGroup.val(v1.u_g_id);
            for (var k in userGroupList) {
                if (userGroupList[k].u_g_id == v1.u_g_id) {
                    txtUserGroup.val(userGroupList[k].u_g_name);
                    break;
                }
            }

            if (v1.seating_unit_id != null) {
                hdnSeatingUnit.val(v1.seating_unit_id);
                for (var ks in unitArray) {
                    if (unitArray[ks].u_unt_id == v1.seating_unit_id) {
                        txtSeatingUnit.val(unitArray[ks].u_unt_name);
                        break;
                    }
                }
            }

            if (v1.user_level != null) {
                ddlUserLevel.val(v1.user_level);
            }

            if (v1.cont_no != null || v1.cont_no != "-") {
                var contact = v1.cont_no.split('-');
                txtContactNo1.val(contact[0]);
                txtContactNo2.val(contact[1]);
                txtContactNo3.val(contact[2]);

            }

            if (v1.mob_no != null || v1.mob_no != "-") {
                var mobile = v1.mob_no.split('-');
                txtMobileNo1.val(mobile[0]);
                txtMobileNo2.val(mobile[1]);

            }

            if (v1.is_sp == true) {
                hdnServiceProvider.val(v1.sp_id);
                for (var ks in spList) {
                    if (spList[ks].u_sp_id == v1.sp_id) {
                        txtServiceProvider.val(spList[ks].u_sp_name);
                        break;
                    }
                }
            }

        });
    }

    if (listLegalEntity_edit.length > 0) {
        var le_ids = [];
        var bg_ids = [];
        $.each(listLegalEntity_edit, function(k, v) {
            le_ids.push(v.le_id);
            bg_ids.push(v.bg_id);
        });
        var i = 0;
        $.each(bg_ids, function(k, v) {
            i = 1;
            $('#ddlBusinessGroup option[value=' + v + ']').attr('selected', 'selected');
        });
        if (i == 1) {
            ddlBusinessGroup.multiselect('rebuild');
            loadLegalEntity();
        }
        var j = 0;
        $.each(le_ids, function(k, v) {
            j = 1;
            $('#ddlLegalEntity option[value=' + v + ']').attr('selected', 'selected');
        });
        if (j == 1) {
            ddlLegalEntity.multiselect('rebuild');
            loadDomain();
            loadCategory();
            loadDivision();
        }
        if (listDomains_edit.length > 0) {
            var d_ids = [];
            $.each(listDomains_edit, function(k, v) {
                d_ids.push(v.le_id + '-' + v.u_dm_id);
            });
            var l = 0;
            $.each(d_ids, function(k, v) {
                l = 1;
                var element = $('#ddlDomain option[value=' + v + ']');
                element.attr('selected', 'selected');
                var arr = element.val().split("-");
                if (!selected_domain[arr[1]]) {
                    selected_domain[element.val()] = element.parent().attr('label');
                }
            });
            if (l == 1)
                ddlDomain.multiselect('rebuild');
        }

        if (listUnits_edit.length > 0) {
            var div_ids = [];
            var cat_ids = [];
            $.each(listUnits_edit, function(k, v) {
                if (div_ids.indexOf(v.div_id) == -1)
                    div_ids.push(v.div_id);
                if (cat_ids.indexOf(v.cat_id) == -1)
                    cat_ids.push(v.cat_id);

                unit_ids_edit.push(v.u_unt_id + '-' + v.le_id);
            });
            var m = 0;
            $.each(div_ids, function(k, v) {
                m = 1;
                $('#ddlDivision option[value=' + v + ']').attr('selected', 'selected');
            });
            if (m == 1)
                ddlDivision.multiselect('rebuild');

            var n = 0;
            $.each(cat_ids, function(k, v) {
                n = 1;
                $('#ddlCategory option[value=' + v + ']').attr('selected', 'selected');
            });
            if (n == 1)
                ddlCategory.multiselect('rebuild');
        }
    }
}

function isComplianceAvailable(lega_entity_id, userID_compliances) {
    client_mirror.haveCompliances(lega_entity_id, userID_compliances, function(error, response) {
        if (error == null) {
            return true;
        } else {
            t_this.possibleFailures(error);
            return false;
        }
    });

}

//open password dialog
showModalDialog = function(user_id, emp_name, isActive, unblock_days, isBlocked, le_id, mode) {
    var statusmsg = "";
    if (mode == "STATUS") {
        btnPasswordSubmit_Status.show();
        btnPasswordSubmit_Block.hide();
        divRemarks.hide();

        if (isActive == true) {
            user_status = false;
            statusmsg = message.deactive_message;
        } else {
            user_status = true;
            statusmsg = message.active_message;
        }
    } else if (mode == "BLOCK") {
        btnPasswordSubmit_Status.hide();
        btnPasswordSubmit_Block.show();
        divRemarks.show();
        if (isBlocked == true) {
            blocked_status = false;
            statusmsg = message.enable_user_message;
        } else {
            blocked_status = true;
            statusmsg = message.disable_user_message;
        }
    }

    CurrentPassword.val('');
    confirm_alert(statusmsg, function(isConfirm) {
        if (isConfirm) {
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete: function() {
                    CurrentPassword.focus();
                    userId = user_id;
                    empName = emp_name;
                    legal_entity_id = le_id;
                },
            });
            return false;
        }
    });
}

//Save User Management data
userManagementPage.prototype.submitProcess = function() {
    var sp_id, is_sp, s_unit, u_level;
    var user_id = hdnUserId.val();
    if (parseInt(ddlUserCategory.val()) == '2') {
        is_sp = false;
        sp_id = null;
        s_unit = null;
        u_level = null;
        Domain_ids = [];
        unit_ids = [];
    } else if (parseInt(ddlUserCategory.val()) == '3') {
        is_sp = false;
        sp_id = null;
        s_unit = parseInt(hdnSeatingUnit.val().trim());
        u_level = null;
        Domain_ids = [];
        unit_ids = [];
    } else if (parseInt(ddlUserCategory.val()) == '4') {
        is_sp = false;
        sp_id = null;
        s_unit = parseInt(hdnSeatingUnit.val().trim());
        u_level = null;
        Domain_ids = getDomainIds();
        unit_ids = getUnits();
    } else if (parseInt(ddlUserCategory.val()) == '5') {
        is_sp = false;
        sp_id = null;
        s_unit = parseInt(hdnSeatingUnit.val().trim());
        u_level = parseInt(ddlUserLevel.val().trim());
        Domain_ids = getDomainIds();
        unit_ids = getUnits();
    } else if (parseInt(ddlUserCategory.val()) == '6') {
        is_sp = true;
        sp_id = parseInt(hdnServiceProvider.val().trim());
        s_unit = null;
        u_level = null;
        Domain_ids = getDomainIds();
        unit_ids = getUnits();
    }

    legalEntity_ids = getLegalEntityIds();

    clientUserDetail = {
        "u_cat_id": parseInt(ddlUserCategory.val()),
        "u_g_id": parseInt(hdnUserGroup.val().trim()),
        "email_id": txtEmailID.val().trim(),
        "emp_name": txtEmployeeName.val().trim(),
        "emp_code": txtEmployeeId.val().trim(),
        "cont_no": txtContactNo1.val().trim() + '-' + txtContactNo2.val().trim() + '-' + txtContactNo3.val().trim(),
        "mob_no": txtMobileNo1.val().trim() + '-' + txtMobileNo2.val().trim(),
        "u_level": u_level,
        "s_unit": s_unit,
        "is_sp": is_sp,
        "sp_id": sp_id,
        "user_entity_ids": legalEntity_ids,
        "user_domain_ids": Domain_ids,
        "user_unit_ids": unit_ids
    };

    clientUserDetail_update = {
        'u_id': parseInt(hdnUserId.val().trim()),
        "u_g_id": parseInt(hdnUserGroup.val().trim()),
        "email_id": txtEmailID.val().trim(),
        "emp_name": txtEmployeeName.val().trim(),
        "emp_code": txtEmployeeId.val().trim(),
        "cont_no": txtContactNo1.val().trim() + '-' + txtContactNo2.val().trim() + '-' + txtContactNo3.val().trim(),
        "mob_no": txtMobileNo1.val().trim() + '-' + txtMobileNo2.val().trim(),
        "u_level": u_level,
        "s_unit": s_unit,
        "is_sp": is_sp,
        "sp_id": sp_id,
        "user_entity_ids": legalEntity_ids,
        "user_domain_ids": Domain_ids,
        "user_unit_ids": unit_ids
    };

    if (user_id == '') {
        client_mirror.saveClientUser(clientUserDetail, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.save_success);
                um_page.clearValues();
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    } else {
        client_mirror.updateClientUser(clientUserDetail_update, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.update_success);
                um_page.clearValues();
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    }
};

userManagementPage.prototype.changeStatus = function(user_id, status, legal_entity_id) {
    t_this = this;
    if (isNotEmpty(CurrentPassword, message.password_required) == false) {
        return false;
    } else {
        if (!isComplianceAvailable(legal_entity_id, user_id)) {
            var password = CurrentPassword.val();
            if (status == "false") { status = false; }
            if (status == "true") { status = true; }
            client_mirror.changeClientUserStatus(user_id, status, empName, password, function(error, response) {
                if (error == null) {
                    Custombox.close();
                    displaySuccessMessage(message.status_success);
                    t_this.showList();
                } else {
                    t_this.possibleFailures(error);
                }
            });
        }
    }
};

userManagementPage.prototype.blockuser = function(user_id, block_status, remarks) {
    t_this = this;
    if (isNotEmpty(CurrentPassword, message.password_required) == false) {
        return false;
    } else {
        var password = CurrentPassword.val();
        if (block_status == "false") { block_status = false; }
        if (block_status == "true") { block_status = true; }
        client_mirror.blockUser(user_id, block_status, remarks, password, function(error, response) {
            if (error == null) {
                Custombox.close();
                if (block_status) {
                    displaySuccessMessage(message.disable_success);
                    um_page.clearValues();
                    t_this.showList();
                } else {
                    displaySuccessMessage(message.enable_success);
                }
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    }
};

userManagementPage.prototype.possibleFailures = function(error) {
    if (error == "EmployeeCodeAlreadyExists") {
        displayMessage(message.employeeid_exists);
    } else if (error == 'UnitsAlreadyAssigned') {
        displayMessage(message.units_already_assigned);
    } else if (error == 'UserLimitExceeds') {
        displayMessage(message.userlimitexceeds);
    } else if (error == 'HaveComplianceFailed') {
        displayMessage(message.reassign_compliance_before_user_disable);
    } else {
        displayMessage(error);
    }
};


//User Group Auto Complete
txtUserGroup.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    if (ddlUserCategory.val() != '') {
        condition_fields.push("u_c_id");
        condition_values.push(ddlUserCategory.val());

        var text_val = $(this).val();
        commonAutoComplete(
            e, divUserGroup, hdnUserGroup, text_val,
            userGroupList, "u_g_name", "u_g_id",
            function(val) {
                onAutoCompleteSuccess(txtUserGroup, hdnUserGroup, val);
            }, condition_fields, condition_values);
    }
});

//Seating unit Auto Complete
txtSeatingUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    if (ddlUserCategory.val() != '') {
        // condition_fields.push("u_c_id");
        // condition_values.push(ddlUserCategory.val());

        var text_val = $(this).val();
        commonAutoComplete(
            e, divSeatingUnit, hdnSeatingUnit, text_val,
            unitArray, "u_unt_name", "u_unt_id",
            function(val) {
                onAutoCompleteSuccess(txtSeatingUnit, hdnSeatingUnit, val);
            }, condition_fields, condition_values);
    }
});

//Service Provider Auto Complete
txtServiceProvider.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    if (ddlUserCategory.val() != '') {
        var text_val = $(this).val();
        commonAutoComplete(
            e, divServiceProvider, hdnServiceProvider, text_val,
            spList, "u_sp_name", "u_sp_id",
            function(val) {
                onAutoCompleteSuccess(txtServiceProvider, hdnServiceProvider, val);
            }, condition_fields, condition_values);
    }
});


//Load User Categories
function loadUserCategories(um_data) {
    ddlUserCategory.empty();
    ddlUserCategory.append($('<option></option>').val('').html('Select'));
    $.each(um_data, function(key, value) {
        ddlUserCategory.append($('<option></option>').val(um_data[key].u_c_id).html(um_data[key].u_c_name));
    });
}

//Load Business Group
function loadBusinessGroup(businessGroupList) {
    if (businessGroupList.length > 0) {
        $.each(businessGroupList, function(key, value) {
            if (value.is_active == false) {
                return;
            }
            var optText = '<option></option>';
            optText = '<option></option>';

            ddlBusinessGroup.append($(optText).val(value.bg_id).html(value.bg_name));
        });
        ddlBusinessGroup.multiselect('rebuild');
    }
    loadLegalEntity();
}

//Load Legal Entity MultiSelect
function loadLegalEntity() {
    ddlLegalEntity.empty();
    var sBusinessGroup = [];
    if (ddlBusinessGroup.val() != null)
        sBusinessGroup = ddlBusinessGroup.val().map(Number);
    if (legalEntityList.length > 0) {
        var others_flag = true;
        var others_str = "";
        var bg_flag = null;
        var bg_str = "";
        $.each(legalEntityList, function(k, v) {
            if (ddlUserCategory.val() == 3) {
                if (v.le_admin == null || v.le_admin == hdnUserId.val()) {
                    if (v.bg_id == null) {
                        if (others_flag)
                            others_str += '<optgroup label="Others">';
                        others_str += '<option value="' + v.le_id + '" >' + v.le_name + '</option>';
                        others_flag = false;
                    } else {
                        $.each(businessGroupList, function(key, value) {
                            if ($.inArray(value.bg_id, sBusinessGroup) >= 0 && v.bg_id == value.bg_id) {
                                if (bg_flag != v.bg_id)
                                    bg_str += '<optgroup label="' + value.bg_name + '">';
                                bg_str += '<option value="' + v.le_id + '">' + v.le_name + '</option>';
                                bg_flag = v.bg_id;
                            }
                        });
                    }
                }

            } else {
                if (v.bg_id == null) {
                    if (others_flag)
                        others_str += '<optgroup label="Others">';
                    others_str += '<option value="' + v.le_id + '" >' + v.le_name + '</option>';
                    others_flag = false;
                } else {
                    $.each(businessGroupList, function(key, value) {
                        if ($.inArray(value.bg_id, sBusinessGroup) >= 0 && v.bg_id == value.bg_id) {
                            if (bg_flag != v.bg_id)
                                bg_str += '<optgroup label="' + value.bg_name + '">';
                            bg_str += '<option value="' + v.le_id + '">' + v.le_name + '</option>';
                            bg_flag = v.bg_id;
                        }
                    });
                }
            }
        });
        var str = bg_str + others_str;
        ddlLegalEntity.html(str);
        ddlLegalEntity.multiselect('rebuild');
    } else {
        ddlLegalEntity.empty();
        ddlLegalEntity.multiselect('rebuild');
    }
}

function loadDivision() {
    ddlDivision.empty();
    var sLegalEntity = [];
    if (ddlLegalEntity.val() != null)
        sLegalEntity = ddlLegalEntity.val().map(Number);
    if (divisionList.length > 0) {
        var bg_flag = null;
        var str = "";
        $.each(legalEntityList, function(key, value) {
            $.each(divisionList, function(k, v) {
                if ($.inArray(value.le_id, sLegalEntity) >= 0 && v.le_id == value.le_id) {
                    if (bg_flag != v.le_id)
                        str += '<optgroup label="' + value.le_name + '">';
                    str += '<option value="' + v.d_id + '">' + v.d_name + '</option>';
                    bg_flag = v.le_id;
                }
            });
        });
        ddlDivision.html(str);
        ddlDivision.multiselect('rebuild');
    } else {
        ddlDivision.empty();
        ddlDivision.multiselect('rebuild');
    }
}

// Load Category
function loadCategory() {
    ddlCategory.empty();
    var sLegalEntity = [];
    if (ddlLegalEntity.val() != null)
        sLegalEntity = ddlLegalEntity.val().map(Number);
    if (categoryList.length > 0) {
        var lg_flag = null;
        var str = "";
        $.each(legalEntityList, function(key, value) {
            $.each(categoryList, function(k, v) {
                if ($.inArray(value.le_id, sLegalEntity) >= 0 && v.le_id == value.le_id) {
                    if (lg_flag != v.le_id)
                        str += '<optgroup label="' + value.le_name + '">';
                    // var dVal = value.le_id + '-' + v.d_id;
                    str += '<option value="' + v.cat_id + '">' + v.cat_name + '</option>';
                    lg_flag = v.le_id;
                }
            });
        });
        ddlCategory.html(str);
        ddlCategory.multiselect('rebuild');
    } else {
        ddlCategory.empty();
        ddlCategory.multiselect('rebuild');
    }
}

//Load Domain
function loadDomain() {
    ddlDomain.empty();
    var sLegalEntity = [];
    if (ddlLegalEntity.val() != null)
        sLegalEntity = ddlLegalEntity.val().map(Number);
    if (domainList.length > 0) {
        var lg_flag = null;
        var str = "";
        $.each(legalEntityList, function(key, value) {
            $.each(domainList, function(k, v) {
                if ($.inArray(value.le_id, sLegalEntity) >= 0 && v.le_id == value.le_id) {
                    if (lg_flag != v.le_id)
                        str += '<optgroup label="' + value.le_name + '">';
                    var dVal = value.le_id + '-' + v.u_dm_id;
                    str += '<option value="' + dVal + '">' + v.u_dm_name + '</option>';
                    lg_flag = v.le_id;
                }
            });
        });
        ddlDomain.html(str);
        ddlDomain.multiselect('rebuild');
    } else {
        ddlDomain.empty();
        ddlDomain.multiselect('rebuild');
    }
}

function getLegalEntityIds() {
    legalEntity_ids = [];
    if (ddlLegalEntity.val() != null) {
        for (var i = 0; i < ddlLegalEntity.val().length; i++) {
            ids = ddlLegalEntity.val();
            legalEntity_ids.push(parseInt(ids[i]))
        }
        return legalEntity_ids;
    }
}

function getDomainIds() {
    Domain_ids = [];
    for (var i = 0; i < ddlDomain.val().length; i++) {
        split = ddlDomain.val()[i].split('-');
        var dict = {};
        dict.le_id = parseInt(split[0]);
        dict.d_id = parseInt(split[1]);
        Domain_ids.push(dict);
    }
    return Domain_ids;
}

function getUnits() {
    unit_ids = [];
    for (var i = 0; i < ACTIVE_UNITS.length; i++) {
        split = ACTIVE_UNITS[i].split('-');
        var dict = {};
        dict.le_id = parseInt(split[1]);
        dict.u_id = parseInt(split[0]);
        unit_ids.push(dict);
    }
    return unit_ids;
}

// Validate Input Characters
txtEmployeeName.on('input', function(e) {
    this.value = isCommon_Name($(this));
});
txtEmployeeId.on('input', function(e) {
    this.value = isAlphanumeric_Shortname($(this));
});
txtContactNo1.on('input', function(e) {
    this.value = isNumbers_Countrycode($(this));
});
txtContactNo2.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtContactNo3.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtMobileNo1.on('input', function(e) {
    this.value = isNumbers_Countrycode($(this));
});
txtMobileNo2.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtEmailID.on('input', function(e) {
    this.value = isCommon_Email($(this));
});


userManagementPage.prototype.clearValues = function() {
    ddlUserCategory.val('');
    hdnUserGroup.val('');
    txtUserGroup.val('');
    divUserGroup.val('');
    txtSeatingUnit.val('');
    hdnSeatingUnit.val('');
    hdnUserId.val('');

    txtServiceProvider.val('');
    hdnServiceProvider.val('');
    divServiceProvider.val('');
    txtEmployeeName.val('');
    txtEmployeeId.val('');
    ddlUserLevel.val('');
    txtEmailID.val('');
    txtContactNo1.val('');
    txtContactNo2.val('');
    txtContactNo3.val('');
    txtMobileNo1.val('');
    txtMobileNo2.val('');

    country.val('');
    countryId.val('');
    businessGroup.val('');
    businessGroupId.val('');
    legalEntity.val('');
    legalEntityId.val('');

    ddlBusinessGroup.empty();
    ddlBusinessGroup.multiselect('rebuild');

    ddlLegalEntity.empty();
    ddlLegalEntity.multiselect('rebuild');

    ddlDivision.empty();
    ddlDivision.multiselect('rebuild');

    ddlCategory.empty();
    ddlCategory.multiselect('rebuild');

    ddlDomain.empty();
    ddlDomain.multiselect('rebuild');

    $('.select-division').hide();
    $('.select-category').hide();
    $('.select-domain').hide();
    $(".view-seating-unit").hide();
    $(".view-service-provider").hide();
    $(".view-user-level").hide();

    UnitList.empty;

    ddlUserCategory.focus();
};

userManagementPage.prototype.onChangeUserCategory = function() {
    t_this = this;

    if (ddlUserCategory.val() == '2') {
        $('.select-business-group').show();
        $('.select-legal-entity').show();
        $('.select-division').hide();
        $('.select-category').hide();
        $('.select-domain').hide();
        $(".view-seating-unit").hide();
        $(".view-service-provider").hide();
        $(".view-user-level").hide();
        btnNext.hide();
        btnPrevious.hide();
        btnSubmit.show();
    } else if (ddlUserCategory.val() == '3') {
        $('.select-business-group').show();
        $('.select-legal-entity').show();
        $('.select-division').hide();
        $('.select-category').hide();
        $('.select-domain').hide();
        $(".view-seating-unit").show();
        $(".view-service-provider").hide();
        $(".view-user-level").hide();
        btnNext.hide();
        btnPrevious.hide();
        btnSubmit.show();
    } else if (ddlUserCategory.val() == '4') {
        $('.select-business-group').show();
        $('.select-legal-entity').show();
        $('.select-division').hide();
        $('.select-category').hide();
        $('.select-domain').show();
        $(".view-seating-unit").show();
        $(".view-service-provider").hide();
        $(".view-user-level").hide();
        btnNext.show();
        btnSubmit.hide();
        btnPrevious.hide();
    } else if (ddlUserCategory.val() == '5') {
        $('.select-business-group').show();
        $('.select-legal-entity').show();
        $('.select-division').show();
        $('.select-category').show();
        $('.select-domain').show();
        $(".view-seating-unit").show();
        $(".view-service-provider").hide();
        $(".view-user-level").show();
        btnNext.show();
        btnSubmit.hide();
        btnPrevious.hide();
    } else if (ddlUserCategory.val() == '6') {
        $('.select-business-group').show();
        $('.select-legal-entity').show();
        $('.select-division').show();
        $('.select-category').show();
        $('.select-domain').show();
        $(".view-seating-unit").hide();
        $(".view-service-provider").show();
        $(".view-user-level").hide();
        btnNext.show();
        btnSubmit.hide();
        btnPrevious.hide();
    } else {
        $('.select-division').hide();
        $('.select-category').hide();
        $('.select-domain').hide();
        $(".view-seating-unit").hide();
        $(".view-service-provider").hide();
        $(".view-user-level").hide();
        btnNext.hide();
        btnPrevious.hide();
        btnSubmit.show();
    }
};


userManagementPage.prototype.selectAllUnits = function() {
    ACTIVE_UNITS = [];
    if (unitArray.length > 0) {
        $('.unit-list li').each(function(index, el) {
            if (chkSelectAll.prop('checked')) {
                if ($(el).hasClass('heading')) {
                    $(el).find('i').addClass('fa fa-check pull-right');
                } else {
                    $(el).addClass('active');
                    $(el).find('i').addClass('fa fa-check pull-right');
                    if (jQuery.inArray($(el).attr('id'), ACTIVE_UNITS) === -1)
                        ACTIVE_UNITS.push($(el).attr('id'));
                }
            } else {
                if ($(el).hasClass('heading')) {
                    $(el).find('i').removeClass('fa fa-check pull-right');
                } else {
                    $(el).removeClass('active');
                    $(el).find('i').removeClass('fa fa-check pull-right');
                }
                $(el).removeClass('active');
                $(el).find('i').removeClass('fa fa-check pull-right');
            }
        });
    }
};

userManagementPage.prototype.loadUnits = function() {
    t_this = this;
    UnitList.empty();
    if (unitArray.length == 0) {
        var clone = UnitRow.clone();
        clone.text('No Units Found');
        UnitList.append(clone);
    } else {
        legalEntity_ids = getLegalEntityIds();
        var le_name = "";
        var u_ids = [];
        $.each(selected_domain, function(le_domain_id, legalentity_name) {
            var arr = le_domain_id.split("-");
            var legalentity_id = arr[0];
            var domain_id = arr[1];
            $.each(unitArray, function(key, value) {
                if ((value.le_id == legalentity_id) && (jQuery.inArray(parseInt(domain_id), value.d_ids) !== -1) && (jQuery.inArray(value.u_unt_id, u_ids) === -1)) {
                    u_ids.push(value.u_unt_id);
                    if (le_name != legalentity_name) {
                        var cloneLe = UnitRow.clone();
                        cloneLe.html(legalentity_name + '<i></i>');
                        cloneLe.addClass('heading');
                        cloneLe.attr('id', 'le' + legalentity_id);
                        UnitList.append(cloneLe);
                        le_name = legalentity_name;
                        cloneLe.click(function() {
                            activateUnit(this, legalentity_id);
                        });
                    }
                    unit_idval = value.u_unt_id + '-' + value.le_id;
                    unit_text = value.u_unt_code + " - " + value.u_unt_name + " - " + value.u_unt_address;
                    var clone = UnitRow.clone();
                    clone.html(unit_text + '<i></i>');
                    clone.attr('id', unit_idval);
                    clone.addClass('le' + legalentity_id);
                    UnitList.append(clone);
                    if (unit_ids_edit.length > 0) {
                        if (jQuery.inArray(unit_idval, unit_ids_edit) !== -1)
                            activateUnit(clone, legalentity_id);
                    }
                    clone.click(function() {
                        activateUnit(this, legalentity_id);
                    });
                }
            });
        });
    }
}


function activateUnit(element, id) {
    if ($(element).hasClass('active')) {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        index = ACTIVE_UNITS.indexOf($(element).attr('id'));
        ACTIVE_UNITS.splice(index, 1);
        if ($('.le' + id).length != $('.le' + id + '.active').length)
            $('#le' + id).find('i').removeClass('fa fa-check pull-right');
        else
            $('#le' + id).find('i').addClass('fa fa-check pull-right');
    } else {
        if ($(element).hasClass('heading')) {
            if ($(element).find('i').hasClass('fa')) {
                $.each($('.le' + id), function(i) {
                    $(this).removeClass('active');
                    $(this).find('i').removeClass('fa fa-check pull-right');
                    index = ACTIVE_UNITS.indexOf($(this).attr('id'));
                    ACTIVE_UNITS.splice(index, 1);
                    ACTIVE_UNITS = ACTIVE_UNITS.filter(item => item !== $(this).attr('id'));
                });
                $(element).find('i').removeClass('fa fa-check pull-right');
            } else {
                $.each($('.le' + id), function(i) {
                    $(this).addClass('active');
                    $(this).find('i').addClass('fa fa-check pull-right');
                    if (jQuery.inArray($(this).attr('id'), ACTIVE_UNITS) === -1)
                        ACTIVE_UNITS.push($(this).attr('id'));
                });
                $(element).find('i').addClass('fa fa-check pull-right');
            }
        } else {
            $(element).addClass('active');
            $(element).find('i').addClass('fa fa-check pull-right');
            if (jQuery.inArray($(element).attr('id'), ACTIVE_UNITS) === -1)
                ACTIVE_UNITS.push($(element).attr('id'));
            if ($('.le' + id).length == $('.le' + id + '.active').length)
                $('#le' + id).find('i').addClass('fa fa-check pull-right');
            else
                $('#le' + id).find('i').removeClass('fa fa-check pull-right');
        }
    }
}



function showTab() {
    hideall = function() {
        $('.user_management_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();

        btnNext.hide();
        btnPrevious.show();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        } else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
    }

    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        btnNext.show();
    } else if (CURRENT_TAB == 2) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-2').addClass('active')
        $('#tab2').addClass('active in');
        $('#tab2').show();

        btnSubmit.show();
    }
};

userManagementPage.prototype.validateMandatory = function(status) {
    if (ddlUserCategory.val().trim().length == 0) {
        displayMessage(message.user_category_required);
        ddlUserCategory.focus();
        return false;
    } else {
        if (ddlUserCategory.val().trim() == 3 || ddlUserCategory.val().trim() == 4 || ddlUserCategory.val().trim() == 5) {
            if (hdnSeatingUnit.val().trim().length == 0) {
                displayMessage(message.seatingunit_required);
                txtSeatingUnit.focus();
                return false;
            }
        } else if (ddlUserCategory.val().trim() == 6) {
            if (hdnServiceProvider.val().trim().length == 0) {
                displayMessage(message.spname_required);
                txtServiceProvider.focus();
                return false;
            }
        }

    }
    if (hdnUserGroup.val().trim().length == 0) {
        displayMessage(message.usergroup_required);
        txtUserGroup.focus();
        return false;
    }
    if (txtEmailID.val().trim().length == 0) {
        displayMessage(message.emailid_required);
        txtEmailID.focus();
        return false;
    } else {
        validateMaxLength('email_id', txtEmailID.val(), "Email id");
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        if (reg.test(txtEmailID.val().trim()) == false) {
            displayMessage(message.invalid_emailid);
            txtEmailID.focus();
            return false;
        }
    }

    if (txtEmployeeName.val().trim().length == 0) {
        displayMessage(message.employeename_required);
        txtEmployeeName.focus();
        return false;
    } else {
        validateMaxLength('employeename', txtEmployeeName.val(), "Employee name");
    }

    if (txtEmployeeId.val().trim().length == 0) {
        displayMessage(message.employeeid_required);
        txtEmployeeId.focus();
        return false;
    } else {
        validateMaxLength('employeeid', txtEmployeeId.val(), "Employee id");
    }

    if (txtContactNo3.val().indexOf('000') >= 0) {
        txtContactNo3.focus();
        displayMessage(message.contactno_invalid);
        return false;
    }
    if (txtMobileNo2.val().trim().length == 0) {
        displayMessage(message.mobile_required);
        txtMobileNo2.focus();
        return false;
    } else if (txtMobileNo2.val().indexOf('000') >= 0) {
        txtMobileNo2.focus();
        displayMessage(message.mobile_invalid);
        return false;
    }


    if (ddlLegalEntity.val() == null) {
        displayMessage(message.legalentity_required);
        ddlLegalEntity.focus();
        return false;
    }

    if (ddlUserCategory.val().trim() == 4 || ddlUserCategory.val().trim() == 5 || ddlUserCategory.val().trim() == 6) {
        if (ddlDomain.val() == null) {
            displayMessage(message.domain_required);
            ddlDomain.focus();
            return false;
        }
    }
    if(status == true) {
        if (ddlUserCategory.val().trim() == 5 || ddlUserCategory.val().trim() == 6) {
            if (ACTIVE_UNITS.length == 0) {
                displayMessage(message.units_required);
                return false;
            }
        }
    }
    return true;
}

userManagementPage.prototype.resendemail = function(id) {
    client_mirror.resendRegistrationEmail(parseInt(id), function(error, response) {
        if (error == null) {
            displaySuccessMessage(message.email_sent);
        } else {
            t_this.possibleFailures(error);
        }
    });
}

key_search = function(cloneRow, le_id, data) {
    key_one = $('.filter-users', cloneRow).val().toLowerCase();
    key_two = $('.filter-user-id', cloneRow).val().toLowerCase();
    key_three = $('.filter-email', cloneRow).val().toLowerCase();
    key_four = $('.filter-mobile', cloneRow).val().toLowerCase();
    d_status = $('.search-status-list', cloneRow).find('li.active').attr('value');
    d_category = $('.search-category-list', cloneRow).find('li.active').attr('value');
    var fList = [];
    for (var v in data) {
        if (le_id == data[v].le_id) {
            emp_name = data[v].emp_name;
            user_name = data[v].user_name;
            if (user_name == null) user_name = "";
            email_id = data[v].email_id;
            mob_no = data[v].mob_no;
            dStatus = data[v].is_active;
            dCategory = data[v].u_cat_id;
            if ((~emp_name.toLowerCase().indexOf(key_one)) && (~user_name.toLowerCase().indexOf(key_two)) && (~email_id.toLowerCase().indexOf(key_three)) && (~mob_no.toLowerCase().indexOf(key_four))) {
                if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)) {
                    if ((d_category == 'all') || (parseInt(d_category) == dCategory))
                        fList.push(data[v]);
                }
            }
        }
    }
    //consol.log(fList);
    return fList
}

//Page Control Events
PageControls = function() {

    //Add Button Click Event
    addButton.click(function() {
        CURRENT_TAB = 1;
        showTab();
        btnNext.hide();
        btnPrevious.hide();
        um_page.showAddScreen();
        um_page.onChangeUserCategory();
        unit_ids_edit = [];
    });

    // Cancel Button Click Event
    cancelButton.click(function() {
        um_page.clearValues();
        um_page.showList();
    });



    //Category onchange
    ddlUserCategory.change(function() {
        um_page.onChangeUserCategory();
    });

    //Business Group onchange
    ddlBusinessGroup.change(function() {
        loadLegalEntity();
    });

    ddlLegalEntity.multiselect({
        buttonWidth: '100%',
        enableClickableOptGroups: true,
        onChange: function(option, checked, select) {
            loadDivision();
            loadCategory();
            loadDomain();
        },
        onDropdownShow: function(event) {
            if (hdnUserId.val() == "" && ddlUserCategory.val() == 3)
                loadLegalEntity();
        }
    });

    if (ddlDomain) {
        ddlDomain.multiselect({
            buttonWidth: '100%',
            enableClickableOptGroups: true,
            onChange: function(option, checked, select) {
                selected_domain = {};
                $('#ddlDomain option:selected').each(function(index, brand) {
                    var arr = $(this).val().split("-");
                    if (!selected_domain[arr[1]]) {
                        selected_domain[$(this).val()] = $(this).parent().attr('label');
                    }
                });
            }
        });
    }

    //Next Button Click Event
    btnNext.click(function() {
        if (um_page.validateMandatory(false)) {
            CURRENT_TAB += 1;
            showTab();
            um_page.loadUnits();
            btnSubmit.show();
            btnPrevious.show();
        }
    });

    // Previous Button Click Event
    btnPrevious.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
        btnNext.show();
        btnSubmit.hide();
        btnPrevious.hide();
    });

    // Submit Button Click Event
    btnSubmit.click(function() {
        if (um_page.validateMandatory(true)) {
            um_page.submitProcess();
        }
    });

    chkSelectAll.click(function() {
        um_page.selectAllUnits();
    });

    btnPasswordSubmit_Status.click(function() {
        var compliancesStatus = 0;
        var userleids = [];
        $.each(listUsers, function(k, v) {
            if(v.le_id == legal_entity_id && v.user_id == userId) {
                userleids = v.le_ids;
            }
        });
        var len = userleids.length;
        $.each(userleids, function(k, v) {
            k++
            client_mirror.haveCompliances(parseInt(v), parseInt(userId), function(error, response) {
                if (error != null) {
                    compliancesStatus = 1;
                    t_this.possibleFailures(error);
                }
                if(k == len && compliancesStatus == 0) {
                    um_page.changeStatus(userId, user_status, legal_entity_id);
                }
            });
        });
    });

    btnPasswordSubmit_Block.click(function() {
        if (txtRemarks.val().trim() == "") {
            displayMessage(message.remarks_required);
        } else {
            um_page.blockuser(userId, blocked_status, txtRemarks.val());
        }
    });

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = client_mirror.getUserLegalEntity();
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.country_required);
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(val);
        }, condition_fields, condition_values);
    });

    businessGroup.keyup(function(e) {
        var text_val = businessGroup.val().trim();
        var businessGroupList = client_mirror.getUserLegalEntity();
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, acBusinessGroup, businessGroupId, text_val, businessGroupList, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = client_mirror.getUserLegalEntity();
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.legalentity_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        if (businessGroupId.val() != '') {
            condition_fields.push("bg_id");
            condition_values.push(businessGroupId.val());
        }
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(val);
        }, condition_fields, condition_values);
    });
    var user_cat_id = client_mirror.getUserCategoryID();
    if (user_cat_id == 1)
        $('#user_filter').show();

    btnShow.click(function() {
        (country.val()) ? c_name = country.val(): c_name = null;
        (businessGroup.val()) ? bg_name = businessGroup.val(): bg_name = null;
        (legalEntity.val()) ? le_name = legalEntity.val(): le_name = null;
        um_page.renderList(listLegalEntity, listUsers, c_name, bg_name, le_name);
    });

    unitFilter.keyup(function(e) {
        var searchText = $(this).val().toLowerCase();
        $('.unit-list > li').each(function() {
            var currentLiText = $(this).text(),
                showCurrentLi = currentLiText.toLowerCase().indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });
}

onCountryAutoCompleteSuccess = function(val) {
    country.val(val[1]);
    countryId.val(val[0]);
    country.focus();
    clearElement([businessGroup, businessGroupId, legalEntity, legalEntityId]);
}

onBusinessGroupAutoCompleteSuccess = function(val) {
    businessGroup.val(val[1]);
    businessGroupId.val(val[0]);
    businessGroup.focus();
    clearElement([legalEntity, legalEntityId]);
}

onLegalEntityAutoCompleteSuccess = function(val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

um_page = new userManagementPage();

$(document).ready(function() {
    PageControls();
    um_page.showList();
});