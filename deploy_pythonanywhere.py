#!/usr/bin/env python
"""
Deploy script para PythonAnywhere
Ejecutar en: /home/angelsh/proyecto-django/prueba/

Pasos:
1. SSH a PythonAnywhere
2. cd /home/angelsh/proyecto-django/prueba
3. python deploy_pythonanywhere.py
"""

import os
import sys
import subprocess

print("=" * 60)
print("DEPLOY SCRIPT - PythonAnywhere")
print("=" * 60)

# Verificar que estamos en el directorio correcto
if not os.path.exists('manage.py'):
    print("ERROR: manage.py no encontrado. Ejecutar desde /home/angelsh/proyecto-django/prueba/")
    sys.exit(1)

steps = [
    ("1. Recolectar archivos estáticos", ["python", "manage.py", "collectstatic", "--noinput"]),
    ("2. Migrar cambios en BD", ["python", "manage.py", "migrate", "--run-syncdb"]),
    ("3. Optimizar imágenes a WebP", ["python", "manage.py", "optimize_images"]),
]

for step_name, cmd in steps:
    print(f"\n{step_name}...")
    print(f"$ {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("[STDERR]:", result.stderr)
        print(f"✓ {step_name} completado")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR en {step_name}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        print("\nContinuando...")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("SIGUIENTES PASOS EN PYTHONANYWHERE WEB INTERFACE:")
print("=" * 60)
print("""
1. Ir a: https://www.pythonanywhere.com/user/angelsh/webapps/
2. Hacer clic en "angelsh.pythonanywhere.com"
3. Presionar el botón [Reload angelsh.pythonanywhere.com] (arriba, botón verde)
4. Esperar 2-3 minutos a que se recargue
5. Probar: https://angelsh.pythonanywhere.com/

Verificar que los cambios están activos:
- Cache headers: curl -I https://angelsh.pythonanywhere.com/static/inicio/css/styles.css | grep Cache-Control
- Debería mostrar: Cache-Control: public, max-age=2592000, immutable
""")

print("\nDeploy completado!")
