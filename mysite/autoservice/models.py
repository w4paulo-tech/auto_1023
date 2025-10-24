from django.db import models as m
import uuid

class Paslauga(m.Model):
    name = m.CharField(verbose_name="Paslaugos tipas", max_length=200)
    price = m.FloatField(verbose_name="Paslaugos kaina \u20ac", default=0)

    def __str__(self):
        return self.name
    
class Automobilis(m.Model):
    make = m.CharField(verbose_name="Markė", max_length=100)
    model = m.CharField(verbose_name="Modelis", max_length=100)
    client = m.CharField(verbose_name="Kliento vardas", max_length=100)
    license_plate = m.CharField(verbose_name="Valstybiniai numeriai", 
                                max_length=6)
    vin_code = m.CharField(verbose_name="VIN", max_length=17)

    def __str__(self):
        return (f"{self.make} {self.model} {self.license_plate}")

class Uzsakymas(m.Model):
    uuid = m.UUIDField(default=uuid.uuid4)
    date = m.DateField(verbose_name="Užsakymo data", null=True, blank=True)
    car = m.ForeignKey(to="Automobilis", verbose_name="Klientas", 
                       on_delete=m.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return (f"{self.uuid}")
    
class UzsakymasInstance(m.Model):
    uzsakymas = m.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", 
                             on_delete=m.CASCADE)
    # paslauga = m.ManyToManyField(to="Paslauga", verbose_name="Paslaugos")
    paslauga = m.ForeignKey(to="Paslauga", verbose_name="Paslauga",
                            on_delete=m.SET_NULL, null=True, blank=True)
    kiekis = m.CharField(verbose_name="Kiekis", max_length=1, default=0)

    UZSAKYMO_STATUSAS = (
        ('a', "Atlikta"),
        ('r', "Ruošiama"),
        ('n', "Nepradėta"),
    )

    statusas = m.CharField(verbose_name="Būsena", max_length=1, 
                           choices=UZSAKYMO_STATUSAS, default="n", blank=True)

    def __str__(self):
        return (f" {self.uzsakymas.uuid} {self.paslauga} {self.kiekis}vnt")
