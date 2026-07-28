from django.urls import path
from . import views

urlpatterns = [
    path("", views.tela_acesso, name="tela_acesso"),
    path("confirmar/", views.convite_view, name="convite_form"),
]
