from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comentario, ConfiguracionSitio


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("fecha", "autor", "contenido")
    search_fields = ("nombre", "contenido")
    list_filter = ("fecha",)
    readonly_fields = ("fecha",)


class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSitio
        fields = "__all__"
        widgets = {
            "color_primario": forms.TextInput(attrs={"type": "color"}),
            "color_secundario": forms.TextInput(attrs={"type": "color"}),
        }


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    form = ConfiguracionForm
    fieldsets = (
        ("Títulos", {"fields": ("nombre_tienda", "titulo_sitio", "titulo_inicio", "titulo_catalogo",
                                "titulo_comentarios", "titulo_formulario")}),
        ("Página principal", {"fields": ("descripcion_inicio", "direccion_tienda", "telefono_tienda", "horario")}),
        ("Colores", {"fields": ("color_primario", "color_secundario")}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Es un registro único: se abre directamente su edición.
        obj = ConfiguracionSitio.obtener()
        return redirect(reverse("admin:publico_configuracionsitio_change", args=[obj.pk]))
