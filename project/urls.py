"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import ListView, DetailView
from project.models import Disease, Examination, Symptom, Person

from project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:doc_id>/', views.home, name='home'),
    path('get_user_history/', views.get_history, name='get_history'),
    path('get_disease/', views.get_disease, name='get_disease'),
    path('save_exam/', views.save_exam, name='save_exam'),
]
