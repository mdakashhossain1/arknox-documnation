import json
from pathlib import Path

import pymupdf


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'assets/js/pdf-manifest.js').read_text(encoding='utf-8').split(' = ', 1)[1].rstrip(';\n'))
issues = []
counts = {}
for path in (root / 'pdfs').glob('*.pdf'):
    with pymupdf.open(path) as document:
        counts[path.name] = len(document)
        for index, page in enumerate(document):
            text = page.get_text()
            if not text.strip():
                issues.append(f'{path.name}: blank page {index + 1}')
            if f'Page {index + 1} of {len(document)}' not in text:
                issues.append(f'{path.name}: incorrect footer on page {index + 1}')
            for block in page.get_text('blocks'):
                x0, y0, x1, y1, *_ = block
                if x0 < 18 or y0 < 12 or x1 > page.rect.width - 18 or y1 > page.rect.height - 18:
                    issues.append(f'{path.name}: content beyond page bounds on page {index + 1}')
with pymupdf.open(root / manifest['full']) as full:
    for chapter_id, chapter in manifest['chapters'].items():
        if chapter_id != 'overview' and chapter['title'] not in full[chapter['page'] - 1].get_text().replace('\n', ' '):
            issues.append(f'Wrong chapter start: {chapter_id}')
    text = ' '.join(page.get_text() for page in full)
    for required in ['XP_PER_LEVEL', 'FCM_CREDENTIALS_PATH', 'DEFAULT_DAILY_QUIZ_TARGET', 'Conclusion Section']:
        if required not in text:
            issues.append(f'Missing reference: {required}')
print(json.dumps({'files': len(counts), 'full_pages': counts.get('quizs-documentation.pdf'), 'issues': issues}, indent=2))
if issues:
    raise SystemExit(1)
