from django.shortcuts import render
from django.http import HttpResponse
from ..services import paymentapiservice, cardapiservice
from ..utils import util
from django.views.decorators.csrf import csrf_exempt
import json

"""
    These views are implemented to use rest api's payment operations
    active_tabs dict is used for frontend purposes 
"""

def index(request):
    active_tabs = {
        "provision": "active show",
        "provisionDetails": "",
        "reconciliation": "",
        "history": ""
    }
    return render(request, 'payment_api_index.html', {"tabs": active_tabs})


def provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        threed_session_id = None
        card_token = None
        card_id = None

        if "cardId" in data:
            card_id = data["cardId"]
        if "cardToken" in data:
            card_token = data["cardToken"]
        if "threeDSessionId" in data:
            threed_session_id = data["threeDSessionId"]

        if data["isMarketPlace"] == 'true':
            response, ref_no = paymentapiservice.make_provision_marketplace(card_id, card_token, data["msisdn"], data["amount"], data["currency"], data["paymentType"],threed_session_id, util.get_client_ip(request))
        else:
            response, ref_no = paymentapiservice.make_provision(card_id, card_token, data["msisdn"], data["amount"], data["currency"], data["paymentType"], threed_session_id, util.get_client_ip(request))

        response["refNo"] = ref_no
        response["threeDSessionId"] = threed_session_id
        return HttpResponse(json.dumps(response), content_type='application/json')


def get_cards_for_payment(request):
    if request.method == 'POST':
        data = request.POST.dict()
        active_tabs = {
            "provision": "active show",
            "provisionDetails": "",
            "reconciliation": "",
            "history": ""
        }
        response = cardapiservice.get_cards(data["msisdn"], util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": active_tabs, "getCardResponse": response, "msisdn": data["msisdn"], "amount": data["amount"], "currency": data["currency"]})


#   Waits for msisdn and referenceNumber as url parameters
def inquire_provision(request):
    if request.method == 'GET':
        msisdn = request.GET.get("msisdn", "")
        ref_no = request.GET.get("referenceNumber", "")
        active_tabs = {
            "provision": "",
            "provisionDetails": "active show",
            "reconciliation": "",
            "history": ""
        }
        response = paymentapiservice.inquire_provision(msisdn, ref_no, util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": active_tabs, "inquireResponse": response})


def reverse_provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = paymentapiservice.reverse_provision(data["msisdn"], data["referenceNumber"], util.get_client_ip(request))
        return HttpResponse(json.dumps(response), content_type='application/json')


def refund_provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = paymentapiservice.refund_provision(data["msisdn"], data["referenceNumber"], data["amount"], util.get_client_ip(request))
        return HttpResponse(json.dumps(response), content_type='application/json')


def get_threed_session_id(request):
    if request.method == 'POST':
        data = request.POST.dict()
        card_token = None
        card_id = None

        if "cardId" in data and data["cardId"] != "":
            card_id = data["cardId"]
        elif "cardToken" in data:
            card_token = data["cardToken"]

        threed_session_response = paymentapiservice.get_threed_session_id(data["msisdn"], data["amount"], card_id, card_token, util.get_client_ip(request))
        threed_session_id = threed_session_response["threeDSessionId"]
        return HttpResponse(json.dumps({"threeDSessionId": threed_session_id}), content_type='application/json')


def show_threed_page(request, threed_session_id):
    return render(request, 'threedsecure.html', {"threeDSessionId": threed_session_id, "callbackUrl": "www.google.com"})

@csrf_exempt
def get_threed_session_result(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = paymentapiservice.get_threed_session_result(data["msisdn"], data["threeDSessionId"], util.get_client_ip(request))
        return HttpResponse(json.dumps(response), content_type='application/json')


def summary_reconcile(request):
    if request.method == 'POST':
        active_tabs = {
            "provision": "",
            "provisionDetails": "",
            "reconciliation": "active show",
            "history": ""
        }
        data = request.POST.dict()
        response = paymentapiservice.get_summary_reconcile(data["reconciliationDate"], data["totalRefundAmount"],
                                                           data["totalRefundCount"], data["totalReverseAmount"],
                                                           data["totalReverseCount"], data["totalSaleAmount"],
                                                           data["totalSaleCount"], util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": active_tabs, "reconcileRequest": data, "reconcileResponse": response})


#
#   History service returns transaction as parts
#   if isAllHistory checkbox is selected, calls the view below
#
def get_history(request):
    if request.method == 'POST':
        active_tabs = {
            "provision": "",
            "provisionDetails": "",
            "reconciliation": "",
            "history": "active show"

        }
        data = request.POST.dict()
        partition_number = 0

        if "isAllHistory" in data and data["isAllHistory"] == 'on':
            return get_all_history(request)

        if "nextPartitionNumber" in data:
            if data["nextPartitionNumber"] == 'None':
                return render(request, 'payment_api_index.html', {"tabs": active_tabs, "historyResponse": {"transactionList": [{"transactionId": "End of history"}]}, "reconcileDate": data["reconcileDate"]})
            elif data["nextPartitionNumber"] != "":
                partition_number = data["nextPartitionNumber"]

        response = paymentapiservice.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": active_tabs, "historyResponse": response, "reconcileDate": data["reconcileDate"]})


# it calls history service until there is no nextPartitionNumber in response
def get_all_history(request):
    if request.method == 'POST':
        active_tabs = {
            "provision": "",
            "provisionDetails": "",
            "reconciliation": "",
            "history": "active show"

        }
        data = request.POST.dict()
        partition_number = 0
        transaction_list = []
        response = paymentapiservice.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
        while partition_number != "" and partition_number is not None:
            partition_number = response["nextPartitionNo"]
            if response["transactionList"] is not None:
                transaction_list.extend(response["transactionList"])
            response = paymentapiservice.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": active_tabs, "historyResponse": {"transactionList": transaction_list}, "reconcileDate": data["reconcileDate"]})


