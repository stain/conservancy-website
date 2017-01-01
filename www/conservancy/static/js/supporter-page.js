/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn,
** Copyright (C) 2016 Brett Smith.
** License: GPLv3-or-later
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

var flipClass = function(elem, byeClass, hiClass) {
    var classList = elem.classList;
    classList.remove(byeClass);
    classList.add(hiClass);
}

var amountIsValid = function(amountInput) {
    var value = parseFloat(amountInput.value);
    var min = parseFloat(amountInput.min);
    /* Is the value is a valid float, it will stringify back to itself. */
    return (String(value) === amountInput.value) && (value >= min);
}

var supportTypeSelector = function(supportTypeHash) {
    return $(supportTypeHash + "Selector");
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
    // enter.  Now we hide those for JavaScript users:
    $('.form-error').addClass('hidden');
    var $formCorrectionNeeded = $('#form-correction-needed');

    $('form.supporter-form input[type=number]').on('focusout', function(event) {
        var amountInput = event.target;
        var wasValid = !amountInput.classList.contains('invalid');
        var isValid = amountIsValid(amountInput);
        if (!wasValid && isValid) {
            flipClass(amountInput, 'invalid', 'valid');
            $('.form-error', amountInput.parentNode).addClass('hidden');
        } else if (wasValid && !isValid) {
            flipClass(amountInput, 'valid', 'invalid');
            $('.form-error', amountInput.parentNode).removeClass('hidden');
        }
    });

    $('form.supporter-form').on('submit', function(event) {
        if (amountIsValid($('input[name=amount]', event.target)[0])) {
            $formCorrectionNeeded.addClass('hidden');
        } else {
            $formCorrectionNeeded.removeClass('hidden')
                .css("font-weight", "bold").css("font-size", "150%");
            event.preventDefault();
        }
    });

    var selectSupportType = function(event) {
        var $selectedLink = $(event.target);
        $(".supporter-type-selector a").removeClass("supporter-type-selector-selected");
        $selectedLink.addClass("supporter-type-selector-selected");
        $(".supporter-type-selection").hide();
        var hashIndex = event.target.href.lastIndexOf('#');
        if (hashIndex > -1) {
            $(event.target.href.slice(hashIndex)).show();
        }
        $formCorrectionNeeded.addClass('hidden');
        return false;
    };
    $(".supporter-type-selector a").bind("click", selectSupportType);

    var selectSupportTypeFromHash = function() {
        return supportTypeSelector(window.location.hash).click();
    };
    $window.bind("hashchange", selectSupportTypeFromHash);
    if (selectSupportTypeFromHash().length === 0) {
        supportTypeSelector("#annual").click();
    }
});
