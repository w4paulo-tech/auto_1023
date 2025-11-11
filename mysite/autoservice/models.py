from django.db import models as m
import uuid
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

class Paslauga(m.Model):
    name = m.CharField(verbose_name=_("Type"))
    price = m.FloatField(verbose_name=_("Price \u20ac"), null=True, default=0)
    
    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.name
    
class Automobilis(m.Model):
    make = m.CharField(verbose_name=_("Make"))
    model = m.CharField(verbose_name=_("Model"))
    client = m.CharField(verbose_name=_("Client"))
    license_plate = m.CharField(verbose_name=_("License plate"))
    vin_code = m.CharField(verbose_name="VIN", max_length=17)
    cover = m.ImageField(verbose_name=_("Cover"), 
                         upload_to="covers",
                         null=True, blank=True)
    description = HTMLField(verbose_name=_("Description"), default="")

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def __str__(self):
        return (f"{self.make} {self.model}")

class Uzsakymas(m.Model):
    date = m.DateTimeField(verbose_name=_("Date"), 
                           auto_now_add=True)
    car = m.ForeignKey(to="Automobilis", 
                       verbose_name=_("Client"), 
                       on_delete=m.SET_NULL, null=True, blank=True,
                       related_name="uzsakymas")
    user = m.ForeignKey(to="autoservice.CustomUser", 
                        verbose_name=_("User"), 
                        on_delete=m.SET_NULL, null=True, blank=True)
    due_back = m.DateField(verbose_name=_("Due back"), null=True, blank=True)
    
    def filled_id(self):
        year = self.date.strftime('%y') if self.date else timezone.now().strftime('%y')
        return f"MA-{(year)}{str(self.id).zfill(4)}"

    def due_date(self):
        return self.due_back and timezone.now().date() > self.due_back
    
    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.line_sum()
        return result
    
    total.short_description = _("Total \u20ac")
               
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-pk']


    def __str__(self):
        return (f"SF Nr.: {self.filled_id()} {self.car}")
    
    UZSAKYMO_STATUSAS = (
        ('a', _("Done")),
        ('r', _("In preparation")),
        ('n', _("Not started")),
        ('s', _("Suspended")),
        ('c', _("Canceled")),
    )
    statusas = m.CharField(verbose_name=_("Status"), 
                           max_length=1, 
                           choices=UZSAKYMO_STATUSAS, 
                           default="n", blank=True)

class UzsakymasInstance(m.Model):
    uzsakymas = m.ForeignKey(to="Uzsakymas", 
                             verbose_name=_("Order"), 
                             on_delete=m.CASCADE, 
                             related_name="lines")
    paslauga = m.ForeignKey(to="Paslauga", 
                            verbose_name=_("Service"),
                            on_delete=m.SET_NULL, null=True, blank=True,
                            related_name="uzsakymas")
    kiekis = m.IntegerField(verbose_name=_("Quantity"), default=1,
                            )
    
    def line_sum(self):
        return self.kiekis * self.paslauga.price
    
    line_sum.short_description = _("Sum \u20ac")

    class Meta:
        verbose_name = _("Order line")
        verbose_name_plural = _("Order lines")

    def __str__(self):
        return (f" {self.paslauga} {self.kiekis}{_('pcs')}")

class Komentaras(m.Model):
    uzsakymas = m.ForeignKey(to="Uzsakymas",
                             verbose_name=_("Order"),
                             on_delete=m.SET_NULL,
                             null=True, blank=True,
                             related_name="komentaras")
    komentatorius = m.ForeignKey(to="autoservice.CustomUser", 
                                 verbose_name=_("Author"),
                                 on_delete=m.SET_NULL, null=True, blank=True)
    sukurta = m.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    turinys = m.TextField(verbose_name=_("Text"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-pk']

class CustomUser(AbstractUser):
    photo = m.ImageField(upload_to="profile_pics", null=True, blank=True)
    email = m.EmailField(unique=True, null=True, blank=True)
    username = m.CharField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

