# Sarthak Bhagat — personal website

A static Jekyll website hosted on GitHub Pages.

## Run locally

Use the Ruby version in `.ruby-version`, then install Bundler and the dependencies:

```sh
gem install bundler
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Open <http://127.0.0.1:4000>. Jekyll rebuilds when content or styles change;
restart the server after changing `_config.yml`.

## Build

```sh
bundle exec jekyll build
```

Generated output lives in `_site/` and should not be committed. Edit `index.md`
for the homepage, `_pages/` for other pages, `_layouts/` for shared templates,
and `css/` or `js/` for styling and interactions.

Shared navigation lives in `_data/navigation.yml`; page introductions live in
`_data/page_intros.yml`. The shared layout is `_layouts/default.html` and the
current visual foundations are in `css/site.css`. The older stylesheets still
provide the specialized bookshelf, travel, and publication layouts.

The travel map uses `_data/travel_places.json`. Add confirmed park names to a
location's `national_parks` array to update the national-park count automatically.
The count uses unique park names, so multiple locations in one park count once.

## X Scholar

`/x-scholar/` presents a snapshot of X posts with likes-based metrics, search,
sorting, year filters, and CSV export. The `Refresh X Scholar` GitHub Actions
workflow refreshes it every six hours (00:23, 06:23, 12:23, and 18:23 UTC), or on
demand from the Actions tab. Scheduled runs can be delayed by GitHub. GitHub
also disables scheduled workflows in public repositories after 60 days without
repository activity; re-enable it from Actions if that happens.

Refresh both snapshots locally with:

```sh
python3 scripts/refresh_x_scholar.py
```

Both collectors must succeed before either published snapshot is replaced. The
workflow commits only the two data files, then explicitly requests a Pages build
(commits made with `GITHUB_TOKEN` do not trigger a Pages build on their own).
Failures leave the existing website data available and appear in Actions.

To refresh only the post index:

```sh
python3 scripts/update_x_scholar.py
```

The updater uses the public FxTwitter API and writes `_data/x_scholar.json`
atomically. Replies and reposts are excluded, and each post is checked against
the profile's handle. The page remains available if the API is unavailable;
statistics only change when the snapshot is refreshed and the site is rebuilt.
Pinned or otherwise omitted posts can be retained across refreshes by adding
their status IDs to `_data/x_scholar_includes.json`.

Refresh the people sidebar after refreshing posts:

```sh
python3 scripts/update_x_scholar_people.py
```

The sidebar collects replies, reposts, and quotes **in both directions**:
other people interacting with the indexed posts, and Sarthak interacting with
other people's posts. Outgoing reposts and quotes come from his timeline;
outgoing replies come from conversations and the replies timeline when that
endpoint is available. Plain mentions are not treated as interactions. The
sidebar ranks by deduplicated interactions, favoring mutual interactions on ties,
and shows eight people. The data retains evidence IDs, types, and directions.
Self-interactions and protected profiles are excluded. Counts describe the
available sample, not a complete history; unavailable endpoints are recorded
in the data rather than described as zero activity.

### Optional likes in the people sidebar

Public FxTwitter provides like **counts**, but does not expose the identities
of likers or the owner's liked-post history. To include authenticated likes,
create a read-capable X developer app and add its OAuth 1.0a user credentials
for **@sarthak__bhagat** under repository **Settings → Secrets and variables →
Actions → Repository secrets**:

- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

The collector checks that the authenticated account matches the site owner. It
only sends GET requests: `/2/users/me`, `/2/users/:id/liked_tweets`, and
`/2/tweets/:id/liking_users`. API access and any X charges depend on the app's
plan. The default bounds are three pages of outgoing likes and the 25 most
recent indexed own posts (up to 100 incoming likers per post). Change
`--likes-post-limit` when running the people collector to adjust the latter.

Secrets stay in the runner environment and are never written to the site or
data files. Without credentials, replies/reposts/quotes still refresh and the
sidebar explicitly says likes are unavailable. An authenticated endpoint failure
is recorded as unavailable/partial, not as proof of no likes. Trigger the workflow
manually after adding credentials to verify access; authenticated fetching cannot
be verified without working credentials.

Run collector tests with:

```sh
python3 -m unittest discover -s scripts/tests -v
```
