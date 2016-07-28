function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//check the url is client or knowledge
function getShortName(){
    var pathArray = window.location.pathname.split( '/' );
    short_name = null;
    if(typeof pathArray[2] === 'undefined'){
        short_name = null;
    }
    if (pathArray[1] == "knowledge") {
      short_name = null;
    }
    else if (pathArray[2] === "login") {
      short_name = null
    }
    else{
      short_name = pathArray[2]
    }
    return short_name
}

$(".btn-forgotpassword-cancel").click(function(){
  window.location.href='/knowledge/login';
});

//validation email
function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( $email );
}

function processForgotpassword(username, shortName, callback) {
  if (shortName == null) {
      var request = [
        "ForgotPassword", {
            "username": username,
            "short_name": null
        }
      ];
      var requestFrame = request;
      BASE_URL = "/knowledge/api/"
  }
  
  jQuery.post(
      BASE_URL + "login",
      JSON.stringify(requestFrame, null, " "),
      function (data) {
          var data = JSON.parse(data);
          var status = data[0];
          var response = data[1];
          matchString = 'success';
          if (status.toLowerCase().indexOf(matchString) != -1){
              callback(null, response);
          }
          else {
              callback(status, null);
          }
      }
  );
}

//submit forgot password process
$("#submit").click(function(){
  displayMessage("");
  var username = $("#username").val().trim();
  if(username.length == 0) {
    displayMessage(message.username_required);
  }
  else if(validateEmail(username) == ''){
    displayMessage(message.invalid_emailid);
  }else {
      displayLoader();
      function onSuccess(data){
        displayMessage(message.forgotpassword_success);
        $("#username").val("");
        hideLoader();
      }
      function onFailure(error){
        if(error == "InvalidUserName"){
          displayMessage(message.nouser_exists);
        }else{
          displayMessage(error);
        }
        hideLoader();
      }

      if(getShortName() == null  || getShortName() == "forgot-password"){
          processForgotpassword(username,
            null,
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

//initialization
$(document).ready(function () {
  $("#username").focus();
});
