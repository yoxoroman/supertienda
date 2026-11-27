# Especificaciones técnicas

| Aspecto | Elección |
|---|---|
| 3.1 Lenguaje | Python 3.12 |
| 3.2 Marco de trabajo | Django 5.2 (incluye Django Admin) |
| 3.3 Gestor de base de datos | PostgreSQL |
| 3.4 Módulos agregados (no nativos) | `psycopg2-binary` (conexión a PostgreSQL), `Pillow` (imágenes de productos), `reportlab` (PDF), `dj-database-url` (configuración por `DATABASE_URL`), `whitenoise` (archivos estáticos), `gunicorn` (servidor WSGI) |
| 3.5 Despliegue | Render: Web Service (Python) + PostgreSQL administrado + disco persistente para imágenes |

## Justificación
- **Django:** trae panel administrativo, autenticación, grupos y permisos listos, lo que cubre casi todo el caso con poco código.
- **PostgreSQL:** gestor robusto, de código abierto y con integridad referencial estricta, útil para la regla de no eliminar registros relacionados.
- **ReportLab:** genera PDF desde Python puro, sin depender de librerías del sistema operativo (a diferencia de WeasyPrint), lo que simplifica el despliegue.
- **Render:** despliegue desde Git, HTTPS incluido y base de datos PostgreSQL administrada en la misma plataforma. Verifique el plan vigente y sus límites antes de contratar.
- **Imágenes:** se guardan en un disco persistente (`MEDIA_ROOT`). Si el plan elegido no ofrece disco, use un servicio externo de almacenamiento.

## Despliegue en Render (resumen)
1. Subir el proyecto a un repositorio Git.
2. Crear una base PostgreSQL en Render y copiar su *Internal Database URL*.
3. Crear un Web Service: *Build command* `./build.sh`, *Start command* `gunicorn config.wsgi`.
4. Variables de entorno: `DATABASE_URL`, `SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS=<su-app>.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://<su-app>.onrender.com`, `MEDIA_ROOT=/var/data/media`.
5. Agregar un disco persistente montado en `/var/data`.
6. Crear el superusuario desde la consola (*Shell*) del servicio: `python manage.py createsuperuser`.
