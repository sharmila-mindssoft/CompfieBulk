$(document).ready(function(){

  $('#accordian-risk > ul > li:has(ul)').addClass("has-sub");

  $('#accordian-risk > ul > li > div.accordian-risk-block').click(function() {
    var checkElement = $(this).next();
    
    $('#accordian-risk li').removeClass('active');
    $(this).closest('li').addClass('active');	
    
    
    if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
      $(this).closest('li').removeClass('active');
      checkElement.slideUp('normal');
    }
    
    if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
      $('#accordian-risk ul ul:visible').slideUp('normal');
      checkElement.slideDown('normal');
    }
    
    if (checkElement.is('ul')) {
      return false;
    } else {
      return true;	
    }		
  });

});