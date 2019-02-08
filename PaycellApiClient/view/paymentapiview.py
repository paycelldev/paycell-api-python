from django.shortcuts import render
from django.http import HttpResponse
from ..services import paymentapiservice, cardapiservice
from ..utils import util
from django.views.decorators.csrf import csrf_exempt
import json

"""
    These views are implemented to use rest api's payment operations
    active_tabs dict is used for frontend purposes 
    Important: prevent cross-site scripting all responses must be validated !!
"""

def index(request):
    return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("provision")})


def provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        card_id = data["cardId"] if "cardId" in data else None
        card_token = data["cardToken"] if "cardToken" in data else None
        threed_session_id = data["threeDSecureId"] if "threeDSecureId" in data else None

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
        response = cardapiservice.get_cards(data["msisdn"], util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("provision"), "getCardResponse": response, "msisdn": data["msisdn"], "amount": data["amount"], "currency": data["currency"]})


#   Waits for msisdn and referenceNumber as url parameters
def inquire_provision(request):
    if request.method == 'GET':
        msisdn = request.GET.get("msisdn", "")
        ref_no = request.GET.get("referenceNumber", "")
        response = paymentapiservice.inquire_provision(msisdn, ref_no, util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("provisionDetails"), "inquireResponse": response})


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
        print("threed_session data: ", data)
        card_id = data["cardId"] if "cardId" in data and data["cardId"] != "" else None
        card_token = data["cardToken"] if "cardToken" in data else None

        threed_session_response = paymentapiservice.get_threed_session_id(data["msisdn"], data["amount"], card_id, card_token, util.get_client_ip(request))
        print("threed_session_response: ", threed_session_response)
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
        data = request.POST.dict()
        response = paymentapiservice.get_summary_reconcile(data["reconciliationDate"], data["totalRefundAmount"],
                                                           data["totalRefundCount"], data["totalReverseAmount"],
                                                           data["totalReverseCount"], data["totalSaleAmount"],
                                                           data["totalSaleCount"], util.get_client_ip(request))

        return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("reconciliation"), "reconcileRequest": data, "reconcileResponse": response})


#
#   History service returns transaction as parts
#   if isAllHistory checkbox is selected, calls the view below
#
def get_history(request):
    if request.method == 'POST':
        data = request.POST.dict()
        partition_number = 0

        if "isAllHistory" in data and data["isAllHistory"] == 'on':
            return get_all_history(request)

        if "nextPartitionNumber" in data:
            if data["nextPartitionNumber"] == 'None':
                return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": {"transactionList": [{"transactionId": "End of history"}]}, "reconcileDate": data["reconcileDate"]})
            elif data["nextPartitionNumber"] != "":
                partition_number = data["nextPartitionNumber"]

        response = paymentapiservice.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
        return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": response, "reconcileDate": data["reconcileDate"]})


# it calls history service until there is no nextPartitionNumber in response
def get_all_history(request):
    if request.method == 'POST':
        data = request.POST.dict()
        partition_number = 0
        transaction_list = []
        while True:
            response = paymentapiservice.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
            partition_number = response["nextPartitionNo"]
            if response["transactionList"]:
                transaction_list.extend(response["transactionList"])

            if not partition_number:
                break
        return render(request, 'payment_api_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": {"transactionList": transaction_list}, "reconcileDate": data["reconcileDate"]})


@csrf_exempt
def get_terms_of_service(request):
    response = paymentapiservice.get_terms_of_service(util.get_client_ip(request))
    return HttpResponse(response["termsOfServiceHtmlContentTR"], content_type='text/html; charset=utf-8')
