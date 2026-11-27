from django.core.validators import RegexValidator
from django.db import models

validar_color = RegexValidator(r"^#[0-9a-fA-F]{6}$", "Use un color hexadecimal, por ejemplo #2e7d32.")


class Comentario(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100, blank=True, help_text="Opcional.")
    contenido = models.TextField(max_length=1000)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    @property
    def autor(self):
        return self.nombre or "Anónimo"

    def __str__(self):
        return f"{self.autor}: {self.contenido[:40]}"


class ConfiguracionSitio(models.Model):
    """Registro único con la personalización visual del sitio (títulos y colores)."""

    nombre_tienda = models.CharField("Nombre de la tienda", max_length=100, default="Supertienda")
    titulo_sitio = models.CharField("Título del sitio administrativo", max_length=100,
                                    default="Supertienda · Administración")
    titulo_inicio = models.CharField("Título de la página principal", max_length=100,
                                     default="Bienvenido a Supertienda")
    titulo_catalogo = models.CharField("Título del catálogo", max_length=100, default="Catálogo de productos")
    titulo_comentarios = models.CharField("Título del listado de comentarios", max_length=100,
                                          default="Lo que opinan nuestros clientes")
    titulo_formulario = models.CharField("Título del formulario de comentarios", max_length=100,
                                         default="Déjenos su comentario")
    descripcion_inicio = models.TextField("Texto de la página principal",
                                          default="Su tienda y abarrotería de confianza. Conozca nuestros productos.")
    direccion_tienda = models.CharField("Dirección", max_length=200, blank=True)
    telefono_tienda = models.CharField("Teléfono", max_length=50, blank=True)
    horario = models.CharField("Horario de atención", max_length=100, blank=True)
    color_primario = models.CharField("Color primario", max_length=7, default="#4caf50", validators=[validar_color])
    color_secundario = models.CharField("Color secundario (encabezados)", max_length=7, default="#2e7d32",
                                        validators=[validar_color])

    class Meta:
        verbose_name = "configuración del sitio"
        verbose_name_plural = "configuración del sitio"

    def __str__(self):
        return "Configuración del sitio"

    def save(self, *args, **kwargs):
        self.pk = 1  # siempre un único registro
        super().save(*args, **kwargs)

    @classmethod
    def obtener(cls):
        return cls.objects.get_or_create(pk=1)[0]
