# tickets/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.db.models import Q
from .models import Chamado, Filial, User, Comentario
from .forms import ChamadoForm, CustomUserCreationForm, AtualizarChamadoForm, ComentarioForm

@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    base_chamados = Chamado.objects.exclude(status='Fechado')
    if request.user.is_staff:
        chamados_visiveis = base_chamados.all()
    else:
        chamados_visiveis = base_chamados.filter(solicitante=request.user)
    if query:
        resultados_busca = chamados_visiveis.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query)
        ).distinct()
    else:
        resultados_busca = chamados_visiveis
    chamados = resultados_busca.order_by('-data_abertura')
    context = { 'chamados': chamados, 'query': query, }
    return render(request, 'tickets/dashboard.html', context)

@login_required
def novo_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.solicitante = request.user
            chamado.save()
            try:
                assunto = f'Novo Chamado Aberto: #{chamado.id} - {chamado.titulo}'
                mensagem = f"""
                Um novo chamado foi aberto.
                Solicitante: {chamado.solicitante.username}
                Filial: {chamado.filial_solicitante.nome if chamado.filial_solicitante else 'Não definida'}
                Número do PC: {chamado.numero_pc or 'Não informado'}
                Descrição: {chamado.descricao}
                Acesse a plataforma para ver mais detalhes.
                """
                remetente = 'suporte.sistema@suaempresa.com'
                destinatarios = ['equipe.suporte@suaempresa.com']
                send_mail(assunto, mensagem, remetente, destinatarios)
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")
            return redirect('dashboard')
    else:
        form = ChamadoForm()
    return render(request, 'tickets/novo_chamado.html', {'form': form})

def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registrar.html', {'form': form})
    
@login_required
def detalhe_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    comentarios = chamado.comentarios.all()
    if request.method == 'POST':
        if 'submit_atualizacao' in request.POST:
            update_form = AtualizarChamadoForm(request.POST, instance=chamado)
            if update_form.is_valid():
                update_form.save()
                return redirect('detalhe_chamado', chamado_id=chamado.id)
        elif 'submit_comentario' in request.POST:
            comment_form = ComentarioForm(request.POST)
            if comment_form.is_valid():
                novo_comentario = comment_form.save(commit=False)
                novo_comentario.chamado = chamado
                novo_comentario.autor = request.user
                novo_comentario.save()
                if request.headers.get('HX-Request'):
                    return render(request, 'partials/comentario.html', {'comentario': novo_comentario})
                return redirect('detalhe_chamado', chamado_id=chamado.id)
    update_form = AtualizarChamadoForm(instance=chamado)
    comment_form = ComentarioForm()
    context = {
        'chamado': chamado,
        'comentarios': comentarios,
        'update_form': update_form,
        'comment_form': comment_form,
    }
    return render(request, 'tickets/detalhe_chamado.html', context)

@login_required
def painel_resolvidos(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    chamados_resolvidos = Chamado.objects.filter(status='Concluído').order_by('-data_abertura')
    context = { 'chamados': chamados_resolvidos }
    return render(request, 'tickets/painel_resolvidos.html', context)

# 👇 A MUDANÇA ESTÁ APENAS NESTA FUNÇÃO 👇
@login_required
def painel_busca_completa(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    query = request.GET.get('q', '')
    
    if query:
        # Removemos o '#' para o caso de o usuário digitar #6
        query_limpo = query.lstrip('#')

        # Construímos a base da busca
        q_objects = Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(solicitante__username__icontains=query)

        # Se o que sobrou for um número, adicionamos a busca por ID
        if query_limpo.isdigit():
            q_objects |= Q(id__exact=query_limpo)
        
        resultados = Chamado.objects.filter(q_objects).distinct()
    else:
        # Se não houver busca, não mostra nada
        resultados = Chamado.objects.none() 

    context = {
        'chamados': resultados.order_by('-data_abertura'),
        'query': query,
    }
    return render(request, 'tickets/painel_busca.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')