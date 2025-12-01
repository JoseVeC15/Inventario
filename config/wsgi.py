"""
WSGI config for production deployment
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Configurar Django antes de obtener la aplicación
from config.settings import configure_django
configure_django()

application = get_wsgi_application()
