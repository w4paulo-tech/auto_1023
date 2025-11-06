from .models import Komentaras, CustomUser
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
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']