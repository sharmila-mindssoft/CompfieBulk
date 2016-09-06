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