function parseHyphenated(a) {
  return a.split('-');
}
function toUpperCamelCase(d) {
  var a = [];
  for (var b = 0; b < d.length; ++b) {
    var c = d[b];
    c = c[0].toUpperCase() + c.slice(1);
    a.push(c);
  }
  return a.join('');
}
function hyphenatedToUpperCamelCase(a) {
  var b = parseHyphenated(a);
  return toUpperCamelCase(b);
}

var m_names = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');

function date_format(date){
  day = date.getDate();
  if (day < 10) {
    day = '0' + day;
  }
  month = m_names[date.getMonth()];
  year = date.getFullYear();
  return day + '-' + month + '-' + year;
}

function current_date(){
  return date_format(new Date());
}

function past_days(days) {
  dat = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * days);
  return date_format(dat);
}
