$(function() {
	$("#userGroupAdd").hide();
	initialize();
});
$("#btnUserGroupAdd").click(function(){
	$("#userGroupAdd").show();
	$("#userGroupView").hide();
	//$("#countryName").val('');
	//$("#countryId").val('');
  	$(".error-message").html('');
  	mirror.getAdminUserGroupList("AdminAPI", success, failure);
	function success(status, data){
		for(var i in data){
			loadsuccessdata(data['user_groups'])
		}
	}
	function failure(status, data){
		for(var i in data){
			//alert(data[i]);
		}
	}
});
$("#btnUserGroupCancel").click(function(){
	$("#userGroupAdd").hide();
	$("#userGroupView").show();
});
function initialize(){
	mirror.getAdminUserGroupList("AdminAPI", success, failure);
	function success(status, data){
		for(var i in data){
			loadsuccessdata(data['user_groups'])
		}
	}
	function failure(status, data){
		for(var i in data){
			//alert(data[i]);
		}
	}

}

function loadsuccessdata(userGroupList){
	
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
		mirror.getAdminUserGroupList("AdminAPI", success, failure);
		function success(status, data){
			for(var i in data){
				loadFormList(data['forms'])
			}
		}
	}
});
function loadFormList(formList){
	for(var catgList in formList){
		
	}
}
function userGroupEdit(countryId, countryName){
	$("#country-add").show();
	$("#country-view").hide();
	$("#countryName").val(countryName);
  	$("#countryId").val(countryId);
}
function userGroupActive(userGroupId, isActive){
  	$("#userGroupId").val( userGroupId);
  	mirror.changeAdminUserGroupStatus("AdminAPI", userGroupId, isActive, success, failure);

	function success(status, data){
		initialize();
	}
	function failure(status, data){
		
	}

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
