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
  for(var i in domainsList) {
    domainList = domainsList[i];
    for(var entity in domainList) {
      domainId = domainList[entity]["domain_id"];
      domainName = domainList[entity]["domain_name"];
      isActive = domainList[entity]["is_active"];
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
  }
   $('#rowToClone').hide();
}
function displayAdd () {
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
  var domain_url = "http://192.168.1.9:8080/SaveDomain";
  var domains_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "SaveDomain",
        { "domain_name": domainName }
    ]
  };
   $("#error").text("Record Added Successfully");
  }
  else{
  var domain_url = "http://192.168.1.9:8080/UpdateDomain";
  var domains_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "UpdateDomain",
      {
          "domain_id": domainId,
          "domain_name": domainName
      }
    ]
  };
  $("#error").text("Record Updated Successfully");
  }
  var options = JSON.stringify(domains_data);
  ajaxCall(domain_url, options, function (data) {
    if(data[0] == 'success'){
      $("#listview").show();
      $("#addview").hide();
      getDomains ();
    }else{
      $("#error").text(data[0]);
    }
  });
}
}

function displayEdit (domainId,domainName) {
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val(domainName);
  $("#domainid").val(domainId);
}

function changeStatus (domainId,isActive) {
  var domain_url = "http://192.168.1.9:8080/ChangeDomainStatus";
  var domains_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "ChangeDomainStatus",
      {
        "domain_id": domainId,
        "is_active": isActive
      }
    ]
  };
  var options = JSON.stringify(domains_data);
  ajaxCall(domain_url, options, function (data) {
    $("#error").text("Status Changed Successfully");
    getDomains ();
  });
}

function getDomains () {
  var domain_url = "http://192.168.1.9:8080/GetDomains";
  var domains_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "GetDomains",
        {}
    ]
  };
  var options = JSON.stringify(domains_data);
  ajaxCall(domain_url, options, function (data) {
    if(data[0] == 'success'){
      tempDomainList = data[1];
      loadDomainList(data[1]);
    }
  });
}

function filter (term, cellNr){
  var filterkey = term.value.toLowerCase();
  var filteredList=[];
  for(var i in tempDomainList) {
    domainList = tempDomainList[i];
    for(var entity in domainList) {
      domainId = domainList[entity]["domain_id"];
      domainName = domainList[entity]["domain_name"];
      isActive = domainList[entity]["is_active"];
      if (~domainName.toLowerCase().indexOf(filterkey)) filteredList.push({"domains" : {"domain_id": domainId,"domain_name": domainName,"is_active": isActive}});
    }
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

function ajaxCall (url, options, callback) {
  $.support.cors = true;
  $.ajax({
    crossDomain: true,
    url: url,
    dataType: 'json',
    type: 'POST',
    data: options,
    crossDomain: true,
    success: function(data) {
        console.log(data);
        callback(data);
    },
    error: function(xhr, status, err) {
        console.error(url, status, err.toString());
        callback(null);
    }
  });
  }