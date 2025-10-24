from django.contrib import admin
from .models import Paslauga, Automobilis, Uzsakymas, UzsakymasInstance

admin.site.register(Paslauga)
admin.site.register(Automobilis)
admin.site.register(Uzsakymas)
admin.site.register(UzsakymasInstance)
