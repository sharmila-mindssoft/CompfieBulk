var countriesList;
var domainsList;
var level1List;
var countriesText;
var domainval;


function initialize(){
	function onSuccess(data){
		countriesList = data['countries'];
		domainsList = data['domains'];
		level1List = data['level_1_statutories'];
		//loadCountries(countriesList);
	}
	function onFailure(error){
		displayMessage(error);
	}
	mirror.getStatutoryNotificationsFilters(
		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}
$("#show-button").click(function(){
	var countries = $("#country").val();
	var countriesNameVal = $("#countryval").val();
	//Domain
	var domain = $("#domain").val();
	var domainNameVal = $("#domainval").val();
	//Level 1 Statutories
	var level1id = $("#level1id").val();
	var fromDate = $("#from-date").val();
	if (fromDate == '')
		fromDate = null;
	var toDate = $("#to-date").val();
	if (toDate == '')
		toDate = null;
	if(level1id == ''){
		level1id = null;
	}
	else{
		level1id = parseInt(level1id);
	}
	var level1NameVal = $("#level1idval").val();
	if(countries == ""){
		displayMessage(message.country_required);
		$(".grid-table-rpt").hide();
	}
	else if(domain == ""){
		displayMessage(message.domain_required);
		$(".grid-table-rpt").hide();
	}
	else{
		clearMessage();
		function onSuccess(data){
			$(".grid-table-rpt").show();
			$(".snCountryVal").text(countriesNameVal);
			$(".snDomainVal").text(domainNameVal);
			loadStatutoryNotificationsList(data['country_wise_notifications']);
		}
		function onFailure(error){
			console.log(error);
		}

		mirror.getStatutoryNotificationsReportData(
			parseInt(countries), parseInt(domain), level1id,
			fromDate, toDate,
			function (error, response){
				if(error == null){
					onSuccess(response);
				}
				else{
					onFailure(error);
				}
			}
		);
	}
});
function getDomainName(domainId){
	var domainName;
	$.each(domainsList, function(key, value){
		if(domainsList[key]['domain_id'] == domainId){
			domainName = domainsList[key]['domain_name'];
		}
	});
	return domainName;
}

function loadStatutoryNotificationsList(data){
	$('.tbody-statutory-notifications-list tr').remove();
	var sno = 0;
	$.each(data, function(key, value) {
		var tableRowHeading = $('#templates .table-statutory-notifications-list .table-row-heading');
		var cloneHeading = tableRowHeading.clone();
		var domainId = data[key]['domain_id'];
		$('.heading', cloneHeading).text(getDomainName(domainId));
		$('.tbody-statutory-notifications-list').append(cloneHeading);
	  	var list = data[key]['notifications'];
	  	$.each(list, function(k, val) {
		  	var arr = [];
			var tableRow = $('#templates .table-statutory-notifications-list .table-row-values');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.statutory-provision', clone).html(list[k]['statutory_provision']);
			$('.statutory-notificaions', clone).html(list[k]['notification_text']);
			$('.date-time', clone).html(list[k]['date_and_time']);
			$('.tbody-statutory-notifications-list').append(clone);
		});
	});
	$(".total-records").html( sno+" records")
}


//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
}

//load country list in autocomplete text box
$("#countryval").keyup(function(e){
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, function(val){
    onCountrySuccess(val)
  })
});

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox
$("#domainval").keyup(function(e){
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#level1val").val(val[1]);
  $("#level1id").val(val[0]);
}
//load statutory list in autocomplete textbox
$("#level1val").keyup(function(e){
  var textval = $(this).val();
  getStatutoryAutocomplete(e, textval, level1List[$("#country").val()][$("#domain").val()], function(val){
    onStatutorySuccess(val)
  })
});

$(function() {
	initialize();
});
