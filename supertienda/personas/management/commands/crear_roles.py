from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

APPS = ["personas", "inventario", "procedimientos", "publico"]

# (app, modelo): acciones permitidas al grupo Vendedores
PERMISOS_VENDEDORES = {
    ("procedimientos", "venta"): ["view", "add"],               # 6.2.1
    ("procedimientos", "detalleventa"): ["view", "add", "change"],  # 6.2.2
    ("personas", "cliente"): ["view", "add", "change"],         # 6.2.3
    ("personas", "vendedor"): ["view"],                         # 6.2.4
    ("publico", "comentario"): ["view"],                        # 6.2.5
    ("inventario", "producto"): ["view"],                       # necesario para elegir productos en una venta
}


class Command(BaseCommand):
    help = "Crea/actualiza los grupos Supervisores y Vendedores con sus permisos."

    def handle(self, *args, **options):
        supervisores, _ = Group.objects.get_or_create(name="Supervisores")
        supervisores.permissions.set(Permission.objects.filter(content_type__app_label__in=APPS))

        vendedores, _ = Group.objects.get_or_create(name="Vendedores")
        permisos = [
            Permission.objects.get(content_type__app_label=app, codename=f"{accion}_{modelo}")
            for (app, modelo), acciones in PERMISOS_VENDEDORES.items()
            for accion in acciones
        ]
        vendedores.permissions.set(permisos)
        self.stdout.write(self.style.SUCCESS("Grupos 'Supervisores' y 'Vendedores' listos."))
