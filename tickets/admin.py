# tickets/admin.py
from django.contrib import admin
from .models import Filial, Chamado, Comentario

admin.site.register(Filial) # Adicione esta linha de volta
admin.site.register(Chamado)
admin.site.register(Comentario)