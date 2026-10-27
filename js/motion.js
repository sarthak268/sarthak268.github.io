/* Dependency-free motion. Content remains visible if this script is unavailable. */
function initializeMotion() {
  'use strict';
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const normalize = path => path.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-bar a').forEach(link => {
    if (link.origin === location.origin && normalize(link.pathname) === normalize(location.pathname)) {
      link.setAttribute('aria-current', 'page');
    }
  });

  const homeParagraphs = document.querySelectorAll('.home-portrait + div > p');
  homeParagraphs.forEach(paragraph => paragraph.classList.add('home-copy-entry'));
  const textPage = ['/misc', '/activity'].includes(normalize(location.pathname));
  if (textPage) document.documentElement.classList.add('motion-text-page');

  if ('IntersectionObserver' in window && !preference.matches) {
    const items = [...document.querySelectorAll('.home-portrait, .home-copy-entry, .timeline-item, .entries > li, .publication-media-card')];
    if (textPage) items.push(...document.querySelectorAll('.talks-year, .list-item'));
    const groups = new Map();
    // Keep each paper's title and metadata together without changing the markup.
    document.querySelectorAll('.pubt').forEach(title => {
      if (title.closest('.publication-media-card')) return;
      const details = title.nextElementSibling;
      const group = details?.matches('.pubd') ? [title, details] : [title];
      groups.set(title, group);
      items.push(title);
    });
    const reveal = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        (groups.get(entry.target) || [entry.target]).forEach(element => {
          element.classList.replace('reveal-pending', 'reveal-visible');
        });
        reveal.unobserve(entry.target);
      });
    }, { threshold: 0.08 });
    document.documentElement.classList.add('motion-ready');
    items.forEach((item, index) => {
      (groups.get(item) || [item]).forEach(element => {
        element.style.setProperty('--reveal-delay', `${Math.min(index % 4, 3) * 85}ms`);
        element.classList.add('reveal-pending');
      });
      reveal.observe(item);
    });
  }

  const photo = document.querySelector('.portrait-photo');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  if (photo) {
    const reset = () => {
      photo.style.removeProperty('--tilt-x');
      photo.style.removeProperty('--tilt-y');
    };
    photo.addEventListener('pointermove', event => {
      if (preference.matches || !finePointer.matches) return;
      const bounds = photo.getBoundingClientRect();
      photo.style.setProperty('--tilt-x', `${(0.5 - (event.clientY - bounds.top) / bounds.height) * 5}deg`);
      photo.style.setProperty('--tilt-y', `${((event.clientX - bounds.left) / bounds.width - 0.5) * 5}deg`);
    });
    photo.addEventListener('pointerleave', reset);
    preference.addEventListener('change', reset);
  }
}

// Publications builds its existing media cards on DOMContentLoaded. Let that
// finish before choosing entrance targets, so no title is animated twice.
if (document.readyState === 'complete') initializeMotion();
else document.addEventListener('DOMContentLoaded', initializeMotion, { once: true });
