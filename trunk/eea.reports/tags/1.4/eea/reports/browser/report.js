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
        if(jQuery(this).attr('href') == '#'){
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

jQuery(document).ready(function(){
  Reports.Tree.initialize();
});
