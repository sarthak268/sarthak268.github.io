/* Progressive enhancement: a little personality without changing the content. */
(function () {
  'use strict';
  function initializePlayful() {
    const root = document.documentElement;
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    const running = new Set();
    root.classList.add('playful-enhanced');

    document.querySelectorAll('.goal-item').forEach(goal => {
      if (goal.querySelector('s')) goal.classList.add('is-complete');
    });

    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.setAttribute('aria-hidden', 'true');
    document.body.appendChild(progress);
    let progressFrame = 0;
    function updateProgress() {
      progressFrame = 0;
      const available = root.scrollHeight - window.innerHeight;
      const fraction = available > 0 ? Math.max(0, Math.min(1, window.scrollY / available)) : 0;
      progress.style.transform = `scaleX(${fraction})`;
    }
    function requestProgress() {
      if (!progressFrame) progressFrame = requestAnimationFrame(updateProgress);
    }
    window.addEventListener('scroll', requestProgress, { passive: true });
    window.addEventListener('resize', requestProgress, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(requestProgress).observe(document.body);
    requestProgress();

    const theme = document.getElementById('theme-toggle');
    theme?.addEventListener('click', () => {
      if (preference.matches || typeof theme.animate !== 'function') return;
      theme.getAnimations().forEach(animation => animation.cancel());
      const animation = theme.animate([
        { transform: 'rotate(0deg) scale(1)' },
        { transform: 'rotate(100deg) scale(.85)', offset: .45 },
        { transform: 'rotate(180deg) scale(1)' }
      ], { duration: 420, easing: 'cubic-bezier(.2,.8,.2,1)' });
      running.add(animation);
      animation.onfinish = animation.oncancel = () => running.delete(animation);
    });
    preference.addEventListener('change', () => {
      if (preference.matches) running.forEach(animation => animation.cancel());
    });

    if (!('IntersectionObserver' in window)) return;
    const chart = document.querySelector('.yearly-chart');
    if (chart) {
      chart.querySelectorAll('.chart-bar').forEach((bar, index) => bar.style.setProperty('--bar-index', index));
      const chartObserver = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          chart.classList.add('is-playful-visible');
          chartObserver.disconnect();
        }
      }, { threshold: .2 });
      chartObserver.observe(chart);
    }

    // Keep the final value available to assistive technology throughout the count-up.
    const targets = document.querySelectorAll('.travel-stat-number, .things-progress-number, .metrics-table tbody td, .person-count');
    if (preference.matches || !targets.length) return;
    const counterObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const element = entry.target;
        counterObserver.unobserve(element);
        if (preference.matches) return;
        const text = Array.from(element.childNodes).find(node => node.nodeType === Node.TEXT_NODE && /^\s*\d+\s*$/.test(node.textContent));
        if (!text) return;
        const original = text.textContent;
        const digits = original.trim();
        const target = Number(digits);
        const visual = document.createElement('span');
        visual.className = 'playful-counter';
        visual.setAttribute('aria-hidden', 'true');
        visual.style.minWidth = `${digits.length}ch`;
        visual.textContent = digits;
        const accessible = document.createElement('span');
        accessible.className = 'playful-sr-only';
        accessible.textContent = digits;
        const fragment = document.createDocumentFragment();
        if (/^\s/.test(original)) fragment.append(document.createTextNode(' '));
        fragment.append(visual, accessible);
        if (/\s$/.test(original)) fragment.append(document.createTextNode(' '));
        text.replaceWith(fragment);
        let start;
        function count(now) {
          if (start === undefined) start = now;
          const fraction = preference.matches ? 1 : Math.min(1, (now - start) / 800);
          const eased = 1 - Math.pow(1 - fraction, 3);
          visual.textContent = String(Math.round(target * eased));
          if (fraction < 1) requestAnimationFrame(count);
        }
        requestAnimationFrame(count);
      });
    }, { threshold: .5 });
    targets.forEach(target => counterObserver.observe(target));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializePlayful, { once: true });
  else initializePlayful();
})();
