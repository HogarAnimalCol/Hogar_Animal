"""
URL configuration for veterinaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from datos import views
from datos import templates


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('citas/', views.citas, name='citas'),
    path('citas_completed/', views.citas_completed, name='citas_completed'),
    path('citas/create/', views.create_cita, name='create_cita'),
    path('citas/<int:cita_id>/', views.cita_detail, name='cita_detail'),
    path('citas/<int:cita_id>/complete', views.complete_cita, name='complete_cita'),
    path('citas/<int:cita_id>/delete', views.delete_cita, name='delete_cita'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/agregar/', views.agregar_mascota, name='agregar_mascota'),
    path('mascotas/<int:pk>/editar/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/<int:pk>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),
]
