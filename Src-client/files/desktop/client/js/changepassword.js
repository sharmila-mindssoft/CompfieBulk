var passwordStrength = 'Weak';

//save change password process for client
$("#submit-client").click(function(){
  displayMessage("");
  var checkLength = changePasswordValidate();

  if(checkLength){
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
    } else if(passwordStrength == 'Weak') {
      displayMessage(message.password_weak);
    } else {
        function onSuccess(data){
          custom_alert("Password Changed Successfully.");
          client_mirror.logout();   
        }
        function onFailure(error){
          if(error == "InvalidCurrentPassword"){
            displayMessage(message.invalid_cpassword);
          }else{
            displayMessage(error);
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
      /*
        assigning keyup event to password field
        so everytime user type code will execute
      */
      passwordStrength = checkStrength($('#newpassword').val());
      if(passwordStrength == 'Strong'){
        $("#password-hint").css('display', 'none');
      }else{
        $("#password-hint").css('display', 'inline-block');
      }
      $('#pw-result').html(passwordStrength);

  });
  $('#confirmpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });
});

$("#newpassword").focus(function(){
  $("#password-hint").css('display', 'inline-block');
});

$("#newpassword").focusout(function(){
  $("#password-hint").css('display', 'none');
});