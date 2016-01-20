function initialize(){
	function onSuccess(status, data){
		loadUnitClosureList(data);
	}
	function onFailure(status, data){
	}
	client_mirror.getUnitClosureList( 
		function(error, response){
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
		$('.popup-error-msg').html("Please Enter password");
	}
	else{
		function success(status, data){
			if(status=='CloseUnitSuccess'){
				$('#unitidval').val("");
				$('.overlay').css("visibility","hidden");
				$('.overlay').css("opacity","0");
				initialize();	
			}
			if(status=='InvalidPassword'){
				$('.popup-error-msg').html("Enter Correct password");
				$('#password').val("");
			}
		}
		function failure(status, data){
			if(status=='InvalidPassword'){
				$('.popup-error-msg').html("Enter Correct password");
				$('#password').val("");
			}
			else{
				$('.popup-error-msg').html(status);	
			}
		}
		client_mirror.closeUnit(parseInt(unitidval), password, success, failure);
	}
}

function loadUnitClosureList(data){
 	$(".tbody-unitclosure-list").find("tr").remove();
 	var sno=0;
	var imageName, title;	
	$.each(data, function(k, values) { 
		var list=data[k];
		$.each(list, function(key, val) { 
			var bgroupName=list[key]['business_group_name'];
			var lentityName=list[key]['legal_entity_name'];
			var unitName=list[key]['unit_name'];
			var divisionName=list[key]['division_name'];
			var unitId=list[key]["unit_id"];
			var address=list[key]["address"];		
			var isActive=list[key]["is_active"];
						
			if(isActive==1){
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
			$('.business-group', clone).text(bgroupName);
			$('.legal-entity', clone).text(lentityName);
			$('.division', clone).text(divisionName);
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