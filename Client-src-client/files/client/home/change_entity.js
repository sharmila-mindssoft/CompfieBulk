
function getLegalEntityChange(LE_ID, LE_NAME){
    var sEntity = [];
    if(LE_ID != 'all'){
        sEntity.push(parseInt(LE_ID))
    }else{
        var USER_LE = client_mirror.getUserLegalEntity();
        $.each(USER_LE, function(key, value) {
            sEntity.push(value.le_id);
        });
    }
    window.sessionStorage.selectedEntity = sEntity;
    window.sessionStorage.selectedEntityName = LE_NAME;
    location.reload();
}

function loadLegalEntityListChange(){
    var LC = '';
    var LC_COUNT = 1;
    var USER_LE = client_mirror.getUserLegalEntity();
    $('.tbody-legal-panel-change').empty();
    $.each(USER_LE, function(key, value) {
        if(LC != value.c_id){
            var countrytableRow = $('#le-templates-change .p-head');
            var clone = countrytableRow.clone();
            $('.acc-title', clone).attr('id', 'heading'+LC_COUNT);
            $('.panel-title a span', clone).text(value.c_name);
            $('.panel-title a', clone).attr('href', '#collapse'+LC_COUNT);
            $('.panel-title a', clone).attr('aria-controls', 'collapse'+LC_COUNT);
            $('.coll-title', clone).attr('id', 'collapse'+LC_COUNT);
            $('.coll-title', clone).attr('aria-labelledb', 'heading'+LC_COUNT);
            $('.tbody-legal-panel-change').append(clone);
	        LC = value.c_id;
	        LC_COUNT++;
        }
        var LERow = $('#le-values-change .table-le-values .row-le-values');
        var clone2 = LERow.clone();
        $('.le_name', clone2).text(value.le_name);
        $(clone2).on('click', function() {
            getLegalEntityChange(value.le_id, value.le_name);
        });
        $('#collapse' + (LC_COUNT-1) + ' .tbody-le-list-change').append(clone2);
    });
}
