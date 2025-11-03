from django.shortcuts import render
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    my_context = {
        'num_paslaugos': Paslauga.objects.count(),
        'num_atlikti_uzsakymai': Uzsakymas.objects.filter(statusas='a').count(),
        'num_automobiliai': Automobilis.objects.count(),
        'num_visits': num_visits,

    }
    return render(request, template_name="index.html", context=my_context)


def automobiliai(request):
    cars = Automobilis.objects.all()
    paginator = Paginator(cars, per_page=6)
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
    paginate_by = 5


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
    paginator = Paginator(auto_paieskos_rezultatai, per_page=1)
    page_number = request.GET.get('page')
    paged_search = paginator.get_page(page_number)
    context = {
        "query": query,
        "autos": auto_paieskos_rezultatai,
        "search": paged_search,
    }
    return render(request, template_name="paieska.html", context=context)