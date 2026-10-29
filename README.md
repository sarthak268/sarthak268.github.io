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
