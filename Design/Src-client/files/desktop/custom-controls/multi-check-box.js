var countryList = [
	{"country_id": 1, "country_name": "India"},
	{"country_id": 2, "country_name": "Singapore"},
	{"country_id": 3, "country_name": "Malaysia"},
	{"country_id": 4, "country_name": "Bhutan"},
	{"country_id": 5, "country_name": "Srilanka"},
	{"country_id": 6, "country_name": "Australia"},
	{"country_id": 7, "country_name": "Pakistan"},
	{"country_id": 8, "country_name": "Afganisthan"}
];

function createLiElement (value, className) {
	var liElement = $("#templates .multi-check-box-li").clone();
	liElement.text(value);
	if (typeof(className) !== "undefined") {
		liElement.addClass(className);
	}
	return liElement;
}

function initializeMultiCheckBox (
	multiCheckBox, items, onClickCallback, OnItemsClickCallback
) {
	var multiCheckBoxUl = $(".multi-check-box-list ul", multiCheckBox);
	for (var i = 0; i < items.length; i++) {
		var country = items[i];
		var liElement = createLiElement(country["country_name"]);
		liElement.addClass(country["country_id"]);
		multiCheckBoxUl.append(liElement);
	}
}

function initialize () {
	initializeMultiCheckBox(
		$(".multi-check-box"),
		countryList,
		function onClickCallback () {
			// body...
		},
		function OnItemsClickCallback () {
			// body...
		}
	);
}

$(function () {
	initialize();
});