/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn.
** License: GPLv3-or-ater
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

$(document).ready(function() {
    $('.toggle-content').hide();

    $('.toggle-control')
     .addClass('clickable')
     .bind('click', function() {
        var $control = $(this);
        var $parent = $control.parents('.toggle-unit');

        $parent.toggleClass('expanded');
        $parent.find('.toggle-content').slideToggle();

        // if control has HTML5 data attributes, use to update text
        if ($parent.hasClass('expanded')) {
            $control.html($control.attr('data-expanded-text'));
        } else {
            $control.html($control.attr('data-text'));
        }
    });
    $('a.donate-now')
      .addClass('clickable')
      .bind('click', function() {
        var $control = $('#donate-box');

        $control.toggleClass('expanded');
        $control.find('.toggle-content').slideUp("slow");
        $control.find('.toggle-content').slideDown("slow");
    });
  });
