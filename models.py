from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class CarModel(models.Model):
    TYPES = [('Sedan','Sedan'),('SUV','SUV'),('Wagon','Wagon'),('Truck','Truck'),('Coupe','Coupe'),('Other','Other')]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=12, choices=TYPES, default='Other')
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2035)], default=2024)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['car_make','name','year'], name='unique_model_make_year')]
    def __str__(self): return f'{self.car_make.name} {self.name} ({self.year})'
