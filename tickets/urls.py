# tickets/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs da Aplicação Principal
    path('', views.dashboard, name='dashboard'),
    path('novo_chamado/', views.novo_chamado, name='novo_chamado'),
    path('chamado/<int:chamado_id>/', views.detalhe_chamado, name='detalhe_chamado'),
    path('resolvidos/', views.painel_resolvidos, name='painel_resolvidos'),

    # 👇 ADICIONE A NOVA URL PARA A BUSCA GERAL 👇
    path('busca/', views.painel_busca_completa, name='painel_busca'),

    # URLs de Autenticação
    path('contas/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('contas/logout/', views.logout_view, name='logout'),
    path('contas/registrar/', views.registrar, name='registrar'),
]