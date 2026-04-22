# Guía de Despliegue - Optimizaciones PageSpeed

## 🚀 Despliegue en Producción

### Opción 1: PythonAnywhere (Tu hosting actual)

PythonAnywhere tiene configuración especial. Para habilitar caché headers:

1. **En el archivo Web app (Configuración PythonAnywhere):**
   - Ve a: https://www.pythonanywhere.com/web_app_setup/
   - Encuentra tu aplicación Django
   - En "Virtualenv" asegúrate está configurado correctamente

2. **Agregar headers de caché vía WSGI:**

Edita tu archivo WSGI (`prueba/wsgi.py`):

```python
"""
WSGI config for prueba project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba.settings')

application = get_wsgi_application()

# Agregar middleware para caché
from django.utils.cache import patch_response_headers

def cache_middleware(environ, start_response):
    """
    Middleware para agregar headers de caché en producción
    """
    def start_response_wrapper(status, response_headers, exc_info=None):
        path = environ.get('PATH_INFO', '')
        
        # Aplicar cache a recursos estáticos y media
        if '/static/' in path or '/media/' in path:
            # Revisar si ya tiene Cache-Control
            headers_dict = dict(response_headers)
            if 'Cache-Control' not in headers_dict:
                response_headers = [
                    ('Cache-Control', 'public, max-age=2592000, immutable'),
                    ('Vary', 'Accept-Encoding'),
                ] + response_headers
        
        return start_response(status, response_headers, exc_info)
    
    return application(environ, start_response_wrapper)

# Usar cache_middleware en producción
if os.getenv('PYTHONANYWHERE_DOMAIN'):
    application = cache_middleware
```

3. **Reload en PythonAnywhere:**
   - Presiona el botón "Reload" en https://www.pythonanywhere.com/web_app_setup/

---

### Opción 2: Nginx + Gunicorn (Recomendado para producción)

#### A) Instalar dependencias
```bash
pip install gunicorn
pip install whitenoise  # Para servir estáticos eficientemente
```

#### B) Actualizar settings.py para producción
```python
# settings.py

# Seguridad
DEBUG = False
ALLOWED_HOSTS = ['angelsh.pythonanywhere.com', 'www.tudominio.com']

# WhiteNoise para estáticos optimizados
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # AGREGAR ESTO
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'prueba.middleware.CacheHeadersMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# WhiteNoise optimizaciones
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### C) Archivo de configuración Nginx

Crea `/etc/nginx/sites-available/tu-app`:

```nginx
server {
    listen 80;
    server_name angelsh.pythonanywhere.com www.tudominio.com;
    
    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name angelsh.pythonanywhere.com www.tudominio.com;
    
    ssl_certificate /ruta/to/cert.pem;
    ssl_certificate_key /ruta/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 10M;
    
    # Cache para estáticos
    location /static/ {
        alias /home/tu-usuario/proyecto-django/prueba/static/;
        expires 30d;
        add_header Cache-Control "public, immutable, max-age=2592000";
        add_header Vary "Accept-Encoding";
        
        # Compresión
        gzip on;
        gzip_types text/css application/javascript;
    }
    
    # Cache para media (imágenes)
    location /media/ {
        alias /home/tu-usuario/proyecto-django/prueba/media/;
        expires 1y;
        add_header Cache-Control "public, immutable, max-age=31536000";
        add_header Vary "Accept-Encoding";
    }
    
    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### D) Comando para ejecutar Gunicorn
```bash
gunicorn --workers 3 \
         --bind 127.0.0.1:8000 \
         --access-logfile /var/log/django/access.log \
         --error-logfile /var/log/django/error.log \
         prueba.wsgi:application
```

---

### Opción 3: Apache + mod_wsgi (Alternativa)

Si usas Apache (como algunos servers compartidos):

**Configuración .htaccess:**
```apache
# Habilitar compresión
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Cache headers para estáticos
<FilesMatch "\.(jpg|jpeg|png|gif|ico|css|js|svg|webp)$">
    Header set Cache-Control "public, max-age=2592000, immutable"
    Header set Vary "Accept-Encoding"
</FilesMatch>

# Cache de 1 año para imágenes
<FilesMatch "\.(jpg|jpeg|png|gif|webp|avif)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>

# HTTPS
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>
```

---

## ✅ Verificación Post-Despliegue

### 1. Verificar Cache Headers
```bash
# Debería retornar Cache-Control con max-age=2592000
curl -I https://angelsh.pythonanywhere.com/static/inicio/css/styles.css
curl -I https://angelsh.pythonanywhere.com/media/fotos/gato.jpeg
```

**Respuesta esperada:**
```
HTTP/2 200
Cache-Control: public, max-age=2592000, immutable
Vary: Accept-Encoding
```

### 2. Verificar HTTPS
```bash
curl -I https://fonts.googleapis.com
# Debe retornar 200 OK
```

### 3. Validar con PageSpeed
- Ir a: https://pagespeed.web.dev
- Ingresar tu URL
- Esperar análisis completo
- Verificar:
  - ✅ Cache TTL: 30 días
  - ✅ No HTTP resources
  - ✅ Imágenes con ALT
  - ✅ Accesibilidad mejorada

### 4. Probar en navegador (DevTools)
```javascript
// En consola del navegador:
// 1. Abre DevTools (F12)
// 2. Ve a Network
// 3. Recarga (F5)
// 4. Busca un CSS o JS
// 5. Verifica:
// - Size: X KiB (si es descargado)
// - Size: X KiB from cache (si está en caché)

// Para limpiar caché y probar de nuevo:
// Ctrl+Shift+Del en Chrome/Firefox (Limpiar historial > Todo el tiempo)
```

---

## 🔧 Troubleshooting

### Problema: Cache-Control header no aparece
**Solución:**
1. Verifica que middleware está en MIDDLEWARE
2. Recarga aplicación en PythonAnywhere
3. Limpia caché del navegador (Ctrl+Shift+Del)
4. Prueba en incógnito

### Problema: HTTPS redirect loop
**Solución:**
```python
# En settings.py, comenta estas líneas en desarrollo:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
```

### Problema: Estáticos no se ven (404)
**Solución:**
```bash
# Ejecuta collectstatic
python manage.py collectstatic --noinput

# Verifica ruta en settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

## 📊 Monitoreo Continuo

Después de desplegar, monitorea periódicamente:

1. **Semanal:** Ejecuta PageSpeed Insights
2. **Mensual:** Revisa logs de errores
3. **Trimestral:** Actualiza dependencias (`pip freeze`)

**Script de monitoreo automático (opcional):**
```bash
#!/bin/bash
# Archivo: monitor_pagespeed.sh

URL="https://angelsh.pythonanywhere.com"
EMAIL="tu@email.com"

# Obtener puntuación
SCORE=$(curl -s "https://pagespeed.web.dev/api/pagespeedonline/v5/runPagespeed?url=$URL" | grep -o '"score":[0-9]*' | head -1)

# Enviar alerta si < 70
if [ ${SCORE#*:} -lt 70 ]; then
    echo "⚠️ PageSpeed bajo: $SCORE" | mail -s "PageSpeed Alert" $EMAIL
fi
```

---

¡Tu aplicación está lista para producción! 🚀
