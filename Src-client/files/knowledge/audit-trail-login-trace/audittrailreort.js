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
CountryVal = $('#countryval');
Country = $('#country')
Category = $('#category');
Show_btn = $(".btn-submit");

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACUser = $('#ac-user');
var ACForm = $('#ac-form');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;

a_page = null;
function Auditpage() {
    this._sno = 0;
    this._userList = {};
    this._formList = {};
    this._categoryList = {};
    this._countryList = {};
    this._auditData = {};
}

Auditpage.prototype.displayMessage = function(message){
    Msg_pan.text(message);
    Msg_pan.show();
};

Auditpage.prototype.clearMessage = function(){
    Msg_pan.text('');
    Msg_pan.hide();
};

Auditpage.prototype.displayLoader = function(){
    Spin_icon.show();
};

Auditpage.prototype.hideLoader = function() {
    Spin_icon.hide();
};

Auditpage.prototype.resetFields = function(){
    $('.tbody-audittrail-list').find('tr').remove();
    $('.grid-table').show();
    this._sno = 0;
    this.clearMessage();
};

Auditpage.prototype.getValue = function(field_name, f_id){
    if (field_name == "category") {
        cg_id = Category_id.val().trim();
        if (cg_id == '') {
            return null;
        }
        return parseInt(cg_id);
    }
    else if (field_name == "user") {
        u_id = User_id.val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    }
    else if (field_name == "form") {
        fr_id = Form_id.val().trim();
        if (fr_id == '') {
            return null;
        }
        return parseInt(fr_id);
    }
    else if (field_name == "country") {
        c_id = Country.val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }
    else if (field_name == "fromdate") {
        f_date = From_date.val().trim();
        return f_date;
    }
    else if (field_name == "todate") {
        t_date = To_date.val().trim();
        return t_date;
    }
    else if (field_name == "username") {
        if (f_id == 0) {
            return 'Administrator';
        }
        else {
            emp_name = null
            $.each(this._userList, function(k, v) {
                if (v.user_id == f_id) {
                    emp_name = v.employee_name;
                    return emp_name;
                }
            });
            return emp_name;
        }
    }
    else if (field_name == "formname") {
        frm_name = null;
        $.each(this._formList, function(k, v) {
            if (v.form_id == f_id) {
                frm_name = v.form_name;
                return frm_name;
            }
        });
        return frm_name;
    }
};

Auditpage.prototype.validateMandatory = function(){
    is_valid = true;
    if (this.getValue("fromdate") == '') {
        this.displayMessage(message.fromdate_required);
        is_valid = false;
    }
    else if (this.getValue("todate") == '') {
        this.displayMessage(message.todate_required);
        is_valid = false;
    }
    return is_valid;
};

Auditpage.prototype.renderAuditData = function(a_page, audit_data){
    $('.tbody-audittrail-list').find('tr').remove();
    showFrom = a_page._sno + 1;
    var is_null = true;
    $.each(audit_data, function(k, v) {
        if (typeof v.action != 'undefined') {
            is_null = false;
            a_page._sno += 1;
            var tableRow = $('#templates .table-audittrail-list .tableRow');
            var rowClone = tableRow.clone();

            f_name = 'Login';
            if (v.action.indexOf('password') >= 0) {
                f_name = 'Change Password';
            }
            if (v.form_id != 0) {
                f_name = a_page.getValue("formname", v.form_id);
            }
            $('.snumber', rowClone).text(parseInt(a_page._sno));
            $('.formname', rowClone).text(f_name);
            $('.username', rowClone).text(a_page.getValue('username', v.user_id));
            $('.datetime', rowClone).text(v.date);
            $('.action', rowClone).text(v.action);
            $('.tbody-audittrail-list').append(rowClone);
        }
    });
    if (is_null == true) {
        a_page.hidePagePan();
    }
    else {
        a_page.showPagePan(showFrom, a_page._sno, a_page._total_record);
    }
    a_page.hideLoader();
};

Auditpage.prototype.fetchData = function() {
    this.displayLoader();
    var t_this = this;
    _from_date = this.getValue("fromdate", null);
    _to_date = this.getValue("todate", null);
    _user_id = this.getValue("user", null);
    _form_id = this.getValue("form", null);
    _country_id = this.getValue("country", null);
    _category_id =this.getValue("category", null);
    _page_limit = parseInt(Item_page_select.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }
    mirror.getAuditTrail(_from_date, _to_date, _user_id, _form_id, _country_id, _category_id, _sno, _page_limit,
        function(error, response) {
            if (error != null) {
                this.displayMessage(error);
            }
            else {
                t_this._sno  = _sno;
                t_this._auditData = response.audit_trail_details;
                t_this._formList = response.forms;
                t_this._userList = response.users;
                t_this._categoryList = response.user_categories;
                t_this._countryList = response.countries;
                if (response.total_records == 0) {
                    t_this.hidePageView();
                    a_page.hidePagePan();
                    $('#no-record-templates').show();
                    return;
                }
                if (t_this._total_record == 0) {
                    $('#no-record-templates').hide();
                    t_this._total_record = response.total_records;
                    t_this.createPageView(t_this, t_this._total_record);
                }
                t_this._total_record = response.total_records;
                t_this.renderAuditData(t_this, t_this._auditData);
            }
        }
    );
};

Auditpage.prototype.renderControl = function(){
    To_date.val(current_date());
    From_date.val(past_days(7));  // 7 days bafore to_date
};
Auditpage.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

Auditpage.prototype.createPageView = function(a_obj, total_records) {
    perPage = parseInt(Item_page_select.val());
    a_obj.hidePageView();
    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
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
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
Auditpage.prototype.hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

Auditpage.prototype.renderPageControls = function(e) {
    var t_this = this;
    Item_page_select.on('change', function(e) {
        t_this.perPage = parseInt($(this).val());
        t_this._sno = 0;
        t_this._on_current_page = 1;
        t_this.createPageView(t_this, t_this._total_record);
        t_this.fetchData();
    });
    t_this._perPage = parseInt(Item_page_select.val());

};

initializeControlEvents = function(a_page){
    User.keyup(function(e) {
        var newUserList = [];
        if(category.val() != '')
        {
            var textval = $(this).val();

            for(var i=0;i<a_page._userList.length;i++)
            {
              if(a_page._userList[i].user_category_id == Category.val())
              {
                newUserList.push({
                  "user_category_id": Category.val(),
                  "user_id": a_page._userList[i].user_id,
                  "employee_name": a_page._userList[i].employee_name
                });
              }
            }
            commonAutoComplete(
                e, ACUser, User, textval,
                a_page._userList, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(User, User_id, val);
            });
        }
        else
        {
            displayMessage(message.user_required);
        }
    });

    Form.keyup(function(e) {
        var textval = $(this).val();
        if(category.val() != '')
        {
            var userId = user_id.val();
            var form_list = [];
            for(var i=0;i<a_page._userList.length;i++)
            {
                var user_check = userId>0?(userId === a_page._userList[i].user_id):false;
                if((a_page._userList[i].user_category_id == Category.val()) &&
                    (user_check == true || user_check == false))
                {
                    for(var j=0;j<a_page._formList;j++)
                    {
                        if(a_page._formList[j].user_id == a_page._userList[i].user_id)
                        {
                            form_list.push({
                                "form_id": a_page._formList[j].form_id,
                                "form_name": a_page._formList[j].form_name
                            });
                        }
                    }
                }
            }

            commonAutoComplete(
                e, ACForm, Form, textval,
                form_list, "form_name", "form_id", function (val) {
                onAutoCompleteSuccess(Form, Form_id, val);
            });
        }
    });

    Category.keyup(function(e) {
        $.each(a_page._categoryList, function (key, value) {
            Category.append($('<option></option>').val(a_page._categoryList[key].user_category_id).html(categoryList[key].user_category_name));
        });
    });

    $('#countryval').keyup(function (e) {
        var textval = $(this).val();
        if(category.val() != '')
        {
            var userId = user_id.val();
            var ctry_list = [];
            for(var i=0;i<a_page._userList.length;i++)
            {
                var user_check = userId>0?(userId === a_page._userList[i].user_id):false;
                if((a_page._userList[i].user_category_id == Category.val()) &&
                    (user_check == true || user_check == false))
                {
                    for(var j=0;j<a_page._countryList;j++)
                    {
                        if(a_page._countryList[j].user_id == a_page._userList[i].user_id)
                        {
                            ctry_list.push({
                                "country_id": a_page._countryList[j].country_id,
                                "country_name": a_page._countryList[j].country_name
                            });
                        }
                    }
                }
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACCountry, Country, text_val,
                countryList, "country_name", "country_id", function (val) {
                onAutoCompleteSuccess(CountryVal, Country, val);
            });
        }
    });


    Show_btn.click(function(e) {
        a_page.resetFields();
        is_valid = a_page.validateMandatory();
        if (is_valid == true) {
            a_page._on_current_page = 1;
            a_page._total_record = 0;
            a_page.fetchData();
            a_page.renderPageControls();

        }
    });


    on_page_load = function() {
        a_page.resetFields();
        is_valid = a_page.validateMandatory();
        if (is_valid == true) {
            a_page.fetchData();
            a_page.renderPageControls();
        }
    }
    on_page_load();

}

a_page = new Auditpage();

$(function () {
    loadItemsPerPage();
    a_page.renderControl();
    initializeControlEvents(a_page);
});