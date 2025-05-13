from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from django import forms # Adicione esta linha

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'geral' # Garante que o tipo de usuário seja 'geral'
            user.save()
            login(request, user) # Loga o usuário automaticamente após o registro
            messages.success(request, 'Registro realizado com sucesso! Você já está logado.')
            return redirect('public_event_list') # Redireciona para a lista de eventos ou dashboard
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserRegistrationForm()
        # Esconder o campo user_type ou definir seu valor padrão
        form.fields['user_type'].initial = 'geral'
        form.fields['user_type'].widget = forms.HiddenInput()


    return render(request, 'users/register.html', {'form': form, 'page_title': 'Crie sua Conta'})
