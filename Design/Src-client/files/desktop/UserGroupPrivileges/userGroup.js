$(function() {
	$("#userGroupAdd").hide();
	initialize();
});
$("#btnUserGroupAdd").click(function(){
	$("#userGroupAdd").show();
	$("#userGroupView").hide();
	$("#formList").hide();
  	$(".error-message").html('');
  	$("#groupName").val('');
  	$("#groupId").val('');
  	
	function success(status, data){
		loadUserGroupdata(data['user_groups']);		
	}
	function failure(status, data){
		
	}
	mirror.getAdminUserGroupList("AdminAPI", success, failure);
});
$("#btnUserGroupCancel").click(function(){
	$("#userGroupAdd").hide();
	$("#userGroupView").show();
});
function initialize(){
	function success(status, data){
		for(var i in data){
			loadUserGroupdata(data['user_groups'])
		}
	}
	function failure(status, data){
		for(var i in data){
			//alert(data[i]);
		}
	}
	mirror.getAdminUserGroupList("AdminAPI", success, failure);
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
		function success(status, data){
			if(status=="GetUserGroupsSuccess"){
				loadFormList(data['forms'], categoryNameVal);			
			}
		}
		function failure(status, data){
		}
		mirror.getAdminUserGroupList("AdminAPI", success, failure);
	}
});
function loadFormList(formList,categoryNameVal){
	$("#tableFormList").find("tr:gt(0)").remove();
	$('.checkedFormId').prop("checked", false);
	var i_incre;
	var tableFormList=document.getElementById("tableFormList");
	var tableRowFormList=document.getElementById("tableRowFormList");
	for(var headingList in formList[categoryNameVal]){
		var cloneFormList=tableRowFormList.cloneNode(true);
		cloneFormList.id = i_incre; 
		cloneFormList.cells[0].innerHTML = '<span class="formHeading">'+headingList+'<span>';
		tableFormList.appendChild(cloneFormList);	
		for(var list in formList[categoryNameVal][headingList]){
			var cloneList=tableRowFormList.cloneNode(true);
			cloneList.cells[0].innerHTML = '<input type="checkbox" class="checkedFormId" value="'+formList[categoryNameVal][headingList][list]['form_id']+'">';
			cloneList.cells[1].innerHTML = '<span class="formName">'+formList[categoryNameVal][headingList][list]['form_name']+'</span>';
			tableFormList.appendChild(cloneList);
			//$('#tableFormList tr:first').appendChild(cloneList);
		}
	}
}
function loadFormListUpdate(formList, userGroupList, categoryNameVal, userGroupId){
	$("#tableFormList").find("tr:gt(0)").remove();
	$('.checkedFormId').prop("checked", false);

	var i_incre;
	var tableFormList=document.getElementById("tableFormList");
	var tableRowFormList=document.getElementById("tableRowFormList");
	for(var headingList in formList[categoryNameVal]){
		var cloneFormList=tableRowFormList.cloneNode(true);
		cloneFormList.id = i_incre; 
		cloneFormList.cells[0].innerHTML = '<span class="formHeading">'+headingList+'<span>';
		tableFormList.appendChild(cloneFormList);	
		for(var list in formList[categoryNameVal][headingList]){
			var cloneList=tableRowFormList.cloneNode(true);
			cloneList.cells[0].innerHTML = '<input type="checkbox" class="checkedFormId" value="'+formList[categoryNameVal][headingList][list]['form_id']+'">';
			cloneList.cells[1].innerHTML = '<span class="formName">'+formList[categoryNameVal][headingList][list]['form_name']+'</span>';
			tableFormList.appendChild(cloneList);
			//$('#tableFormList tr:first').appendChild(cloneList);
		}
	}
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
		mirror.saveAdminUserGroup("AdminAPI", userGroupInsertDetails, success, failure);
	}
	if(groupIdVal!=''){
		$(".checkedFormId:checked").each(function() {
			chkArray.push($(this).val());
		});	
		/* join array separated by comma*/
		var selectedVal;
		selectedVal = chkArray.join(',') + ",";
		function success(status, data){
			console.log(status);
			if(status=="UpdateUserGroupSuccess"){
				$("#userGroupAdd").hide();
		  		$("#userGroupView").show();
				initialize();
			}
			if(status=="GroupNameAlreadyExists"){
				$(".error-message").html(status);
			}
		}
		function failure(status, data){
			console.log(status);
		}
		var userGroupInsertDetails=[parseInt(groupIdVal), groupNameVal, categoryNameVal, selectedVal];
		mirror.updateAdminUserGroup("AdminAPI", userGroupInsertDetails, success, failure);
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