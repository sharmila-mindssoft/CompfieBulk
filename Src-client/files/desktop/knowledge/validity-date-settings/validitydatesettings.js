COUNTRIES = ''
DOMAINS = ''
VALIDITY_DATES = ''
COUNTRY_DOMAIN_MAPPINGS = ''

country_names = {}
domain_names = {}
values_to_save = []

function initialize(){
  function onSuccess(data) {
    COUNTRIES = data["countries"];
    DOMAINS = data["domains"];
    VALIDITY_DATES = data["validity_dates"];
    COUNTRY_DOMAIN_MAPPINGS = data["country_domain_mappings"]
    initialize_maps();
    loadValidityDatesList();
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getValidityDateList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
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
  $.each(COUNTRY_DOMAIN_MAPPINGS, function (country_id, domain_list) {
    if(domain_list.length > 0){
      var tableRow = $('#templates .table-dconfig-list .table-dconfig-countries-row');
      var clone = tableRow.clone();
      $('.dconfig-country-name', clone).text(
        country_names[parseInt(country_id)]
      );
      $('.dconfig-country-name', clone).addClass('heading');
      $('.tbody-validity-config-list').append(clone);
      for (var dcount = 0; dcount < domain_list.length; dcount++) {
        domain_id = parseInt(domain_list[dcount])
        var tableRowDomains = $('#templates .table-dconfig-list .table-dconfig-domain-row');
        var clone1 = tableRowDomains.clone();
        $('.dconfig-domain-name', clone1).text(domain_names[domain_id]);
        $('.dconfig-validity-days', clone1).addClass("val-"+country_id+"-"+domain_id);
        $('.validity-day-setting-id', clone1).addClass("id-"+country_id+"-"+domain_id);
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
}

$(".btn-submit").click(function(){
  save_validity_date_settings();
});

function save_validity_date_settings(){
  var result = collect_and_validate_values()
  if(result != false && values_to_save.length > 0){
    function onSuccess(data) {
      displayMessage(message.settings_save_success);
    }
    function onFailure(error) {
      custom_alert(error);
    }
    mirror.saveValidityDateSettings(
      values_to_save, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}

function collect_and_validate_values(){
  values_to_save = []
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
        if(parseInt(validity_days) > 365){
          displayMessage(message.invalid_validity_days);
          return false;
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
      }else{
        displayMessage(message.validity_date_required);
        return false;
        break;
      }
    }
  });
}

//initialization
$(function () {
  initialize();
});


