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
        var $children = $(this).children();
        $children.each(function(i,v){
            if ( this.tagName === "H3" ) {
                $(this).detach().replaceWith('<li>' + this.innerHTML + '</li>').appendTo('#eea-tabs');
            }
            else {
                $(this).addClass('eea-tabs-panel').appendTo('#eea-tabs-panels'); 
            }
        });
    });
    var figure_batch = function() {
        $(".map-photo-album").delegate('.listingBar', "click", function(e){
            var item = e.target, queries_index, queries, link;
            if ( item.tagName === "A" ) {
                item = item.href;
                queries_index = item.indexOf('?');
                queries = item.slice(queries_index);
                link = item.slice(0, queries_index);
                link = link + '/report_figures' + queries;
                $.get(link, function(data) {
                    $(".map-photo-album").html($(data).find('.map-photo-album').children());
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
