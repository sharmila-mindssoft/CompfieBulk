$(function() {
	$("#userprivilege-add").hide();
	initialize();
});
$("#btn-userprivilege-add").click(function(){
	$("#userprivilege-add").show();
	$("#userprivilege-view").hide();
  $(".error-message").html('');  
  $("#user-privilege-id").val('');
  	
	function success(status, data){
		loadUserGroupdata(data['user_groups']);
		loadFormData(data['forms'])		
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUserGroups("ClientAdminAPI", success, failure);
});
function loadFormData(formlist){
	$.each(formlist, function(key, value) {  
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
}
$("#btn-userprivilege-cancel").click(function(){
	$("#userprivilege-add").hide();
	$("#userprivilege-view").show();
});
function initialize(){
	function success(status, data){
		for(var i in data){
			loadUserGroupdata(data['user_groups'])
		}
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUserGroups("ClientAdminAPI", success, failure);
}

function loadUserGroupdata(userGroupList){
	$(".tbody-userprivilege-list").find("tr").remove();
 	var sno=0;
	var imageName, title;
	for(var j in userGroupList){
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

		var tableRow=$('#templates .table-userprivilege-list .table-row');
		var clone=tableRow.clone();
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
  
  if(groupNameVal==''){
	  $(".error-message").html("Please Enter Group Name ");  	
  }
  else if(chkArray.length==0){
 		$(".error-message").html("Please select atlease on form name ");  	 	
  }
  else if(groupIdVal==''){
    var selectedVal;
    selectedVal = chkArray.join(',') + ",";
    function success(status, data){  
      if(status=="SaveUserGroupSuccess"){
        $("#userprivilege-add").hide();
        $("#userprivilege-view").show();
        initialize();
      }
      if(status=="userGroupNameAlreadyExists"){
        $(".error-message").html(status);
      }
    }
    function failure(status, data){
    }
    var userGroupInsertDetails={};
    userGroupInsertDetails['user_group_name']=groupNameVal;
    userGroupInsertDetails['form_type']="client";
    userGroupInsertDetails['form_ids']=chkArray;
    mirror.saveClientUserGroup("ClientAdminAPI", userGroupInsertDetails, success, failure);
  }
  if(groupIdVal!=''){
    var selectedVal;
    selectedVal = chkArray.join(',') + ",";
    function success(status, data){
      if(status=="UpdateUserGroupSuccess"){
        $("#userprivilege-add").hide();
        $("#userprivilege-view").show();
        initialize();
      }
      if(status=="GroupNameAlreadyExists"){
        $(".error-message").html(status);
      }
    }
    function failure(status, data){
      console.log(status);
    }
    var userGroupUpdateDetails={};
    userGroupUpdateDetails['user_group_id']=parseInt(groupIdVal);
    userGroupUpdateDetails['user_group_name']=groupNameVal;
    userGroupUpdateDetails['form_type']="client";
    userGroupUpdateDetails['form_ids']=chkArray;
    mirror.updateClientUserGroup("ClientAdminAPI", userGroupUpdateDetails, success, failure);
  }
  
});
function userPrivilegeEdit(userGroupId, userGroupName){
  $("#userprivilege-add").show();
  $("#userprivilege-view").hide();
  $("#user-privilege-name").val(userGroupName);
  $("#user-privilege-id").val(userGroupId);  
  function success(status, data){
    if(status=="GetUserGroupsSuccess"){
      loadFormListUpdate(data['forms'],data['user_groups'], userGroupId);     
    }
  }
  function failure(status, data){
  }
  mirror.getClientUserGroups("ClientAdminAPI", success, failure);
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
  function success(status, data){
    initialize();
  }
  function failure(status, data){
  }
  mirror.changeClientUserGroupStatus("ClientAdminAPI", userGroupId, isActive, success, failure);
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