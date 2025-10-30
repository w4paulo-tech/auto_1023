from django.shortcuts import render
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    my_context = {
        'num_paslaugos': Paslauga.objects.count(),
        'num_atlikti_uzsakymai': Uzsakymas.objects.filter(statusas='a').count(),
        'num_automobiliai': Automobilis.objects.count()

    }
    return render(request, template_name="index.html", context=my_context)


def automobiliai(request):
    cars = Automobilis.objects.all()
    paginator = Paginator(cars, per_page=3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)    
    context = {
        'automobiliai': paged_cars,
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
    paginate_by = 2


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"

def paieska(request):
    query = request.GET.get('query')
    auto_paieskos_rezultatai = Automobilis.objects.filter(
        Q(client__icontains=query) |
        Q(make__icontains=query) |
        Q(model__icontains=query) |
        Q(license_plate__icontains=query) |
        Q(vin_code__icontains=query)
    )
    context = {
        "query": query,
        "autos": auto_paieskos_rezultatai,
    }
    return render(request, template_name="paieska.html", context=context)