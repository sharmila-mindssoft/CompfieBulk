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
		clone.cells[1].innerHTML=form_type;
		clone.cells[2].innerHTML=user_group_name;
		clone.cells[3].innerHTML='<img src="/images/icon-edit.png" id="editid" onclick="userGroupEdit('+userGroupId+',\''+user_group_name+'\')"/>';
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
			loadFormList(data['forms'], categoryNameVal)
		
		}
		function failure(status, data){
		}
		mirror.getAdminUserGroupList("AdminAPI", success, failure);
	}
});
function loadFormList(formList,categoryNameVal){
	var i_incre;
	var tableFormList=document.getElementById("tableFormList");
	var tableRowFormList=document.getElementById("tableRowFormList");
	
	
	console.log(formList[categoryNameVal]);
	for(var list in formList[categoryNameVal]){
		var cloneFormList=tableRowFormList.cloneNode(true);
		cloneFormList.id = i_incre; 
		cloneFormList.cells[0].innerHTML = '<input type="checkbox" name="formListChkBox" >';
		cloneFormList.cells[1].innerHTML = list;
		tableFormList.appendChild(cloneFormList);	
		console.log(list);
	}
	// for(var catgList in formList){		
	// //	console.log(catgList);
	// 	for(var list in catgList){
	// 		console.log(list);
	// 		// console.log(list['masters']);
			
	// 	}
	// }
	// //$('#tableRowFormList').hide();
	// cloneFormList.id = i_incre; 
	// 		cloneFormList.cells[0].innerHTML = '<input type="checkbox" name="formListChkBox" >';
	// 		cloneFormList.cells[1].innerHTML = catgList;
	// 		tableFormList.appendChild(cloneFormList);	
}
function userGroupEdit(userGroupId, userGroupName){
	$("#userGroupAdd").show();
	$("#userGroupView").hide();
	$("#userGroupName").val(userGroupName);
  	$("#userGroupId").val(userGroupId);
}
function userGroupActive(userGroupId, isActive){
  	$("#userGroupId").val( userGroupId);
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
