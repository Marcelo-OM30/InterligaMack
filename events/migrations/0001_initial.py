# Generated by Django 5.2 on 2025-05-07 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título do Evento')),
                ('program', models.TextField(verbose_name='Programação')),
                ('date', models.DateField(verbose_name='Data')),
                ('start_time', models.TimeField(verbose_name='Horário de Início')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='Horário de Término')),
                ('location', models.CharField(max_length=300, verbose_name='Local')),
                ('speaker_bios', models.TextField(blank=True, null=True, verbose_name='Currículos dos Palestrantes')),
                ('invitation_details', models.TextField(blank=True, null=True, verbose_name='Detalhes do Convite')),
                ('devotional_text', models.TextField(blank=True, null=True, verbose_name='Devocional')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-date', '-start_time'],
            },
        ),
        migrations.CreateModel(
            name='EventRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Data da Solicitação')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado'), ('in_progress', 'Em Andamento'), ('completed', 'Concluído'), ('cancelled', 'Cancelado')], default='pending', max_length=20, verbose_name='Status da Solicitação')),
                ('needs_sound_system', models.BooleanField(default=False, verbose_name='Necessita Sonorização?')),
                ('sound_system_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Sonorização')),
                ('needs_photography', models.BooleanField(default=False, verbose_name='Necessita Fotografia?')),
                ('photography_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Fotografia')),
                ('needs_support_cleaning', models.BooleanField(default=False, verbose_name='Necessita Apoio/Limpeza?')),
                ('support_cleaning_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Apoio/Limpeza')),
                ('needs_recording_transmission', models.BooleanField(default=False, verbose_name='Necessita Gravação/Transmissão?')),
                ('recording_transmission_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Gravação/Transmissão')),
                ('needs_journalistic_coverage', models.BooleanField(default=False, verbose_name='Necessita Cobertura Jornalística?')),
                ('journalistic_coverage_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Cobertura Jornalística')),
                ('needs_maintenance', models.BooleanField(default=False, verbose_name='Necessita Manutenção?')),
                ('maintenance_details', models.TextField(blank=True, null=True, verbose_name='Detalhes Manutenção')),
                ('auditorium_requested', models.CharField(blank=True, max_length=100, null=True, verbose_name='Auditório Solicitado')),
                ('internal_notes', models.TextField(blank=True, null=True, verbose_name='Observações Internas')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Evento Associado')),
            ],
            options={
                'verbose_name': 'Solicitação de Evento',
                'verbose_name_plural': 'Solicitações de Eventos',
                'ordering': ['-request_date'],
            },
        ),
    ]
