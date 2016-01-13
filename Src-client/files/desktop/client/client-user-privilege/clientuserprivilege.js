function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
$("#btn-userprivilege-add").click(function(){
	$("#userprivilege-view").hide();
	$("#userprivilege-add").show();
	clearMessage(); 
  	$("#user-privilege-id").val('');
  	$("#user-privilege-name").val('');
	$('.form-checkbox').each(function() {
		this.checked = false; 
	});  	
	function onSuccess(data){
		loadUserGroupdata(data['user_groups']);
		loadFormData(data['forms']['menus'])		
	}
	function onFailure(error){
		console.log(status);
	}
	client_mirror.getClientUserGroups(
		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
});
function loadFormData(formlist){
	$.each(formlist, function(key, value) {  
		var tableRowHeading = $('#templates-form-list .table-userprivilege-form-list .table-row-heading');
		var clone=tableRowHeading.clone();
		$('.heading-name', clone).text(key);
		if(value.length != 0){
			$('.tbody-userprivilege-form-list').append(clone);
		}
		$.each(value, function(i) { 
			var formName = value[i]['form_name'];
			var formId = value[i]['form_id'];
			var tableRowForms = $('#templates-form-list .table-userprivilege-form-list .table-row-form-list');
			var clone1 = tableRowForms.clone();
			$('.form-checkbox', clone1).val(formId);
			$('.form-name', clone1).text(formName);		
			$('.tbody-userprivilege-form-list').append(clone1);	
		});
	});
}
$("#btn-userprivilege-cancel").click(function(){
	$("#userprivilege-add").hide();
	$("#userprivilege-view").show();
});
function initialize(){
	function onSuccess(data){
		loadUserGroupdata(data['user_groups']);
	}
	function onFailure(status, data){
		console.log(status);
	}
	client_mirror.getClientUserGroups(
		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}

function loadUserGroupdata(userGroupList){
	$(".tbody-userprivilege-list").find("tr").remove();
 	var sno = 0;
	var imageName, title;
	for(var j in userGroupList){
		var user_group_name = userGroupList[j]["user_group_name"];
		var isActive = userGroupList[j]["is_active"];
		var userGroupId = userGroupList[j]["user_group_id"];
				
		if(isActive == true){
			imageName = "icon-active.png";
			title = "Click here to deactivate"
			statusVal = false;
		}
		else{
			imageName = "icon-inactive.png";	
			title = "Click here to Activate"
			statusVal = true;
		}

		var tableRow = $('#templates .table-userprivilege-list .table-row');
		var clone = tableRow.clone();
		sno = sno + 1;
		$('.sno', clone).text(sno);
		$('.usergroup-name', clone).text(user_group_name);
		$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="userPrivilegeEdit('+userGroupId+',\''+user_group_name+'\')"/>');
		$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="userPrivilegeActive('+userGroupId+', '+statusVal+')"/>');
		$('.tbody-userprivilege-list').append(clone);			
	}
}

$("#submit").click(function(){
	var groupIdVal = $("#user-privilege-id").val();
	var groupNameVal = $("#user-privilege-name").val();
	var chkArray = [];
	$(".form-checkbox:checked").each(function() {
		chkArray.push($(this).val());
	}); 
	
	if(groupNameVal == ''){
	  	displayMessage("Please Enter Group Name ");  	
	}
	else if(chkArray.length == 0){
		displayMessage("Please select atleast on form name ");  	 	
	}
	else if(groupIdVal == ''){
		chkArrayInt = chkArray.map(function(item) {
			return parseInt(item, 10);
		});
		function onSuccess(data){  
	    	$("#userprivilege-add").hide();
	   		$("#userprivilege-view").show();
	   		initialize();
	 	}
		function onFailure(error){
			if(error == "userGroupNameAlreadyExists"){
	   			displayMessage(error);
	  		}
		}
		var userGroupInsertDetails;
		userGroupInsertDetails = client_mirror.getSaveClientUserGroupDict(groupNameVal, chkArrayInt)
		client_mirror.saveClientUserGroup(userGroupInsertDetails,
			function (error, response){
				if(error == null){
					onSuccess(response);
				}
				else{
					onFailure(error);
				}
			}
		);
	}
	if(groupIdVal != ''){
		chkArrayInt = chkArray.map(function(item) {
	   		return parseInt(item, 10);
		});
		function onSuccess(data){
		    $("#userprivilege-add").hide();
		    $("#userprivilege-view").show();
		    initialize();
		}
		function onFailure(error){
			if(error == "GroupNameAlreadyExists"){
				displayMessage("Group Name Already Exists");
			}
		}
		var userGroupUpdateDetails;
		userGroupUpdateDetails = client_mirror.getUpdateClientUserGroupDict(parseInt(groupIdVal), groupNameVal, chkArrayInt);
		client_mirror.updateClientUserGroup(userGroupUpdateDetails,
			function (error, response){
				if(error == null){
					onSuccess(response);
				}
				else{
					onFailure(error);
				}
			}
		);
	}

});
function userPrivilegeEdit(userGroupId, userGroupName){
	$("#userprivilege-add").show();
	$("#userprivilege-view").hide();
	$("#user-privilege-name").val(userGroupName);
	$("#user-privilege-id").val(userGroupId);  
	function onSuccess(data){
		loadFormListUpdate(data['forms']['menus'], data['user_groups'], userGroupId);     
	}
	function onFailure(error){
		console.log(error);
	}
	client_mirror.getClientUserGroups(
		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}
function loadFormListUpdate(formList, userGroupList, userGroupId){
	$.each(formList, function(key, value) {  
		var tableRowHeading=$('#templates-form-list .table-userprivilege-form-list .table-row-heading');
		var clone=tableRowHeading.clone();
		$('.heading-name', clone).text(key);
		if(value.length!=0){
			$('.tbody-userprivilege-form-list').append(clone);
		}
		$.each(value, function(i) { 
			var formName=value[i]['form_name'];
			var formId=value[i]['form_id'];
			var tableRowForms=$('#templates-form-list .table-userprivilege-form-list .table-row-form-list');
			var clone1=tableRowForms.clone();
			$('.form-checkbox', clone1).val(formId);
			$('.form-name', clone1).text(formName);		
			$('.tbody-userprivilege-form-list').append(clone1);	
		});
	});
	$.each(userGroupList, function(key, value){
		if(userGroupList[key]['user_group_id'] == userGroupId){
      var formIds=userGroupList[key]['form_ids'];
      for(var i=0; i<formIds.length; i++){
        $('.form-checkbox[value="'+formIds[i]+'"]').prop("checked", true);
      }
		}
	});
}
function userPrivilegeActive(userGroupId, isActive){
  	function onSuccess(data){
   		initialize();
  	}
  	function onFailure(error){
 	}
  	client_mirror.changeClientUserGroupStatus(userGroupId, isActive, 
  		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}
$("#search-user-group-name").keyup(function() { 
  var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".usergroup-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
   
});

$('.checkbox-full-check').click(function(event) {  
	if(this.checked) { 
		$('.form-checkbox').each(function() { 
			this.checked = true;  
	  	});
	}
	else{
	  $('.form-checkbox').each(function() {
	    this.checked = false; 
	  });        
	}
});
$(function() {
	initialize();
});