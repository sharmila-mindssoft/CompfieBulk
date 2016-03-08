var domainsList;
function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}
$(".btn-domain-add").click(function(){
  $("#domain-view").hide();
  $("#domain-add").show();
  $("#domainname").val('');
  $("#domainid").val('');
  $(".error-message").html('');
});
$(".btn-domain-cancel").click(function(){
  $("#domain-add").hide();
  $("#domain-view").show();
});

function getDomains () {
  function onSuccess(data){
    domainsList = data["domains"];
    loadDomainList(domainsList);
  }
  function onFailure(error){
    displayMessage(error);
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

function loadDomainList (domainsList) {
  var j = 1;
  var imgName = null;
  var passStatus = null;
  var domainId = 0;
  var domainName = null;
  var isActive = false;
  $(".tbody-domain-list1").find("tr").remove();
    for(var entity in domainsList) {
      domainId = domainsList[entity]["domain_id"];
      domainName = domainsList[entity]["domain_name"];
      isActive = domainsList[entity]["is_active"];
      if(isActive == true) {
        passStatus=false;
        imgName="icon-active.png"
      }
      else {
        passStatus=true;
        imgName="icon-inactive.png"
      }
      var tableRow=$('#templates .table-domain-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.domain-name', clone).text(domainName);
      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+domainId+',\''+domainName+'\')"/>');
      $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+domainId+','+passStatus+')"/>');
      $('.tbody-domain-list1').append(clone);
      j = j + 1;
    }
}

function validate(){
  if($("#domainname").val().trim().length==0){
    displayMessage('Domain Name Required');
  }else{
    displayMessage('');
    return true
  }
}

$("#submit").click(function(){
  var domainId = $("#domainid").val();
  var domainName = $("#domainname").val().trim();

if(validate()){
  if($("#domainid").val() == ''){
    function onSuccess(response) {
      getDomains ();
      $("#domain-add").hide();
      $("#domain-view").show();
    }    function onFailure(error){
                      
        if(error == "DomainNameAlreadyExists"){
            displayMessage("Domain Name Already Exists");
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
      }
    function onFailure(error) {
        if(error == "InvalidDomainId"){
            displayMessage("Invalid Domain Id");
        }  

        if(error == 'DomainNameAlreadyExists'){
            displayMessage("Domain Name Already Exists");
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

$('#domainname').keypress(function (e) {
  if (e.which == 13) {
    if(validate()){
      jQuery('#submit').focus().click();
    }
  }
});

function displayEdit (domainId,domainName) {
  $(".error-message").text("");
  $("#domain-view").hide();
  $("#domain-add").show();
  $("#domainname").val(domainName);
  $("#domainid").val(domainId);
}

function changeStatus (domainId,isActive) {

  var msgstatus='deactivate';
  if(isActive){
    msgstatus='activate';
  }
  var answer = confirm('Are you sure want to '+msgstatus+ '?');
  if (answer)
  {
    function onSuccess(response){
      getDomains ();
    }
    function onFailure(error){
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
    }    
}

$("#search-domain-name").keyup(function() { 
  var filterkey = this.value.toLowerCase();
  var filteredList=[];
    for(var entity in domainsList) {
      domainName = domainsList[entity]["domain_name"];
      if (~domainName.toLowerCase().indexOf(filterkey)) filteredList.push(domainsList[entity]);
    }
  loadDomainList(filteredList);
});

$(document).ready(function () {
  getDomains ();
});