from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html

from personas.models import Vendedor

from .models import DetalleVenta, Venta
from .pdf import generar_factura, generar_informe, q


def _pdf(contenido, nombre):
    respuesta = HttpResponse(contenido, content_type="application/pdf")
    respuesta["Content-Disposition"] = f'inline; filename="{nombre}"'
    return respuesta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    fields = ("producto", "cantidad", "precio_actual", "subtotal_q")
    readonly_fields = ("subtotal_q",)
    autocomplete_fields = ("producto",)
    extra = 0
    min_num = 1
    validate_min = True

    @admin.display(description="Subtotal")
    def subtotal_q(self, obj):
        return q(obj.subtotal) if obj.pk else "—"


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "fecha_hora", "cliente", "vendedor", "total_q", "boton_factura")
    list_filter = ("fecha_hora", "vendedor")
    date_hierarchy = "fecha_hora"
    search_fields = ("cliente__dpi", "cliente__nombres", "cliente__apellidos",
                     "vendedor__nombres", "vendedor__apellidos")
    autocomplete_fields = ("cliente", "vendedor")
    inlines = [DetalleVentaInline]
    actions = ["informe_pdf"]

    def get_queryset(self, request):
        return (super().get_queryset(request)
                .select_related("cliente", "vendedor")
                .prefetch_related("detalles"))

    def get_changeform_initial_data(self, request):
        inicial = super().get_changeform_initial_data(request)
        vendedor = Vendedor.objects.filter(usuario=request.user, activo=True).first()
        if vendedor:
            inicial.setdefault("vendedor", vendedor.pk)
        return inicial

    @admin.display(description="Total")
    def total_q(self, obj):
        return q(obj.total)

    @admin.display(description="Factura")
    def boton_factura(self, obj):
        url = reverse("admin:procedimientos_venta_factura", args=[obj.pk])
        return format_html('<a class="button" href="{}" target="_blank">Factura PDF</a>', url)

    # --- PDF de una venta (botón en la lista y en la ficha) ---
    def get_urls(self):
        propias = [path("<path:object_id>/factura/", self.admin_site.admin_view(self.factura_view),
                        name="procedimientos_venta_factura")]
        return propias + super().get_urls()  # antes que la ruta genérica <object_id>/

    def factura_view(self, request, object_id):
        venta = self.get_object(request, object_id)
        if venta is None:
            raise Http404("La venta no existe.")
        if not self.has_view_permission(request, venta):
            raise PermissionDenied
        return _pdf(generar_factura(venta), f"factura_{venta.pk:06d}.pdf")

    # --- PDF de las ventas seleccionadas ---
    @admin.action(description="Generar informe PDF de las ventas seleccionadas", permissions=["view"])
    def informe_pdf(self, request, queryset):
        return _pdf(generar_informe(queryset.order_by("fecha_hora")), "informe_ventas.pdf")


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_q", "subtotal_q")
    list_select_related = ("venta", "producto")
    search_fields = ("producto__nombre", "producto__codigo")
    autocomplete_fields = ("venta", "producto")

    @admin.display(description="Precio unitario")
    def precio_q(self, obj):
        return q(obj.precio_actual)

    @admin.display(description="Subtotal")
    def subtotal_q(self, obj):
        return q(obj.subtotal)
