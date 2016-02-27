var auditTrailList;
var formList;
var userList;
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
function initialize(){
	function onSuccess(data){
		auditTrailList = data['audit_trail_details'];
		formList = data['forms'];
		userList = data['users'];
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.getAuditTrail(
		function(error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}

$("#show").click(function(){
	var fromDateValue = $("#from-date").val();
	var toDateValue = $("#to-date").val();
	var userIdValue = $("#userid").val();
	var formIdValue = $("#formid").val();

	if(fromDateValue == ''){
		displayMessage('Enter From Date');
	}
	else if(toDateValue == ''){
		displayMessage('Enter To Date');
	}
	else{
	 	$(".tbody-audittrail-list").find("tr").remove();
	 	$('.grid-table').show();
	 	function getUserName(userId){
	 		var userName;
	 		$.each(userList, function(key){
	 			if(userList[key]['user_id'] == userId){
	 				userName = userList[key]['employee_name'];
	 			}
	 		});
	 		return userName;
	 	}
	 	function getFormName(formId){
	 		var formName;
	 		$.each(formList, function(key){
	 			if(formList[key]['form_id'] == formId){
	 				formName = formList[key]['form_name'];
	 			}
	 		});
	 		return formName;
	 	}
		var sno = 0;

		$.each(auditTrailList, function (key, value){
			//from Date Conversion
			var fromDate = fromDateValue.split("-");
			var fromsplitDate = fromDate[1]+","+fromDate[0]+","+fromDate[2];
			var fromDateVal = new Date(fromsplitDate).getTime();
			//To Date Conversion
			var toDate = toDateValue.split("-");
			var tosplitDate = toDate[1]+","+toDate[0]+","+toDate[2];
			var toDateVal = new Date(tosplitDate).getTime();
			//Api Date conversion
			var auditDateValue = auditTrailList[key]['date'];
			var auditDate = auditDateValue.split("-");
			var auditdatesplit = auditDate[1]+","+auditDate[0]+","+auditDate[2];
			var auditDateVal = new Date(auditdatesplit).getTime();

			var auditUser = auditTrailList[key]['user_id'];
			var auditFormId = auditTrailList[key]['form_id'];
			var formCheckval;
			var userCheckval;
			//userid empty, formid empty
			if((fromDateVal <= auditDateVal) && (toDateVal >= auditDateVal) && userIdValue == '' && formIdValue == ''){	

				var tableRow = $('#templates .table-audittrail-list .tableRow');
				var clone = tableRow.clone();
				sno = sno + 1;
				$('.sno', clone).text(sno);
				$('.username', clone).text(getUserName(auditUser));
				$('.datetime', clone).text(auditDateValue);
				$('.formname', clone).text(getFormName(auditFormId));
				$('.action', clone).text(auditTrailList[key]['action']);
				$('.tbody-audittrail-list').append(clone);
			}
			//userid empty
			if((fromDateVal <= auditDateVal) && (toDateVal >= auditDateVal) && (userIdValue == '') && (formIdValue == auditFormId)){	

				var tableRow = $('#templates .table-audittrail-list .tableRow');
				var clone = tableRow.clone();
				sno = sno + 1;
				$('.sno', clone).text(sno);
				$('.username', clone).text(getUserName(auditUser));
				$('.datetime', clone).text(auditDateValue);
				$('.formname', clone).text(getFormName(auditFormId));
				$('.action', clone).text(auditTrailList[key]['action']);
				$('.tbody-audittrail-list').append(clone);
			}
			//formid empty
			if((fromDateVal <= auditDateVal) && (toDateVal >= auditDateVal) && userIdValue == auditUser && formIdValue == ''){	

				var tableRow = $('#templates .table-audittrail-list .tableRow');
				var clone = tableRow.clone();
				sno = sno + 1;
				$('.sno', clone).text(sno);
				$('.username', clone).text(getUserName(auditUser));
				$('.datetime', clone).text(auditDateValue);
				$('.formname', clone).text(getFormName(auditFormId));
				$('.action', clone).text(auditTrailList[key]['action']);
				$('.tbody-audittrail-list').append(clone);
			}
			//all != empty
			if((fromDateVal <= auditDateVal) && (toDateVal >= auditDateVal) && userIdValue == auditUser && formIdValue == auditFormId){	

				var tableRow = $('#templates .table-audittrail-list .tableRow');
				var clone = tableRow.clone();
				sno = sno + 1;
				$('.sno', clone).text(sno);
				$('.username', clone).text(getUserName(auditUser));
				$('.datetime', clone).text(auditDateValue);
				$('.formname', clone).text(getFormName(auditFormId));
				$('.action', clone).text(auditTrailList[key]['action']);
				$('.tbody-audittrail-list').append(clone);
			}

		});
	}
});
function hidemenu(){
	$("#userListView").hide(); 
}

$("#user").keyup(function(){
	var textval = $(this).val();
	$("#userListView").show();
	var users = userList;
	var suggestions = [];
	$('#userListView ul').empty();
	if(textval.length>0){
	    for(var i in users){
	    	if (~users[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([users[i]["user_id"],users[i]["employee_name"]]); 
	    }
	    var str='';
	    for(var i in suggestions){
	    	str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
	    }
	    $('#userListView ul').append(str);
	    $("#userid").val('');
	}
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#user").val(checkname);
  $("#userid").val(checkval);
}

function hideMenuFormList(){
	$("#formListView").hide(); 
}

$("#formname").keyup(function(){
	var textval = $(this).val();
	$("#formListView").show();
	var forms = formList;
	var suggestions = [];
	$('#formListView ul').empty();
	if(textval.length>0){
	    for(var i in forms){
	    	if (~forms[i]["form_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([forms[i]["form_id"],forms[i]["form_name"]]); 
	    }
	    var str='';
	    for(var i in suggestions){
	    	str += '<li id="'+suggestions[i][0]+'"onclick="activate_text1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
	    }
	    $('#formListView ul').append(str);
	    $("#formid").val('');
	}
});
//selectedt selected autocomplte value to textbox
function activate_text1 (element,checkval,checkname) {
  	$("#formname").val(checkname);
  	$("#formid").val(checkval);
}

$(function() {
	initialize();
});

