from django.forms import ModelForm
from django import forms
from .models import Cita, Mascota
from django.contrib.auth.models import User

class CreateCitaForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)  # Campo para seleccionar un usuario

    class Meta:
        model = Cita
        fields = ['title', 'description', 'mascota', 'date', 'user']  # Incluye los campos relevantes
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Selector de fecha
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            if request.user.is_staff:
                # El administrador puede ver todas las mascotas y todos los usuarios
                self.fields['mascota'].queryset = Mascota.objects.all()
                self.fields['user'].queryset = User.objects.all()
                self.fields['completed'] = forms.BooleanField(required=False, label='¿Cita completada?')  # Solo admins ven este campo
            else:
                # Los usuarios solo ven sus propias mascotas
                self.fields['mascota'].queryset = Mascota.objects.filter(dueño=request.user)
                # Establecer el usuario actual y ocultar el campo user
                self.fields['user'].initial = request.user
                self.fields['user'].widget = forms.HiddenInput()
                # Ocultar el campo 'completed' para usuarios normales
                self.fields.pop('completed', None)
                
class MascotaForm(forms.ModelForm):
    dueño = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'dueño']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and not request.user.is_superuser:
            self.fields['dueño'].widget = forms.HiddenInput()
            self.fields['dueño'].initial = request.user
