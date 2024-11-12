from django.db import models

class Tila(models.Model):
    nimi = models.CharField(max_length=100)
    sijainti = models.CharField(max_length=200)

class Varaaja(models.Model):
    nimi = models.CharField(max_length=100)
    yhteystiedot = models.CharField(max_length=200)

class Varaus(models.Model):
    tila = models.ForeignKey(Tila, on_delete=models.CASCADE, related_name='varaukset')
    varaaja = models.ForeignKey(Varaaja, on_delete=models.CASCADE, related_name='varaukset')
    alku_aika = models.DateTimeField()
    loppu_aika = models.DateTimeField()
