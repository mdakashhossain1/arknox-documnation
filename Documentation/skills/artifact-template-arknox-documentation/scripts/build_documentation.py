import argparse
import html
import json
import re
import shutil
from pathlib import Path

from PIL import Image
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Spacer
from reportlab.platypus.tableofcontents import TableOfContents

import layout_engine as layout


SKILL = Path(__file__).resolve().parents[1]


def safe_path(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'Asset path must remain inside output: {value}')
    return path


def validate(data, output):
    for key in ('project', 'intro', 'chapters'):
        if not data.get(key):
            raise ValueError(f'Missing {key}')
    ids = {'overview', 'conclusion'}
    for chapter in data['chapters']:
        for key in ('id', 'title', 'intro', 'steps', 'fields', 'verify', 'sources'):
            if not chapter.get(key):
                raise ValueError(f'Chapter requires {key}: {chapter.get("id")}')
        identifier = chapter['id']
        if identifier in ids or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier):
            raise ValueError(f'Duplicate, reserved, or invalid chapter id: {identifier}')
        ids.add(identifier)
        if any(len(row) != 3 for row in chapter['fields']):
            raise ValueError(f'Field rows need three cells: {identifier}')
        for item in [chapter, *chapter.get('gallery', [])]:
            if not item.get('imageFile'):
                continue
            path = safe_path(output, item['imageFile'])
            if not path.is_file():
                raise ValueError(f'Missing screenshot: {path}')
            points = item.get('points', [])
            if len(points) != len(item.get('marks', [])):
                raise ValueError(f'One legend per annotation required: {path}')
            if path.suffix.lower() != '.svg':
                with Image.open(path) as image:
                    width, height = image.size
                for point in points:
                    if len(point) != 4 or not all(0 <= value <= (width if i % 2 == 0 else height) for i, value in enumerate(point)):
                        raise ValueError(f'Annotation outside screenshot: {path}')


def contact():
    return [layout.para('By: <b>Arknox</b>'), layout.para('Email: info@arknox.in'), layout.para('Contact: +91-8787388949'), Spacer(1, 14)]


def cover(data):
    story = [layout.para(html.escape(data['project']), 'title'), layout.para(html.escape(data.get('subtitle', 'Administrator and Application Documentation')), 'subtitle'), *contact(), layout.para(data['intro'])]
    for title, text in data.get('overview', []):
        story += [layout.para(title, 'heading'), *layout.rich_blocks(text)]
    story += [layout.para('How to use this document', 'heading'), layout.para('The complete PDF is continuous, with contents and chapter bookmarks. Open index.html for sidebar navigation, page controls, and full or chapter PDF downloads. All reader assets are local.'), layout.para('Screenshot provenance', 'heading'), layout.para(data.get('provenance', 'Consult each screenshot caption for its capture environment and verification limits.'))]
    return story


def closing(data):
    story = [layout.para('Conclusion Section', 'chapter'), layout.para(data.get('conclusion', f'Use this guide to configure and verify {html.escape(data["project"])}. Confirm each documented workflow in the intended environment.'))]
    if data.get('access'):
        story += [layout.para('Administrator access', 'heading'), layout.para(data['access'])]
    if data.get('release_checks'):
        story.append(layout.para('Release verification', 'heading'))
        story += [layout.para(f'{i}. {text}') for i, text in enumerate(data['release_checks'], 1)]
    return story + [layout.para('Contact for support', 'heading'), layout.para('Email: info@arknox.in<br/>Support Center: +91-8787388949'), layout.para('Arknox', 'small')]


def figure(item):
    if not item.get('imageFile'):
        return []
    caption = item.get('caption', 'Illustrative diagram - not a live screenshot' if item.get('illustrative') else 'Actual local preview - values may differ')
    story = [Spacer(1, 8), layout.Screenshot(item), layout.para(caption, 'caption')]
    story += [layout.para(f'<b>{i}.</b> {text}', 'small') for i, text in enumerate(item.get('marks', []), 1)]
    return story + [Spacer(1, 7)]


def chapter_body(chapter):
    story = [layout.para(chapter['intro'])]
    if chapter.get('path'):
        story.append(layout.para('Screen / location: ' + chapter['path'], 'small'))
    story += figure(chapter) + [layout.para('Step by step', 'heading')]
    story += [layout.para(f'<b>{i}.</b> {text}') for i, text in enumerate(chapter['steps'], 1)]
    story += [layout.para('Field definitions and change impact', 'heading'), layout.grid([['Field / Feature', 'Definition and source', 'Effect of changes'], *chapter['fields']]), Spacer(1, 10)]
    if chapter.get('note'):
        story.append(layout.para('<b>Current implementation limit</b><br/>' + chapter['note'], 'note'))
    for title, text in chapter.get('details', []):
        story += [layout.para(title, 'heading'), *layout.rich_blocks(text)]
    story += [layout.para('Verification after saving', 'heading'), layout.para(chapter['verify'])]
    for item in chapter.get('gallery', []):
        story += [layout.para(item['title'], 'heading'), layout.para(item.get('intro', '')), *figure(item)]
    story += [layout.para('Technical sources', 'heading')]
    story += [layout.para(html.escape(source), 'small') for source in chapter['sources']]
    return story


def build(data, output):
    validate(data, output)
    output.mkdir(parents=True, exist_ok=True)
    branding = output / 'assets/images/official'
    branding.mkdir(parents=True, exist_ok=True)
    for name in ('arknox-header.png', 'arknox-watermark.png'):
        shutil.copy2(SKILL / 'assets/branding' / name, branding / name)
    pdfs, pages = output / 'pdfs', output / 'assets/pdf-pages'
    pdfs.mkdir(exist_ok=True)
    pages.mkdir(parents=True, exist_ok=True)
    layout.ROOT = output
    layout.register_fonts()
    story = cover(data) + [PageBreak(), layout.para('Contents', 'chapter')]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOC', parent=layout.STYLES['body'], alignment=TA_LEFT, fontSize=10, leading=13.5, spaceBefore=3, spaceAfter=0)]
    story += [toc, PageBreak()]
    for chapter in data['chapters']:
        story += [layout.chapter_heading(chapter), *chapter_body(chapter), PageBreak()]
    story += closing(data)
    title = data['project'] + ' Documentation'
    document = layout.OfficialDocument(pdfs / 'documentation.pdf', title)
    document.multiBuild(story, canvasmaker=layout.NumberedCanvas)
    entries = {'overview': {'title': 'Overview', 'page': 1, 'pdf': 'pdfs/overview.pdf', 'group': 'Start here'}}
    for chapter in data['chapters']:
        entries[chapter['id']] = {'title': chapter['title'], 'label': chapter.get('label', chapter['title']), 'page': document.chapter_pages[chapter['id']], 'pdf': f'pdfs/{chapter["id"]}.pdf', 'group': chapter.get('group', 'Guide')}
    overview = layout.OfficialDocument(pdfs / 'overview.pdf', title)
    overview.build(cover(data) + [PageBreak(), *closing(data)], canvasmaker=layout.NumberedCanvas)
    for chapter in data['chapters']:
        chapter_doc = layout.OfficialDocument(pdfs / f'{chapter["id"]}.pdf', chapter['title'])
        chapter_doc.build([layout.chapter_heading(chapter), *contact(), *chapter_body(chapter), Spacer(1, 14), *closing(data)], canvasmaker=layout.NumberedCanvas)
    with layout.fitz.open(pdfs / 'documentation.pdf') as pdf:
        for i, page in enumerate(pdf, 1):
            page.get_pixmap(matrix=layout.fitz.Matrix(1.6, 1.6), alpha=False).save(str(pages / f'page-{i:03d}.jpg'), jpg_quality=85)
        manifest = {'project': data['project'], 'full': 'pdfs/documentation.pdf', 'pages': len(pdf), 'pageWidth': layout.WIDTH, 'pageHeight': layout.HEIGHT, 'chapters': entries}
    (output / 'manifest.js').write_text('window.arknoxManual = ' + json.dumps(manifest, ensure_ascii=False) + ';\n', encoding='utf-8')
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    for name in ('index.html', 'reader.css', 'reader.js'):
        shutil.copy2(SKILL / 'assets/reader' / name, output / name)
    source = output / 'content.json'
    source.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(output), 'pages': manifest['pages'], 'pdfs': len(entries) + 1}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(json.loads(args.content.read_text(encoding='utf-8-sig')), args.output.resolve())


if __name__ == '__main__':
    main()
