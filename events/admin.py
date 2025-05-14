from django.contrib import admin
from .models import Event, EventRequest, Speaker

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lattes_link')
    search_fields = ('name', 'bio')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'status', 'created_by', 'event_request') # Adicionado event_request
    list_filter = ('date', 'status', 'speakers')
    search_fields = ('name', 'long_description', 'location', 'speakers__name')
    filter_horizontal = ('speakers',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'short_description', 'long_description', 'imagem_destaque', 'image')
        }),
        ('Data e Local', {
            'fields': ('date', 'location') 
        }),
        ('Palestrantes', { 
            'fields': ('speakers',)
        }),
        ('Detalhes Adicionais e Controle', {
            'fields': ('organizer_name', 'contact_email', 'contact_phone', 'status', 
                       'stream_link', # Adicionado stream_link
                       'created_by', 'event_request')
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'event_request')

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('event_name_proposal', 'requester', 'request_date', 'status', 'created_at') 
    list_filter = ('status', 'request_date')
    search_fields = ('event_name_proposal', 'requester__username', 'internal_notes') 
    readonly_fields = ('created_at', 'updated_at', 'requester', 'request_date')
    actions = ['approve_requests', 'reject_requests']

    fieldsets = (
        ('Detalhes da Solicitação', {
            'fields': (
                'event_name_proposal', 
                'requester', 
                'request_date', 
                'auditorium_requested',
                'stream_requested', # Adicionado
                'suggested_stream_link', # Adicionado
            )
        }),
        ('Necessidades Específicas (Detalhes)', {
            'classes': ('collapse',), 
            'fields': (
                'needs_sound_system', 'sound_system_details',
                'needs_photography', 'photography_details',
                'needs_support_cleaning', 'support_cleaning_details',
                'needs_recording_transmission', 'recording_transmission_details',
                'needs_journalistic_coverage', 'journalistic_coverage_details',
                'needs_maintenance', 'maintenance_details',
            )
        }),
        ('Status e Observações Internas', {
            'fields': ('status', 'internal_notes') 
        }),
    )

    def approve_requests(self, request, queryset):
        for event_request_obj in queryset:
            if not hasattr(event_request_obj, 'approved_event') or not event_request_obj.approved_event:
                event_data = {
                    'name': event_request_obj.event_name_proposal,
                    'created_by': event_request_obj.requester,
                    'event_request': event_request_obj, 
                    'status': 'draft', 
                }
                
                if event_request_obj.auditorium_requested:
                    event_data['location'] = event_request_obj.auditorium_requested
                
                # Adicionar link da transmissão se solicitado e sugerido
                if event_request_obj.stream_requested and event_request_obj.suggested_stream_link:
                    event_data['stream_link'] = event_request_obj.suggested_stream_link
                elif event_request_obj.stream_requested:
                    # Se solicitado mas sem link, pode-se adicionar uma nota ou deixar em branco para preenchimento manual
                    pass

                description_parts = []
                if event_request_obj.sound_system_details:
                    description_parts.append(f"Sonorização: {event_request_obj.sound_system_details}")
                if event_request_obj.photography_details:
                    description_parts.append(f"Fotografia: {event_request_obj.photography_details}")
                if event_request_obj.support_cleaning_details:
                    description_parts.append(f"Apoio/Limpeza: {event_request_obj.support_cleaning_details}")
                if event_request_obj.recording_transmission_details:
                    description_parts.append(f"Gravação/Transmissão: {event_request_obj.recording_transmission_details}")
                if event_request_obj.journalistic_coverage_details:
                    description_parts.append(f"Cobertura Jornalística: {event_request_obj.journalistic_coverage_details}")
                if event_request_obj.maintenance_details:
                    description_parts.append(f"Manutenção: {event_request_obj.maintenance_details}")
                if event_request_obj.internal_notes:
                    description_parts.append(f"\nObservações Internas da Solicitação:\n{event_request_obj.internal_notes}")
                
                if description_parts:
                    event_data['long_description'] = "\n\n".join(description_parts)

                Event.objects.create(**event_data)
            
            event_request_obj.status = 'approved'
            event_request_obj.save()
    approve_requests.short_description = "Aprovar solicitações selecionadas e criar eventos"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
    reject_requests.short_description = "Rejeitar solicitações selecionadas"
