import argparse
from pathlib import Path
from zipfile import ZipFile


parser = argparse.ArgumentParser()
parser.add_argument('reference')
parser.add_argument('output')
args = parser.parse_args()
destination = Path(args.output)
destination.mkdir(parents=True, exist_ok=True)
with ZipFile(args.reference) as archive:
    for source, name in [('word/media/image135.png', 'arknox-watermark.png'), ('word/media/image136.png', 'arknox-header.png')]:
        (destination / name).write_bytes(archive.read(source))
print('Extracted only the two official branding assets; project screenshots were not imported.')
