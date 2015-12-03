$(document).ready(function(){
	getStatutoryMappings()
});

function getStatutoryMappings(){
	function success(status,data){
		var industriesList = data["industries"];
		var statutoryLevelsList = data["statutory_levels"];
		var statutoriesList = data["statutories"];
		var countriesList = data["countries"];
		var domainsList = data["domains"];
		var geographyLevelsList = data["geography_levels"];
		var statutoryNaturesList = data["statutory_natures"];
		var geographiesList = data["geographies"];
		var statutoryMappingsList = data["statutory_mappings"];
		
		loadStatutoryMappingList(statutoryMappingsList);
	}
	function failure(data){
	}
	mirror.getStatutoryMappings(success, failure);
}
function loadStatutoryMappingList(statutoryMappingsList) {
	var j = 1;
	var imgName = '';
	var passStatus = '';
	var statutorymappingId = 0;
	var isActive = 0;
	var industryName = '';
	var statutoryNatureName = '';
	var countryName = '';
	var domainName = '';
	var approvalStatus = '';


	$(".tbody-statutorymapping-list").find("tr").remove();
	for(var entity in statutoryMappingsList) {
		statutorymappingId = entity;
        industryName = statutoryMappingsList[entity]["industry_names"];
        statutoryNatureName = statutoryMappingsList[entity]["statutory_nature_name"];        
        var statutoryMappings='';
        for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
        	statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
        }
        var complianceNames='';
        for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
        	complianceNames = complianceNames + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
        }
        statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
        countryName = statutoryMappingsList[entity]["country_name"];
        domainName = statutoryMappingsList[entity]["domain_name"];
        isActive = statutoryMappingsList[entity]["is_active"];
        approvalStatus = statutoryMappingsList[entity]["approval_status"];
        if(isActive == 1) {
          passStatus="0";
          imgName="icon-active.png"
        }
        else {
          passStatus="1";
          imgName="icon-inactive.png"
         }
         if(approvalStatus == '0'){
         	approvalStatus = "Pending";
         }
        var tableRow=$('#templates .table-statutorymapping .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(j);
        $('.country', clone).text(countryName);
        $('.domain', clone).text(domainName);
        $('.industry', clone).text(industryName);
        $('.statutorynature', clone).text(statutoryNatureName);
        $('.statutory', clone).html(statutoryMappings);
        $('.compliancetask', clone).html(complianceNames);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+statutorymappingId+')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+statutorymappingId+','+passStatus+')"/>');
        $('.approvalstatus', clone).text(approvalStatus);
        $('.tbody-statutorymapping-list').append(clone);
        j = j + 1;
      	}
      }

      function displayAdd () {
	    $("#error").text('');
	    $("#listview").hide();
	    $("#addview").show();
	}

	function changeStatus (userId,isActive) {
		/*mirror.changeAdminUserStatus("AdminAPI", userId, isActive, success, failure);
		function success(status,data){
			GetUsers();
			$("#error").text("Status Changed Successfully");
		}
		function failure(data){
		}*/
	}

	function filter (term, cellNr){
		var filterkey = term.value.toLowerCase();
		var table = document.getElementById("filter_statutorymapping");
		var ele;
		for (var r = 1; r < table.rows.length; r++){
			ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
			if (ele.toLowerCase().indexOf(filterkey)>=0 )
				table.rows[r].style.display = '';
			else table.rows[r].style.display = 'none';
		}
	} 