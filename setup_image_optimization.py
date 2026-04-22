#!/usr/bin/env python
"""
Script de Setup automático para optimización de imágenes
Ejecutar: python setup_image_optimization.py
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Imprime un header formateado"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_pillow():
    """Verifica que Pillow está instalado"""
    print("🔍 Verificando dependencias...")
    try:
        from PIL import Image
        print("   ✅ Pillow está instalado")
        return True
    except ImportError:
        print("   ❌ Pillow no está instalado")
        print("   Instalando Pillow...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow>=9.0.0"])
            print("   ✅ Pillow instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("   ❌ Error al instalar Pillow")
            print("   Ejecuta manualmente: pip install Pillow")
            return False


def optimize_images():
    """Ejecuta el comando optimize_images"""
    print_header("🖼️ Optimizando Imágenes")
    
    try:
        # Cambiar a carpeta prueba
        original_dir = os.getcwd()
        prueba_dir = Path(__file__).parent / "prueba"
        
        if prueba_dir.exists():
            os.chdir(prueba_dir)
        
        # Ejecutar comando
        subprocess.check_call([
            sys.executable, "manage.py", 
            "optimize_images",
            "--quality", "80"
        ])
        
        os.chdir(original_dir)
        print("\n✅ Imágenes optimizadas correctamente")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al optimizar imágenes: {e}")
        os.chdir(original_dir)
        return False


def collectstatic():
    """Ejecuta collectstatic"""
    print_header("📦 Recopilando archivos estáticos")
    
    try:
        prueba_dir = Path(__file__).parent / "prueba"
        original_dir = os.getcwd()
        
        if prueba_dir.exists():
            os.chdir(prueba_dir)
        
        subprocess.check_call([
            sys.executable, "manage.py",
            "collectstatic",
            "--noinput",
            "--clear"
        ])
        
        os.chdir(original_dir)
        print("\n✅ Archivos estáticos recopilados")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"⚠️  collectstatic con warning: {e}")
        os.chdir(original_dir)
        return True  # No es fatal


def create_backup():
    """Crea backup de imágenes antes de optimizar"""
    print_header("💾 Creando backup")
    
    try:
        import shutil
        
        media_dir = Path(__file__).parent / "prueba" / "media"
        static_dir = Path(__file__).parent / "prueba" / "inicio" / "static"
        
        if media_dir.exists():
            backup_dir = media_dir.parent / "media_backup"
            if not backup_dir.exists():
                shutil.copytree(media_dir, backup_dir)
                print(f"✅ Backup de media creado en: {backup_dir}")
        
        if static_dir.exists():
            backup_dir = static_dir.parent / "static_backup"
            if not backup_dir.exists():
                shutil.copytree(static_dir, backup_dir)
                print(f"✅ Backup de static creado en: {backup_dir}")
        
        return True
    
    except Exception as e:
        print(f"⚠️  Warning al crear backup: {e}")
        return True  # No es fatal


def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print("  🚀 SETUP AUTOMÁTICO - OPTIMIZACIÓN DE IMÁGENES")
    print("="*60)
    
    # 1. Verificar Pillow
    if not check_pillow():
        print("\n❌ Setup cancelado: Instala Pillow manualmente")
        sys.exit(1)
    
    # 2. Crear backup
    if not create_backup():
        print("\n⚠️  Continuando sin backup...")
    
    # 3. Optimizar imágenes
    if not optimize_images():
        print("\n❌ Error al optimizar imágenes")
        sys.exit(1)
    
    # 4. Collectstatic
    if not collectstatic():
        print("\n⚠️  Error en collectstatic (no crítico)")
    
    # 5. Resumen
    print_header("✅ SETUP COMPLETADO")
    
    print("📊 Próximos pasos:")
    print("   1. Limpia caché del navegador: Ctrl+Shift+Del")
    print("   2. Recarga la página: F5")
    print("   3. F12 → Network → Verifica imágenes .webp")
    print("   4. Ejecuta PageSpeed: https://pagespeed.web.dev")
    print("")
    print("📁 Ubicaciones importantes:")
    print(f"   Media folder: {Path(__file__).parent / 'prueba' / 'media'}")
    print(f"   Static folder: {Path(__file__).parent / 'prueba' / 'inicio' / 'static'}")
    print(f"   Backup: {Path(__file__).parent / 'prueba' / 'media_backup'}")
    print("")
    print("📖 Documentación:")
    print("   - IMAGENES_GUIA_RAPIDA.md")
    print("   - OPTIMIZACION_IMAGENES.md")
    print("   - RESUMEN_IMAGENES.md")
    print("")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
