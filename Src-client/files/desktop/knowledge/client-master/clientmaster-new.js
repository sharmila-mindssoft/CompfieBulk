function initialize(type_of_initialization){
  showPage(type_of_initialization);
  if(type_of_initialization == "list"){

  }else if(type_of_initialization == "add"){

  }else if(type_of_initialization == "edit"){

  }else{
    // Invalid initialization Do nothing
  }
}

function showPage(type_of_initialization){
  if(type_of_initialization == "list"){
    $("#clientgroup-view").show();
    $("#clientgroup-add").hide();
  }else{
    $("#clientgroup-view").hide();
    $("#clientgroup-add").show();
  }
}

/*
  Handling Button Clicks
*/
$(".btn-clientgroup-add").click(function(){
    addClient();
});


/*
  Handling Add
*/
function addClient(){
    initialize("add");
}

$(document).ready(function () {
    initialize("list");
});
