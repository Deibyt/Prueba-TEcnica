"""proyectoPrueba URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myapp import views

from myapp.views import calcular_suma_costos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('calcular-suma-costos/', calcular_suma_costos, name='calcular_suma_costos'),
    path('calcular_suma_emp1/', views.calcular_suma_emp1, name='calcular_suma_emp1'),
    path('calcular_suma_emp2/', views.calcular_suma_emp2, name='calcular_suma_emp2'),
    path('calcular_suma_emp3/', views.calcular_suma_emp3, name='calcular_suma_emp3'),
    path('calcular_suma_emp4/', views.calcular_suma_emp4, name='calcular_suma_emp4'),
    path('calcular_suma_emp5/', views.calcular_suma_emp5, name='calcular_suma_emp5'),
    path('calificar_riesgos_emp_g/', views.calificar_riesgos_emp_g, name='calificar_riesgos_emp_g'),
    path('calificar_riesgos_emp1/', views.calificar_riesgos_emp1, name='calificar_riesgos_emp1'),
    path('calificar_riesgos_emp2/', views.calificar_riesgos_emp2, name='calificar_riesgos_emp2'),
    path('calificar_riesgos_emp3/', views.calificar_riesgos_emp3, name='calificar_riesgos_emp3'),
    path('calificar_riesgos_emp4/', views.calificar_riesgos_emp4, name='calificar_riesgos_emp4'),
    path('calificar_riesgos_emp5/', views.calificar_riesgos_emp5, name='calificar_riesgos_emp5'),
    path('mostrar_datos_emp1/', views.mostrar_datos_emp1, name='mostrar_datos_emp1'),
    path('mostrar_datos_emp2/', views.mostrar_datos_emp2, name='mostrar_datos_emp2'),
    path('mostrar_datos_emp3/', views.mostrar_datos_emp3, name='mostrar_datos_emp3'),
    path('mostrar_datos_emp4/', views.mostrar_datos_emp4, name='mostrar_datos_emp4'),
    path('mostrar_datos_emp5/', views.mostrar_datos_emp5, name='mostrar_datos_emp5'),
    path('modelo_riesgos_emp1/', views.modelo_riesgos_emp1, name='modelo_riesgos_emp1'),
    path('modelo_riesgos_emp2/', views.modelo_riesgos_emp2, name='modelo_riesgos_emp2'),
    path('modelo_riesgos_emp3/', views.modelo_riesgos_emp3, name='modelo_riesgos_emp3'),
    path('modelo_riesgos_emp4', views.modelo_riesgos_emp4, name='modelo_riesgos_emp4'),
    path('modelo_riesgos_emp5/', views.modelo_riesgos_emp5, name='modelo_riesgos_emp5'),
    path('calificar-riesgos-emp/', views.calificar_riesgos_emp, name='calificar_riesgos_emp'),

]
