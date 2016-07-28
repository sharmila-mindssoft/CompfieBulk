var domainsList;

$(".btn-domain-add").click(function(){
  $("#domain-view").hide();
  $("#domain-add").show();
  $("#domainname").val('');
  $("#domainid").val('');
  $(".error-message").html('');
  $("#domainname").focus();
});
$(".btn-domain-cancel").click(function(){
  $("#domain-add").hide();
  $("#domain-view").show();
});

//get domains list from api
function getDomains () {
  function onSuccess(data){
    domainsList = data["domains"];
    loadDomainList(domainsList);
  }
  function onFailure(error){
    custom_alert(error);
  }
  mirror.getDomainList(
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

//display domains list in view page
function loadDomainList (domainsList) {
  var j = 1;
  $(".tbody-domain-list1").find("tr").remove();

  $.each(domainsList, function(key, value) {
    var domainName = value["domain_name"];;
    var domainId = value["domain_id"];
    var isActive = value["is_active"];

    var passStatus = null;
    var classValue = null;

    if(isActive == true) {
      passStatus = false;
      classValue = "active-icon";
    }
    else {
      passStatus=true;
      classValue = "inactive-icon";
    }

    var tableRow = $('#templates .table-domain-master .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(j);
    $('.domain-name', clone).text(domainName);

    $('.edit-icon').attr('title', 'Edit');
    $(".edit-icon", clone).on("click", function() {
        displayEdit(domainId, domainName);
    });

    $(".status", clone).addClass(classValue);
    $('.active-icon').attr('title', 'Deactivate');
    $('.inactive-icon').attr('title', 'Activate');
    $(".status", clone).on("click", function() {
        changeStatus(domainId, passStatus);
    });

    $('.tbody-domain-list1').append(clone);
    j = j + 1;
  });
}

//validation
function validate(){
  var checkLength = domainValidate();
  if(checkLength){
    if($("#domainname").val().trim().length==0){
      displayMessage(message.domainname_required);
    }else{
      displayMessage('');
      return true
    }
  }
}

//save or update domain master
$("#submit").click(function(){
  var domainId = $("#domainid").val();
  var domainName = $("#domainname").val().trim();

if(validate()){
  if($("#domainid").val() == ''){
    function onSuccess(response) {
      getDomains ();
      $("#domain-add").hide();
      $("#domain-view").show();
      $("#search-domain-name").val('');
    }    function onFailure(error){

        if(error == "DomainNameAlreadyExists"){
            displayMessage(message.domainname_exists);
        }else{
          displayMessage(error);
        }
    }
    mirror.saveDomain(domainName,
    function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
  }
  else{
    function onSuccess(response){
      getDomains();
      $("#domain-add").hide();
      $("#domain-view").show();
      $("#search-domain-name").val('');
      }
    function onFailure(error) {
        if(error == "InvalidDomainId"){
            displayMessage(message.invalid_domainid);
        }

        else if(error == 'DomainNameAlreadyExists'){
            displayMessage(message.domainname_exists);
        }
        else{
          displayMessage(error);
        }
    }
    mirror.updateDomain(parseInt(domainId), domainName,
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      });
  }
}
});

//save or update domain master when press enter key
$('#domainname').keypress(function (e) {
  if (e.which == 13) {
    if(validate()){
      jQuery('#submit').focus().click();
    }
  }
});

//edit domain master
function displayEdit (domainId,domainName) {
  $(".error-message").text("");
  $("#domain-view").hide();
  $("#domain-add").show();
  $("#domainname").val(domainName.replace(/##/gi,'"'));
  $("#domainid").val(domainId);
}


//activate/deactivate domain master
function changeStatus (domainId,isActive) {

  var msgstatus = message.deactive_message;
  if(isActive){
      msgstatus = message.active_message;
  }
  $( ".warning-confirm" ).dialog({
      title: message.title_status_change,
      buttons: {
          Ok: function() {
            $( this ).dialog( "close" );

            function onSuccess(response){
              getDomains ();
              $("#search-domain-name").val('');
            }
            function onFailure(error){
              if(error == "TransactionExists"){
                  custom_alert(message.trasaction_exists)
              }else{
                  custom_alert(error)
              }
            }
            mirror.changeDomainStatus(domainId, isActive,
              function (error, response) {
                if (error == null){
                  onSuccess(response);
                }
                else {
                  onFailure(error);
                }
              });
          },
          Cancel: function() {
              $( this ).dialog( "close" );
          }
      },
      open: function ()  {
          $(".warning-message").html(msgstatus);
      }
  });
}

//filter process
$("#search-domain-name").keyup(function() {
  var filterkey = this.value.toLowerCase();
  var filteredList=[];
    for(var entity in domainsList) {
      domainName = domainsList[entity]["domain_name"];
      if (~domainName.toLowerCase().indexOf(filterkey)) filteredList.push(domainsList[entity]);
    }
  loadDomainList(filteredList);
});

//initialization
$(document).ready(function () {
  getDomains ();
  $("#domainname").focus();
});

$('#domainname').on('input', function (e) {
    this.value = isAlphabetic($(this));
});