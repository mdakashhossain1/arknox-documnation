import argparse
import html
import json
import math
import os
import re
import subprocess
from pathlib import Path

import pymupdf as fitz
from bs4 import BeautifulSoup, NavigableString
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / 'pdfs'
PAGE_DIR = ROOT / 'assets' / 'pdf-pages'
WIDTH, HEIGHT = A4
LEFT, RIGHT, TOP, BOTTOM = 56.7, 63.7, 72, 72
CONTENT_WIDTH = WIDTH - LEFT - RIGHT
PURPLE = colors.HexColor('#6059F7')
BLUE = colors.HexColor('#259CF1')
STYLES = {}
SCREENSHOTS = {}


def register_fonts():
    directory = Path(os.environ.get('ARKNOX_FONT_DIR', 'C:/Windows/Fonts'))
    for name, filename in [('Body', 'calibri.ttf'), ('BodyBold', 'calibrib.ttf'), ('BodyItalic', 'calibrii.ttf'), ('BodyBoldItalic', 'calibriz.ttf'), ('Company', 'BELL.TTF'), ('Footer', 'timesbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(directory / filename)))
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic', boldItalic='BodyBoldItalic')
    base = ParagraphStyle('Body', fontName='Body', fontSize=11, leading=14.5, alignment=TA_JUSTIFY, textColor=colors.black, spaceAfter=8, splitLongWords=True, allowWidows=0, allowOrphans=0)
    STYLES.update({
        'body': base,
        'title': ParagraphStyle('Title', parent=base, fontName='BodyBold', fontSize=22, leading=27, alignment=TA_LEFT, spaceAfter=9, keepWithNext=True),
        'chapter': ParagraphStyle('Chapter', parent=base, fontName='BodyBold', fontSize=22, leading=27, alignment=TA_CENTER, textColor=BLUE, spaceAfter=14, keepWithNext=True),
        'subtitle': ParagraphStyle('Subtitle', parent=base, fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=20, keepWithNext=True),
        'heading': ParagraphStyle('Heading', parent=base, fontName='BodyBold', fontSize=12, leading=16, alignment=TA_LEFT, textColor=PURPLE, spaceBefore=12, spaceAfter=6, keepWithNext=True),
        'small': ParagraphStyle('Small', parent=base, fontSize=9, leading=12, alignment=TA_LEFT, textColor=colors.HexColor('#404040')),
        'caption': ParagraphStyle('Caption', parent=base, fontName='BodyItalic', fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=5),
        'cell': ParagraphStyle('Cell', parent=base, fontSize=9.5, leading=12.5, alignment=TA_LEFT, spaceAfter=0),
        'cellhead': ParagraphStyle('CellHead', parent=base, fontName='BodyBold', fontSize=9.5, leading=12, alignment=TA_LEFT, textColor=colors.white, spaceAfter=0),
        'code': ParagraphStyle('Code', parent=base, fontName='Courier', fontSize=8, leading=11, alignment=TA_LEFT, backColor=colors.HexColor('#F3F3F7'), borderColor=colors.HexColor('#D9D9D9'), borderWidth=.5, borderPadding=8, spaceBefore=8, spaceAfter=12),
        'note': ParagraphStyle('Note', parent=base, backColor=colors.HexColor('#F5F3FF'), borderPadding=9, spaceBefore=9, spaceAfter=13),
    })


def normalized(text):
    return str(text).replace('\u00a0', ' ').replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')


def inline(value):
    soup = BeautifulSoup(str(value), 'html.parser')

    def walk(node):
        if isinstance(node, NavigableString):
            return html.escape(normalized(node))
        if node.name in ['script', 'style', 'button', 'svg']:
            return ''
        children = ''.join(walk(child) for child in node.children)
        if node.name in ['b', 'strong']:
            return f'<b>{children}</b>'
        if node.name in ['i', 'em']:
            return f'<i>{children}</i>'
        if node.name == 'br':
            return '<br/>'
        if node.name == 'code':
            return f'<font face="Courier" size="9">{children}</font>'
        return children

    return ''.join(walk(child) for child in soup.children).strip()


def para(value, style='body'):
    return Paragraph(inline(value), STYLES[style])


def rich_blocks(value):
    result = []
    for part in re.split(r'(<pre[\s\S]*?</pre>|<ol[\s\S]*?</ol>|<ul[\s\S]*?</ul>|<p[\s\S]*?</p>)', str(value)):
        if not part.strip():
            continue
        if part.startswith('<pre'):
            text = BeautifulSoup(part, 'html.parser').get_text()
            result.append(Paragraph(html.escape(normalized(text)).replace('\n', '<br/>'), STYLES['code']))
        elif part.startswith(('<ol', '<ul')):
            listing = BeautifulSoup(part, 'html.parser').find(['ol', 'ul'])
            for index, item in enumerate(listing.find_all('li', recursive=False), 1):
                prefix = f'{index}. ' if listing.name == 'ol' else '• '
                result.append(para(prefix + str(item)))
        else:
            result.append(para(part))
    return result


def grid(rows, widths=None):
    widths = widths or [CONTENT_WIDTH * .23, CONTENT_WIDTH * .35, CONTENT_WIDTH * .42]
    formatted = [[para(cell, 'cellhead' if index == 0 else 'cell') for cell in row] for index, row in enumerate(rows)]
    table = Table(formatted, colWidths=widths, repeatRows=1, hAlign='LEFT', splitByRow=1, splitInRow=0)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FAF9FF')]),
        ('GRID', (0, 0), (-1, -1), .5, colors.HexColor('#D9D9D9')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return table


class Screenshot(Flowable):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.path = ROOT / item['imageFile']
        if self.path.suffix == '.svg':
            self.drawing = svg2rlg(str(self.path))
            self.source_width, self.source_height = self.drawing.width, self.drawing.height
        else:
            self.drawing = None
            with Image.open(self.path) as image:
                self.source_width, self.source_height = image.size
        self.points = item.get('points', [])
        scale = min(CONTENT_WIDTH / self.source_width, 355 / self.source_height)
        self.width, self.height = self.source_width * scale, self.source_height * scale
        self.hAlign = 'CENTER'
        self.keepWithNext = True

    def draw(self):
        canvas = self.canv
        if self.drawing:
            canvas.saveState()
            canvas.scale(self.width / self.source_width, self.height / self.source_height)
            renderPDF.draw(self.drawing, canvas, 0, 0)
            canvas.restoreState()
        else:
            canvas.drawImage(str(self.path), 0, 0, self.width, self.height, mask='auto')
        radius = 11 if self.item.get('mobile') else 21
        scale = self.width / self.source_width
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#AC3500'))
        canvas.setLineWidth(max(.8, 3.5 * scale))
        for index, point in enumerate(self.points):
            x = point[0] * scale
            y = self.height - point[1] * scale
            end_x, end_y = point[2] * scale, self.height - point[3] * scale
            start_x, start_y = x - radius * scale * .7, y - radius * scale * .5
            canvas.line(start_x, start_y, end_x, end_y)
            angle = math.atan2(end_y - start_y, end_x - start_x)
            length = max(4, 9 * scale)
            arrow = canvas.beginPath()
            arrow.moveTo(end_x, end_y)
            arrow.lineTo(end_x - length * math.cos(angle - .45), end_y - length * math.sin(angle - .45))
            arrow.lineTo(end_x - length * math.cos(angle + .45), end_y - length * math.sin(angle + .45))
            arrow.close()
            canvas.setFillColor(colors.HexColor('#AC3500'))
            canvas.drawPath(arrow, fill=1, stroke=0)
            canvas.setStrokeColor(colors.white)
            canvas.circle(x, y, radius * scale, fill=1, stroke=1)
            canvas.setStrokeColor(colors.HexColor('#AC3500'))
            canvas.setFillColor(colors.white)
            canvas.setFont('BodyBold', max(5, radius * scale * 1.1))
            canvas.drawCentredString(x, y - radius * scale * .36, str(index + 1))
        canvas.restoreState()

class NumberedCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self.pages)
        for state in self.pages:
            self.__dict__.update(state)
            self.setFont('Footer', 12)
            self.setFillColor(colors.black)
            self.drawCentredString(WIDTH / 2, 39, f'Page {self._pageNumber} of {total}')
            super().showPage()
        super().save()


class OfficialDocument(BaseDocTemplate):
    def __init__(self, path, title):
        super().__init__(str(path), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM, title=title, author='Arknox', pageCompression=1)
        self.chapter_pages = {}
        frame = Frame(LEFT, BOTTOM, CONTENT_WIDTH, HEIGHT - TOP - BOTTOM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='official', frames=frame, onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        logo = ROOT / 'assets/images/official/arknox-watermark.png'
        canvas.setFillAlpha(.065)
        canvas.drawImage(str(logo), LEFT, (HEIGHT - 474.6) / 2, 474.6, 474.6, mask='auto')
        canvas.restoreState()
        if doc.page > 1:
            canvas.saveState()
            canvas.drawImage(str(ROOT / 'assets/images/official/arknox-header.png'), LEFT, HEIGHT - 57, 24, 24, mask='auto')
            canvas.setFont('Company', 11)
            canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 40, 'Arknox')
            canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 54, 'www.arknox.in')
            canvas.restoreState()

    def afterFlowable(self, flowable):
        chapter_id = getattr(flowable, 'chapter_id', None)
        if chapter_id:
            self.chapter_pages[chapter_id] = self.page
            self.canv.bookmarkPage(chapter_id)
            self.canv.addOutlineEntry(flowable.getPlainText(), chapter_id, 0, False)
            self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, chapter_id))


def chapter_heading(chapter):
    heading = para(chapter['title'], 'chapter')
    heading.chapter_id = chapter['id']
    return heading


