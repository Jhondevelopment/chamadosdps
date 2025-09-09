# tickets/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Chamado, User, Comentario

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao', 'numero_pc', 'urgencia', 'filial_solicitante']
        labels = {
            'titulo': _('Título'),
            'descricao': _('Descrição Detalhada'),
            'numero_pc': _('Número do PC'),
            'urgencia': _('Nível de Urgência'),
            'filial_solicitante': _('Filial'),
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'numero_pc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: TI-PC-0123'}),
            'urgencia': forms.Select(attrs={'class': 'form-select'}),
            'filial_solicitante': forms.Select(attrs={'class': 'form-select'}),
        }

# 👇 A MUDANÇA ESTÁ NESTA CLASSE 👇
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

        # Adicionamos este dicionário para personalizar o texto de ajuda
        help_texts = {
            'username': _('*Obrigatório. Apenas coloque seu nome + Primeira letra do sobrenome ex: CarlosP.'),
        }

class AtualizarChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['status', 'atribuido_a']
        labels = {
            'status': _('Status'),
            'atribuido_a': _('Atribuído a'),
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'atribuido_a': forms.Select(attrs={'class': 'form-select'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': _('Adicionar um Comentário'),
        }
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Digite seu comentário aqui...'}),
        }