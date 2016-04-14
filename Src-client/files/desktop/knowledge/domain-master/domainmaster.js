var domainsList;

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
  var title;
  $(".tbody-domain-list1").find("tr").remove();
    for(var entity in domainsList) {
      domainId = domainsList[entity]["domain_id"];
      domainName = domainsList[entity]["domain_name"];
      isActive = domainsList[entity]["is_active"];
      if(isActive == true) {
        passStatus=false;
        imgName="icon-active.png"
        title = "Click here to deactivate"
      }
      else {
        passStatus=true;
        imgName="icon-inactive.png"
        title = "Click here to activate"
      }
      var tableRow=$('#templates .table-domain-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.domain-name', clone).text(domainName);
      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+domainId+',\''+domainName+'\')"/>');
      $('.status', clone).html('<img src=\'/images/'+imgName+'\' title="'+title+'" onclick="changeStatus('+domainId+','+passStatus+')"/>');
      $('.tbody-domain-list1').append(clone);
      j = j + 1;
    }
}

function validate(){
  if($("#domainname").val().trim().length==0){
    displayMessage(message.domainname_required);
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
      $("#search-domain-name").val('');
    }    function onFailure(error){

        if(error == "DomainNameAlreadyExists"){
            displayMessage(message.domainname_exists);
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

        if(error == 'DomainNameAlreadyExists'){
            displayMessage(message.domainname_exists);
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
      $("#search-domain-name").val('');
    }
    function onFailure(error){
      alert(error);
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
  $("#domainname").focus();
});