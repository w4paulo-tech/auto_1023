from django.contrib import admin as a
from .models import Paslauga, Automobilis, Uzsakymas, UzsakymasInstance as Eilute

class EiluteInLine(a.TabularInline):
    model = Eilute
    extra = 0
    can_delete = False
    fields = ['paslauga', 'kiekis', 'line_sum']
    readonly_fields = ['line_sum']

class UzsakymasAdmin(a.ModelAdmin):
    list_display = ['car', 'date', 'total', 'statusas']
    inlines = [EiluteInLine]
    readonly_fields = ['date', 'total']
    fieldsets = [
        ('General', {'fields': ('car', 'date', 'total', 'statusas')}),
    ]

class AutomobilisAdmin(a.ModelAdmin):
    list_display = ['make', 'model', 'client', 'license_plate',
                    'vin_code']
    list_filter = ['make', 'model', 'client']
    search_fields = ['license_plate', 'vin_code']
    
class PaslaugaAdmin(a.ModelAdmin):
    list_display = ['name', 'price']

class EiluteAdmin(a.ModelAdmin):
    list_display = ['uzsakymas', 'paslauga', 'kiekis', 'line_sum']
    readonly_fields = ['line_sum']

    fieldsets = [
        ('Gneral', {'fields': ('uzsakymas', 'paslauga', 'kiekis', 'line_sum')}),
    ]
a.site.register(Paslauga, PaslaugaAdmin)
a.site.register(Automobilis, AutomobilisAdmin)
a.site.register(Uzsakymas, UzsakymasAdmin)
a.site.register(Eilute, EiluteAdmin)
