$(document).ready(function(){
  $('#accordian > ul > li:has(ul)').addClass("has-sub");
	
  $('#accordian > ul > li > div.accordian-block').click(function() {
	
	
	var checkElement = $(this).next();
    
    $('#accordian li').removeClass('active');
    $(this).closest('li').addClass('active');	
		
    if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
      $(this).closest('li').removeClass('active');
      checkElement.slideUp('normal');
    }
    
    if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
      $('#accordian ul ul:visible').slideUp('normal');
      checkElement.slideDown('normal');
    }
    
    if (checkElement.is('ul')) {
      return false;
    } else {
      return true;	
    }		
  });
  
  $(".pinToggles").click(function(event){
    event.stopPropagation();
});

});

