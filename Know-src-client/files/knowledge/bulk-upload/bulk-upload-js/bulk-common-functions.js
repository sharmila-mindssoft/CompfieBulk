var maxUnitSelection = 50;
function commonArrayAutoComplete(
    e, ac_div, text_val, list_val, callback
) {
    ac_div.show();
    var suggestions = [];
    ac_div.find('ul').empty();
    var checkKey = [16, 17, 18, 19, 20, 27, 33, 34, 42, 91, 92, 112, 113,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144, 145];
    if (text_val.length > 0 && $.inArray(e.keyCode, checkKey) == -1) {

        for (var i in list_val) {

            if (~list_val[i].toLowerCase().indexOf(text_val.toLowerCase())) {
                suggestions.push([
                    list_val[i]
                ]);
            }

        }

        var str = '';
        for (var i in suggestions) {
            str += '<li id="' + suggestions[i] +
            '"onclick="activate_text(this,' + callback + ')">' +
            suggestions[i] + '</li>';
        }
        ac_div.find('ul').append(str);
    } else {
        $('.ac-textbox').hide();
    }
    onCommonArrowKey(e, ac_div, callback);
}

var bulkPageList = [500, 750, 1000];
function bulkLoadItemsPerPage() {
    for (var i = 0; i < bulkPageList.length; i++) {
        var Id = bulkPageList[i];
        $('#items_per_page').append($('<option value="' + Id + '">' + Id + '</option>'));
    };
}

function IsCommonInputBulkUpload(inputElm) {
    //allowed => alphanumeric, dot, comma, Hyphen, @, hash
    //return inputElm.val().replace(/[^ 0-9A-Za-z_.,-]/gi, '');
    var start = inputElm.selectionStart, end = inputElm.selectionEnd;
    inputElm.value = $(inputElm).val().replace(/[^ 0-9A-Za-z.,-]/gi, '');
    inputElm.setSelectionRange(start, end);
}