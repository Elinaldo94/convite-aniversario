from django.db import models

class Familia(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da família"
    )
    limite_pessoas = models.PositiveIntegerField(
        verbose_name="Limite de acompanhantes"
    )

    def __str__(self):
        return f"{self.nome} (até {self.limite_pessoas} pessoas)"