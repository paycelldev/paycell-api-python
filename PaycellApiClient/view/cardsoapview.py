from django.shortcuts import render
from django.http import HttpResponse
from ..services.provisionsoapservice import ProvisionSoapClient
from ..utils import util, constants
from django.views.decorators.csrf import csrf_exempt
import json
from zeep.helpers import serialize_object
"""
    These views are implemented to use SOAP api's card operations
    active_tabs dict is used for frontend purposes 
"""


provision_soap_client = ProvisionSoapClient()


def get_cards(request):
    if request.method == 'POST':
        data = request.POST.dict()
        active_tabs = {
            "addCard": "",
            "getCards": "active show",
            "removeCard": ""
        }
        response = provision_soap_client.get_cards(data["msisdn"], util.get_client_ip(request))
        return render(request, 'card_soap_index.html', {"tabs": active_tabs, "getCardResponse": response, "msisdn": data["msisdn"]})


@csrf_exempt
def hash_data(request):
    if request.method == 'POST':
        data = request.POST.dict()
        secure_data = util.digest_list_sha1([constants.APPLICATION_PASSWORD.upper(), constants.APPLICATION_NAME.upper()])
        hash_value = util.digest_list_sha1([constants.APPLICATION_NAME.upper(), data["transactionId"], data["transactionDateTime"], constants.SECURE_CODE.upper(), secure_data.upper()])
        return HttpResponse(json.dumps({"hashValue": hash_value}), content_type='application/json')


def register_card(request):
    if request.method == 'POST':
        data = request.POST.dict()
        threed_session_id = None
        if "threeDSessionId" in data:
            threed_session_id = data["threeDSessionId"]
        response = provision_soap_client.register_card(data["alias"], data["msisdn"], data["cardToken"], data["eulaId"], data["isDefault"], threed_session_id, util.get_client_ip(request))
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')


def delete_card(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = provision_soap_client.delete_card(data["msisdn"], data["cardId"], util.get_client_ip(request))
        return HttpResponse(json.dumps(serialize_object(response)), content_type='application/json')
