var tempDomainList;
function clearMessage() {
    $("#error").hide();
    $("#error").text("");
}
function displayMessage(message) {
    $("#error").text(message);
    $("#error").show();
}
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
    displayMessage("");
    $("#listview").hide();
    $("#addview").show();
    $("#domainname").val('');
    $("#domainid").val('');
}

function saveRecord () {
    domainId = parseInt($("#domainid").val());
    domainName = $("#domainname").val();

    if(domainName == ''){
        displayMessage("Domain Name Required");
    }
    else{
        if($("#domainid").val() == ''){
            function onSuccess(response) {
                getDomains ();
                $("#listview").show();
                $("#addview").hide();
                displayMessage("Record Added Successfully");
            }
            function onFailure(error){
                if(error == "InvalidDomainId"){
                    displayMessage("Invalid Domain Id");
                }                
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
                }
            );
        }
        else{

    function onSuccess(response){
     
        getDomains()
        $("#listview").show();
        $("#addview").hide();
        $("#error").text("Record Updated Successfully");
     
    }
    function onFailure(error) {
        if(error == 'DomainNameAlreadyExists'){
            displayMessage("Domain Name Already Exists");
        }
    }
    mirror.updateDomain(domainId, domainName,
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
}   

function displayEdit (domainId,domainName) {
  $("#error").text("");
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val(domainName);
  $("#domainid").val(domainId);
}

function changeStatus (domainId,isActive) {
  function onSuccess(response){
    getDomains ();
    $("#error").text("Status Changed Successfully");
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
        }
    );
}

function getDomains () {
    function onSuccess(data){
        tempDomainList = data["domains"];
        domainsList = data["domains"];
        loadDomainList(domainsList);
    }
    function onFailure(error){
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
});