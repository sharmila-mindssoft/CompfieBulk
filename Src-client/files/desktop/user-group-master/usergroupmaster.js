$("#btnUserGroupAdd").click(function(){
	$("#userGroupView").hide();
	$("#userGroupAdd").show();
	$("#formList").hide();
	clearMessage();
	$("#groupName").val('');
	$("#groupId").val('');
});
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}

function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
$("#btnUserGroupCancel").click(function(){
	$("#userGroupAdd").hide();
	$("#userGroupView").show();
});
function initialize(){
	function onSuccess(data){
		loadUserGroupdata(data['user_groups']);
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.getAdminUserGroupList(
		function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        }
	);
}

function loadUserGroupdata(userGroupList){
	$(".tbody-usergroups-list").find("tr").remove();
 	var sno=0;
	var imageName, title;
	for(var j in userGroupList){
		var form_type=userGroupList[j]["form_type"];
		var user_group_name=userGroupList[j]["user_group_name"];
		var isActive=userGroupList[j]["is_active"];
		var userGroupId=userGroupList[j]["user_group_id"];
				
		if(isActive==1){
			imageName="icon-active.png";
			title="Click here to deactivate"
			statusVal=0;
		}
		else{
			imageName="icon-inactive.png";	
			title="Click here to Activate"
			statusVal=1;
		}

		var tableRow=$('#templates .table-usergroup-list .table-row');
		var clone=tableRow.clone();
		sno = sno + 1;
		$('.sno', clone).text(sno);
		$('.group-name', clone).text(user_group_name);
		$('.catg-name', clone).text(form_type);
		$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="userGroupEdit('+userGroupId+',\''+user_group_name+'\', \''+form_type+'\')"/>');
		$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="userGroupActive('+userGroupId+', '+statusVal+')"/>');
		$('.tbody-usergroups-list').append(clone);			
	}
}

$("#btnUserGroupShow").click(function(){
	var groupNameVal = $("#groupName").val();
	var categoryNameVal = $("#categoryName").val();

	if(groupNameVal=='' || groupNameVal==null){
		$(".error-message").html('Group Name Required');
	}
	else{
		$(".error-message").html('');
		$("#formList").show();
		function onSuccess( data){
			loadFormList(data['forms'], categoryNameVal);			
		}
		function onFailure(error){
			if(error == "GroupNameAlreadyExists"){
				displayMessage("Group Name Already Exists")
			}
		}
		mirror.getAdminUserGroupList(
			function (error, response) {
	            if (error == null){
	                onSuccess(response);
	            }
	            else {
	                onFailure(error);
	            }
	        }
		);
	}
});
function loadFormList(formList,categoryNameVal){
	$(".tableFormList").find("tr:gt(0)").remove();
	$('.checkedFormId').prop("checked", false);
	var i_incre;
	var tableRowList=$('#templates-form-heading .table-form-heading .table-row-form-heading');
	var clone1=tableRowList.clone();	
	$.each(formList[categoryNameVal], function(key, value){
		$('.formHeading', clone1).text(key);
		if(value.length!=0){
			$('.tableFormList').append(clone1);
		}
		$.each(value, function(i) { 
			var formName=value[i]['form_name'];
			var formId=value[i]['form_id'];
			var tableRowForms=$('#templates-form-list .table-form-list .table-row-form');
			var clone2=tableRowForms.clone();
			$('.checkbox-val', clone2).html('<input type="checkbox" class="checkedFormId" value="'+value[i]['form_id']+'">');
			$('.form-name', clone2).html(formName);		
			$('.tableFormList').append(clone2);	
		});
	});
}
function loadFormListUpdate(formList, userGroupList, categoryNameVal, userGroupId){
	$(".tableFormList").find("tr:gt(0)").remove();
	$('.checkedFormId').prop("checked", false);

	var i_incre;
	var tableRowList=$('#templates-form-heading .table-form-heading .table-row-form-heading');
	var clone1=tableRowList.clone();	
	$.each(formList[categoryNameVal], function(key, value){
		$('.formHeading', clone1).text(key);
		if(value.length!=0){
			$('.tableFormList').append(clone1);
		}
		$.each(value, function(i) { 
			var formName=value[i]['form_name'];
			var formId=value[i]['form_id'];
			var tableRowForms=$('#templates-form-list .table-form-list .table-row-form');
			var clone2=tableRowForms.clone();
			$('.checkbox-val', clone2).html('<input type="checkbox" class="checkedFormId" value="'+value[i]['form_id']+'">');
			$('.form-name', clone2).text(formName);		
			$('.tableFormList').append(clone2);	
		});
	});

	for(var userGroupDetails in userGroupList){	
		if(userGroupList[userGroupDetails]['user_group_id'] == userGroupId){
			var formIds=userGroupList[userGroupDetails]['form_ids'];
			for(var i=0; i<formIds.length; i++){
				$('.checkedFormId[value="'+formIds[i]+'"]').prop("checked", true);
			}
		}
	}
}
$("#btnUserGroupSubmit").click(function(){
	var groupIdVal = $("#groupId").val();
	var groupNameVal = $("#groupName").val();
	var categoryNameVal = $("#categoryName").val();
	var chkArray = [];
	if(groupIdVal==''){
		$(".checkedFormId:checked").each(function() {
			chkArray.push($(this).val());
		});	
		/* join array separated by comma*/
		var selectedVal;
		selectedVal = chkArray.join(',') + ",";
		function success(status, data){
			if(status=="SaveUserGroupSuccess"){
				$("#userGroupAdd").hide();
		  		$("#userGroupView").show();
				initialize();
			}
			if(status=="GroupNameAlreadyExists"){
				$(".error-message").html(status);
			}
		}
		function failure(status, data){
		}
		var userGroupInsertDetails=[groupNameVal,categoryNameVal, selectedVal];
		mirror.saveAdminUserGroup(userGroupInsertDetails, 
		   function (error, response) {
                if (error == null){
                  onSuccess(response);
                }
                else {
                  onFailure(error);
                }
            }
        );
	}
	if(groupIdVal!=''){
		$(".checkedFormId:checked").each(function() {
			chkArray.push($(this).val());
		});	
		/* join array separated by comma*/
		var selectedVal;
		selectedVal = chkArray.join(',') + ",";
		function onSuccess(status){
			if(status=="UpdateUserGroupSuccess"){
				$("#userGroupAdd").hide();
		  		$("#userGroupView").show();
				initialize();
			}
			
		}
		function onFailure(error){
			if(error=="GroupNameAlreadyExists"){
				displayMessage("Group Name Already Exists");
			}
		}
		var userGroupInsertDetails=[parseInt(groupIdVal), groupNameVal, categoryNameVal, selectedVal];
		mirror.updateAdminUserGroup(userGroupInsertDetails,
		    function (error, response) {
                if (error == null){
                  onSuccess(response);
                }
                else {
                  onFailure(error);
                }
            }
        );
	}
	
});
function userGroupEdit(userGroupId, userGroupName, formType){
	$("#userGroupAdd").show();
	$("#userGroupView").hide();
	$("#groupId").val(userGroupId);
	$("#groupName").val(userGroupName);
 	$("#userGroupId").val(formType);  
 	//$("#formList").show();	
 	function success(status, data){
		if(status=="GetUserGroupsSuccess"){
			loadFormListUpdate(data['forms'],data['user_groups'], formType, userGroupId);			
		}
	}
	function failure(status, data){
	}
	mirror.getAdminUserGroupList("AdminAPI", success, failure);
}
function userGroupActive(userGroupId, isActive){
  	$("#userGroupId").val(userGroupId);
  	function success(status, data){
		initialize();
	}
	function failure(status, data){
	}
	mirror.changeAdminUserGroupStatus("AdminAPI", userGroupId, isActive, success, failure);
}

$("#groupNameSearch").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".group-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
   
});
$("#categoryNameSearch").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".catg-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
   
});
$('.checkbox-full-check').click(function(event) {  
	if(this.checked) { 
	  $('.checkedFormId').each(function() { 
	    this.checked = true;  
	  });
	}else{
	  $('.checkedFormId').each(function() {
	    this.checked = false; 
	  });        
	}
});

$(function() {
	initialize();
});
