var compliancesList;


function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function load_compliances (compliancesList) {
  var j = 1;
  $(".tbody-complainces-list").find("tr").remove();
    for(var entity in compliancesList) {
      var tableRow = $('#head-templates .tbl_heading');
      var clone = tableRow.clone();
      $('.heading', clone).html(entity);
      $('.tbody-compliances-list').append(clone);
      var compliances = compliancesList[entity];
      for(var compliance in compliances){
        var complianceId = compliances[compliance]["compliance_id"];
        var unitId = compliances[compliance]["unit_id"];
        var completeDays = compliances[compliance]["complete_within_days"];
        var tableRow1=$('#templates .table-compliances .table-row');
        var clone1=tableRow1.clone();
        $('.sno', clone1).text(j);
        $('.statutory', clone1).text(compliances[compliance]["compliance_name"]);
        $('.compliance-task', clone1).text(compliances[compliance]["statutory_provision"]);
        $('.description', clone1).text(compliances[compliance]["description"]);
        $('.duration', clone1).text(completeDays);
        $('.startdate', clone1).html('<input type="text" class="input-box" width="200px" readonly="readonly" id="startdate'+j+'"/>');
        $('.action', clone1).html('<input type="button" class="btn-submit" value="Start" onclick="submitOnOccurence('+complianceId+','+j+','+unitId+',\''+completeDays+'\')"/>');

        /*$(clone1, '.action').on("click", function(e){   
            submitOnOccurence(complianceId, j, unitId, completeDays);
        });*/

        $('.tbody-compliances-list').append(clone1);
        
        $("#startdate"+j).datetimepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });
        j = j + 1;
      } 
    }
}

function convert_date (data){
  var datetime = data.split(" ");
  var date = datetime[0].split("-");
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  for(var j=0;j<months.length;j++){
      if(date[1]==months[j]){
           date[1]=months.indexOf(months[j])+1;
       }                      
  } 
  if(date[1]<10){
      date[1]='0'+date[1];
  } 
  return new Date(date[2], date[1]-1, date[0]);
}

function submitOnOccurence(complianceId, count, unitId, complete_within_days){
  var startdate = $('#startdate'+count).val();
  var d = new Date();
  var month = d.getMonth()+1;
  var day = d.getDate();
  var output = d.getFullYear() + '/' + month + '/' + day;
  var currentDate = new Date(output);

  if(startdate != ''){
    var convertDueDate = convert_date(startdate);
    if (convertDueDate > currentDate) {
        displayMessage(message.startdate_greater_today);
        return false;
    }
    displayLoader();
    function onSuccess(data){
      displayMessage(message.action_success);
      //getOnOccuranceCompliances ();
      $('#startdate'+count).val('');
      hideLoader();
      //window.location.href='/compliance-task-details'
    }
    function onFailure(error){
      displayMessage(error);
      hideLoader();
    }
    client_mirror.startOnOccurrenceCompliance(complianceId, startdate, unitId, complete_within_days, 
      function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    }
    );
  }else{
    displayMessage(message.startdate_required);
    return false;
  }
  
}

function getOnOccuranceCompliances () {
  function onSuccess(data){
    compliancesList = data["compliances"];
    load_compliances(compliancesList);
  }
  function onFailure(error){
  }
  client_mirror.getOnOccurrenceCompliances(
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

$(document).ready(function () {
  getOnOccuranceCompliances ();
});