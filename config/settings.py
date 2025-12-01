import os
from django.conf import settings

def configure_django():
    """Configura Django si no está configurado"""
    if not settings.configured:
        # Para health checks de Fly.io, permitir todas las IPs
        allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '*')
        if allowed_hosts_str == '*':
            allowed_hosts = ['*']
        else:
            allowed_hosts = allowed_hosts_str.split(',')
        
        settings.configure(
            DEBUG=os.getenv('DEBUG', 'False') == 'True',
            SECRET_KEY=os.getenv('SECRET_KEY', 'mi-clave-secreta-super-segura-CAMBIAR-EN-PRODUCCION'),
            ALLOWED_HOSTS=allowed_hosts,
            ROOT_URLCONF='config.urls',
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ['app/views/templates'],
                'APP_DIRS': False,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                    ],
                },
            }],
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': os.getenv('DB_DATABASE', 'JoseVeC'),
                    'USER': os.getenv('MYSQL_USER', 'JoseVeC'),
                    'PASSWORD': os.getenv('MYSQL_PASSWORD', 'password'),
                    'HOST': os.getenv('DB_HOST', 'mysql'),
                    'PORT': os.getenv('DB_PORT', '3306'),
                }
            },
            INSTALLED_APPS=[
                'django.contrib.sessions',
                'django.contrib.contenttypes',
                'django.contrib.staticfiles',
            ],
            SESSION_ENGINE='django.contrib.sessions.backends.db',
            USE_TZ=True,
            STATIC_URL='/static/',
            STATICFILES_DIRS=[
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static'),
            ],
        )
