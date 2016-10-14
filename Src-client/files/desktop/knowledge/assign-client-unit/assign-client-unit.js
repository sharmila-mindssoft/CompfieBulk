
function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
      
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getUnassignedUnitsList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        loadGroups();
        loadLegalEntities();
        loadClientServers();
    }
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#view").show();
        $("#add").hide();
    }else{
        $("#view").hide();
        $("#add").show();
    }
}

$(function(){
	initialize("list");
});
