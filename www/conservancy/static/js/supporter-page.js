/* Copyright (C) 2012-2013 Denver Gingerich, 
** Copyright (C) 2013-2014 Bradley M. Kuhn,
** Copyright (C) 2016 Brett Smith.
** License: GPLv3-or-later
**  Find a copy of GPL at https://sfconservancy.org/GPLv3
*/

var NEW_AMOUNT_EVENT = 'conservancy:newamount';

var flipClass = function(elem, byeClass, hiClass) {
    var classList = elem.classList;
    classList.remove(byeClass);
    classList.add(hiClass);
}

var buildAmountData = function(amountInput) {
    var amountData = {
        minAmount: parseFloat(amountInput.min),
        newAmount: parseFloat(amountInput.value),
    }
    if (amountInput.dataset.oldAmount !== undefined) {
        amountData.oldAmount = parseFloat(amountInput.dataset.oldAmount);
    }
    return amountData;
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

    $('form.supporter-form').each(function(index, form) {
        var $amountInput = $('input[type=number]', form).first();
        var $amountError = $('.form-error', $amountInput[0].parentNode);

        $amountError.on(NEW_AMOUNT_EVENT, function(event, amountData) {
            var isValid = amountData.newAmount >= amountData.minAmount;
            if (amountData.oldAmount === undefined) {
                if (isValid) {
                    $amountError.addClass('hidden');
                } else {
                    flipClass($amountInput[0], 'valid', 'invalid');
                    $amountError.removeClass('hidden');
                }
            } else if (isValid) {
                flipClass($amountInput[0], 'invalid', 'valid');
                $amountError.fadeOut();
            } else if (amountData.oldAmount >= amountData.minAmount) {
                flipClass($amountInput[0], 'valid', 'invalid');
                $amountError.fadeIn();
            }
        });

        $amountInput.on('input', function(event) {
            event.target.classList.remove('invalid');
        }).on('focusout', function(event) {
            var amountInput = event.target;
            var amountData = buildAmountData(amountInput);
            $amountError.trigger(NEW_AMOUNT_EVENT, amountData);
            amountInput.dataset.oldAmount = amountData.newAmount;
        }).trigger('focusout');

        $(form).on('submit', function(event) {
            var amountData = buildAmountData($amountInput[0]);
            if (amountData.newAmount >= amountData.minAmount) {
                $formCorrectionNeeded.addClass('hidden');
            } else {
                $formCorrectionNeeded.removeClass('hidden')
                    .css("font-weight", "bold").css("font-size", "150%");
                event.preventDefault();
            }
        });
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
