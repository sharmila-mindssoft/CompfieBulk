
$(document).ready(function(){
	GetStatutories();
});

function GetStatutories(){
	function success(status,data){
		alert(status);
		
	}
	function failure(data){
	}
	mirror.getStatutoryMappings(success, failure);
}
