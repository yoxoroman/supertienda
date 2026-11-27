from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Venta(models.Model):
    fecha_hora = models.DateTimeField("Fecha y hora", default=timezone.now)
    # PROTECT: no se puede eliminar un vendedor/cliente que aparezca en una venta.
    vendedor = models.ForeignKey("personas.Vendedor", on_delete=models.PROTECT, related_name="ventas",
                                 limit_choices_to={"activo": True})
    cliente = models.ForeignKey("personas.Cliente", on_delete=models.PROTECT, related_name="ventas",
                                limit_choices_to={"activo": True})

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    def __str__(self):
        return f"Venta #{self.pk}" if self.pk else "Venta nueva"

    @property
    def total(self):
        # all() aprovecha prefetch_related cuando existe
        return sum((d.subtotal for d in self.detalles.all()), Decimal("0.00"))


class DetalleVenta(models.Model):
    # PROTECT: una venta con detalles no puede eliminarse; un producto vendido tampoco.
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name="detalles")
    producto = models.ForeignKey("inventario.Producto", on_delete=models.PROTECT, related_name="detalles_venta",
                                 limit_choices_to={"activo": True})
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_actual = models.DecimalField(
        "Precio unitario (Q)", max_digits=10, decimal_places=2, blank=True,
        validators=[MinValueValidator(0)],
        help_text="Si se deja vacío se toma el precio de venta vigente del producto.",
    )

    class Meta:
        verbose_name = "detalle de venta"
        verbose_name_plural = "detalles de ventas"
        constraints = [
            models.UniqueConstraint(fields=["venta", "producto"], name="producto_unico_por_venta"),
        ]

    def __str__(self):
        return f"{self.venta} - {self.producto.nombre} x{self.cantidad}"

    @property
    def subtotal(self):
        return Decimal(self.cantidad or 0) * (self.precio_actual or Decimal("0"))

    def save(self, *args, **kwargs):
        # El precio queda "congelado" al momento de la venta aunque luego cambie el del producto.
        if self.precio_actual is None:
            self.precio_actual = self.producto.precio_venta
        super().save(*args, **kwargs)
