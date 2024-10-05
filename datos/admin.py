from django.contrib import admin
from .models import Cita, Mascota


class CitaAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Cita, CitaAdmin)
admin.site.register(Mascota)