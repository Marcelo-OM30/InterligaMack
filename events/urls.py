from django.urls import path
from . import views

app_name = 'events' # Namespace para as URLs deste app

urlpatterns = [
    path('publicos/', views.public_event_list, name='public_event_list'),
    path('eventrequest/', views.create_event_request, name='create_event_request'),
    path('minhas-solicitacoes/', views.list_my_event_requests, name='list_my_event_requests'),
    path('adicionar/', views.add_event_view, name='add_event'),
    path('<int:event_id>/', views.public_event_detail, name='public_event_detail'), # Nova URL
    # ... outras URLs específicas do app 'events'
]
