from collections import defaultdict
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from num2words import num2words
from django.conf import settings
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import os

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

    # ===== AGRUPAR PRODUCTOS REPETIDOS =====
    detalles = comprobante.id_compra.detalle_compra_set.select_related('id_producto').all()
    productos_agrupados = defaultdict(lambda: {"nombre": "", "cantidad": 0, "precio": 0, "subtotal": 0})
    
    for det in detalles:
        codigo = det.id_producto.id_producto
        productos_agrupados[codigo]["nombre"] = det.id_producto.nombre_producto
        productos_agrupados[codigo]["cantidad"] += det.cantidad_producto_compra
        productos_agrupados[codigo]["precio"] = det.precio_unitario_compra
        productos_agrupados[codigo]["subtotal"] += det.cantidad_producto_compra * det.precio_unitario_compra

    # Convertir a lista de listas para la tabla
    data_header = ["Producto", "Cant.", "Precio", "Subtotal"]
    data_rows = []
    total = 0
    
    for prod in productos_agrupados.values():
        data_rows.append([
            prod["nombre"],
            str(prod["cantidad"]),
            f"${prod['precio']:.2f}",
            f"${prod['subtotal']:.2f}"
        ])
        total += prod["subtotal"]

    # ===== CALCULAR PAGINACIÓN =====
    max_rows_first_page = 10  # Máximo 10 filas en primera página
    max_rows_other_pages = 20  # Máximo 20 filas en páginas siguientes (más espacio disponible)
    
    # Calcular total de páginas necesarias
    if len(data_rows) <= max_rows_first_page:
        total_pages = 1
    else:
        remaining_rows = len(data_rows) - max_rows_first_page
        additional_pages = (remaining_rows + max_rows_other_pages - 1) // max_rows_other_pages
        total_pages = 1 + additional_pages

    # ===== FUNCIÓN PARA DIBUJAR ENCABEZADO =====
    def draw_header(page_num):
        # Fondo blanco
        p.setFillColor(fondo_blanco)
        p.rect(0, 0, width, height, fill=1)

        # LOGO
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        if os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            p.drawImage(logo, 10, height - 130, width=140, height=140, mask='auto')

        # TÍTULO DE LA FLORISTERÍA
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(morado_principal)
        p.drawString(140, height - 60, "FLORISTERÍA FLOWERS TODAY")

        # INFORMACIÓN DE CONTACTO
        p.setFont("Helvetica", 10)
        p.setFillColor(texto_secundario)
        p.drawString(140, height - 80, "Colonia El Carmen, Pasaje B, San Marcos, San Salvador")
        p.drawString(140, height - 95, "Tel: +503 2234-5678 | Email: contacto@flowerstoday.sv")

        # LÍNEA SEPARADORA
        p.setStrokeColor(linea_sutil)
        p.setLineWidth(1)
        p.line(80, height - 120, width - 80, height - 120)

        return height - 150  # Posición Y donde continúa el contenido

    # ===== FUNCIÓN PARA DIBUJAR INFO DEL COMPROBANTE Y CLIENTE =====
    def draw_comprobante_info():
        # INFO COMPROBANTE
        y_pos = height - 180
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(bg_dark)
        p.drawString(80, y_pos, "COMPROBANTE DE PAGO")

        # Código de Comprobante
        codigo_texto = f"Código de Comprobante: {comprobante.id_comprobante}"
        max_width_codigo = 250
        font_name = "Helvetica"
        font_size = 11

        while stringWidth(codigo_texto, font_name, font_size) > max_width_codigo and font_size > 6:
            font_size -= 1

        p.setFont(font_name, font_size)
        p.setFillColor(texto_principal)

        if stringWidth(codigo_texto, font_name, font_size) <= max_width_codigo:
            p.drawString(80, y_pos - 25, codigo_texto)
        else:
            estilo = ParagraphStyle(
                name="CodigoComprobante",
                fontName=font_name,
                fontSize=font_size,
                leading=font_size + 2,
                textColor=texto_principal
            )
            parrafo_codigo = Paragraph(codigo_texto, estilo)
            parrafo_codigo.wrapOn(p, max_width_codigo, 40)
            parrafo_codigo.drawOn(p, 80, y_pos - 40)

        # Fecha
        p.setFont("Helvetica", 11)
        p.setFillColor(texto_principal)
        p.drawString(350, y_pos - 25, f"Fecha: {comprobante.fecha_comprobante.strftime('%d/%m/%Y')}")

        # Estado
        estado_texto = 'ENTREGADO' if comprobante.estado_comprobante == 'Pa' else 'PENDIENTE DE ENTREGAR'
        estado_color = texto_verde if comprobante.estado_comprobante == 'Pa' else texto_rojo
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(estado_color)
        p.drawString(80, y_pos - 50, f"Estado: {estado_texto}")

        # CLIENTE
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

        return y_pos - 90  # Posición Y después de la información del cliente

    # ===== FUNCIÓN PARA DIBUJAR PIE DE PÁGINA =====
    def draw_footer(page_num, is_last_page=False):
        # Numeración de página
        p.setFont("Helvetica", 9)
        p.setFillColor(texto_secundario)
        p.drawRightString(width - 80, 30, f"Página {page_num} de {total_pages}")
        
        if is_last_page:
            # Total y información final solo en la última página
            y_footer = 150
            
            p.setStrokeColor(linea_sutil)
            p.setLineWidth(1)
            p.line(80, y_footer, width - 80, y_footer)

            p.setFont("Helvetica-Bold", 20)
            p.setFillColor(morado_principal)
            p.drawRightString(width - 80, y_footer - 25, f"TOTAL: ${total:.2f}")

            p.setFont("Helvetica-Oblique", 10)
            p.setFillColor(texto_secundario)
            p.drawRightString(width - 80, y_footer - 45, f"Son: {num2words(total, lang='es').capitalize()} dólares exactos.")

            # Línea decorativa
            p.setStrokeColor(linea_sutil)
            p.setLineWidth(1)
            p.line(80, y_footer - 70, width - 80, y_footer - 70)

            # Mensaje de agradecimiento
            p.setFont("Helvetica-Oblique", 11)
            p.setFillColor(morado_principal)
            p.drawCentredString(width / 2, y_footer - 90, "¡Gracias por su compra!")

            p.setFont("Helvetica", 9)
            p.setFillColor(texto_secundario)
            p.drawCentredString(width / 2, y_footer - 105, "Flowers Today - Hacemos especial cada momento")

            # Fecha de generación
            p.setFont("Helvetica", 8)
            p.setFillColor(texto_secundario)
            p.drawString(80, 50, f"Generado: {comprobante.fecha_comprobante.strftime('%d/%m/%Y %H:%M')}")

    # ===== FUNCIÓN PARA DIBUJAR TABLA =====
    def draw_table(table_data, y_position, include_header=True):
        if include_header:
            full_data = [data_header] + table_data
        else:
            full_data = table_data

        table = Table(full_data, colWidths=[250, 60, 80, 80])
        
        # Estilos de la tabla
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
        
        # Calcular altura de la tabla
        table_height = len(full_data) * 30  # Aproximadamente 30 puntos por fila
        
        table.wrapOn(p, width, height)
        table.drawOn(p, 80, y_position - table_height)
        
        return y_position - table_height

    # ===== GENERAR PÁGINAS =====
    current_row = 0
    current_page = 1

    while current_row < len(data_rows):
        # Determinar cuántas filas mostrar en esta página
        if current_page == 1:
            max_rows = max_rows_first_page
            # Dibujar encabezado de la floristería
            table_y_start = draw_header(current_page)
            # Dibujar información del comprobante y cliente (solo primera página)
            table_y_start = draw_comprobante_info()
        else:
            max_rows = max_rows_other_pages
            # Solo dibujar encabezado de la floristería
            table_y_start = draw_header(current_page)

        # Obtener las filas para esta página
        end_row = min(current_row + max_rows, len(data_rows))
        page_data = data_rows[current_row:end_row]
        
        # Dibujar sección de productos
        if current_page == 1:
            p.setFont("Helvetica-Bold", 14)
            p.setFillColor(bg_dark)
            p.drawString(80, table_y_start - 20, "DETALLE")
            table_start_position = table_y_start - 20  # Reducir espacio entre DETALLE y tabla
        else:
            # No mostrar título en páginas siguientes
            table_start_position = table_y_start + 20
        
        # Dibujar tabla
        include_header = True  # Incluir encabezado en cada página para claridad
        table_y_end = draw_table(page_data, table_start_position, include_header)
        
        # Dibujar pie de página
        is_last_page = (end_row >= len(data_rows))
        draw_footer(current_page, is_last_page)
        
        # Avanzar a siguiente página si es necesario
        current_row = end_row
        current_page += 1
        
        if current_row < len(data_rows):
            p.showPage()

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')