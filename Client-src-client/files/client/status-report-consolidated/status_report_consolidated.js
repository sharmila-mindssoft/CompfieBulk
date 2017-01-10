var country = $("#country");
var legalEntity = $("#legal-entity");
var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");
var unit = $("#unit");
var unitId = $("#unit-id");
var acUnit = $("#ac-unit");
var act = $("#act");
var actId = $("#act-id");
var acAct = $("#ac-act");
var complianceTask = $("#compliance-task");
var complianceTaskId = $("#compliance-task-id");
var acComplianceTask = $("#ac-compliance-task");
var complianceFrequency = $("#compliance-frequency");
var userType = $("#user-type");
var user = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");
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

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, 1];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        if (unitList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "u_name", "u_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        if (actList.length == 0)
            displayMessage(message.act_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act_name", "act_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        if (complianceTaskList.length == 0)
            displayMessage(message.complianceTask_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "c_task", "c_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    user.keyup(function(e) {
        var text_val = user.val().trim();
        var userList = REPORT._users;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUser, userId, text_val, userList, "u_name", "u_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        //if (REPORT.validate()) {
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues()
        //}
    });

}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    REPORT.fetchUnitList(val[0]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    REPORT.fetchActList(val[0]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    REPORT.fetchComplianceaskList(val[0]);
}

onComplianceTaskAutoCompleteSuccess = function(REPORT, val) {
    complianceTask.val(val[1]);
    complianceTaskId.val(val[0]);
    complianceTask.focus();
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    user.val(val[1]);
    userId.val(val[0]);
    user.focus();
}

StatusReportConsolidated = function() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._frequencies = [];
    this._user_type = [];
    this._users = [];
    this._compliance_task_status = [];
    this._service_providers = [];
}

StatusReportConsolidated.prototype.loadSearch = function() {
    reportView.hide();
    country.empty();
    legalEntity.empty();
    domain.val('');
    domainId.val('');
    unit.val('');
    unitId.val('');
    act.val('');
    actId.val('');
    complianceTask.val('');
    complianceTaskId.val('');
    complianceFrequency.empty();
    userType.empty();
    user.val('');
    userId.val('');
    fromDate.val('');
    toDate.val('');
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india"},{"c_id":1,"c_name":"srilanka"}],"entities":[{"le_id":1,"le_name":"RG Legal Entity"},{"le_id":2,"le_name":"ABC Legal Entity"}],"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":2,"is_active":true}],"frequencies":[{"f_id":1,"f_name":"Periodical"},{"f_id":2,"f_name":"Review"},{"f_id":3,"f_name":"Flexi Review"},{"f_id":4,"f_name":"One Time"}],"user_type":[{"user_type_id":1,"user_type_name":"Assignee"},{"user_type_id":2,"user_type_name":"Concurrence"},{"user_type_id":3,"user_type_name":"Approval"}],"compliance_task_status":[{"comp_task_status_id":1,"comp_task_status":"Complied"},{"comp_task_status_id":2,"comp_task_status":"Delayed Compliances"},{"comp_task_status_id":3,"comp_task_status":"Inprogress"},{"comp_task_status_id":4,"comp_task_status":"Not Complied"}],"service_providers":[{"s_p_id":1,"s_p_name":"String","s_p_shrot":"short"}],"users":[{"u_id":1,"u_name":"Siva ","is_active":true},{"u_id":2,"u_name":"Hari","is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._entities = object.entities;
    t_this._domains = object.domains;
    t_this._frequencies = object.frequencies;
    t_this._userType = object.user_type;
    t_this._users = object.users;
    t_this._complianceTaskStatus = object.compliance_task_status;
    t_this._serviceProviders = object.service_providers;

    t_this.renderCountriesList(t_this._countries);
    t_this.renderLegalEntityList(t_this._entities);
    t_this.renderComplianceFrequencyList(t_this._frequencies);
    t_this.renderUserTypeList(t_this._userType);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.fetchUnitList = function() {
    t_this = this;
    var jsondata = '{"units":[{"u_id":1,"u_name":"RG Madurai Unit","u_code":"RG1034","address":"12 RJ Complex, Main road, Madurai, 625022","d_id":1,"is_active":true},{"u_id":2,"u_name":"RG Dindugal Unit","u_code":"RG1035","address":"10 RG Complex, Main road, Dindugal, 623020","d_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._units = object.units;
};

StatusReportConsolidated.prototype.fetchActList = function() {
    t_this = this;
    var jsondata = '{"acts":[{"act_id":1,"act_name":"The Batteries Act","u_id":1,"is_active":true},{"act_id":2,"act_name":"Indian Partnership Act, 1932","u_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._acts = object.acts;
};

StatusReportConsolidated.prototype.fetchComplianceaskList = function() {
    t_this = this;
    var jsondata = '{"compliance_task":[{"c_id":1,"c_task":"FORM I - Half yearly returns Submission","act_id":1,"is_active":true},{"c_id":2,"c_task":"FORM II - Registration","act_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._compliance_task = object.compliance_task;
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

StatusReportConsolidated.prototype.validate = function() {
    if (domain) {
        if (isNotEmpty(domain, message.domain_required) == false)
            return false;
        else if (isLengthMinMax(domain, 1, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }
    if (unit) {
        if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 50, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
            return false;
    }
    if (complianceTask) {
        if (isLengthMinMax(complianceTask, 0, 50, message.complianceTask_max) == false)
            return false;
        else if (isCommonName(complianceTask, message.complianceTask_str) == false)
            return false;
    }
    if (user) {
        if (isLengthMinMax(user, 0, 50, message.user_max) == false)
            return false;
        else if (isCommonName(user, message.user_str) == false)
            return false;
    }
    if (fromDate) {
        if (isNotEmpty(fromDate, message.fromdate_required) == false)
            return false;
    }
    if (toDate) {
        if (isNotEmpty(toDate, message.todate_required) == false)
            return false;
    }
    return true;
};

showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
    });
}

StatusReportConsolidated.prototype.fetchReportValues = function() {
    t_this = this;
    var jsondata = '{"GetStatusReportConslidatedSuccess":{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance-task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1004 - Suresh","activity-status":"Approved","activity-date":"20-Aug-2016","doc_list":[],"completion-date":"18-Aug-2016","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance-task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1002 - Rajkumar","activity-status":"Submitted","activity-date":"18-Aug-2016","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8090/report/status-consolidated"}],"completion-date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance-task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1004 - Suresh","activity-status":"Pending","activity-date":"","doc_list":[],"completion-date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance-task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1002 - Rajkumar","activity-status":"Submitted","activity-date":"19-Aug-2016","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8090/report/status-consolidated"}],"completion-date":"","com_id":1,"f_id":1}]}}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._entities = object.entities;
    t_this._domains = object.domains;
    t_this._frequencies = object.frequencies;
    t_this._userType = object.user_type;
    t_this._users = object.users;
    t_this._complianceTaskStatus = object.compliance_task_status;
    t_this._serviceProviders = object.service_providers;
};

StatusReportConsolidated.prototype.loadReportValues = function() {
    Domain_name.focus();
};
























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
    } else if (error == 'InvaliddomainId') {
        //this.displayMessage(msg.invalid_domainId);
        this.displayMessage("invalid domainId");
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


StatusReportConsolidated.prototype.submitProcess = function() {
    d_id = parseInt(Domain_id.val());
    name = Domain_name.val().trim();
    c_ids = MultiSelect_Country.val().map(Number);
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
    REPORT.loadSearch();
});
