from django.forms import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import CreateCitaForm, MascotaForm
from .models import Cita, Mascota
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import IntegrityError


# Create your views here.

def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            login(request, user)  # Iniciar sesión al usuario después del registro
            return redirect('citas')  # Redirigir a la vista de citas después del registro
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {
        'form': form
    })

        
@login_required
def citas(request):
    query = request.GET.get('q')
    if request.user.is_staff:
        citas = Cita.objects.filter(completed=False)  # Admin ve todas las citas no completadas
    else:
        citas = Cita.objects.filter(user=request.user, completed=False)  # Usuario ve solo sus citas no completadas

    if query:
        citas = citas.filter(title__icontains=query) | citas.filter(description__icontains=query) | citas.filter(user__username__icontains=query)

    return render(request, 'citas.html', {'citas': citas})

@login_required
def citas_completed(request):
    query = request.GET.get('q')
    if request.user.is_staff:
        citas = Cita.objects.filter(completed=True).order_by('-date')  # Admin ve todas las citas completadas
    else:
        citas = Cita.objects.filter(user=request.user, completed=True).order_by('-date')  # Usuario ve solo sus citas completadas

    if query:
        citas = citas.filter(title__icontains=query) | citas.filter(description__icontains=query) | citas.filter(user__username__icontains=query)

    return render(request, 'citas_completed.html', {'citas': citas})
@login_required
def create_cita(request):
    if request.method == 'POST':
        form = CreateCitaForm(request.POST, request=request)
        if form.is_valid():
            new_cita = form.save(commit=False)
            if request.user.is_staff:
                # Si es admin, se asigna el usuario y si la cita está completada
                new_cita.user = form.cleaned_data['user']
                new_cita.completed = form.cleaned_data.get('completed', False)
            else:
                # Si es un usuario normal, se asigna el usuario actual
                new_cita.user = request.user
            new_cita.save()
            return redirect('citas')  # Redirige a la página de citas asignadas
        else:
            return render(request, 'create_cita.html', {
                'form': form,
                'error': 'Por favor, proporciona datos válidos.'
            })
    else:
        form = CreateCitaForm(request=request)

    return render(request, 'create_cita.html', {'form': form})

@login_required
def cita_detail(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)  # Permite que el admin acceda a cualquier cita
    if request.method == 'GET':
        form = CreateCitaForm(instance=cita)
        return render(request, 'cita_detail.html', {'cita': cita, 'form': form})
    else:
        try:
            form = CreateCitaForm(request.POST, instance=cita)
            form.save()
            return redirect('citas')
        except ValueError:
            return render(request, 'cita_detail.html', {'cita': cita, 'form': form, 'error': "Error updating cita"})

@login_required    
def complete_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    if request.method == 'POST':
        cita.date = timezone.now()  # Marca la fecha como ahora
        cita.completed = True  # Marca la cita como completada
        cita.save()
        return redirect('citas')

@login_required    
def delete_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)  # Permite que el admin acceda a cualquier cita
    if request.method == 'POST':
        cita.delete()
        return redirect('citas')

#Vistas para mascota

@login_required
def lista_mascotas(request):
    query = request.GET.get('q')
    if request.user.is_superuser:
        mascotas = Mascota.objects.all()  # Admin ve todas las mascotas
    else:
        mascotas = Mascota.objects.filter(dueño=request.user)  # Usuario ve solo sus mascotas

    if query:
        mascotas = mascotas.filter(nombre__icontains=query) | mascotas.filter(especie__icontains=query) | mascotas.filter(raza__icontains=query)

    return render(request, 'lista_mascotas.html', {'mascotas': mascotas})

@login_required
def agregar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request=request)  # Pasa el request aquí
        if form.is_valid():
            mascota = form.save(commit=False)
            if request.user.is_superuser:
                mascota.dueño = form.cleaned_data['dueño']
            else:
                mascota.dueño = request.user
            mascota.save()
            return redirect('lista_mascotas')  # Redirige a la lista de mascotas
        else:
            print(form.errors)  # Imprimir errores de validación en la consola
    else:
        form = MascotaForm(request=request)
    
    return render(request, 'agregar_mascota.html', {'form': form})

@login_required
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('lista_mascotas') 
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'editar_mascota.html', {'form': form})

@login_required
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.method == 'POST':
        try:
            mascota.delete()
            return redirect('lista_mascotas')
        except Exception as e:
            print(f"Error al eliminar la mascota: {e}")  # Esto ayudará a identificar el problema
            return render(request, 'error.html', {'error': str(e)})
    return render(request, 'confirmar_eliminar.html', {'mascota': mascota})


@login_required        
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecto'
           })
        else:
            login(request, user)
            return redirect('citas')
                
def is_admin(user):
    return user.is_superuser
                     
