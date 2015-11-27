var tempIndustryList;
function loadIndustryList (industriesList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var industryId = 0;
  var industryName = '';
  var isActive = 0;
  var industryList;

  $(".tbody-industry-list").find("tr").remove();
    for(var entity in industriesList) {
      industryId = industriesList[entity]["industry_id"];
      industryName = industriesList[entity]["industry_name"];
      isActive = industriesList[entity]["is_active"];
      if(isActive == 1) {
        passStatus="0";
        imgName="icon-active.png"
      }
      else {
        passStatus="1";
        imgName="icon-inactive.png"
      }
      var tableRow=$('#templates .table-industry-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.industry-name', clone).text(industryName);
      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+industryId+',\''+industryName+'\')"/>');
      $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+industryId+','+passStatus+')"/>');
      $('.tbody-industry-list').append(clone);
      j = j + 1;
    }
}
function displayAdd () {
  $("#error").text("");
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
  function success(status,data) {
    if(status == 'success') {
      getIndustries ();
      $("#listview").show();
      $("#addview").hide();
      $("#error").text("Record Added Successfully");
    } else {
      $("#error").text(status);
    }
  }
  function failure(data){

  }
  mirror.saveIndustry("SaveIndustry", industryName, success, failure);
  }
  else{
    function success(status,data){
      if(status == 'success') {
         getIndustries ();
        $("#listview").show();
        $("#addview").hide();
        $("#error").text("Record Updated Successfully");
      } else {
        $("#error").text(status);
      }
    }
    function failure(data) {
    }
    mirror.updateIndustry("UpdateIndustry", industryId, industryName, success, failure);
  }
}
}

function displayEdit (industryId,industryName) {
  $("#listview").hide();
  $("#addview").show();
  $("#industryname").val(industryName);
  $("#industryid").val(industryId);
  $("#error").text("");
}

function changeStatus (industryId,isActive) {
  function success(status,data){
    getIndustries ();
    $("#error").text("Status Changed Successfully");
  }
  function failure(data){
  }
  mirror.changeIndustryStatus("ChangeIndustryStatus", industryId, isActive, success, failure);
}

function getIndustries () {

  function success(status,data){
    tempIndustryList = data["industries"];
    industriesList = data["industries"];
    loadIndustryList(industriesList);
  }
  function failure(data){
  }
  mirror.getIndustryList("GetIndustries", success, failure);
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
    for(var entity in tempIndustryList) {
      industryName = tempIndustryList[entity]["industry_name"];
      if (~industryName.toLowerCase().indexOf(filterkey)) filteredList.push(tempIndustryList[entity]);
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