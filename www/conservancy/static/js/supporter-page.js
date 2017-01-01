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

var checkAmountValid = function(amountInput) {
    var value = parseFloat(amountInput.value);
    var min = parseFloat(amountInput.min);
    /* Is the value is a valid float, it will stringify back to itself. */
    var isValid = (String(value) === amountInput.value) && (value >= min);
    amountInput.dataset.valid = isValid ? '1' : '0';
    return isValid;
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
    var $formCorrectionNeeded = $('#form-correction-needed');
    $formCorrectionNeeded.addClass('hidden');

    $('form.supporter-form input[type=number]').on('input', function(event) {
        event.target.classList.remove('invalid');
    }).on('focusout', function(event) {
        var amountInput = event.target;
        var wasValid = amountInput.dataset.valid === '1';
        var isValid = checkAmountValid(amountInput);
        if (isValid) {
            flipClass(amountInput, 'invalid', 'valid');
            if (!wasValid) {
                $('.form-error', amountInput.parentNode).fadeOut();
            }
        } else if (wasValid) {
            flipClass(amountInput, 'valid', 'invalid');
            $('.form-error', amountInput.parentNode).fadeIn();
        }
    }).each(function(index, elem) {
        if (checkAmountValid(elem)) {
            $('.form-error', elem.parentNode).addClass('hidden');
        } else {
            elem.classList.add('invalid');
            $('.form-error', elem.parentNode).removeClass('hidden');
        }
    });

    $('form.supporter-form').on('submit', function(event) {
        if (checkAmountValid($('input[name=amount]', event.target)[0])) {
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
