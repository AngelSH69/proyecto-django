# ⚡ COMANDOS RÁPIDOS - COPIAR Y PEGAR EN PYTHONANYWHERE

## OPCIÓN 1: Bash Console (MÁS RÁPIDO)

En PythonAnywhere, ir a **Consoles** → **Bash console** y ejecutar:

```bash
cd /home/angelsh/proyecto-django
git pull origin main
cd prueba
python manage.py collectstatic --noinput
python manage.py optimize_images
```

Luego ir a **Web** y presionar **[Reload angelsh.pythonanywhere.com]** (botón verde).

---

## OPCIÓN 2: Python Console

En PythonAnywhere, ir a **Consoles** → **New Python 3.x console** y ejecutar:

```python
import os
os.chdir('/home/angelsh/proyecto-django')
os.system('git pull origin main')
os.chdir('prueba')
os.system('python manage.py collectstatic --noinput')
os.system('python manage.py optimize_images')
```

Luego ir a **Web** y presionar **[Reload angelsh.pythonanywhere.com]** (botón verde).

---

## VERIFICACIÓN RÁPIDA

```bash
# Test 1: Cache headers
curl -I https://angelsh.pythonanywhere.com/static/inicio/css/styles.css | grep Cache-Control

# Test 2: WebP creado
curl -I https://angelsh.pythonanywhere.com/media/fotos/usuariofoto.webp | head -1

# Test 3: CSS diferido
curl https://angelsh.pythonanywhere.com/ | grep 'media="print"' | head -1
```

---

## RESULTADOS ESPERADOS

### Test 1 Output:
```
Cache-Control: public, max-age=2592000, immutable
```
✅ Si lo ves = PERFECTO

### Test 2 Output:
```
HTTP/2 200
```
✅ Si es 200 = WebP generado correctamente

### Test 3 Output:
```
<link href="/static/inicio/css/bootstrap.min.css" ... media="print" ...>
```
✅ Si ves media="print" = CSS diferido configurado

---

## SI ALGO FALLA

### Error: `git pull` no funciona
→ Tal vez necesites configurar SSH key
→ En PythonAnywhere, Web → Configuración → Repo (reinicia)

### Error: `python manage.py` no encontrado
→ Verifica que estás en `/home/angelsh/proyecto-django/prueba`
→ Comando: `cd /home/angelsh/proyecto-django/prueba && pwd`

### Error: Module not found
→ PythonAnywhere usa venv específico
→ Usa: `/home/angelsh/.virtualenvs/proyecto-django/bin/python` en lugar de `python`

### Cache-Control aún muestra "None"
→ Recargar web app nuevamente
→ Esperar 3-5 minutos
→ Limpiar caché del navegador (Ctrl+Shift+Del)

---

## TIEMPO ESTIMADO: 3-5 minutos

1. Git pull: 30 segundos
2. Collectstatic: 1-2 minutos
3. Optimize images: 1-2 minutos
4. Reload web app: 1-2 minutos

---

## ÚLTIMO PASO: Verificar en Google PageSpeed

1. Abrir: https://pagespeed.web.dev/
2. URL: `https://angelsh.pythonanywhere.com`
3. Click "Analyze"
4. Esperar 2-3 minutos

**Deberías ver:**
- ✅ Cache TTL: 30 days (verde)
- ✅ Render Blocking: < 100 ms (verde)
- ✅ Image delivery: WebP (verde)
- ✅ Performance Score: 60-75 (arriba de 50)

---

**¡Eso es todo! El deploy debería estar completado en 5-10 minutos total.**
