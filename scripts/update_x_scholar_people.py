#!/usr/bin/env python3
"""Collect verifiable public reply/repost/quote authors for the X Scholar sidebar."""
import argparse
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def fetch_pages(job, max_pages):
    kind, post_id = job
    if kind == 'replies':
        path, key = f'/2/conversation/{post_id}', 'replies'
    else:
        path, key = f'/2/status/{post_id}/{kind}', 'results'
    entries = []
    cursor = None
    seen = set()
    pages = 0
    complete = False
    error = None
    for page in range(max_pages):
        query = {} if kind == 'replies' else {'count': 100}
        if cursor:
            query['cursor'] = cursor
        url = API + path + ('?' + urllib.parse.urlencode(query) if query else '')
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Sarthak-X-Scholar/1.0', 'Accept': 'application/json'})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = json.load(response)
            if data.get('code') != 200:
                error = f'API {data.get("code")}'
                break
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            error = str(exc)
            break
        pages += 1
        batch = data.get(key) or []
        entries.extend(batch)
        following = (data.get('cursor') or {}).get('bottom')
        if not batch or not following or following in seen:
            complete = True
            break
        seen.add(following)
        cursor = following
        time.sleep(0.15)
    return {'kind': kind, 'post_id': post_id, 'entries': entries, 'pages': pages,
            'complete': complete, 'error': error}


def profile_from(user, owner):
    handle = user.get('screen_name', '')
    if not re.fullmatch(r'[A-Za-z0-9_]{1,15}', handle) or handle.lower() == owner.lower():
        return None
    if user.get('protected'):
        return None
    avatar = user.get('avatar_url') or ''
    parsed = urllib.parse.urlparse(avatar)
    if parsed.scheme != 'https' or parsed.hostname not in {'pbs.twimg.com', 'abs.twimg.com'}:
        avatar = ''
    name = user.get('name') or handle
    initials = ''.join(word[0] for word in name.split()[:2]).upper()
    return {'handle': handle, 'name': name, 'profile_url': f'https://x.com/{handle}',
            'avatar_url': avatar, 'initials': initials}


def collect_people(responses, owner):
    people = {}
    for response in responses:
        kind, root_id = response['kind'], response['post_id']
        for item in response['entries']:
            if kind == 'reposts':
                user, evidence_id = item, root_id
                evidence_url = f'https://x.com/{owner}/status/{root_id}/retweets'
            else:
                if item.get('type', 'status') != 'status':
                    continue
                user = item.get('author') or {}
                evidence_id = str(item.get('id', ''))
                if not re.fullmatch(r'\d+', evidence_id):
                    continue
                if kind == 'replies':
                    target = item.get('replying_to') or {}
                    if not isinstance(target, dict) or target.get('screen_name', '').lower() != owner.lower():
                        continue
                else:
                    quote = item.get('quote') or {}
                    if not isinstance(quote, dict) or str(quote.get('id', '')) != root_id:
                        continue
                evidence_url = f'https://x.com/{user.get("screen_name")}/status/{evidence_id}'
            profile = profile_from(user, owner)
            if not profile:
                continue
            key = profile['handle'].lower()
            if key not in people:
                people[key] = {**profile, 'evidence': {}, 'post_ids': set()}
            person = people[key]
            # A person reposting several posts counts once as a person, once per post as an interaction.
            person['evidence'][(kind, evidence_id)] = {'kind': kind, 'post_id': root_id,
                                                      'id': evidence_id, 'url': evidence_url}
            person['post_ids'].add(root_id)
    output = []
    for person in people.values():
        evidence = list(person['evidence'].values())
        counts = collections.Counter(e['kind'] for e in evidence)
        output.append({k: v for k, v in person.items() if k not in {'evidence', 'post_ids'}} | {
            'post_count': len(person['post_ids']), 'replies': counts['replies'],
            'reposts': counts['reposts'], 'quotes': counts['quotes'], 'evidence': evidence,
        })
    return sorted(output, key=lambda p: (-p['post_count'], -(p['replies'] + p['quotes']), p['handle'].lower()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-pages', type=int, default=3)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--output', type=Path, default=ROOT / '_data' / 'x_scholar_people.json')
    args = parser.parse_args()
    if args.max_pages < 1 or not 1 <= args.workers <= 8:
        parser.error('Use positive page counts and 1–8 workers.')
    snapshot = json.loads((ROOT / '_data' / 'x_scholar.json').read_text())
    owner = snapshot['handle']
    jobs = []
    for post in snapshot['posts']:
        if (post.get('replies') or 0) > 0:
            jobs.append(('replies', post['id']))
        if (post.get('reposts') or 0) > 0:
            jobs.extend([('reposts', post['id']), ('quotes', post['id'])])
    responses = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = [pool.submit(fetch_pages, job, args.max_pages) for job in jobs]
        for index, future in enumerate(as_completed(pending), 1):
            responses.append(future.result())
            if index % 20 == 0 or index == len(jobs):
                print(f'Checked {index}/{len(jobs)} public interaction lists.', flush=True)
    people = collect_people(responses, owner)
    if not people:
        raise RuntimeError('No verified people returned; existing snapshot left unchanged.')
    coverage = collections.Counter()
    for response in responses:
        if response['pages']:
            coverage[response['kind']] += 1
    now = dt.datetime.now(dt.timezone.utc)
    data = {'handle': owner, 'updated_at': now.isoformat(), 'updated_date': now.date().isoformat(),
            'posts_considered': len(snapshot['posts']), 'people_found': len(people),
            'lists_checked': len(responses), 'lists_available': dict(coverage),
            'scope': 'Verified public replies to the author, reposts, and quote posts on indexed posts. Public API results may be incomplete.',
            'ranking': 'Distinct indexed posts interacted with; ties use replies and quotes, then handle.',
            'people': people[:12]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(args.output)
    print(f'Saved {min(len(people), 12)} profiles from {len(people)} verified people.', flush=True)
    for person in people[:8]:
        print(f'  @{person["handle"]}: {person["post_count"]} posts, {person["replies"]} replies, '
              f'{person["reposts"]} reposts, {person["quotes"]} quotes', flush=True)


if __name__ == '__main__':
    main()
