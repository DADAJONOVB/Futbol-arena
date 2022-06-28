from django.db import models


class FutbolKlub(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='klub')

    def __str__(self):
        return self.name

class Turnir(models.Model):
    name = models.CharField(max_length=255)    
    
    def __str__(self):
        return self.name
    
class TurnirTur(models.Model):
    name = models.CharField(max_length=255)
    turnir = models.ForeignKey(Turnir, on_delete=models.CASCADE)
    data_start = models.DateField()

    def __str__(self):
        return self.name

class Match(models.Model):
    data = models.DateField()
    turnir_tur = models.ForeignKey(TurnirTur, on_delete=models.CASCADE)
    first_klub = models.ForeignKey(FutbolKlub, on_delete=models.CASCADE, related_name='bir')
    first_klub_result = models.PositiveIntegerField(blank=True, null=True)
    second_klub = models.ForeignKey(FutbolKlub, on_delete=models.CASCADE, related_name='ikki')
    second_klub_result = models.PositiveIntegerField(blank=True, null=True)
    winner = models.ForeignKey(FutbolKlub, on_delete=models.CASCADE, blank=True, null=True, related_name='golib')

    def __str__(self):
        return self.first_klub, self.second_klub