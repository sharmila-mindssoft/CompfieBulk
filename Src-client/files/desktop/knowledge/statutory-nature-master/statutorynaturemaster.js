function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}

function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
$("#btn-statutory-nature-add").click(function(){
    $("#statutory-nature-view").hide();
    $("#statutory-nature-add").show();
    $("#statutory-nature-name").val('');
    $("#statutory-nature-id").val('');
    displayMessage('');
});
$("#btn-statutory-nature-cancel").click(function(){
    $("#statutory-nature-add").hide();
    $("#statutory-nature-view").show();
});
function initialize(){
    clearMessage();
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
        for(var j in statNature){
            var statNatureName = statNature[j]['statutory_nature_name'];
            var statNatureId = statNature[j]['statutory_nature_id'];
            var statNatureActive = statNature[j]['is_active'];
            if(statNatureActive == true){
                imageName = "icon-active.png";
                title = "Click here to deactivate";
                statusVal = false;
            }
            else{
                imageName = "icon-inactive.png";
                title = "Click here to Activate";
                statusVal = true;
            }
            var tableRow = $('#templates .table-statutory-nature-list .table-row');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.statutory-nature-name', clone).text(statNatureName);
            $('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="statNature_edit('+statNatureId+',\''+statNatureName+'\')"/>');
            $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="statNature_active('+statNatureId+', '+statusVal+')"/>');
            $('.tbody-statutory-nature-list').append(clone);
        }
    }
}

$('#statutory-nature-name').keypress(function (e) {
    var statutoryNatureNameVal = $("#statutory-nature-name").val().trim();
    if (e.which == 13) {
        if(statutoryNatureNameVal == ''){
            displayMessage('Statutory Nature Name Required');
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
    if(statutoryNatureNameVal == ""){
        displayMessage('Statutory Nature Name Required');
    }
    else if (statutoryNatureNameVal.length > 50) {
        displayMessage('Not Extended 50 Characters');
    }
    else if(statutoryNatureIdVal == ''){
        function onSuccess(data){
            $("#statutory-nature-add").hide();
            $("#statutory-nature-view").show();
            initialize();
        }
        function onFailure(error){
            if(error == 'StatutoryNatureNameAlreadyExists'){
                displayMessage('Statutory Nature Name Already Exists');
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
            initialize();
            clearMessage();
        }
        function onFailure(error){
            if(error == 'InvalidStatutoryNatureId'){
                displayMessage('Invalid Statutory Nature Name');
            }
            if(error == 'StatutoryNatureNameAlreadyExists'){
                displayMessage('Statutory Nature Name Already Exists');
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
});
function statNature_edit(statNatureId, statNatureName){
    clearMessage();
    $("#statutory-nature-add").show();
    $("#statutory-nature-view").hide();
    $("#statutory-nature-name").val(statNatureName);
    $("#statutory-nature-id").val(statNatureId);
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
            initialize();
        }
        function failure(status, data){
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