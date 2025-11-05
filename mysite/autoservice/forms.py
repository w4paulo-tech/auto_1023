from .models import Komentaras
from django import forms as f

class KomentarasForm(f.ModelForm):
    class Meta:
        model = Komentaras
        fields = ['turinys']