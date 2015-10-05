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
        var tableCount = 0;
        var grid = $(".statutory-master");
        if (data.length > 0) {
            console.log(data);

            var table = $("<table></table>");
            var headerRow = $("<tr></tr>");
            var row = $("<tr></tr>");
            for (var i=0; i< data.length; i++) {
                var tableCount = 0;
                if (data.length % 4 == 0) {
                    tableCount += 1;
                    grid.appendTo(table);
                    table = $("<table></table>");
                    headerRow = $("<tr></tr>");
                    row = $("<tr></tr>");
                }
                else {

                    var headerCell = $("<td></td>");
                    headerCell.text(data[i][2]);
                    headerRow.appendTo(headerCell);
                    
                    var rowCell = $("<td></td>");
                    var list = $("<ul />");
                    var input = $("<input type='text' class='filter-text-box' placeholder='Search'>");
                    var addText = $("<div align='center'> <input type='text' calss='input-box' placeholder=" 
                        + data[i][2] + "/> <span> <img src='/Static/images/icon-plus.png' /> </span> "
                        + "</div>");
                    rowCell.appendTo(input);
                    rowCell.appendTo(list);
                    rowCell.appendTo(addText);
                }
            }
        }
        
    });
}

$(".master-country").keydown(function (e) {
    if (e.keyCode == 13) {
        level_by_country($(".master-country").val());
    }
});


