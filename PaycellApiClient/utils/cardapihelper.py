from .constants import APPLICATION_NAME, APPLICATION_PASSWORD, MERCHANT_CODE
from datetime import datetime
import random
"""
    These are static util function which are implemented to create request dicts for each api service with given parameters 
    These functions are related to api's card operation

"""


def create_request_header(client_ip):
    return {
        "applicationName": APPLICATION_NAME,
        "applicationPwd": APPLICATION_PASSWORD,
        "clientIPAddress": client_ip,
        "transactionDateTime": datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3],
        "transactionId": random.randrange(1000000000000000000, 99999999999999999999),
    }


def create_get_card_request(msisdn, client_ip):
    return {
        "requestHeader": create_request_header(client_ip),
        "msisdn": msisdn
    }


def create_register_card_request(alias, msisdn,card_token, eula_id, is_default, threed_session_id, client_ip):
    return {
        "requestHeader": create_request_header(client_ip),
        "alias": alias,
        "cardToken": card_token,
        "eulaId": eula_id,
        "isDefault": is_default,
        "msisdn": msisdn,
        "threeDSessionId": threed_session_id
    }


def create_delete_card_request(msisdn, card_id, client_ip):
    return {
        "requestHeader": create_request_header(client_ip),
        "cardId": card_id,
        "msisdn": msisdn,
    }


def create_update_card_request(msisdn, card_id, alias, is_default, eula_id, threed_session_id, client_ip):
    default = None if is_default == 'false' or not is_default else is_default
    return {
        "requestHeader": create_request_header(client_ip),
        "alias": alias,
        "cardId": card_id,
        "eulaId": eula_id,
        "isDefault": default,
        "msisdn": msisdn,
        "threeDSessionId": threed_session_id
    }