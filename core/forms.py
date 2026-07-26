from django import forms

class ConviteForm(forms.Form):
    familia = forms.CharField(
        label="Família",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nome da família"
        })
    )

    confirmou = forms.ChoiceField(
        label="Você vai à festa?",
        choices=[("Sim", "Sim"), ("Não", "Não")],
        widget=forms.RadioSelect
    )

    acompanhantes = forms.IntegerField(
        label="Número de acompanhantes",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0"
        })
    )

    nomes_acompanhantes = forms.CharField(
        label="Nomes dos acompanhantes",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Digite os nomes separados por vírgula"
        })
    )