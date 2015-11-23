var tempStatutoryLevelsList;

$(document).ready(function(){
	GetStatutoryLevels()
});

function GetStatutoryLevels(){
	function success(status,data){
		tempStatutoryLevelsList = data["statutorylevels"];
		statutoryLevelsList = data["statutorylevels"];

		loadStatutoryLevelList(statutoryLevelsList);
	}
	function failure(data){
	}
	mirror.getAdminUserList("AdminAPI", success, failure);
}


function loadStatutoryLevelList(statutoryLevelsList) {
	  var j = 1;
	  var imgName = '';
    var passStatus = '';
    var userId = 0;
    var employeeName = '';
    var isActive = 0;
    var designation = '';
    var userList;

    $('#rowToClone').show();
    $("#tableToModify").find("tr:gt(0)").remove();
    for(var entity in usersList) {
    	userId = usersList[entity]["user_id"];
        employeeName = usersList[entity]["employee_name"];
        isActive = usersList[entity]["is_active"];
        designation = usersList[entity]["designation"];
        for(var k in userGroupsList){
        	if(userGroupsList[k]["user_group_id"] == usersList[entity]["user_group_id"]){
        		usergroup = userGroupsList[k]["user_group_name"];
        		break;
        	}
        }
        if(isActive == 1) {
        	passStatus="0";
        	imgName="icon-active.png"
        }
        else {
        	passStatus="1";
       	 	imgName="icon-inactive.png"
       	 }
       	 var row = document.getElementById("rowToClone"); 
      	 var table = document.getElementById("tableToModify");
      	 var clone = row.cloneNode(true);
       	 clone.id = j; 
      	 clone.cells[0].innerHTML = j;
      	 clone.cells[1].innerHTML = employeeName;
      	 clone.cells[2].innerHTML = usergroup;
       	 clone.cells[3].innerHTML = designation;
      	 clone.cells[4].innerHTML = '<img src=\'/images/icon-edit.png\' onclick="displayEdit('+userId+',\''+employeeName+'\')"/>'
      	 clone.cells[5].innerHTML = '<img src=\'/images/'+imgName+'\' onclick="changeStatus('+userId+','+passStatus+')"/>'
      	 table.appendChild(clone);
      	 j = j + 1;
      	}
      	$('#rowToClone').hide();
      }
