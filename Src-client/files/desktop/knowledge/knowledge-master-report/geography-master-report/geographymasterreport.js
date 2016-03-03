var countriesList;
var geographiesList;

function getGeography(){
  function onSuccess(data){
    geographiesList = data["geographies"];
    countriesList = data["countries"];
  }
  function onFailure(error){
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


function loadGeographyList(geographyList){
  var sno=0;
  var geography = '';
  var isActive = 0;
  var title;  
  $(".tbody-geography-list").find("tr").remove();
  for(var list in geographyList) {
    geography = geographyList[list]["geography"];
    isActive = geographyList[list]["is_active"];
    var geographyimage = geography.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
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
$('.tbody-geography-list').append(clone);
  }
  $("#total-records").html('Total : '+sno+' records');
}

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide(); 
});

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  $("#autocompleteview").show();
  var countries = countriesList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == 1) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text').append(str);
    $("#country").val('');
    }else{
      $("#country").val('');
       $("#autocompleteview").hide();
    }
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);

  var geographyList = geographiesList[checkval];
  loadGeographyList(geographyList);
}
//Autocomplete Script ends

//filter process

$("#search-geography-name").keyup(function(){
  var filterkey = $("#search-geography-name").val().toLowerCase();
  var filteredList=[];
  var geographyList = geographiesList[1];
  for(var entity in geographyList) {
      geogtaphyname = geographyList[entity]["geography"];
      if (~geogtaphyname.toLowerCase().indexOf(filterkey)) 
      {
        filteredList.push(geographyList[entity]);
      }   
  }
  loadGeographyList(filteredList);
});

$(function() {
  getGeography();
});
