(function (a) {
  a(document).ready(function () {
    a('#cssmenu').prepend('<div id="indicatorContainer"><div id="pIndicator"><div id="cIndicator"></div></div></div>');
    var f = a('#cssmenu>ul>li:first');
    a('#cssmenu>ul>li').each(function () {
      if (a(this).hasClass('active')) {
        f = a(this);
      }
    });
    var b = f.position().left;
    var g = f.width();
    b = b + g / 2 - 6;
    if (f.hasClass('has-sub')) {
      b -= 6;
    }
    a('#cssmenu #pIndicator').css('left', b);
    var e, d, c = a('#cssmenu pIndicator');
    a('#cssmenu>ul>li').hover(function () {
      e = a(this);
      var h = e.width();
      if (a(this).hasClass('has-sub')) {
        d = e.position().left + h / 2 - 12;
      } else {
        d = e.position().left + h / 2 - 6;
      }
      a('#cssmenu #pIndicator').css('left', d);
    }, function () {
      a('#cssmenu #pIndicator').css('left', b);
    });
    a('#cssmenu>ul').prepend('<li id="menu-button"></li>');
    a('#menu-button').click(function () {
      if (a(this).parent().hasClass('open')) {
        a(this).parent().removeClass('open');
      } else {
        a(this).parent().addClass('open');
      }
    });
  });
}(jQuery));