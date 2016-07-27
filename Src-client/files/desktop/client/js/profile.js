function initialize(){
    var userprofile = client_mirror.getUserProfile();
    clearMessage();
    var contactNo = (userprofile['contact_no']).split('-');
    $('.employee-name').text(userprofile['employee_name']);

    if(userprofile['designation'] == null || userprofile['designation'] == "None" ){
        $('.designation').text("");
    }
    else{
        $('.designation').text(userprofile['designation']);         
    }   
    $('.email-id').text(userprofile['email_id']);
    $('.countrycode').val(contactNo[0]);
    $('.areacode').val(contactNo[1]);
    $('.mobile').val(contactNo[2]);
    $('.employee-id').text(userprofile['employee_code']);
    $('.usergroup').text(userprofile['user_group']);
    
    if(userprofile['address'] == null || userprofile['address'] == "None" ){
        $('.textarea.address').val("");
    }
    else{
        $('textarea.address').val(userprofile['address']);      
    }       
    $('.userid').val(userprofile['user_id']);
}
$('.countrycode').on('input', function (event) {   
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('.areacode').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('.mobile').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$("#submit").click(function(){
    var checkLength = profileValidate();
    if(checkLength){
        var countrycode = $(".countrycode").val().trim();
        var areacode = $(".areacode").val().trim();
        var mobile = $(".mobile").val().trim();
        var address = $(".address").val().trim();
       
        function onSuccess(data){
            initialize();
            displayMessage(message.updated_success);
        }
        function onFailure(error){
            displayMessage(error);
        }
        client_mirror.updateUserProfile( countrycode+"-"+areacode+"-"+mobile, address,
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

$(function() {
    initialize();
});

