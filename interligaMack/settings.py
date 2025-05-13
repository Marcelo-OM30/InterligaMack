from pathlib import Path
import os # Certifique-se que 'os' está importado

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key' # Substitua por uma chave segura em produção

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Deve vir antes de django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Meus Apps
    'users.apps.UsersConfig',
    'events.apps.EventsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interligaMack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Opcional: diretório de templates globais
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'interligaMack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/' # URL para servir arquivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Diretórios onde o Django procurará arquivos estáticos adicionais
]
# Diretório para onde o collectstatic copiará todos os arquivos estáticos para deploy
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected') 


# Media files (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.UserProfile'

# Redirecionamentos de Login e Logout
LOGIN_URL = 'users:login'  # Supondo que sua URL de login se chama 'login' no app 'users'
LOGIN_REDIRECT_URL = 'home' # Para onde ir após o login bem-sucedido
LOGOUT_REDIRECT_URL = 'home' # Para onde ir após o logout bem-sucedido


# Configurações do Django Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Interliga Mack Admin",
    "site_header": "Interliga Mack",
    "site_logo": "images/logo-vermelho-mack.png",
    "login_logo": "images/logo-vermelho-mack.png",
    "site_icon": "images/logo-vermelho-mack.png",
    "welcome_sign": "Bem-vindo ao Admin Interliga Mack",
    "copyright": "Mackenzie",
    "theme": "flatly",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "users.UserProfile": "fas fa-user",
        "auth.Group": "fas fa-users",
        "events.Event": "fas fa-calendar-alt",
        "events.EventRequest": "fas fa-clipboard-list",
        # O ícone para o link customizado será pego da definição do link abaixo
    },
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "custom_css": "css/custom_admin.css",

    # "topmenu_links": [
    #     {"name": "Ver Site Público", "url": "home", "new_window": True},
    # ],

    "custom_links": {
        # Tentaremos adicionar o link dentro do grupo 'events'
        # O nome 'events' aqui deve corresponder ao app_label do seu app 'events'
        "events": [
            {
                "name": "Ver Site Público",
                "url": "home",
                "icon": "fas fa-globe",
                "new_window": True,
                # "permissions": [] 
            }
        ]
    },

    # Definindo a ordem dos apps no menu lateral explicitamente
    # Certifique-se de que 'users' e 'events' são os app_labels corretos
    # dos seus aplicativos. 'auth' é para o app de autenticação do Django.
    "order_with_respect_to": ["auth", "users", "events"],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly", 
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
