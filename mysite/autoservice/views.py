from django.shortcuts import render
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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

@login_required(login_url="/accounts/login/")
def automobiliai(request):
    cars = Automobilis.objects.all()
    paginator = Paginator(cars, per_page=6)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)    
    context = {
        'automobiliai': paged_cars,
    }
    return render(request, template_name="autos.html", context=context)

@login_required(login_url="/accounts/login/")
def auto(request, automobilis_id):
    context = {
        'auto': Automobilis.objects.get(id=automobilis_id)
    }
    return render(request, template_name="auto.html", context=context)


class UzsakymasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"
    paginate_by = 5

class ManoEiluteListView(LoginRequiredMixin, generic.ListView):
    model = Eilute
    template_name = "mano_uzsakymai.html"
    context_object_name = "instances"
    paginate_by = 5
    
    def get_queryset(self):
        return Uzsakymas.objects.filter(user=self.request.user)


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"

my_query = ""    

def paieska(request):
    query = request.GET.get('query')
    global my_query
    if query:
        my_query = query
    auto_paieskos_rezultatai = Automobilis.objects.filter(
        Q(client__icontains=my_query) |
        Q(make__icontains=my_query) |
        Q(model__icontains=my_query) |
        Q(license_plate__icontains=my_query) |
        Q(vin_code__icontains=my_query)
    )
    paginator = Paginator(auto_paieskos_rezultatai, per_page=6)
    page_number = request.GET.get('page')
    paged_search = paginator.get_page(page_number)

    context = {
        "query": my_query,
        "autos": paged_search,
        "search": paged_search,
    }
    return render(request, template_name="paieska.html", context=context)