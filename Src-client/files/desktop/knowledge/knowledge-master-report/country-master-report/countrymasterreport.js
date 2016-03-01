function initialize(){
    function success(status, data){
        loadCountriesList(data);
    }
    function failure(status, data){
    }
    mirror.getCountryList(success, failure);
}

function loadCountriesList(countriesList){
    var sno=0;
    var title;
    for(var i in countriesList){
        var countries = countriesList[i];
        for(var j in countries){
            var isActive = countries[j]["is_active"];
            if(isActive == 1){ title = "Active"; }
            else { title = "Inactive"; }
            var tableRow = $('#templates .table-country-report .table-row');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.country-name', clone).text(countries[j]["country_name"]);
            $('.is-active', clone).text(title);
            $('.tbody-country-list').append(clone);     }
    }
    $("#total-records").html('Total : '+sno+' records');
}
$("#search-country-name").keyup(function() {
    var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".country-name").text().toLowerCase();
        $(this).toggle(id.indexOf(value) !== -1);;
    });
    count = $('tr:visible').length-3;
    $("#total-records").html('Total : '+count+' records');
});
$(function() {
    initialize();
});