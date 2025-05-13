from django.contrib import admin
from .models import Event, EventRequest

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'status', 'created_by', 'created_at') # Substituído 'title' por 'name', removido 'start_time' (agora parte de 'date')
    list_filter = ('status', 'date', 'location', 'created_by')
    search_fields = ('name', 'location', 'short_description', 'long_description', 'organizer_name')
    ordering = ('-date',)
    # raw_id_fields = ('event_request', 'created_by') # Se você tiver muitos usuários/solicitações
    
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'location', 'status')
        }),
        ('Detalhes do Evento', {
            'fields': ('short_description', 'long_description', 'image', 'organizer_name', 'contact_email', 'contact_phone')
        }),
        ('Origem e Criação', {
            'fields': ('event_request', 'created_by'),
            'classes': ('collapse',), # Opcional, para agrupar campos menos usados
        }),
    )
    readonly_fields = ('created_at', 'updated_at') # Campos que não devem ser editados diretamente

    def get_queryset(self, request):
        # Opcional: otimizar queryset
        return super().get_queryset(request).select_related('created_by', 'event_request')

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('event_name_proposal', 'requester', 'request_date', 'status', 'auditorium_requested')
    list_filter = ('status', 'request_date', 'requester', 'auditorium_requested')
    search_fields = ('event_name_proposal', 'requester__username', 'requester__email', 'auditorium_requested', 'internal_notes')
    ordering = ('-request_date',)
    # raw_id_fields = ('requester',)

    fieldsets = (
        ('Informações da Solicitação', {
            'fields': ('event_name_proposal', 'requester', 'status', 'request_date')
        }),
        ('Detalhes da Necessidade', {
            'fields': (
                'needs_sound_system', 'sound_system_details',
                'needs_photography', 'photography_details',
                'needs_support_cleaning', 'support_cleaning_details',
                'needs_recording_transmission', 'recording_transmission_details',
                'needs_journalistic_coverage', 'journalistic_coverage_details',
                'needs_maintenance', 'maintenance_details',
                'auditorium_requested',
            )
        }),
        ('Administrativo', {
            'fields': ('internal_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('request_date', 'created_at', 'updated_at')

    def approve_requests(self, request, queryset):
        created_events_count = 0
        for event_request_obj in queryset:
            if event_request_obj.status == 'pending': # Processar apenas as pendentes
                # Lógica para criar um Event a partir do EventRequest
                # Adapte os campos conforme necessário
                try:
                    event, created = Event.objects.update_or_create(
                        event_request=event_request_obj, # Para evitar duplicatas se a ação for rodada de novo
                        defaults={
                            'name': event_request_obj.event_name_proposal,
                            # 'date': event_request_obj.requested_date_time, # Se EventRequest tiver este campo
                            # 'location': event_request_obj.requested_location, # Se EventRequest tiver este campo
                            # 'short_description': event_request_obj.some_short_description_field,
                            # 'long_description': event_request_obj.some_long_description_field,
                            # 'organizer_name': event_request_obj.proposing_department, # Exemplo
                            # 'contact_email': event_request_obj.contact_email, # Exemplo
                            # 'image': event_request_obj.image_proposal, # Se EventRequest tiver imagem
                            'status': 'published', # Ou 'draft', dependendo do seu fluxo
                            'created_by': request.user, # Ou um usuário específico do cerimonial
                        }
                    )
                    if created:
                        created_events_count += 1
                    
                    event_request_obj.status = 'approved'
                    event_request_obj.save()

                except Exception as e:
                    # Lidar com possíveis erros na criação do Event
                    self.message_user(request, f"Erro ao processar solicitação ID {event_request_obj.id}: {e}", level='error')
            
            elif event_request_obj.status == 'approved':
                 self.message_user(request, f"Solicitação ID {event_request_obj.id} já está aprovada.", level='warning')
            else:
                self.message_user(request, f"Não é possível aprovar solicitação ID {event_request_obj.id} com status '{event_request_obj.get_status_display()}'.", level='warning')


        if created_events_count > 0:
            self.message_user(request, f'{created_events_count} eventos foram criados e as solicitações correspondentes aprovadas.')
        else:
            self.message_user(request, 'Nenhum novo evento foi criado. Verifique o status das solicitações ou mensagens de erro.', level='info')

    approve_requests.short_description = "Aprovar e Criar Eventos para solicitações selecionadas"

    actions = [approve_requests]
