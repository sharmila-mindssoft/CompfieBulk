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
Category = $('#categoryName');
Show_btn = $("#show");
var msg = message;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACUser = $('#ac-user');
var ACForm = $('#ac-form');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');

a_page = null;
function Auditpage() {
    this._sno = 0;
    this._userList = {};
    this._formList = {};
    this._categoryList = {};
    this._countryList = {};
    this._auditData = {};
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
}

/*Auditpage.prototype.displayMessage = function(message){
    Msg_pan.text(message);
    Msg_pan.show();
};*/

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
    $('.grid-table').hide();
    this._sno = 0;
    CountryVal.val('');
    Form.val('');
    User.val('');
    this.clearMessage();
};

Auditpage.prototype.getValue = function(field_name, f_id){
    if (field_name == "category") {
        cg_id = Category.val();
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
    else if (field_name == "usercategory") {
        if (f_id == 0) {
            return 'Administrator';
        }
        else {
            category_name = null
            $.each(this._categoryList, function(k, v) {
                if (v.user_category_id == f_id) {
                    category_name = v.user_category_name;
                    return category_name;
                }
            });
            return category_name;
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
    if (this.getValue("category") == '' || this.getValue("category") == null) {
        displayMessage(msg.catgname_required);
        is_valid = false;
    }
    else if (this.getValue("country") == '' || this.getValue("country") == null) {
        displayMessage(msg.country_required);
        is_valid = false;
    }
    else if (this.getValue("fromdate") == '' || this.getValue("fromdate") == null) {
        displayMessage(msg.fromdate_required);
        is_valid = false;
    }
    else if (this.getValue("todate") == ''  || this.getValue("todate") == null) {
        displayMessage(msg.todate_required);
        is_valid = false;
    }
    return is_valid;
};

Auditpage.prototype.renderAuditData = function(a_page, audit_data){
    $('.grid-table').show();
    $('.tbody-audittrail-list').find('tr').remove();
    $('.countryval').text(CountryVal.val())
    $('.typeval').text($('#categoryName option:selected').text());
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
            $('.username', rowClone).text(a_page.getValue('username', v.user_id));
            $('.usertype', rowClone).text(a_page.getValue('usercategory', v.user_category_id));
           //$('.usertype', rowClone).text("categoryName");
            $('.formname', rowClone).text(f_name);
            $('.action', rowClone).text(v.action);
            $('.datetime', rowClone).text(v.date);
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
    //this.displayLoader();
    var t_this = this;
    _from_date = this.getValue("fromdate", null);
    _to_date = this.getValue("todate", null);
    _user_id = this.getValue("user", null);
    _form_id = this.getValue("form", null);
    _country_id = this.getValue("country", null);
    _category_id =this.getValue("category", null);
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }
    console.log(_from_date, _to_date, _user_id, _form_id, _country_id, _category_id, _sno, _page_limit)
    mirror.getAuditTrail(_from_date, _to_date, _user_id, _form_id, _country_id, _category_id, _sno, _page_limit,
        function(error, response) {
            if (error != null) {
                t_this.displayMessage(error);
            }
            else {
                //t_this.hideLoader();
                t_this._sno  = _sno;
                t_this._auditData = response.audit_trail_details;
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

Auditpage.prototype.fetchFiltersData = function() {
    var t_this = this;
    mirror.getAuditTrailFilter(
        function(error, response) {
            if (error != null) {
                this.displayMessage(error);
            }
            else {
                console.log(response)
                t_this._auditData = response.audit_trail_details;
                t_this._formList = response.forms_list;
                t_this._userList = response.users;
                t_this._categoryList = response.user_categories;
                t_this._countryList = response.audit_trail_countries;
                t_this.setControlValues();
            }
        }
    );
};

Auditpage.prototype.setControlValues = function(e) {
    User.keyup(function(e) {
        var newUserList = [];
        if(Category.val() != '')
        {
            var textval = $(this).val();
            if(Category.val() > 2){
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
            }
            else{
                for(var i=0;i<a_page._userList.length;i++)
                {
                    newUserList.push({
                        "user_category_id": Category.val(),
                        "user_id": a_page._userList[i].user_id,
                        "employee_name": a_page._userList[i].employee_name
                    });
                }
            }

            commonAutoComplete(
                e, ACUser, User_id, textval,
                newUserList, "employee_name", "user_id", function (val) {
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
        var form_list = [];
        if(Category.val() != '')
        {
            var userId = User_id.val();
            console.log("user:"+userId, Category.val())
            if(Category.val() > 2){
                for(var i=0;i<a_page._auditData.length;i++)
                {
                    frm_user_id = a_page._auditData[i].user_id;
                    if(userId > 0){
                        if((a_page._auditData[i].user_category_id == Category.val()) &&
                            (userId == frm_user_id)){
                            console.log("1:"+form_list.length)
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                            console.log("2:"+form_list.length)
                        }
                    }
                    else
                    {
                        if((a_page._auditData[i].user_category_id == Category.val())){
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                        }
                    }
                }
            }
            else
            {
                for(var i=0;i<a_page._auditData.length;i++)
                {
                    if(userId > 0){
                        if((a_page._auditData[i].user_id == userId)){
                            console.log("1:"+form_list.length)
                            form_list = a_page.pushForms("admin", a_page._auditData[i].form_id, form_list);
                            console.log("2:"+form_list.length)
                        }
                    }
                    else
                    {
                        form_list = a_page.pushForms("admin", a_page._auditData[i].form_id, form_list);
                    }
                }
            }
            commonAutoComplete(
                e, ACForm, Form_id, textval,
                form_list, "form_name", "form_id", function (val) {
                onAutoCompleteSuccess(Form, Form_id, val);
            });
        }
    });


    Category.empty();
    Category.append($('<option></option>').val('').html('Select'));
    $.each(a_page._categoryList, function (key, value) {
        Category.append($('<option></option>').val(a_page._categoryList[key].user_category_id).html(a_page._categoryList[key].user_category_name));
    });

    CountryVal.keyup(function (e) {
        var textval = $(this).val();
        if(Category.val() != '')
        {
            var userId = User_id.val();
            var ctry_list = [];
            if(Category.val() > 2){
                for(var i=0;i<a_page._userList.length;i++)
                {
                    db_user_id = a_page._userList[i].user_id;
                    if(userId > 0){
                        if((a_page._userList[i].user_category_id == Category.val()) &&
                        (db_user_id == userId)){
                            ctry_list = a_page.pushCountries("user",db_user_id);
                        }
                    }
                    else
                    {
                        if(a_page._userList[i].user_category_id == Category.val()){
                            ctry_list = a_page.pushCountries("user",db_user_id);
                        }
                    }
                }
            }
            else{
                ctry_list = a_page.pushCountries("admin",0);
            }
            commonAutoComplete(
                e, ACCountry, Country, textval,
                ctry_list, "country_name", "country_id", function (val) {
                onAutoCompleteSuccess(CountryVal, Country, val);
            });
        }
    });
}

Auditpage.prototype.pushCountries = function(u_type, user_id){
    var a_page = this;
    var userCheck = false;
    var ctry_list = [];
    for(var j=0;j<a_page._countryList.length;j++)
    {
        if(u_type == "user"){
            userCheck = user_id>0?(user_id == a_page._countryList[j].user_id):false;
        }
        else if(u_type == "admin"){
            userCheck = true;
        }
        if(userCheck == true){
            if(ctry_list.length > 0)
            {
                var arr_country = [];
                element = a_page._countryList[j].country_id;
                arr_country = ctry_list.reduce(function(arr, e, i) {
                    if (e.country_id === element)
                        arr.push(i);
                    return arr;
                }, []);


                if(arr_country.length == 0){
                    ctry_list.push({
                        "country_id": a_page._countryList[j].country_id,
                        "country_name": a_page._countryList[j].country_name
                    });
                }
            }
            else
            {
                ctry_list.push({
                    "country_id": a_page._countryList[j].country_id,
                    "country_name": a_page._countryList[j].country_name
                });
            }
        }
    }
    return ctry_list;
};

Auditpage.prototype.pushForms = function(u_type, form_id, form_list){
    var a_page = this;
    var userCheck = false;
    //var form_list = [];

    if(u_type == "user"){
        var arr_form_id = [];
        element = form_id;
        arr_form_id = a_page._formList.reduce(function(arr, e, i) {
            if (e.form_id === element)
                arr.push(i);
            return arr;
        }, []);

        if(arr_form_id.length > 0){
            userCheck = true;
        }
    }

    if(u_type == "admin"){
        userCheck = true;
    }

    console.log("check:"+userCheck)
    if(userCheck == true){
        form_name = null;
        console.log("id:"+form_id)
        if(form_id > 0){
            for(var j=0;j<a_page._formList.length;j++)
            {
                if(form_id == a_page._formList[j].form_id){
                    form_name = a_page._formList[j].form_name;
                    break;
                }
            }
        }
        else{
            form_name = "Login"
        }
        console.log("name:"+form_name);
        if(form_list.length > 0)
        {
            var arr_form = [];
            element = form_id;
            arr_form = form_list.reduce(function(arr, e, i) {
                if (e.form_id === element)
                    arr.push(i);
                return arr;
            }, []);


            if(arr_form.length == 0){
                form_list.push({
                    "form_id": form_id,
                    "form_name": form_name
                });
            }
        }
        else
        {
            console.log("name:"+form_name);
            form_list.push({
                "form_id": form_id,
                "form_name": form_name
            });
        }
    }
    console.log(form_list.length)
    return form_list;
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
    perPage = parseInt(ItemsPerPage.val());
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
    ItemsPerPage.on('change', function(e) {
        t_this.perPage = parseInt($(this).val());
        t_this._sno = 0;
        t_this._on_current_page = 1;
        t_this.createPageView(t_this, t_this._total_record);
        t_this.fetchData();
    });
    t_this._perPage = parseInt(ItemsPerPage.val());

};

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

initializeControlEvents = function(a_page){

    Show_btn.click(function(e) {
        //a_page.resetFields();
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
        a_page.renderPageControls();
    }
    on_page_load();

}

a_page = new Auditpage();

$(function () {
    loadItemsPerPage();
    initializeControlEvents(a_page);
    a_page.fetchFiltersData();
    a_page.renderControl();
});