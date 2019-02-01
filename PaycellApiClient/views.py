from django.shortcuts import render

def index(request):
    if request.method == 'GET':
        active_tabs = {
            "addCard": "active show",
            "getCards": "",
            "removeCard": ""
        }
        return render(request, 'card_api_index.html', {"tabs": active_tabs})


def soap_index(request):
    if request.method == 'GET':
        active_tabs = {
            "addCard": "active show",
            "getCards": "",
            "removeCard": ""
        }
        return render(request, 'card_soap_index.html', {"tabs": active_tabs})