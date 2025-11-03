from django.db import models as m
import uuid

class Paslauga(m.Model):
    name = m.CharField(verbose_name="Paslaugos tipas")
    price = m.FloatField(verbose_name="Paslaugos kaina \u20ac", 
                         )

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return self.name
    
class Automobilis(m.Model):
    make = m.CharField(verbose_name="Markė")
    model = m.CharField(verbose_name="Modelis")
    client = m.CharField(verbose_name="Kliento vardas")
    license_plate = m.CharField(verbose_name="Valstybiniai numeriai")
    vin_code = m.CharField(verbose_name="VIN", max_length=17)
    cover = m.ImageField(verbose_name="Viršelis", upload_to="covers",
                         null=True, blank=True)

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def filled_id(self):
        return str(self.id).zfill(6)


    def __str__(self):
        return (f"{self.filled_id()} {self.make} {self.model}")

class Uzsakymas(m.Model):
    date = m.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
    car = m.ForeignKey(to="Automobilis", verbose_name="Klientas", 
                       on_delete=m.SET_NULL, null=True, blank=True,
                       )
    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.line_sum()
        return result
    
    total.short_description = "Viso \u20ac"
               
    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return (f"ID: {self.car} - {self.date.strftime('%Y-%m-%d %H:%M')}")
    
    UZSAKYMO_STATUSAS = (
        ('a', "Atlikta"),
        ('r', "Ruošiama"),
        ('n', "Nepradėta"),
        ('s', "Sustabdyta"),
        ('c', "Atšaukta"),
    )
    statusas = m.CharField(verbose_name="Būsena", max_length=1, 
                           choices=UZSAKYMO_STATUSAS, default="n", blank=True)

class UzsakymasInstance(m.Model):
    uzsakymas = m.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", 
                             on_delete=m.CASCADE, related_name="lines")
    paslauga = m.ForeignKey(to="Paslauga", verbose_name="Paslauga",
                            on_delete=m.SET_NULL, null=True, blank=True,
                            related_name="uz")
    kiekis = m.IntegerField(verbose_name="Kiekis")
    
    def line_sum(self):
        return self.kiekis * self.paslauga.price
    
    line_sum.short_description = "Suma \u20ac"

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def __str__(self):
        return (f" {self.paslauga} {self.kiekis}vnt")
