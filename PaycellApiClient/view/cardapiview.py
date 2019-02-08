from django.shortcuts import render
from django.http import HttpResponse
from ..services import cardapiservice
from ..utils import util, constants
from django.views.decorators.csrf import csrf_exempt
import json

"""
    These views are implemented to use rest api's card operations
    active_tabs dict is used for frontend purposes 
    Important: prevent cross-site scripting all responses must be validated !!
"""

def get_cards(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = cardapiservice.get_cards(data["msisdn"], util.get_client_ip(request))
        return render(request, 'card_api_index.html', {"tabs": util.select_active_card_tab("getCards"), "getCardResponse": response, "msisdn": data["msisdn"]})

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
        threed_session_id = data["threeDSecureId"] if "threeDSecureId" in data else None
        print(data, "\n", threed_session_id)
        response = cardapiservice.register_card(data["alias"], data["msisdn"], data["cardToken"], data["eulaId"], data["isDefault"], threed_session_id, util.get_client_ip(request))
        return HttpResponse(json.dumps(response), content_type='application/json')


def delete_card(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = cardapiservice.delete_card(data["msisdn"], data["cardId"], util.get_client_ip(request))
        return HttpResponse(json.dumps(response), content_type='application/json')
