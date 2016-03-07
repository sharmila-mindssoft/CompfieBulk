var businessGroupsList;
var legalEntitiesList;
var divisionsList;
var unitsList;

function initialize(){
	function onSuccess(data){
		businessGroupsList = data['business_groups'];
		legalEntitiesList = data['legal_entities'];
		divisionsList = data['divisions'];
		unitsList = data['units'];
		loadUnitClosureList(unitsList);
	}
	function onFailure(error){
		console.log(error);
	}
	client_mirror.getUnitClosureList(
		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}

function showPopup(unitId){
	$('#unitidval').val(unitId);
	$('.overlay').css("visibility","visible");
	$('.overlay').css("opacity","1");
	$('.popup-error-msg').html("");
	$('#password').html("");
}
$('.close').click(function(){
	$('#unitidval').val("");
	$('.overlay').css("visibility","hidden");
	$('.overlay').css("opacity","0");
});
function unit_close(){
	var unitidval=$('#unitidval').val();
	var password=$('#password').val();
	if(password==''){
		$('.popup-error-msg').html("Enter password");
	}
	else{
		function onSuccess(data){
			$('#unitidval').val("");
			$('.overlay').css("visibility","hidden");
			$('.overlay').css("opacity","0");
			initialize();
		}
		function onFailure(error){
			if(error == 'InvalidPassword'){
				$('.popup-error-msg').html("Enter Correct password");
				$('#password').val("");
			}
		}
		client_mirror.closeUnit(parseInt(unitidval), password,
			function (error, response){
				if(error == null){
					onSuccess(response);
				}
				else{
					onFailure(error);
				}
			}
		);
	}
}
function getBusinessGroupsName(businessgroupid){
	var businessGroupName;
	if(businessgroupid != null){
		$.each(businessGroupsList, function(key, value){
			if(businessGroupsList[key]['business_group_id'] == businessgroupid){
				businessGroupName = businessGroupsList[key]['business_group_name'];
			}
		});	
	}
	else{
		businessGroupName = '';
	}
	return businessGroupName;
}

function getLegalEntityName(legalentityid){
	var legalEntityName;
	if(legalentityid != null){
		$.each(legalEntitiesList, function(key, value){
			if(legalEntitiesList[key]['legal_entity_id'] == legalentityid){
				legalEntityName = legalEntitiesList[key]['legal_entity_name'];
			}
		});	
	}
	else{
		legalEntityName = '';
	}
	return legalEntityName;
}
function getDivisionName(divisionid){
	var divisionName;
	if(divisionid != null){
		$.each(divisionsList, function(key, value){
			if(divisionsList[key]['division_id'] == divisionid){
				divisionName = divisionsList[key]['division_name'];
			}
		});	
	}
	else{
		divisionName = '';
	}
	return divisionName;
}

function loadUnitClosureList(unitsListData){
 	$(".tbody-unitclosure-list").find("tr").remove();
 	var sno=0;
	var imageName, title;	
	$.each(unitsListData, function(k, values) { 
		var list=unitsListData[k];
		var bgroupid=list['business_group_id'];
		var lentityid=list['legal_entity_id'];
		var divisionid=list['division_id'];
		var unitName=list['unit_name'];	
		var unitId=list["unit_id"];
		var address=list["unit_address"];		
		var isClosed=list["is_active"];
					
		if(isClosed==0){
			imageName="deletebold.png";
			title="close"
			statusVal=0;
		}
		else{
			imageName="";	
			title=""
		}
		var tableRow=$('#templates .table-unitclosure-list .table-row');
		var clone=tableRow.clone();
		sno = sno + 1;
		$('.sno', clone).text(sno);
		$('.business-group', clone).text(getBusinessGroupsName(bgroupid));
		$('.legal-entity', clone).text(getLegalEntityName(lentityid));
		$('.division', clone).text(getDivisionName(divisionid));
		$('.unit', clone).text(unitName);
		$('.unit-address', clone).text(address);
		if(imageName==''){
			$('.is-active', clone).text('closed');	
		}
		else{
			$('.is-active', clone).html('<img src="/images/'+imageName+'" class="popupoverlay" onClick="showPopup('+unitId+')" title="'+title+'"/>');	
		}		
		$('.tbody-unitclosure-list').append(clone);
	});
}
$("#business-group-search").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".business-group").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#legalentity-search").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".legal-entity").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#division-search").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".division").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#unit-search").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".unit").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#address-search").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".unit-address").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});
$(function() {
	initialize();
});