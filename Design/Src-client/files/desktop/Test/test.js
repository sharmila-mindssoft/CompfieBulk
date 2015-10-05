function loadCountry (countries) {
	console.log(countries);
	for (var country in countries) {
		console.log(country);
		console.log(countries[country]);

		var option = $("<option></option>");
		option.val(country);
		option.text(countries[country])
		$(".country").append(option);
	}
}

function initialize () {
	$.ajax({
		url: "/test2",
		type: "get",
		data: "",
		success: function (data) {
			var countries = JSON.parse(data);
			loadCountry(countries);
		}
	});
}

$(document).ready(function () {
	initialize();
});