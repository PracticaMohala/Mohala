import os
import dj_database_url
from pathlib import Path

# Carpeta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# La clave secreta se leerá desde Railway
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-yw8ipn#h#l*3rau(91-_*@hou*2ra=wkota3mriwczp8pupd=i')

# DEBUG: En Railway será False, en tu PC será True si creas la variable
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Permitir que el dominio de Railway y localhost funcionen
ALLOWED_HOSTS = ['*']

# --- CONFIGURACIÓN DE SEGURIDAD PARA RAILWAY ---
# Esto soluciona el error 403 que te daba al entrar al admin
CSRF_TRUSTED_ORIGINS = [
    'https://*.up.railway.app',
    'https://mohala-production.up.railway.app' # Cambia esto por tu URL real de Railway si es distinta
]

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuestionario',  # Tu app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Sistema_Mohala.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
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

WSGI_APPLICATION = 'Sistema_Mohala.wsgi.application'

# BASE DE DATOS: Configuración automática para Railway
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de idioma y hora
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES) ---
STATIC_URL = '/static/'

# Esto evita el warning si la carpeta no existe aún
STATICFILES_DIRS = []
STATIC_DIR = os.path.join(BASE_DIR, 'static')
if os.path.exists(STATIC_DIR):
    STATICFILES_DIRS.append(STATIC_DIR)

# ROOT es donde WhiteNoise guardará todo para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Almacenamiento optimizado para Railway (WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Tipo de campo por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'