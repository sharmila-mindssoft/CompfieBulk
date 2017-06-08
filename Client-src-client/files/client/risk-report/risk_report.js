var CountryNameLabel = $(".country-name");
var CountryNameAC = $(".country-name-ac");

var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal-entity");
var LegalEntityId = $("#legal-entity-id");
var ACLegalEntity = $("#ac-legal-entity");

var BusinessGroupNameLabel = $(".business-group-name");
var BusinessGroupNameAC = $(".business-group-name-ac");

var BusinessGroupName = $("#business_group_name");
var BusinessGroupId = $("#business_group_id");
var ACBusinessGroup = $("#ac-business-group");

var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");

var DivisionName = $("#division");
var DivisionId = $("#division-id");
var ACDivision = $("#ac-division");

var CategoryName = $("#category");
var CategoryId = $("#category-id");
var ACCategory = $("#ac-category");

var unit = $("#unit");
var unitId = $("#unit-id");
var acUnit = $("#ac-unit");

var act = $("#act");
var actId = $("#act-id");
var acAct = $("#ac-act");

var complianceTask = $("#compliance-task");

var complianceTaskStatus = $("#compliance-task-status");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var _page_limit = 25;
var csv = false;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function PageControls() {
    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._entities;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.country_required);
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    BusinessGroupName.keyup(function(e) {
        var text_val = BusinessGroupName.val().trim();
        var bgList = REPORT._entities;
        if (bgList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, ACBusinessGroup, BusinessGroupId, text_val, bgList, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        if (BusinessGroupId.val() != '') {
            condition_fields.push("bg_id");
            condition_values.push(BusinessGroupId.val());
        }
        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    DivisionName.keyup(function(e) {
        var text_val = DivisionName.val().trim();
        var divisionList = REPORT._divisions;
        commonAutoComplete(e, ACDivision, DivisionId, text_val, divisionList, "division_name", "division_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        });
    });

    CategoryName.keyup(function(e) {
        var text_val = CategoryName.val().trim();
        var categoryList = REPORT._categories;
        if (DivisionId.val() != '') {
            condition_fields = ["division_id"];
            condition_values = [DivisionId.val()];
        }
        commonAutoComplete(e, ACCategory, CategoryId, text_val, categoryList, "category_name", "category_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
        });
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        var condition_fields = [];
        var condition_values = [];
        if (DivisionId.val() != '') {
            condition_fields = ["division_id"];
            condition_values = [DivisionId.val()];
        }
        if (CategoryId.val() != '') {
            if (condition_fields != "undefined") {
                condition_fields.push("category_id");
                condition_values.push(CategoryId.val());
            } else {
                condition_fields = ["category_id"];
                condition_values = [CategoryId.val()];
            }

        }
        for (var i = 0; i < REPORT._units.length; i++) {
            unitList.push({
                "division_id": REPORT._units[i].division_id,
                "category_id": REPORT._units[i].category_id,
                "unit_id": REPORT._units[i].unit_id,
                "unit_name": REPORT._units[i].unit_code + " - " + REPORT._units[i].unit_name
            });
        }
        if (condition_fields.length > 0) {
            commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
                onUnitAutoCompleteSuccess(REPORT, val);
            }, condition_fields, condition_values);
        } else {
            commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
                onUnitAutoCompleteSuccess(REPORT, val);
            });
        }

    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = [];
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];
        actList = REPORT._acts;
        if (unitId.val() != "") {
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        if (actList.length == 0)
            displayMessage(message.act_required);
        commonAutoComplete(e, acAct, actId, text_val, actList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            this._on_current_page = 1;
            this._sno = 0;
            this._total_record = 0;
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            csv = true;
            REPORT.exportReportValues();
        }
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        this._on_current_page = 1;
        this._sno = 0;
        createPageView(t_this._total_record);
        csv = false;
        REPORT.fetchReportValues();
    });

}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onCountryAutoCompleteSuccess = function(REPORT, val) {
    country.val(val[1]);
    countryId.val(val[0]);
    country.focus();
    clearElement([BusinessGroupName, BusinessGroupId, LegalEntityName, LegalEntityId, domain, domainId, DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, act, actId, complianceTask]);
}

onBusinessGroupAutoCompleteSuccess = function(REPORT, val) {
    BusinessGroupName.val(val[1]);
    BusinessGroupId.val(val[0]);
    BusinessGroupName.focus();
    clearElement([LegalEntityName, LegalEntityId, domain, domainId, DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, act, actId, complianceTask]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([domain, domainId, DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, act, actId, complianceTask]);
    REPORT.fetchDomainList(countryId.val(), BusinessGroupId.val(), val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, act, actId, complianceTask]);
}

onDivisionAutoCompleteSuccess = function(REPORT, val) {
    DivisionName.val(val[1]);
    DivisionId.val(val[0]);
    DivisionName.focus();
    clearElement([CategoryId, CategoryName, unit, unitId, act, actId, complianceTask]);
}

onCategoryAutoCompleteSuccess = function(REPORT, val) {
    CategoryName.val(val[1]);
    CategoryId.val(val[0]);
    CategoryName.focus();
    clearElement([unit, unitId, act, actId, complianceTask]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask]);
}

RiskReport = function() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._divisions = [];
    this._categories = [];
    this._units = [];
    this._acts = [];
    this._compliance_task_status = [];
    this._report_data = [];
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._RiskCompliances = [];
}

RiskReport.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('');
    BusinessGroupName.val('');
    BusinessGroupId.val('');
    LegalEntityName.val('');
    LegalEntityId.val('');
    domain.val('');
    domainId.val('');
    DivisionName.val('');
    DivisionId.val('');
    CategoryId.val('');
    CategoryName.val('');
    unit.val('');
    unitId.val('');
    act.val('');
    actId.val('');
    complianceTask.val('');
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

RiskReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

RiskReport.prototype.loadEntityDetails = function() {
    t_this = this;
    if (t_this._entities.length > 1) {
        CountryNameAC.show();
        CountryNameLabel.hide();
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
        BusinessGroupNameLabel.hide();
        BusinessGroupNameAC.show();
    } else {
        c_name = t_this._entities[0]["c_name"];
        c_id = t_this._entities[0]["c_id"];
        CountryNameLabel.show();
        CountryNameAC.hide();
        CountryNameLabel.text(c_name);
        country.val(c_name);
        countryId.val(c_id);
        le_name = t_this._entities[0]["le_name"];
        le_id = t_this._entities[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(le_name);
        LegalEntityName.val(le_name);
        LegalEntityId.val(le_id);
        var BG_NAME = '-';
        if (t_this._entities[0]["bg_name"] != null) {
            BG_NAME = t_this._entities[0]["bg_name"];
        }
        var BG_ID = '';
        if (t_this._entities[0]["bg_id"] != null) {
            BG_ID = t_this._entities[0]["bg_id"];
        }
        BusinessGroupNameLabel.show();
        BusinessGroupNameAC.hide();
        BusinessGroupNameLabel.text(BG_NAME);
        BusinessGroupName.val(BG_NAME);
        BusinessGroupId.val(BG_ID);
        REPORT.fetchDomainList(c_id, BG_ID, le_id);
    }
    hideLoader();
};

RiskReport.prototype.fetchDomainList = function(c_id, bg_id, le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getRiskReportFilters(parseInt(c_id), parseInt(bg_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._domains = response.domains;
            t_this._divisions = response.divisions;
            t_this._categories = response.categories;
            t_this._units = response.units_list;
            t_this._acts = response.act_legal_entity;
            t_this._compliance_task_status = response.compliance_task_status;
            REPORT.renderComplianceTaskStatusList(t_this._compliance_task_status);
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

RiskReport.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.task_status_id + '"> ' + e.task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

RiskReport.prototype.validate = function() {
    if (country) {
        if (isNotEmpty(country, message.country_required) == false)
            return false;
        else if (isLengthMinMax(country, 1, 50, message.country_max) == false)
            return false;
        else if (isCommonName(country, message.country_str) == false)
            return false;
    }
    if (countryId.val() == "") {
        displayMessage(message.country_required);
        country.focus();
        return false;
    }
    if (BusinessGroupName) {
        if (isLengthMinMax(BusinessGroupName, 0, 50, message.businessgroup_max) == false)
            return false;
        else if (isCommonName(BusinessGroupName, message.businessgroup_str) == false)
            return false;
    }

    if (LegalEntityName) {
        if (isNotEmpty(LegalEntityName, message.legalentity_required) == false)
            return false;
        else if (isLengthMinMax(LegalEntityName, 1, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(LegalEntityName, message.legalentity_str) == false)
            return false;
    }
    if (LegalEntityId.val() == "") {
        displayMessage(message.legalentity_required);
        LegalEntityName.focus();
        return false;
    }
    if (domain) {
        if (isNotEmpty(domain, message.domain_required) == false)
            return false;
        else if (isLengthMinMax(domain, 1, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }
    if (domainId.val() == "") {
        displayMessage(message.domain_required);
        domain.focus();
        return false;
    }
    if (DivisionName) {
        if (isLengthMinMax(DivisionName, 0, 50, message.division_max) == false)
            return false;
        else if (isCommonName(DivisionName, message.division_str) == false)
            return false;
    }
    if (CategoryName) {
        if (isLengthMinMax(CategoryName, 0, 50, message.category_max) == false)
            return false;
        else if (isCommonName(CategoryName, message.category_str) == false)
            return false;
    }
    if (unit) {
        if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 500, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
            return false;
    }
    if (complianceTask) {
        if (isLengthMinMax(complianceTask, 0, 150, message.complianceTask_max) == false)
            return false;
        else if (isCommonName(complianceTask, message.complianceTask_str) == false)
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

RiskReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    bg_id = BusinessGroupId.val();
    if (bg_id == "")
        bg_id = 0;
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    div_id = DivisionId.val();
    if (div_id == "")
        div_id = 0;
    cg_id = CategoryId.val();
    if (cg_id == "")
        cg_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compliance_task = complianceTask.val().trim();
    if (compliance_task == "")
        compliance_task = null;
    c_t_s = $('#compliance-task-status option:selected').text().trim();
    check_count = false;
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0;
        check_count = true;
    } else {
        this._sno = (this._on_current_page - 1) * _page_limit;
        check_count;
        check_count = false;
    }
    console.log(this._sno, _page_limit)
    displayLoader();
    client_mirror.getRiskReportData(
        parseInt(c_id), parseInt(bg_id), parseInt(le_id), parseInt(d_id), parseInt(div_id), parseInt(cg_id),
        parseInt(unit_id), stat_map, compliance_task, c_t_s, csv, this._sno, _page_limit,
        function(error, response) {
            console.log(error, response)
            if (error == null) {
                t_this._RiskCompliances = response.risk_report;
                if (check_count == true)
                    t_this._total_record = response.total_count;
                if (response.risk_report.length == 0) {
                    hidePageView();
                    hidePagePan();
                    //Export_btn.hide();
                    PaginationView.hide();
                    t_this.showReportValues();
                } else {
                    if (t_this._sno == 0) {
                        createPageView(t_this._total_record);
                    }
                    //Export_btn.show();
                    PaginationView.show();
                    t_this.showReportValues();
                }
                hideLoader();
            } else {
                t_this.possibleFailures(error);
                hideLoader();
            }
        });
};

RiskReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._RiskCompliances;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.dom-header').text(domain.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var unitname = "";
    var actname = "";
    var complianceHistoryId = null;
    var is_null = true;
    var fileList = [];
    showFrom = t_this._sno + 1;
    unit_names = [];
    act_names = [];
    for (var i = 0; i < data.length; i++) {
        var occur = -1;
        for (var j = 0; j < unit_names.length; j++) {
            if (data[i].unit_name == unit_names[j]) {
                occur = 1;
                break;
            }
        }
        if (occur < 0) {
            unit_names.push(data[i].unit_name);
        }
    }
    for (var i = 0; i < data.length; i++) {
        var occur = -1;
        for (var j = 0; j < act_names.length; j++) {
            if (data[i].statutory_mapping == act_names[j]) {
                occur = 1;
                break;
            }
        }
        if (occur < 0) {
            act_names.push(data[i].statutory_mapping);
        }
    }

    var u_count = 1;
    var sub_cnt = 0;

    for (var i = 0; i < unit_names.length; i++) {
        u_count = 1;
        var actname = "";
        for (var sm = 0; sm < act_names.length; sm++) {
            s_count = 1;
            actname = act_names[sm];
            $.each(data, function(k, v) {
                is_null = false;
                if (v.logo_url != null)
                    clientLogo.attr("src", v.logo_url);
                else
                    clientLogo.remove();
                if (v.unit_name == unit_names[i]) {
                    // unit name cloning
                    if (u_count == 1) {
                        var cloneone = $('#template #report-table .row-one').clone();
                        $('.unit-name', cloneone).text(v.unit_name);
                        reportTableTbody.append(cloneone);
                        u_count = u_count + 1;
                    }
                    if (actname == v.statutory_mapping) {
                        if (s_count == 1) {
                            var clonetwo = $('#template #report-table .row-two').clone();
                            $('.act-name', clonetwo).text(v.statutory_mapping);
                            reportTableTbody.append(clonetwo);
                            actname = v.statutory_mapping;
                            s_count = s_count + 1;
                        }

                        var clonethree = $('#template #report-table .row-three').clone();
                        t_this._sno += 1;
                        $('.sno', clonethree).text(t_this._sno);
                        $('.compliance-task', clonethree).text(v.compliance_task);
                        $('.frequency', clonethree).text(v.frequency_name);
                        $('.admin-incharge', clonethree).text(v.admin_incharge);
                        var ass_name = null;
                        if (v.assignee_name != null && v.assignee_name.indexOf("-") >= 0) {
                            ass_name = v.assignee_name.split("-")[1];
                        }
                        $('.assignee', clonethree).text(ass_name);
                        $('.compliance-task-status', clonethree).text(v.task_status);
                        $('.penal-consq', clonethree).text(v.penal_consequences);
                        // $('.view-data', clonethree).html("View");
                        if (v.assignee_name != null) {
                            $('.view-data a', clonethree).on('click', function() {
                                displayPopup(
                                    v.start_date, v.due_date, v.assignee_name, v.assigned_on, v.concurrer_name,
                                    v.concurred_on, v.approver_name, v.approved_on, v.comp_remarks, 1
                                );
                            });
                        } else {
                            if (v.assignee_name == null) {
                                $('.view-data a', clonethree).on('click', function() {
                                    displayPopup(
                                        v.start_date, v.due_date, v.assignee_name, v.assigned_on, v.concurrer_name,
                                        v.concurred_on, v.approver_name, v.approved_on, v.comp_remarks, 0
                                    );
                                });
                            }
                        }

                        if (v.document_name != null && v.document_name != "" && v.document_name != "-") {
                            var files = v.document_name.split(",");
                            $.each(files, function(k1) {
                                $('.uploaded-document', clonethree).append(
                                    $('<a/>')
                                    .addClass("c-pointer")
                                    .attr("onClick", "downloadFile("+LegalEntityId.val()+", "+countryId.val()+", "+domainId.val()+", "+v.unit_id+", '"+v.start_date+"', '"+files[k1]+"')")
                                    .text(files[k1]),
                                    $('<br/>')
                                );
                            });
                        } else {
                            $('.uploaded-document', clonethree).html("-");
                        }

                        reportTableTbody.append(clonethree);
                        j = j + 1;
                    }
                }
            });
        }
    }

    if (is_null == true) {
        //a_page.hidePagePan();
        reportTableTbody.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        reportTableTbody.append(clone4);
    } else {
        showPagePan(showFrom, t_this._sno, t_this._total_record);
    }
};

downloadFile = function(le_id, c_id, d_id, u_id, date, file) {
    client_mirror.downloadTaskFile(parseInt(le_id), parseInt(c_id), parseInt(d_id), parseInt(u_id), date, file);
};

function download_url(doc_url) {
    if (doc_url != null) {
        window.open(doc_url, '_blank');
    }
}

$('.close').click(function() {
    $('.overlay').css('visibility', 'hidden');
    $('.overlay').css('opacity', '0');
});

function displayPopup(
    start_date, due_date, assignee_name, assigned_on, concurrer_name,
    concurred_on, approver_name, approved_on, comp_remarks, record_cnt
) {
    if (record_cnt == 0) {
        $('.overlay').css('visibility', 'visible');
        $('.overlay').css('opacity', '1');
        $('.popup-list').find('tr').remove();
        $('.empty').show();
        $('.not-empty').hide();

        Custombox.open({
            target: '#custom-modal',
            effect: 'contentscale',
            complete: function() {
                isAuthenticate = false;
            }
        });
    } else {
        $('.not-empty').show();
        $('.overlay').css('visibility', 'visible');
        $('.overlay').css('opacity', '1');
        $('.popup-list').find('tr').remove();
        $('.empty').hide();
        $('.start-date').html(start_date);
        $('.due-date').html(due_date);
        if (assigned_on == null)
            assigned_on = "-"
        if (assignee_name == null)
            assignee_name = "-"
        $('.assignee-name').html(assignee_name + "<br>" + assigned_on);
        if (concurred_on == null)
            concurred_on = "-"
        if (concurrer_name == null)
            concurrer_name = "-"
        $('.concurrer-name').html(concurrer_name + "<br>" + concurred_on);
        if (approved_on == null)
            approved_on = "-"
        if (approver_name == null)
            approver_name = "-"
        $('.approver-name').html(approver_name + "<br>" + approved_on);
        $('.compl-remarks').html(comp_remarks);

        Custombox.open({
            target: '#custom-modal',
            effect: 'contentscale',
            complete: function() {
                isAuthenticate = false;
            }
        });
    }

}

RiskReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    bg_id = BusinessGroupId.val();
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    div_id = DivisionId.val();
    if (div_id == "")
        div_id = 0;
    cg_id = CategoryId.val();
    if (cg_id == "")
        cg_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compliance_task = complianceTask.val().trim();
    if (compliance_task == "")
        compliance_task = null;
    c_t_s = $('#compliance-task-status option:selected').text().trim();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0
    } else {
        this._sno = (this._on_current_page - 1) * _page_limit;
    }
    displayLoader();
    client_mirror.getRiskReportData(
        parseInt(c_id), parseInt(bg_id), parseInt(le_id), parseInt(d_id), parseInt(div_id), parseInt(cg_id),
        parseInt(unit_id), stat_map, compliance_task, c_t_s, csv, this._sno, _page_limit,
        function(error, response) {
            console.log(error, response)
            if (error == null) {
                hideLoader();
                if (csv) {
                    document_url = response.link;
                    $(location).attr('href', document_url);
                }
            } else {
                t_this.possibleFailures(error);
                hideLoader();
            }
        });
};

RiskReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage(message.domainname_exists);
    } else if (error == "ExportToCSVEmpty") {
        displayMessage(message.empty_export);
    } else {
        displayMessage(error);
    }
};

// Pagination Functions - begins

hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

createPageView = function(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            console.log(cPage, REPORT._on_current_page)
            if (parseInt(REPORT._on_current_page) != cPage) {
                REPORT._on_current_page = cPage;
                REPORT.fetchReportValues();
            }
        }
    });
};
showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

// Pagination Ends

REPORT = new RiskReport();

$(document).ready(function() {
    displayLoader();
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});