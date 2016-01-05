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
  function success(status,data){
    domainsList = data["domains"];
    loadDomainList(domainsList);
  }
  function failure(data){
  }
  mirror.getDomainList(success, failure);
}

function loadDomainList (domainsList) {
  var j = 1;
  var imgName = null;
  var passStatus = null;
  var domainId = 0;
  var domainName = null;
  var isActive = 0;
  var domainList;
  $(".tbody-domain-list").find("tr").remove();
    for(var entity in domainsList) {
      domainId = domainsList[entity]["domain_id"];
      domainName = domainsList[entity]["domain_name"];
      isActive = domainsList[entity]["is_active"];
      if(isActive == 1) {
        passStatus="0";
        imgName="icon-active.png"
      }
      else {
        passStatus="1";
        imgName="icon-inactive.png"
      }
      var tableRow=$('#templates .table-domain-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.domain-name', clone).text(domainName);
      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+domainId+',\''+domainName+'\')"/>');
      $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+domainId+','+passStatus+')"/>');
      $('.tbody-domain-list').append(clone);
      j = j + 1;
    }
}

function validate(){
  if($("#domainname").val().length==0){
    $(".error-message").html('Domain Name Required');
  }else{
    $(".error-message").html('');
    return true
  }
}

$("#submit").click(function(){
  var domainId = $("#domainid").val();
  var domainName = $("#domainname").val();

if(validate()){
  if($("#domainid").val() == ''){
    function success(status,data) {
      if(status == 'success') {
        $("#domain-add").hide();
        $("#domain-view").show();
        getDomains ();
      } else {
        $(".error-message").html(status);
      }
    }
    function failure(data){
      $(".error-message").html(status);
    }
    mirror.saveDomain(domainName, success, failure);
  }
  else{
    function success(status,data){
      if(status == 'success') {
        $("#domain-add").hide();
        $("#domain-view").show();
        getDomains ();
      } else {
        $(".error-message").html(status);
      }
    }
    function failure(data) {
    }
    mirror.updateDomain(parseInt(domainId), domainName, success, failure);
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
  function success(status,data){
    getDomains ();
  }
  function failure(data){
  }
  mirror.changeDomainStatus(parseInt(domainId), isActive, success, failure);
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