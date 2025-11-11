from django.contrib import admin as a
from .models import (Paslauga, Automobilis, Uzsakymas, Komentaras, 
                     UzsakymasInstance as Eilute,  CustomUser)
from django.contrib.auth.admin import UserAdmin

class EiluteInLine(a.TabularInline):
    model = Eilute
    extra = 0
    can_delete = False
    fields = ['paslauga', 'kiekis', 'line_sum']
    readonly_fields = ['line_sum']

class UzsakymasAdmin(a.ModelAdmin):
    list_display = ['car', 'date', 'due_back', 'total', 'statusas', 'user']
    inlines = [EiluteInLine]
    readonly_fields = ['date', 'total']
    fieldsets = [
        ('General', {'fields': ('car', 'date', 'due_back', 
                                'total', 'statusas', 'user')}),
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
        ('General', {'fields': ('uzsakymas', 'paslauga', 'kiekis', 'line_sum')}),
    ]

class KomentarasAdmin(a.ModelAdmin):
    list_display = ['uzsakymas', 'komentatorius', 'sukurta', 'turinys']

class CustomUserAdmin(a.ModelAdmin):
    list_display = ['username', 'email']
    fieldsets = UserAdmin.fieldsets

a.site.register(Komentaras, KomentarasAdmin)
a.site.register(Paslauga, PaslaugaAdmin)
a.site.register(Automobilis, AutomobilisAdmin)
a.site.register(Uzsakymas, UzsakymasAdmin)
a.site.register(Eilute, EiluteAdmin)
a.site.register(CustomUser, CustomUserAdmin)
