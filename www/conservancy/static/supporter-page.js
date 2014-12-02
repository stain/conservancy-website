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
    $('#amount').on('input', function() {
        var input=$(this);
        var value = input.val();
        var errorElement=$("span", input.parent());

        var re = /^[0-9\,\.]+$/;
        var isValid = (re.test(value) && parseInt(value) >= 120);
        if (isValid)  {
           input.removeClass("invalid").addClass("valid");
           errorElement.removeClass("form-error-show").addClass("form-error");
        }
        else {
            input.removeClass("valid").addClass("invalid");
            errorElement.removeClass("form-error").addClass("form-error-show");
        }
    });
    /* Handle toggling of annual/monthly form selections */
    $('.supporter-type-selection#monthly').hide();
    $('#annualSelector').css("font-weight", "bold").css("font-size", "127%");

    $("a[href$='monthly']").bind('click', function() {
        $('.supporter-type-selection#annual').hide();
        $('.supporter-type-selection#monthly').show();
        $('#monthlySelector').css("font-weight", "bold").css("font-size", "127%");
        $('#annualSelector').css("font-weight", "normal").css("font-size", "125%");
    });
    $("a[href$='annual']").bind('click', function() {
        $('.supporter-type-selection#annual').show();
        $('.supporter-type-selection#monthly').hide();
        $('#annualSelector').css("font-weight", "bold").css("font-size", "127%");
        $('#monthlySelector').css("font-weight", "normal").css("font-size", "125%");
    });

  });

$(window).load(function () {
    verifySelctionCorrectOnPageLoad = function() {
        var ourURL = document.URL;
        if (ourURL.search("#monthly") > 0) {
            $('.supporter-type-selection#annual').hide();
            $('.supporter-type-selection#monthly').show();
            $('#monthlySelector').css("font-weight", "bold").css("font-size", "127%");
            $('#annualSelector').css("font-weight", "normal").css("font-size", "125%");
        }
        if (ourURL.search("#annual") > 0) {
            $('.supporter-type-selection#monthly').hide();
            $('.supporter-type-selection#annual').show();
            $('#annualSelector').css("font-weight", "bold").css("font-size", "127%");
            $('#monthlySelector').css("font-weight", "normal").css("font-size", "125%");
        }
    }
    if (location.hash) {
        setTimeout(verifySelctionCorrectOnPageLoad, 1);
    }
    window.addEventListener("hashchange", verifySelctionCorrectOnPageLoad);
});
