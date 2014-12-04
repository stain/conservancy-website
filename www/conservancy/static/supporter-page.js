/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn.
** License: GPLv3-or-later
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
    $(".t-shirt-size-selector").hide();
    $('input[name=os1]:radio').change(function() {
        var input=$(this);
        var value = input.val();
        if (value == "Yes") {
            $(".t-shirt-size-selector").show();
            $("#no_shipping").val("2");
        } else {
            $(".t-shirt-size-selector").hide();
            $("#no_shipping").val("0");
        }
    });
    $('*#amount').addClass("valid");
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
    $("#supporter-form-submit").click(function(event){
	var valid = $('.amount').hasClass("valid");
        if (! valid) {
            $("#form-correction-needed").removeClass("form-error").addClass("form-error-show")
                                        .css("font-weight", "bold").css("font-size", "150%");
	    event.preventDefault();
        } else {
            $("#form-correction-needed").removeClass("form-error-show").addClass("form-error");
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
