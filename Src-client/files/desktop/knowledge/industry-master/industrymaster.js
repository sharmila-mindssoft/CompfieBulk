var industriesList;
function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

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
  function onSuccess(data){
      industriesList = data["industries"];
      loadIndustryList(industriesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  mirror.getIndustryList(
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

function loadIndustryList (industriesList) {
  var j = 1;
  var imgName = null;
  var passStatus = null;
  var industryId = 0;
  var industryName = null;
  var isActive = false;

  $(".tbody-industry-list").find("tr").remove();
    for(var entity in industriesList) {
      industryId = industriesList[entity]["industry_id"];
      industryName = industriesList[entity]["industry_name"];
      isActive = industriesList[entity]["is_active"];
      if(isActive == true) {
        passStatus=false;
        imgName="icon-active.png"
      }
      else {
        passStatus=true;
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
  if($("#industryname").val().trim().length==0){
    displayMessage('Industry Name Required');
  }else{
    displayMessage('');
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
    function onSuccess(response) {
      getIndustries ();
      $("#industry-add").hide();
      $("#industry-view").show();
    }
    function onFailure(error){
        if(error == "InvalidIndustryId"){
            displayMessage("Invalid Industry Id");
        }                
        if(error == "IndustryNameAlreadyExists"){
            displayMessage("Industry Name Already Exists");
        }
    }
    mirror.saveIndustry(industryName,
    function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
  }
  else{
    function onSuccess(response) {
      getIndustries ();
      $("#industry-add").hide();
      $("#industry-view").show();
    }
    function onFailure(error){            
        if(error == "IndustryNameAlreadyExists"){
            displayMessage("Industry Name Already Exists");
        }
    }
    mirror.updateIndustry(parseInt(industryId), industryName,
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
}); 

function displayEdit (industryId,industryName) {
  $(".error-message").text("");
  $("#industry-view").hide();
  $("#industry-add").show();
  $("#industryname").val(industryName);
  $("#industryid").val(industryId);
}

function changeStatus (industryId,isActive) {
  function onSuccess(response){
    getIndustries ();
  }
  function onFailure(error){
  }
  mirror.changeIndustryStatus(industryId, isActive,
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