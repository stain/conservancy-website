// Handles related-objects functionality: lookup link for raw_id_admin=True
// and Add Another links.

function showPopupFromLink(elem, nameTrimRegexp, popupParamName) {
    var name = elem.id.replace(nameTrimRegexp, '');
    // IE doesn't like periods in the window name, so convert temporarily.
    name = name.replace(/\./g, '___');
    var url = new URL(elem.href);
    url.searchParams.set(popupParamName, '1');
    var win = window.open(url.toString(), name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    return showPopupFromLink(triggeringLink, /^lookup_/, 'pop');
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = win.name.replace(/___/g, '.');
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
}

function showAddAnotherPopup(triggeringLink) {
    return showPopupFromLink(triggeringLink, /^add_/, '_popup');
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    var name = win.name.replace(/___/g, '.');
    var elem = document.getElementById(name);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elem.nodeName == 'INPUT') {
            elem.value = newId;
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}
