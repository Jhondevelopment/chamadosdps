# tickets/models.py
from django.db import models
from django.contrib.auth.models import User

class Filial(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Chamado(models.Model):
    URGENCIA_CHOICES = (
        ('B', 'Baixa'),
        ('M', 'Moderada'),
        ('A', 'Alta'),
    )
    # 👇 A ALTERAÇÃO ESTÁ NESTA LISTA 👇
    STATUS_CHOICES = (
        ('Aberto', 'Aberto'),
        ('Em Atendimento', 'Em Atendimento'),
        ('Aguardando Informação', 'Aguardando Informação'),
        ('Concluído', 'Concluído'), # Alterado aqui
        ('Fechado', 'Fechado'),
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    filial_solicitante = models.ForeignKey(Filial, on_delete=models.PROTECT, null=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    urgencia = models.CharField(max_length=1, choices=URGENCIA_CHOICES)
    numero_pc = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Aberto')
    atribuido_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados_atribuidos')

    def __str__(self):
        return f"#{self.id} - {self.titulo}"

class Comentario(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.chamado.titulo}'