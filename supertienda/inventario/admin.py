from django.contrib import admin
from django.utils.html import format_html

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("miniatura", "codigo", "nombre", "marca", "presentacion", "costo_compra", "precio_venta", "activo")
    list_filter = ("activo", "marca")
    search_fields = ("codigo", "nombre", "marca")

    @admin.display(description="Imagen")
    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:40px;border-radius:4px">', obj.imagen.url)
        return "—"
