var industriesList;

$(".btn-industry-add").click(function(){
  $("#industry-view").hide();
  $("#industry-add").show();
  $("#industryname").val('');
  $("#industryid").val('');
  $(".error-message").html('');
  $("#industryname").focus();
});
$(".btn-industry-cancel").click(function(){
  $("#industry-add").hide();
  $("#industry-view").show();
});

// get industry list from api
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

//display industry list in view page
function loadIndustryList (industriesList) {
  var j = 1;

  $(".tbody-industry-list-view").find("tr").remove();
    $.each(industriesList, function(key, value) {
      var industryId = value["industry_id"];
      var industryName = value["industry_name"];
      var isActive = value["is_active"];

      var passStatus = null;
      var classValue = null;

      if(isActive == true) {
        passStatus = false;
        classValue = "active-icon";
      }
      else {
        passStatus=true;
        classValue = "inactive-icon";
      }

      var tableRow=$('#templates .table-industry-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.industry-name', clone).text(industryName);

      $('.edit-icon').attr('title', 'Edit');
      $(".edit-icon", clone).on("click", function() {
          displayEdit(industryId, industryName);
      });

      $(".status", clone).addClass(classValue);
      $('.active-icon').attr('title', 'Deactivate');
      $('.inactive-icon').attr('title', 'Activate');
      $(".status", clone).on("click", function() {
          changeStatus(industryId, passStatus);
      });

      $('.tbody-industry-list-view').append(clone);
      j = j + 1;
    });
}

// validation
function validate(){
  var checkLength = industryValidate();
  if(checkLength){
    if($("#industryname").val().trim().length==0){
      displayMessage(message.industryname_required);
    }else{
      displayMessage('');
      return true
    }
  }
}

//save or update industry master on enter key press
$('#industryname').keypress(function (e) {
  if (e.which == 13) {
    if(validate()){
      jQuery('#submit').focus().click();
    }
  }
});

// save or update industry master 
$("#submit").click(function(){
  var industryId = $("#industryid").val();
  var industryName = $("#industryname").val().trim();

if(validate()){
  if(industryId == ''){
    function onSuccess(response) {
      getIndustries ();
      $("#industry-add").hide();
      $("#industry-view").show();
    }
    function onFailure(error){
        if(error == "InvalidIndustryId"){
            displayMessage(message.invalid_industryid);
        }                
        if(error == "IndustryNameAlreadyExists"){
            displayMessage(message.industryname_exists);
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
            displayMessage(message.industryname_exists);
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

// edit industry master
function displayEdit (industryId,industryName) {
  $(".error-message").text("");
  $("#industry-view").hide();
  $("#industry-add").show();
  $("#industryname").val(industryName.replace(/##/gi,'"'));
  $("#industryid").val(industryId);
}

// activate / deactivate industry master
function changeStatus (industryId,isActive) {
  var msgstatus = message.deactive_message;
  if(isActive){
      msgstatus = message.active_message;
  }
  $( ".warning-confirm" ).dialog({
      title: message.title_status_change,
      buttons: {
          Ok: function() {
              $( this ).dialog( "close" );

              function onSuccess(response){
                getIndustries ();
              }
              function onFailure(error){
                if(error == "TransactionExists"){
                    alert(message.trasaction_exists)
                }else{
                    alert(error)
                }
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
          },
          Cancel: function() {
              $( this ).dialog( "close" );
          }
      },
      open: function ()  {
          $(".warning-message").html(msgstatus);
      }
  });
}

//filter process
$("#search-industry-name").keyup(function() { 
  var filterkey = this.value.toLowerCase();
  var filteredList=[];
    for(var entity in industriesList) {
      industryName = industriesList[entity]["industry_name"];
      if (~industryName.toLowerCase().indexOf(filterkey)) filteredList.push(industriesList[entity]);
    }
  loadIndustryList(filteredList);
});

//initialization
$(document).ready(function () {
  getIndustries ();
});