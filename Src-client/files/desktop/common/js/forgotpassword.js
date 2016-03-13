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
    short_name = null;
    if(typeof pathArray[2] === 'undefined'){
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

$("#submit").click(function(){
    displayMessage("");
    var username = $("#username").val().trim();
    if(username.length == 0) {
      displayMessage("Username required");
    }else if(validateEmail(username) == ''){
      displayMessage("Invalid email id");
    }else {

        function onSuccess(data){
          displayMessage("Password reset link has been sent to your email Id");
          $("#username").val("");
        }
        function onFailure(error){
          if(error == "InvalidUserName"){
            displayMessage("No such user exists");
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
