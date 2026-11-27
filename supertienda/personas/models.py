from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

validar_dpi = RegexValidator(r"^\d{13}$", "El DPI debe tener exactamente 13 dígitos numéricos.")


class Persona(models.Model):
    """Datos comunes de clientes y vendedores (modelo abstracto: no crea tabla)."""

    # El DPI se guarda como texto para conservar ceros a la izquierda.
    dpi = models.CharField("DPI", max_length=13, unique=True, validators=[validar_dpi])
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefonos = models.CharField("Teléfonos", max_length=100, help_text="Separe varios números con coma.")
    email = models.EmailField("Correo electrónico", blank=True)
    direccion = models.CharField("Dirección", max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["apellidos", "nombres"]

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __str__(self):
        return f"{self.nombre_completo} ({self.dpi})"


class Cliente(Persona):
    class Meta(Persona.Meta):
        verbose_name = "cliente"
        verbose_name_plural = "clientes"


class Vendedor(Persona):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="vendedor",
        verbose_name="usuario del sistema",
        help_text="Opcional. Si se asocia, el vendedor aparece preseleccionado al crear ventas.",
    )

    class Meta(Persona.Meta):
        verbose_name = "vendedor"
        verbose_name_plural = "vendedores"
