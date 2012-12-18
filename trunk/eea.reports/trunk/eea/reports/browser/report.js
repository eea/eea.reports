var Reports = {'version': '1.0.0'};
Reports.Tree = {
    initialize: function(){
        this.elements = jQuery('li.tree-level-3:has(ul)');
        var tree = this;
        this.elements.each(function(){
            jQuery(this).css('list-style', 'none');
            var div = jQuery('<div>');
            div.addClass('tree-level-arrow');
            div.addClass('tree-level-open');
            div.css('margin-left', '-1.7em');
            if (jQuery.browser.msie && jQuery.browser.version < 8){
                div.css('margin-left', '-2.1em');
            }
            var element = this;
            div.click(function(evt){
                tree.toggle(element, this);
            });
            jQuery(this).prepend(div);
            div.click();

            jQuery('a:first', jQuery(element)).click(function(evt){
                if(jQuery(this).attr('href') === '#'){
                    tree.toggle(element, jQuery('div:first', jQuery(element)));
                    return false;
                }
            });
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

jQuery(document).ready(function($){
    Reports.Tree.initialize();
    if(window.Figures){
        window.Figures.Load();
    }
    
    var $publication_controls = $("#publication_versions_controls");
    $publication_controls.click(function(e){
        var $target = $(e.target);
        if ( $target.hasClass('first') ) {
            $target.addClass('hidden').next().removeClass('hidden');
            $publication_controls.next().slideDown();
        }
        else {
            $target.addClass('hidden').prev().removeClass('hidden');
            $publication_controls.next().slideUp();
        }
        e.preventDefault();
    });

    var related_items = $("#relatedItems, #publicationMaps");
    related_items.find('.visualNoMarker').each(function(i,v) {
        var $self = $(this);
        var $children = $self.children();
        $children.each(function(i,v){
            if ( this.tagName === "H3" ) {
                $('<li />').html($(this).detach().html()).appendTo('#eea-tabs');
            }
            else {
                $(this).addClass('eea-tabs-panel')
                       .appendTo('#eea-tabs-panels');
                $(this).data($self.data());
            }
        });
    });
    var figure_batch = function() {
        var $tab_panels = $("#eea-tabs-panels");
        $tab_panels.delegate('.listingBar', "click", function(e){
            var item = e.target, queries_index, queries, href, link, data_attr;
            var $panel = $(this).closest('.eea-tabs-panel');
            if ( item.tagName === "A" ) {
                $panel.html('<img src="++resource++faceted_images/ajax-loader.gif" />');
                data_attr = $panel.data();
                href = item.href;
                if ( href.indexOf('b=true') === -1 ) {
                    queries_index = href.indexOf('?');
                    queries = href.slice(queries_index);
                    link = href.slice(0, queries_index);
                    href = link               +
                           data_attr.template +
                           queries            +
                           '&'                +
                           $.param({ m: data_attr.relation, b: true, c: data_attr.count });
                }
                $.get(href, function(data) {
                    $panel.html($(data).children().eq(1).remove());
                });
            }
            e.preventDefault();
        });
    };
    if ( related_items.length ) {
        $("#eea-tabs-panels").addClass('eea-tabs-panels');
        $("#eea-tabs").addClass('eea-tabs');
        window.EEA.eea_tabs();
        figure_batch();
    }
});
