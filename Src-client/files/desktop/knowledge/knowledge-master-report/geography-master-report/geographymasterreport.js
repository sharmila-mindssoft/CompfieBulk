var countriesList;
var geographiesList;

//get geography master data from api
function getGeography(){
  function onSuccess(data){
    geographiesList = data["geographies"];
    countriesList = data["countries"];
  }
  function onFailure(error){
    displayMessage(error);
  }
  mirror.getGeographyReport(
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

//display geography master details in view page
function loadGeographyList(geographyList){
  var sno=0;
  var geography = '';
  var isActive = 0;
  var title;
  $(".tbody-geography-report-list").find("tr").remove();
  for(var list in geographyList) {
    geography = geographyList[list]["geography"];
    isActive = geographyList[list]["is_active"];
    var geographyimage = geography.replace(/>>/gi,' <img src=\'/knowledge/images/right_arrow.png\'/> ');
    if(isActive == 1) {
      title="Active";
    }
    else {
      title="Inacive";
     }
    var tableRow=$('#templates .table-geography-report .table-row');
var clone=tableRow.clone();
sno = sno + 1;
$('.sno', clone).text(sno);
$('.geography-name', clone).html(geographyimage);
$('.is-active', clone).text(title);
$('.tbody-geography-report-list').append(clone);
  }
  $("#total-records").html('Total : '+sno+' records');
}

//Autocomplete Script Starts
//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
  $("#countryval").focus();
  var geographyList = geographiesList[val[0]];
  $("#search-geography-name").val('');
  loadGeographyList(geographyList);
}

//load country list in autocomplete text box  
$("#countryval").keyup(function(e){
  function callback(val){
    onCountrySuccess(val)
  }
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, callback, flag=true)
});
//Autocomplete Script ends

//filter process
$("#search-geography-name").keyup(function(){
  var filterkey = $("#search-geography-name").val().toLowerCase();
  var filteredList=[];
  var cId = '';
  if($("#country").val() != '') cId = $("#country").val();

  var geographyList = geographiesList[cId];
  for(var entity in geographyList) {
      geogtaphyname = geographyList[entity]["geography"];
      if (~geogtaphyname.toLowerCase().indexOf(filterkey))
      {
        filteredList.push(geographyList[entity]);
      }
  }
  loadGeographyList(filteredList);
});

//initialization
$(function() {
  getGeography();
  $("#countryval").focus();
});
