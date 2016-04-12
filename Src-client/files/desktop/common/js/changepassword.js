function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$("#submit").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage(getMessage('cpassword-required'));
  } else if(newpassword.length == 0) {
    displayMessage(getMessage('npassword-required'));
  } else if(confirmpassword.length == 0) {
    displayMessage(getMessage('conpassword-required'));
  } else if(confirmpassword != newpassword) {
    displayMessage(getMessage('password-notmatch'));
  } else {
      function onSuccess(data){
          displayMessage(getMessage('password-changed-success'));
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
      }
      function onFailure(error){
        if(error == "InvalidCurrentPassword"){
          displayMessage(getMessage('invalid-cpassword'));
        }
      }
      mirror.changePassword(currentpassword, newpassword, 
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
});

$("#submit-client").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage(getMessage('cpassword-required'));
  } else if(newpassword.length == 0) {
    displayMessage(getMessage('npassword-required'));
  } else if(confirmpassword.length == 0) {
    displayMessage(getMessage('conpassword-required'));
  } else if(confirmpassword != newpassword) {
    displayMessage(getMessage('password-notmatch'));
  } else {
      function onSuccess(data){
          displayMessage(getMessage('password-changed-success'));
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
      }
      function onFailure(error){
        if(error == "InvalidCurrentPassword"){
          displayMessage(getMessage('invalid-cpassword'));
        }
      }

      client_mirror.changePassword(currentpassword, newpassword, 
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
});

$(document).ready(function(){
  $("#currentpassword").focus();
  $('#currentpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });
  $('#newpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });
  $('#confirmpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });
});