/* Copyright (C) 2012-2013 Denver Gingerich,
** Copyright (C) 2013-2014 Bradley M. Kuhn,
** Copyright (C) 2016 Brett Smith.
** License: GPLv3-or-later
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

$(document).ready(function() {
    /* When the browser doesn't support any video source, replace it
       with the HTML inside the <video> element. */
    var showVideoInnerHTML = function(event) {
        var video = event.target.parentNode;
        var div = document.createElement('div');
        div.classList = video.classList;
        div.innerHTML = video.innerHTML;
        video.parentNode.replaceChild(div, video);
    }
    $('video').each(function(index, video) {
        $('source', video).last().on('error', showVideoInnerHTML);
    });

    /* Set up the fundraiser multiprogressbar near the top of each page. */
    var siteFinalGoal = $('span#site-fundraiser-final-goal').text();
    var noCommaSiteFinalGoal = parseInt(siteFinalGoal.replace(/,/g, ""));
    var siteMatchCount = $('span#site-fundraiser-match-count').text();
    var noCommaSiteMatchCount = parseInt(siteMatchCount.replace(/,/g, ""));
    if (! noCommaSiteMatchCount) {
        noCommaSiteMatchCount = "0";
    }
    var barParts = [{
        value: (noCommaSiteMatchCount / noCommaSiteFinalGoal) * 100,
        text: "$" + noCommaSiteMatchCount.toLocaleString() + " matched!",
        barClass: "progress",
        textClass: "soFarText",
    }];
    if (barParts[0].value < 100) {
        var matchesLeft = noCommaSiteFinalGoal - noCommaSiteMatchCount;
        barParts.push({
            value: 100,
            text: "$" + matchesLeft.toLocaleString() + " to go!",
            barClass: "final-goal",
            textClass: "goalText",
        });
    }
    $('#siteprogressbar').empty().multiprogressbar({parts: barParts});

    $('span#fundraiser-percentage').css({ 'color'        : 'green',
                                          'font-weight'  : 'bold',
                                          'float'        : 'right',
                                          'margin-right' : '40%',
                                          'margin-top'   : '2.5%',
                                          'text-align'   : 'inherit'});

    /* Set up donation form elements used across the whole site. */
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
        var $otherTextControl = $('.donate-sidebar');

        setTimeout(function() { $control.find('.toggle-content').slideUp(100);
                                $control.toggleClass('expanded');
                                $control.find('.toggle-content').slideDown(800).fadeOut(10);
                                $otherTextControl.find('.donate-box-highlight').fadeOut(100);
                              }, 300);
          setTimeout(function() { $control.find('.toggle-content').fadeIn(2000);
                                  $otherTextControl.find('.donate-box-highlight')
                                  .css({'font-weight': 'bold', 'font-size' : '110%' });
                                  $otherTextControl.find('.donate-box-highlight').fadeIn(10000);
                                }, 500);
    });

    $('input[name=on0]:radio').on('change', function(event, duration) {
        var $input = $(this);
        var wantShirt = $input.val() == "wantGiftYes";
        var $form = $input.parents('form').last();
        var $tShirtSelector = $('.t-shirt-size-selector', $form);
        $('input', $tShirtSelector).prop('disabled', wantShirt);
        $('input[name=no_shipping]', $form).val(wantShirt ? '2' : '0');
        if (wantShirt) {
            $tShirtSelector.slideDown(duration);
        } else {
            $tShirtSelector.slideUp(duration);
        }
    }).filter(':checked').trigger('change', 0);
});
