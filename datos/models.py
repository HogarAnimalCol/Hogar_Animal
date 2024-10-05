from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)  # Por ejemplo: perro, gato, etc.
    raza = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    dueño = models.ForeignKey(User, on_delete=models.CASCADE)  # Vincula la mascota a un usuario

    def __str__(self):
        return f"{self.nombre} - {self.especie} ({self.raza})"

class Cita(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=True, blank=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)  # Campo para seleccionar la mascota
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - by ' + self.user.username
