from django.shortcuts import render


def app_index(request):
    if request.method == 'GET':
        return render(request, 'app_index.html')