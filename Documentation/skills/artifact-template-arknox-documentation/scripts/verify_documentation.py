import argparse
import json
from pathlib import Path

import pymupdf


def verify(root):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    issues = []
    files = [manifest['full'], *(chapter['pdf'] for chapter in manifest['chapters'].values())]
    for name in files:
        path = root / name
        if not path.is_file():
            issues.append('Missing PDF: ' + name)
            continue
        with pymupdf.open(path) as pdf:
            if pdf.metadata.get('author') != 'Arknox':
                issues.append('Incorrect author: ' + name)
            text = ''.join(page.get_text() for page in pdf)
            if 'info@arknox.in' not in text:
                issues.append('Missing contact email: ' + name)
            for i, page in enumerate(pdf, 1):
                if f'Page {i} of {len(pdf)}' not in page.get_text():
                    issues.append(f'Invalid page footer: {name} page {i}')
                if not page.get_text().strip():
                    issues.append(f'Blank page: {name} page {i}')
                for block in page.get_text('blocks'):
                    x0, y0, x1, y1 = block[:4]
                    if x0 < 18 or y0 < 18 or x1 > page.rect.width - 18 or y1 > page.rect.height - 18:
                        issues.append(f'Content outside page safety bounds: {name} page {i}')
    with pymupdf.open(root / manifest['full']) as pdf:
        if len(pdf) != manifest['pages']:
            issues.append('Manifest page count mismatch')
        for identifier, chapter in manifest['chapters'].items():
            if identifier != 'overview' and chapter['title'] not in pdf[chapter['page'] - 1].get_text():
                issues.append('Incorrect chapter start: ' + identifier)
    for i in range(1, manifest['pages'] + 1):
        if not (root / f'assets/pdf-pages/page-{i:03d}.jpg').is_file():
            issues.append(f'Missing page render: {i}')
    for name in ('index.html', 'reader.css', 'reader.js', 'manifest.js', 'content.json'):
        if not (root / name).is_file():
            issues.append('Missing reader asset: ' + name)
    print(json.dumps({'pdfs': len(files), 'pages': manifest['pages'], 'issues': issues}, indent=2))
    return bool(issues)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(verify(args.output.resolve()))
