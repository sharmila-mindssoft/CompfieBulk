function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function getShortName(){
  var pathArray = window.location.pathname.split( '/' );
  console.log(pathArray)
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
  var pathArray = window.location.pathname.split( '/' );
  if (pathArray[1] === 'knowledge'){
    window.location.href='/knowledge/login';
  }else{
    window.location.href='/login/'+getShortName();
  }

});

function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( $email );
}

function processForgotpassword(username, shortName, callback) {
  var request = [
      "ForgotPassword", {
          "username": username,
          "short_name": null
      }
  ];
  if (shortName == null) {
      var requestFrame = request;
      BASE_URL = "/knowledge/api/"
  }
  else {
      var requestFrame = [
          shortName,
          request
      ];
      BASE_URL = "/api/"
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

$("#submit").click(function(){
  displayMessage("");
  var username = $("#username").val().trim();
  if(username.length == 0) {
    displayMessage(getMessage('username-required'));
  }else if(validateEmail(username) == ''){
    displayMessage(getMessage('invalid-emailid'));
  }else {

    function onSuccess(data){
      displayMessage(getMessage('forgotpassword-success'));
      $("#username").val("");
    }
    function onFailure(error){
      if(error == "InvalidUserName"){
        displayMessage(getMessage('nouser-exists'));
      }
    }

    if(getShortName() == null  || getShortName() == "forgot-password"){
        mirror.forgotPassword(username,
          function (error, response) {
            if (error == null){
              onSuccess(response);
            }
            else {
              onFailure(error);
            }
        }
      );
    }else{
        client_mirror.forgotPassword(username,
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

$(document).ready(function () {
  $("#username").focus();
});
