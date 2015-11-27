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

function createDivElement (value, className) {
	var divElement = $("<div></div>");
	divElement.text(value);
	if (typeof(className) !== "undefined") {
		divElement.addClass(className);
	}
	return divElement;
}

function initializeMultiCheckBox (
	multiCheckBox, items, onClickCallback, OnItemsClickCallback
) {
	$(".multi-check-box-selected", multiCheckBox).empty();
	var multiCheckBoxUl = $(".multi-check-box-list ul", multiCheckBox);
	for (var i = 0; i < items.length; i++) {
		var item = items[i];
		var liElement = createLiElement(item["item_name"]);
		liElement.addClass(item["item_id"].toString());
		liElement.on("click", function () {
			$(this).toggleClass("active");
			var className = $(this).attr('class');
			var itemId = className.split(" ")[1];
			var selectedDiv = $(".multi-check-box-selected", multiCheckBox);
			var selectedItems = json.parse(selectedDiv.text());
			

			var item2 = {"item_id": itemId, "item_name": $(this).text()};
			var item3 = {itemId: item2};
			var selectedItems2 = 
			var itemDiv = createDivElement(item3);
			selectedDiv.text(itemDiv);
		});
		multiCheckBoxUl.append(liElement);
	}
}

function initialize () {
	var items = [];
	for (var i = 0; i < countryList.length; i++) {
		items.push({
			"item_id": countryList[i]["country_id"],
			"item_name": countryList[i]["country_name"],
		});
	}
	initializeMultiCheckBox(
		$(".multi-check-box"),
		items,
		function onClickCallback () {
			// body...
		},
		function OnItemsClickCallback () {
			// body...
		}
	);

	var width = $(".multi-check-box-textbox").outerWidth();
	console.log(width);
	$(".multi-check-box-list ul").width(width);
}

$(function () {
	initialize();
});