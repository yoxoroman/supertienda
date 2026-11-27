from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("comentarios/", views.comentarios, name="comentarios"),
    path("comentarios/nuevo/", views.comentario_nuevo, name="comentario_nuevo"),
]
