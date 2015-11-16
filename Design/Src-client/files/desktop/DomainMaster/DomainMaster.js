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
  /*var domainsList = {
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
  };*/

    /*jQuery.ajax({
          url: "http://192.168.1.3:8080/GetDomains",
          type: "post",
          dataType: 'json',
          cache : false,
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({ "session_token": "b4c59894336c4ee3b598f5e4bd2b276b","request": ["GetDomains",{}]
 }),
          success: function(msg) {
            alert(msg);
        }
      });*/
  //loadDomainList(domainsList);

  







$(document).ready(function () {
  var domain_url = "http://localhost:8080/ApiCall";
            var domains_data = {
                    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
                    "request" : [
                        "GetDomains",
                        {}
                    ]
                };
            var options = JSON.stringify(domains_data);
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
                        console.log(data)
                        var result = data["data"];
                        if (result !== null) {
                            callback(result);
                        }
                        else {
                            callback(null);
                        }
                    },
                    error: function(xhr, status, err) {
                        console.error(url, status, err.toString());
                        callback(null);
                    }
                });
            }
            ajaxCall(domain_url, options, function (data) {
                console.log(data)
            });
});




          