from collections import defaultdict
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from num2words import num2words
from django.conf import settings
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
from datetime import datetime
from django.utils import timezone


def generar_comprobante_pdf(id_comprobante):
    comprobante = get_object_or_404(Comprobante_Pago, id_comprobante=id_comprobante)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ===== PALETA DE COLORES =====
    morado_principal = colors.HexColor("#6C2DC7")
    texto_verde = colors.HexColor("#28A745")
    bg_dark = colors.HexColor("#343a40")
    fondo_blanco = colors.white
    texto_principal = colors.HexColor("#212529")
    texto_secundario = colors.HexColor("#6C757D")
    texto_rojo = colors.HexColor("#DC3545")
    linea_sutil = colors.HexColor("#E9ECEF")

    # ===== AGRUPAR PRODUCTOS =====
    productos_agrupados = defaultdict(lambda: {"nombre": "", "cantidad": 0, "precio": 0, "subtotal": 0})
    total = 0

    if hasattr(comprobante.id_compra, "detalle_compra_set"):
        detalles_productos = comprobante.id_compra.detalle_compra_set.select_related('id_producto').all()
        for det in detalles_productos:
            codigo = det.id_producto.id_producto
            productos_agrupados[codigo]["nombre"] = det.id_producto.nombre_producto
            productos_agrupados[codigo]["cantidad"] += det.cantidad_producto_compra
            productos_agrupados[codigo]["precio"] = det.precio_unitario_compra
            productos_agrupados[codigo]["subtotal"] += det.cantidad_producto_compra * det.precio_unitario_compra

    # ===== AGRUPAR SERVICIOS =====
    servicios_agrupados = defaultdict(lambda: {"nombre": "", "cantidad": 0,"precio": 0, "subtotal": 0})
    if hasattr(comprobante.id_compra, "detalle_servicio_set"):
        detalles_servicios = comprobante.id_compra.detalle_servicio_set.select_related('id_servicio').all()
        for det in detalles_servicios:
            codigo = det.id_servicio.id_servicio
            servicios_agrupados[codigo]["nombre"] = 'Arreglo Personalizado ' + det.id_servicio.id_categoria_servicio.nombre_categoria_servicio
            servicios_agrupados[codigo]["cantidad"] += det.cantidad_producto_servicio
            servicios_agrupados[codigo]["precio"] = det.precio_unitario_servicio
            servicios_agrupados[codigo]["subtotal"] += det.cantidad_producto_servicio * det.precio_unitario_servicio

    # ===== DATOS TABLAS =====
    data_header = ["Descripción", "Cant.", "Precio", "Subtotal"]
    data_productos = []
    for prod in productos_agrupados.values():
        data_productos.append([
            prod["nombre"],
            str(prod["cantidad"]),
            f"${prod['precio']:.2f}",
            f"${prod['subtotal']:.2f}"
        ])
        total += prod["subtotal"]

    data_servicios = []
    for serv in servicios_agrupados.values():
        data_servicios.append([
            serv["nombre"],
            str(serv["cantidad"]),
            f"${serv['precio']:.2f}",
            f"${serv['subtotal']:.2f}"
        ])
        total += serv["subtotal"]

    # ===== PAGINACIÓN =====
    max_rows_first_page = 10
    max_rows_other_pages = 20

    total_rows = len(data_productos) + len(data_servicios)
    if total_rows <= max_rows_first_page:
        total_pages = 1
    else:
        remaining_rows = total_rows - max_rows_first_page
        additional_pages = (remaining_rows + max_rows_other_pages - 1) // max_rows_other_pages
        total_pages = 1 + additional_pages

    # ===== FUNCIONES AUXILIARES =====
    def draw_header(page_num):
        p.setFillColor(fondo_blanco)
        p.rect(0, 0, width, height, fill=1)

        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        if os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            p.drawImage(logo, 10, height - 130, width=140, height=140, mask='auto')

        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(morado_principal)
        p.drawString(140, height - 60, "FLORISTERÍA FLOWERS TODAY")

        p.setFont("Helvetica", 10)
        p.setFillColor(texto_secundario)
        p.drawString(140, height - 80, "Colonia El Carmen, Pasaje B, San Marcos, San Salvador")
        p.drawString(140, height - 95, "Tel: +503 2234-5678 | Email: contacto@flowerstoday.sv")

        p.setStrokeColor(linea_sutil)
        p.setLineWidth(1)
        p.line(80, height - 120, width - 80, height - 120)

        return height - 150

    def draw_comprobante_info():
        y_pos = height - 180
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(bg_dark)
        p.drawString(80, y_pos, "COMPROBANTE DE PAGO")

        codigo_texto = f"Código de Comprobante: {comprobante.codigo_comprobante}"
        p.setFont("Helvetica", 10)
        p.setFillColor(texto_principal)
        p.drawString(80, y_pos - 25, codigo_texto)

        p.drawString(350, y_pos - 25, f"Fecha: {comprobante.fecha_comprobante.strftime('%d/%m/%Y')}")

        estado_texto = 'ENTREGADO' if comprobante.estado_comprobante == 'Pa' else 'PENDIENTE DE ENTREGAR'
        estado_color = texto_verde if comprobante.estado_comprobante == 'Pa' else texto_rojo
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(estado_color)
        p.drawString(80, y_pos - 50, f"Estado: {estado_texto}")

        y_pos -= 80
        usuario = comprobante.id_compra.id_usuario
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(bg_dark)
        p.drawString(80, y_pos, "CLIENTE")

        p.setFont("Helvetica", 11)
        p.setFillColor(texto_principal)
        p.drawString(80, y_pos - 25, f"Nombre: {usuario.nombre_usuario} {usuario.apellido_usuario}")
        p.drawString(80, y_pos - 42, f"Correo: {usuario.correo_usuario}")
        if hasattr(usuario, 'telefono_usuario'):
            p.drawString(80, y_pos - 59, f"Tel: {usuario.telefono_usuario}")

        return y_pos - 90

    def draw_footer(page_num, is_last_page=False):
        p.setFont("Helvetica", 9)
        p.setFillColor(texto_secundario)
        p.drawRightString(width - 80, 30, f"Página {page_num} de {total_pages}")

        if is_last_page:
            y_footer = 150
            p.setStrokeColor(linea_sutil)
            p.line(80, y_footer, width - 80, y_footer)

            p.setFont("Helvetica-Bold", 20)
            p.setFillColor(morado_principal)
            p.drawRightString(width - 80, y_footer - 25, f"TOTAL: ${total:.2f}")

            p.setFont("Helvetica-Oblique", 10)
            p.setFillColor(texto_secundario)
            p.drawRightString(width - 80, y_footer - 45, f"Son: {num2words(total, lang='es').capitalize()} dólares exactos.")

            p.setStrokeColor(linea_sutil)
            p.line(80, y_footer - 70, width - 80, y_footer - 70)

            p.setFont("Helvetica-Oblique", 11)
            p.setFillColor(morado_principal)
            p.drawCentredString(width / 2, y_footer - 90, "¡Gracias por su compra!")

            p.setFont("Helvetica", 9)
            p.setFillColor(texto_secundario)
            p.drawCentredString(width / 2, y_footer - 105, "Flowers Today - Hacemos especial cada momento")

            p.setFont("Helvetica", 8)
            p.setFillColor(texto_secundario)
            p.drawString(80, 50, f"Generado: {timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')}")

    def draw_table(table_data, y_position, include_header=True):
        if not table_data:
            return y_position
        full_data = [data_header] + table_data if include_header else table_data
        table = Table(full_data, colWidths=[250, 60, 80, 80])
        table_style = [
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
        if include_header:
            table_style.extend([
                ('BACKGROUND', (0, 0), (-1, 0), morado_principal),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('LINEBELOW', (0, 0), (-1, 0), 2, morado_principal),
            ])
        table.setStyle(TableStyle(table_style))
        table_height = len(full_data) * 30
        table.wrapOn(p, width, height)
        table.drawOn(p, 80, y_position - table_height)
        return y_position - table_height

    # ===== GENERAR PÁGINAS =====
    current_page = 1
    y_position = draw_header(current_page)
    y_position = draw_comprobante_info()

    # Sección Productos
    if data_productos:
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(bg_dark)
        p.drawString(80, y_position - 20, "DETALLE DE PRODUCTOS")
        y_position = draw_table(data_productos, y_position - 40, include_header=True)

    # Sección Servicios
    if data_servicios:
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(bg_dark)
        p.drawString(80, y_position - 20, "DETALLE DE SERVICIOS")
        y_position = draw_table(data_servicios, y_position - 40, include_header=True)

    draw_footer(current_page, is_last_page=True)

    p.setTitle(f"Comprobante {comprobante.codigo_comprobante} - Flowers Today")
    p.save()
    buffer.seek(0)

    nombre_archivo = f"Comprobante_{comprobante.codigo_comprobante}_{datetime.now().strftime('%Y%m%d')}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response
