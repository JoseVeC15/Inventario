#!/usr/bin/env python
"""Script para recolectar archivos estáticos"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
from config.settings import configure_django
configure_django()

# Importar y ejecutar collectstatic
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
