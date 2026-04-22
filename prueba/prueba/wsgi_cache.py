# archivo: prueba/wsgi_cache.py
"""
WSGI wrapper para agregar headers de caché en PythonAnywhere
Este archivo maneja el caché directamente sin depender de middleware de Django
"""

import os
import re
from django.core.wsgi import get_wsgi_application
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba.settings')
application = get_wsgi_application()


class CacheHeadersWSGI:
    """Middleware WSGI que agrega headers de caché a todos los recursos"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        # Determinar TTL según tipo de recurso
        cache_ttl = None
        
        # Imágenes: 30 días
        if re.search(r'\.(jpg|jpeg|png|gif|webp|avif|svg)$', path, re.IGNORECASE):
            cache_ttl = 2592000  # 30 días
        
        # CSS/JS: 30 días
        elif re.search(r'\.(css|js)$', path, re.IGNORECASE):
            cache_ttl = 2592000  # 30 días
        
        # Fonts: 1 año
        elif re.search(r'\.(woff|woff2|ttf|eot|otf)$', path, re.IGNORECASE):
            cache_ttl = 31536000  # 1 año
        
        def custom_start_response(status, response_headers, exc_info=None):
            """Agregar headers de caché antes de enviar respuesta"""
            
            if cache_ttl:
                # Convertir headers a lista mutable
                headers_list = list(response_headers)
                
                # Verificar si ya existe Cache-Control
                has_cache_control = False
                for i, (header, value) in enumerate(headers_list):
                    if header.lower() == 'cache-control':
                        has_cache_control = True
                        break
                
                # Agregar Cache-Control si no existe
                if not has_cache_control:
                    headers_list.append((
                        'Cache-Control',
                        f'public, max-age={cache_ttl}, immutable'
                    ))
                
                # Agregar header Vary para gzip
                headers_list.append(('Vary', 'Accept-Encoding'))
                
                response_headers = headers_list
            
            return start_response(status, response_headers, exc_info)
        
        return self.app(environ, custom_start_response)


# Aplicar el middleware WSGI
application = CacheHeadersWSGI(application)
