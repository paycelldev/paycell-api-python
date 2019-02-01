from ..utils import cardapihelper, restclient, constants

""" 
    Card related api calls are made here.
    Since there is no class variables these functions are implemented as static.
    Each function gets required parameters, passes them to 'apihelper' which returns the request dict,
    then makes the post request to paycell api, returns response dict
"""


def get_cards(msisdn, client_ip):
    request = cardapihelper.create_get_card_request(msisdn, client_ip)
    response = restclient.make_post_request(constants.URL_GET_CARDS, request, {'content-type': 'application/json'})
    return response.json()


def register_card(alias, msisdn, card_token, eula_id, is_default, threed_session_id, client_ip):
    request = cardapihelper.create_register_card_request(alias, msisdn, card_token, eula_id, is_default, threed_session_id, client_ip)
    response = restclient.make_post_request(constants.URL_REGISTER_CARD, request, {'content-type': 'application/json'})
    return response.json()


def delete_card(msisdn, card_id, client_ip):
    request = cardapihelper.create_delete_card_request(msisdn, card_id, client_ip)
    response = restclient.make_post_request(constants.URL_DELETE_CARD, request, {'content-type': 'application/json'})
    return response.json()

