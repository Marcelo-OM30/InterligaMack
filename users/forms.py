from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Obrigatório. Um email válido para notificações.')
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=150, required=True, label='Sobrenome')
    # registration_id = forms.CharField(max_length=100, required=False, label='Matrícula/ID (Opcional)')

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'user_type') # 'registration_id'
        # Definir user_type como 'geral' por padrão para registros públicos
        # Isso pode ser feito na view ou no form, se não quisermos que o usuário escolha.
        # Por segurança, é melhor definir na view.

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Não permitir que o usuário defina o tipo de usuário no formulário de registro público
        if 'user_type' in self.fields:
            self.fields['user_type'].widget = forms.HiddenInput()
            self.fields['user_type'].initial = 'geral'
        
        # Exemplo: Remover o help_text do campo username
        # self.fields['username'].help_text = None 
        
        # Exemplo: Alterar o help_text do campo username
        # self.fields['username'].help_text = 'Escolha um nome de usuário único.'

        # Exemplo: Remover o help_text (lista de requisitos) do campo password1
        # CUIDADO: Remover isso não é recomendado para UX, pois o usuário não saberá as regras da senha.
        # self.fields['password1'].help_text = None
