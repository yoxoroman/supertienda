from .models import ConfiguracionSitio


def tema(request):
    return {"tema": ConfiguracionSitio.obtener()}
