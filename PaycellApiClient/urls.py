from django.urls import path

from . import views
from .view import cardapiview, paymentapiview, cardsoapview, paymentsoapview

urlpatterns = [
    #Uses rest clients
    path('', views.index, name='index'),
    path('getcards/', cardapiview.get_cards, name='getcards'),
    path('hashdata/', cardapiview.hash_data, name='hashdata'),
    path('registercard/', cardapiview.register_card, name='registercard'),
    path('deletecard/', cardapiview.delete_card, name='deletecard'),
    path('payment/', paymentapiview.index, name='payment_index'),
    path('getcardsforpayment/', paymentapiview.get_cards_for_payment, name='getcardsforpayment'),
    path('provision/', paymentapiview.provision, name="provision"),
    path('inquireprovision/', paymentapiview.inquire_provision, name='inquire_provision'),
    path('reverseprovision/', paymentapiview.reverse_provision, name='reverse_provision'),
    path('refundprovision/', paymentapiview.refund_provision, name='refund_provision'),
    path('threedsessionid/', paymentapiview.get_threed_session_id, name='get_threed_session_id'),
    path('showthreedpage/<slug:threed_session_id>', paymentapiview.show_threed_page, name='show_threed_page'),
    path('threedsessionresult/', paymentapiview.get_threed_session_result, name='get_threed_session_result'),
    path('summaryreconcile/', paymentapiview.summary_reconcile, name='summary_reconcile'),
    path('history/', paymentapiview.get_history, name='history'),

    #Uses soap clients
    path('soap/', views.soap_index, name='soap_index'),
    path('soap/getcards/', cardsoapview.get_cards, name='soap_getcards'),
    path('soap/hashdata/', cardsoapview.hash_data, name='soap_hashdata'),
    path('soap/registercard/', cardsoapview.register_card, name='soap_registercard'),
    path('soap/deletecard/', cardsoapview.delete_card, name='soap_deletecard'),
    path('soap/payment/', paymentsoapview.index, name='soap_payment_index'),
    path('soap/getcardsforpayment/', paymentsoapview.get_cards_for_payment, name='soap_getcardsforpayment'),
    path('soap/provision/', paymentsoapview.provision, name="soap_provision"),
    path('soap/inquireprovision/', paymentsoapview.inquire_provision, name='soap_inquire_provision'),
    path('soap/reverseprovision/', paymentsoapview.reverse_provision, name='soap_reverse_provision'),
    path('soap/refundprovision/', paymentsoapview.refund_provision, name='soap_refund_provision'),
    path('soap/threedsessionid/', paymentsoapview.get_threed_session_id, name='soap_get_threed_session_id'),
    path('soap/showthreedpage/<slug:threed_session_id>', paymentsoapview.show_threed_page, name='soap_show_threed_page'),
    path('soap/threedsessionresult/', paymentsoapview.get_threed_session_result, name='soap_get_threed_session_result'),
    path('soap/summaryreconcile/', paymentsoapview.summary_reconcile, name='soap_summary_reconcile'),
    path('soap/history/', paymentsoapview.get_history, name='soap_history')
]