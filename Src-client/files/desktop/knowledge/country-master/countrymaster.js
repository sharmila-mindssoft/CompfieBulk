var counList;

$(".btn-country-add").click(function(){
    $("#country-add").show();
    $("#country-view").hide();
    $("#country-name").val('');
    $("#country-id").val('');
    displayMessage('');
});

$(".btn-country-cancel").click(function(){
    $("#country-add").hide();
    $("#country-view").show();
    $("#search-country-name").val("");
    loadCountriesList(counList);
});

//get countries list from api
function initialize(){
    function onSuccess(data){
        $("#search-country-name").val("");
        counList = data;
        loadCountriesList(data);
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getCountryList(
        function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        }
    );
}
//display cpuntry details in view page
function loadCountriesList(countriesList){
    $(".tbody-countries-list").find("tr").remove();
    var sno = 0;
    var imageName = null;
    var title = null;
    $.each(countriesList, function(i, value){
        var countries = countriesList[i];
        $.each(countries, function(j, value){
            var countryId = countries[j]["country_id"];
            var countryName = countries[j]["country_name"];
            var isActive = countries[j]["is_active"];
            if(isActive == true){
                imageName = "icon-active.png";
                title = "Click here to deactivate"
                statusVal = false;
            }
            else{
                imageName = "icon-inactive.png";
                title = "Click here to Activate"
                statusVal = true;
            }
            var tableRow = $('#templates .table-countries-list .table-row');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.country-name', clone).text(countryName);
            $('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="country_edit('+countryId+',\''+countryName+'\')"/>');
            $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="country_active('+countryId+', '+statusVal+')"/>');
            $('.tbody-countries-list').append(clone);
        });
    });
}
$('#country-name').keypress(function (e) {
    var countryNameValue = $("#country-name").val();
    if (e.which == 13 && $(this).val() != "") {
        jQuery('#submit').focus().click();
    }
});

//save/update country details
$("#submit").click(function(){
    var countryIdValue = $("#country-id").val();
    var countryNameValue = $("#country-name").val().trim();
    if(countryNameValue.length == 0){
        displayMessage(message.country_required);
    }
    else{
        if(countryIdValue == ''){
            function onSuccess(response){
                $("#country-add").hide();
                $("#country-view").show();
                $("#search-country-name").val("");
                initialize();
            }
            function onFailure(error){
                if(error == 'CountryNameAlreadyExists'){
                    displayMessage(message.countryname_exists);
                }
            }
            mirror.saveCountry(countryNameValue,
                function (error, response) {
                    if (error == null){
                        onSuccess(response);
                    }
                    else {
                        onFailure(error);
                    }
                }
            );
        }
        else{
            function onSuccess(response){
                $("#country-add").hide();
                $("#country-view").show();
                initialize();
            }
            function onFailure(error){
                if(error == 'InvalidCountryId') {
                    displayMessage(message.countryname_invalid);
                }
                if(error == 'CountryNameAlreadyExists'){
                    displayMessage(message.countryname_exists);
                }
            }
            mirror.updateCountry(parseInt(countryIdValue), countryNameValue,
                function (error, response) {
                    if (error == null){
                        onSuccess(response);
                    }
                    else {
                        onFailure(error);
                    }
                }
            );
        }
    }

});
//edit country
function country_edit(countryId, countryName){
    $("#country-view").hide();
    $("#country-add").show();
    clearMessage();
    $("#country-name").val(countryName);
    $("#country-id").val(countryId);
}
//activate/deactivate country
function country_active(countryId, isActive){
    var msgstatus='deactivate';
    if(isActive){
        msgstatus='activate';
    }
    var answer = confirm('Are you sure want to '+msgstatus+ '?');
    if (answer)
    {
        $("#country-id").val(countryId);
        function onSuccess(response){
            initialize();
        }
        function onFailure(error){
            alert(error)
        }
        mirror.changeCountryStatus( parseInt(countryId), isActive,
            function (error, response) {
                if (error == null){
                    onSuccess(response);
                }
                else {
                    onFailure(error);
                }
            }
        );
    }
}
//filter process
$("#search-country-name").keyup(function() {
    var count = 0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".country-name").text().toLowerCase();
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});
//initialization
$(function() {
    initialize();
});