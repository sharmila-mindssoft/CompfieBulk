/*
    Audittrail.js

    audittrailpage prototype will have
    initialize page controls,
    clear and show content and message,
    post callback,
    render page content

*/
Msg_pan = $('.error-message');
Spin_icon = $('.loading-indicator-spin');
From_date = $('#from-date');
To_date = $('#to-date');
User_id = $('#userid');
User = $('#user');
Form_id = $('#formid');
Form = $('#formname');
Group_id = $('#group-id');
Group = $('#groupsval');
BusinessGroup_id = $('#businessgroupid');
BusinessGroup = $('#businessgroupsval');
LegalEntity_id = $('#legalentityid');
LegalEntity = $('#legalentityval');
Division_id = $('#divisionid');
Division = $('#divisionval');
Div_Category_id = $('#categoryid');
Div_Category = $('#categoryval');
Unit_id = $('#unitid');
Unit = $('#unitval');
Category = $('#categoryName');
Show_btn = $("#show");
Export_btn = $("#export");

//var ACCountry = $('#ac-country');
//CountryVal = $('#countryval');
//Country = $('#country')

//Autocomplete variable declaration
var ACUser = $('#ac-user');
var ACForm = $('#ac-form');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDivision = $('#ac-division');
var ACDivCategory = $('#ac-category');
var ACUnit = $('#ac-unit');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var csv = false;

a_page = null;

function Auditpage() {
    this._sno = 0;
    this._userList = {};
    this._formList = {};
    this._categoryList = {};
    //this._countryList = {};
    this._auditData = {};
    this._clientUsers = {};
    this._clientForms = {};
    this._clients = {};
    this._businessGroups = {};
    this._legalEntities = {};
    this._divisions = {};
    this._divCategories = {};
    this._unitList = {};
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
}

/*Auditpage.prototype.displayMessage = function(message){
    Msg_pan.text(message);
    Msg_pan.show();
};*/
//To clear the messages
Auditpage.prototype.clearMessage = function() {
    Msg_pan.text('');
    Msg_pan.hide();
};

// To display the loader until the action happens
Auditpage.prototype.displayLoader = function() {
    Spin_icon.show();
};

// To Hide the Loader once done
Auditpage.prototype.hideLoader = function() {
    Spin_icon.hide();
};

// Resets the filter fields
Auditpage.prototype.resetFields = function() {
    $('.tbody-audittrail-list').find('tr').remove();
    $('.grid-table').hide();
    this._sno = 0;
    //CountryVal.val('');
    Form.val('');
    Form_id.val('');
    User.val('');
    User_id.val('');
    Group.val('');
    Group_id.val('');
    BusinessGroup.val('');
    BusinessGroup_id.val('');
    LegalEntity.val('');
    LegalEntity_id.val('');
    Division.val('');
    Division_id.val('');
    Div_Category_id.val('');
    Div_Category.val('');
    Unit_id.val('');
    Unit.val('');
    $('.group-name').hide();
    $('.bg-name').hide();
    $('.le-name').hide();
    $('.division-name').hide();
    $('.category-name').hide();
    $('.unit-name').hide();
    //this.clearMessage();
};

// To get the corresponding value
Auditpage.prototype.getValue = function(field_name, f_id) {
    if (field_name == "category") {
        cg_id = Category.val();
        if (cg_id == '') {
            return null;
        }
        return parseInt(cg_id);
    } else if (field_name == "group" && $('#categoryName option:selected').text() == "Client") {
        g_id = Group_id.val().trim();
        if (g_id == '') {
            return null;
        }
        return parseInt(g_id);
    } else if (field_name == "bg" && $('#categoryName option:selected').text() == "Client") {
        bg_id = BusinessGroup_id.val().trim();
        if (bg_id == '') {
            return null;
        }
        return parseInt(bg_id);
    } else if (field_name == "legalentity" && $('#categoryName option:selected').text() == "Client") {
        le_id = LegalEntity_id.val().trim();
        if (le_id == '') {
            return null;
        }
        return parseInt(le_id);
    } else if (field_name == "div" && $('#categoryName option:selected').text() == "Client") {
        div_id = Division_id.val().trim();
        if (div_id == '') {
            return null;
        }
        return parseInt(div_id);
    } else if (field_name == "divcg" && $('#categoryName option:selected').text() == "Client") {
        div_cg_id = Div_Category_id.val().trim();
        if (div_cg_id == '') {
            return null;
        }
        return parseInt(div_cg_id);
    } else if (field_name == "unit" && $('#categoryName option:selected').text() == "Client") {
        unit_id = Unit_id.val().trim();
        if (unit_id == '') {
            return null;
        }
        return parseInt(unit_id);
    } else if (field_name == "user") {
        u_id = User_id.val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    } else if (field_name == "form") {
        fr_id = Form_id.val().trim();
        if (fr_id == '') {
            return null;
        }
        return parseInt(fr_id);
    }
    /*else if (field_name == "country") {
        c_id = Country.val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }*/
    else if (field_name == "fromdate") {
        f_date = From_date.val().trim();
        return f_date;
    } else if (field_name == "todate") {
        t_date = To_date.val().trim();
        return t_date;
    } else if (field_name == "username") {
        if (f_id == 0 || f_id == "1" || f_id == "3") {
            return 'Administrator';
        } else {
            emp_name = null
            if ($('#categoryName option:selected').text() == "Client") {
                $.each(this._clientUsers, function(k, v) {
                    if (v.user_id == f_id) {
                        emp_name = v.employee_name;
                        return emp_name;
                    }
                });
            } else {
                $.each(this._userList, function(k, v) {
                    if (v.user_id == f_id) {
                        emp_name = v.employee_name;
                        return emp_name;
                    }
                });
            }

            return emp_name;
        }
    } else if (field_name == "usercategory") {
        if (f_id == 0) {
            return 'Administrator';
        } else {
            category_name = null
            if ($('#categoryName option:selected').text() == "Client") {
                $.each(this._clientUsers, function(k, v) {
                    if (v.user_category_id == f_id) {
                        category_name = v.user_category_name;
                        return category_name;
                    }
                });
            } else {
                $.each(this._categoryList, function(k, v) {
                    if (v.user_category_id == f_id) {
                        category_name = v.user_category_name;
                        return category_name;
                    }
                });
            }
            return category_name;
        }
    } else if (field_name == "categoryid") {
        if (f_id == 0) {
            return 'Client Admin';
        } else {
            category_id = null
            if ($('#categoryName option:selected').text() == "Client") {
                $.each(this._clientUsers, function(k, v) {
                    if (v.user_id == f_id) {
                        category_id = v.user_category_id;
                        return category_id;
                    }
                });
            }
            return category_id;
        }
    } else if (field_name == "formname") {
        frm_name = null;
        if ($('#categoryName option:selected').text() == "Client") {
            $.each(this._clientForms, function(k, v) {
                if (v.form_id == f_id) {
                    frm_name = v.form_name;
                    return frm_name;
                }
            });
        } else {
            $.each(this._formList, function(k, v) {
                if (v.form_id == f_id) {
                    frm_name = v.form_name;
                    return frm_name;
                }
            });
        }

        return frm_name;
    }
};

Auditpage.prototype.validateMandatory = function() {
    is_valid = true;
    if (this.getValue("category") == '' || this.getValue("category") == null) {
        displayMessage(message.catgname_required);
        is_valid = false;
    }
    /*else if (this.getValue("country") == '' || this.getValue("country") == null) {
        displayMessage(message.country_required);
        is_valid = false;
    }*/
    else if ((this.getValue("group") == '' || this.getValue("group") == null) && ($('#categoryName option:selected').text() == "Client")) {
        displayMessage(message.group_required);
        is_valid = false;
    } else if ((this.getValue("legalentity") == '' || this.getValue("legalentity") == null) && ($('#categoryName option:selected').text() == "Client")) {
        displayMessage(message.legalentity_required);
        is_valid = false;
    } else if (this.getValue("fromdate") == '' || this.getValue("fromdate") == null) {
        displayMessage(message.fromdate_required);
        is_valid = false;
    } else if (this.getValue("todate") == '' || this.getValue("todate") == null) {
        displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};



// Binds the data from DB
Auditpage.prototype.renderAuditData = function(a_page, audit_data) {
    $('.details').show();
    $('#compliance_animation')
        .removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
    $('.grid-table').show();
    $('.tbody-audittrail-list').find('tr').remove();
    //$('.countryval').text(CountryVal.val())
    $('.typeval').text($('#categoryName option:selected').text());
    showFrom = a_page._sno + 1;
    var is_null = true;

    if ($('#categoryName option:selected').text() == "Client") {
        $('.knowledge').hide();
        $('.client').show();

        $.each(audit_data, function(k, v) {
            if (typeof v.action != 'undefined') {
                is_null = false;
                a_page._sno += 1;
                var tableRow = $('#templates .table-audittrail-list .client-tableRow');
                var rowClone = tableRow.clone();

                f_name = 'Login';
                if (v.action.indexOf('password') >= 0) {
                    f_name = 'Change Password';
                }
                if (v.form_id != 0) {
                    f_name = a_page.getValue("formname", v.form_id);
                }
                $('.snumber', rowClone).text(parseInt(a_page._sno));
                $('.group-name', rowClone).text(Group.val());
                if (LegalEntity_id.val() == "")
                    $('.le-name', rowClone).text("");
                else
                    $('.le-name', rowClone).text(LegalEntity.val());
                var u_name = a_page.getValue('username', v.user_id);
                if (u_name.indexOf("None") >= 0) {
                    u_name = "Administrator";
                }
                $('.username', rowClone).text(u_name);
                $('.usertype', rowClone).text(a_page.getValue('usercategory', v.user_category_id));
                //$('.usertype', rowClone).text("categoryName");
                $('.formname', rowClone).text(f_name);
                $('.action', rowClone).text(v.action);
                $('.datetime', rowClone).text(v.date);
                $('.tbody-audittrail-list').append(rowClone);
            }
        });
    } else {
        $('.knowledge').show();
        $('.client').hide();

        $.each(audit_data, function(k, v) {
            if (typeof v.action != 'undefined') {
                is_null = false;
                a_page._sno += 1;
                var tableRow = $('#templates .table-audittrail-list .know-tableRow');
                var rowClone = tableRow.clone();

                f_name = 'Login';
                if (v.action.indexOf('password') >= 0) {
                    f_name = 'Change Password';
                }
                if (v.form_id != 0) {
                    f_name = a_page.getValue("formname", v.form_id);
                }
                $('.snumber', rowClone).text(parseInt(a_page._sno));
                var u_name = a_page.getValue('username', v.user_id);
                if (u_name.indexOf("None") >= 0) {
                    u_name = "Administrator";
                }
                $('.username', rowClone).text(u_name);
                $('.usertype', rowClone).text(a_page.getValue('usercategory', v.user_category_id));
                //$('.usertype', rowClone).text("categoryName");
                $('.formname', rowClone).text(f_name);
                $('.action', rowClone).text(v.action);
                $('.datetime', rowClone).text(v.date);
                $('.tbody-audittrail-list').append(rowClone);
            }
        });
    }

    if (is_null == true) {
        //a_page.hidePagePan();
        $('.tbody-audittrail-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-audittrail-list').append(clone4);
    } else {
        a_page.showPagePan(showFrom, a_page._sno, a_page._total_record);
    }
    a_page.hideLoader();
};

//To export data
Auditpage.prototype.exportData = function() {
    //this.displayLoader();
    var t_this = this;
    _from_date = this.getValue("fromdate", null);
    _to_date = this.getValue("todate", null);
    _user_id = this.getValue("user", null);
    _form_id = this.getValue("form", null);
    //_country_id = this.getValue("country", null);
    if ($('#categoryName option:selected').text() == "Client") {
        _category_id = this.getValue("categoryid", _user_id);
        _client_id = this.getValue("group", null);
        _bg_id = this.getValue("bg", null);
        _le_id = this.getValue("legalentity", null);
        _div_id = this.getValue("div", null);
        _div_cg_id = this.getValue("divcg", null);
        _unit_id = this.getValue("unit", null);
    } else {
        _category_id = this.getValue("category", null);
        _client_id = null;
        _bg_id = null;
        _le_id = null;
        _div_id = null;
        _div_cg_id = null;
        _unit_id = null;
    }
    t_this.displayLoader();
    mirror.exportAuditTrail(
        _from_date, _to_date, _user_id, _form_id, _category_id, _client_id,
        _le_id, _unit_id, csv,
        function(error, response) {
            hideLoader();
            if (error == null) {
                t_this.hideLoader();
                if (csv) {
                    var download_url = response.link;
                    $(location).attr('href', download_url);
                }
            }
            else {
                t_this.hideLoader();
                if (error == "ExportToCSVEmpty") {
                    displayMessage(message.empty_export);
                }else {
                    displayMessage(error);
                }
            }
        });

};

// To get the audit log data from DB - by passing user type, user name, form name and dates, country
Auditpage.prototype.fetchData = function() {
    //this.displayLoader();
    var t_this = this;
    _from_date = this.getValue("fromdate", null);
    _to_date = this.getValue("todate", null);
    _user_id = this.getValue("user", null);
    _form_id = this.getValue("form", null);
    //_country_id = this.getValue("country", null);
    if ($('#categoryName option:selected').text() == "Client") {
        _category_id = this.getValue("categoryid", _user_id);
        _client_id = this.getValue("group", null);
        _bg_id = this.getValue("bg", null);
        _le_id = this.getValue("legalentity", null);
        _div_id = this.getValue("div", null);
        _div_cg_id = this.getValue("divcg", null);
        _unit_id = this.getValue("unit", null);
    } else {
        _category_id = this.getValue("category", null);
        _client_id = null;
        _bg_id = null;
        _le_id = null;
        _div_id = null;
        _div_cg_id = null;
        _unit_id = null;
    }
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        _sno = 0
    } else {
        _sno = (this._on_current_page - 1) * _page_limit;
    }
    t_this.displayLoader();
    console.log(_from_date, _to_date, _user_id, _form_id, _category_id, _client_id, _le_id, _unit_id)
    mirror.getAuditTrail(
        _from_date, _to_date, _user_id, _form_id, _category_id, _client_id,
        _le_id, _unit_id, _sno, _page_limit,
        function(error, response) {
            if (error != null) {
                t_this.hideLoader();
                displayMessage(error);
            } else {
                t_this.hideLoader();
                t_this._sno = _sno;
                t_this._auditData = response.audit_trail_details;
                if (response.audit_trail_details.length == 0) {
                    t_this.hidePageView();
                    a_page.hidePagePan();
                    //Export_btn.hide();
                    PaginationView.hide();
                    t_this.renderAuditData(t_this, t_this._auditData);
                } else {
                    t_this._total_record = response.total_records;
                    if (t_this._sno == 0) {
                        t_this.createPageView(t_this, t_this._total_record);
                    }
                    //Export_btn.show();
                    PaginationView.show();
                    t_this.renderAuditData(t_this, t_this._auditData);
                }
            }
        }
    );
};

// Bind the data in search filter from DB
Auditpage.prototype.fetchFiltersData = function() {
    var t_this = this;
    mirror.getAuditTrailFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                this.displayMessage(error);
            } else {
                t_this._auditData = response.audit_trail_details;
                t_this._formList = response.forms_list;
                t_this._userList = response.users;
                t_this._categoryList = response.user_categories;
                //t_this._countryList = response.audit_trail_countries;
                t_this._clientUsers = response.audit_client_users;
                t_this._clientForms = response.client_audit_details;
                t_this._clients = response.clients;
                t_this._businessGroups = response.business_group_list;
                t_this._legalEntities = response.unit_legal_entity;
                t_this._divisions = response.divs;
                t_this._divCategories = response.categories;
                t_this._unitList = response.client_audit_units;
                t_this.setControlValues();
            }
        }
    );
};

// Set auto complete field values from DB
Auditpage.prototype.setControlValues = function(e) {
    User.keyup(function(e) {
        var newUserList = [];
        if (Category.val() != '') {
            var textval = $(this).val();
            if (Category.val() >= 2) {
                for (var i = 0; i < a_page._userList.length; i++) {
                    if (a_page._userList[i].user_category_id == Category.val()) {
                        var occur = -1;
                        for (var j = 0; j < newUserList.length; j++) {
                            if (newUserList[j].employee_name == "Console Admin") {
                                occur = 1;
                            }
                        }
                        if (occur < 0) {
                            newUserList.push({
                                "user_category_id": Category.val(),
                                "user_id": a_page._userList[i].user_id,
                                "employee_name": a_page._userList[i].employee_name
                            });
                        }
                    }
                }
            } else {
                for (var i = 0; i < a_page._userList.length; i++) {
                    newUserList.push({
                        "user_category_id": Category.val(),
                        "user_id": a_page._userList[i].user_id,
                        "employee_name": a_page._userList[i].employee_name
                    });
                }
            }

            commonAutoComplete(
                e, ACUser, User_id, textval,
                newUserList, "employee_name", "user_id",
                function(val) {
                    onAutoCompleteSuccess(User, User_id, val);
                });
        } else {
            displayMessage(message.user_required);
        }
    });


    Group.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                commonAutoComplete(
                    e, ACGroup, Group_id, textval,
                    a_page._clients, "group_name", "client_id",
                    function(val) {
                        onAutoCompleteSuccess(Group, Group_id, val);
                    });
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });

    BusinessGroup.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                if (Group_id.val() != "" && Group_id.val() > 0) {
                    bg_list = [];
                    for (var i = 0; i < a_page._businessGroups.length; i++) {
                        if (a_page._businessGroups[i].client_id == Group_id.val()) {
                            bg_list.push({
                                "business_group_id": a_page._businessGroups[i].business_group_id,
                                "business_group_name": a_page._businessGroups[i].business_group_name
                            });
                        }
                    }
                    commonAutoComplete(
                        e, ACBusinessGroup, BusinessGroup_id, textval,
                        bg_list, "business_group_name", "business_group_id",
                        function(val) {
                            onAutoCompleteSuccess(BusinessGroup, BusinessGroup_id, val);
                        });
                } else {
                    displayMessage(message.group_required);
                }
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });

    LegalEntity.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                if (Group_id.val() != "" && Group_id.val() > 0) {
                    le_list = [];
                    for (var i = 0; i < a_page._legalEntities.length; i++) {
                        var bg_check = true;
                        var businessgroupid = BusinessGroup_id.val();
                        if (businessgroupid > 0 && (businessgroupid != a_page._legalEntities[i].business_group_id)) {
                            bg_check = false;
                        }
                        if (a_page._legalEntities[i].client_id == Group_id.val() && bg_check == true) {
                            le_list.push({
                                "legal_entity_id": a_page._legalEntities[i].legal_entity_id,
                                "legal_entity_name": a_page._legalEntities[i].legal_entity_name
                            });
                        }
                    }
                    commonAutoComplete(
                        e, ACLegalEntity, LegalEntity_id, textval,
                        le_list, "legal_entity_name", "legal_entity_id",
                        function(val) {
                            onAutoCompleteSuccess(LegalEntity, LegalEntity_id, val);
                        });
                } else {
                    displayMessage(message.group_required);
                }
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });

    Division.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                if ((Group_id.val() != "" && Group_id.val() > 0) && (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)) {
                    div_list = [];
                    for (var i = 0; i < a_page._divisions.length; i++) {
                        var bg_check = true;
                        var businessgroupid = BusinessGroup_id.val();
                        if (businessgroupid > 0 && (businessgroupid != a_page._divisions[i].business_group_id)) {
                            bg_check = false;
                        }
                        if (a_page._divisions[i].client_id == Group_id.val() && bg_check == true &&
                            a_page._divisions[i].legal_entity_id == LegalEntity_id.val()) {
                            div_list.push({
                                "division_id": a_page._divisions[i].division_id,
                                "division_name": a_page._divisions[i].division_name
                            });
                        }
                    }
                    commonAutoComplete(
                        e, ACDivision, Division_id, textval,
                        div_list, "division_name", "division_id",
                        function(val) {
                            onAutoCompleteSuccess(Division, Division_id, val);
                        });
                } else {
                    if (Group_id.val() != "" && Group_id.val() > 0)
                        displayMessage(message.group_required);
                    else if (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)
                        displayMessage(message.legalentity_required);
                }
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });

    Div_Category.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                if ((Group_id.val() != "" && Group_id.val() > 0) && (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)) {
                    div_catg_list = [];
                    for (var i = 0; i < a_page._divCategories.length; i++) {
                        var bg_check = true;
                        var businessgroupid = BusinessGroup_id.val();
                        if (businessgroupid > 0 && (businessgroupid != a_page._divCategories[i].business_group_id)) {
                            bg_check = false;
                        }

                        var div_check = true;
                        var divisionid = Division_id.val();
                        if (divisionid > 0 && (divisionid != a_page._divCategories[i].division_id)) {
                            div_check = false;
                        }
                        if (a_page._divCategories[i].client_id == Group_id.val() && bg_check == true &&
                            a_page._divCategories[i].legal_entity_id == LegalEntity_id.val() && div_check == true) {
                            div_catg_list.push({
                                "category_id": a_page._divCategories[i].category_id,
                                "category_name": a_page._divCategories[i].category_name
                            });
                        }
                    }
                    commonAutoComplete(
                        e, ACDivCategory, Div_Category_id, textval,
                        div_catg_list, "category_name", "category_id",
                        function(val) {
                            onAutoCompleteSuccess(Div_Category, Div_Category_id, val);
                        });
                } else {
                    if (Group_id.val() != "" && Group_id.val() > 0)
                        displayMessage(message.group_required);
                    else if (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)
                        displayMessage(message.legalentity_required);
                }
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });


    Unit.keyup(function(e) {
        if (Category.val() != '') {
            var textval = $(this).val();
            if ($('#categoryName option:selected').text() == "Client") {
                if ((Group_id.val() != "" && Group_id.val() > 0) && (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)) {
                    unit_list = [];
                    for (var i = 0; i < a_page._unitList.length; i++) {
                        var bg_check = true;
                        var businessgroupid = BusinessGroup_id.val();
                        if (businessgroupid > 0 && (businessgroupid != a_page._unitList[i].business_group_id)) {
                            bg_check = false;
                        }

                        var div_check = true;
                        var divisionid = Division_id.val();
                        if (divisionid > 0 && (divisionid != a_page._unitList[i].division_id)) {
                            div_check = false;
                        }

                        var cg_check = true;
                        var catgid = Div_Category_id.val();
                        if (catgid > 0 && (catgid != a_page._unitList[i].category_id)) {
                            cg_check = false;
                        }
                        if (a_page._unitList[i].client_id == Group_id.val() && bg_check == true &&
                            a_page._unitList[i].legal_entity_id == LegalEntity_id.val() && div_check == true &&
                            cg_check == true) {
                            unit_list.push({
                                "unit_id": a_page._unitList[i].unit_id,
                                "unit_name": a_page._unitList[i].unit_name
                            });
                        }
                    }
                    commonAutoComplete(
                        e, ACUnit, Unit_id, textval,
                        unit_list, "unit_name", "unit_id",
                        function(val) {
                            onAutoCompleteSuccess(Unit, Unit_id, val);
                        });
                } else {
                    if (Group_id.val() != "" && Group_id.val() > 0)
                        displayMessage(message.group_required);
                    else if (LegalEntity_id.val() != "" && LegalEntity_id.val() > 0)
                        displayMessage(message.legalentity_required);
                }
            } else {
                displayMessage(message.user_category_required);
            }
        } else {
            displayMessage(message.user_required);
        }
    });

    Form.keyup(function(e) {
        var textval = $(this).val();
        var form_list = [];
        if (Category.val() != '' && Category.val() > 0) {
            if (Category.val() == 1) {
                for (var i = 0; i < a_page._auditData.length; i++) {
                    if ((a_page._auditData[i].user_category_id == Category.val())) {
                        form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                    }
                }
            } else if ($('#categoryName option:selected').text() != "Client") {
                var userId = User_id.val();
                for (var i = 0; i < a_page._auditData.length; i++) {
                    frm_user_id = a_page._auditData[i].user_id;
                    if (userId > 0) {
                        if ((a_page._auditData[i].user_category_id == Category.val()) &&
                            (userId == frm_user_id)) {
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                        }
                    } else {
                        if ((a_page._auditData[i].user_category_id == Category.val())) {
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                        }
                    }
                }
            } else if ($('#categoryName option:selected').text() == "Client") {
                form_list = a_page._clientForms;
            }


            commonAutoComplete(
                e, ACForm, Form_id, textval,
                form_list, "form_name", "form_id",
                function(val) {
                    onAutoCompleteSuccess(Form, Form_id, val);
                });
        }
    });

    Category.empty();
    Category.append($('<option></option>').val('').html('Select'));
    $.each(a_page._categoryList, function(key, value) {
        Category.append($('<option></option>').val(a_page._categoryList[key].user_category_id).html(a_page._categoryList[key].user_category_name));
    });

}


// To push forms inside form list without any duplication
Auditpage.prototype.pushForms = function(u_type, form_id, form_list) {
    var a_page = this;
    var userCheck = false;
    //var form_list = [];
    if (u_type == "user") {
        var arr_form_id = [];
        element = form_id;
        arr_form_id = a_page._formList.reduce(function(arr, e, i) {
            if (e.form_id === element)
                arr.push(i);
            return arr;
        }, []);

        if (arr_form_id.length > 0) {
            userCheck = true;
        }

        if (arr_form_id.length == 0 && form_id == 0) {
            userCheck = true;
        }
    }
    if (u_type == "admin") {
        userCheck = true;
    }
    if (userCheck == true) {
        form_name = null;
        if (form_id > 0) {
            for (var j = 0; j < a_page._formList.length; j++) {
                if (form_id == a_page._formList[j].form_id) {
                    form_name = a_page._formList[j].form_name;
                    break;
                }
            }
        } else {
            form_name = "Login"
        }
        if (form_list.length > 0) {
            var arr_form = [];
            element = form_id;
            arr_form = form_list.reduce(function(arr, e, i) {
                if (e.form_id === element)
                    arr.push(i);
                return arr;
            }, []);

            if (arr_form.length == 0) {
                form_list.push({
                    "form_id": form_id,
                    "form_name": form_name
                });
            }
        } else {
            form_list.push({
                "form_id": form_id,
                "form_name": form_name
            });
        }
    }

    return form_list;
};

Auditpage.prototype.renderControl = function() {
    To_date.val(current_date());
    From_date.val(past_days(7)); // 7 days bafore to_date
};

// Pagination Functions - begins
Auditpage.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

Auditpage.prototype.createPageView = function(a_obj, total_records) {
    perPage = parseInt(ItemsPerPage.val());
    a_obj.hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(a_obj._on_current_page) != cPage) {
                a_obj._on_current_page = cPage;
                a_obj.fetchData();
            }
        }
    });
};
Auditpage.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
Auditpage.prototype.hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

Auditpage.prototype.renderPageControls = function(e) {
    var t_this = this;
    ItemsPerPage.on('change', function(e) {
        t_this.perPage = parseInt($(this).val());
        t_this._sno = 0;
        t_this._on_current_page = 1;
        t_this.createPageView(t_this, t_this._total_record);
        t_this.fetchData();
    });
    t_this._perPage = parseInt(ItemsPerPage.val());

};
// Pagination Ends

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if (current_id == "group-id") {
        clearElement([BusinessGroup_id, BusinessGroup, LegalEntity_id, LegalEntity, Division_id, Division, Div_Category_id, Div_Category, Unit_id, Unit]);
    } else if (current_id == "businessgroupid") {
        clearElement([LegalEntity_id, LegalEntity, Division_id, Division, Div_Category_id, Div_Category, Unit_id, Unit]);
    } else if (current_id == "legalentityid") {
        clearElement([Division_id, Division, Div_Category_id, Div_Category, Unit_id, Unit]);
    } else if (current_id == "divisionid") {
        clearElement([Div_Category_id, Div_Category, Unit_id, Unit]);
    } else if (current_id == "categoryid") {
        clearElement([Unit_id, Unit]);
    }
}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

initializeControlEvents = function(a_page) {

    Show_btn.click(function(e) {
        //a_page.resetFields();
        //Export_btn.hide();
        is_valid = a_page.validateMandatory();
        if (is_valid == true) {
            a_page._on_current_page = 1;
            a_page._total_record = 0;
            a_page.fetchData();
            a_page.renderPageControls();
        }
    });

    Export_btn.click(function(e) {
        is_valid = a_page.validateMandatory();
        if (is_valid == true) {
            csv = true;
            a_page.exportData();
        }
    });

    Category.change(function(e) {
        a_page.resetFields();
        if (parseInt(Category.val()) >= 2) {
            $('.user-list').show();
            User.val('');
            if ($('#categoryName option:selected').text() == "Client") {
                $('.group-name').show();
                $('.bg-name').show();
                $('.le-name').show();
                $('.division-name').show();
                $('.category-name').show();
                $('.unit-name').show();
            }
        } else {
            $('.user-list').hide();
            $('.group-name').hide();
            $('.bg-name').hide();
            $('.le-name').hide();
            $('.division-name').hide();
            $('.category-name').hide();
            $('.unit-name').hide();
        }


    });

    on_page_load = function() {
        a_page.resetFields();
        a_page.renderPageControls();
    }
    on_page_load();

}

// Instance Creation of the page class
a_page = new Auditpage();

// Form Initalize
$(function() {
    loadItemsPerPage();
    initializeControlEvents(a_page);
    a_page.fetchFiltersData();
    a_page.renderControl();
});