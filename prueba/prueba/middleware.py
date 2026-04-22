"""
Middleware personalizado para optimizar PageSpeed Insights
Agrega headers de caché a recursos estáticos y medias
"""

from django.utils.decorators import decorator_from_middleware
from django.utils.cache import patch_response_headers


class CacheHeadersMiddleware:
    """
    Middleware que agrega headers de caché para mejorar PageSpeed.
    - Estáticos: 30 días (2592000 segundos)
    - Media: 30 días (2592000 segundos)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Aplicar cache headers a recursos estáticos y media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            # Cache por 30 días para imágenes, CSS, JS
            patch_response_headers(
                response,
                cache_timeout=2592000  # 30 días en segundos
            )
            
            # Agregar headers explícitos de caché
            response['Cache-Control'] = 'public, max-age=2592000, immutable'
            response['ETag'] = request.path  # Para validar en el navegador
        
        return response
