var tempIndustryList;
function loadIndustryList (industriesList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var industryId = 0;
  var industryName = '';
  var isActive = 0;
  var industryList;

  $('#rowToClone').show();
  $("#tableToModify").find("tr:gt(0)").remove();
  for(var i in industriesList) {
    industryList = industriesList[i];
    for(var entity in industryList) {
      industryId = industryList[entity]["industry_id"];
      industryName = industryList[entity]["industry_name"];
      isActive = industryList[entity]["is_active"];
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
      clone.cells[1].innerHTML = industryName;
      clone.cells[2].innerHTML = '<img src=\'/images/icon-edit.png\' onclick="displayEdit('+industryId+',\''+industryName+'\')"/>'
      clone.cells[3].innerHTML = '<img src=\'/images/'+imgName+'\' onclick="changeStatus('+industryId+','+passStatus+')"/>'
      table.appendChild(clone);
      j = j + 1;
    }
  }
  $('#rowToClone').hide();
}
function displayAdd () {
  $("#listview").hide();
  $("#addview").show();
  $("#industryname").val('');
  $("#industryid").val('');
}

function saveRecord () {
  industryId = parseInt($("#industryid").val());
  industryName = $("#industryname").val();


if(industryName == ''){
  $("#error").text("Industry Name Required");
}else{
  if($("#industryid").val() == ''){
  var industry_url = "http://192.168.1.9:8080/SaveIndustry";
  var industry_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "SaveIndustry",
        { "industry_name": industryName }
    ]
  };
  }
  else{
  var industry_url = "http://192.168.1.9:8080/UpdateIndustry";
  var industry_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "UpdateIndustry",
      {
          "industry_id": industryId,
          "industry_name": industryName
      }
    ]
  };
  }
  var options = JSON.stringify(industry_data);
  ajaxCall(industry_url, options, function (data) {
    if(data[0] == 'success'){
      $("#listview").show();
      $("#addview").hide();
      getIndustries ();
    }else{
      $("#error").text(data[0]);
    }
  });
}
}

function displayEdit (industryId,industryName) {
  $("#listview").hide();
  $("#addview").show();
  $("#industryname").val(industryName);
  $("#industryid").val(industryId);
}

function changeStatus (industryId,isActive) {
  var industry_url = "http://192.168.1.9:8080/ChangeIndustryStatus";
  var industry_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "ChangeIndustryStatus",
      {
        "industry_id": industryId,
        "is_active": isActive
      }
    ]
  };
  var options = JSON.stringify(industry_data);
  ajaxCall(industry_url, options, function (data) {
    getIndustries ();
  });
}

function getIndustries () {
  var industry_url = "http://192.168.1.9:8080/GetIndustries";
  var industry_data = {
    "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    "request" : [
        "GetIndustries",
        {}
    ]
  };
  var options = JSON.stringify(industry_data);
  ajaxCall(industry_url, options, function (data) {
    if(data[0] == 'success'){
      tempIndustryList = data[1];
      loadIndustryList(data[1]);
    }
  });
}

function filter (term, cellNr){
 /* var filterkey = term.value.toLowerCase();
  var table = document.getElementById("tableToModify");
  var ele;
  for (var r = 1; r < table.rows.length; r++){
    ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
    if (ele.toLowerCase().indexOf(filterkey)>=0 )
      table.rows[r].style.display = '';
    else table.rows[r].style.display = 'none';
  }*/
  var filterkey = term.value.toLowerCase();
  var filteredList=[];
  for(var i in tempIndustryList) {
    industryList = tempIndustryList[i];
    for(var entity in industryList) {
      industryId = industryList[entity]["industry_id"];
      industryName = industryList[entity]["industry_name"];
      isActive = industryList[entity]["is_active"];
      if (~industryName.toLowerCase().indexOf(filterkey)) filteredList.push({"industries" : {"industry_id": industryId,"industry_name": industryName,"is_active": isActive}});
    }
  }
  loadIndustryList(filteredList);
}

$(document).ready(function () {
  getIndustries ();

  $('#industryname').keydown(function (e) {
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