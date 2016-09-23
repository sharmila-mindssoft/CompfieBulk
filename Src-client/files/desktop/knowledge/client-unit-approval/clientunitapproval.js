function initialize(){
  function onSuccess(data) {
 
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getClientUnitApprovalList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

//initialization
$(function () {
  initialize();
});