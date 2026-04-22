#!/usr/bin/env python
"""
Script para convertir imágenes a WebP y redimensionarlas automáticamente
Mejora significativamente PageSpeed
"""

import os
import sys
from pathlib import Path
from PIL import Image
from io import BytesIO

# Configuración
MEDIA_DIR = Path(__file__).parent / 'prueba' / 'media'
STATIC_DIR = Path(__file__).parent / 'prueba' / 'inicio' / 'static'

# Dimensiones máximas por uso
SIZE_CONFIGS = {
    'user_avatar': (96, 96),        # Avatar de usuario
    'thumbnail': (80, 80),           # Miniaturas en tabla
    'medium': (400, 400),            # Imágenes medianas
    'large': (1200, 1200),           # Imágenes grandes
}

# Calidad de compresión WebP
WEBP_QUALITY = 80


def get_image_size_config(filename):
    """
    Determina la configuración de tamaño basada en el nombre o tipo de imagen
    """
    filename_lower = filename.lower()
    
    if 'avatar' in filename_lower or 'perfil' in filename_lower:
        return 'user_avatar'
    elif 'thumbnail' in filename_lower or 'thumb' in filename_lower:
        return 'thumbnail'
    elif 'thumb' in filename_lower or 'small' in filename_lower:
        return 'thumbnail'
    else:
        # Por defecto: detectar tamaño de la imagen original
        return None


def convert_to_webp(image_path, max_size=None):
    """
    Convierte imagen a WebP con compresión y redimensionamiento
    
    Args:
        image_path: Ruta de la imagen original
        max_size: Tupla (width, height) para redimensionar
    
    Returns:
        Ruta del archivo WebP creado
    """
    
    image_path = Path(image_path)
    
    if not image_path.exists():
        print(f"❌ Archivo no existe: {image_path}")
        return None
    
    # Abrir imagen
    try:
        img = Image.open(image_path)
        
        # Convertir RGBA a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Redimensionar si es necesario
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Crear ruta de salida WebP
        webp_path = image_path.with_suffix('.webp')
        
        # Guardar como WebP con compresión
        img.save(
            webp_path,
            'WEBP',
            quality=WEBP_QUALITY,
            method=6  # Método 6 = máxima compresión
        )
        
        # Obtener información de ahorro
        original_size = image_path.stat().st_size
        webp_size = webp_path.stat().st_size
        saving = original_size - webp_size
        percent = (saving / original_size * 100) if original_size > 0 else 0
        
        print(f"✅ {image_path.name}")
        print(f"   Original: {original_size/1024:.1f} KB")
        print(f"   WebP: {webp_size/1024:.1f} KB")
        print(f"   Ahorrado: {saving/1024:.1f} KB ({percent:.1f}%)")
        
        return webp_path
    
    except Exception as e:
        print(f"❌ Error procesando {image_path}: {e}")
        return None


def optimize_images_in_directory(directory, pattern="*.{jpg,jpeg,png,gif}", max_size=None):
    """
    Optimiza todas las imágenes en un directorio
    """
    
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ Directorio no existe: {directory}")
        return
    
    print(f"\n📁 Procesando: {directory}")
    print(f"{'='*60}")
    
    # Buscar archivos de imagen
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    images = []
    
    for ext in image_extensions:
        images.extend(directory.glob(f'**/*{ext}'))
        images.extend(directory.glob(f'**/*{ext.upper()}'))
    
    if not images:
        print("⚠️  No se encontraron imágenes")
        return
    
    total_savings = 0
    converted = 0
    
    for image_path in images:
        # Saltar si ya existe el WebP
        webp_path = image_path.with_suffix('.webp')
        if webp_path.exists():
            print(f"⏭️  {image_path.name} (WebP ya existe)")
            continue
        
        result = convert_to_webp(image_path, max_size)
        if result:
            converted += 1
            webp_size = result.stat().st_size
            original_size = image_path.stat().st_size
            total_savings += (original_size - webp_size)
    
    print(f"\n{'='*60}")
    print(f"📊 Resumen:")
    print(f"   Imágenes convertidas: {converted}")
    print(f"   Ahorro total: {total_savings/1024/1024:.1f} MB")
    print(f"{'='*60}\n")


def optimize_media_folder():
    """
    Optimiza todas las imágenes en la carpeta media/
    """
    print("\n🖼️  OPTIMIZANDO CARPETA MEDIA")
    print("="*60)
    
    media_fotos = MEDIA_DIR / 'fotos'
    if media_fotos.exists():
        optimize_images_in_directory(media_fotos)
    
    media_archivos = MEDIA_DIR / 'archivos'
    if media_archivos.exists():
        optimize_images_in_directory(media_archivos)


def optimize_static_folder():
    """
    Optimiza todas las imágenes en la carpeta static/
    """
    print("\n🎨 OPTIMIZANDO CARPETA STATIC")
    print("="*60)
    
    static_images = STATIC_DIR / 'inicio' / 'images'
    if static_images.exists():
        optimize_images_in_directory(static_images)


def main():
    """
    Función principal
    """
    print("\n" + "="*60)
    print("🚀 OPTIMIZADOR DE IMÁGENES PARA PAGESPEED")
    print("="*60)
    
    # Verificar que PIL está instalado
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow no está instalado")
        print("   Instala con: pip install Pillow")
        sys.exit(1)
    
    # Optimizar folders
    optimize_media_folder()
    optimize_static_folder()
    
    print("\n✅ Optimización completada!")
    print("\n📝 Notas:")
    print("   1. Se crearon archivos .webp para cada imagen")
    print("   2. Los navegadores modernos cargarán WebP automáticamente")
    print("   3. Los navegadores antiguos usan la imagen original como fallback")
    print("   4. Ejecuta collectstatic después de optimizar:")
    print("      python manage.py collectstatic --noinput")


if __name__ == '__main__':
    main()
