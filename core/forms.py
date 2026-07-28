from django import forms
from .models import Convidado

class AcessoForm(forms.Form):
    codigo = forms.CharField(
        label="Digite o código do seu convite:",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg text-center",
            "placeholder": "EX: SILVA123"
        })
    )

class RespostaConviteForm(forms.ModelForm):
    confirmou = forms.ChoiceField(
        choices=[("Sim", "Sim"), ("Não", "Não")],
        widget=forms.RadioSelect,
        label="Confirmar presença?",
    )

    class Meta:
        model = Convidado
        fields = ["confirmou", "quantidade_vinda"]
        widgets = {
            # Mantém os atributos nativos do HTML para navegadores modernos
            "quantidade_vinda": forms.NumberInput(attrs={
                "class": "form-control", 
                "min": "1",
                "value": "1"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantidade_vinda'].required = False

        # 1. Força o valor 'Sim' se o convidado ainda não tiver uma resposta salva
        if not self.instance.confirmou:
            self.data = self.data.copy() if self.data else {}
            self.fields['confirmou'].initial = "Sim"
            self.instance.confirmou = "Sim"

        # 2. CORREÇÃO DEFINITIVA DO ZERO: Se a resposta for "Sim" (ou padrão), impede o 0 do banco de subir para a tela
        if self.instance.confirmou == "Sim" and (self.instance.quantidade_vinda == 0 or self.instance.quantidade_vinda is None):
            self.initial['quantidade_vinda'] = 1
            # Atualiza o dado do próprio objeto para o Django preencher o campo com 1
            self.instance.quantidade_vinda = 1

    def clean_quantidade_vinda(self):
        quantidade = self.cleaned_data.get('quantidade_vinda')
        confirmou = self.cleaned_data.get('confirmou')

        confirmou_str = str(confirmou).strip().lower()

        # Se o usuário marcou que NÃO vai, a quantidade zero é permitida e aceita
        if confirmou_str in ['false', 'não', 'nao', '2', '0', 'none', '']:
            return 0

        # Trava de segurança no backend caso ele tente digitar 0 ou esvaziar o campo
        if quantidade is None or quantidade < 1:
            raise forms.ValidationError(
                "Como você confirmou presença, a quantidade de participantes deve ser de pelo menos 1 pessoa."
            )

        limite = self.instance.limite_pessoas 
        if quantidade > limite:
            raise forms.ValidationError(
                f"O limite máximo de participantes para este convite é de {limite} pessoas."
            )

        return quantidade

    def clean(self):
        cleaned_data = super().clean()
        confirmou = cleaned_data.get('confirmou')

        if confirmou == "Não":
            cleaned_data['quantidade_vinda'] = 0
            
        return cleaned_data
