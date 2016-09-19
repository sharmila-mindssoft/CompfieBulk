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
Show_btn = $(".btn-submit");
Item_page_select = $('#items_per_page');

a_page = null;
function Auditpage() {
    this._sno = 0;
    this._userList = {};
    this._formList = {};
    this._auditData = {};
    this._total_record = 0;
    this._perPage = 0;
    this._on_current_page = 1;
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
    if (field_name == "user") {
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
    _page_limit = parseInt(Item_page_select.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }
    mirror.getAuditTrail(_from_date, _to_date, _user_id, _form_id, _sno, _page_limit,
        function(error, response) {
            if (error != null) {
                this.displayMessage(error);
            }
            else {
                t_this._sno  = _sno;
                t_this._auditData = response.audit_trail_details;
                t_this._formList = response.forms;
                t_this._userList = response.users;
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
        var textval = $(this).val();
        getUserAutocomplete(e, textval, a_page._userList, function (v) {
            User.val(v[1]);
            User_id.val(v[0]);
        });
    });

    Form.keyup(function(e) {
        var textval = $(this).val();
        getFormAutocomplete(e, textval, a_page._formList, function (v) {
            Form.val(v[1]);
            Form_id.val(v[0]);
        });
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