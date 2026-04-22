"""
Django management command para optimizar imágenes
Uso: python manage.py optimize_images
"""

from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from PIL import Image
import os


class Command(BaseCommand):
    help = 'Optimiza imágenes a formato WebP para mejorar PageSpeed Insights'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=80,
            help='Calidad de compresión WebP (1-100, default: 80)'
        )
        parser.add_argument(
            '--resize',
            action='store_true',
            help='Redimensionar imágenes según su uso'
        )
        parser.add_argument(
            '--folder',
            type=str,
            default=None,
            help='Procesar solo esta carpeta (media, static, etc.)'
        )

    def handle(self, *args, **options):
        try:
            from PIL import Image
        except ImportError:
            raise CommandError(
                'Pillow no está instalado. '
                'Instala con: pip install Pillow'
            )

        quality = options['quality']
        resize = options['resize']
        folder = options['folder']

        self.stdout.write(self.style.SUCCESS(
            '\n🚀 OPTIMIZADOR DE IMÁGENES PARA PAGESPEED'
        ))
        self.stdout.write('='*60)

        # Rutas
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        media_dir = base_dir / 'media'
        static_dir = base_dir / 'inicio' / 'static'

        total_savings = 0
        converted = 0
        
        # Procesar carpetas
        if folder is None or folder == 'media':
            total_savings += self._process_directory(
                media_dir, quality, resize
            )
            converted += self._count_webp(media_dir)

        if folder is None or folder == 'static':
            total_savings += self._process_directory(
                static_dir, quality, resize
            )
            converted += self._count_webp(static_dir)

        # Resumen
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS(f'📊 Resumen:'))
        self.stdout.write(f'   Imágenes convertidas: {converted}')
        self.stdout.write(f'   Ahorro total: {total_savings/1024/1024:.1f} MB')
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\n✅ Optimización completada!\n'))

    def _process_directory(self, directory, quality, resize):
        """Procesa un directorio de imágenes"""
        
        if not directory.exists():
            self.stdout.write(self.style.WARNING(f'⚠️  {directory} no existe'))
            return 0

        self.stdout.write(f'\n📁 Procesando: {directory}')
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        images = []

        for ext in image_extensions:
            images.extend(directory.glob(f'**/*{ext}'))
            images.extend(directory.glob(f'**/*{ext.upper()}'))

        if not images:
            self.stdout.write(self.style.WARNING('⚠️  No se encontraron imágenes'))
            return 0

        total_savings = 0

        for image_path in sorted(images):
            webp_path = image_path.with_suffix('.webp')
            
            # Saltar si WebP ya existe
            if webp_path.exists():
                self.stdout.write(f'⏭️  {image_path.name} (WebP ya existe)')
                continue

            try:
                # Abrir imagen
                img = Image.open(image_path)

                # Convertir RGBA a RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(
                        img,
                        mask=img.split()[-1] if img.mode == 'RGBA' else None
                    )
                    img = background

                # Información original
                original_size = image_path.stat().st_size
                original_dims = img.size

                # Redimensionar si está especificado y es muy grande
                if resize and max(img.size) > 1200:
                    img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)

                # Guardar como WebP
                img.save(webp_path, 'WEBP', quality=quality, method=6)

                webp_size = webp_path.stat().st_size
                saving = original_size - webp_size
                percent = (saving / original_size * 100) if original_size > 0 else 0

                total_savings += saving

                self.stdout.write(f'✅ {image_path.name}')
                self.stdout.write(f'   Original: {original_size/1024:.1f} KB ({original_dims})')
                self.stdout.write(f'   WebP: {webp_size/1024:.1f} KB')
                self.stdout.write(f'   Ahorro: {saving/1024:.1f} KB ({percent:.1f}%)')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en {image_path.name}: {e}'))

        return total_savings

    def _count_webp(self, directory):
        """Cuenta archivos WebP creados"""
        if not directory.exists():
            return 0
        return len(list(directory.glob('**/*.webp')))
