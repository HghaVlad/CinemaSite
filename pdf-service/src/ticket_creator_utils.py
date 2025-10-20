import os.path

from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

rob_reg = os.path.join('assets', 'Roboto-Regular.ttf')
rob_bold = os.path.join('assets', 'Roboto-Bold.ttf')

pdfmetrics.registerFont(TTFont('Roboto', rob_reg))
pdfmetrics.registerFont(TTFont('Roboto-Bold', rob_bold))


def generate_ticket_pdf(filename, **kwargs):
    c = canvas.Canvas(filename, pagesize=A6)
    width, height = A6

    styles = {
        'bg_color': colors.HexColor("#FFFFFF"),
        'main_color': colors.HexColor("#B5C69F"),
        'text_dark': colors.HexColor("#4E342E"),
        'text_light': colors.HexColor("#9EBA78"),
        'font_normal': 'Roboto',
        'font_bold': 'Roboto-Bold'
    }

    c.setFillColor(styles['bg_color'])
    c.rect(0, 0, width, height, fill=1)

    draw_main_frame(c, width, height, styles)
    draw_header(c, width, height, styles)
    draw_movie_info(c, width, height, styles, **kwargs)
    draw_logo(c, width, height)
    draw_client_info(c, width, styles, **kwargs)

    c.save()


def draw_main_frame(c, width, height, styles):
    c.setStrokeColor(styles['main_color'])
    c.setLineWidth(2)
    c.roundRect(10, 10, width - 20, height - 20, 10)


def draw_logo(c, width, height):
    try:
        logo_path = os.path.join('assets', 'absolute_logo.jpeg')
        logo = ImageReader(logo_path)
        c.drawImage(logo, width / 2 - 68, height / 2 - 92, width=140, height=140, mask='auto')
    except Exception as e:
        print(f"Ошибка загрузки логотипа: {e}")


def draw_header(c, width, height, styles):
    c.setFont(styles['font_bold'], 16)
    c.setFillColor(styles['text_light'])
    c.drawCentredString(width / 2, height - 40, "ABSOLUTE CINEMA")


def draw_movie_info(c, width, height, styles, **kwargs):
    y_position = height - 70
    c.setFont(styles['font_bold'], 12)
    c.setFillColor(styles['text_dark'])

    info = [
        ("ФИЛЬМ:", kwargs['film']),
        ("ВРЕМЯ:", kwargs['time']),
        ("РЯД:", kwargs['row']),
        ("МЕСТО:", kwargs['seat'])
    ]

    for label, value in info:
        c.drawString(20, y_position, label)
        c.setFont(styles['font_normal'], 10)
        c.drawString(80, y_position, value)
        y_position -= 20
        c.setFont(styles['font_bold'], 10)


def draw_client_info(c, width, styles, **kwargs):
    c.setFont(styles['font_bold'], 10)
    c.setFillColor(styles['text_light'])
    c.drawString(20, 90, "ПОСЕТИТЕЛЬ:")
    c.setFont(styles['font_normal'], 9)
    c.setFillColor(styles['text_dark'])

    client_info = [
        f"{kwargs['user_name']} {kwargs['user_surname']}",
        f"Email: {kwargs['user_email']}"
    ]

    y_position = 75
    for line in client_info:
        c.drawString(20, y_position, line)
        y_position -= 15
