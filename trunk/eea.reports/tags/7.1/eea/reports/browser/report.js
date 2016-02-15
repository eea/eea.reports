/*
 * Hides the content of a Publication with Folders through a
 * slider similar to the data-and-maps table show and hide
 * eg: http://eea.europa.eu/publications/corinair-nomenclatures
 * */
var Reports = {'version': '1.1.0'};
Reports.Tree = {
    initialize: function(){
        this.elements = jQuery('li.tree-level-3:has(ul)');
        var tree = this;
        this.elements.each(function(){
            var $li = jQuery(this).css('list-style', 'none');
            var $link = $li.children('a');
            var div = jQuery('<div>');
            div.addClass('tree-level-arrow');
            div.addClass('tree-level-open');
            div.css('margin-left', '-1.7em');
            var element = this;
            $link.add(div).click(function(ev){
                tree.toggle(element, div);
                ev.preventDefault();
            });
            jQuery(this).prepend(div);
            $link.click();
        });
    },

    toggle: function(element, button){
        if(jQuery(button).hasClass('tree-level-open')){
            this.close(element, button);
        }else{
            this.open(element, button);
        }
    },

    open: function(element, button){
        jQuery(button).removeClass('tree-level-close');
        jQuery(button).addClass('tree-level-open');
        jQuery('ul', element).slideDown();
    },

    close: function(element, button){
        jQuery(button).removeClass('tree-level-open');
        jQuery(button).addClass('tree-level-close');
        jQuery('ul', element).slideUp();
    }
};

jQuery(document).ready(function(){
    Reports.Tree.initialize();
});
