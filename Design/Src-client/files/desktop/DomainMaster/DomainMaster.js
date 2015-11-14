function loadDomainList (domainsList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var domainId = '';
  var domainName = '';
  var isActive = '';
  var domainList;
  for(var i in domainsList) {
    domainList = domainsList[i];
    for(var entity in domainList) {
      domainId = domainList[entity]["domain_id"];
      domainName = domainList[entity]["domain_name"];
      isActive = domainList[entity]["is_active"];
      if(isActive=='true') {
        passStatus="false";
        imgName="icon-active.png"
      }
      else {
        passStatus="true";
        imgName="icon-inactive.png"
      }
      var row = document.getElementById("rowToClone"); 
      var table = document.getElementById("tableToModify");
      var clone = row.cloneNode(true);
      clone.id = j; 
      clone.cells[0].innerHTML = j;
      clone.cells[1].innerHTML = domainName;
      clone.cells[2].innerHTML = '<a href = "#" onclick="displayEdit('+domainId+',\''+domainName+'\')"><img src=\'/images/icon-edit.png\'/></a>'
      clone.cells[3].innerHTML = '<a href = "#" onclick="changeStatus('+domainId+',\''+passStatus+'\')"><img src=\'/images/'+imgName+'\'/></a>'
      table.appendChild(clone);
      j = j + 1;
    }
    $('#rowToClone').hide();
  }
}
function displayAdd () {
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val('');
  $("#domainid").val('');
}

function saveRecord () {
  alert($("#domainname").val());
  alert($("#domainid").val());
  $("#listview").show();
  $("#addview").hide();
}

function displayEdit (domainId,domainName) {
  $("#listview").hide();
  $("#addview").show();
  $("#domainname").val(domainName);
  $("#domainid").val(domainId);
}

function changeStatus (domainId,isActive) {
  alert(domainId);
  alert(isActive);
}

function initialize () {
  var domainsList = {
    "domains": [
    {
      "domain_id": "1",
      "domain_name": "Finance Law",
      "is_active": "true"
    },
    {
      "domain_id": "2",
      "domain_name": "Industrial Law",
      "is_active": "false"
    },
    {
      "domain_id": "3",
      "domain_name": "Labour Law",
      "is_active": "true"
    }
    ]
  };
  loadDomainList(domainsList);
}

$(document).ready(function () {
  initialize();
});




          