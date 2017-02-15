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

var filterStatus = $('#filter-status');
var currentPassword = $('#current-password');
var passwordSubmitButton = $('#password-submit');

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

serviceProviderPage = function() {
    this._serviceProviderList = [];
}

serviceProviderPage.prototype.showList = function() {
    addScreen.hide();
    viewScreen.show();
    this.fetchServiceProviders();

    //  FilterUserGroupName.val('');
    //  FilterCategoryName.val('');
    //  FormList.hide();

    //  Search_status.removeClass();
    //  Search_status.addClass('fa');
    //  Search_status.text('All');
};

serviceProviderPage.prototype.fetchServiceProviders = function() {
    t_this = this;

    client_mirror.getServiceProviders(function(error, response) {
        if (error == null) {
            t_this._serviceProviderList = response.service_providers;
            t_this.renderList(t_this._serviceProviderList);
        } else {
            t_this.possibleFailures(error);
        }
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
        //No Records Found
    } else {
        $.each(sp_data, function(k, v) {
            var cloneRow = $('#template .table-service-provider .table-row').clone();

            $('.sno', cloneRow).text(j);
            $('.sp-name', cloneRow).text(v.s_p_name);
            $('.sp-contact-name', cloneRow).text(v.cont_person);
            $('.sp-contact-number', cloneRow).text(v.cont_no);
            $('.sp-contact-email', cloneRow).text(v.e_id);

            // $('.edit i').attr('title', 'Click Here to Edit');
            // $('.edit i', cloneRow).on('click', function() {
            //     t_this.showEdit(v.u_g_id, v.u_g_name, v.u_c_id, v.f_ids);
            // });
            if (v.is_active == true) {
                $('.status i').attr('title', 'Click Here to Deactivate');
                $('.status i', cloneRow).removeClass('fa-times text-danger');
                $('.status i', cloneRow).addClass('fa-check text-success');
            } else {
                $('.status i').attr('title', 'Click Here to Activate');
                $('.status i', cloneRow).removeClass('fa-check text-success');
                $('.status i', cloneRow).addClass('fa-times text-danger');
            }
            if (v.is_blocked == true) {
                $('.blocked i', cloneRow).addClass('text-danger');
                $('.blocked i', cloneRow).removeClass('text-muted');
            } else {
                $('.blocked i', cloneRow).removeClass('text-danger');
                $('.blocked i', cloneRow).addClass('text-muted');
            }

            // $('.status i', cloneRow).on('click', function(e) {
            //     t_this.showModalDialog(e, v.u_g_id, v.is_active);
            // });
            // $('.status').hover(function() {
            //     showTitle(this);
            // });
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
    }
    if (isLengthMinMax(txtServiceProviderName, 2, 50, message.spname_max50) == false) {
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
    }
    if (isLengthMinMax(txtShortName, 2, 20, message.shortname_max20) == false) {
        shortname_max20.focus();
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
    }
    if (isLengthMinMax(txtContactPerson, 2, 50, message.contactpersonname_max50) == false) {
        txtContactPerson.focus();
        return false;
    }
    if (isNotEmpty(txtContact1, message.countrycode_required) == false) {
        txtContact1.focus();
        return false;
    }
    if (isLengthMinMax(txtContact1, 3, 4, message.countrycode_max4) == false) {
        txtContact1.focus();
        return false;
    }
    if (isNotEmpty(txtContact2, message.areacode_required) == false) {
        txtContact2.focus();
        return false;
    }
    if (isLengthMinMax(txtContact2, 3, 4, message.areacode_max4) == false) {
        txtContact2.focus();
        return false;
    }
    if (isNotEmpty(txtContact3, message.contactno_required) == false) {
        txtContact3.focus();
        return false;
    }
    if (isLengthMinMax(txtContact3, 10, 10, message.contactno_max10) == false) {
        txtContact3.focus();
        return false;
    }
    if (txtMobile2.val() != '') {
        if (isLengthMinMax(txtMobile2, 10, 10, message.mobile_max10) == false) {
            txtMobile2.focus();
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
    }
    if (txtAddress.val() != '') {
        if (isLengthMinMax(txtAddress, 10, 500, message.address_max500) == false) {
            txtAddress.focus();
            return false;
        }
    }

    return (true);
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

    if (sp_id == '') {
        //Submit Process
        client_mirror.saveServiceProvider(s_p_name, s_p_short, cont_from, cont_to, cont_person, cont_no, mob_no, e_id, address, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.save_success);
                t_this.showList();
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

};


key_search = function(mainList) {
    key_one = filterserviceProvider.val().toLowerCase();
    key_two = filterContactPerson.val().toLowerCase();
    key_three = filterContactNo.val().toLowerCase();
    key_four = filterEmailID.val().toLowerCase();
    key_five = filterRemarks.val().toLowerCase();

    //d_status = Search_status_ul.find('li.active').attr('value');
    var fList = [];
    for (var entity in mainList) {
        uGName = mainList[entity].s_p_name;
        cNames = mainList[entity].cont_person;
        //dStatus = mainList[entity].is_active;
        if ((~uGName.toLowerCase().indexOf(key_one)) && (~cNames.toLowerCase().indexOf(key_two)) && (~cNames.toLowerCase().indexOf(key_three)) && (~cNames.toLowerCase().indexOf(key_four)) && (~cNames.toLowerCase().indexOf(key_five))) {
            //if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)) {
            fList.push(mainList[entity]);
            //}
        }
    }
    return fList
}


//Page Control Events
PageControls = function() {

    // To call date picker function. assign to date field 
    $(".from-date, .to-date").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
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
            sp_page.showList();
        }
    });

    //Password Submit
    // PasswordSubmitButton.click(function() {
    //     u_p_page.validateAuthentication();
    // });

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
}

sp_page = new serviceProviderPage();

$(document).ready(function() {
    PageControls();
    sp_page.showList();
});