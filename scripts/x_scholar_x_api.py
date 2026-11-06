"""Optional, read-only X user API access. Credentials stay in environment variables."""
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request

from x_scholar_interactions import interaction

CREDENTIALS = ('X_API_KEY', 'X_API_SECRET', 'X_ACCESS_TOKEN', 'X_ACCESS_TOKEN_SECRET')


def encode(value):
    return urllib.parse.quote(str(value), safe='~')


def authorization(url, values, nonce=None, timestamp=None):
    key, secret, token, token_secret = values
    oauth = {'oauth_consumer_key': key, 'oauth_token': token,
             'oauth_nonce': nonce or secrets.token_hex(16),
             'oauth_timestamp': str(timestamp if timestamp is not None else int(time.time())),
             'oauth_signature_method': 'HMAC-SHA1', 'oauth_version': '1.0'}
    parsed = urllib.parse.urlsplit(url)
    params = list(oauth.items()) + urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    normalized = '&'.join(f'{k}={v}' for k, v in sorted((encode(k), encode(v)) for k, v in params))
    base_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, '', ''))
    base = '&'.join(('GET', encode(base_url), encode(normalized)))
    signing_key = encode(secret) + '&' + encode(token_secret)
    oauth['oauth_signature'] = base64.b64encode(
        hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()).decode()
    return 'OAuth ' + ', '.join(f'{encode(k)}="{encode(v)}"' for k, v in sorted(oauth.items()))


def as_public_profile(user):
    return {'screen_name': user.get('username', ''), 'name': user.get('name'),
            'avatar_url': user.get('profile_image_url'), 'protected': user.get('protected', False)}


class XReadClient:
    def __init__(self, values):
        self.values = values

    def get(self, path, query=None):
        url = 'https://api.x.com/2' + path
        if query:
            url += '?' + urllib.parse.urlencode(query)
        request = urllib.request.Request(url, headers={
            'Authorization': authorization(url, self.values),
            'User-Agent': 'Sarthak-X-Scholar/2.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        if result.get('errors'):
            raise ValueError('X returned an incomplete result')
        return result


def collect_likes(owner, posts, max_pages=3, post_limit=25, client=None):
    values = tuple(os.environ.get(name, '') for name in CREDENTIALS)
    metadata = {'configured': all(values) or client is not None,
                'incoming_available': False, 'outgoing_available': False,
                'incoming_posts_checked': 0, 'outgoing_pages_checked': 0,
                'complete': False}
    if client is None and not all(values):
        metadata['status'] = 'not_connected'
        return [], metadata
    client = client or XReadClient(values)
    events = []
    try:
        me = client.get('/users/me')['data']
        if me.get('username', '').lower() != owner.lower():
            raise ValueError('Authenticated account does not match the X Scholar owner')
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
        metadata['status'] = 'authentication_failed'
        return [], metadata
    try:
        token = None
        seen = set()
        for _ in range(max_pages):
            query = {'max_results': 100, 'expansions': 'author_id',
                     'user.fields': 'username,name,profile_image_url,protected'}
            if token:
                query['pagination_token'] = token
            data = client.get(f'/users/{me["id"]}/liked_tweets', query)
            metadata['outgoing_available'] = True
            metadata['outgoing_pages_checked'] += 1
            users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
            for post in data.get('data', []):
                user = as_public_profile(users.get(post.get('author_id'), {}))
                events.append(interaction(user, owner, 'likes', 'outgoing', post.get('id'), post.get('id')))
            following = data.get('meta', {}).get('next_token')
            if not following or following in seen:
                break
            seen.add(following)
            token = following
            time.sleep(1)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
        metadata['outgoing_error'] = True
    # Bound authenticated requests; this is a recent sample, never an all-time claim.
    for post in sorted(posts, key=lambda p: int(p['id']), reverse=True)[:post_limit]:
        if not post.get('likes'):
            continue
        try:
            data = client.get(f'/tweets/{post["id"]}/liking_users', {
                'max_results': 100, 'user.fields': 'username,name,profile_image_url,protected'})
            metadata['incoming_available'] = True
            metadata['incoming_posts_checked'] += 1
            for user in data.get('data', []):
                events.append(interaction(as_public_profile(user), owner, 'likes', 'incoming', post['id'], post['id']))
            time.sleep(1)
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
            metadata['incoming_error'] = True
            break
    metadata['status'] = 'available' if metadata['incoming_available'] and metadata['outgoing_available'] else 'partial_or_unavailable'
    metadata['scope'] = f'Up to {post_limit} recent own posts (up to 100 likers each) and {max_pages} pages of own likes.'
    return [event for event in events if event], metadata
