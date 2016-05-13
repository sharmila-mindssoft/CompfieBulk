!function($){ 'use strict';

    $.fn.filtertable = function(options) {
        var filtertable = this;
        var filtertableCore = new (function($filtertable) {
        
            this.getIndex = function($field) {
                return $field.parents('tr').children('td, th').index($field);
            };
            
            this.getBody = function() {
                return $filtertable.children('tbody');
            };
            
            this.getRows = function() {
                return this.getBody().children('tr');
            };
            
            this.getField = function(index, $row) {
                return $row.children('td, th').eq(index);
            };
            
            this.getValue = function(index, $row) {
                return this.getField(index, $row).text();
            };
            
        })($(this));   
        
        this.filterList = [];
        
        this.displayAll = function() {

            filtertableCore.getRows().each(function() {
                $(this).show();
            });
          
            return this;
        };

        this.filter = function filter(index, matches) {
        
            var regex = new RegExp(matches, 'i');
            
            filtertableCore.getRows().each(function () {
                if(true !== regex.test(filtertableCore.getValue(index, $(this)))) {
                    $(this).hide();
                }
            });
          
            return this;
        };
        
        this.addFilter = function addFilter(selector) {
            filtertable.filterList.push(selector);
            var filterAction = function() {
            
                 filtertable.displayAll();
                 
                 $(filtertable.filterList).each(function(index, selector) {
                 
                    $(filtertable).find(selector).each(function() {
                        var $this =  $(this);
                        filtertable.filter(filtertableCore.getIndex($this.parent('td, th')), $this.val());  
                    });
                 
                 });
            };
            
            $(selector).on('change keyup keydown', filterAction);
            
            filterAction();
            return this;
        };          
        return this;
    };

    

}(jQuery);