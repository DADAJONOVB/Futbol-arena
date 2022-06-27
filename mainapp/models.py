from django.db import models


class FutbolKlub(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='klub')



class Turnir(models.Model):
    name = models.CharField(max_length=255)
    
    
    
class TurnirTur(models.Model):
    turnir = models.ForeignKey(Turnir, on_delete=models.CASCADE)
    klub_bir = models.ForeignKey(FutbolKlub, on_delete=models.CASCADE)
    klub_ikki = models.ForeignKey(FutbolKlub, on_delete=models.CASCADE)