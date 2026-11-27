from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from inventario.models import Producto
from personas.models import Cliente, Vendedor

from .models import DetalleVenta, Venta


class BaseTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(dpi="1234567890101", nombres="Ana", apellidos="López",
                                              telefonos="5555-1111", direccion="Zona 1")
        self.vendedor = Vendedor.objects.create(dpi="1234567890202", nombres="Luis", apellidos="Pérez",
                                                telefonos="5555-2222", direccion="Zona 2")
        self.producto = Producto.objects.create(codigo="A1", nombre="Arroz", marca="X", presentacion="1 lb",
                                                costo_compra=Decimal("3.00"), precio_venta=Decimal("5.00"))
        self.venta = Venta.objects.create(cliente=self.cliente, vendedor=self.vendedor)
        self.detalle = DetalleVenta.objects.create(venta=self.venta, producto=self.producto, cantidad=3)
        call_command("crear_roles", verbosity=0)


class ModeloTests(BaseTest):
    def test_precio_actual_y_totales(self):
        self.assertEqual(self.detalle.precio_actual, Decimal("5.00"))
        self.assertEqual(self.detalle.subtotal, Decimal("15.00"))
        self.assertEqual(self.venta.total, Decimal("15.00"))
        self.producto.precio_venta = Decimal("9.00")  # el precio histórico no cambia
        self.producto.save()
        self.detalle.refresh_from_db()
        self.assertEqual(self.detalle.precio_actual, Decimal("5.00"))

    def test_no_se_eliminan_registros_relacionados(self):
        for obj in (self.cliente, self.vendedor, self.producto, self.venta):
            with self.assertRaises(ProtectedError):
                obj.delete()


class AdminTests(BaseTest):
    def test_factura_y_informe_pdf(self):
        admin = User.objects.create_superuser("admin", password="x")
        self.client.force_login(admin)
        r = self.client.get(reverse("admin:procedimientos_venta_factura", args=[self.venta.pk]))
        self.assertEqual(r["Content-Type"], "application/pdf")
        self.assertTrue(r.content.startswith(b"%PDF"))
        r = self.client.post(reverse("admin:procedimientos_venta_changelist"),
                             {"action": "informe_pdf", "_selected_action": [self.venta.pk]})
        self.assertTrue(r.content.startswith(b"%PDF"))
        self.assertContains(self.client.get(reverse("admin:procedimientos_venta_changelist")), "Q 15.00")

    def test_permisos_vendedores(self):
        u = User.objects.create_user("vend", password="x", is_staff=True)
        u.groups.add(Group.objects.get(name="Vendedores"))
        for perm in ("procedimientos.view_venta", "procedimientos.add_venta", "procedimientos.add_detalleventa",
                     "procedimientos.change_detalleventa", "personas.change_cliente", "personas.view_vendedor",
                     "publico.view_comentario"):
            self.assertTrue(u.has_perm(perm), perm)
        for perm in ("procedimientos.change_venta", "procedimientos.delete_venta", "procedimientos.delete_detalleventa",
                     "personas.delete_cliente", "personas.add_vendedor", "personas.change_vendedor",
                     "publico.add_comentario", "publico.change_comentario"):
            self.assertFalse(u.has_perm(perm), perm)
        self.client.force_login(u)  # un vendedor también genera la factura
        r = self.client.get(reverse("admin:procedimientos_venta_factura", args=[self.venta.pk]))
        self.assertEqual(r.status_code, 200)

    def test_tema_configurable(self):
        admin = User.objects.create_superuser("admin", password="x")
        self.client.force_login(admin)
        self.assertContains(self.client.get(reverse("admin:index")), "Supertienda")


class PublicoTests(BaseTest):
    def test_paginas_publicas(self):
        for nombre in ("inicio", "catalogo", "comentarios", "comentario_nuevo"):
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)
        r = self.client.post(reverse("comentario_nuevo"), {"nombre": "", "contenido": "Excelente"}, follow=True)
        self.assertContains(r, "Anónimo")
