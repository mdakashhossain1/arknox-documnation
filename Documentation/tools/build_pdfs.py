import argparse
import html
import json
import math
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
ORDER = ['overview', 'requirements', 'cpanel-setup', 'local-terminal', 'admin-login-dash', 'admin-categories', 'admin-quizzes', 'admin-questions', 'admin-attempts', 'admin-users', 'admin-notifications', 'admin-settings', 'admin-targets', 'admin-attendance', 'admin-offerwall', 'admin-list-guide', 'settings-general', 'settings-email', 'settings-firebase', 'settings-captcha', 'settings-migrations', 'environment-settings', 'app-walkthrough', 'app-profile-guide', 'app-results-guide', 'app-attendance-guide', 'app-achievements-guide', 'app-inbox-guide', 'customization-map', 'troubleshooting', 'mobile-app', 'firebase-google', 'monetization', 'build-publish', 'delivery-agreement']
STYLES = {}
SCREENSHOTS = {}


def register_fonts():
    directory = Path('C:/Windows/Fonts')
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
        self.path = ROOT / item.get('imageFile', f"assets/images/walkthrough/{item['image']}.jpg")
        metadata = SCREENSHOTS.get(item['image'], {})
        if self.path.suffix == '.svg':
            self.drawing = svg2rlg(str(self.path))
            self.source_width, self.source_height = self.drawing.width, self.drawing.height
        else:
            self.drawing = None
            from PIL import Image
            with Image.open(self.path) as image:
                self.source_width, self.source_height = image.size
        self.points = metadata.get('points', [])
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
            if not point or not 3 <= point['y'] <= 96:
                continue
            x = min(96, point['x'] + 9) / 100 * self.width
            y = self.height - max(4, point['y'] - 6) / 100 * self.height
            end_x, end_y = point['x'] / 100 * self.width, self.height - point['y'] / 100 * self.height
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


def figures(item):
    if not item.get('image'):
        return []
    story = [Spacer(1, 8), Screenshot(item)]
    caption = 'Illustrative setup map - not a live hosting screenshot' if item.get('illustrative') else 'Actual source preview - local demo data - live values may differ'
    story.append(para(caption, 'caption'))
    for index, text in enumerate(item.get('marks', [])):
        story.append(para(f'<b>{index + 1}.</b> {text}', 'small'))
    story.append(Spacer(1, 7))
    return story


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


def contact_block():
    return [para('By: <b>Arknox</b>'), para('Email: info@arknox.in'), para('Contact: +91-8787388949'), Spacer(1, 14)]


def closing():
    return [para('Conclusion Section', 'chapter'), para('Use this guide to configure Quizs, verify the actual app behavior, and keep administrator content, server configuration, and native app changes in their correct places.'), para('Administrator access', 'heading'), para('Open your own backend domain followed by /admin/login. Use the credentials created for that deployment. Accounts, passwords, and URLs from unrelated reference projects do not apply to Quizs.'), para('Release verification', 'heading'), para('Complete a category, quiz, question, attempt, result, target/profile, notification, and attendance test. Confirm native integrations separately on the intended device and provider account.'), para('Contact for support', 'heading'), para('Email: info@arknox.in<br/>Support Center: +91-8787388949'), para('Arknox', 'small')]


def structured_story(chapter):
    story = [para(chapter.get('intro', ''))]
    if chapter.get('path'):
        story.append(para(f"Screen / location: {chapter['path']}", 'small'))
    story += figures(chapter)
    story.append(para('Step by step', 'heading'))
    for index, step in enumerate(chapter['steps']):
        story.append(para(f'<b>{index + 1}.</b> {step}'))
    story += [para('Field definitions and change impact', 'heading'), grid([['Field / Feature', 'Definition and source', 'Effect of changes'], *chapter['fields']]), Spacer(1, 10)]
    if chapter.get('note'):
        story.append(para(f"<b>Current implementation limit</b><br/>{chapter['note']}", 'note'))
    if chapter.get('details'):
        story.append(para('Data and behavior in detail', 'heading'))
        for title, text in chapter['details']:
            story.append(para(title, 'heading'))
            story += rich_blocks(text)
    story += [para('Verification after saving', 'heading'), para(chapter['verify'])]
    for gallery in chapter.get('gallery', []):
        story += [para(gallery['title'], 'heading'), para(gallery['intro'])] + figures(gallery)
    story.append(para('Technical sources', 'heading'))
    story.append(para('Server paths are inside Quiz Application Admin; lib paths are inside Quiz Application.', 'small'))
    for source in chapter['sources']:
        story.append(para(source, 'small'))
    return story


def html_story(section):
    story = []

    def visit(node):
        if isinstance(node, NavigableString):
            return
        if node.name in ['script', 'style', 'svg', 'button', 'h1']:
            return
        if node.name in ['h2', 'h3', 'h4', 'h5']:
            story.append(para(str(node), 'heading'))
        elif node.name == 'pre':
            story.extend(rich_blocks(str(node)))
        elif node.name == 'table':
            rows = [[str(cell) for cell in row.find_all(['th', 'td'], recursive=False)] for row in node.find_all('tr')]
            if rows:
                widths = [CONTENT_WIDTH / len(rows[0])] * len(rows[0])
                story.extend([grid(rows, widths), Spacer(1, 10)])
        elif node.name in ['p', 'li']:
            if node.get_text(strip=True):
                story.append(para(str(node)))
        elif node.name == 'img':
            return
        else:
            for child in node.children:
                visit(child)

    for child in section.children:
        visit(child)
    return story


def overview_story():
    return [para('Quizs', 'title'), para('Administrator and Application Documentation', 'subtitle'), *contact_block(), para('Quizs combines a Laravel administrator panel and API with a Flutter quiz application. This guide explains setup, content management, account controls, notifications, settings, environment variables, and the sources behind app statistics.'), para('Read the step-by-step workflows, field references, screenshots, and verification notes before changing a feature. Administrator saves, server configuration, and app releases affect different parts of the system.'), para('Administrator Features', 'heading'), para('Manage categories, quizzes, bilingual questions, attempts, users, attendance, notifications, and default daily targets. Inspect analytics and reporting using their actual database definitions.'), para('Application Features', 'heading'), para('Follow authentication, quiz answering, explanations, results, profile statistics, attendance, achievements, and inbox flows. Native push, sign-in, ads, and app updates require separate device/provider verification.'), para('How to use this document', 'heading'), para('The complete PDF is continuous and includes a contents page and PDF bookmarks. The index.html reader adds sidebar navigation. Download the full manual or one chapter; both use the same official document format.'), para('Screenshot provenance', 'heading'), para('Screenshots use this project’s local demo data. The cPanel setup map is illustrative. The faint logo, publisher header, purple headings, justified body text, and conclusion treatment follow the supplied official format reference.')]


def main():
    global SCREENSHOTS
    parser = argparse.ArgumentParser()
    parser.add_argument('--node', required=True)
    args = parser.parse_args()
    exported = json.loads(subprocess.check_output([args.node, str(ROOT / 'tools/export_content.cjs')], text=True, encoding='utf-8'))
    SCREENSHOTS = exported['screenshots']
    dynamic = {chapter['id']: chapter for chapter in exported['chapters']}
    soup = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
    sections = {section['id']: section for section in soup.select('section.doc-section')}
    PDF_DIR.mkdir(exist_ok=True)
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    titles = {}
    for chapter_id in ORDER:
        titles[chapter_id] = dynamic[chapter_id]['title'] if chapter_id in dynamic else sections[chapter_id].find('h1').get_text(' ', strip=True)
    titles['overview'] = 'Quizs Administrator and Application Documentation'

    def content(chapter_id):
        if chapter_id == 'overview':
            return overview_story()
        if chapter_id in dynamic:
            return structured_story(dynamic[chapter_id])
        return html_story(sections[chapter_id])

    story = content('overview') + [PageBreak(), para('Contents', 'chapter')]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOC', parent=STYLES['body'], alignment=TA_LEFT, fontSize=10, leading=13.5, spaceBefore=3, spaceAfter=0)]
    story += [toc, PageBreak()]
    for chapter_id in ORDER[1:]:
        chapter = {'id': chapter_id, 'title': titles[chapter_id]}
        story += [chapter_heading(chapter), *content(chapter_id), PageBreak()]
    story += closing()
    full = OfficialDocument(PDF_DIR / 'quizs-documentation.pdf', titles['overview'])
    full.multiBuild(story, canvasmaker=NumberedCanvas)
    chapter_pages = {'overview': 1, **full.chapter_pages}
    for chapter_id in ORDER:
        chapter = {'id': chapter_id, 'title': titles[chapter_id]}
        story = content(chapter_id) if chapter_id == 'overview' else [chapter_heading(chapter), *contact_block(), *content(chapter_id)]
        story += [Spacer(1, 14), *closing()]
        document = OfficialDocument(PDF_DIR / f'{chapter_id}.pdf', titles[chapter_id])
        document.build(story, canvasmaker=NumberedCanvas)
    pdf = fitz.open(PDF_DIR / 'quizs-documentation.pdf')
    for index, page in enumerate(pdf):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
        pixmap.save(str(PAGE_DIR / f'page-{index + 1:03d}.jpg'), jpg_quality=85)
    manifest = {'full': 'pdfs/quizs-documentation.pdf', 'pages': len(pdf), 'pageWidth': WIDTH, 'pageHeight': HEIGHT, 'chapters': {chapter_id: {'page': chapter_pages[chapter_id], 'title': titles[chapter_id], 'pdf': f'pdfs/{chapter_id}.pdf'} for chapter_id in ORDER}}
    (ROOT / 'assets/js/pdf-manifest.js').write_text('window.quizsPdfManifest = ' + json.dumps(manifest, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    print(json.dumps({'pdfs': len(ORDER) + 1, 'full_pages': len(pdf), 'chapter_pages': chapter_pages, 'full_size_mb': round((PDF_DIR / 'quizs-documentation.pdf').stat().st_size / 1048576, 2)}, indent=2))


if __name__ == '__main__':
    main()
