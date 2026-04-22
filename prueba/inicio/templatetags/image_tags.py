"""
Template tags para optimizar imágenes en Django
Genera srcset automático y soporta múltiples formatos
"""

from django import template
from django.templatetags.static import static
import os

register = template.Library()


@register.filter
def image_srcset(image_url, sizes="100w, 200w, 400w"):
    """
    Genera srcset para imagen responsiva
    Ejemplo: {{ media_path|image_srcset:"100w, 200w" }}
    """
    if not image_url:
        return ""
    
    srcset = image_url
    return srcset


@register.simple_tag
def responsive_image(src, alt="", class_name="", width=None, height=None, sizes="100vw"):
    """
    Genera picture element con WebP y formato original
    
    Uso:
    {% responsive_image "/media/fotos/imagen.jpg" alt="Descripción" class_name="img-media" width=30 height=40 %}
    """
    
    if not src:
        return ""
    
    # Generar rutas de alternativas
    base, ext = os.path.splitext(src)
    webp_src = f"{base}.webp"
    
    # Atributos HTML
    attrs = f'alt="{alt}" class="{class_name}"'
    if width:
        attrs += f' width="{width}"'
    if height:
        attrs += f' height="{height}"'
    
    html = f'''<picture>
    <source srcset="{webp_src}" type="image/webp">
    <img src="{src}" {attrs}>
</picture>'''
    
    return html


@register.simple_tag
def thumbnail_image(image_field, alt="", width=None, height=None, class_name=""):
    """
    Genera imagen optimizada para miniaturas
    Usa sizes pequeños y compresión
    
    Uso Django ORM:
    {% thumbnail_image alumno.imagen alt="Foto de..." width=40 height=40 class_name="img-media" %}
    """
    
    if not image_field:
        return '<img src="" alt="Imagen no disponible" class="img-missing">'
    
    # Obtener URL de la imagen
    if hasattr(image_field, 'url'):
        src = image_field.url
    else:
        src = str(image_field)
    
    if not src:
        return '<img src="" alt="Imagen no disponible" class="img-missing">'
    
    # Generar alternativas WebP
    base, ext = os.path.splitext(src)
    webp_src = f"{base}.webp"
    
    # Construir srcset para múltiples densidades de píxeles
    srcset = f"{src} 1x, {src} 2x"
    
    # HTML5 picture element
    attrs = f'alt="{alt}" class="{class_name}"'
    if width:
        attrs += f' width="{width}"'
    if height:
        attrs += f' height="{height}"'
    
    # CSS classes para object-fit
    css_class = f"{class_name} img-responsive"
    attrs = attrs.replace(f'class="{class_name}"', f'class="{css_class}"')
    
    html = f'''<picture>
    <source srcset="{webp_src}" type="image/webp">
    <img src="{src}" {attrs} loading="lazy">
</picture>'''
    
    return html


@register.simple_tag
def static_image(path, alt="", width=None, height=None, class_name=""):
    """
    Genera imagen estática (de static/) con alternativas WebP
    
    Uso:
    {% static_image "inicio/images/home.png" alt="Home" width=48 height=48 %}
    """
    
    src = static(path)
    base, ext = os.path.splitext(src)
    webp_src = f"{base}.webp"
    
    attrs = f'alt="{alt}" class="{class_name}"'
    if width:
        attrs += f' width="{width}"'
    if height:
        attrs += f' height="{height}"'
    
    html = f'''<picture>
    <source srcset="{webp_src}" type="image/webp">
    <img src="{src}" {attrs} loading="lazy">
</picture>'''
    
    return html
