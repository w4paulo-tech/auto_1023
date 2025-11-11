from .models import Paslauga, Uzsakymas, Automobilis, UzsakymasInstance as Eilute, CustomUser
from .forms import (KomentarasForm, CustomUserCreateForm, CustomUserUpdateForm, 
                    InstanceCreateUpdateForm)
from django.shortcuts import render, reverse, redirect
from django.views import generic
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"
    form_class = KomentarasForm

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.get_object().pk}) 
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.instance.uzsakymas = self.get_object()
        form.instance.komentatorius = self.request.user
        form.save()
        return super().form_valid(form)
    
my_query = ""    

def paieska(request):
    query = request.GET.get('query')
    if query:
        global my_query
        my_query = query
    else:
        my_query = ""
    
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

class SignUp(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=...):
        return self.request.user
    
    def form_invalid(self, form):
        self.request.user.refresh_from_db()
        return self.render_to_response(self.get_context_data(form=form))

class UzsakymasInstanceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    template_name = "uzsakymas_form.html"
    form_class = InstanceCreateUpdateForm
    success_url = reverse_lazy('manouzsakymai')

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class UzsakymasUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    template_name = "uzsakymas_form.html"
    form_class = InstanceCreateUpdateForm
    # success_url = reverse_lazy('manouzsakymai')
    
    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().user == self.request.user

class UzsakymasDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    template_name = "uzsakymas_delete.html"
    context_object_name = "uzsakymas"
    success_url = reverse_lazy('manouzsakymai')

    def test_func(self):
        return self.get_object().user == self.request.user

class PaslaugaCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Eilute
    template_name = "paslauga_form.html"
    # form_class = PaslaugaKiekisForm
    fields = ['paslauga', 'kiekis']
    # success_url = reverse_lazy('manouzsakymai')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uzsakymas_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.kwargs['pk']})
    
    def test_func(self):
        return Uzsakymas.objects.get(pk=self.kwargs['pk']).user == self.request.user
    
    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class PaslaugaUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Eilute
    template_name = "paslauga_form.html"
    fields = ['paslauga', 'kiekis']
    context_object_name = "paslauga"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uzsakymas_id'] = self.get_object().uzsakymas.pk
        return context

    def get_success_url(self):
        # return reverse("uzsakymas", kwargs={"pk": self.object.uzsakymas_id})
        uzsakymas_pk = self.object.uzsakymas_id
        return reverse("uzsakymas", kwargs={"pk": uzsakymas_pk})
    
    def test_func(self):
        # return Uzsakymas.objects.get(pk=self.get_object().uzsakymas.pk).user == self.request.user
        return self.get_object().uzsakymas.user == self.request.user

    def form_valid(self, form):
        # form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class PaslaugaDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Eilute
    template_name = "paslauga_delete.html"
    context_object_name = "paslauga"

    def get_success_url(self):
        uzsakymas_pk = self.object.uzsakymas_id
        return reverse("uzsakymas", kwargs={"pk": uzsakymas_pk})
    
    def test_func(self):
        # return Uzsakymas.objects.get(pk=self.get_object().uzsakymas.pk).user == self.request.user
        return self.get_object().uzsakymas.user == self.request.user
