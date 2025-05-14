from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', help_text='Obrigatório. Um email válido para notificações.')
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
        
        # Definir etiquetas em português para campos herdados do UserCreationForm
        if 'username' in self.fields:
            self.fields['username'].label = 'Nome de usuário'
            # Você pode também ajustar o help_text aqui se necessário, por exemplo:
            # self.fields['username'].help_text = 'Um nome de usuário único para acesso ao sistema.'
        
        if 'password1' in self.fields:
            self.fields['password1'].label = 'Senha'
            # O help_text padrão do password1 é útil, então geralmente não o removemos
            # a menos que queiramos fornecer instruções personalizadas.
            # Exemplo: self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres...'

        if 'password2' in self.fields:
            self.fields['password2'].label = 'Confirmação de senha'
            # self.fields['password2'].help_text = 'Repita a senha informada anteriormente.'

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
