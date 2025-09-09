# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Aponta todas as outras requisições para o arquivo urls.py do nosso app 'tickets'
    path('', include('tickets.urls')),
]