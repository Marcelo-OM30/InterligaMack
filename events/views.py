from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CombinedEventRequestForm # Se você ainda usa este form
from .models import Event, EventRequest
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .forms import EventForm

def is_solicitante(user):
    return user.is_authenticated and user.user_type == 'solicitante'

@login_required
@user_passes_test(is_solicitante, login_url='/admin/login/') # Redireciona para login se não for solicitante
def create_event_request(request):
    if request.method == 'POST':
        form = CombinedEventRequestForm(request.POST)
        if form.is_valid():
            # Criar o objeto Event
            event = Event.objects.create(
                title=form.cleaned_data['title'],
                program=form.cleaned_data['program'],
                date=form.cleaned_data['date'],
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                location=form.cleaned_data['location'],
                speaker_bios=form.cleaned_data['speaker_bios'],
                invitation_details=form.cleaned_data['invitation_details'],
                devotional_text=form.cleaned_data['devotional_text']
            )

            # Criar o objeto EventRequest
            EventRequest.objects.create(
                requester=request.user,
                event=event,
                needs_sound_system=form.cleaned_data['needs_sound_system'],
                sound_system_details=form.cleaned_data['sound_system_details'],
                needs_photography=form.cleaned_data['needs_photography'],
                photography_details=form.cleaned_data['photography_details'],
                needs_support_cleaning=form.cleaned_data['needs_support_cleaning'],
                support_cleaning_details=form.cleaned_data['support_cleaning_details'],
                needs_recording_transmission=form.cleaned_data['needs_recording_transmission'],
                recording_transmission_details=form.cleaned_data['recording_transmission_details'],
                needs_journalistic_coverage=form.cleaned_data['needs_journalistic_coverage'],
                journalistic_coverage_details=form.cleaned_data['journalistic_coverage_details'],
                needs_maintenance=form.cleaned_data['needs_maintenance'],
                maintenance_details=form.cleaned_data['maintenance_details'],
                auditorium_requested=form.cleaned_data['auditorium_requested'],
                internal_notes=form.cleaned_data['internal_notes']
                # status é 'pending' por padrão
            )
            messages.success(request, 'Sua solicitação de evento foi enviada com sucesso!')
            # Redirecionar para uma página de sucesso ou lista de solicitações
            return redirect('list_my_event_requests') # Precisaremos criar esta URL e view
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CombinedEventRequestForm()

    return render(request, 'events/create_event_request.html', {'form': form, 'page_title': 'Solicitar Cerimonial de Evento'})

@login_required
@user_passes_test(is_solicitante, login_url='/admin/login/')
def list_my_event_requests(request):
    # Esta view listará as solicitações do usuário logado.
    # Implementação futura.
    event_requests = EventRequest.objects.filter(requester=request.user).order_by('-request_date')
    return render(request, 'events/list_my_event_requests.html', {'event_requests': event_requests, 'page_title': 'Minhas Solicitações de Evento'})

@login_required
@user_passes_test(is_solicitante, login_url='/admin/login/')
def event_request_detail(request, request_id):
    event_request = get_object_or_404(EventRequest, id=request_id, requester=request.user)
    # Garante que o usuário só pode ver suas próprias solicitações
    return render(request, 'events/event_request_detail.html', {'event_request': event_request, 'page_title': f'Detalhes da Solicitação: {event_request.event.title}'})

def public_event_list(request):
    """
    View para listar eventos publicados e futuros para o público.
    """
    now = timezone.now()
    # Filtra eventos que estão publicados E cuja data é futura ou hoje
    events = Event.objects.filter(
        status='published', 
        date__gte=now
    ).order_by('date') # Ordena pelos mais próximos primeiro

    context = {
        'events': events,
        'page_title': 'Eventos' # ALTERADO DE "Próximos Eventos" PARA "Eventos"
    }
    # Usaremos um novo template para esta lista pública
    return render(request, 'events/public_event_list.html', context)

@staff_member_required # Garante que apenas staff (admin) possa acessar
def add_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user # Associa o evento ao usuário logado
            event.save()
            form.save_m2m() # Salva as relações ManyToMany (como speakers)
            messages.success(request, 'Evento adicionado com sucesso!')
            return redirect('events:public_event_list') # Ou para uma lista de eventos no admin
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'page_title': 'Adicionar Novo Evento'
    }
    return render(request, 'events/add_event.html', context)

def public_event_detail(request, event_id):
    """
    View para exibir os detalhes de um evento público específico.
    """
    event = get_object_or_404(Event, pk=event_id, status='published')
    # Você pode adicionar mais contexto aqui se necessário (ex: eventos relacionados, comentários, etc.)
    context = {
        'event': event,
        'page_title': event.name # Título da página será o nome do evento
    }
    return render(request, 'events/public_event_detail.html', context)

# Adicionar outras views conforme necessário (detalhes da solicitação, editar, cancelar, etc.)

