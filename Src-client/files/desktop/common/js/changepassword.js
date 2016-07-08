//save change password process for knowledge
$("#submit").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage(message.cpassword_required);
  } else if(newpassword.length == 0) {
    displayMessage(message.npassword_required);
  } else if(confirmpassword.length == 0) {
    displayMessage(message.conpassword_required);
  } else if(confirmpassword != newpassword) {
    displayMessage(message.password_notmatch);
  } else {
      function onSuccess(data){
        alert("Password Changed Successfully.");
        frms = window.location.href.split("/");
        if (frms.indexOf("knowledge") == -1) {
          client_mirror.logout();
        }
        else {
          mirror.logout();
        }
      }
      function onFailure(error){
        if(error == "InvalidCurrentPassword"){
          displayMessage(message.invalid_cpassword);
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

//save change password process for client
$("#submit-client").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage(message.cpassword_required);
  } else if(newpassword.length == 0) {
    displayMessage(message.npassword_required);
  } else if(confirmpassword.length == 0) {
    displayMessage(message.conpassword_require);
  } else if(confirmpassword != newpassword) {
    displayMessage(message.password_notmatch);
  } else {
      function onSuccess(data){
        alert("Password Changed Successfully.");
        frms = window.location.href.split("/");
        if (frms.indexOf("knowledge") == -1) {
          client_mirror.logout();
        }
        else {
          mirror.logout();
        }
      }
      function onFailure(error){
        if(error == "InvalidCurrentPassword"){
          displayMessage(message.invalid_cpassword);
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

function getItemObject (form_url, form_name) {
  var itemObject = $("#nav-bar-templates .sub-menu-item li").clone();
  if (form_url !== null)
      $(".menu-url", itemObject).attr("href", form_url);
  $(".menu-item", itemObject).text(form_name);
  return itemObject;
}

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