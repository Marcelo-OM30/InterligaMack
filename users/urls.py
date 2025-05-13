from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('registrar/', views.register, name='user_register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'page_title': 'Login'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Adicionar outras URLs de usuário aqui (perfil, etc.)
]
