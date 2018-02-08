var clientGroupsList = [];
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');

function initialize(type_of_initialization) {
	displayLoader();
	function onSuccess(data) {
	    clientGroupsList = data.client_group_list;
	    hideLoader();
	}

	function onFailure(error) {
	    displayMessage(error);
	    hideLoader();
	}
	mirror.getClientGroupsList(function(error, response) {
		console.log(error, response)
	    if (error == null) {
	        onSuccess(response);
	    } else {
	        onFailure(error);
	    }
	});
}

//Load All Groups  ---------------------------------------------------------------------------------------------
function loadClientGroups(e, textval, callback) {
	groupSelect_id.val('');
    groupListBox.show();
    groupUListCtrl.empty();

    var grplist = [];
    if (textval.length > 0) {
    	for (var i in clientGroupsList) {
    		if (~clientGroupsList[i].group_name.toLowerCase().indexOf(textval.toLowerCase())) {
    			var ul_list = document.getElementById("ac-group");
                var li_list = ul_list.getElementsByTagName("li");
                var occur = -1;
                for (var j = 0; j < li_list.length; j++) {
                    if (li_list[j].textContent == clientGroupsList[i].group_name)
                        occur = 1;
                }
                if (occur < 0) {
                    var obj = $(".group-list-drop-down li");
                    var clone = obj.clone();
                    clone.attr("id", clientGroupsList[i].client_id);
                    clone.click(function() {
                        activate_text(this, callback);
                    });
                    clone.text(clientGroupsList[i].group_name);
                    groupUListCtrl.append(clone);
                }
    		}
    	}
    } else {
        $('.ac-textbox').hide();
    }
    onArrowKey_Client(e, 'ac-textbox', 'group', callback);
}

// Arrow key functionality
function onArrowKey_Client(e, ac_item, multipleselect, callback) {
    var ccount;
    if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
        chosen = '';
    }
    if (e.keyCode == 40) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen + 1 < $('.' + ac_item + ' li').length) {
            chosen++;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen > 0) {
            chosen--;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 13) {
        var ac_id = $('.' + ac_item + ' li:eq(' + chosen + ')').attr('id');
        var ac_name = $('.' + ac_item + ' li:eq(' + chosen + ')').text();
        groupSelect_name.val(ac_name);
        groupSelect_id.val(ac_id);
        return false;
    }
}
//store the selected groups name and id
function onClientGroupSuccess(val) {
    groupSelect_name.val(val[1]);
    groupSelect_id.val(val[0]);
    groupSelect_name.focus();
}

// To invoke loading of client groups list
groupSelect_name.keyup(function(e) {
    var textval = $(this).val();
    loadClientGroups(e, textval, function(val) {
        onClientGroupSuccess(val);
    });
});

// Document Loading process

$(document).ready(function() {
	$('.view-summary').hide();
    $(".animateprogress").click(function() {
      $('.invaliddata').hide();
      $('.view-summary').hide();
      $('.download-file').hide();
      setTimeout(function(){
    $('#myModal').modal('hide');
      $('.invaliddata').show();
      $('.view-summary').show();
      $('.download-file').hide();
      displayMessage("Records are not uploaded successfully");
      }, 2000);
    });
    initialize();
});