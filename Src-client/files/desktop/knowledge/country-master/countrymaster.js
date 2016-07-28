var counList;

$(".btn-country-add").click(function(){
    $("#country-add").show();
    $("#country-view").hide();
    $("#country-name").val('');
    $("#country-id").val('');
    displayMessage('');
    // $("#country-name").focus();
    // $('#country-name').select();
    // $('#country-name').trigger('focus');
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
        custom_alert(error);
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
    
    $.each(countriesList, function(i, value){
        var countries = countriesList[i];
        $.each(countries, function(j, value){
            var countryId = countries[j]["country_id"];
            var countryName = countries[j]["country_name"];
            var isActive = countries[j]["is_active"];
            var passStatus = null;
            var classValue = null;

            if(isActive == true) {
              passStatus = false;
              classValue = "active-icon";
            }
            else {
              passStatus=true;
              classValue = "inactive-icon";
            }
            var tableRow = $('#templates .table-countries-list .table-row');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.country-name', clone).text(countryName);
            
            $('.edit-icon').attr('title', 'Edit');
            $(".edit-icon", clone).on("click", function() {
                country_edit(countryId, countryName);
            });

            $(".status", clone).addClass(classValue);
            $('.active-icon').attr('title', 'Deactivate');
            $('.inactive-icon').attr('title', 'Activate');
            $(".status", clone).on("click", function() {
                country_active(countryId, passStatus);
            });

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

    var checkLength = countryValidate();

    if(checkLength){
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
                    }else{
                        displayMessage(error);
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
                    else if(error == 'CountryNameAlreadyExists'){
                        displayMessage(message.countryname_exists);
                    }else{
                        displayMessage(error);
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
    }
});
//edit country
function country_edit(countryId, countryName){
    $("#country-view").hide();
    $("#country-add").show();
    clearMessage();
    $("#country-name").val(countryName.replace(/##/gi,'"'));
    $("#country-id").val(countryId);
}
//activate/deactivate country
function country_active(countryId, isActive){
    var msgstatus = message.deactive_message;
    if(isActive){
        msgstatus = message.active_message;
    }
    $( ".warning-confirm" ).dialog({
        title: message.title_status_change,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );
                $("#country-id").val(countryId);
                function onSuccess(response){
                    initialize();
                }
                function onFailure(error){
                    if(error == "TransactionExists"){
                        custom_alert(message.trasaction_exists)
                    }else{
                        custom_alert(error)
                    }
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
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        open: function ()  {
            $(".warning-message").html(msgstatus);
        }
    });
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

$('#country-name').on('input', function (e) {
    this.value = isAlphabetic($(this));
});