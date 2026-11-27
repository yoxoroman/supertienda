# Requerimientos funcionales — Registro de ventas para Supertienda

## Gestión de datos (sitio administrativo)
- **RF-01** Registrar, consultar, editar y desactivar **clientes** (DPI de 13 dígitos, nombres, apellidos, teléfonos, email, dirección, activo).
- **RF-02** Registrar, consultar, editar y desactivar **vendedores** con los mismos datos que un cliente.
- **RF-03** Mantener un **catálogo de productos** (código, nombre, marca, presentación, costo de compra, precio de venta, activo, imagen).
- **RF-04** Registrar **ventas** (fecha y hora, vendedor, cliente) con uno o varios **detalles** (producto, cantidad, precio actual).
- **RF-05** Guardar el precio del producto al momento de la venta, aunque después cambie en el catálogo.
- **RF-06** No permitir eliminar ningún registro que esté relacionado con otro (clientes, vendedores, productos o ventas con detalles).
- **RF-07** Mostrar en la lista de ventas el total de cada venta en Quetzales, y en cada detalle su subtotal (cantidad × precio unitario).

## Roles y permisos
- **RF-08** **Supervisores:** crear, ver, editar y eliminar todos los registros.
- **RF-09** **Vendedores:**
  - Ventas: ver y crear (no editar ni eliminar).
  - Detalles de venta y clientes: ver, crear y editar (no eliminar).
  - Vendedores y comentarios: solo ver.
- **RF-10** Supervisores y vendedores deben poder generar documentos PDF tipo factura.

## Informes PDF
- **RF-11** Generar la **factura PDF de una venta**: datos del cliente, vendedor, fecha y hora, tabla de detalle (producto, cantidad, precio unitario, subtotal) y total.
- **RF-12** Generar un **informe PDF de todas las ventas seleccionadas** en la lista.

## Personalización
- **RF-13** Personalizar desde el sitio administrativo los títulos del sitio y de las páginas, y los colores de las plantillas.

## Sitio público (sin iniciar sesión)
- **RF-14** Página principal con información de la tienda y enlaces a las demás páginas y al sitio administrativo.
- **RF-15** Listado de comentarios recibidos.
- **RF-16** Formulario para enviar comentarios (fecha automática, nombre opcional, contenido).
- **RF-17** Catálogo público de productos activos (sin mostrar costos de compra).

## Usabilidad
- **RF-18** Toda la navegación se realiza mediante enlaces en forma de botones; nunca es obligatorio escribir una URL.
