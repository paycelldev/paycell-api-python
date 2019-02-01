from zeep import Client
from ..utils import cardapihelper, paymentapihelper

"""
    This class is the SOAP client of paycell api.
    Each function of the client class takes necessary parameters, than passes them into helper class which returns request dict.
    Finally they return response dict
"""


class ProvisionSoapClient(object):
    def __init__(self):
        self.client = Client('https://tpay-test.turkcell.com.tr/tpay/provision/services/ws?wsdl')

    def get_cards(self, msisdn, client_ip):
        request = cardapihelper.create_get_card_request(msisdn, client_ip)
        return self.client.service.getCards(**request)

    def register_card(self, alias, msisdn, card_token, eula_id, is_default, threed_session_id, client_ip):
        request = cardapihelper.create_register_card_request(alias, msisdn, card_token, eula_id, is_default, threed_session_id, client_ip)
        return self.client.service.registerCard(**request)

    def delete_card(self, msisdn, card_id, client_ip):
        request = cardapihelper.create_delete_card_request(msisdn, card_id, client_ip)
        return self.client.service.deleteCard(**request)

    def make_provision(self, card_id, card_token, msisdn, amount, currency,  payment_type, threed_session_id, client_ip):
        request = paymentapihelper.create_provision_request(card_id, card_token, msisdn, amount, currency, payment_type, threed_session_id, client_ip)
        return self.client.service.provision(**request), request["referenceNumber"]

    def inquire_provision(self, msisdn, reference_number, client_ip):
        request = paymentapihelper.create_inquire_provision_request(msisdn, reference_number, client_ip)
        return self.client.service.inquire(**request)

    def reverse_provision(self, msisdn, reference_number, client_ip):
        request = paymentapihelper.create_reverse_provision_request(msisdn, reference_number, client_ip)
        return self.client.service.reverse(**request)

    def refund_provision(self, msisdn, reference_number, amount, client_ip):
        request = paymentapihelper.create_refund_provision_request(msisdn, reference_number, amount, client_ip)
        return self.client.service.refund(**request)

    def get_summary_reconcile(self, reconciliation_date, total_refund_amount, total_refund_count, total_reverse_amount, total_reverse_count, total_sale_amount, total_sale_count, client_ip):
        request = paymentapihelper.create_summary_reconcile_request(reconciliation_date, total_refund_amount, total_refund_count, total_reverse_amount, total_reverse_count, total_sale_amount, total_sale_count, client_ip)
        return self.client.service.summaryReconciliation(**request)

    def get_threed_session_id(self, msisdn, amount, card_id, card_token, client_ip):
        request = paymentapihelper.create_threed_session_request(msisdn, amount, card_id, card_token, client_ip)
        return self.client.service.getThreeDSession(**request)

    def get_threed_session_result(self, msisdn, session_id, client_ip):
        request = paymentapihelper.create_threed_session_result_request(msisdn, session_id, client_ip)
        return self.client.service.getThreeDSessionResult(**request)

    def make_provision_marketplace(self, card_id, card_token, msisdn, amount, currency,  payment_type, threed_session_id, client_ip):
        request = paymentapihelper.create_provision_request(card_id, card_token, msisdn, amount, currency, payment_type, threed_session_id, client_ip)
        return self.client.service.provisionForMarketPlace(**request), request["referenceNumber"]

    def get_history(self, reconciliation_date, partition_no, client_ip):
        request = paymentapihelper.create_get_history_request(reconciliation_date, partition_no, client_ip)
        return self.client.service.getProvisionHistory(**request)
