# Supertienda — Registro de ventas (Django + PostgreSQL)

## Puesta en marcha local
```bash
python -m venv venv && source venv/bin/activate     # en Windows: venv\Scripts\activate
pip install -r requirements.txt

# Crear la base en PostgreSQL:  createdb supertienda   (o desde pgAdmin)
export DATABASE_URL=postgres://yoxo:Josue123.@localhost:5432/supertienda
# En Windows (PowerShell):  $env:DATABASE_URL="postgres://USUARIO:CLAVE@localhost:5432/supertienda"

python manage.py migrate
python manage.py crear_roles          # crea los grupos Supervisores y Vendedores
python manage.py createsuperuser
python manage.py runserver
```
Sitio público: http://127.0.0.1:8000/ · Administración: http://127.0.0.1:8000/admin/

## Dar de alta al personal
1. Con el superusuario, cree usuarios en el admin, marque **Es staff** y asígnelos al grupo **Supervisores** o **Vendedores**.
2. Opcional: en el registro del vendedor, asocie su usuario para que se preseleccione en las ventas.

## Pruebas
`python manage.py test`

## Estructura
- `personas/` Clientes y Vendedores · `inventario/` Productos · `procedimientos/` Ventas, Detalles y PDF
- `publico/` Comentarios, personalización del tema y páginas públicas · `docs/` documentos del caso