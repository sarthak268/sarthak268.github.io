#!/usr/bin/env python3
"""Refresh a static X Scholar snapshot from the public FxTwitter API."""
import argparse
import collections
import datetime as dt
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.fxtwitter.com'


def fetch(path):
    request = urllib.request.Request(API + path, headers={
        'User-Agent': 'Sarthak-X-Scholar/1.0 (public profile snapshot)',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    if data.get('code') != 200:
        raise RuntimeError(f'API returned {data.get("code")}: {data.get("message", path)}')
    return data


def h_index(posts):
    likes = sorted((p['likes'] for p in posts if p['likes'] is not None), reverse=True)
    return max((rank for rank, count in enumerate(likes, 1) if count >= rank), default=0)


def metrics(posts):
    return {'likes': sum(p['likes'] or 0 for p in posts),
            'h_index': h_index(posts),
            'i10_index': sum(p['likes'] is not None and p['likes'] >= 10 for p in posts)}


def make_post(raw, handle):
    if raw.get('type', 'status') != 'status':
        return None
    if raw.get('author', {}).get('screen_name', '').lower() != handle.lower():
        return None  # Reposts of other authors are not this profile's publications.
    if raw.get('replying_to') or raw.get('replying_to_status'):
        return None
    text = raw.get('text', '').strip()
    if not text or not re.fullmatch(r'\d+', str(raw.get('id', ''))):
        return None
    timestamp = raw.get('created_timestamp')
    if timestamp:
        date = dt.datetime.fromtimestamp(timestamp, dt.timezone.utc)
    else:
        date = dt.datetime.strptime(raw['created_at'], '%a %b %d %H:%M:%S %z %Y')
    # Remove standalone shortlinks from the displayed title; retain original text for search/export.
    title = re.sub(r'https?://\S+', '', text)
    title = re.sub(r'\s+', ' ', title).strip() or text
    if len(title) > 260:
        title = title[:257].rsplit(' ', 1)[0] + '…'
    likes = raw.get('likes')
    likes = likes if isinstance(likes, int) and likes >= 0 else None
    return {
        'id': str(raw['id']), 'url': f'https://x.com/{handle}/status/{raw["id"]}',
        'text': text, 'title': title, 'date': date.date().isoformat(), 'year': date.year,
        'likes': likes, 'reposts': raw.get('reposts', raw.get('retweets')),
        'replies': raw.get('replies'), 'views': raw.get('views'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--handle', default='sarthak__bhagat')
    parser.add_argument('--max-pages', type=int, default=30)
    parser.add_argument('--output', type=Path, default=ROOT / '_data' / 'x_scholar.json')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]{1,15}', args.handle) or args.max_pages < 1:
        parser.error('Use a valid X handle and a positive page limit.')
    profile = fetch('/' + args.handle)['user']
    posts = {}
    cursor = None
    seen_cursors = set()
    complete = False
    for page in range(args.max_pages):
        query = {'count': 100}
        if cursor:
            query['cursor'] = cursor
        try:
            data = fetch('/2/profile/' + args.handle + '/statuses?' + urllib.parse.urlencode(query))
        except urllib.error.HTTPError as error:
            if error.code == 404 and posts:
                complete = True
                break
            raise
        results = data.get('results', [])
        for raw in results:
            post = make_post(raw, args.handle)
            if post:
                posts[post['id']] = post
        print(f'Page {page + 1}: {len(results)} timeline entries; {len(posts)} original posts indexed.', flush=True)
        next_cursor = (data.get('cursor') or {}).get('bottom')
        if not results or not next_cursor or next_cursor == cursor or next_cursor in seen_cursors:
            complete = True
            break
        seen_cursors.add(next_cursor)
        cursor = next_cursor
        time.sleep(0.25)
    if not posts:
        raise RuntimeError('No original posts returned; existing snapshot left unchanged.')
    # The timeline can omit pinned posts; explicitly included IDs survive refreshes.
    known_ids = set()
    required_ids = set()
    include_path = ROOT / '_data' / 'x_scholar_includes.json'
    if include_path.exists():
        includes = json.loads(include_path.read_text())
        required_ids.update(str(post_id) for post_id in includes.get('post_ids', [])
                            if re.fullmatch(r'\d+', str(post_id)))
        known_ids.update(required_ids)
    # Also include older public posts already linked from this website.
    for path in [ROOT / 'index.md', *sorted((ROOT / '_pages').glob('*.md'))]:
        known_ids.update(re.findall(r'(?:x\.com|twitter\.com)/' + re.escape(args.handle) + r'/status/(\d+)', path.read_text()))
    for post_id in sorted(known_ids - posts.keys()):
        try:
            raw = fetch('/' + args.handle + '/status/' + post_id)['tweet']
            post = make_post(raw, args.handle)
            if post:
                posts[post['id']] = post
            elif post_id in required_ids:
                raise RuntimeError(f'Included post {post_id} is not an original post by @{args.handle}.')
        except (urllib.error.HTTPError, KeyError, RuntimeError) as error:
            if post_id in required_ids:
                raise RuntimeError(f'Could not refresh required post {post_id}; existing snapshot left unchanged.') from error
            print(f'Could not refresh linked post {post_id}: {error}', flush=True)
    now = dt.datetime.now(dt.timezone.utc)
    since_year = now.year - 5
    ordered = sorted(posts.values(), key=lambda p: (p['likes'] if p['likes'] is not None else -1, p['id']), reverse=True)
    yearly = collections.defaultdict(int)
    for post in ordered:
        yearly[post['year']] += post['likes'] or 0
    max_likes = max(yearly.values(), default=1) or 1
    years = [{'year': year, 'likes': count, 'height': round(count / max_likes * 100, 2)}
             for year, count in sorted(yearly.items())]
    snapshot = {
        'handle': args.handle, 'name': profile['name'], 'profile_url': f'https://x.com/{args.handle}',
        'followers': profile.get('followers'), 'updated_at': now.isoformat(),
        'updated_date': now.date().isoformat(), 'since_year': since_year,
        'source': API, 'timeline_exhausted': complete,
        'scope': 'Original posts and quote posts returned by the public timeline; replies and reposts excluded.',
        'post_count': len(ordered), 'metrics': metrics(ordered),
        'recent_metrics': metrics([p for p in ordered if p['year'] >= since_year]),
        'years': years, 'posts': ordered,
    }
    # Replace atomically only after a successful fetch and validation.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(args.output)
    print(f'Saved {len(ordered)} posts to {args.output}; {snapshot["metrics"]}.', flush=True)


if __name__ == '__main__':
    main()
