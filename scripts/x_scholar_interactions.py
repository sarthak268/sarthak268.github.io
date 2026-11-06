"""Normalize only evidenced interactions, with an explicit direction."""
import collections
import re
import urllib.parse

KINDS = {'replies', 'reposts', 'quotes', 'likes'}
DIRECTIONS = {'incoming', 'outgoing'}


def valid_id(value):
    return bool(re.fullmatch(r'\d+', str(value or '')))


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
    return {'handle': handle, 'name': name, 'profile_url': f'https://x.com/{handle}',
            'avatar_url': avatar, 'initials': ''.join(word[0] for word in name.split()[:2]).upper()}


def interaction(user, owner, kind, direction, post_id, evidence_id):
    profile = profile_from(user, owner)
    if not profile or kind not in KINDS or direction not in DIRECTIONS:
        return None
    if not valid_id(post_id) or not valid_id(evidence_id):
        return None
    author = owner if direction == 'outgoing' else profile['handle']
    # A like/repost is evidenced by its source list, rather than a new post.
    if kind in {'likes', 'reposts'}:
        target_author = owner if direction == 'incoming' else profile['handle']
        url = f'https://x.com/{target_author}/status/{post_id}'
    else:
        url = f'https://x.com/{author}/status/{evidence_id}'
    return {'profile': profile, 'evidence': {'kind': kind, 'direction': direction,
            'post_id': str(post_id), 'id': str(evidence_id), 'url': url}}


def outgoing_from_status(raw, owner):
    if raw.get('type', 'status') != 'status':
        return []
    result = []
    author = raw.get('author') or {}
    reposter = raw.get('reposted_by') or {}
    if reposter.get('screen_name', '').lower() == owner.lower():
        result.append(interaction(author, owner, 'reposts', 'outgoing', raw.get('id'), raw.get('id')))
    if author.get('screen_name', '').lower() == owner.lower():
        quote = raw.get('quote') or {}
        if isinstance(quote, dict) and quote.get('type', 'status') == 'status':
            result.append(interaction(quote.get('author') or {}, owner, 'quotes', 'outgoing',
                                      quote.get('id'), raw.get('id')))
        target = raw.get('replying_to') or {}
        if isinstance(target, dict) and target.get('screen_name'):
            user = {'screen_name': target['screen_name'], 'name': target.get('display_name')}
            result.append(interaction(user, owner, 'replies', 'outgoing',
                                      target.get('status') or raw.get('replying_to_status'), raw.get('id')))
    return [item for item in result if item]


def aggregate(events):
    people = {}
    for item in events:
        if not item:
            continue
        profile, evidence = item['profile'], item['evidence']
        key = profile['handle'].lower()
        person = people.setdefault(key, {**profile, 'evidence': {}})
        # A partial reply target must not overwrite a full name or avatar.
        if profile['name'].lower() != key or person['name'].lower() == key:
            person.update({k: v for k, v in profile.items() if v})
        event_key = (evidence['direction'], evidence['kind'], evidence['id'], evidence['post_id'])
        person['evidence'][event_key] = evidence
    output = []
    for person in people.values():
        evidence = sorted(person.pop('evidence').values(),
                          key=lambda e: (e['direction'], e['kind'], int(e['id']), int(e['post_id'])))
        counts = collections.Counter(e['kind'] for e in evidence)
        directions = collections.Counter(e['direction'] for e in evidence)
        output.append({**person, 'interaction_count': len(evidence),
                       'post_count': len({e['post_id'] for e in evidence}),
                       'incoming': directions['incoming'], 'outgoing': directions['outgoing'],
                       **{kind: counts[kind] for kind in sorted(KINDS)}, 'evidence': evidence})
    return sorted(output, key=lambda p: (-p['interaction_count'],
                  -min(p['incoming'], p['outgoing']), p['handle'].lower()))
