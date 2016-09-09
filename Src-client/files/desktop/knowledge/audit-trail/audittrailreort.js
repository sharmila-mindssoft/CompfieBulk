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

a_page = null;
function Auditpage() {
	this._sno = 0;
	this._userList = {};
	this._formList = {};
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
	$.each(audit_data, function(k, v) {
		if (typeof v.action != 'undefined') {
			this._sno += 1;
			var tableRow = $('#templates .table-audittrail-list .tableRow');
			var rowClone = tableRow.clone();

			f_name = 'Login';
			if (v.action.indexOf('password') >= 0) {
				f_name = 'Change Password';
			}
			if (v.form_id != 0) {
				f_name = a_page.getValue("formname", v.form_id);
			}

			$('.formname', rowClone).text(f_name);
			$('.username', rowClone).text(a_page.getValue('username', v.user_id));
			$('.datetime', rowClone).text(v.date);
			$('.action', rowClone).text(v.action);
			$('.tbody-audittrail-list').append(rowClone);
		}

	});
};

Auditpage.prototype.fetchData = function() {
	var t_this = this;
	_from_date = this.getValue("fromdate", null);
	_to_date = this.getValue("todate", null);
	_user_id = this.getValue("user", null);
	_form_id = this.getValue("form", null);
	_sno = this._sno;
	mirror.getAuditTrail(_from_date, _to_date, _user_id, _form_id, _sno, function(error, response) {
		if (error != null) {
			this.displayMessage(error);
		}
		else {
			t_this._auditData = response.audit_trail_details;
			t_this._formList = response.forms;
			t_this._userList = response.users;
			t_this.renderAuditData(t_this, t_this._auditData);
		}
	});

};

Auditpage.prototype.renderControl = function(){
	To_date.val(current_date());
	From_date.val(past_days(7));  // 7 days bafore to_date
};

Auditpage.prototype.renderPages = function() {
	alert('');
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
			a_page.fetchData();
		}
	});
	on_page_load = function() {
		a_page.resetFields();
		is_valid = a_page.validateMandatory();
		if (is_valid == true) {
			a_page.fetchData();
		}
	}
	on_page_load();

}

a_page = new Auditpage();

$(function () {
	a_page.renderControl();
	initializeControlEvents(a_page);
});