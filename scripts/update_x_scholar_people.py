#!/usr/bin/env python3
"""Collect evidenced interactions in both directions for the X Scholar sidebar."""
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

from x_scholar_interactions import aggregate, interaction, outgoing_from_status
from x_scholar_x_api import collect_likes

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


def collect_events(responses, owner):
    events = []
    for response in responses:
        kind, root_id = response['kind'], response['post_id']
        for item in response['entries']:
            if kind == 'reposts':
                user, evidence_id = item, root_id
            else:
                if item.get('type', 'status') != 'status':
                    continue
                events.extend(outgoing_from_status(item, owner))
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
            events.append(interaction(user, owner, kind, 'incoming', root_id, evidence_id))
    return [event for event in events if event]


def fetch_outgoing_replies(owner, max_pages):
    """Alternate timelines may expose replies; a 404 is unavailable, not zero replies."""
    events, cursor, seen = [], None, set()
    metadata = {'available': False, 'pages': 0, 'complete': False}
    for _ in range(max_pages):
        query = {'count': 100, 'with_replies': '1'}
        if cursor:
            query['cursor'] = cursor
        url = API + '/2/profile/' + owner + '/statuses?' + urllib.parse.urlencode(query)
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Sarthak-X-Scholar/2.0'})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = json.load(response)
            if data.get('code') != 200:
                raise ValueError('Timeline unavailable')
        except (urllib.error.URLError, TimeoutError, ValueError):
            metadata['error'] = True
            break
        metadata['available'] = True
        metadata['pages'] += 1
        for raw in data.get('results', []):
            events.extend(outgoing_from_status(raw, owner))
        following = (data.get('cursor') or {}).get('bottom')
        if not data.get('results') or not following or following in seen:
            metadata['complete'] = True
            break
        cursor = following
        seen.add(cursor)
        time.sleep(.25)
    return events, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-pages', type=int, default=3)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--snapshot', type=Path, default=ROOT / '_data' / 'x_scholar.json')
    parser.add_argument('--timeline-pages', type=int, default=30)
    parser.add_argument('--likes-post-limit', type=int, default=25)
    parser.add_argument('--output', type=Path, default=ROOT / '_data' / 'x_scholar_people.json')
    args = parser.parse_args()
    if min(args.max_pages, args.timeline_pages, args.likes_post_limit) < 1 or not 1 <= args.workers <= 8:
        parser.error('Use positive page counts and 1–8 workers.')
    snapshot = json.loads(args.snapshot.read_text())
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
    # Do not publish an outgoing-only list when the incoming source has failed.
    if jobs and not any(response['pages'] for response in responses):
        raise RuntimeError('All incoming interaction lists failed; existing snapshot left unchanged.')
    events = collect_events(responses, owner)
    events.extend(snapshot.get('outgoing_interactions', []))
    replies, reply_coverage = fetch_outgoing_replies(owner, args.timeline_pages)
    events.extend(replies)
    likes, like_coverage = collect_likes(owner, snapshot['posts'], args.max_pages, args.likes_post_limit)
    events.extend(likes)
    people = aggregate(events)
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
            'scope': 'Observed replies, reposts, and quotes in both directions, plus authenticated likes when available. A sample, not a complete history.',
            'ranking': 'Deduplicated interactions in both directions; ties favor mutual interactions, then handle.',
            'outgoing_reply_coverage': reply_coverage, 'likes_coverage': like_coverage,
            'people': people}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(args.output)
    print(f'Saved {len(people)} verified profiles. Likes: {like_coverage["status"]}.', flush=True)
    for person in people[:8]:
        print(f'  @{person["handle"]}: {person["incoming"]} incoming, {person["outgoing"]} outgoing', flush=True)


if __name__ == '__main__':
    main()
