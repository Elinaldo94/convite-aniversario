from django.test import TestCase
from django.urls import reverse
from .forms import RespostaConviteForm
from .models import Convidado

class ConviteFormTest(TestCase):
    def test_form_valido(self):
        form_data = {
            "confirmou": "Sim",
            "quantidade_vinda": 2
        }
        # Criamos uma instância fake de convidado para o init ler o limite de pessoas
        convidado_teste = Convidado(limite_pessoas=5)
        form = RespostaConviteForm(data=form_data, instance=convidado_teste)
        self.assertTrue(form.is_valid())

    def test_form_invalido_por_limite(self):
        form_data = {
            "confirmou": "Sim",
            "quantidade_vinda": 10 # Ultrapassa o limite de 5
        }
        convidado_teste = Convidado(limite_pessoas=5)
        form = RespostaConviteForm(data=form_data, instance=convidado_teste)
        self.assertFalse(form.is_valid())
