var compliancesList;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}



function submitcompliance(){

  /*function onSuccess(data){
    load_firstwizard();
  }
  function onFailure(error){
    displayMessage(error)
  }
  client_mirror.saveAssignedComplianceFormData(assignComplianceCountryId, assignComplianceAssigneeId, 
    assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName, 
    assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance, 
    function (error, response) {
    if (error == null){
      onSuccess(response);
    }
    else {
      onFailure(error);
    }
  }
  );*/
}


function load_compliances (compliancesList) {
  var j = 1;
  var domainId = 0;
  $(".tbody-complainces-list").find("tr").remove();
    for(var entity in compliancesList) {
      domainId = domainsList[entity]["domain_id"];
      
      var tableRow=$('#templates .table-compliances .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.statutory', clone).text(domainName);
      $('.compliance-task', clone).text(j);
      $('.description', clone).text(j);
      $('.duration', clone).text(j);
      $('.startdate', clone).text(j);
      $('.action', clone).text(j);

      $('.tbody-compliances').append(clone);
      j = j + 1;
    }
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