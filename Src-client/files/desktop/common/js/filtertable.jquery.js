!function (a) {
  a.fn.filtertable = function (c) {
    var b = this;
    var f = new function (g) {
      this.getIndex = function (h) {
        return h.parents('tr').children('td, th').index(h);
      };
      this.getBody = function () {
        return g.find('tbody');
      };
      this.getRows = function () {
        return this.getBody().children('tr');
      };
      this.getField = function (i, h) {
        return h.children('td, th').eq(i);
      };
      this.getValue = function (i, h) {
        return this.getField(i, h).text();
      };
    }(a(this));
    this.filterList = [];
    this.displayAll = function () {
      f.getRows().each(function () {
        a(this).show();
      });
      return this;
    };
    this.filter = function e(h, j) {
      var g = j.replace(/[\(\)\[\]]/gi, '');
      var i = new RegExp(g, 'i');
      f.getRows().each(function () {
        if (true !== i.test(f.getValue(h, a(this)))) {
          a(this).hide();
        }
      });
      return this;
    };
    this.addFilter = function d(h) {
      b.filterList.push(h);
      var g = function () {
        b.displayAll();
        a(b.filterList).each(function (j, i) {
          a(b).find(i).each(function () {
            var k = a(this);
            b.filter(f.getIndex(k.parent('td, th')), k.val());
          });
        });
      };
      a(h).on('change keyup keydown', g);
      g();
      return this;
    };
    return this;
  };
}(jQuery);