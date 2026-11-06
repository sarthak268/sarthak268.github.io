#!/usr/bin/env python3
"""Stage both snapshots before replacing either published data file."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def refresh(root=ROOT, run=subprocess.run):
    with tempfile.TemporaryDirectory(prefix='x-scholar-') as directory:
        staged = Path(directory)
        posts, people = staged / 'posts.json', staged / 'people.json'
        run([sys.executable, str(root / 'scripts/update_x_scholar.py'), '--output', str(posts)], check=True)
        run([sys.executable, str(root / 'scripts/update_x_scholar_people.py'),
             '--snapshot', str(posts), '--output', str(people)], check=True)
        post_data, people_data = json.loads(posts.read_text()), json.loads(people.read_text())
        if not post_data.get('posts') or not people_data.get('people'):
            raise RuntimeError('Empty refresh; published snapshots left unchanged.')
        if post_data['handle'] != people_data['handle']:
            raise RuntimeError('Mismatched accounts; published snapshots left unchanged.')
        for source, name in [(posts, 'x_scholar.json'), (people, 'x_scholar_people.json')]:
            destination = root / '_data' / name
            temporary = destination.with_suffix('.tmp')
            temporary.write_bytes(source.read_bytes())
            temporary.replace(destination)
    print('Both X Scholar snapshots refreshed successfully.', flush=True)


if __name__ == '__main__':
    refresh()
