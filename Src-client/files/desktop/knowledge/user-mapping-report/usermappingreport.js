var countriesList;
var clientList;
var businessGroupList;
var lagelEntityList;
var divisionList;
var categoryList;
var assignedUnitList;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

//load all the filters
function initialize() {
  console.log("inside data");
  function onSuccess(data) {
    countriesList = data.countries;
    clientList = data.usermapping_group_details;
    businessGroupList = data.usermapping_business_groups;
    lagelEntityList = data.usermapping_legal_entities;
    divisionList = data.usermapping_unit;
    categoryList = data.usermapping_unit;
    assignedUnitList = data.usermapping_unit;
    console.log("data:"+data);
    //loadCountries(countriesList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getUserMappingReportFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
