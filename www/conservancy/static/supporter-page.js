/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn.
** License: GPLv3-or-later
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

$(document).ready(function() {
    var goal  = $('span#fundraiser-goal').text();
    var soFar = $('span#fundraiser-so-far').text();
    var donationCount = $('span#fundraiser-donation-count').text();
    var noCommaGoal = parseFloat(goal.replace(/,/g, ""));
    var noCommaSoFar = parseFloat(soFar.replace(/,/g, ""));
    var noCommaDonationCount = parseInt(donationCount.replace(/,/g, ""));
    var percentage = (parseFloat(noCommaSoFar) / parseFloat(noCommaGoal)) * 100;
    var curValue = 0.00;
    var incrementSoFar = 0.00;
    var curDonationCount = 0;
    var incrementDonationCount = Math.round( 0.01 * donationCount );

    $('span#fundraiser-percentage').css({ 'color'        : 'green',
                                          'font-weight'  : 'bold',
                                          'float'        : 'right',
                                          'margin-right' : '40%',
                                          'margin-top'   : '2.5%',
                                          'text-align'   : 'inherit'});
    function riseDonationProgressBar() {
        if (curValue >= percentage) {
            $('span#fundraiser-so-far').text(soFar);
            $("#progressbar").progressbar({ value :  percentage });
            $('span#fundraiser-percentage').text(percentage.toFixed(1) + "%");
        } else {
            var newVal = (curValue / 100.00) * noCommaGoal;
            $("#progressbar").progressbar({ value:  curValue });
            $('span#fundraiser-so-far').text(newVal.toLocaleString());
            curValue += 0.5;
            setTimeout(riseDonationProgressBar, 50);
        }
    }
    function riseDonationCount() {
        if (curDonationCount >= noCommaDonationCount) {
            $('span#fundraiser-donation-count').text(donationCount);
        } else {
            $('span#fundraiser-donation-count').text(curDonationCount.toLocaleString());
            incrementDonationCount += incrementDonationCount;
            setTimeout(riseDonationCount, 50);
        }
    }
    if (noCommaDonationCount > 0) {
        riseDonationCount();
    }
    if (noCommaSoFar > 0.00 and noCommaGoal > 0.00) {
        $('span#fundraiser-percentage').text("");
        $("#progressbar").progressbar({ value:  curValue });
        riseDonationProgressBar();
    }

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
    $(".dinner-form-submit").click(function (event) {
        validateFormAtSubmission($(".dinner-form input#amount"), event);
    });
    /* Handle toggling of annual/monthly form selections */
    $('.supporter-type-selection#monthly').hide();
    $('#annualSelector').css("font-weight", "bold").css("font-size", "127%");

    $("a[href$='monthly']").bind('click', function() {
        $('.supporter-type-selection#annual').hide();
        $('.supporter-type-selection#monthly').show();
        $('#monthlySelector').css("font-weight", "bold").css("font-size", "127%");
        $('#annualSelector').css("font-weight", "normal").css("font-size", "125%");
        $("#form-correction-needed").removeClass("form-error-show").addClass("form-error");
    });
    $("a[href$='annual']").bind('click', function() {
        $('.supporter-type-selection#annual').show();
        $('.supporter-type-selection#monthly').hide();
        $('#annualSelector').css("font-weight", "bold").css("font-size", "127%");
        $('#monthlySelector').css("font-weight", "normal").css("font-size", "125%");
    });
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
