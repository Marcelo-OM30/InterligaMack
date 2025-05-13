from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('solicitante', 'Solicitante Interno'),
        ('geral', 'Usuário Geral'), # Alunos, Palestrantes, Fornecedores, Público em Geral
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='geral',
        verbose_name='Tipo de Usuário'
    )
    # Adicione outros campos específicos do perfil do usuário aqui, se necessário
    # Ex: matricula (para solicitantes internos ou alunos), departamento (para solicitantes)
    registration_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Matrícula/ID')
    department = models.CharField(max_length=200, blank=True, null=True, verbose_name='Departamento/Unidade')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
