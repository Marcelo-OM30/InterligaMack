from django import forms
from .models import Event, EventRequest

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = [
            'event_name_proposal', # Campo para o nome proposto do evento
            'needs_sound_system', 'sound_system_details',
            'needs_photography', 'photography_details',
            'needs_support_cleaning', 'support_cleaning_details',
            'needs_recording_transmission', 'recording_transmission_details',
            'needs_journalistic_coverage', 'journalistic_coverage_details',
            'needs_maintenance', 'maintenance_details',
            'auditorium_requested', 
            'internal_notes',
            # Adicionar outros campos do EventRequest que o solicitante deve preencher
            # Por exemplo: 'requested_date_time', 'target_audience', 'event_description_proposal', etc.
            # Estes campos precisam existir no modelo EventRequest.
        ]
        widgets = {
            'sound_system_details': forms.Textarea(attrs={'rows': 2}),
            'photography_details': forms.Textarea(attrs={'rows': 2}),
            'support_cleaning_details': forms.Textarea(attrs={'rows': 2}),
            'recording_transmission_details': forms.Textarea(attrs={'rows': 2}),
            'journalistic_coverage_details': forms.Textarea(attrs={'rows': 2}),
            'maintenance_details': forms.Textarea(attrs={'rows': 2}),
            'internal_notes': forms.Textarea(attrs={'rows': 3}),
            # 'event_description_proposal': forms.Textarea(attrs={'rows': 5}), # Exemplo
            # 'requested_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), # Exemplo
        }
        labels = {
            'event_name_proposal': 'Nome Proposto para o Evento',
            # Adicionar labels amigáveis para outros campos
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        # Aplicar classes CSS aos widgets
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.PasswordInput, forms.DateInput, forms.DateTimeInput, forms.TimeInput, forms.Textarea)):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip()
            elif isinstance(widget, forms.Select):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-select'.strip()
            elif isinstance(widget, forms.CheckboxInput):
                current_class = widget.attrs.get('class', '')
                # Bootstrap 5 espera que o input esteja antes do label para .form-check-input
                # A renderização padrão do Django pode precisar de um wrapper para estilização correta de checkboxes.
                widget.attrs['class'] = f'{current_class} form-check-input'.strip()
            elif isinstance(widget, forms.ClearableFileInput):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip()
        
        # if 'requested_date_time' in self.fields: # Exemplo se você adicionar este campo
        #     self.fields['requested_date_time'].input_formats = ('%Y-%m-%dT%H:%M',)


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.requester = self.user
        if commit:
            instance.save()
        return instance


class CombinedEventRequestForm(forms.Form): # Este é um forms.Form, não ModelForm
    # Campos de Evento (que iriam para o modelo Event)
    title = forms.CharField(label='Título do Evento', max_length=200) # Corresponde a 'name' em Event
    program = forms.CharField(label='Programação (Descrição Detalhada)', widget=forms.Textarea(attrs={'rows': 5})) # Corresponde a 'long_description' em Event
    date = forms.DateTimeField(label='Data e Hora do Evento', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    # start_time e end_time não existem mais separadamente no modelo Event, 'date' é DateTimeField
    location = forms.CharField(label='Local', max_length=300)
    
    # Campos que podem ir para short_description, organizer_name, etc. em Event
    short_description_combined = forms.CharField(label='Descrição Curta do Evento', widget=forms.Textarea(attrs={'rows': 3}), required=False)
    organizer_name_combined = forms.CharField(label='Nome do Organizador/Departamento', max_length=150, required=False)
    contact_email_combined = forms.EmailField(label='E-mail de Contato do Evento', required=False)
    contact_phone_combined = forms.CharField(label='Telefone de Contato do Evento', max_length=20, required=False)
    image_combined = forms.ImageField(label='Imagem do Evento', required=False)

    # Campos de EventRequest (serviços e notas)
    needs_sound_system = forms.BooleanField(label='Necessita Sonorização?', required=False)
    sound_system_details = forms.CharField(label='Detalhes Sonorização', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    needs_photography = forms.BooleanField(label='Necessita Fotografia?', required=False)
    photography_details = forms.CharField(label='Detalhes Fotografia', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    needs_support_cleaning = forms.BooleanField(label='Necessita Apoio/Limpeza?', required=False)
    support_cleaning_details = forms.CharField(label='Detalhes Apoio/Limpeza', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    needs_recording_transmission = forms.BooleanField(label='Necessita Gravação/Transmissão?', required=False)
    recording_transmission_details = forms.CharField(label='Detalhes Gravação/Transmissão', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    needs_journalistic_coverage = forms.BooleanField(label='Necessita Cobertura Jornalística?', required=False)
    journalistic_coverage_details = forms.CharField(label='Detalhes Cobertura Jornalística', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    needs_maintenance = forms.BooleanField(label='Necessita Manutenção?', required=False)
    maintenance_details = forms.CharField(label='Detalhes Manutenção', widget=forms.Textarea(attrs={'rows':2}), required=False)
    auditorium_requested = forms.CharField(label='Auditório Solicitado', max_length=100, required=False)
    internal_notes = forms.CharField(label='Observações Internas (para equipe de cerimonial)', widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar classes CSS aos widgets
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.PasswordInput, forms.DateInput, forms.DateTimeInput, forms.TimeInput, forms.Textarea, forms.CharField)): # Adicionado CharField
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip()
            elif isinstance(widget, forms.Select):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-select'.strip()
            elif isinstance(widget, forms.CheckboxInput):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-check-input'.strip()
            elif isinstance(widget, forms.ClearableFileInput) or isinstance(widget, forms.ImageField): # Adicionado ImageField
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip() # BS5 usa form-control para file inputs

        if 'date' in self.fields: # Para o CombinedEventRequestForm
            self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)


    def clean(self):
        cleaned_data = super().clean()
        
        service_fields = {
            'needs_sound_system': 'sound_system_details',
            'needs_photography': 'photography_details',
            'needs_support_cleaning': 'support_cleaning_details',
            'needs_recording_transmission': 'recording_transmission_details',
            'needs_journalistic_coverage': 'journalistic_coverage_details',
            'needs_maintenance': 'maintenance_details',
        }

        for needs_field, details_field in service_fields.items():
            if cleaned_data.get(needs_field) and not cleaned_data.get(details_field):
                self.add_error(details_field, f'Por favor, forneça detalhes para {self.fields[needs_field].label.lower().replace("necessita ", "").replace("?", "")}.')
        
        return cleaned_data

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 
            'date', 
            'location', 
            'short_description', 
            'long_description', 
            'image', 
            'status', 
            'organizer_name', 
            'contact_email',  
            'contact_phone',
            'event_request', # Adicionado para permitir vincular a uma solicitação
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'long_description': forms.Textarea(attrs={'rows': 6}),
            # 'image' não precisa de widget customizado aqui se o __init__ cuida da classe
        }
        help_texts = {
            'name': 'O nome oficial do evento.',
            'date': 'Data e hora de início do evento.',
            'location': 'Local onde o evento ocorrerá.',
            'short_description': 'Uma breve descrição que aparecerá nas listagens (máx. 200 caracteres).',
            'long_description': 'Descrição detalhada do evento, incluindo programação, palestrantes, etc.',
            'image': 'Uma imagem promocional para o evento (opcional).',
            'status': 'Defina o status do evento (ex: Aprovado, Rascunho).',
            'organizer_name': 'Nome do responsável ou departamento organizador.',
            'contact_email': 'E-mail de contato para informações sobre o evento.',
            'contact_phone': 'Telefone de contato (opcional).',
        }
        labels = {
            'name': 'Nome do Evento',
            'date': 'Data e Hora',
            'location': 'Local',
            'short_description': 'Descrição Curta',
            'long_description': 'Descrição Detalhada',
            'image': 'Imagem do Evento',
            'status': 'Status do Evento',
            'organizer_name': 'Nome do Organizador/Departamento',
            'contact_email': 'E-mail de Contato',
            'contact_phone': 'Telefone de Contato',
            'event_request': 'Solicitação de Evento Original (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.fields:
            self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)
        
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.PasswordInput, forms.DateInput, forms.DateTimeInput, forms.TimeInput, forms.Textarea)):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip()
            elif isinstance(widget, forms.Select): # Usado para event_request (ForeignKey) e status (choices)
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-select'.strip()
            elif isinstance(widget, forms.ClearableFileInput):
                current_class = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{current_class} form-control'.strip()
