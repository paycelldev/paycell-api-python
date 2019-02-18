from .constants import APPLICATION_NAME, APPLICATION_PASSWORD, MERCHANT_CODE, REFENCE_NUMBER_PREFIX
from datetime import datetime
import random
"""
    These are static util function which are implemented to create request dicts for each api service with given parameters 
    These functions are related to api's payment operation

"""

def create_request_header(client_ip):
    return {
        "applicationName": APPLICATION_NAME,
        "applicationPwd": APPLICATION_PASSWORD,
        "clientIPAddress": client_ip,
        "transactionDateTime": datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3],
        "transactionId": random.randrange(1000000000000000000, 99999999999999999999),
    }


def create_provision_request(card_id, card_token, msisdn, amount, installment_count, currency, payment_type, threed_session_id,  client_ip):
    header = create_request_header(client_ip)
    return {
        "requestHeader": header,
        "cardId": card_id,
        "cardToken": card_token,
        "merchantCode": MERCHANT_CODE,
        "msisdn": msisdn,
        "referenceNumber": REFENCE_NUMBER_PREFIX + header["transactionDateTime"],
        "amount": amount,
        "installmentCount" : installment_count,
        "currency": currency,
        "paymentType": payment_type,
        "acquirerBankCode": "111",
        "threeDSessionId":  threed_session_id
    }


def create_inquire_provision_request(msisdn, reference_number, client_ip):
    header = create_request_header(client_ip)
    return {
        "requestHeader": header,
        "merchantCode": MERCHANT_CODE,
        "msisdn": msisdn,
        "referenceNumber": REFENCE_NUMBER_PREFIX + header["transactionDateTime"],
        "originalReferenceNumber": reference_number
    }


def create_reverse_provision_request(msisdn, reference_number, client_ip):
    header = create_request_header(client_ip)
    return {
        "requestHeader": header,
        "merchantCode": MERCHANT_CODE,
        "msisdn": msisdn,
        "referenceNumber": REFENCE_NUMBER_PREFIX + header["transactionDateTime"],
        "originalReferenceNumber": reference_number
    }


def create_refund_provision_request(msisdn, reference_number, amount, client_ip):
    header = create_request_header(client_ip)
    return {
        "requestHeader": header,
        "merchantCode": MERCHANT_CODE,
        "msisdn": msisdn,
        "amount": amount,
        "referenceNumber": REFENCE_NUMBER_PREFIX + header["transactionDateTime"],
        "originalReferenceNumber": reference_number
    }

#
#   Only one of cardId, and cardToken must have value for getting three d session id,
#   However, in provision service both of them can have value (case: paying with stored card + cvc)
#
def create_threed_session_request(msisdn, amount, card_id, card_token, client_ip):
    header = create_request_header(client_ip)
    return {
        "requestHeader": header,
        "merchantCode": MERCHANT_CODE,
        "msisdn": msisdn,
        "amount": amount,
        "target": "MERCHANT",
        "transactionType": "AUTH",
        "cardId": card_id,
        "cardToken": card_token
    }


def create_start_threed_session_request(session_id):
    return {
        "threeDSessionId": session_id,
        "callbackurl": "localhost:9090/threedlistener/"
    }


def create_threed_session_result_request(msisdn, session_id, client_ip):
    return {
       "requestHeader": create_request_header(client_ip),
       "merchantCode": MERCHANT_CODE,
       "msisdn": msisdn,
       "threeDSessionId": session_id
    }


def create_summary_reconcile_request(reconciliation_date, total_refund_amount, total_refund_count, total_reverse_amount, total_reverse_count, total_sale_amount, total_sale_count, client_ip):
    return {
        "requestHeader": create_request_header(client_ip),
        "merchantCode": MERCHANT_CODE,
        "reconciliationDate": reconciliation_date,
        "totalRefundAmount": total_refund_amount,
        "totalRefundCount": total_refund_count,
        "totalReverseAmount": total_reverse_amount,
        "totalReverseCount": total_reverse_count,
        "totalSaleAmount": total_sale_amount,
        "totalSaleCount": total_sale_count
    }


def create_get_history_request(reconciliation_date, partition_no, client_ip):
    return {
        "requestHeader": create_request_header(client_ip),
        "merchantCode": MERCHANT_CODE,
        "partitionNo": partition_no,
        "reconciliationDate": reconciliation_date
    }


def create_get_terms_of_service_request(client_ip):
    return {
        "requestHeader": create_request_header(client_ip)
    }


