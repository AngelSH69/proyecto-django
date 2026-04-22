# 🎬 GUÍA VISUAL DE DESPLIEGUE - PASO A PASO

## PASO 1: Git Push (en tu máquina)

```bash
cd c:\Users\Angel\proyectos\proyecto-django

# Ver cambios realizados
git status

# Agregar todos los cambios
git add .

# Commit
git commit -m "🚀 PageSpeed optimization final: cache headers, deferred CSS, image optimization"

# Push a GitHub
git push origin main
```

**Verificar:** En GitHub, deberías ver los nuevos commits en tu rama.

---

## PASO 2: Login en PythonAnywhere

1. Abrir: https://www.pythonanywhere.com
2. Click "Login"
3. Usuario: `angelsh`
4. Contraseña: [tu contraseña]

---

## PASO 3: Git Pull en PythonAnywhere

### Opción A: Bash Console (MÁS RÁPIDO)

1. En PythonAnywhere, ir a **"Consoles"** en menú superior
2. Click **"Bash console"** (o crear nuevo)
3. Ejecutar:
   ```bash
   cd /home/angelsh/proyecto-django
   git pull origin main
   ```
4. Debe mostrar: `Already up to date.` o `Fast-forward ...`

### Opción B: Web Interface
1. Dashboard → Click en tu proyecto
2. Buscar sección "Source code"
3. Click "Reload source from git"
4. Esperar a que complete

---

## PASO 4: Ejecutar Django Management Commands

**En Bash console:**

```bash
cd /home/angelsh/proyecto-django/prueba

# Recolectar archivos estáticos (CSS, JS, imágenes)
python manage.py collectstatic --noinput

# Optimizar imágenes a WebP
python manage.py optimize_images
```

**Salida esperada:**
```
132 static files copied to '/home/angelsh/proyecto-django/prueba/prueba/static'

Optimizando imágenes...
Procesadas 4 imágenes
- usuariofoto.avif → usuariofoto.webp (450 KB → 45 KB) ✓
Total ahorrado: 3.8 MB
```

---

## PASO 5: Recargar Web App

1. En PythonAnywhere, ir a **"Web"** en menú
2. Click en **"angelsh.pythonanywhere.com"**
3. PRESIONAR BOTÓN **[Reload angelsh.pythonanywhere.com]** (verde, arriba)
4. Esperar 2-3 minutos (muestra "Reloading...")

**Nota:** Esto reinicia el servidor con los cambios nuevos.

---

## PASO 6: Pruebas de Verificación

### Test en Bash Console:

```bash
# Test 1: Verificar Cache-Control header
curl -I https://angelsh.pythonanywhere.com/static/inicio/css/styles.css 2>/dev/null | grep -i cache-control

# Test 2: Verificar WebP existe
curl -I https://angelsh.pythonanywhere.com/media/fotos/usuariofoto.webp 2>/dev/null | head -1

# Test 3: Verificar CSS diferido en HTML
curl https://angelsh.pythonanywhere.com/static/inicio/ 2>/dev/null | grep 'media="print"' | head -1
```

**Resultados esperados:**

Test 1:
```
Cache-Control: public, max-age=2592000, immutable
```

Test 2:
```
HTTP/2 200
```

Test 3:
```
<link href="/static/inicio/css/bootstrap.min.css" ... media="print" ...>
```

---

## PASO 7: Google PageSpeed Insights

1. Abrir: https://pagespeed.web.dev/
2. Pegar URL: `https://angelsh.pythonanywhere.com`
3. Click **"Analyze"** (o Enter)
4. Esperar 2-3 minutos

### Resultados esperados:

**Problema 1: Cache TTL**
- ✅ Debe mostrar 30 días (verde)

**Problema 2: Render Blocking**
- ✅ Debe mostrar < 100 ms (verde)

**Problema 3: Image Delivery**
- ✅ Debe mostrar imágenes en WebP (verde)

---

## PASO 8: Verificar Performance Score

En PageSpeed Insights, scroll arriba:

**Antes:** ~30-35
**Después:** 60-75

Si ves mejora ≥ 20 puntos → ¡ÉXITO! 🎉

---

## 📊 COMPARATIVA ANTES/DESPUÉS

### Antes:
```
Cache TTL: None (rojo)           ❌
Render blocking: 440 ms (rojo)   ❌
Image delivery: 7,030 KiB (rojo) ❌
Performance score: 30-35         ❌
```

### Después:
```
Cache TTL: 30 days (verde)       ✅
Render blocking: < 100 ms (verde) ✅
Image delivery: < 2 MB (verde)   ✅
Performance score: 60-75         ✅
```

---

## 🆘 SI ALGO NO FUNCIONA

### Cache headers sigue en "None"
**Solución:**
```bash
# Verificar que wsgi.py tiene el middleware
cat /home/angelsh/proyecto-django/prueba/prueba/wsgi.py | grep -A 5 "CacheHeadersWSGI"

# Si no aparece, copiar wsgi.py nuevamente
# Recargar web app
```

### Imágenes siguen siendo grandes
**Solución:**
```bash
# Verificar que optimize_images.py existe
ls /home/angelsh/proyecto-django/prueba/registros/management/commands/

# Si no existe, crear desde:
# prueba/registros/management/commands/optimize_images.py

# Ejecutar nuevamente
cd /home/angelsh/proyecto-django/prueba
python manage.py optimize_images
```

### CSS no carga
**Solución:**
```bash
# Recolectar static files
cd /home/angelsh/proyecto-django/prueba
python manage.py collectstatic --noinput

# Recargar web app desde PythonAnywhere Web interface
```

### Ver logs de error
En PythonAnywhere:
1. Web → angelsh.pythonanywhere.com
2. Scroll abajo → "Server log" o "Error log"
3. Buscar línea con "ERROR" en rojo

---

## ⏱️ TIEMPO ESTIMADO

- Paso 1-2 (Git): **2 min**
- Paso 3 (Git pull): **1 min**
- Paso 4 (Commands): **3-5 min**
- Paso 5 (Reload): **2-3 min**
- Paso 6 (Tests): **1 min**
- Paso 7 (PageSpeed): **3-5 min**
- **Total: 12-17 minutos**

---

## ✅ CHECKLIST FINAL

- [ ] Git push completado
- [ ] Git pull en PythonAnywhere completado
- [ ] `collectstatic` ejecutado
- [ ] `optimize_images` ejecutado
- [ ] Web app reloaded
- [ ] Cache header test: OK
- [ ] WebP test: OK
- [ ] CSS diferido test: OK
- [ ] PageSpeed Insights: analizado
- [ ] Performance score mejoró ≥ 20 puntos
- [ ] Sin errores en server log

**Si todo está checkado: ¡DESPLIEGUE EXITOSO! 🎉**

---

**Última actualización:** 2026-04-22
**Versión:** Final
**Status:** Listo para ejecutar
