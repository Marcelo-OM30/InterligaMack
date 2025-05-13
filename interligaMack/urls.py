from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar settings
from django.conf.urls.static import static # Importar static
from events.views import public_event_list # Importar a view para a rota raiz

admin.site.site_header = "Interliga Mack"
admin.site.site_title = "Portal Admin Interliga Mack"
admin.site.index_title = "Bem-vindo ao Portal de Administração Interliga Mack"

urlpatterns = [
    path('', public_event_list, name='home'), # Rota raiz do site
    path('admin/', admin.site.urls),
    path('eventos/', include('events.urls')),
    path('contas/', include('users.urls')), # Inclui as URLs do app users
]

# Servir arquivos de mídia e estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # STATIC_ROOT é para produção
