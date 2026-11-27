# Diagrama Entidad-Relación

**Notación elegida: pie de gallo (crow's foot).** Muestra en el mismo dibujo la cardinalidad (uno/muchos) y la opcionalidad (obligatorio/opcional) de cada relación, se traduce directamente a llaves foráneas y es la notación que usan Mermaid, dbdiagram.io y la mayoría de herramientas de modelado actuales.

```mermaid
erDiagram
    CLIENTE ||--o{ VENTA : "realiza"
    VENDEDOR ||--o{ VENTA : "registra"
    VENTA ||--|{ DETALLE_VENTA : "contiene"
    PRODUCTO ||--o{ DETALLE_VENTA : "se vende en"
    USUARIO |o--o| VENDEDOR : "se asocia a"

    CLIENTE {
        bigint id PK
        char13 dpi UK
        string nombres
        string apellidos
        string telefonos
        string email
        string direccion
        boolean activo
    }
    VENDEDOR {
        bigint id PK
        char13 dpi UK
        string nombres
        string apellidos
        string telefonos
        string email
        string direccion
        boolean activo
        bigint usuario_id FK
    }
    PRODUCTO {
        bigint id PK
        string codigo UK
        string nombre
        string marca
        string presentacion
        decimal costo_compra
        decimal precio_venta
        boolean activo
        string imagen
    }
    VENTA {
        bigint id PK
        datetime fecha_hora
        bigint vendedor_id FK
        bigint cliente_id FK
    }
    DETALLE_VENTA {
        bigint id PK
        bigint venta_id FK
        bigint producto_id FK
        int cantidad
        decimal precio_actual
    }
    COMENTARIO {
        bigint id PK
        datetime fecha
        string nombre
        text contenido
    }
```

## Notas
- `DETALLE_VENTA` resuelve la relación muchos a muchos entre `VENTA` y `PRODUCTO`; tiene restricción única (`venta`, `producto`).
- Todas las llaves foráneas usan `ON DELETE PROTECT` (Django), por lo que no se puede borrar un cliente, vendedor, producto o venta relacionados.
- `COMENTARIO` no se relaciona con otras entidades. `USUARIO` es el modelo de autenticación de Django.
- `CONFIGURACION_SITIO` (registro único con títulos y colores) tampoco se relaciona y se omite del diagrama.
