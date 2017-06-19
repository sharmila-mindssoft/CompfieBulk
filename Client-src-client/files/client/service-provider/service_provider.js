var addScreen = $("#add-screen");
var viewScreen = $("#list-screen");
var addButton = $("#btn-add");
var cancelButton = $("#cancelButton");
var btnSubmit = $('#btnSubmit');

var listContainer = $('#tbody-list');
var filterserviceProvider = $('#filterserviceProvider');
var filterContactPerson = $('#filterContactPerson');
var filterContactNo = $('#filterContactNo');
var filterEmailID = $('#filterEmailID');
var filterRemarks = $('#filterRemarks');
var CurrentPassword = $('#current-password');
var btnPasswordSubmit_Status = $('#btnPasswordSubmit_Status');
var btnPasswordSubmit_Block = $('#btnPasswordSubmit_Block');
var divRemarks = $('#divRemarks');
var txtRemarks = $('#txtRemarks');

var filterStatus = $('#filter-status');


var isAuthenticate;
var sp_page = null;

var search_status = $('#search-status');
var search_status_ul = $('.search-status-list');
var search_status_li = $('.search-status-li');

var serviceProviderID = $('#serviceProvider-id');
var txtServiceProviderName = $('#txtServiceProviderName');
var txtShortName = $('#txtShortName');
var txtFromDate = $('#txtFromDate');
var txtToDate = $('#txtToDate');
var txtContactPerson = $('#txtContactPerson');
var txtContact1 = $('#txtContact1');
var txtContact2 = $('#txtContact2');
var txtContact3 = $('#txtContact3');
var txtMobile1 = $('#txtMobile1');
var txtMobile2 = $('#txtMobile2');
var txtEmailID = $('#txtEmailID');
var txtAddress = $('#txtAddress');

var spId = null;
var spName = null;
var sp_status = null;
var blocked_status = null
var remarks = "";
var _serviceProviderList;

serviceProviderPage = function() {
    this._serviceProviderList = [];
}

serviceProviderPage.prototype.showList = function() {
    addScreen.hide();
    viewScreen.show();
    this.fetchServiceProviders();
};

serviceProviderPage.prototype.fetchServiceProviders = function() {
    t_this = this;
    displayLoader();
    client_mirror.getServiceProviders(function(error, response) {
        if (error == null) {
            // t_this._serviceProviderList = response.service_providers;
            // t_this.renderList(t_this._serviceProviderList);
            _serviceProviderList = response.service_providers;
            t_this.renderList(_serviceProviderList);
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};

serviceProviderPage.prototype.showAddScreen = function() {
    t_this = this;
    viewScreen.hide();
    addScreen.show();
    txtServiceProviderName.focus();
};

serviceProviderPage.prototype.possibleFailures = function(error) {
    if (error == "UserGroupNameAlreadyExists") {
        displayMessage(message.domainname_required);
    } else if (error == 'InvalidUserGroupId') {
        displayMessage(message.invalid_usergroupid);
    } else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else {
        displayMessage(error);
    }
};

serviceProviderPage.prototype.renderList = function(sp_data) {
    t_this = this;
    var j = 1;
    listContainer.find('tr').remove();
    if (sp_data.length == 0) {
        var no_record_row = $("#template .table-no-record tr");
        var clone = no_record_row.clone();
        listContainer.append(clone);
    } else {
        $.each(sp_data, function(k, v) {
            var cloneRow = $('#template .table-service-provider .table-row').clone();

            $('.sno', cloneRow).text(j);
            $('.sp-name', cloneRow).text(v.s_p_name);
            $('.sp-contact-name', cloneRow).text(v.cont_person);
            $('.sp-contact-number', cloneRow).text(v.cont_no);
            $('.sp-contact-email', cloneRow).text(v.e_id);
            $('.sp-contact-remarks', cloneRow).text(v.remarks);

            $('.edit i').attr('title', 'Click Here to Edit');

            if (v.is_active == true) {
                $('.status i', cloneRow).removeClass('fa-times text-danger');
                $('.status i', cloneRow).addClass('fa-check text-success');
                $('.status i', cloneRow).attr('title', 'Click here to Deactivate');
            } else {
                $('.status i', cloneRow).removeClass('fa-check text-success');
                $('.status i', cloneRow).addClass('fa-times text-danger');
                $('.status i', cloneRow).attr('title', 'Click here to Activate');
            }
            if (v.is_blocked == true) {
                $('.blocked i', cloneRow).addClass('text-danger');
                $('.blocked i', cloneRow).removeClass('text-muted');
                if (v.unblock_days == 0) {
                    $('.blocked i', cloneRow).hide();
                } else {
                    $('.blocked i', cloneRow).attr('title', 'Days left ' + v.unblock_days + ' day(s)');
                }
            } else {
                $('.blocked i', cloneRow).removeClass('text-danger');
                $('.blocked i', cloneRow).addClass('text-muted');
                $('.blocked i', cloneRow).attr('title', 'Click here to Block');
            }

            if (v.is_blocked == false) {
                $('.edit i', cloneRow).attr("onClick", "showEdit(" + v.s_p_id + ", '" + v.s_p_name + "', '" + v.s_p_short + "', '" + v.cont_from + "', '" + v.cont_to + "', '" + v.cont_person + "', '" + v.cont_no + "', '" + v.mob_no + "', '" + v.e_id + "', '" + v.address + "')");

                $('.status i', cloneRow).attr("onClick", "showModalDialog(" + v.s_p_id + ",'" + v.s_p_name + "'," + v.is_active + "," + v.unblock_days + "," + v.is_blocked + ",'STATUS')");
            }

            $('.blocked i', cloneRow).attr("onClick", "showModalDialog(" + v.s_p_id + ",'" + v.s_p_name + "'," + v.is_active + "," + v.unblock_days + "," + v.is_blocked + ",'BLOCK')");

            listContainer.append(cloneRow);
            j = j + 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

//Validate Fields
serviceProviderPage.prototype.validate = function() {
    if (isNotEmpty(txtServiceProviderName, message.spname_required) == false) {
        txtServiceProviderName.focus();
        return false;
    } else if (!validateMaxLength("serviceprovidername", txtServiceProviderName.val().trim(), "Service Provider name")) {
        txtServiceProviderName.focus();
        return false;
    }
    if (isCommonName(txtServiceProviderName, message.spname_str) == false) {
        txtServiceProviderName.focus();
        return false;
    }
    if (isNotEmpty(txtShortName, message.shortname_required) == false) {
        txtShortName.focus();
        return false;
    } else if (!validateMaxLength("serviceprovider_shortname", txtShortName.val().trim(), "Short Name")) {
        txtShortName.focus();
        return false;
    }
    if (isNotEmpty(txtFromDate, message.contractfrom_required) == false) {
        txtFromDate.focus();
        return false;
    }
    if (isNotEmpty(txtToDate, message.contractto_required) == false) {
        txtToDate.focus();
        return false;
    }
    if (isNotEmpty(txtContactPerson, message.contactperson_required) == false) {
        txtContactPerson.focus();
        return false;
    } else if (!validateMaxLength("serviceprovider_contact_person", txtContactPerson.val().trim(), "Contact Person")) {
        txtContactPerson.focus();
        return false;
    }
    if (isCommonName(txtContactPerson, message.contactname_str) == false) {
        txtContactPerson.focus();
        return false;
    }
    if (isNotEmpty(txtContact3, message.contactno_required) == false) {
        txtContact3.focus();
        return false;
    } else if (txtContact3.val().indexOf('000') >= 0) {
        txtContact3.focus();
        displayMessage(message.contactno_invalid);
        return false;
    } else if (validateMaxLength('serviceprovider_countrycode', txtContact1.val(), "Country Code") == false) {
        txtContact1.focus();
        return false;
    } else if (validateMaxLength('areacode', txtContact2.val(), "Area Code") == false) {
        txtContact2.focus();
        return false;
    } else if (!validateMaxLength("serviceprovider_contact_number", txtContact3.val().trim(), "Contact Number")) {
        txtContact3.focus();
        return false;
    }

    if (validateMaxLength('serviceprovider_mcountrycode', txtMobile1.val(), "Mobile Country Code") == false) {
        txtMobile1.focus();
        return false;
    }
    if (txtMobile2.val() != '') {
        if (isLengthMinMax(txtMobile2, 10, 10, message.mobile_required_10) == false) {
            txtMobile2.focus();
            return false;
        } else if (txtMobile2.val().indexOf('000') >= 0) {
            txtMobile2.focus();
            displayMessage(message.mobile_invalid);
            return false;
        }
    }
    if (isNotEmpty(txtEmailID, message.email_required) == false) {
        txtEmailID.focus();
        return false;
    }
    if (!validateEmail(txtEmailID.val())) {
        displayMessage(message.invalid_emailid);
        txtEmailID.focus();
        return false;
    } else if (validateMaxLength('email_id', txtEmailID.val(), "Email id") == false) {
        txtEmailID.focus();
        return false;
    }
    if (txtAddress.val() != '') {
        if (!validateMaxLength("serviceprovider_address", txtAddress.val().trim(), "Address")) {
            txtAddress.focus();
            return false;
        }
    }
    return (true);
};

showEdit = function(s_p_id, s_p_name, s_p_short, cont_from, cont_to, cont_person, cont_no, mob_no, e_id, address) {
    t_this = sp_page;
    t_this.showAddScreen();

    serviceProviderID.val(s_p_id);
    txtServiceProviderName.val(s_p_name);
    txtShortName.val(s_p_short);
    txtFromDate.val(cont_from);
    txtToDate.val(cont_to);
    txtContactPerson.val(cont_person);
    if (cont_no != null) {
        var contact = cont_no.split('-');
        txtContact1.val(contact[0]);
        txtContact2.val(contact[1]);
        txtContact3.val(contact[2]);
    }
    if (mob_no != null || mob_no != "-") {
        var mobile = mob_no.split('-');
        txtMobile1.val(mobile[0]);
        txtMobile2.val(mobile[1]);
    }

    txtEmailID.val(e_id);
    txtAddress.val(address);
};


serviceProviderPage.prototype.submitProcess = function() {
    var sp_id = serviceProviderID.val();
    var s_p_name = txtServiceProviderName.val();
    var s_p_short = txtShortName.val();
    var cont_from = txtFromDate.val();
    var cont_to = txtToDate.val();
    var cont_person = txtContactPerson.val();
    var cont_no = txtContact1.val() + '-' + txtContact2.val() + '-' + txtContact3.val();
    var mob_no = txtMobile1.val() + '-' + txtMobile2.val();
    var e_id = txtEmailID.val();
    var address = txtAddress.val();
    var t_this = this;
    displayLoader();
    if (sp_id == '') {
        //Submit Process
        client_mirror.saveServiceProvider(s_p_name, s_p_short, cont_from, cont_to, cont_person, cont_no, mob_no, e_id, address, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.sp_save_success.replace('SP_NAME', s_p_name));
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
            hideLoader();
        });
    } else {
        //Update Process
        var spDetailarray = client_mirror.getUpdateServiceProviderDict([parseInt(sp_id), s_p_name, s_p_short, cont_from, cont_to, cont_person, cont_no, mob_no, e_id, address])
        client_mirror.updateServiceProvider(spDetailarray, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.sp_update_success.replace('SP_NAME', s_p_name));
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
            hideLoader();
        });

    }
};

//open password dialog
showModalDialog = function(sp_id, s_p_name, isActive, unblock_days, isBlocked, mode) {
    t_this = sp_page;
    statusmsg = "";
    if (mode == "STATUS") {
        btnPasswordSubmit_Status.show();
        btnPasswordSubmit_Block.hide();
        divRemarks.hide();

        if (isActive == true) {
            sp_status = false;
            statusmsg = message.deactive_message;
        } else {
            sp_status = true;
            statusmsg = message.active_message;
        }
    } else if (mode == "BLOCK") {
        btnPasswordSubmit_Status.hide();
        btnPasswordSubmit_Block.show();
        divRemarks.show();
        txtRemarks.val('');

        if (isBlocked == true) {
            blocked_status = false;
            statusmsg = message.unblock_message;
        } else {
            blocked_status = true;
            statusmsg = message.block_message;
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
                    spId = sp_id;
                    spName = s_p_name;
                },
            });
            // e.preventDefault();
        }
    });
}

serviceProviderPage.prototype.changeStatus = function(sp_id, status) {
    t_this = this;
    if (isNotEmpty(CurrentPassword, message.password_required) == false) {
        return false;
    } else {
        var password = CurrentPassword.val();
        if (status == "false") { status = false; }
        if (status == "true") { status = true; }
        client_mirror.changeServiceProviderStatus(sp_id, status, password, function(error, response) {
            if (error == null) {
                Custombox.close();
                if (status) {
                    displaySuccessMessage(message.sp_activate);
                } else {
                    displaySuccessMessage(message.sp_deactivate);
                }
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    }
};

serviceProviderPage.prototype.blockSP = function(sp_id, block_status, remarks) {
    t_this = this;
    if (isNotEmpty(CurrentPassword, message.password_required) == false) {
        return false;
    }
    if (txtRemarks.val().trim() == "") {
        displayMessage(message.remarks_required);
        return false;
    } else if (!validateMaxLength("remark", txtRemarks.val().trim(), "remark")) {
        txtRemarks.focus();
        return false;
    } else {
        var password = CurrentPassword.val();
        if (block_status == "false") { block_status = false; }
        if (block_status == "true") { block_status = true; }
        client_mirror.blockServiceProvider(sp_id, block_status, remarks, password, function(error, response) {
            if (error == null) {
                Custombox.close();
                if (block_status) {
                    displaySuccessMessage(message.sp_block_success.replace('SP_NAME', spName));
                } else {
                    displaySuccessMessage(message.sp_unblock_success.replace('SP_NAME', spName));
                }
                t_this.showList();
            } else {
                t_this.possibleFailures(error);
            }
        });
    }
};

serviceProviderPage.prototype.clearValues = function() {
    serviceProviderID.val('');
    txtServiceProviderName.val('');
    txtShortName.val('');
    txtFromDate.val('');
    txtToDate.val('');
    txtContactPerson.val('');
    txtContact1.val('');
    txtContact2.val('');
    txtContact3.val('');
    txtMobile1.val('');
    txtMobile2.val('');
    txtEmailID.val('');
    txtAddress.val('');

    filterserviceProvider.val('');
    filterContactPerson.val('');
    filterContactNo.val('');
    filterEmailID.val('');
    filterRemarks.val('');

    search_status.removeClass();
    search_status.addClass('fa');
    search_status.text('All');
};

serviceProviderPage.prototype.possibleFailures = function(error) {
    if (error == "ServiceProviderNameAlreadyExists") {
        displayMessage(message.spname_exists);
    } else if (error == 'InvalidUserGroupId') {
        displayMessage(message.CannotChangeStatusOfContractExpiredSP);
    } else if (error == 'CannotDeactivateUserExists') {
        displayMessage(message.cannot_deactivate_sp);
    } else if (error == 'CannotChangeStatusOfContractExpiredSP') {
        displayMessage(message.cannot_change_status);
    } else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else if (error == 'HaveComplianceFailed') {
        displayMessage(message.reassign_compliance_before_user_disable);
    } else {
        displayMessage(error);
    }
};


key_search = function(mainList) {
    key_one = filterserviceProvider.val().toLowerCase();
    key_two = filterContactPerson.val().toLowerCase();
    key_three = filterContactNo.val().toLowerCase();
    key_four = filterEmailID.val().toLowerCase();
    key_five = filterRemarks.val().toLowerCase();
    d_status = search_status_ul.find('li.active').attr('value');
    var fList = [];
    for (var entity in mainList) {
        s_p_name = mainList[entity].s_p_name;
        cont_person = mainList[entity].cont_person;
        cont_no = mainList[entity].cont_no;
        e_id = mainList[entity].e_id;
        remarks = mainList[entity].remarks == null ? '' : mainList[entity].remarks;
        dStatus = mainList[entity].is_active;

        if ((~s_p_name.toLowerCase().indexOf(key_one)) && (~cont_person.toLowerCase().indexOf(key_two)) &&
            (~cont_no.toLowerCase().indexOf(key_three)) && (~e_id.toLowerCase().indexOf(key_four)) && (~remarks.toLowerCase().indexOf(key_five))) {
            if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)) {
                fList.push(mainList[entity]);
            }
        }
    }
    return fList
}

// Validate Input Characters
txtServiceProviderName.on('input', function(e) {
    this.value = isCommon_Name($(this));
});
txtShortName.on('input', function(e) {
    this.value = isAlphanumeric_Shortname($(this));
});
txtContactPerson.on('input', function(e) {
    this.value = isCommon_Name($(this));
});
txtContact1.on('input', function(e) {
    this.value = isNumbers_Countrycode($(this));
});
txtContact2.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtContact3.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtMobile1.on('input', function(e) {
    this.value = isNumbers_Countrycode($(this));
});
txtMobile2.on('input', function(e) {
    this.value = isNumbers($(this));
});
txtAddress.on('input', function(e) {
    this.value = isCommon_Address($(this));
});


//Page Control Events
PageControls = function() {
    var currentDate;

    current_date_ymd(function(c_date) {
        currentDate = c_date;

        // To call date picker function. assign to date field
        $(".from-date, .to-date").datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: "dd-M-yy",
            // minDate: currentDate,
            onSelect: function(selectedDate) {
                if ($(this).hasClass("from-date") == true) {
                    var dateMin = $('.from-date').datepicker("getDate");
                    var rMin = new Date(dateMin.getFullYear(), dateMin.getMonth(), dateMin.getDate()); // +1
                    $('.to-date').datepicker("option", "minDate", rMin);
                }
                if ($(this).hasClass("to-date") == true) {
                    var dateMin = $('.to-date').datepicker("getDate");
                }
            }
        });
    });

    //Add Button Click Event
    addButton.click(function() {
        sp_page.clearValues();
        sp_page.showAddScreen();
    });

    // Cancel Button Click Event
    cancelButton.click(function() {
        sp_page.clearValues();
        sp_page.showList();
    });

    // //Submit Button Click Event
    btnSubmit.click(function() {
        if (sp_page.validate()) {
            sp_page.submitProcess();
            sp_page.clearValues();
            // sp_page.showList();
        }
    });

    btnPasswordSubmit_Status.click(function() {
        var compliancesStatus = 0;
        var spUsers = [];
        $.each(_serviceProviderList, function(k, v) {
            if (v.s_p_id == spId) {
                spUsers = v.sp_users;
            }
        });

        var len = spUsers.length;
        $.each(spUsers, function(k1, v1) {
            if (v1 != 0) {
                k1++

                sp_le_split = v1.split('-');
                if (sp_le_split.length > 0) {
                    spID_split = sp_le_split[0];
                    leIDs_split = sp_le_split[1];
                    leID_splt = leIDs_split.split(',');
                }
                client_mirror.haveCompliances(parseInt(leID_splt[0]), parseInt(spID_split), function(error, response) {
                    if (error != null) {
                        compliancesStatus = 1;
                        t_this.possibleFailures(error);
                    }
                    if (k1 == len && compliancesStatus == 0) {
                        sp_page.changeStatus(spId, sp_status);
                        sp_page.clearValues();
                    }
                });
            } else {
                sp_page.changeStatus(spId, sp_status);
                sp_page.clearValues();
            }
        });


    });

    btnPasswordSubmit_Block.click(function() {
        sp_page.blockSP(spId, blocked_status, txtRemarks.val());
        txtRemarks.val('');
        sp_page.clearValues();
    });

    //Service Provider Name Filter
    filterserviceProvider.keyup(function() {
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });

    //Contact Person Filter
    filterContactPerson.keyup(function() {
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });

    //
    filterContactNo.keyup(function() {
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });

    filterEmailID.keyup(function() {
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });

    filterRemarks.keyup(function() {
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });

    search_status_ul.click(function(event) {
        search_status_li.each(function(index, el) {
            $(el).removeClass('active');
        });
        $(event.target).parent().addClass('active');

        var currentClass = $(event.target).find('i').attr('class');
        search_status.removeClass();
        if (currentClass != undefined) {
            search_status.addClass(currentClass);
            search_status.text('');
        } else {
            search_status.addClass('fa');
            search_status.text('All');
        }
        fList = key_search(sp_page._serviceProviderList);
        sp_page.renderList(fList);
    });
}

sp_page = new serviceProviderPage();

$(document).ready(function() {
    PageControls();
    sp_page.showList();
});