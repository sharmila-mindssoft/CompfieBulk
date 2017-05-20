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

var division = $("#division");
var divisionId = $("#division-id");
var acDivision = $("#ac-division");

var category = $("#category");
var categoryId = $("#category-id");
var acCategory = $("#ac-category");

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
var complianceTaskStatus = $("#compliance-task-status");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
var legalEntityName = $("#legal-entity-name");
var countryName = $("#country-name");
var domainName = $("#domain-name");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var f_count = 1;
var LOGO = null;

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

    businessGroup.keyup(function(e) {
        var text_val = businessGroup.val().trim();
        var businessGroupList = REPORT._entities;
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, acBusinessGroup, businessGroupId, text_val, businessGroupList, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.legalentity_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        if (businessGroupId.val() != '') {
            condition_fields.push("bg_id");
            condition_values.push(businessGroupId.val());
        }
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        if (domainList.length == 0 && text_val != '')
            displayMessage(message.domain_required);
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, legalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    division.keyup(function(e) {
        var text_val = division.val().trim();
        var divisionList = REPORT._divisions;
        var condition_fields = ["le_id"];
        var condition_values = [legalEntityId.val()];
        commonAutoComplete(e, acDivision, divisionId, text_val, divisionList, "div_name", "div_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    category.keyup(function(e) {
        var text_val = category.val().trim();
        var categoryList = REPORT._categorys;
        var condition_fields = ["div_id", "le_id"];
        var condition_values = [divisionId.val(), legalEntityId.val()];
        commonAutoComplete(e, acCategory, categoryId, text_val, categoryList, "cat_name", "cat_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        var condition_fields = ["d_ids"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act", "act", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "c_task", "compliance_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        on_current_page = 1;
        processSubmit(false, true);
    });

    exportButton.click(function() {
        processSubmit(true, false);
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        f_count = 1;
        on_current_page = 1;
        createPageView(t_this._total_count);
        processSubmit(false, false);
    });
}

processSubmit = function(csv, count_qry) {
    if (REPORT.validate()) {
        REPORT.fetchReportValues(csv, count_qry);
    }
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
    clearElement([businessGroup, businessGroupId, legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onBusinessGroupAutoCompleteSuccess = function(REPORT, val) {
    businessGroup.val(val[1]);
    businessGroupId.val(val[0]);
    businessGroup.focus();
    clearElement([legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
    clearElement([domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchDomainList(val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    //REPORT.fetchDivisionList(val[0]);
}

onDivisionAutoCompleteSuccess = function(REPORT, val) {
    division.val(val[1]);
    divisionId.val(val[0]);
    division.focus();
    clearElement([category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    //REPORT.fetchCategoryList(val[0], domainId.val());
}

onCategoryAutoCompleteSuccess = function(REPORT, val) {
    category.val(val[1]);
    categoryId.val(val[0]);
    category.focus();
    clearElement([unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, complianceTaskId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, complianceTaskId]);
}

onComplianceTaskAutoCompleteSuccess = function(REPORT, val) {
    complianceTask.val(val[1]);
    complianceTaskId.val(val[0]);
    complianceTask.focus();
}

StatutorySettingsUnitWise = function() {
    this._entities = [];
    this._domains = [];
    this._divisions = [];
    this._categorys = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._frequencies = [];
    this._compliance_task_status = [];
    this._report_data = [];
    this._total_count = [];
}

StatutorySettingsUnitWise.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, businessGroup, businessGroupId, legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    complianceFrequency.empty();
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

StatutorySettingsUnitWise.prototype.fetchSearchList = function() {
    t_this = this;

    /*var jsondata = '[{"c_id":1,"le_name":"LG Legal Entity","le_id":1,"bg_name":"LG Business Group","bg_id":1,"c_name":"India"},{"c_id":2,"le_name":"LG Legal Entity Two","le_id":3,"bg_name":null,"bg_id":null,"c_name":"Sri Lanka"}]';
    var object = jQuery.parseJSON(jsondata);
    t_this._entities = object;*/
    t_this._entities = client_mirror.getSelectedLegalEntity();
    t_this._complianceTaskStatus = ComplianceTaskStatuses; // common-functions.js
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatutorySettingsUnitWise.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getStatutorySettingsUnitWiseFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.units;
            t_this._acts = response.acts;
            t_this._compliance_task = response.compliances;
            t_this._divisions = response.div_infos;
            t_this._categorys = response.cat_infos;
            t_this._frequencies = response.compliance_frequency;
            t_this.renderComplianceFrequencyList(t_this._frequencies);
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};


StatutorySettingsUnitWise.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.frequency_id + '"> ' + e.frequency + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

StatutorySettingsUnitWise.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="All">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.name + '"> ' + e.name + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

StatutorySettingsUnitWise.prototype.validate = function() {
    if (country) {
        if (isNotEmpty(country, message.country_required) == false)
            return false;
        else if (isLengthMinMax(country, 1, 50, message.country_max) == false)
            return false;
        else if (isCommonName(country, message.country_str) == false)
            return false;
    }
    if (businessGroup) {
        if (isLengthMinMax(businessGroup, 0, 50, message.businessgroup_max) == false)
            return false;
        else if (isCommonName(businessGroup, message.businessgroup_str) == false)
            return false;
    }
    if (legalEntity) {
        if (isNotEmpty(legalEntity, message.legalentity_required) == false)
            return false;
        else if (isLengthMinMax(legalEntity, 1, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(legalEntity, message.legalentity_str) == false)
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
    if (division) {
        if (isLengthMinMax(division, 0, 50, message.division_max) == false)
            return false;
        else if (isCommonName(division, message.division_str) == false)
            return false;
    }
    if (category) {
        if (isLengthMinMax(category, 0, 50, message.category_max) == false)
            return false;
        else if (isCommonName(category, message.category_str) == false)
            return false;
    }
    if (unit) {
        if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 100, message.act_max) == false)
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

StatutorySettingsUnitWise.prototype.fetchReportValues = function(csv, count_qry) {
    t_this = this;
    /*var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":1,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":2,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Annual Returns","frequency":"Periodical","due_date":"","task_status":"Assigned","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":3,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":4,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;*/

    var c_id = parseInt(countryId.val());
    var bg_id = parseInt(businessGroupId.val());
    if (!bg_id) bg_id = null
    var le_id = parseInt(legalEntityId.val());
    var d_id = parseInt(domainId.val());
    var div_id = parseInt(divisionId.val());
    if (!div_id) div_id = null
    var cat_id = parseInt(categoryId.val());
    if (!cat_id) cat_id = null
    var u_id = parseInt(unitId.val());
    if (!u_id) u_id = null
    var act = actId.val();
    if (!act) act = null
    var compliance_task_id = parseInt(complianceTaskId.val());
    if (!compliance_task_id) compliance_task_id = null
    var comp_fre_id = parseInt(complianceFrequency.val());
    var comp_task_status_id = complianceTaskStatus.val();

    var t_count = parseInt(on_current_page) * parseInt(ItemsPerPage.val());
    if (on_current_page == 1) { f_count = 1 } else { f_count = ((parseInt(on_current_page) - 1) * parseInt(ItemsPerPage.val())) + 1; }
    displayLoader();
    client_mirror.getStatutorySettingsUnitWise(c_id, bg_id, le_id, d_id, u_id, div_id, cat_id, act, compliance_task_id,
        comp_fre_id, comp_task_status_id, f_count, t_count, csv, count_qry,
        function(error, response) {
            if (error == null) {
                t_this._report_data = response.statutory_settings_unit_Wise_list;
                if (response.total_count != 0)
                    t_this._total_count = response.total_count;
                LOGO = response.logo_url;
                if (csv == false) {
                    reportView.show();
                    showAnimation(reportView);
                    REPORT.showReportValues();
                    if (f_count == 1)
                        createPageView(t_this._total_count);
                } else {
                    document_url = response.link;
                    if (document_url != null)
                        $(location).attr('href', document_url);
                    else
                        displayMessage(message.empty_export);
                }
            } else {
                t_this.possibleFailures(error);
            }
            hideLoader();
        });
};

StatutorySettingsUnitWise.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    if (LOGO != null)
        clientLogo.attr("src", LOGO);
    else
        clientLogo.remove();
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    var j = f_count;
    reportTableTbody.find('tr').remove();
    var unitId = "";
    var actname = "";
    var complianceId = "";
    var tree = "";
    var i = 0;
    if (data.length > 0) {
        $.each(data, function(k, v) {
            if (unitId != v.unit_id) {
                var cloneone = $('#template #report-table .row-one').clone();
                $('.unit-name', cloneone).text(v.unit);
                reportTableTbody.append(cloneone);
                unitId = v.unit_id;
            }

            if (actname != v.act_name) {
                var clonetwo = $('#template #report-table .row-two').clone();
                $('.act-name', clonetwo).text(v.act_name);
                reportTableTbody.append(clonetwo);
                actname = v.act_name;
            }
            if (complianceId != v.compliance_id) {
                i = i + 1;
                var clonethree = $('#template #report-table .row-three').clone();
                $('.sno', clonethree).text(j);
                $('.compliance-task', clonethree).text(v.compliance_task);
                $('.frequency', clonethree).text(v.frequency);
                $('.due-date', clonethree).text(v.due_date);
                $('.compliance-task-status', clonethree).text(v.task_status);
                /*if (v.doc_list.length > 0) {
                    $.each(v.doc_list, function(k1, v1) {
                        $('.uploaded-document a', clonethree).text(v1.doc_name).attr("href", v1.doc_url);
                    });
                } else {
                    $('.uploaded-document', clonethree).text('-');
                }*/
                if (v.document_name != "")
                    $('.uploaded-document', clonethree).text(v.document_name);
                else
                    $('.uploaded-document', clonethree).text('-');
                $(clonethree).attr("onClick", "treeShowHide('tree" + i + "')");
                $(clonethree).attr("onmouseover", "treePointer(this,'tree" + i + "')");
                $(clonethree).attr("id", "tree" + i);
                reportTableTbody.append(clonethree);
                complianceId = v.compliance_id;
                j = j + 1;
            } else {
                if (tree == v.compliance_id) {
                    var clonefive = $('#template #report-table .row-five').clone();
                    $('.user-name', clonefive).text(v.user_name);
                    $('.due-date', clonefive).text(v.due_date);
                    $('.tree' + i + ' .tree-body').append(clonefive);
                } else {
                    var clonefour = $('#template #report-table .row-four').clone();
                    $(clonefour).addClass("tree" + i);
                    $('.user-name', clonefour).text(v.user_name);
                    $('.due-date', clonefour).text(v.due_date);
                    reportTableTbody.append(clonefour);
                    tree = v.compliance_id
                }
                complianceId = v.compliance_id;
            }

        });
        showPagePan(f_count, j, t_this._total_count);
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
        hidePagePan();
    }
};

treeShowHide = function(tree) {
    if ($('.' + tree)) {
        if ($('.' + tree).is(":visible") == true)
            $('.' + tree).hide();
        else
            $('.' + tree).show();
    }
};

treePointer = function(ele,tree) {
    if($('.' + tree).length > 0) {
        $('#' + tree).css( 'cursor', 'pointer' );
    }
};

showPagePan = function(start, end, total) {
    var showText = 'Showing ' + start + ' to ' + (end - 1) + ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

hidePagePan = function() {
    CompliacneCount.text('');
    PaginationView.hide();
}

createPageView = function(total_records) {
    if (parseInt(total_records) > 0) {
        perPage = parseInt(ItemsPerPage.val());
        Pagination.empty();
        Pagination.removeData('twbs-pagination');
        Pagination.unbind('page');

        Pagination.twbsPagination({
            totalPages: Math.ceil(total_records / perPage),
            visiblePages: visiblePageCount,
            onPageClick: function(event, page) {
                cPage = parseInt(page);
                if (parseInt(on_current_page) != cPage) {
                    on_current_page = cPage;
                    processSubmit(false, false);
                }
            }
        });
    }
};

StatutorySettingsUnitWise.prototype.exportReportValues = function() {
    alert('export');
};

StatutorySettingsUnitWise.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

StatutorySettingsUnitWise.prototype.loadEntityDetails = function() {
    t_this = this;
    if (t_this._entities.length > 1) {
        country.parent().show();
        filterCountryName.hide();

        legalEntity.parent().show();
        filterLegalEntityName.hide();

        businessGroup.parent().show();
        filterBusinessGroupName.hide();
    } else {
        filterCountryName.show();
        filterCountryName.html(t_this._entities[0]["c_name"]);
        countryId.val(t_this._entities[0]["c_id"]);
        country.parent().hide();
        country.val(t_this._entities[0]["c_name"]);

        filterLegalEntityName.show();
        filterLegalEntityName.html(t_this._entities[0]["le_name"]);
        legalEntityId.val(t_this._entities[0]["le_id"]);
        legalEntity.parent().hide();
        legalEntity.val(t_this._entities[0]["le_name"]);

        var BG_NAME = '-';
        if (t_this._entities[0]["bg_name"] != null)
            BG_NAME = t_this._entities[0]["bg_name"];

        var BG_ID = '';
        if (t_this._entities[0]["bg_id"] != null)
            BG_ID = t_this._entities[0]["bg_id"];

        filterBusinessGroupName.show();
        filterBusinessGroupName.html(BG_NAME);
        businessGroupId.val(BG_ID);
        businessGroup.parent().hide();
        businessGroup.val(BG_NAME);

        REPORT.fetchDomainList(t_this._entities[0]["le_id"]);
    }
};

REPORT = new StatutorySettingsUnitWise();

$(document).ready(function() {
    PageControls();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
    loadItemsPerPage();
});
