/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn,
** Copyright (C) 2016 Brett Smith.
** License: GPLv3-or-later
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

var supportTypeSelector = function(supportTypeHash) {
    return $(".supporter-type-selector a[href=" + supportTypeHash + "]");
};

var $window = $(window);

$window.load(function() {
    var $selectorLink = supportTypeSelector(window.location.hash);
    if ($selectorLink.length > 0) {
        $window.scrollTop($selectorLink.offset().top);
    }
});

$(document).ready(function() {
    var siteFinalGoal = $('span#site-fundraiser-final-goal').text();
    var noCommaSiteFinalGoal = parseInt(siteFinalGoal.replace(/,/g, ""));
    var siteMatchCount = $('span#site-fundraiser-match-count').text();
    var noCommaSiteMatchCount = parseInt(siteMatchCount.replace(/,/g, ""));
    if (! noCommaSiteMatchCount) {
        noCommaSiteMatchCount = "0";
    }
    var barParts = [{
        value: (noCommaSiteMatchCount / noCommaSiteFinalGoal) * 100,
        text: noCommaSiteMatchCount.toLocaleString() + " matched!",
        barClass: "progress",
        textClass: "soFarText",
    }];
    if (barParts[0].value < 100) {
        var matchesLeft = noCommaSiteFinalGoal - noCommaSiteMatchCount;
        barParts.push({
            value: 100,
            text: matchesLeft.toLocaleString() + " to go!",
            barClass: "final-goal",
            textClass: "goalText",
        });
    }
    var $progressBar = $('#siteprogressbar');
    $progressBar.empty();
    $progressBar.multiprogressbar(barParts);

    $('span#fundraiser-percentage').css({ 'color'        : 'green',
                                          'font-weight'  : 'bold',
                                          'float'        : 'right',
                                          'margin-right' : '40%',
                                          'margin-top'   : '2.5%',
                                          'text-align'   : 'inherit'});

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
    $(".t-shirt-size-selector").hide();
    $('input[name=on0]:radio').change(function() {
        var input=$(this);
        var tShirtSelector = input.parent().children('.t-shirt-size-selector')
        var noShippingSelector = input.parent().children('input#no_shipping');
        var value = input.val();
        if (value == "wantGiftYes") {
            tShirtSelector.show();
            noShippingSelector.val("2");
        } else {
            tShirtSelector.hide();
            noShippingSelector.val("0");
        }
    });

    // Forms start in "invalid" form, with the errors shown, so that
    // non-Javascript users see the errors by default and know what they must
    // enter.  The following two lines correct that.
    $('*#amount').addClass("valid");
    $('.supporter-form-inputs .form-error-show')
        .removeClass('form-error-show').addClass('form-error');
    $('.dinner-form-inputs .form-error-show')
        .removeClass('form-error-show').addClass('form-error');

    $('*#amount').on('input', function() {
        var input=$(this);
        var value = input.val();
        var errorElement=$("span#error", input.parent());
        var noCommaValue = value;
        noCommaValue = value.replace(/,/g, "");
        var re = /^((\d{1,3}(,?\d{3})*?(\.\d{0,2})?)|\d+(\.\d{0,2})?)$/;
        var isValid = ( re.test(value) &&
                        parseInt(noCommaValue) >= parseInt(input.attr("minimum")));
        if (isValid)  {
           input.removeClass("invalid").addClass("valid");
           errorElement.removeClass("form-error-show").addClass("form-error");
           $("#form-correction-needed").removeClass("form-error-show").addClass("form-error");
        }
        else {
            input.removeClass("valid").addClass("invalid");
            errorElement.removeClass("form-error").addClass("form-error-show");
        }
    });
    var validateFormAtSubmission = function(element, event) {
            var valid = element.hasClass("valid");
            if (! valid) {
                $("#form-correction-needed").removeClass("form-error").addClass("form-error-show")
                                        .css("font-weight", "bold").css("font-size", "150%");
	        event.preventDefault();
            } else {
                $("#form-correction-needed").removeClass("form-error-show").addClass("form-error");
            }
    };
    $(".supporter-form-submit#monthly").click(function (event) {
        validateFormAtSubmission($(".supporter-form#monthly input#amount"), event);
    });
    $(".supporter-form-submit#annual").click(function (event) {
        validateFormAtSubmission($(".supporter-form#annual input#amount"), event);
    });
    $(".supporter-form-submit#renewal").click(function (event) {
        validateFormAtSubmission($(".supporter-form#renewal input#amount"), event);
    });
    $(".dinner-form-submit").click(function (event) {
        validateFormAtSubmission($(".dinner-form input#amount"), event);
    });

    var selectSupportType = function(event) {
        var $selectedLink = $(event.target);
        $(".supporter-type-selector a").removeClass("supporter-type-selector-selected");
        $selectedLink.addClass("supporter-type-selector-selected");
        $(".supporter-type-selection").each(function(index, element) {
            var $element = $(element);
            if (event.target.href.endsWith("#" + element.id)) {
                $element.show();
            } else {
                $element.hide();
            }
        });
        $("#form-correction-needed").removeClass("form-error-show").addClass("form-error");
        return false;
    };
    $(".supporter-type-selector a").bind("click", selectSupportType);

    var selectSupportTypeFromHash = function() {
        return supportTypeSelector(window.location.hash).click();
    };
    $window.bind("hashchange", selectSupportTypeFromHash);
    var $selectorLink = selectSupportTypeFromHash();
    if ($selectorLink.length === 0) {
        supportTypeSelector("#annual").click();
    }

    $( ".footnote-mark" ).tooltip({
        items: "a",
        hide: { duration: 5000 },
        position: {
            my: "center bottom-20",
            at: "center left",
            using: function( position, feedback ) {
                $( this ).css( position );
                $( "<div>" )
                    .addClass( "arrow" )
                    .addClass( feedback.vertical )
                    .addClass( feedback.horizontal )
                    .appendTo( this );
            }
        },
        content: function() {
            return $('.footnote-1-text').text();
        }
    });
});
