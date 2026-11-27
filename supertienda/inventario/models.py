from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    codigo = models.CharField("Código", max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100)
    presentacion = models.CharField("Presentación", max_length=100)
    costo_compra = models.DecimalField("Costo de compra (Q)", max_digits=10, decimal_places=2,
                                       validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField("Precio de venta (Q)", max_digits=10, decimal_places=2,
                                       validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="productos/", blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.presentacion})"
