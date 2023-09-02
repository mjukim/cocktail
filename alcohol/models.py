from django.db import models

# Create your models here.
class Cocktail(models.Model):
    name = models.CharField(max_length=255)
    aroma = models.CharField(max_length=255)
    taste = models.CharField(max_length=255)
    finish = models.CharField(max_length=255)
    kind = models.CharField(max_length=50)
    alcohol = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    
