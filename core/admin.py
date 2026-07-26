from django.contrib import admin
from .models import Familia

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ("nome", "limite_pessoas")
    search_fields = ("nome",)