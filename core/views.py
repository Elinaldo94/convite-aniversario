from django.shortcuts import render, redirect, get_object_or_404
from .forms import AcessoForm, RespostaConviteForm
from .models import Convidado

def tela_acesso(request):
    erro = None
    if request.method == "POST":
        form = AcessoForm(request.POST)
        if form.is_valid():
            codigo_digitado = form.cleaned_data["codigo"].strip().upper()
            try:
                # Busca o convidado pela senha
                convidado = Convidado.objects.get(codigo_acesso__iexact=codigo_digitado)
                # Salva o ID dele na sessão do navegador
                request.session["convidado_id"] = convidado.id
                return redirect("convite_form")
            except Convidado.DoesNotExist:
                erro = "Código inválido. Por favor, verifique o seu convite de papel."
    else:
        form = AcessoForm()
        
    return render(request, "convite/acesso.html", {"form": form, "erro": erro})


def convite_view(request):
    convidado_id = request.session.get("convidado_id")
    if not convidado_id:
        return redirect("tela_acesso")
        
    convidado = get_object_or_404(Convidado, id=convidado_id)
    status_popup = None  

    if request.method == 'POST':
        # 1. PEGAMOS OS DADOS DO POST PARA ANALISAR ANTES DA VALIDAÇÃO
        dados_post = request.POST.copy()
        resposta_radio = dados_post.get('confirmou', '').strip().lower()

        # 2. SE ELE MARCOU "NÃO", CORRIGIMOS A QUANTIDADE PARA NÃO TRAVAR O DJANGO
        if resposta_radio in ['false', 'não', 'nao', '2', '0']:
            dados_post['quantidade_vinda'] = 0  # Força 0 pessoas vindo se ele não vai

        form = RespostaConviteForm(dados_post, instance=convidado)
        
        if form.is_valid():
            form.save()
            
            valor_confirmou = form.cleaned_data.get('confirmou')
            valor_str = str(valor_confirmou).strip().lower()
            
            if valor_str in ['true', 'sim', '1', 'yes', 's']:
                status_popup = "confirmado"
            else:
                status_popup = "recusado"
                
            return render(request, 'convite/convite_form.html', {
                'form': form,
                'convidado': convidado,
                'sucesso': status_popup  
            })
        else:
            # SE O FORMULÁRIO DEU ERRO, IMPRIMIMOS NO TERMINAL PARA VOCÊ VER
            print(f"--- ERROS DO FORMULÁRIO: {form.errors.as_data()} ---")
            
    else:
        form = RespostaConviteForm(instance=convidado)
    
    return render(request, 'convite/convite_form.html', {
        'form': form,
        'convidado': convidado,
        'sucesso': status_popup  
    })
