import hashlib
import base64


# hashes strings in a given list then returns the result in iso-8859 format
def digest_list_sha1(message_list):
    m = hashlib.sha256()
    for message in message_list:
        m.update(str(message).encode('utf-8'))
    return base64.b64encode(m.digest()).decode('iso-8859-1')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def select_active_provision_tab(active_tab):
    tabs = {
        "provision": "",
        "provisionDetails": "",
        "reconciliation": "",
        "history": ""
    }
    tabs[active_tab] = "active show"
    return tabs

def select_active_card_tab(active_tab):
    tabs = {
        "addCard": "",
        "getCards": "",
        "removeCard": ""
    }
    tabs[active_tab] = "active show"
    return tabs