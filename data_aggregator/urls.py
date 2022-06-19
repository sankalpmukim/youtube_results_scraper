import imp
from django.urls import path
from . import views

urlpatterns = [
    path('activate/', views.activate, name='activate'),
    path('deactivate/', views.deactivate, name='deactivate'),
]
