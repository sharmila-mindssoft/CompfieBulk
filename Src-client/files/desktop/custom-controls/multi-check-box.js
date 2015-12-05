
function createLiElement (element, value, className) {
	var liElement = $("#templates .multi-check-box-li", element).clone();
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
	parent, items, OnItemsClickCallback
) {
	var multiCheckBox = $(".multi-check-box", parent);
	var selectedDiv = $(".multi-check-box-selected", multiCheckBox);
	selectedDiv.empty();

	function filterSuggestions (suggestions, searchString) {
		if (searchString.length == 0)
			return suggestions;

		searchString = searchString.toLowerCase();
		var suggestions2 = [];
		for (var i = 0; i < suggestions.length; i++) {
			var item = suggestions[i];
			var itemName = item["item_name"].toLowerCase();
			if (itemName.indexOf(searchString) >= 0) {
				suggestions2.push(item);
			}
		}
		return suggestions2;
	}

	function updateDropDown () {
		$(".multi-check-box-dropdown", multiCheckBox).removeClass("empty");
		var selectedItemsCount = $("div", selectedDiv).length;
		var selectedItems = selectedItemsCount + " Selected";
		if (selectedItemsCount <= 3) {
			var _items = [];
			var selectedDivs = $("div", selectedDiv);
			for (var i = 0; i < selectedDivs.length; i++) {
				_items.push($(selectedDivs[i]).text());
			}
			selectedItems = _items.join(", ");
		}
		if (selectedItemsCount == 0) {
			$(".multi-check-box-dropdown", multiCheckBox).addClass("empty");
			$(".multi-check-box-dropdown", multiCheckBox).val("Select One");
		}
		else {
			$(".multi-check-box-dropdown", multiCheckBox).val(selectedItems);
		}
	}

	function onItemClick (element) {
		var className = element.attr('class');
		var itemId = className.split(" ")[1];
		if (element.hasClass("active")) {
			element.removeClass("active");
			if ($("." + itemId, selectedDiv).length > 0) {
				$("." + itemId, selectedDiv).remove();
			}
		}
		else {
			element.addClass("active");
			var itemDiv = createDivElement(element.text(), itemId);
			selectedDiv.append(itemDiv);
		}
		updateDropDown();
		OnItemsClickCallback(itemId, element.text());
	}

	function prepareLiElement (i, item) {
		var liElement = createLiElement(parent, item["item_name"]);
		var itemId = item["item_id"].toString();
		liElement.addClass(itemId);
		if ($("." + itemId, selectedDiv).length > 0)
			liElement.addClass("active");
		liElement.on("click", function () {
			onItemClick($(this));
		});
		liElement.attr("tabindex", i);
		liElement.on("keydown", function (e) {
			if (e.keyCode == 27 || e.keyCode == 9) {
				$(".multi-check-box-suggestions", multiCheckBox).hide();
			}
			if (e.keyCode == 40) {
				$(this).next().focus();
			}
			if (e.keyCode == 38) {
				if ( $(this).is(':first-child') ) {
					$(".multi-check-box-textbox", multiCheckBox).focus();
				}
				else
					$(this).prev().focus();
			}
			if (e.keyCode == 32) {
				onItemClick($(this));
			}
		});
		return liElement;
	}

	function fillUpSuggestions (suggestions) {
		$(".multi-check-box-list", multiCheckBox).hide();
		var multiCheckBoxUl = $(".multi-check-box-ul", multiCheckBox);
		multiCheckBoxUl.empty();
		if (suggestions.length == 0)
			return;
		$(".multi-check-box-list", multiCheckBox).show();
		for (var i = 0; i < suggestions.length; i++) {
			var item = suggestions[i];
			var liElement = prepareLiElement(i, item);
			multiCheckBoxUl.append(liElement);
		}
	}

	$(".multi-check-box-textbox", multiCheckBox).on("focus", function (e) {
		var items2 = filterSuggestions(items, $(this).val());
		fillUpSuggestions(items2);
	});

	$(".multi-check-box-textbox", multiCheckBox).on("keyup", function (e) {
		if (e.keyCode == 27)
			return;
		var items2 = filterSuggestions(items, $(this).val());
		fillUpSuggestions(items2);
	});

	$(".multi-check-box-textbox", multiCheckBox).on("keydown", function (e) {
		if (e.keyCode == 27)
			$(".multi-check-box-suggestions", multiCheckBox).hide();
		if (e.keyCode == 40) {
			$(".multi-check-box-li", multiCheckBox)[0].focus();
		}
	});

	$(".multi-check-box-dropdown", multiCheckBox).on("click", function (e) {
		if ($(".multi-check-box-suggestions", multiCheckBox).is(":visible"))
			$(".multi-check-box-suggestions", multiCheckBox).hide();
		else {
			$(".multi-check-box-suggestions", multiCheckBox).show();
			$(".multi-check-box-textbox", multiCheckBox).focus();
		}
	});

	$(document).on("keyup", function (e) {
		if (e.keyCode == 27) {
			var hovered = $(".multi-check-box-li:hover", multiCheckBox).length;
			if (hovered <= 0)
				$(".multi-check-box-suggestions", multiCheckBox).hide();
		}
	});

	$(document).on("click", function (e) {
		var hovered = $(".multi-check-box-li:hover", multiCheckBox).length;
		if (hovered > 0)
			return;
		var hovered = $(".multi-check-box-textbox:hover", multiCheckBox).length;
		if (hovered > 0)
			return;
		var hovered = $(".multi-check-box-dropdown:hover", multiCheckBox).length;
		if (hovered > 0)
			return;
		$(".multi-check-box-suggestions", multiCheckBox).hide();
	});


	function getSelected () {
		var _items = [];
		$.each($("div", selectedDiv), function (i, div) {
			_items.push({
				"item_id": parseInt($(div).attr("class")),
				"item_name": $(div).text()
			});
		});
		return _items;
	}

	function setSelected (all_items) {
		selectedDiv.empty();
		for (var i = 0; i < all_items.length; i++) {
			var item = all_items[i];
			if (item["selected"] == 0)
				continue;
			var itemDiv = createDivElement(
				item["item_name"], item["item_id"].toString()
			);
			selectedDiv.append(itemDiv);
		}
		updateDropDown();
	}

	setSelected(items);

	return {
		getSelected: getSelected,
		setSelected: setSelected
	}
}