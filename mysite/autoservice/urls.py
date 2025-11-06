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
    path('profile/', views.ProfileUpdateView.as_view(), name='profile')
    
]