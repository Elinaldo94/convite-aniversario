from django.contrib import admin
from .models import Convidado

@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ("nome_grupo", "codigo_acesso", "limite_pessoas", "confirmou", "quantidade_vinda")
    list_filter = ("confirmou",)
    search_fields = ("nome_grupo", "codigo_acesso")
