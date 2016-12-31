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
    /* We've sometimes published links that say #renew instead of #renewal.
       Rewrite that to work as intended. */
    if (window.location.hash === "#renew") {
        window.location.hash = "#renewal";
    }
    var $selectorLink = supportTypeSelector(window.location.hash);
    if ($selectorLink.length > 0) {
        $window.scrollTop($selectorLink.offset().top);
    }
});

$(document).ready(function() {
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
                        parseInt(noCommaValue) >= parseInt(input.attr("min")));
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
    if (parseFloat($("form#annual").get(0).dataset.upgradeFromAmount) > 0) {
        supportTypeSelector("#annual").click();
        $(".supporter-type-selector").hide();
    }
    else if ($selectorLink.length === 0) {
        supportTypeSelector("#annual").click();
    }
});
