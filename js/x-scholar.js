/* Local search, sorting, filtering, pagination, and CSV export for a static snapshot. */
(function () {
  'use strict';
  const body = document.getElementById('post-rows');
  if (!body) return;
  const rows = Array.from(body.rows);
  const search = document.getElementById('post-search');
  const year = document.getElementById('post-year');
  const more = document.getElementById('show-more-posts');
  const count = document.getElementById('post-result-count');
  const range = document.getElementById('posts-range');
  const empty = document.getElementById('empty-results');
  const clear = document.getElementById('clear-filters');
  const sorts = Array.from(document.querySelectorAll('th[data-sort]'));
  const charts = Array.from(document.querySelectorAll('.chart-year'));
  const pageSize = 20;
  let limit = pageSize;
  let sortKey = 'likes';
  let descending = true;
  let filtered = [];

  function compare(a, b) {
    let result;
    if (sortKey === 'title') {
      result = a.dataset.title.localeCompare(b.dataset.title, undefined, { sensitivity: 'base' });
    } else if (sortKey === 'year') {
      result = a.dataset.date.localeCompare(b.dataset.date);
    } else {
      const aLikes = a.dataset.likes === '' ? -1 : Number(a.dataset.likes);
      const bLikes = b.dataset.likes === '' ? -1 : Number(b.dataset.likes);
      result = aLikes - bLikes;
    }
    return (descending ? -result : result) || b.dataset.date.localeCompare(a.dataset.date) || b.dataset.id.localeCompare(a.dataset.id);
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    filtered = rows.filter(row => (!year.value || row.dataset.year === year.value) &&
      (!query || row.dataset.text.toLocaleLowerCase().includes(query))).sort(compare);
    rows.forEach(row => { row.hidden = true; });
    // Moving existing nodes preserves the real links and keeps all text in the HTML.
    filtered.forEach((row, index) => {
      row.hidden = index >= limit;
      body.appendChild(row);
    });
    const visible = Math.min(limit, filtered.length);
    count.textContent = `${filtered.length} ${filtered.length === 1 ? 'post' : 'posts'}${year.value ? ' from ' + year.value : ''}`;
    range.textContent = filtered.length ? `Showing ${visible} of ${filtered.length}` : '';
    more.hidden = visible >= filtered.length;
    empty.hidden = filtered.length !== 0;
    clear.hidden = !query && !year.value;
    sorts.forEach(header => {
      const active = header.dataset.sort === sortKey;
      header.setAttribute('aria-sort', active ? (descending ? 'descending' : 'ascending') : 'none');
      header.querySelector('.sort-arrow').textContent = active ? (descending ? '↓' : '↑') : '';
    });
    charts.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.year === year.value)));
  }

  function filterChanged() { limit = pageSize; render(); }
  search.addEventListener('input', filterChanged);
  year.addEventListener('change', filterChanged);
  more.addEventListener('click', () => {
    const next = filtered[limit];
    limit += pageSize;
    render();
    next?.querySelector('a')?.focus({ preventScroll: true });
  });
  clear.addEventListener('click', () => {
    search.value = '';
    year.value = '';
    filterChanged();
    search.focus();
  });
  document.getElementById('post-tools').addEventListener('submit', event => event.preventDefault());
  sorts.forEach(header => header.querySelector('button').addEventListener('click', () => {
    if (sortKey === header.dataset.sort) descending = !descending;
    else { sortKey = header.dataset.sort; descending = sortKey !== 'title'; }
    limit = pageSize;
    render();
  }));
  charts.forEach(button => button.addEventListener('click', () => {
    year.value = year.value === button.dataset.year ? '' : button.dataset.year;
    filterChanged();
  }));

  function csvCell(value) {
    let text = String(value ?? '');
    // Prevent spreadsheet software from interpreting post text as formulas.
    if (/^[=+@-]/.test(text)) text = "'" + text;
    return '"' + text.replaceAll('"', '""') + '"';
  }
  document.getElementById('post-export').addEventListener('click', () => {
    const data = [['Text', 'Author', 'Date', 'Likes', 'URL'], ...filtered.map(row =>
      [row.dataset.text, 'Sarthak Bhagat', row.dataset.date, row.dataset.likes, row.dataset.url])];
    const csv = '\ufeff' + data.map(row => row.map(csvCell).join(',')).join('\r\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const download = document.createElement('a');
    download.href = url;
    download.download = 'sarthak-x-scholar.csv';
    document.body.appendChild(download);
    download.click();
    download.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  document.getElementById('post-tools').hidden = false;
  [...charts, ...sorts.map(header => header.querySelector('button'))].forEach(button => { button.disabled = false; });
  render();
})();
