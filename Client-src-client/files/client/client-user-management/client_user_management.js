var categoryList;
var userGroupList;
var businessGroupList;
var legalEntityList;
var divisionList;
var categoryList;
var domainList;
var unitArray;

var addScreen = $("#add-screen");
var viewScreen = $("#list-screen");
var addButton = $("#btn-add");
var cancelButton = $("#cancelButton");
var btnSubmit = $('#btnSubmit');
var btnNext = $('#btnNext');

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

var CURRENT_TAB = 1;

var businessGroup_ids = [];
var legalEntity_ids = [];
var ACTIVE_UNITS = [];

var um_page = null;

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

userManagementPage = function() {
    this._userCategory = [];
    this._userGroup = [];
}

userManagementPage.prototype.showList = function() {
    addScreen.hide();
    viewScreen.show();
    this.fetchUserManagement();
};

userManagementPage.prototype.fetchUserManagement = function() {
    t_this = this;

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

            loadUserCategories(t_this._userCategory)
            loadBusinessGroup(businessGroupList);
            loadLegalEntity();

        } else {
            // t_this.possibleFailures(error);
        }
    });
};

userManagementPage.prototype.renderList = function(um_data) {
    t_this = this;
}

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
    // ddlBusinessGroup.empty();
    $.each(businessGroupList, function(key, value) {
        if (value.is_active == false) {
            return;
        }
        var optText = '<option></option>';
        // if ($.inArray(value.bg_id, businessGroup_ids) >= 0) {
        optText = '<option selected="selected"></option>';
        // }
        ddlBusinessGroup.append($(optText).val(value.bg_id).html(value.bg_name));
    });
    ddlBusinessGroup.multiselect('rebuild');
}

//Load Legal Entity MultiSelect
function loadLegalEntity() {
    // ddlLegalEntity.empty();

    if (ddlBusinessGroup.val() != null) {
        var sBusinessGroup = ddlBusinessGroup.val().map(Number);
        var str = '';

        $.each(businessGroupList, function(key, value) {
            var bgID = value.bg_id;
            if ($.inArray(bgID, sBusinessGroup) >= 0) {
                var flag = true;
                $.each(legalEntityList, function(key1, v) {
                    // if ($.inArray(bgID, v.businessGroup_ids) >= 0) {
                    var sText = '';
                    // $.each(legalEntity_ids, function(key2, value2) {
                    //     if (v.le_id == value2.le_id && bgID == value2.bg_id) {
                    //         sText = 'selected="selected"'
                    //     }
                    // });
                    if (flag) {
                        str += '<optgroup label="' + value.bg_name + '">';
                    }
                    var dVal = bgID + '-' + v.le_id;
                    str += '<option value="' + dVal + '" ' + sText + '>' + v.le_name + '</option>';
                    flag = false;
                    // }
                });
                if (flag == false) str += '</optgroup>'
            }
        });
        ddlLegalEntity.append(str);
        ddlLegalEntity.multiselect('rebuild');
    } else {
        ddlLegalEntity.empty();
        $.each(legalEntityList, function(key, value) {
            if (value.is_active == false) {
                return;
            }
            var optText = '<option></option>';
            optText = '<option selected="selected"></option>';

            ddlLegalEntity.append($(optText).val(value.le_id).html(value.le_name));
        });
        ddlLegalEntity.multiselect('rebuild');
    }
}

function loadDivision() {
    ddlDivision.empty();

    if (ddlLegalEntity.val() != null) {
        var sLegalEntity = ddlLegalEntity.val().map(Number);
        var str = '';

        $.each(legalEntityList, function(key, value) {
            var leID = value.le_id;
            // if ($.inArray(leID, sLegalEntity) >= 0) {
            var flag = true;
            $.each(divisionList, function(key1, v) {
                // if ($.inArray(bgID, v.businessGroup_ids) >= 0) {
                var sText = '';
                // $.each(legalEntity_ids, function(key2, value2) {
                //     if (v.le_id == value2.le_id && bgID == value2.bg_id) {
                //         sText = 'selected="selected"'
                //     }
                // });
                if (flag) {
                    str += '<optgroup label="' + value.le_name + '">';
                }
                var dVal = leID + '-' + v.le_id;
                str += '<option value="' + dVal + '" ' + sText + '>' + v.d_name + '</option>';
                flag = false;
                // }
            });
            if (flag == false) str += '</optgroup>'
                // }
        });
        ddlDivision.append(str);
        ddlDivision.multiselect('rebuild');

    } else {}
}

// Load Category
function loadCategory() {
    ddlCategory.empty();

    if (ddlLegalEntity.val() != null) {
        var sLegalEntity = ddlLegalEntity.val().map(Number);
        var str = '';

        $.each(legalEntityList, function(key, value) {
            var leID = value.le_id;
            // if ($.inArray(leID, sLegalEntity) >= 0) {
            var flag = true;
            $.each(categoryList, function(key1, v) {
                // if ($.inArray(bgID, v.businessGroup_ids) >= 0) {
                var sText = '';
                // $.each(legalEntity_ids, function(key2, value2) {
                //     if (v.le_id == value2.le_id && bgID == value2.bg_id) {
                //         sText = 'selected="selected"'
                //     }
                // });
                if (flag) {
                    str += '<optgroup label="' + value.le_name + '">';
                }
                var dVal = leID + '-' + v.le_id;
                str += '<option value="' + dVal + '" ' + sText + '>' + v.cat_name + '</option>';
                flag = false;
                // }
            });
            if (flag == false) str += '</optgroup>'
                // }
        });
        ddlCategory.append(str);
        ddlCategory.multiselect('rebuild');

    } else {}
}

//Load Domain
function loadDomain() {
    // ddlDomain.empty();

    if (ddlLegalEntity.val() != null) {
        //var sLegalEntity = ddlLegalEntity.val().map(Number);
        // split = ddlLegalEntity.val().split('-');
        // var sLegalEntity = parseint(split[1]);
        var sLegalEntity = [];

        for (var i = 0; i < ddlLegalEntity.val().length; i++) {
            var split = ddlLegalEntity.val()[i].split('-');
            sLegalEntity.push(parseInt(split[1]))
        }

        var str = '';

        $.each(legalEntityList, function(key, value) {
            var leID = value.le_id;
            if ($.inArray(leID, sLegalEntity) != -1) {
                var flag = true;
                $.each(domainList, function(key1, v) {
                    // if ($.inArray(leID, v.businessGroup_ids) >= 0) {
                    if (leID == v.le_id) {
                        var sText = '';
                        // $.each(legalEntity_ids, function(key2, value2) {
                        //     if (v.le_id == value2.le_id && bgID == value2.bg_id) {
                        //         sText = 'selected="selected"'
                        //     }
                        // });
                        if (flag) {
                            str += '<optgroup label="' + value.le_name + '">';
                        }
                        var dVal = leID + '-' + v.u_dm_id;
                        // alert(v.u_dm_id + '-' + v.u_dm_name);
                        str += '<option value="' + dVal + '" ' + sText + '>' + v.u_dm_name + '</option>';
                        flag = false;
                        // }
                    }
                });
                if (flag == false) str += '</optgroup>'
            }
        });
        // ddlDomain.multiselect('destroy');
        ddlDomain.append(str);
        ddlDomain.multiselect('rebuild');

    } else {}
}

//Save User Management data
userManagementPage.prototype.submitProcess = function() {
    var sp_id, is_sp, s_unit, u_level;
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
        sp_id = 1;
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

    client_mirror.saveClientUser(clientUserDetail, function(error, response) {
        if (error == null) {
            displaySuccessMessage(message.save_success);
            t_this.showList();
        }
    });
};

function getLegalEntityIds() {
    legalEntity_ids = [];
    for (var i = 0; i < ddlLegalEntity.val().length; i++) {
        split = ddlLegalEntity.val()[i].split('-');
        legalEntity_ids.push(parseInt(split[1]))
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

userManagementPage.prototype.showAddScreen = function() {
    t_this = this;
    viewScreen.hide();
    addScreen.show();
};

userManagementPage.prototype.clearValues = function() {
    ddlUserCategory.val('');
    hdnUserGroup.val('');
    txtUserGroup.val('');
    divUserGroup.val('');
    txtSeatingUnit.val('');
    hdnSeatingUnit.val('');

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

    // ddlBusinessGroup.empty();
    // ddlLegalEntity.empty();
    // ddlDivision.empty();
    // ddlCategory.empty();
    // ddlDomain.empty();

    // legalEntity_ids = [];
    // businessGroup_ids = [];
    // Domain_ids = [];

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

        btnSubmit.hide();
        btnNext.hide();
        // PreviousButton.hide();
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
        // PreviousButton.show();

        // if (validateFirstTab() == false) {
        //     CURRENT_TAB -= 1;
        //     return false;
        // } else {
        //     displayLoader();
        //     mirror.getAssignStatutoryWizardTwoCount(
        //         int(val_domain_id), ACTIVE_UNITS,
        //         function(error, data) {
        //             if (error == null) {
        //                 totalRecord = data.total_records;
        //                 if (data.unit_total > 5000 && ACTIVE_UNITS.length > 1) {
        //                     displayMessage(message.maximum_compliance_selection_reached);
        //                     hideLoader();
        //                     CURRENT_TAB -= 1;
        //                     return false;
        //                 } else {
        //                     callAPI(API_Wizard2);
        //                     hideall();
        //                     enabletabevent(2);
        //                     $('.tab-step-2').addClass('active')
        //                     $('#tab2').addClass('active in');
        //                     $('#tab2').show();
        //                     SubmitButton.show();
        //                     PreviousButton.show();
        //                     SaveButton.show();
        //                     ShowMore.show();
        //                     showBreadCrumbText();
        //                 }
        //             } else {
        //                 displayMessage(error);
        //                 hideLoader();
        //                 CURRENT_TAB -= 1;
        //                 return false;
        //             }
        //         }
        //     );
        // }
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
                displayMessage("Select Seating Unit");
                txtSeatingUnit.focus();
                return false;
            } else if (ddlUserCategory.val().trim() == 6) {
                if (hdnServiceProvider.val().trim().length == 0) {
                    displayMessage("Select Seating Unit");
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
    return true;
}

//Page Control Events
PageControls = function() {

    //Add Button Click Event
    addButton.click(function() {
        um_page.clearValues();
        btnNext.hide();
        um_page.showAddScreen();
    });

    // Cancel Button Click Event
    cancelButton.click(function() {
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


    //Submit Button Click Event
    btnNext.click(function() {
        CURRENT_TAB += 1;
        showTab();
        um_page.loadUnits();
    });

    // //Submit Button Click Event
    btnSubmit.click(function() {
        if (um_page.validateMandatory()) {
            um_page.submitProcess();
            um_page.clearValues();
            // um_page.showList();
        }
    });

    chkSelectAll.click(function() {
        um_page.selectAllUnits();
    });
}

um_page = new userManagementPage();

$(document).ready(function() {
    PageControls();
    um_page.showList();
});