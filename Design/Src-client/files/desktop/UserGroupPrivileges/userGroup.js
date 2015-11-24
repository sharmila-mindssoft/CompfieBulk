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
	// saveUserGroupDetail = ["Knowledge User 1", "Knowledge" , "11,53"];
 	$('#tableRow').show();
  	$("#tableUserGroupList").find("tr:gt(0)").remove();
  	var sno=1;
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
		var tableName = document.getElementById("tableUserGroupList");
		var tableRow=document.getElementById('tableRow');
		var clone=tableRow.cloneNode(true);
		clone.id = sno; 

		clone.cells[0].innerHTML =sno;
		clone.cells[1].innerHTML=user_group_name;
		clone.cells[2].innerHTML=form_type;
		clone.cells[3].innerHTML='<img src="/images/icon-edit.png" id="editid" onclick="userGroupEdit('+userGroupId+',\''+user_group_name+'\', \''+form_type+'\')"/>';
		clone.cells[4].innerHTML='<img src="/images/'+imageName+'" title="'+title+'" onclick="userGroupActive('+userGroupId+', '+statusVal+')"/>';
		tableName.appendChild(clone);
  		sno = sno + 1;
	}
	$('#tableRow').hide();

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

function filter (term, cellNr){
	var suche = term.value.toLowerCase();
	var table = document.getElementById("tableCountriesList");
	var ele;
	for (var r = 1; r < table.rows.length; r++){
		ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
		if (ele.toLowerCase().indexOf(suche)>=0 )
			table.rows[r].style.display = '';
		else table.rows[r].style.display = 'none';
	}
}
