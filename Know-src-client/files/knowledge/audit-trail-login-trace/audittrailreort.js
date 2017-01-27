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
Category = $('#categoryName');
Show_btn = $("#show");
Export_btn = $("#export");
var msg = message;

//var ACCountry = $('#ac-country');
//CountryVal = $('#countryval');
//Country = $('#country')

//Autocomplete variable declaration
var ACUser = $('#ac-user');
var ACForm = $('#ac-form');

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
Auditpage.prototype.clearMessage = function(){
    Msg_pan.text('');
    Msg_pan.hide();
};

// To display the loader until the action happens
Auditpage.prototype.displayLoader = function(){
    Spin_icon.show();
};

// To Hide the Loader once done
Auditpage.prototype.hideLoader = function() {
    Spin_icon.hide();
};

// Resets the filter fields
Auditpage.prototype.resetFields = function(){
    $('.tbody-audittrail-list').find('tr').remove();
    $('.grid-table').hide();
    this._sno = 0;
    //CountryVal.val('');
    Form.val('');
    Form_id.val('');
    User.val('');
    User_id.val('');
    //this.clearMessage();
};

// To get the corresponding value
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
    }
    else if (field_name == "todate") {
        t_date = To_date.val().trim();
        return t_date;
    }
    else if (field_name == "username") {
        if (f_id == 0 || f_id == "1" || f_id == "3") {
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
    /*else if (this.getValue("country") == '' || this.getValue("country") == null) {
        displayMessage(msg.country_required);
        is_valid = false;
    }*/
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



// Binds the data from DB
Auditpage.prototype.renderAuditData = function(a_page, audit_data){
    $('.grid-table').show();
    $('.tbody-audittrail-list').find('tr').remove();
    //$('.countryval').text(CountryVal.val())
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
            var u_name = a_page.getValue('username', v.user_id);
            if(u_name.indexOf("None") >= 0){
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
    if (is_null == true) {
        //a_page.hidePagePan();
        $('.tbody-audittrail-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-audittrail-list').append(clone4);
    }
    else {
        a_page.showPagePan(showFrom, a_page._sno, a_page._total_record);
    }
    a_page.hideLoader();
};

//To export data
Auditpage.prototype.exportData = function() {
    //this.displayLoader();
    if($('.tbody-audittrail-list').find('tr').length > 0){
        var t_this = this;
        _from_date = this.getValue("fromdate", null);
        _to_date = this.getValue("todate", null);
        _user_id = this.getValue("user", null);
        _form_id = this.getValue("form", null);
        //_country_id = this.getValue("country", null);
        _category_id =this.getValue("category", null);

        t_this.displayLoader();
        mirror.exportAuditTrail(_from_date, _to_date, _user_id, _form_id, _category_id, csv,
            function(error, response) {
                hideLoader();
                if(error == null){
                    t_this.hideLoader();
                    if (csv) {
                      var download_url = data.link;
                      window.open(download_url, '_blank');
                    }
                }
            });
    }else{
        displayMessage(message.export_empty);
    }
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
    _category_id =this.getValue("category", null);
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }
    t_this.displayLoader();
    mirror.getAuditTrail(_from_date, _to_date, _user_id, _form_id, _category_id, _sno, _page_limit,
        function(error, response) {
            if (error != null) {
                t_this.hideLoader();
                displayMessage(error);
            }
            else {
                t_this.hideLoader();
                t_this._sno  = _sno;
                t_this._auditData = response.audit_trail_details;
                if (response.audit_trail_details.length == 0) {
                    t_this.hidePageView();
                    a_page.hidePagePan();
                    Export_btn.hide();
                    PaginationView.hide();
                    t_this.renderAuditData(t_this, t_this._auditData);
                }
                else{
                    t_this._total_record = response.total_records;
                    if (t_this._sno == 0) {
                        t_this.createPageView(t_this, t_this._total_record);
                    }
                    Export_btn.show();
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
            if (error != null) {
                this.displayMessage(error);
            }
            else {
                t_this._auditData = response.audit_trail_details;
                t_this._formList = response.forms_list;
                t_this._userList = response.users;
                t_this._categoryList = response.user_categories;
                //t_this._countryList = response.audit_trail_countries;
                t_this.setControlValues();
            }
        }
    );
};

// Set auto complete field values from DB
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
        if(Category.val() != '' && Category.val() > 0)
        {
            if(Category.val() == 1){
                for(var i=0;i<a_page._auditData.length;i++)
                {
                    if((a_page._auditData[i].user_category_id == Category.val())){
                        form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                    }
                }
            }else{
                var userId = User_id.val();
                for(var i=0;i<a_page._auditData.length;i++)
                {
                    frm_user_id = a_page._auditData[i].user_id;
                    if(userId > 0){
                        if((a_page._auditData[i].user_category_id == Category.val()) &&
                            (userId == frm_user_id)){
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                        }
                    }else{
                        if((a_page._auditData[i].user_category_id == Category.val())){
                            form_list = a_page.pushForms("user", a_page._auditData[i].form_id, form_list);
                        }
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

}


// To push forms inside form list without any duplication
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

        if(arr_form_id.length == 0 && form_id == 0){
            userCheck = true;
        }
    }
    if(u_type == "admin"){
        userCheck = true;
    }
    if(userCheck == true){
        form_name = null;
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
            form_list.push({
                "form_id": form_id,
                "form_name": form_name
            });
        }
    }

    return form_list;
};

Auditpage.prototype.renderControl = function(){
    To_date.val(current_date());
    From_date.val(past_days(7));  // 7 days bafore to_date
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
// Pagination Ends

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

initializeControlEvents = function(a_page){

    Show_btn.click(function(e) {
        a_page.resetFields();
        Export_btn.hide();
        is_valid = a_page.validateMandatory();
        if (is_valid == true) {
            a_page._on_current_page = 1;
            a_page._total_record = 0;
            a_page.fetchData();
            a_page.renderPageControls();
        }
    });

    Export_btn.click(function(e) {
        csv = true;
        a_page.exportData();
    });

    Category.change(function(e) {
        a_page.resetFields();
        if(parseInt(Category.val()) > 2){
            $('.user-list').show();
            User.val('');
        }else{
            $('.user-list').hide();
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
$(function () {
    loadItemsPerPage();
    initializeControlEvents(a_page);
    a_page.fetchFiltersData();
    a_page.renderControl();
});