$(function() {
	initialize();
});
function initialize(){
	function success(status, data){
		console.log(data);
		loadDomainList(data);
	}
	function failure(status, data){
	}
	mirror.getDomainList(success, failure);
}

function loadDomainList(domainList){
  	var sno=0;
	var title;	
	for(var i in domainList){
		var domains=domainList[i];
		for(var j in domains){
			var isActive=domains[j]["is_active"];
			if(isActive==1){ title="Active"; }
			else { title="Inacive"; }
			var tableRow=$('#templates .table-domain-report .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.domain-name', clone).text(domains[j]["domain_name"]);
			$('.is-active', clone).text(title);
			$('.tbody-domain-list').append(clone);			
		}
	
	}
	$("#total-records").html('Total : '+sno+' records');
}
$("#search-domain-name").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".domain-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
    count = $('tr:visible').length-3;
    $("#total-records").html('Total : '+count+' records');
});
