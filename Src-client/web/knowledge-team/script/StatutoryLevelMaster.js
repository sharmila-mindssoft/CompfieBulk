function arrayForEach(a, action) {
    for (var i = 0; i < a.length; ++i)
        action(a[i], i);
}
function apiCall(url, options, callback) {
	$.ajax({
        crossDomain: true,
        url: url,
        dataType: 'json',
        type: 'POST',
        data: options,
        success: function(result) {
        	callback(result)
        },
        error: function(xhr, status, err) {
            console.error(url, status, err.toString());
            callback(JSON.stringify(null));
        }
    });
}

var level_by_country = function (country) {
	var url = "/statutory-level/list";
	var options = {"country": country};
	apiCall (url, options, function (data) {
		if (data.length > 0) {
			$(".level-title").map(function (i) {
				var level = data[i];
				if (typeof(level) !== "undefined") {
					$(this).val(level[2]);
				}
			});
		}
		else {
			$(".level-title").map(function (i) {
				$(this).val('');
			});	
		}
	});
}
var changeStatus = function(country) {
	url = "/statutory-level/status";
	var options = {"country": country}
	apiCall(url, options, function(data) {
		$(".level-active").map(function (i) {
			var name = $(this).attr("name")
			if (name == country) {
				if (data == "A") {
					$(this).attr("src", "/Static/images/icon-active.png");
				}
				else {
					$(this).attr("src", "/Static/images/icon-inactive.png");	
				}
			}
		});
		$(".level-edit").map(function (i) {
			var name = $(this).attr("name")
			if (name == country) {
				if (data == "A") {
					$(this).attr("onclick", "location.href='/statutory-level/edit?country=" + country + "'");
				}
				else {
					$(this).attr("onclick", null);
				}
			}
		});
	});

}
$(".level-country").keydown(function (e) {
	if (e.keyCode == 13) {
		level_by_country($(".level-country").val());
	}
});

$(".add-level").click(function() {
	window.location.href="/statutory-level/add";
});

$(".save-level").click(function() {
	loadCountry();
	var levelTitles = [];
	var textValues = [];
	$('.level-title').map(function(i) {
		var title = $(this).val()
		var name = $(this).attr("name")
		if (! $.isNumeric(name))
			name = 0
		textValues.push([i+1, $(this).val(), name]);
	}).get();

	for (i = 0; i < textValues.length; i++ ){
		var t = textValues[i]
		if (t[1].length != 0) {
			if (i > 0) {
				var t1 = textValues[i-1];
				if (t1[1].length == 0) {
					alert("Please enter previous level");
					return;
				}	
			}
			levelTitles.push(t);
		}
	}

	var country = $(".level-country").val();
	if (country.length == 0) {
		alert("Select country");
		return;
	}
	var saveUrl = "/statutory-level/save";
	var options = {"levels": JSON.stringify(levelTitles), "country":country};
	apiCall(saveUrl, options, function (data) {
		alert("data saved");
		window.location.href = "/statutory-level";
	});
});
