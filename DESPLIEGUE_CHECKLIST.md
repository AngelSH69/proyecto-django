# ✅ CHECKLIST DE DESPLIEGUE - PAGESPEED FINAL

## 📋 PRE-DESPLIEGUE (En tu máquina local)

- [ ] Verificar `prueba/wsgi.py` tiene CacheHeadersWSGI middleware
- [ ] Verificar `inicio/templates/inicio/encabezado.html` tiene CSS diferido
- [ ] Verificar `registros/management/commands/optimize_images.py` existe
- [ ] Hacer git commit: `git add . && git commit -m "PageSpeed optimization: cache headers, deferred CSS, image optimization"`
- [ ] Hacer git push

## 🚀 EN PYTHONANYWHERE WEB INTERFACE

**URL:** https://www.pythonanywhere.com/user/angelsh/webapps/

### Opción A: Usar Bash Console
1. [ ] Click "Consoles" → "Bash console"
2. [ ] Ejecutar:
   ```bash
   cd /home/angelsh/proyecto-django/prueba
   python manage.py collectstatic --noinput
   python manage.py optimize_images
   ```
3. [ ] Ver output: debe mostrar "Optimizadas X imágenes"

### Opción B: Consola Python
1. [ ] Click "Consoles" → "New Python 3.x console"
2. [ ] Ejecutar línea por línea:
   ```python
   import os
   os.chdir('/home/angelsh/proyecto-django/prueba')
   os.system('python manage.py collectstatic --noinput')
   os.system('python manage.py optimize_images')
   ```

## 🔄 RECARGAR WEB APP

1. [ ] Ir a "Web" en el menú
2. [ ] Click en "angelsh.pythonanywhere.com"
3. [ ] Presionar botón **[Reload angelsh.pythonanywhere.com]** (verde, arriba)
4. [ ] Esperar 2-3 minutos a que recargue completamente

## ✅ VERIFICACIÓN POST-DESPLIEGUE

### Test 1: Cache Headers
```bash
curl -I https://angelsh.pythonanywhere.com/static/inicio/css/styles.css | grep Cache-Control
```
**Resultado esperado:**
```
Cache-Control: public, max-age=2592000, immutable
```
- [ ] ✅ Si muestra arriba: PERFECTO

### Test 2: CSS cargado (sin blockers)
```bash
curl -I https://angelsh.pythonanywhere.com/static/inicio/css/bootstrap.min.css | grep Cache-Control
```
**Resultado esperado:**
```
Cache-Control: public, max-age=2592000, immutable
```
- [ ] ✅ Si muestra arriba: PERFECTO

### Test 3: Imágenes WebP
```bash
curl -I https://angelsh.pythonanywhere.com/media/fotos/usuariofoto.webp
```
**Resultado esperado:**
```
HTTP/2 200
```
(No debe mostrar 404)
- [ ] ✅ Si muestra 200: WebP se generó

### Test 4: HTML contiene CSS diferido
```bash
curl https://angelsh.pythonanywhere.com/ | grep 'media="print"'
```
**Resultado esperado:**
```
<link href="/static/inicio/css/bootstrap.min.css" rel="stylesheet" type="text/css" media="print" onload="...">
```
- [ ] ✅ Si muestra arriba: CSS está diferido

## 🌐 VERIFICAR EN PAGESPEED INSIGHTS

**URL:** https://pagespeed.web.dev/

1. [ ] Pegar: `https://angelsh.pythonanywhere.com`
2. [ ] Click "Analyze"
3. [ ] Esperar 1-2 minutos

### Resultados esperados:

#### Problema 1: Cache TTL
**Antes:** "Cache TTL: None" (rojo)
**Después:** "Cache TTL: 30 days" (verde)
- [ ] ✅ Debe mostrar "30 days"

#### Problema 2: Render Blocking
**Antes:** "440 ms" (rojo)
**Después:** "< 100 ms" (verde)
- [ ] ✅ Debe ser muchísimo menor

#### Problema 3: Image Delivery
**Antes:** "7,030 KiB" (rojo)
**Después:** "< 2,000 KiB" (verde, con WebP)
- [ ] ✅ Debe mostrar imágenes en WebP

### Performance Score
**Antes:** ~30-35
**Después:** 60-75 (estimado)
- [ ] ✅ Debe mejorar significativamente

## 🔧 TROUBLESHOOTING

### Si Cache-Control aún muestra "None"
1. [ ] Verificar que `wsgi.py` fue modificado correctamente
2. [ ] Limpiar caché del navegador: Ctrl+Shift+Del
3. [ ] Esperar 5 minutos después de reload
4. [ ] Recargar web app nuevamente

### Si CSS no carga
1. [ ] Ejecutar: `python manage.py collectstatic --noinput`
2. [ ] Recargar web app
3. [ ] Limpiar caché del navegador

### Si imágenes siguen siendo grandes
1. [ ] Verificar que `optimize_images.py` existe
2. [ ] Ejecutar: `python manage.py optimize_images`
3. [ ] Verificar que `.webp` se crearon
4. [ ] Ejecutar: `python manage.py collectstatic --noinput`
5. [ ] Recargar web app

### Si algo sigue sin funcionar
Revisar logs en PythonAnywhere:
1. [ ] Web → angelsh.pythonanywhere.com → "Server log" (abajo)
2. [ ] Buscar errores (rojo)
3. [ ] Buscar líneas que mencionen "middleware" o "cache"

## 📝 NOTAS FINALES

- Los cambios están en la rama principal
- WSGI middleware se carga automáticamente (no requiere settings.py)
- CSS diferido mantiene fallback `<noscript>` para navegadores sin JS
- Imágenes WebP tienen fallback JPEG automático en `<picture>`
- Todo es compatible con navegadores antiguos

**Estimado de mejora:**
- ✅ 3x más rápido en primera carga
- ✅ 10x más rápido en cargas recurrentes (caché)
- ✅ PageSpeed Score mejora 20-30 puntos
- ✅ SEO mejora automáticamente en Google

---

**Status:** Listo para desplegar
**Tiempo estimado:** 10-15 minutos
**Riesgo:** Mínimo (todos los cambios son compatibles hacia atrás)
