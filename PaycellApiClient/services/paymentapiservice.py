from ..utils import paymentapihelper, restclient, constants
""" 
    Payment related api calls are made here.
    Since there is no class variables these functions are implemented as static.
    Each function gets required parameters, passes them to 'apihelper' which returns the request dict,
    then makes the post request to paycell api, returns response dict
"""


def make_provision(card_id, card_token, msisdn, amount, currency,  payment_type, threed_session_id, client_ip):
    request = paymentapihelper.create_provision_request(card_id, card_token, msisdn, amount, currency, payment_type, threed_session_id, client_ip)
    response = restclient.make_post_request(constants.URL_PROVISION, request,  {'content-type': 'application/json'})
    return response.json(), request["referenceNumber"]


def make_provision_marketplace(card_id, card_token, msisdn, amount, currency,  payment_type, threed_session_id, client_ip):
    request = paymentapihelper.create_provision_request(card_id, card_token, msisdn, amount, currency, payment_type, threed_session_id, client_ip)
    response = restclient.make_post_request(constants.URL_PROVISION_FOR_MARKET_PLACE, request,  {'content-type': 'application/json'})
    return response.json(), request["referenceNumber"]


def inquire_provision(msisdn, reference_number, client_io):
    request = paymentapihelper.create_inquire_provision_request(msisdn, reference_number, client_io)
    response = restclient.make_post_request(constants.URL_INQUIRE, request,  {'content-type': 'application/json'})
    return response.json()


def reverse_provision(msisdn, reference_number, client_ip):
    request = paymentapihelper.create_reverse_provision_request(msisdn, reference_number, client_ip)
    response = restclient.make_post_request(constants.URL_REVERSE, request,  {'content-type': 'application/json'})
    return response.json()


def refund_provision(msisdn, reference_number, amount, client_ip):
    request = paymentapihelper.create_refund_provision_request(msisdn, reference_number, amount, client_ip)
    response = restclient.make_post_request(constants.URL_REFUND, request,  {'content-type': 'application/json'})
    return response.json()


def get_threed_session_id(msisdn, amount, card_id, card_token, client_ip):
    request = paymentapihelper.create_threed_session_request(msisdn, amount, card_id, card_token, client_ip)
    response = restclient.make_post_request(constants.URL_GET_THREED_SESSION, request,  {'content-type': 'application/json'})
    return response.json()


def start_threed_session(session_id):
    request = paymentapihelper.create_start_threed_session_request(session_id)
    response = restclient.make_post_request(constants.URL_THREED_SECURE, request, {'content-type': 'application/json'})
    return response


def get_threed_session_result(msisdn, session_id, client_ip):
    request = paymentapihelper.create_threed_session_result_request(msisdn, session_id, client_ip)
    response = restclient.make_post_request(constants.URL_GET_THREED_SESSION_RESULT, request, {'content-type': 'application/json'})
    return response.json()


def get_summary_reconcile(reconciliation_date, total_refund_amount, total_refund_count, total_reverse_amount, total_reverse_count, total_sale_amount, total_sale_count, client_ip):
    request = paymentapihelper.create_summary_reconcile_request(reconciliation_date, total_refund_amount, total_refund_count, total_reverse_amount, total_reverse_count, total_sale_amount, total_sale_count, client_ip)
    response = restclient.make_post_request(constants.URL_SUMMARY_RECONCILIATION, request, {'content-type': 'application/json'})
    return response.json()


def get_history(reconciliation_date, partition_no, client_ip):
    request = paymentapihelper.create_get_history_request(reconciliation_date, partition_no, client_ip)
    response = restclient.make_post_request(constants.URL_GET_PROVISION_HISTORY, request, {'content-type': 'application/json'})
    return response.json()