"""
WSGI config for production deployment
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django manualmente
from config.settings import configure_django
configure_django()

# Obtener la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
