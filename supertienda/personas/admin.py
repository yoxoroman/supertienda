from django.contrib import admin

from .models import Cliente, Vendedor


class PersonaAdmin(admin.ModelAdmin):
    list_display = ("dpi", "apellidos", "nombres", "telefonos", "email", "activo")
    list_filter = ("activo",)
    search_fields = ("dpi", "nombres", "apellidos", "telefonos", "email")


@admin.register(Cliente)
class ClienteAdmin(PersonaAdmin):
    pass


@admin.register(Vendedor)
class VendedorAdmin(PersonaAdmin):
    raw_id_fields = ("usuario",)
