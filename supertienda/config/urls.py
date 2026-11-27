from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.index_title = "Gestión de Supertienda"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("publico.urls")),
    # Imágenes de productos. Para una tienda pequeña basta; en alto tráfico use un almacenamiento externo.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
