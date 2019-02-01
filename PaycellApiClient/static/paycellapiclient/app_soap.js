/*
    This is a copy app.js with only different endpoints which are implemented as SOAP client
*/

var leadingZeros = function(text, digits){
	var result = String(text);
	while(result.length < digits){
		result = "0"+result;
	}
	return result;
}

var generateTransactionDateTime = function() {
	var date = new Date();
	var year = String(date.getFullYear());
	var month = leadingZeros(date.getMonth()+1, 2);
	var day = leadingZeros(date.getDate(), 2);
	var hours = leadingZeros(date.getHours(), 2);
	var minutes = leadingZeros(date.getMinutes(), 2);
	var seconds = leadingZeros(date.getSeconds(), 2);
	var milliseconds = leadingZeros(date.getMilliseconds(), 3);
	return year+month+day+hours+minutes+seconds+milliseconds;
}

var registerCard = function(token) {
    var isThreeDSecure = $('#addCardIsThreed').is(':checked');
    var alias = $("#addCardAlias").val();
    var eulaId = $("#addCardEula").val();
    var isDefault = $('#addCardIsDefault').is(':checked');
    var msisdn = $("#addCardMsisdn").val();

    if (isThreeDSecure) {
        getThreeDSessionIdForAddCard(msisdn, token, alias, isDefault, eulaId);
    } else {
        makeRegisterCardCall(alias, token, eulaId, isDefault, msisdn, null);
    }

}

var makeRegisterCardCall = function(alias, cardToken, eulaId, isDefault, msisdn, threeDSessionId) {
    request = $.ajax({
        url: "/paycellapiclient/soap/registercard/",
        type: "POST",
        dataType: 'json',
        data: {
           "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
           "alias": alias,
           "cardToken": cardToken,
           "eulaId": eulaId,
           "isDefault": isDefault,
           "msisdn": msisdn,
           "threeDSecureId" : threeDSessionId,
        },
        success: function(input) {
           alert("Card Register result: \n\n\n" + input.responseHeader.responseDescription);
        },
    });
}

/*
    This method makes a call to get three d session
    After getting the id and opens a new tab for three d session
    Since this application works on local, after the session is started callback url is not called
    Because of this reason, this method checks for 3d session result every 5 seconds,
    this may lead to call add card service several times, when the callback url is called this will not be a problem
*/
var getThreeDSessionIdForAddCard = function(msisdn, cardToken, alias, isDefault, eulaId){
    var count = 0;

    request = $.ajax({
        url: "/paycellapiclient/soap/threedsessionid/",
        type: "POST",
        dataType: 'json',
        data: {
                "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                "msisdn": msisdn,
                "amount": 1,
                "cardToken": cardToken
              },
        success: function(input) {
            var threedPage = "/paycellapiclient/showthreedpage/" + input.threeDSessionId;
            window.open(threedPage);

            //Check every second for 30 seconds.
            var timer = setInterval(function() {
                //Check for the session result
                checkThreeDSessionResultForAddCard(msisdn, input.threeDSessionId, cardToken, alias, isDefault, eulaId, timer);
            }, 5000);
        }
    });
}
/*
    This method is checks for the result of 3d session and when the result is successful
    calls the addcard service to complete the add card process
*/
var checkThreeDSessionResultForAddCard = function(msisdn, threeDSessionId, cardToken, alias, isDefault, eulaId, timer){
    request = $.ajax({
        url: "/paycellapiclient/soap/threedsessionresult/",
        type: "POST",
        dataType: 'json',
        data: {
                "msisdn": msisdn,
                "threeDSessionId": threeDSessionId
              },
        success: function(input) {
            console.log(input);
            if (input.threeDOperationResult && input.threeDOperationResult.threeDResult == '0') {
                makeRegisterCardCall(alias, cardToken, eulaId, isDefault, msisdn, threeDSessionId);
                clearInterval(timer);

            }
        }
    });
}


var getToken = function(transactionId, transactionDateTime, hashData) {
    var body = {
          "header":{
            "applicationName":"PAYCELLTEST",
            "transactionDateTime": transactionDateTime,
            "transactionId": transactionId
          },
          "creditCardNo": $("#addCardNo").val(),
          "expireDateMonth": $("#addCardExpireMonth").val(),
          "expireDateYear": $("#addCardExpireYear").val(),
          "cvcNo": $("#addCardCvc").val(),
          "hashData": hashData
    };

    request = $.ajax({
        url: "https://omccstb.turkcell.com.tr/paymentmanagement/rest/getCardTokenSecure",
        type: "POST",
        dataType: 'json',
        data: JSON.stringify(body),
        success: function(input) {
            if (!input.cardToken || 0 === input.cardToken.length) {
                alert("Card token cannot be created");
            } else {
                registerCard(input.cardToken);
            }
        },
    });
}

function addCard() {
    var transactionId = Math.floor((Math.random() * 99999999999999999999) + 10000000000000000000);
    var transactionDateTime = generateTransactionDateTime();

    request = $.ajax({
        url: "/paycellapiclient/soap/hashdata/",
        type: "POST",
        dataType: 'json',
        data: {  "transactionDateTime": transactionDateTime,
                 "transactionId": transactionId
              },
        success: function(input) {
            getToken(transactionId, transactionDateTime, input.hashValue);
        },
    });
}


function removeCard(el) {
    var cardId = $(el).parents("div.row").children().find("p#cardId").text();
    var msisdn = $("#getCardMsisdn").val();

    request = $.ajax({
        url: "/paycellapiclient/soap/deletecard/",
        type: "POST",
        dataType: 'json',
        data: {
                "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                "msisdn": msisdn,
                "cardId": cardId
              },
        success: function(input) {
            console.log(input);
            alert("Remove card result: \n\n\n" + input.responseDescription);
        },
    });
}

function payWithStoredCard(el) {
    var transactionId = Math.floor((Math.random() * 99999999999999999999) + 10000000000000000000);
    var transactionDateTime = generateTransactionDateTime();
    var cardId = $(el).parents("div.row").children().find("p#cardId").text();
    var expireMonth = $(el).parents("div.row").children().find("#storedCardExpireMonth").val();
    var expireYear =$(el).parents("div.row").children().find("#storedCardExpireYear").val();
    var cvc =$(el).parents("div.row").children().find("#storedCardCvc").val();

    //if there is extra fields
    if (expireYear || expireMonth || cvc) {
            request = $.ajax({
            url: "/paycellapiclient/soap/hashdata/",
            type: "POST",
            dataType: 'json',
            data: {  "transactionDateTime": transactionDateTime,
                     "transactionId": transactionId
                  },
            success: function(input) {
                getCardTokenForProvision(transactionId, transactionDateTime, null, cardId, expireMonth, expireYear, cvc, input.hashValue, makeProvisionCall);
            },
        });
    //pay with stored card
    } else {
        makeProvisionCall(null, cardId);
    }
}


var checkThreeDSessionResult = function(msisdn, threeDSessionId, amount, cardId, cardToken, timer){
    request = $.ajax({
        url: "/paycellapiclient/soap/threedsessionresult/",
        type: "POST",
        dataType: 'json',
        data: {
                "msisdn": msisdn,
                "threeDSessionId": threeDSessionId
              },
        success: function(input) {
            console.log(input);
            if (input.threeDOperationResult && input.threeDOperationResult.threeDResult == '0') {
                makeProvisionServiceCall(cardToken, cardId, msisdn, threeDSessionId);
                clearInterval(timer);
            }
        }
    });
}

var getThreeDSessionId = function(msisdn, amount, cardId, cardToken){
    var count = 0;

    request = $.ajax({
        url: "/paycellapiclient/soap/threedsessionid/",
        type: "POST",
        dataType: 'json',
        data: {
                "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                "msisdn": msisdn,
                "amount": amount,
                "cardId": cardId,
                "cardToken": cardToken
              },
        success: function(input) {
            var threedPage = "/paycellapiclient/showthreedpage/" + input.threeDSessionId;
            window.open(threedPage);

            //Check every second for 30 seconds.
            var timer = setInterval(function() {
                checkThreeDSessionResult(msisdn, input.threeDSessionId, amount, cardId, cardToken, timer);
            }, 5000);
        }
    });
}



var makeProvisionCall = function(token, cardId, threeDSessionId) {
    var msisdn = $("#getCardsMsisdn").val();
    var isThreeDSecure = $("#isThreeDSecure").is(':checked');
    var isMarketPlace = $("#isMarketPlace").is(':checked');

    if (isThreeDSecure) {
        getThreeDSessionId(msisdn, $("#amount").val(), cardId, token);
    } else {
        makeProvisionServiceCall(token, cardId, msisdn, isMarketPlace, threeDSessionId);
    }
}

var makeProvisionServiceCall = function(token,cardId, msisdn, isMarketPlace, threeDSessionId) {
        request = $.ajax({
            url: "/paycellapiclient/soap/provision/",
            type: "POST",
            dataType: 'json',
            data: {
                    "cardToken": token,
                    "cardId": cardId,
                    "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                    "currency": $("#currency").val(),
                    "msisdn":  msisdn,
                    "threeDSecureId" : threeDSessionId,
                    "isMarketPlace" : isMarketPlace,
                    "amount": $("#amount").val(),
                    "paymentType" : $("#paymentType").val()
                  },
            success: function(input) {
                alert("Provision result: \n\n\n" + input.responseHeader.responseDescription + "\n\n" + JSON.stringify(input));
                var statusPage= "/paycellapiclient/soap/inquireprovision/?msisdn=" + msisdn + "&referenceNumber=" + input.refNo;
                window.location = statusPage
            },
        });
}

function payWithCustomCard() {

    var transactionId = Math.floor((Math.random() * 99999999999999999999) + 10000000000000000000);
    var transactionDateTime = generateTransactionDateTime();

    request = $.ajax({
        url: "/paycellapiclient/soap/hashdata/",
        type: "POST",
        dataType: 'json',
        data: {  "transactionDateTime": transactionDateTime,
                 "transactionId": transactionId
              },
        success: function(input) {
            var cardNo = $("#customCardNo").val();
            var expMonth = $("#customCardExpireMonth").val();
            var expYear =  $("#customCardExpireYear").val();
            var cvc =  $("#customCardCvc").val();
            getCardTokenForProvision(transactionId, transactionDateTime, cardNo, null, expMonth, expYear, cvc, input.hashValue, makeProvisionCall);
        },
    });
}

function getCardTokenForProvision(transactionId, transactionDateTime,cardNo, cardId, expMonth, expYear, cvc, hashValue, callback) {
    var body = {
          "header":{
            "applicationName":"PAYCELLTEST",
            "transactionDateTime": transactionDateTime,
            "transactionId": transactionId
          },
          "creditCardNo": cardNo,
          "expireDateMonth": expMonth,
          "expireDateYear": expYear,
          "cvcNo": cvc,
          "hashData": hashValue
    };

    request = $.ajax({
        url: "https://omccstb.turkcell.com.tr/paymentmanagement/rest/getCardTokenSecure",
        type: "POST",
        dataType: 'json',
        data: JSON.stringify(body),
        success: function(input) {
            if (!input.cardToken || 0 === input.cardToken.length) {
                alert("Card token cannot be created \n\n" + JSON.stringify(input));
            } else {
                callback(input.cardToken, cardId)
                //alert("Get Card Token result: \n\n\n" + JSON.stringify(input));
            }
        },
    });
}


function reverseProvision(el) {
    const urlParams = new URLSearchParams(window.location.search);
    const msisdn = urlParams.get('msisdn');
    const referenceNumber = urlParams.get('referenceNumber');

    request = $.ajax({
        url: "/paycellapiclient/soap/reverseprovision/",
        type: "POST",
        dataType: 'json',
        data: {
                "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                "msisdn": msisdn,
                "referenceNumber" : referenceNumber
              },
        success: function(input) {
            alert("Reverse Payment result: \n\n\n" + input.responseHeader.responseDescription + "\n\n" + JSON.stringify(input));
            location.reload(true);
        },
    });

}

function refundProvision(el) {
    const urlParams = new URLSearchParams(window.location.search);
    const msisdn = urlParams.get('msisdn');
    const referenceNumber = urlParams.get('referenceNumber');

    request = $.ajax({
        url: "/paycellapiclient/soap/refundprovision/",
        type: "POST",
        dataType: 'json',
        data: {
                "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val(),
                "msisdn": msisdn,
                "referenceNumber" : referenceNumber,
                "amount" :  $("#refundAmount").val()
              },
        success: function(input) {
            alert("Refund Payment result: \n\n\n" + input.responseHeader.responseDescription + "\n\n" + JSON.stringify(input));
            location.reload(true);
        },
    });


}