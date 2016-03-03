
function initialize(){
	function success(status, data){
		loadStatNatureData(data);
	}
	function failure(status, data){
	}
	mirror.getStatutoryNatureList(success, failure);
}
function loadStatNatureData(statNatureList){
  	var sno = 0;
	var title;
	for(var i in statNatureList){
		var statNature = statNatureList[i];
		for(var j in statNature){
			var isActive = statNature[j]["is_active"];
			if(isActive == 1){ title = "Active"; }
			else { title = "Inacive"; }
			var tableRow = $('#templates .table-stat-nature-report .table-row');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.stat-nature-name', clone).text(statNature[j]["statutory_nature_name"]);
			$('.is-active', clone).text(title);
			$('.tbody-stat-nature-list').append(clone);
		}
	}
	$("#total-records").html('Total : '+sno+' records');
}
$("#search-stat-nature-name").keyup(function() {
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".stat-nature-name").text().toLowerCase();
        $(this).toggle(id.indexOf(value) !== -1);;
    });
    count = $('tr:visible').length-3;
    $("#total-records").html('Total : '+count+' records');
});

$(function() {
	initialize();
});