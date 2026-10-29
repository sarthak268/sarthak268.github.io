/* Shared navigation and theme behavior, with no framework dependency. */
(function () {
  'use strict';
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const menu = document.getElementById('menu-toggle');
  const nav = document.getElementById('site-nav');

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#121212' : '#faf9f6';
  }
  applyTheme(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
  toggle.addEventListener('click', () => {
    const theme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(theme);
    try { localStorage.setItem('theme', theme); } catch (error) {}
  });
  window.addEventListener('storage', event => {
    if (event.key === 'theme' && ['light', 'dark'].includes(event.newValue)) applyTheme(event.newValue);
  });

  function setMenu(open) {
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    menu.querySelector('span').textContent = open ? '−' : '+';
  }
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menu.focus();
    }
  });
  const desktop = window.matchMedia('(min-width: 761px)');
  desktop.addEventListener('change', () => setMenu(false));
  // Without JavaScript all navigation links remain visible.
  root.classList.add('site-ready');
})();
