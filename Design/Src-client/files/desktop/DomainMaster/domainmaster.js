var tempDomainList;
function loadDomainList (domainsList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var domainId = 0;
  var domainName = '';
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
function displayAdd () {
  $("#error").text("");
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val('');
  $("#domainid").val('');
}

function saveRecord () {
  domainId = parseInt($("#domainid").val());
  domainName = $("#domainname").val();

if(domainName == ''){
  $("#error").text("Domain Name Required");
}else{
  if($("#domainid").val() == ''){
    function success(status,data) {
      if(status == 'success') {
        getDomains ();
        $("#listview").show();
        $("#addview").hide();
        $("#error").text("Record Added Successfully");
      } else {
        $("#error").text(status);
      }
    }
    function failure(data){

    }
    mirror.saveDomain("SaveDomain", domainName, success, failure);
  }
  else{

    function success(status,data){
      if(status == 'success') {
        getDomains()
        $("#listview").show();
        $("#addview").hide();
        $("#error").text("Record Updated Successfully");
      } else {
        $("#error").text(status);
      }
    }
    function failure(data) {
    }
    mirror.updateDomain("UpdateDomain", domainId, domainName, success, failure);
  }
}
}   

function displayEdit (domainId,domainName) {
  $("#error").text("");
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val(domainName);
  $("#domainid").val(domainId);
}

function changeStatus (domainId,isActive) {
  function success(status,data){
    getDomains ();
    $("#error").text("Status Changed Successfully");
  }
  function failure(data){
  }
  mirror.changeDomainStatus("ChangeDomainStatus", domainId, isActive, success, failure);
}

function getDomains () {
  function success(status,data){
    tempDomainList = data["domains"];
    domainsList = data["domains"];
    loadDomainList(domainsList);
  }
  function failure(data){
  }
  mirror.getDomainList("GetDomains", success, failure);
}

function filter (term, cellNr){
  var filterkey = term.value.toLowerCase();
  var filteredList=[];
    for(var entity in tempDomainList) {
      domainName = tempDomainList[entity]["domain_name"];
      if (~domainName.toLowerCase().indexOf(filterkey)) filteredList.push(tempDomainList[entity]);
    }
  loadDomainList(filteredList);
}

$(document).ready(function () {
  getDomains ();
  $('#domainname').keydown(function (e) {
  var key = e.keyCode;
  if (!((key == 8) || (key == 32) || (key == 46) || (key >= 65 && key <= 90))) {
  e.preventDefault();
  }
});
});