"""Generación de PDF (facturas e informes) con ReportLab."""
from io import BytesIO
from xml.sax.saxutils import escape

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from publico.models import ConfiguracionSitio


def q(valor):
    return f"Q {valor:,.2f}"


def _fecha(dt):
    return timezone.localtime(dt).strftime("%d/%m/%Y %H:%M")


def _documento(buffer, titulo):
    return SimpleDocTemplate(buffer, pagesize=letter, title=titulo, leftMargin=2 * cm, rightMargin=2 * cm,
                             topMargin=2 * cm, bottomMargin=2 * cm)


def _estilos():
    base = getSampleStyleSheet()
    return base["Normal"], ParagraphStyle("T", parent=base["Title"], fontSize=20)


def _tabla(datos, anchos, color, alineacion_derecha_desde=1):
    t = Table(datos, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f3f3")]),
        ("ALIGN", (alineacion_derecha_desde, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def generar_factura(venta):
    config = ConfiguracionSitio.obtener()
    color = colors.HexColor(config.color_secundario)
    normal, titulo = _estilos()
    cliente, vendedor = venta.cliente, venta.vendedor

    buffer = BytesIO()
    doc = _documento(buffer, f"Factura {venta.pk:06d}")
    e = [
        Paragraph(escape(config.nombre_tienda), titulo),
        Paragraph(f"<b>Factura No.</b> {venta.pk:06d}", normal),
        Paragraph(f"<b>Fecha y hora:</b> {_fecha(venta.fecha_hora)}", normal),
        Spacer(1, 0.5 * cm),
        Paragraph("<b>Cliente</b>", normal),
        Paragraph(escape(f"{cliente.nombre_completo} — DPI {cliente.dpi}"), normal),
        Paragraph(escape(f"Tel.: {cliente.telefonos}  |  {cliente.email or 'sin correo'}"), normal),
        Paragraph(escape(f"Dirección: {cliente.direccion}"), normal),
        Spacer(1, 0.3 * cm),
        Paragraph("<b>Vendedor</b>", normal),
        Paragraph(escape(f"{vendedor.nombre_completo} — DPI {vendedor.dpi}"), normal),
        Spacer(1, 0.6 * cm),
    ]
    filas = [["Producto", "Cantidad", "Precio unitario", "Subtotal"]]
    for d in venta.detalles.all():
        filas.append([Paragraph(escape(f"{d.producto.nombre} ({d.producto.presentacion})"), normal),
                      d.cantidad, q(d.precio_actual), q(d.subtotal)])
    e.append(_tabla(filas, [8 * cm, 2.2 * cm, 3.4 * cm, 3.4 * cm], color))
    e.append(Spacer(1, 0.4 * cm))
    total = Table([["TOTAL", q(venta.total)]], colWidths=[13.6 * cm, 3.4 * cm])
    total.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 12),
                               ("ALIGN", (0, 0), (-1, -1), "RIGHT"), ("LINEABOVE", (0, 0), (-1, 0), 1, color)]))
    e.append(total)
    doc.build(e)
    return buffer.getvalue()


def generar_informe(ventas):
    config = ConfiguracionSitio.obtener()
    color = colors.HexColor(config.color_secundario)
    normal, titulo = _estilos()

    buffer = BytesIO()
    doc = _documento(buffer, "Informe de ventas")
    e = [Paragraph(escape(config.nombre_tienda), titulo),
         Paragraph(f"<b>Informe de ventas seleccionadas</b> — generado {_fecha(timezone.now())}", normal),
         Spacer(1, 0.5 * cm)]
    filas = [["No.", "Fecha y hora", "Cliente", "Vendedor", "Total"]]
    general = 0
    for v in ventas:
        general += v.total
        filas.append([f"{v.pk:06d}", _fecha(v.fecha_hora),
                      Paragraph(escape(v.cliente.nombre_completo), normal),
                      Paragraph(escape(v.vendedor.nombre_completo), normal), q(v.total)])
    e.append(_tabla(filas, [1.8 * cm, 3.4 * cm, 4.8 * cm, 4.2 * cm, 2.8 * cm], color, alineacion_derecha_desde=4))
    e.append(Spacer(1, 0.4 * cm))
    e.append(Paragraph(f"<b>Cantidad de ventas:</b> {len(filas) - 1} &nbsp;&nbsp; <b>Total general:</b> {q(general)}",
                       normal))
    doc.build(e)
    return buffer.getvalue()
