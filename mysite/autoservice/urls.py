from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.auto, name='automobilis'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>/', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path('paieska/', views.paieska, name='paieska'),
    path('manouzsakymai', views.ManoEiluteListView.as_view(), name='manouzsakymai'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('uzsakymai/create/', views.UzsakymasInstanceCreateView.as_view(), name='uzsakymas_create'),
    path('uzsakymai/<int:pk>/delete/', views.UzsakymasDeleteView.as_view(), name='uzsakymas_delete'),
    path('uzsakymai/<int:pk>/update/', views.UzsakymasUpdateView.as_view(), name='uzsakymas_update'),
    path('uzsakymai/<int:pk>/createpaslauga/', views.PaslaugaCreateView.as_view(), name='paslauga_create'),
    path('eilute/<int:pk>/update/', views.PaslaugaUpdateView.as_view(), name='paslauga_update'),
    path('eilute/<int:pk>/delete/', views.PaslaugaDeleteView.as_view(), name='paslauga_delete'),
    
]