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

var UnitRow = $("#template .unit-row li");
var UnitList = $(".unit-list");
var SelectAll = $('.select_all');
var SelectedUnitCount = $(".selected_checkbox_count");
var chkSelectAll = $('.select_all');

var legalEntityRow = $("#template .legal-entity-row");

var CURRENT_TAB = 1;

var businessGroup_ids = [];
var legalEntity_ids = [];
var ACTIVE_UNITS = [];
var unit_ids_edit = [];

var um_page = null;

userManagementPage = function() {
        this._userCategory = [];
        this._userGroup = [];
    }
    // ===================================================================================
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
            t_this.renderList(listLegalEntity, listUsers);

        } else {
            // t_this.possibleFailures(error);
        }
    });

    // ===================================================================================    
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
            // t_this.possibleFailures(error);
        }
    });
};

//User List
userManagementPage.prototype.renderList = function(ul_legal, ul_users) {
    t_this = this;
    listContainer.empty();
    if (ul_legal.length == 0) {
        //No Records Found
    } else {
        $.each(ul_legal, function(k, v) {
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

            var j = 1;
            $.each(ul_users, function(k1, v1) {
                if (v.le_id == v1.le_id) {
                    var cloneUserRow = $('#template .user-row-table tr').clone();

                    var user_name = v1.user_name;
                    $('.sno', cloneUserRow).text(j);
                    $('.um-employee-name', cloneUserRow).text(v1.emp_name);
                    $('.um-user-name', cloneUserRow).text(user_name);
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
                    }

                    $('.edit i').attr('title', 'Click Here to Edit');
                    $('.edit i', cloneUserRow).attr("onClick", "showEdit('" + v1.user_id + "')");

                    $('.um-category i', cloneUserRow).addClass(cat_class);
                    $('.user-row-body', cloneRow).append(cloneUserRow);

                    j = j + 1;
                }
            });
            listContainer.append(cloneRow);
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
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
            // t_this.possibleFailures(error);
        }
    });
}

userManagementPage.prototype.showEditView = function(listUser_edit, listLegalEntity_edit, listDomains_edit, listUnits_edit) {
    t_this = this;
    t_this.showAddScreen();

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
                $('#ddlDomain option[value=' + v + ']').attr('selected', 'selected');
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
                if (v.le_admin == null) {
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
                                // var dVal = value.bg_id + '-' + v.le_id;
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
                            // var dVal = value.bg_id + '-' + v.le_id;
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
        $.each(divisionList, function(k, v) {
            $.each(legalEntityList, function(key, value) {
                if ($.inArray(value.le_id, sLegalEntity) >= 0 && v.le_id == value.le_id) {
                    if (bg_flag != v.le_id)
                        str += '<optgroup label="' + value.le_name + '">';
                    // var dVal = value.le_id + '-' + v.d_id;
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
        $.each(categoryList, function(k, v) {
            $.each(legalEntityList, function(key, value) {
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
        $.each(domainList, function(k, v) {
            $.each(legalEntityList, function(key, value) {
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
    for (var i = 0; i < ddlLegalEntity.val().length; i++) {
        ids = ddlLegalEntity.val();
        legalEntity_ids.push(parseInt(ids))
    }
    return legalEntity_ids;
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
                $(el).addClass('active');
                $(el).find('i').addClass('fa fa-check pull-right');
                var chkid = $(el).attr('id');
                // ACTIVE_UNITS.push(parseInt(chkid));
                ACTIVE_UNITS.push(chkid);
            } else {
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
        $.each(unitArray, function(key, value) {
            unit_idval = value.u_unt_id + '-' + value.le_id;
            unit_text = value.u_unt_code + " - " + value.u_unt_name + " - " + value.u_unt_address;
            var clone = UnitRow.clone();
            clone.html(unit_text + '<i></i>');
            clone.attr('id', unit_idval);
            UnitList.append(clone);
            if (unit_ids_edit.length > 0) {
                if (jQuery.inArray(unit_idval, unit_ids_edit) !== -1)
                    activateUnit(clone);
            }
            clone.click(function() {
                activateUnit(this);
            });
        });
    }
}


function activateUnit(element) {

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        // index = ACTIVE_UNITS.indexOf(parseInt(chkid));
        index = ACTIVE_UNITS.indexOf(chkid);
        ACTIVE_UNITS.splice(index, 1);
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        // ACTIVE_UNITS.push(parseInt(chkid));
        ACTIVE_UNITS.push(chkid);
    }
}

function showTab() {
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
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

userManagementPage.prototype.validateMandatory = function() {
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
            } else if (ddlUserCategory.val().trim() == 6) {
                if (hdnServiceProvider.val().trim().length == 0) {
                    displayMessage(message.spname_required);
                    txtServiceProvider.focus();
                    return false;
                }
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
    if (txtMobileNo2.val().trim().length == 0) {
        displayMessage(message.mobile_required);
        txtMobileNo2.focus();
        return false;
    }
    if (ddlLegalEntity.val() == null) {
        displayMessage(message.legalentity_required);
        ddlLegalEntity.focus();
        return false;
    } else {}


    if (ddlUserCategory.val().trim() == 4 || ddlUserCategory.val().trim() == 5 || ddlUserCategory.val().trim() == 6) {
        if (ddlDomain.val() == null) {
            displayMessage(message.domain_required);
            ddlDomain.focus();
            return false;
        } else {}
    }
    if (ddlUserCategory.val().trim() == 5 || ddlUserCategory.val().trim() == 6) {
        if (ACTIVE_UNITS.length == 0) {
            displayMessage(message.units_required);
            return false;
        }
    }
    return true;
}



//Page Control Events
PageControls = function() {

    //Add Button Click Event
    addButton.click(function() {
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

    //Legal Entity onchange
    ddlLegalEntity.change(function() {
        loadDivision();
        loadCategory();
        loadDomain();
    });

    //Next Button Click Event
    btnNext.click(function() {
        CURRENT_TAB += 1;
        showTab();
        um_page.loadUnits();
        btnSubmit.show();
        btnPrevious.show();
    });

    // //Previous Button Click Event
    btnPrevious.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
        btnNext.show();
        btnSubmit.hide();
        btnPrevious.hide();
    });

    // //Submit Button Click Event
    btnSubmit.click(function() {
        if (um_page.validateMandatory()) {
            um_page.submitProcess();
        }
    });

    chkSelectAll.click(function() {
        um_page.selectAllUnits();
    });
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