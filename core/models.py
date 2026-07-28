from django.db import models

class Convidado(models.Model):
    nome_grupo = models.CharField(
        max_length=100,
        verbose_name="Nome no Convite (ex: Família Silva)"
    )
    codigo_acesso = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Senha do Convite de Papel"
    )
    limite_pessoas = models.PositiveIntegerField(
        verbose_name="Limite total de convidados (incluindo o titular)"
    )
    confirmou = models.CharField(
        max_length=3,
        choices=[("Sim", "Sim"), ("Não", "Não")],
        blank=True,
        null=True,
        verbose_name="Confirmou presença?"
    )
    quantidade_vinda = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantas pessoas realmente vão"
    )

    def __str__(self):
        return f"{self.nome_grupo} (Código: {self.codigo_acesso})"
