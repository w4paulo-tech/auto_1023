from django.shortcuts import render
from django.http import HttpResponse
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute

def index(request):
    my_context = {
        'num_paslaugos': Paslauga.objects.count(),
        'num_atlikti_uzsakymai': Uzsakymas.objects.filter(statusas='a').count(),
        'num_automobiliai': Automobilis.objects.count()

    }
    return render(request, template_name="index.html", context=my_context)
