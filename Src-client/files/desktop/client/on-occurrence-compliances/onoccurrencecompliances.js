var compliancesList;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}



function startcompliance(){

 
}


function load_compliances (compliancesList) {
  var j = 1;
  $(".tbody-complainces-list").find("tbody").remove();
    for(var entity in compliancesList) {
      var tableRow = $('#head-templates .tbl_heading');
      var clone = tableRow.clone();
      $('.heading', clone).html(entity);
      $('.tbody-compliances-list').append(clone);
      
      var compliances = compliancesList[entity];
      for(var compliance in compliances){
        var complianceId = compliances[compliance]["compliance_id"];
        var tableRow1=$('#templates .table-compliances .table-row');
        var clone1=tableRow1.clone();
        $('.sno', clone1).text(j);
        $('.statutory', clone1).text(compliances[compliance]["compliance_name"]);
        $('.compliance-task', clone1).text(compliances[compliance]["statutory_provision"]);
        $('.description', clone1).text(compliances[compliance]["description"]);
        $('.duration', clone1).text(compliances[compliance]["complete_within_days"]);
        $('.startdate', clone1).html('<input type="text" id="startdate'+ complianceId +'" class="input-box"/>');
        $('.action', clone1).on("click", function(e){
            var startdate = $(".startdate", clone1).val();
            submitOnOccurence(complianceId, compliances[compliance]["complete_within_days"],
              startdate);
        });

        $('.tbody-compliances-list').append(clone1);
        j = j + 1;

        $("#startdate"+complianceId).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            onClose: function( selectedDate ) {
            $( "#startdate"+complianceId ).datepicker( "option", "minDate", selectedDate );
          }
        });
      }
    }
}
function submitOnOccurence(complianceId, complete_within_days,  startdate, unitId){
   function onSuccess(data){
    //load_firstwizard();
  }
  function onFailure(error){
    displayMessage(error)
  }
  client_mirror.startOnOccurrenceCompliance( complianceId, complete_within_days,  startdate, unitId, 
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


function getOnOccuranceCompliances () {
  function onSuccess(data){
    compliancesList = data["compliances"];
    load_compliances(compliancesList);
  }
  function onFailure(error){
  }
  client_mirror.getOnOccurrenceCompliances(
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

$(document).ready(function () {
  getOnOccuranceCompliances ();
});