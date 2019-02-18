from django.shortcuts import render
from django.http import HttpResponse
from ..services.provisionsoapservice import ProvisionSoapClient
from ..utils import util
from django.views.decorators.csrf import csrf_exempt
from zeep.helpers import serialize_object
import json

"""
    This is a duplicate of paymentapiview.py
    Only difference is this view uses paycell api's SOAP client
    active_tabs dict is used for frontend purposes
"""
provision_soap_client = ProvisionSoapClient()


def index(request):
    return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("provision")})


# This view handles gets information from frontend and makes the provision api call
# if the customer uses a stored card the cardId parameter has a value
# if the customer uses a custom card the cardToken parameter has a value
# if the transaction is 3d secure threeDSessionId value has value
# if the isMarketPlace checkbox is selected on the frontend it makes a call to marketplace provision api
def provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        card_id = data["cardId"] if "cardId" in data else None
        card_token = data["cardToken"] if "cardToken" in data else None
        threed_session_id = data["threeDSecureId"] if "threeDSecureId" in data else None

        if data["isMarketPlace"] == 'true':
            response, ref_no = provision_soap_client.make_provision_marketplace(card_id, card_token, data["msisdn"], data["amount"], data["installmentCount"],  data["currency"], data["paymentType"],threed_session_id, util.get_client_ip(request))
        else:
            response, ref_no = provision_soap_client.make_provision(card_id, card_token, data["msisdn"], data["amount"], data["installmentCount"], data["currency"], data["paymentType"], threed_session_id, util.get_client_ip(request))

        response["refNo"] = ref_no
        response["threeDSessionId"] = threed_session_id
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')


def get_cards_for_payment(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = provision_soap_client.get_cards(data["msisdn"], util.get_client_ip(request))
        return render(request, 'payment_soap_index.html', {"tabs":  util.select_active_provision_tab("provision"), "getCardResponse": response, "msisdn": data["msisdn"], "amount": data["amount"], "currency": data["currency"], "installmentCount": data["installmentCount"]})

def inquire_provision(request):
    if request.method == 'GET':
        msisdn = request.GET.get("msisdn", "")
        ref_no = request.GET.get("referenceNumber", "")
        response = provision_soap_client.inquire_provision(msisdn, ref_no, util.get_client_ip(request))
        return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("provisionDetails"), "inquireResponse": response, "referenceId": ref_no})


def reverse_provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = provision_soap_client.reverse_provision(data["msisdn"], data["referenceNumber"], util.get_client_ip(request))
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')


def refund_provision(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = provision_soap_client.refund_provision(data["msisdn"], data["referenceNumber"], data["amount"], util.get_client_ip(request))
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')


def get_threed_session_id(request):
    if request.method == 'POST':
        data = request.POST.dict()
        card_id = data["cardId"] if "cardId" in data and data["cardId"] != "" else None
        card_token = data["cardToken"] if "cardToken" in data else None

        threed_session_response = provision_soap_client.get_threed_session_id(data["msisdn"], data["amount"], card_id, card_token, util.get_client_ip(request))
        threed_session_id = threed_session_response["threeDSessionId"]
        return HttpResponse(json.dumps({"threeDSessionId": threed_session_id}), content_type='application/json')


def show_threed_page(request, threed_session_id):
    return render(request, 'threedsecure.html', {"threeDSessionId": threed_session_id, "callbackUrl": "www.google.com"})

@csrf_exempt
def get_threed_session_result(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = provision_soap_client.get_threed_session_result(data["msisdn"], data["threeDSessionId"], util.get_client_ip(request))
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')


def summary_reconcile(request):
    if request.method == 'POST':

        data = request.POST.dict()
        response = provision_soap_client.get_summary_reconcile(data["reconciliationDate"], data["totalRefundAmount"],
                                                           data["totalRefundCount"], data["totalReverseAmount"],
                                                           data["totalReverseCount"], data["totalSaleAmount"],
                                                           data["totalSaleCount"], util.get_client_ip(request))
        return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("reconciliation"), "reconcileRequest": data, "reconcileResponse": response})

def get_history(request):
    if request.method == 'POST':
        data = request.POST.dict()
        partition_number = 0

        if "isAllHistory" in data and data["isAllHistory"] == 'on':
            return get_all_history(request)

        if "nextPartitionNumber" in data:
            if data["nextPartitionNumber"] == 'None':
                return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": {"transactionList": [{"transactionId": "End of history"}]}, "reconcileDate": data["reconcileDate"]})
            elif data["nextPartitionNumber"] != "":
                partition_number = data["nextPartitionNumber"]

        response = provision_soap_client.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
        return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": response, "reconcileDate": data["reconcileDate"]})


def get_all_history(request):
    if request.method == 'POST':
        data = request.POST.dict()
        partition_number = 0
        transaction_list = []
        while True:
            response = provision_soap_client.get_history(data["reconcileDate"], partition_number, util.get_client_ip(request))
            partition_number = response["nextPartitionNo"]
            if response["transactionList"]:
                transaction_list.extend(response["transactionList"])

            if not partition_number:
                break
        return render(request, 'payment_soap_index.html', {"tabs": util.select_active_provision_tab("history"), "historyResponse": {"transactionList": transaction_list}, "reconcileDate": data["reconcileDate"]})


