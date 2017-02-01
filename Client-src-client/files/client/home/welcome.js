var LastAct = '';
var actCount = 1;
function loadLegalEntityList(user_le){

	    $.each(user_le, function(key, value) {
	        if(LastAct != value.le_name){
	            var acttableRow = $('#act-templates .p-head');
	            var clone = acttableRow.clone();

	            $('.acc-title', clone).attr('id', 'heading'+actCount);
	            $('.panel-title a span', clone).text(value.level_1_s_name);
	            $('.panel-title a', clone).attr('href', '#collapse'+actCount);
	            $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

	            $('.coll-title', clone).attr('id', 'collapse'+actCount);
	            $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);

	           
	            $('.tbody-legal-panel').append(clone);

	        LastAct = value.level_1_s_name;
	        actCount = actCount + 1;
	        }

       
        /*var complianceDetailtableRow = $('#statutory-value .table-statutory-values .compliance-details');
        var clone2 = complianceDetailtableRow.clone();
        var combineId = value.comp_id + '#' + value.level_1_s_id + '#' + value.u_id;
        $('.combineid-class', clone2).attr('id', 'combineid'+statutoriesCount);
        $('.combineid-class', clone2).val(combineId);

        if(value.s_s == 0){
            clone2.addClass('new_row');
        }else if(value.s_s == 4){
            clone2.addClass('rejected_row');
        }

        $('.sno', clone2).text(statutoriesCount);
        
        $('#collapse'+count+' .tbody-legal-panel').append(clone2);

        
        statutoriesCount++;
        sno++;*/
    });

}

$(document).ready(function () {
  if (!client_mirror.verifyLoggedIn())
    return;
  var user_le = client_mirror.getUserLegalEntity();
  loadLegalEntityList(user_le);
});
