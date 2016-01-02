var industriesList;
$(".btn-industry-add").click(function(){
  $("#industry-view").hide();
  $("#industry-add").show();
  $("#industryname").val('');
  $("#industryid").val('');
  $(".error-message").html('');
});
$(".btn-industry-cancel").click(function(){
  $("#industry-add").hide();
  $("#industry-view").show();
});

function getIndustries () {
  function success(status,data){
    industriesList = data["industries"];
    loadIndustryList(industriesList);
  }
  function failure(data){
  }
  mirror.getIndustryList(success, failure);
}

function loadIndustryList (industriesList) {
  var j = 1;
  var imgName = null;
  var passStatus = null;
  var industryId = 0;
  var industryName = null;
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

function validate(){
  if($("#industryname").val().length==0){
    $(".error-message").html('Industry Name Required');
  }else{
    $(".error-message").html('');
    return true
  }
}

$('#industryname').keypress(function (e) {
  if (e.which == 13) {
    if(validate()){
      jQuery('#submit').focus().click();
    }
  }
});

$("#submit").click(function(){
  var industryId = $("#industryid").val();
  var industryName = $("#industryname").val();

if(validate()){
  if($("#industryid").val() == ''){
    function success(status,data) {
      if(status == 'success') {
        $("#industry-add").hide();
        $("#industry-view").show();
        getIndustries ();
      } else {
        $(".error-message").html(status);
      }
    }
    function failure(data){
      $(".error-message").html(status);
    }
    mirror.saveIndustry(industryName, success, failure);
  }
  else{
    function success(status,data){
      if(status == 'success') {
        $("#industry-add").hide();
        $("#industry-view").show();
        getIndustries ();
      } else {
        $(".error-message").html(status);
      }
    }
    function failure(data) {
    }
    mirror.updateIndustry(parseInt(industryId), industryName, success, failure);
  }
}
}); 

function displayEdit (industryId,industryName) {
  $(".error-message").text("");
  $("#industry-view").hide();
  $("#industry-add").show();
  $("#industryname").val(industryName);
  $("#industryid").val(industryId);
}

function changeStatus (industryId,isActive) {
  function success(status,data){
    getIndustries ();
  }
  function failure(data){
  }
  mirror.changeIndustryStatus(industryId, isActive, success, failure);
}


function getIndustries () {
  function success(status,data){
    tempIndustryList = data["industries"];
    industriesList = data["industries"];
    loadIndustryList(industriesList);
  }
  function failure(data){
  }
  mirror.getIndustryList(success, failure);
}

$("#search-industry-name").keyup(function() { 
  var filterkey = this.value.toLowerCase();
  var filteredList=[];
    for(var entity in industriesList) {
      industryName = industriesList[entity]["industry_name"];
      if (~industryName.toLowerCase().indexOf(filterkey)) filteredList.push(industriesList[entity]);
    }
  loadIndustryList(filteredList);
});

$(document).ready(function () {
  getIndustries ();
});