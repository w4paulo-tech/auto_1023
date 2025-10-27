from django.contrib import admin as a
from .models import Paslauga, Automobilis, Uzsakymas, UzsakymasInstance

class UzsakymasInstanceInLine(a.TabularInline):
    model = UzsakymasInstance
    extra = 0
    can_delete = False

class UzsakymasAdmin(a.ModelAdmin):
    list_display = ['car', 'date', 'total']
    inlines = [UzsakymasInstanceInLine]

class AutomobilisAdmin(a.ModelAdmin):
    list_display = ['make', 'model', 'client', 'license_plate',
                    'vin_code']
    list_filter = ['make', 'model', 'client']
    search_fields = ['license_plate', 'vin_code']
    
    
class PaslaugaAdmin(a.ModelAdmin):
    list_display = ['name', 'price']

class UzsakymasInstanceAdmin(a.ModelAdmin):
    list_display = ['uzsakymas', 'paslauga', 'kiekis', 'line_sum']

a.site.register(Paslauga, PaslaugaAdmin)
a.site.register(Automobilis, AutomobilisAdmin)
a.site.register(Uzsakymas, UzsakymasAdmin)
a.site.register(UzsakymasInstance, UzsakymasInstanceAdmin)
