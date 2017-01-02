var country = $("#country");
var legalEntity = $("#legal-entity");
var domain = $("#domain");
var domainID = $("#domain");
var acDomain = $("#ac-domain");
var unit = $("#unit");
var act = $("#act");
var complianceTask = $("#compliance-task");
var complianceFrequency = $("#compliance-frequency");
var userType = $("#user-type");
var user = $("#user");
var fromDate = $("#from-date");
var toDate = $("#to-date");
var complianceTaskStatus = $("#compliance-task-status");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
var legalEntityName = $("#legal-entity-name");
var countryName = $("#country-name");
var domainName = $("#domain-name");
var reportTableTbody = $("#report-table-tbody");
var templates = $("#templates");
var reportTable = $("#report-table");
var reportTable = $("#total-record");
var REPORT = null;



function PageControls() {
    showButton.click(function() {
        reportView.show();
        showAnimation(reportView);
        REPORT.loadReportValues();
    });


    domain.keyup(function(e) {
        //alert(REPORT.toSource());
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, 1];
        var text_val = $(this).val();
        commonAutoComplete(e, acDomain, domainID, text_val, domainList, "d_name", "d_id", function(val) {
            onAutoCompleteSuccess(domain, domainID, val);
        }, condition_fields, condition_values);

    });
}

function StatusReportConsolidated() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._frequencies = [];
    this._user_type = [];
    this._compliance_task_status = [];
    this._service_providers = [];
}

StatusReportConsolidated.prototype.loadFilter = function() {
    reportView.hide();
    this.fetchFilterList();
};

StatusReportConsolidated.prototype.fetchFilterList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india"},{"c_id":1,"c_name":"srilanka"}],"entities":[{"le_id":1,"le_name":"RG Legal Entity"},{"le_id":2,"le_name":"ABC Legal Entity"}],"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":2,"is_active":true}],"frequencies":[{"f_id":1,"f_name":"Periodical"},{"f_id":2,"f_name":"Review"},{"f_id":3,"f_name":"Flexi Review"},{"f_id":4,"f_name":"One Time"}],"user_type":[{"user_type_id":1,"user_type_name":"Assignee"},{"user_type_id":2,"user_type_name":"Concurrence"},{"user_type_id":3,"user_type_name":"Approval"}],"compliance_task_status":[{"comp_task_status_id":1,"comp_task_status":"Complied"},{"comp_task_status_id":2,"comp_task_status":"Delayed Compliances"},{"comp_task_status_id":3,"comp_task_status":"Inprogress"},{"comp_task_status_id":4,"comp_task_status":"Not Complied"}],"service_providers":[{"s_p_id":1,"s_p_name":"String","s_p_shrot":"short"}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._entities = object.entities;
    t_this._domains = object.domains;
    t_this._frequencies = object.frequencies;
    t_this._userType = object.user_type;
    t_this._complianceTaskStatus = object.compliance_task_status;
    t_this._serviceProviders = object.service_providers;

    t_this.renderCountriesList(t_this._countries);
    t_this.renderLegalEntityList(t_this._entities);
    t_this.renderComplianceFrequencyList(t_this._frequencies);
    t_this.renderUserTypeList(t_this._userType);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.renderCountriesList = function(data) {
    t_this = this;
    country.empty();
    var countryName = [];
    $.each(data, function(i, e) {
        //countryName.push(e.c_name+",");
        countryName = e.c_name;
    });
    country.html(countryName);
};

StatusReportConsolidated.prototype.renderLegalEntityList = function(data) {
    t_this = this;
    legalEntity.empty();
    var legalEntityName = [];
    $.each(data, function(i, e) {
        //legalEntityName.push(e.le_name+",");
        legalEntityName = e.le_name;
    });
    legalEntity.html(legalEntityName);
};

StatusReportConsolidated.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.f_id + '"> ' + e.f_name + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

StatusReportConsolidated.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.user_type_id + '"> ' + e.user_type_name + ' </option>';
    });
    userType.html(userTypeList);
};

StatusReportConsolidated.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.comp_task_status_id + '"> ' + e.comp_task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

StatusReportConsolidated.prototype.loadReportValues = function() {
    AddScreen.show();
    Domain_name.focus();
};





















showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated', function() {
        $(this).removeClass();
    });
}


StatusReportConsolidated.prototype.displayMessage = function(message) {
    Msg_pan.text(message);
    Msg_pan.show();
};

StatusReportConsolidated.prototype.clearMessage = function() {
    Msg_pan.text('');
    Msg_pan.hide();
};

StatusReportConsolidated.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        //this.displayMessage(msg.domainname_exists);
        this.displayMessage("Domain name exists");
    } else if (error == 'InvalidDomainId') {
        //this.displayMessage(msg.invalid_domainid);
        this.displayMessage("invalid domainid");
    } else if (error == 'InvalidPassword') {
        //this.displayMessage(msg.invalid_password);
        this.displayMessage("invalid password");
    } else {
        this.displayMessage(error);
    }
};

StatusReportConsolidated.prototype.popupWarning = function(message, callback) {
    var Warning_popup = $('.warning-confirm');
    Warning_popup.dialog({
        //title: msg.title_status_change,
        title: "title status change",
        buttons: {
            Ok: function() {
                $(this).dialog('close');
                callback(true);
            },
            Cancel: function() {
                $(this).dialog('close');
                callback(false);
            }
        },
        open: function() {
            $('.warning-message').html(message);
        }
    });
};


StatusReportConsolidated.prototype.showAddScreen = function() {
    AddScreen.show();
    Domain_name.focus();
};

//Status Title
function showTitle(e) {
    if (e.className == "fa c-pointer status fa-times text-danger") {
        e.title = 'Click Here to Activate';
    } else if (e.className == "fa c-pointer status fa-check text-success") {
        e.title = 'Click Here to Deactivate';
    }
}

//open password dialog
function showModalDialog(e, domainId, isActive) {
    t_this = this;
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
                        t_this.changeStatus(domainId, passStatus);
                    }
                },
            });
            e.preventDefault();
        }
    });
}

//validate
StatusReportConsolidated.prototype.validateAuthentication = function() {
    t_this = this;
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        //this.displayMessage(msg.password_required);
        this.displayMessage("password required");
        CurrentPassword.focus();
        return false;
    } else {
        validateMaxLength('password', password, "Password");
    }
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        } else {
            t_this.possibleFailures(error);
        }
    });
}

StatusReportConsolidated.prototype.fetchCountryMultiselect = function() {
    var str = '';
    for (var i in REPORT._CountryList) {
        d = REPORT._CountryList[i];
        if (d.is_active == true) {
            var selected = '';
            if ($.inArray(d.country_id, REPORT._country_ids) >= 0)
                selected = ' selected ';
            else
                selected = '';
            str += '<option value="' + d.country_id + '" ' + selected + '>' + d.country_name + '</option>';
        }
    }
    MultiSelect_Country.html(str).multiselect('rebuild');
};

StatusReportConsolidated.prototype.showEdit = function(d_id, d_name, d_country) {
    this.showAddScreen();
    Domain_name.val(d_name);
    Domain_id.val(d_id);
    this._country_ids = d_country;
    this.fetchCountryMultiselect();
};

StatusReportConsolidated.prototype.changeStatus = function(d_id, status) {
    mirror.changeDomainStatus(d_id, status, function(error, response) {
        if (error == null) {
            t_this.showList();
        } else {
            t_this.possibleFailures(error);
        }
    });
};

StatusReportConsolidated.prototype.validate = function() {
    var checkLength = domainValidate();
    if (checkLength) {
        if (Domain_name.val().trim().length == 0) {
            //this.displayMessage(msg.domainname_required);
            this.displayMessage("domainname_required");
        } else {
            this.displayMessage('');
            return true;
        }
    }
};

function DomainValidate() {
    if (MultiSelect_Country.val() == null) {
        //displayMessage(msg.country_required);
        displayMessage("country_required");
        MultiSelect_Country.focus();
        return false;
    }
    if (Domain_name.val().trim().length == 0) {
        //displayMessage(msg.domainname_required);
        displayMessage("domainname_required");
        Domain_name.focus();
        return false;
    } else {
        validateMaxLength('domainname', Domain_name.val(), "Domain name");
    }
    return true;
}

StatusReportConsolidated.prototype.submitProcess = function() {
    d_id = parseInt(Domain_id.val());
    name = Domain_name.val().trim();
    c_ids = MultiSelect_Country.val().map(Number);
    DomainValidate();
    t_this = this;
    if (Domain_id.val() == '') {
        mirror.saveDomain(name, c_ids, function(error, response) {
            if (error == null) {
                t_this.displayMessage(error);
                displaySuccessMessage(message.save_success);
                t_this.showList();
            } else {
                t_this.displayMessage(error);
            }
        });
    } else {
        mirror.updateDomain(d_id, name, c_ids, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.update_success);
                t_this.showList();
            } else {
                t_this.displayMessage(error);
            }
        });
    }
};

function chkbox_select(item, id, name, active) {
    a_klass = Country_li_active;
    eveClick = "";
    li_string = ''
    if (active == true) {
        li_string = '<li id="' + id + '" class="' + a_klass + '" onclick=list_click(this) >' + name + '</li>';
    } else {
        li_string = '<li id="' + id + '" onclick=list_click(this) >' + name + '</li>';
    }
    return li_string;
}

function list_click(element) {
    country_class = 'active_selectbox_country';

    klass = $(element).attr('class');
    if (klass == country_class) {
        $(element).removeClass(country_class);
        REPORT._country_ids.splice(REPORT._country_ids.indexOf(parseInt(element.id)));
    } else {
        $(element).addClass(country_class);
        REPORT._country_ids.push(parseInt(element.id));
    }
    Country.val(REPORT._country_ids.length + ' Selected');
}

function key_search(mainList) {
    d_key = SearchDomain.val().toLowerCase();
    c_key = SearchCountry.val().toLowerCase();
    d_status = $('.search-status-li.active').attr('value');
    var fList = [];
    for (var entity in mainList) {
        dName = mainList[entity].domain_name;
        cnames = mainList[entity].c_names;
        dStatus = mainList[entity].is_active;

        var flg = false;

        if (c_key.length == 0) {
            flg = true;
        } else {
            for (var c in cnames) {
                if (~cnames[c].toLowerCase().indexOf(c_key)) {
                    flg = true;
                    continue;
                }
            }
        }

        if ((~dName.toLowerCase().indexOf(d_key)) && flg == true) {
            if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)) {
                fList.push(mainList[entity]);
            }
        }
    }
    return fList
}

REPORT = new StatusReportConsolidated();

$(document).ready(function() {
    PageControls();
    REPORT.loadFilter();
});
