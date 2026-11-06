import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.parse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from refresh_x_scholar import refresh
from update_x_scholar import make_post
from update_x_scholar_people import collect_events
from x_scholar_interactions import aggregate, interaction, outgoing_from_status
from x_scholar_x_api import authorization, collect_likes

OWNER = 'owner'
ALICE = {'screen_name': 'Alice', 'name': 'Alice Example'}


class InteractionsTest(unittest.TestCase):
    def test_directions_deduplication_and_self_exclusion(self):
        outgoing = {'id': '200', 'author': {'screen_name': OWNER},
                    'quote': {'id': '100', 'author': ALICE}}
        events = outgoing_from_status(outgoing, OWNER)
        events.extend(events[:])
        events.append(interaction(ALICE, OWNER, 'likes', 'outgoing', '100', '100'))
        events.append(interaction(ALICE, OWNER, 'replies', 'incoming', '300', '400'))
        events.append(interaction({'screen_name': OWNER}, OWNER, 'likes', 'incoming', '300', '300'))
        events.append(interaction({**ALICE, 'protected': True}, OWNER, 'likes', 'incoming', '300', '300'))
        people = aggregate(events)
        self.assertEqual(len(people), 1)
        self.assertEqual((people[0]['incoming'], people[0]['outgoing'], people[0]['interaction_count']), (1, 2, 3))
        self.assertEqual(people[0]['post_count'], 2)

    def test_outgoing_reposts_need_owner_evidence(self):
        raw = {'id': '100', 'author': ALICE, 'reposted_by': {'screen_name': OWNER}}
        self.assertEqual(outgoing_from_status(raw, OWNER)[0]['evidence']['direction'], 'outgoing')
        raw['reposted_by']['screen_name'] = 'someone_else'
        self.assertEqual(outgoing_from_status(raw, OWNER), [])

    def test_direct_replies_only_and_owner_replies_are_outgoing(self):
        replies = [{'id': '200', 'author': ALICE, 'replying_to': {'screen_name': OWNER, 'status': '100'}},
                   {'id': '201', 'author': {'screen_name': OWNER}, 'replying_to': {'screen_name': 'Alice', 'status': '200'}},
                   {'id': '202', 'author': ALICE, 'replying_to': {'screen_name': 'other', 'status': '500'}}]
        events = collect_events([{'kind': 'replies', 'post_id': '100', 'entries': replies}], OWNER)
        person = aggregate(events)[0]
        self.assertEqual((person['incoming'], person['outgoing']), (1, 1))
        self.assertEqual(person['name'], 'Alice Example')

    def test_post_index_still_excludes_replies_and_reposts(self):
        self.assertIsNone(make_post({'author': ALICE}, OWNER))
        self.assertIsNone(make_post({'author': {'screen_name': OWNER}, 'replying_to': ALICE}, OWNER))

    def test_missing_parent_is_not_fabricated(self):
        self.assertEqual(outgoing_from_status({'id': '200', 'author': {'screen_name': OWNER},
                         'replying_to': {'screen_name': 'Alice'}}, OWNER), [])


class LikesTest(unittest.TestCase):
    def test_oauth_signature_matches_published_oauth_example(self):
        header = authorization('http://photos.example.net/photos?file=vacation.jpg&size=original',
                               ('dpf43f3p2l4k3l03', 'kd94hf93k423kf44', 'nnch734d00sl2jdk', 'pfkkdhi9sl3r4s00'),
                               nonce='kllo9940pd9333jh', timestamp=1191242096)
        self.assertIn('oauth_signature="' + urllib.parse.quote('tR3+Ty81lMeYAr/Fid0kMTYa/WM=', safe='') + '"', header)

    def test_no_credentials_never_fabricates_zero_likes(self):
        with patch.dict('os.environ', {}, clear=True):
            events, coverage = collect_likes(OWNER, [])
        self.assertEqual(events, [])
        self.assertEqual(coverage['status'], 'not_connected')
        self.assertFalse(coverage['incoming_available'])

    @patch('x_scholar_x_api.time.sleep')
    def test_authenticated_likes_in_both_directions(self, _sleep):
        class Client:
            def get(self, path, query=None):
                if path == '/users/me':
                    return {'data': {'id': '1', 'username': OWNER}}
                if path == '/users/1/liked_tweets':
                    return {'data': [{'id': '100', 'author_id': '2'}],
                            'includes': {'users': [{'id': '2', 'username': 'Alice', 'name': 'Alice Example'}]}}
                if path == '/tweets/300/liking_users':
                    return {'data': [{'id': '2', 'username': 'Alice', 'name': 'Alice Example'}]}
                raise AssertionError(path)
        events, coverage = collect_likes(OWNER, [{'id': '300', 'likes': 1}], client=Client())
        self.assertEqual(coverage['status'], 'available')
        person = aggregate(events)[0]
        self.assertEqual((person['incoming'], person['outgoing'], person['likes']), (1, 1, 2))

    def test_wrong_authenticated_account_is_rejected(self):
        class Client:
            def get(self, path, query=None):
                return {'data': {'id': '2', 'username': 'someone_else'}}
        events, coverage = collect_likes(OWNER, [], client=Client())
        self.assertFalse(events)
        self.assertEqual(coverage['status'], 'authentication_failed')


class RefreshTest(unittest.TestCase):
    def test_second_collector_failure_keeps_both_old_snapshots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_data').mkdir()
            for name in ['x_scholar.json', 'x_scholar_people.json']:
                (root / '_data' / name).write_text('previous snapshot')
            def run(command, check):
                if 'update_x_scholar_people.py' in command[1]:
                    raise subprocess.CalledProcessError(1, command)
                Path(command[-1]).write_text(json.dumps({'handle': OWNER, 'posts': [{'id': '1'}]}))
            with self.assertRaises(subprocess.CalledProcessError):
                refresh(root=root, run=run)
            for name in ['x_scholar.json', 'x_scholar_people.json']:
                self.assertEqual((root / '_data' / name).read_text(), 'previous snapshot')

    def test_success_promotes_both_snapshots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_data').mkdir()
            def run(command, check):
                key = 'people' if 'update_x_scholar_people.py' in command[1] else 'posts'
                Path(command[-1]).write_text(json.dumps({'handle': OWNER, key: [{'id': '1'}]}))
            refresh(root=root, run=run)
            self.assertEqual(json.loads((root / '_data/x_scholar_people.json').read_text())['handle'], OWNER)


if __name__ == '__main__':
    unittest.main()
