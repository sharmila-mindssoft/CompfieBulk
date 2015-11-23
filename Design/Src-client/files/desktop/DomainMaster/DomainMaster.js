var tempDomainList;
function loadDomainList (domainsList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var domainId = 0;
  var domainName = '';
  var isActive = 0;
  var domainList;

  $('#rowToClone').show();
  $("#tableToModify").find("tr:gt(0)").remove();
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
      var row = document.getElementById("rowToClone"); 
      var table = document.getElementById("tableToModify");
      var clone = row.cloneNode(true);
      clone.id = j; 
      clone.cells[0].innerHTML = j;
      clone.cells[1].innerHTML = domainName;
      clone.cells[2].innerHTML = '<img src=\'/images/icon-edit.png\' onclick="displayEdit('+domainId+',\''+domainName+'\')"/>'
      clone.cells[3].innerHTML = '<img src=\'/images/'+imgName+'\' onclick="changeStatus('+domainId+','+passStatus+')"/>'
      table.appendChild(clone);
      j = j + 1;
    }
   $('#rowToClone').hide();
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
    saveDomainDetail = [domainName];
    function success(status,data) {
      if(status == 'SaveDomainSuccess') {
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
    mirror.saveDomain("SaveDomain", saveDomainDetail, success, failure);
  }
  else{

    updateDomainDetail = [domainId, domainName];
    function success(status,data){
      if(status == 'UpdateDomainSuccess') {
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
    mirror.updateDomain("UpdateDomain", updateDomainDetail, success, failure);
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