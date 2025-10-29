from django.shortcuts import render
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute
from django.views import generic

def index(request):
    my_context = {
        'num_paslaugos': Paslauga.objects.count(),
        'num_atlikti_uzsakymai': Uzsakymas.objects.filter(statusas='a').count(),
        'num_automobiliai': Automobilis.objects.count()

    }
    return render(request, template_name="index.html", context=my_context)


def automobiliai(request):
    context = {
        'automobiliai': Automobilis.objects.all(),
    }
    return render(request, template_name="autos.html", context=context)


def auto(request, automobilis_id):
    context = {
        'auto': Automobilis.objects.get(id=automobilis_id)
    }
    return render(request, template_name="auto.html", context=context)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"