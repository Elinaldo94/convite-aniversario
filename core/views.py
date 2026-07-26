from django.shortcuts import render, redirect
from .forms import ConviteForm
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def convite_form(request):
    if request.method == "POST":
        form = ConviteForm(request.POST)
        if form.is_valid():
            familia = form.cleaned_data["familia"]
            confirmou = form.cleaned_data["confirmou"]
            acompanhantes = form.cleaned_data["acompanhantes"]
            nomes_acompanhantes = form.cleaned_data["nomes_acompanhantes"]

            # Autenticação com Google Sheets
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name("BD/credenciais.json", scope)
            client = gspread.authorize(creds)

            # Abrir planilha
            sheet = client.open("Respostas Convite").sheet1

            # Adicionar linha com os dados
            sheet.append_row([
                familia,
                confirmou,
                acompanhantes,
                nomes_acompanhantes
            ])

            return redirect("obrigado")
    else:
        form = ConviteForm()

    return render(request, "convite/convite_form.html", {"form": form})


def obrigado(request):
    return render(request, "convite/obrigado.html")