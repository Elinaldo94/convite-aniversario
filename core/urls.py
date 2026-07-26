from django.urls import path
from . import views

urlpatterns = [
    path("", views.convite_form, name="convite_form"),
    path("obrigado/", views.obrigado, name="obrigado"),
]
