"""
WSGI config for prueba project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba.settings')

application = get_wsgi_application()

# ========== CACHE HEADERS WSGI MIDDLEWARE ==========
# Agrega headers de caché automáticamente a todos los recursos
# Sin depender de nginx o middleware de Django

import re

class CacheHeadersWSGI:
    """Agrega Cache-Control headers para optimizar PageSpeed"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        cache_ttl = None
        
        # Determinar TTL según tipo de recurso
        if re.search(r'\.(jpg|jpeg|png|gif|webp|avif|svg)$', path, re.IGNORECASE):
            cache_ttl = 2592000  # Imágenes: 30 días
        elif re.search(r'\.(css|js)$', path, re.IGNORECASE):
            cache_ttl = 2592000  # CSS/JS: 30 días
        elif re.search(r'\.(woff|woff2|ttf|eot)$', path, re.IGNORECASE):
            cache_ttl = 31536000  # Fonts: 1 año
        
        def custom_start_response(status, response_headers, exc_info=None):
            """Wrapper para agregar cache headers"""
            if cache_ttl:
                headers_list = list(response_headers)
                
                # No sobrescribir si ya existe Cache-Control
                if not any(h[0].lower() == 'cache-control' for h in headers_list):
                    headers_list.append((
                        'Cache-Control',
                        f'public, max-age={cache_ttl}, immutable'
                    ))
                
                # Agregar Vary header
                headers_list.append(('Vary', 'Accept-Encoding'))
                response_headers = headers_list
            
            return start_response(status, response_headers, exc_info)
        
        return self.app(environ, custom_start_response)

# Aplicar middleware WSGI
application = CacheHeadersWSGI(application)
