from django.db import models
from django.core import validators

class Sestavina(models.Model):
    ime = models.CharField(max_length=30)


class Mera(models.Model):
    ime = models.CharField(max_length=30)


class TipJedi(models.Model):
    ime = models.CharField(max_length=30)


class Recept(models.Model):
    ime = models.CharField(max_length=50)
    ocena = models.FloatField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)])
    povezava = models.URLField(max_length=200)
    zahtevnost = models.FloatField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)])
    cas_priprave = models.FloatField(validators=[validators.MinValueValidator(0)])
    postopek = models.TextField(max_length=10000)
    tipi = models.ManyToManyField(TipJedi)
    sestavine = models.ManyToManyField(Sestavina, through='Priprava')


class Priprava(models.Model):
    kolicina = models.FloatField
    mera = models.ForeignKey(Mera, on_delete=models.CASCADE)
    sestavina = models.ForeignKey(Sestavina, on_delete=models.CASCADE)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
