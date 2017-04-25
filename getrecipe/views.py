from django.shortcuts import render

def index(request):
    return render(request, 'getrecipe/index.html', {'ime': "Uporabnik"})
