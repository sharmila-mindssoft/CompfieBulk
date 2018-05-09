bulk_upload_max_length = {
  // Bulk upload 
  'reason': 500,
}

$.extend(max_length, bulk_upload_max_length);
function postValidate(isValid, errMsg, inputElm) {
    if (!isValid) {
        displayMessage(errMsg);
        if(errMsg.indexOf("From Date Required") < 0)
            inputElm.focus();
    }
}


/* Validate that input value length is between minLength and maxLength */
function isLengthMinMax(inputElm, minLength, maxLength, errMsg) {
    var inputValue = inputElm.val().trim();
    console.log(inputValue)
    if ((inputValue.length >= minLength) && (inputValue.length <= maxLength)) {
      isValid = true;
    }
    else {
      isValid = false
    }

    postValidate(isValid, errMsg, inputElm);
    return isValid;
}
