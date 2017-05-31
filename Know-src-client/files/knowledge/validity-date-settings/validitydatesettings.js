COUNTRIES = ''
DOMAINS = ''
VALIDITY_DATES = ''
COUNTRY_DOMAIN_MAPPINGS = ''

country_names = {}
domain_names = {}
values_to_save = []

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize(){
  function onSuccess(data) {
    COUNTRIES = data["countries"];
    DOMAINS = data["domains"];
    VALIDITY_DATES = data["validity_date_settings"];
    COUNTRY_DOMAIN_MAPPINGS = data["country_domain_mappings"]
    initialize_maps();
    loadValidityDatesList();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getValidityDateList(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}

function initialize_maps(){
  $.each(COUNTRIES, function (key, value){
     country_names[
      parseInt(value["country_id"])
    ] = value["country_name"]
  });
  $.each(DOMAINS, function (key, value){
     domain_names[
      parseInt(value["domain_id"])
    ] = value["domain_name"]
  });
}

function loadValidityDatesList(){
  var count = 0;
  $('.tbody-validity-config-list').empty();

  $.each(COUNTRY_DOMAIN_MAPPINGS, function (country_id, domain_list) {
    ++ count;
    if(domain_list.length > 0){
      var tableRow = $('#templates .table-dconfig-list .table-dconfig-countries-row');
      var clone = tableRow.clone();
      $('.dconfig-country-name', clone).text(
        country_names[parseInt(country_id)]
      );
      //$('.dconfig-country-name', clone).addClass('heading');
      $('.tbody-validity-config-list').append(clone);
      for (var dcount = 0; dcount < domain_list.length; dcount++) {
        domain_id = parseInt(domain_list[dcount])
        var tableRowDomains = $('#templates .table-dconfig-list .table-dconfig-domain-row');
        var clone1 = tableRowDomains.clone();
        $('.dconfig-domain-name', clone1).text(domain_names[domain_id]);
        $('.dconfig-validity-days', clone1).addClass("val-"+country_id+"-"+domain_id);
        $('.validity-day-setting-id', clone1).addClass("id-"+country_id+"-"+domain_id);
        $('.dconfig-validity-days', clone1).on('input', function (e) {
          this.value = isNumbers($(this));
        });
        $.each(VALIDITY_DATES, function (key, value){
          if(parseInt(value["country_id"]) == country_id &&
            parseInt(value["domain_id"]) == domain_id
          ){
            $('.validity-day-setting-id', clone1).val(value["validity_days_id"]);
            $('.dconfig-validity-days', clone1).val(value["validity_days"]);
          }
        });

        $('.tbody-validity-config-list').append(clone1);
      }
    }
  });
  if(count <= 0){
    $("#btn-submit").hide();
    $('.tbody-validity-config-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-validity-config-list').append(clone4);
  }
}

$("#btn-submit").click(function(){
  save_validity_date_settings();
});

function save_validity_date_settings() {
  var result = collect_and_validate_values()
  if(result != false && values_to_save.length > 0){
    function onSuccess(data) {
      displaySuccessMessage(message.settings_save_success);
      initialize();
    }
    function onFailure(error, response) {
      if(error == "SaveValidityDateSettingsFailure")
      {
        var msgText = '';
        for(var i=0;i<COUNTRIES.length;i++){
          if(COUNTRIES[i].country_id == response.country_id){
            msgText = COUNTRIES[i].country_name;
            break;
          }
        }
        for(var i=0;i<DOMAINS.length;i++){
          if(DOMAINS[i].domain_id == response.domain_id){
            msgText =  "Enter days between 0 to 366 for "+DOMAINS[i].domain_name+" under "+msgText;
            break;
          }
        }
        displayMessage(msgText);
      }else{
        displayMessage(error);
      }
    }
    displayLoader();
    mirror.saveValidityDateSettings(
      values_to_save, function (error, response) {
      if (error == null) {
        onSuccess(response);
        hideLoader();
      } else {
        onFailure(error, response);
        hideLoader();
      }
    });
  }
  /*else{
        if(values_to_save.length == 0)
          displayMessage(message.validity_date_required);
      }*/
}

function collect_and_validate_values(){
  values_to_save = []
  c_name = null;
  var returnVal = true;
  $.each(COUNTRY_DOMAIN_MAPPINGS, function (country_id, domain_list) {
    for (var dcount = 0; dcount < domain_list.length; dcount++) {
      domain_id = parseInt(domain_list[dcount])
      validity_days = $(".val-"+country_id+"-"+domain_id).val()
      validity_days_id = $(".id-"+country_id+"-"+domain_id).val()
      if(
          validity_days != "" &&
          validity_days != "undefined" &&
          validity_days != null
       ){
        if (validateMaxLength("validity_days", validity_days, "Validity Days") == false){
          displayMessage(message.validity_settings_max);
          returnVal =false;
          break;
        }
        if (parseInt(validity_days) > 366){
          var msgText = '';
          for(var i=0;i<COUNTRIES.length;i++){
            if(COUNTRIES[i].country_id == country_id){
              c_name = COUNTRIES[i].country_name;
              //break;
            }
          }
          for(var i=0;i<DOMAINS.length;i++){
            if(DOMAINS[i].domain_id == domain_id){
              msgText =  message.validity_settings_days.replace('domain_name', DOMAINS[i].domain_name) + c_name;
              //break;
            }
          }
          displayMessage(msgText);
          returnVal =false;
          break;
        }
        if(validity_days_id){
          validity_days_id = parseInt(validity_days_id)
        }
        value = mirror.get_validity_day_setting(
          validity_days_id, parseInt(country_id), parseInt(domain_id),
          parseInt(validity_days)
        )
        values_to_save.push(value)

      }
      /*else{
        displayMessage(message.validity_date_required);
        returnVal = false;
        break;
      }*/
    }
  });
  return returnVal;
}

//initialization
$(function () {
    initialize();
});


