from django.test import TestCase
from django.urls import reverse
from .forms import ConviteForm

class ConviteFormTest(TestCase):
    def test_form_valido(self):
        form_data = {
            "familia": "Família Silva",
            "confirmou": "Sim",
            "acompanhantes": 2,
            "nomes_acompanhantes": "Maria, João"
        }
        form = ConviteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalido(self):
        form_data = {
            "familia": "",
            "confirmou": "Sim",
            "acompanhantes": -1,
            "nomes_acompanhantes": ""
        }
        form = ConviteForm(data=form_data)
        self.assertFalse(form.is_valid())


class ConviteViewsTest(TestCase):
    def test_acesso_formulario(self):
        response = self.client.get(reverse("convite_form"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Família")

    def test_redirecionamento_obrigado(self):
        form_data = {
            "familia": "Família Souza",
            "confirmou": "Sim",
            "acompanhantes": 1,
            "nomes_acompanhantes": "Carlos"
        }
        response = self.client.post(reverse("convite_form"), data=form_data)
        self.assertEqual(response.status_code, 302)  # redireciona
        self.assertRedirects(response, reverse("obrigado"))