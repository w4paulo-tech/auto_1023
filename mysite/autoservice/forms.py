from .models import Komentaras, CustomUser, Uzsakymas, Paslauga, UzsakymasInstance
from django import forms as f
from django.contrib.auth.forms import UserCreationForm

class KomentarasForm(f.ModelForm):
    class Meta:
        model = Komentaras
        fields = ['turinys']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserUpdateForm(f.ModelForm):
    # email = f.EmailField(unique=True)
    class Meta:
        
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']
        # widgets = {'email': f.EmailField(attrs={'type': ''})}

class InstanceCreateUpdateForm(f.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['car', 'statusas', 'due_back']
        widgets = {'due_back': f.DateInput(attrs={'type': 'date'})}
       