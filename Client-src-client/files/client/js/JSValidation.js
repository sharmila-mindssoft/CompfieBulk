function postValidate(isValid, errMsg, inputElm) {
    if (!isValid) {
        displayMessage(errMsg);
        if(errMsg.indexOf("From Date Required") < 0)
            inputElm.focus();
    } else {
        hideMessage();
    }
}


/* Validate that input value is not empty. */
function isNotEmpty(inputElm, errMsg) {
    var isValid = (inputElm.val().trim() !== "");
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value contains one or more digits */
function isNumeric(inputElm, errMsg) {
    var isValid = true;
    if (inputElm.val() != "")
        isValid = (inputElm.val().trim().match(/^\d+$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value contains one or more digits and one dot*/
function isNumbersDot(inputElm, errMsg) {
    var isValid = true;
    if (inputElm.val() != "")
        isValid = (inputElm.val().trim().match(/^[0-9]*\.?[0-9]*$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value contains only one or more letters */
function isAlphabetic(inputElm, errMsg) {
    var isValid = (inputElm.val().trim().match(/^[a-zA-Z]+$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value contains one or more digits or letters */
function isAlphanumeric(inputElm, errMsg) {
    var isValid = (inputElm.val().trim().match(/^[0-9a-zA-Z]+$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value length is between minLength and maxLength */
function isLengthMinMax(inputElm, minLength, maxLength, errMsg) {
    var inputValue = inputElm.val().trim();
    var isValid = (inputValue.length >= minLength) && (inputValue.length <= maxLength);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/* Validate that input value length is between min and max */
function isMinMax(inputElm, min, max, errMsg) {
    var inputValue = parseFloat(inputElm.val().trim());
    var isValid = (inputValue >= parseFloat(min)) && (inputValue <= parseFloat(max));
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}


// Validate that input value is a valid email address
function isValidEmail(inputElm, errMsg) {
    var isValid = true;
    if (inputElm.val() != "")
        var isValid = (inputElm.val().trim().match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

/*
 * Validate that a selection is made (not default of "") in <select> input
 *
 * @param selectElm (object): the <select> element
 */
function isSelected(selectElm, errMsg) {
    // You need to set the default value of <select>'s <option> to "".
    var isValid = (selectElm.val() !== ""); // value in selected <option>
    postValidate(isValid, errMsg, selectElm);
    return isValid;
}

/*
 * Validate that one of the checkboxes or radio buttons is checked.
 * Checkbox and radio are based on name attribute, not id.
 *
 * @param inputName (string): name attribute of the checkbox or radio
 */
function isChecked(inputName, errMsg) {
    var isChecked = false;
    for (var i = 0; i < inputName.length; ++i) {
        if (inputName[i].checked) {
            isChecked = true;
            break;
        }
    }
    postValidate(isChecked, errMsg, inputName);
    return isChecked;
}

function isMultiselect(inputName, errMsg) {
    var isChecked = false;
    if ($(inputName).find("input[type=checkbox]")) {

        var checkboxlist = $(inputName).find("input[type=checkbox]");
        for (var i = 0; i < checkboxlist.length; ++i) {
            if (checkboxlist[i].checked) {
                isChecked = true;
                break;
            }
        }
    }

    inputName = $(inputName).find('.multiselect'); // checkboxlist
    postValidate(isChecked, errMsg, inputName);
    return isChecked;
}

// Validate password, 4-8 characters of [a-zA-Z0-9_]
function isValidPassword(inputElm, errMsg) {
    var isValid = (inputElm.val().trim().match(/^\w{4,20}$/) !== null);
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

// Verify password.
function verifyPassword(pwElm, pwVerifiedElm, errMsg) {
    var isTheSame = (pwElm.val() === pwVerifiedElm.val());
    postValidate(isTheSame, errMsg, pwVerifiedElm);
    return isTheSame;
}

/*
 * The "onclick" handler for the "reset" button to clear the display,
 * including the previous error messages and error box.
 */
function clearForm() {
    $('.errorBox').each(function(index) {
        $(this).removeClass('.errorBox');
    });
}

// Validate that input value is a valid alphanumeric, dot, comma, Hyphen
function isCommonName(inputElm, errMsg) {
    var isValid = (inputElm.val().trim().match(/^[ A-Za-z0-9_.,-]*$/) !== null); //allowed => alphanumeric, dot, comma, Hyphen
    postValidate(isValid, errMsg, inputElm);
    return isValid;
}

//Validate that end value is greater than start value
function isGreaterThen(startInputElm, endInputElm, errMsg) {
    var isValid = true;
    if (startInputElm.val() != "" && endInputElm.val())
        isValid = (parseInt(startInputElm.val()) < parseInt(endInputElm.val()));
    postValidate(isValid, errMsg, endInputElm);
    return isValid;
}

//Validate that end value is greater than or equeal start value
function isGreaterThenOrEqual(startInputElm, endInputElm, errMsg) {
    var isValid = true;
    if (startInputElm.val() != "" && endInputElm.val())
        isValid = (parseInt(startInputElm.val()) <= parseInt(endInputElm.val()));
    postValidate(isValid, errMsg, endInputElm);
    return isValid;
}

//Validate that if parant value not emplty
function isParantBasedNotEmpty(parantInputElm, childInputElm, errMsg) {
    var isValid = true;
    if (parantInputElm.val().trim() != "")
        isValid = (childInputElm.val().trim() !== "");
    postValidate(isValid, errMsg, childInputElm);
    return isValid;
}

//Validate that revised value biggest
function isRevisedBiggest(firstInputElm, secondInputElm, errMsg) {
    var isValid = true;
    if (firstInputElm.val().trim() != "" && secondInputElm.val().trim() != "")
        isValid = (parseInt(firstInputElm.val()) <= parseInt(secondInputElm.val()));
    postValidate(isValid, errMsg, secondInputElm);
    return isValid;
}
/* Validate that input value is not empty. */
function isNotEmptyNew(inputElm, errMsg, errElm) {
    var isValid = (inputElm.val().trim() !== "");
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

function isLengthMinMaxNew(inputElm, minLength, maxLength, errMsg, errElm) {
    var inputValue = inputElm.val().trim();
    var isValid = (inputValue.length >= minLength) && (inputValue.length <= maxLength);
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

function isMinMaxNew(inputElm, min, max, errMsg, errElm) {
    var inputValue = parseFloat(inputElm.val().trim());
    var isValid = (inputValue >= parseFloat(min)) && (inputValue <= parseFloat(max));
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

function isImageNew(inputElm, errMsg, exts, errElm) {
    var isValid = new RegExp('(' + exts.join('|').replace(/\./g, '\\.') + ')$').test(inputElm.val());
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

function isDocumentAndImageNew(inputElm, errMsg, exts, errElm) {
    var isValid = new RegExp('(' + exts.join('|').replace(/\./g, '\\.') + ')$').test(inputElm.val());
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

/* Validate that input value contains one or more digits and one dot*/
function isNumbersDotNew(inputElm, errMsg, errElm) {
    var isValid = true;
    if (inputElm.val() != "")
        isValid = (inputElm.val().trim().match(/^[0-9]*\.?[0-9]*$/) !== null);
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(inputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}

//Validate that end value is greater than start value
function isGreaterThenNew(startInputElm, endInputElm, errMsg, errElm) {
    var isValid = true;
    if (startInputElm.val() != "" && endInputElm.val())
        isValid = (parseInt(startInputElm.val()) < parseInt(endInputElm.val()));
    if (isValid == false) {
        $(errElm).html(errMsg);
        $(endInputElm).focus();
    } else { $(errElm).html(""); }
    return isValid;
}