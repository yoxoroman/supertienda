from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from inventario.models import Producto

from .forms import ComentarioForm
from .models import Comentario


def inicio(request):
    return render(request, "publico/inicio.html")


def comentarios(request):
    pagina = Paginator(Comentario.objects.all(), 10).get_page(request.GET.get("page"))
    return render(request, "publico/comentarios.html", {"pagina": pagina})


def comentario_nuevo(request):
    form = ComentarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "¡Gracias! Su comentario fue enviado.")
        return redirect("comentarios")
    return render(request, "publico/comentario_form.html", {"form": form})


def catalogo(request):
    productos = Producto.objects.filter(activo=True)
    pagina = Paginator(productos, 12).get_page(request.GET.get("page"))
    return render(request, "publico/catalogo.html", {"pagina": pagina})
