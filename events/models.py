from django.db import models
from django.conf import settings
from django.utils import timezone

class Speaker(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Palestrante")
    bio = models.TextField(blank=True, null=True, verbose_name="Minibiografia")
    lattes_link = models.URLField(blank=True, null=True, verbose_name="Link do Currículo Lattes")
    photo = models.ImageField(upload_to='speakers_photos/', blank=True, null=True, verbose_name="Foto")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Palestrante"
        verbose_name_plural = "Palestrantes"
        ordering = ['name']


class EventRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'solicitante'}, 
        related_name='user_event_requests', 
        verbose_name='Solicitante'
    )

    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Data da Solicitação')
    
    needs_sound_system = models.BooleanField(default=False, verbose_name='Necessita Sonorização?')
    sound_system_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Sonorização')

    needs_photography = models.BooleanField(default=False, verbose_name='Necessita Fotografia?')
    photography_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Fotografia')

    needs_support_cleaning = models.BooleanField(default=False, verbose_name='Necessita Apoio/Limpeza?')
    support_cleaning_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Apoio/Limpeza')

    needs_recording_transmission = models.BooleanField(default=False, verbose_name='Necessita Gravação/Transmissão?')
    recording_transmission_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Gravação/Transmissão')

    needs_journalistic_coverage = models.BooleanField(default=False, verbose_name='Necessita Cobertura Jornalística?')
    journalistic_coverage_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Cobertura Jornalística')

    needs_maintenance = models.BooleanField(default=False, verbose_name='Necessita Manutenção?')
    maintenance_details = models.TextField(blank=True, null=True, verbose_name='Detalhes Manutenção')

    auditorium_requested = models.CharField(max_length=100, blank=True, null=True, verbose_name='Auditório Solicitado')
    
    stream_requested = models.BooleanField(default=False, verbose_name='Solicita Transmissão pela TV Mackenzie?')
    suggested_stream_link = models.URLField(blank=True, null=True, verbose_name='Link Sugerido para Transmissão (se houver)')

    internal_notes = models.TextField(blank=True, null=True, verbose_name='Observações Internas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status da Solicitação')

    event_name_proposal = models.CharField(max_length=200, verbose_name='Nome Proposto do Evento')

    def __str__(self):
        return f"Solicitação para '{self.event_name_proposal}' por {self.requester} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Solicitação de Evento'
        verbose_name_plural = 'Solicitações de Eventos'
        ordering = ['-request_date']


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome do Evento')
    date = models.DateTimeField(verbose_name='Data e Hora do Evento')
    location = models.CharField(max_length=200, verbose_name='Local do Evento')
    
    short_description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Descrição Curta')
    long_description = models.TextField(blank=True, null=True, verbose_name='Descrição Detalhada')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True, verbose_name='Imagem do Evento')
    organizer_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nome do Organizador/Departamento')
    contact_email = models.EmailField(blank=True, null=True, verbose_name='E-mail de Contato')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone de Contato')

    program = models.TextField(blank=True, null=True, verbose_name='Programação do Evento')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Horário de Início')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Horário de Término')
    speaker_bios = models.TextField(blank=True, null=True, verbose_name='Biografia dos Palestrantes (texto)') # Se for usar o ManyToMany com Speaker, este pode ser redundante ou para um resumo.
    invitation_details = models.TextField(blank=True, null=True, verbose_name='Detalhes do Convite')
    devotional_text = models.TextField(blank=True, null=True, verbose_name='Texto Devocional')
    event_request = models.OneToOneField(
        EventRequest, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_event',
        verbose_name='Solicitação de Evento Original (se houver)'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_events',
        verbose_name='Criado Por'
    )
    
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft', 
        verbose_name='Status do Evento'
    )
    
    stream_link = models.URLField(blank=True, null=True, verbose_name="Link da Transmissão (TV Mackenzie)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    imagem_destaque = models.ImageField(
        upload_to='eventos_destaques/',  
        blank=True,                     
        null=True                       
    )

    speakers = models.ManyToManyField(Speaker, blank=True, related_name="events", verbose_name="Palestrantes")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
