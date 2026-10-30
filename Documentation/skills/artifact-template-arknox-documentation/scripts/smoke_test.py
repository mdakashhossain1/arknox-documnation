import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

import build_documentation as builder


def main():
    root = Path(tempfile.mkdtemp(prefix='arknox-skill-test-'))
    image = root / 'assets/images/walkthrough/layout-fixture.png'
    image.parent.mkdir(parents=True)
    with Image.open(builder.SKILL / 'assets/reference.png') as reference:
        reference.save(image)
    data = {
        'project': 'Library Portal Layout Test',
        'intro': 'This synthetic project checks the portable documentation engine. It is not a product guide.',
        'provenance': 'The image is the retained document reference, used only as a layout-test fixture.',
        'release_checks': ['Inspect tables, numbered lists, image annotations, and downloads.'],
        'chapters': [{
            'id': 'catalogue', 'title': 'Manage the catalogue', 'group': 'Test fixture',
            'intro': 'Synthetic text verifies a project title and chapter independent of Quizs.',
            'steps': ['Read the synthetic fixture.', 'Check its formatting without changing application data.'],
            'fields': [[f'Fixture row {i}', 'Synthetic definition for pagination verification.', 'Synthetic effect used to check repeated headers.'] for i in range(1, 31)],
            'details': [['List formatting', '<ol><li>First separate step.</li><li>Second separate step.</li></ol><p>Separate paragraph.</p><pre>KEY=value\nSECOND_KEY=other</pre>']],
            'verify': 'The test verifier should report no structural issues.',
            'sources': ['Synthetic layout fixture; not an application source claim'],
            'imageFile': 'assets/images/walkthrough/layout-fixture.png',
            'caption': 'Retained reference used as a synthetic layout fixture',
            'points': [[120, 150, 250, 200]], 'marks': ['Synthetic annotation position.']
        }]
    }
    source = root / 'content.json'
    source.write_text(json.dumps(data), encoding='utf-8')
    subprocess.run([sys.executable, str(builder.SKILL / 'scripts/build_documentation.py'), '--content', str(source), '--output', str(root)], check=True)
    subprocess.run([sys.executable, str(builder.SKILL / 'scripts/verify_documentation.py'), '--output', str(root)], check=True)
    invalid = json.loads(json.dumps(data))
    invalid['chapters'][0]['imageFile'] = '../outside.png'
    try:
        builder.validate(invalid, root)
    except ValueError:
        pass
    else:
        raise AssertionError('Outside asset paths were not rejected')
    print(json.dumps({'test_output': str(root), 'path_escape_rejected': True}))


if __name__ == '__main__':
    main()
