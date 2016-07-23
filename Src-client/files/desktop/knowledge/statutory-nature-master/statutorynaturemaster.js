$("#btn-statutory-nature-add").click(function(){
    $("#statutory-nature-view").hide();
    $("#statutory-nature-add").show();
    $("#statutory-nature-name").val('');
    $("#statutory-nature-id").val('');
    displayMessage('');
    $("#statutory-nature-name").focus();

});
$("#btn-statutory-nature-cancel").click(function(){
    $("#statutory-nature-add").hide();
    $("#statutory-nature-view").show();
});
function initialize(){
    clearMessage();
    $('.filter-text-box').val();
    function onSuccess(data){
        loadStatNatureData(data);
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getStatutoryNatureList(function (error, response){
        if(error == null){
            onSuccess(response);
        }
        else{
            onFailure(error);
        }
    });
}
function loadStatNatureData(statNatureList){
  $(".tbody-statutory-nature-list").find("tr").remove();
    var sno = 0;
    for(var i in statNatureList){
        var statNature = statNatureList[i];
        $.each(statNature, function(key, value) {
            var statNatureName = value['statutory_nature_name'];
            var statNatureId = value['statutory_nature_id'];
            var statNatureActive = value['is_active'];
            var passStatus = null;
            var classValue = null;

            if(statNatureActive == true) {
              passStatus = false;
              classValue = "active-icon";
            }
            else {
              passStatus=true;
              classValue = "inactive-icon";
            }
            var tableRow = $('#templates .table-statutory-nature-list .table-row');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.statutory-nature-name', clone).text(statNatureName);
            
            $('.edit-icon').attr('title', 'Edit');
            $(".edit-icon", clone).on("click", function() {
                statNature_edit(statNatureId, statNatureName);
            });

            $(".status", clone).addClass(classValue);
            $('.active-icon').attr('title', 'Deactivate');
            $('.inactive-icon').attr('title', 'Activate');
            $(".status", clone).on("click", function() {
                statNature_active(statNatureId, passStatus);
            });

            $('.tbody-statutory-nature-list').append(clone);
        });
    }
}

$('#statutory-nature-name').keypress(function (e) {
    var statutoryNatureNameVal = $("#statutory-nature-name").val().trim();
    if (e.which == 13) {
        if(statutoryNatureNameVal == ''){
            displayMessage(message.statutorynature_required);
        }
        else{
            jQuery('#btn-statutory-nature-submit').focus().click();
        }
  }
});
$("#btn-statutory-nature-submit").click(function(){
    clearMessage();
    var statutoryNatureIdVal = $("#statutory-nature-id").val();
    var statutoryNatureNameVal = $("#statutory-nature-name").val().trim();
    
    var checkLength = statutoryNatureValidate();
    if(checkLength){
        if(statutoryNatureNameVal == ""){
            displayMessage(message.statutorynature_required);
        }
        else if(statutoryNatureIdVal == ''){
            function onSuccess(data){
                $("#statutory-nature-add").hide();
                $("#statutory-nature-view").show();
                $("#search-statutory-nature-name").val('');
                initialize();
            }
            function onFailure(error){
                if(error == 'StatutoryNatureNameAlreadyExists'){
                    displayMessage(message.statutoryname_exists);
                }
            }
            mirror.saveStatutoryNature(statutoryNatureNameVal, function (error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            });
        }
        else{
            function onSuccess(data){
                $("#statutory-nature-add").hide();
                $("#statutory-nature-view").show();
                $("#search-statutory-nature-name").val('');
                initialize();
                clearMessage();
            }
            function onFailure(error){
                if(error == 'InvalidStatutoryNatureId'){
                    displayMessage(message.stat_nature_invalid);
                }
                if(error == 'StatutoryNatureNameAlreadyExists'){
                    displayMessage(message.statutoryname_exists);
                }
            }
            mirror.updateStatutoryNature(parseInt(statutoryNatureIdVal), statutoryNatureNameVal,
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

    }
});
function statNature_edit(statNatureId, statNatureName){
    clearMessage();
    $("#statutory-nature-add").show();
    $("#statutory-nature-view").hide();
    $("#statutory-nature-name").val(statNatureName.replace(/##/gi,'"'));
    $("#statutory-nature-id").val(statNatureId);
    $("#statutory-nature-name").focus();
}
function statNature_active(statNatureId, isActive){
    var msgstatus='deactivate';
    if(isActive){
        msgstatus='activate';
    }
    var answer = confirm('Are you sure want to '+msgstatus+ '?');
    if (answer)
    {
        function success(status, data){
            $("#search-statutory-nature-name").val('');
            initialize();
        }
        function failure(error){
            alert(error)
        }
        mirror.changeStatutoryNatureStatus(parseInt(statNatureId), isActive, success, failure);
    }
}
$("#search-statutory-nature-name").keyup(function() {
    var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".statutory-nature-name").text().toLowerCase();
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});
$(function() {
    initialize();
});