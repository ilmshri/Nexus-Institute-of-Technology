/* Nexus round-2 previews — shared motion layer.
   Scroll reveals, SVG draw-on, stat counters, scroll-spun gears, gentle
   hero parallax. Everything is additive (no-JS pages stay complete and
   readable) and everything is OFF under prefers-reduced-motion.
   The brightness value is design law: nothing here dims anything. */
(function () {
  'use strict';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  /* ---------- reveal-on-enter ---------- */
  var autoTargets = [
    ['[data-reveal]', null],                 // explicit, keeps its own class
    ['.statgrid .stat', 'reveal'],
    ['.cardgrid > *', 'reveal'],
    ['.twocol > *', 'reveal'],
    ['.notegrid > *', 'reveal'],
    ['.cta-band', 'reveal'],
    ['.hero-plate', 'reveal'],
    ['.semgroup', 'reveal']
  ];
  var els = [];
  autoTargets.forEach(function (t) {
    document.querySelectorAll(t[0]).forEach(function (el, i) {
      if (t[1] && !el.classList.contains('reveal') &&
          !el.classList.contains('reveal-left') && !el.classList.contains('reveal-right')) {
        el.classList.add(t[1]);
        el.style.transitionDelay = Math.min(i * 60, 240) + 'ms';
      }
      if (el.hasAttribute('data-reveal')) {
        el.classList.add(el.getAttribute('data-reveal') || 'reveal');
      }
      els.push(el);
    });
  });
  document.querySelectorAll('.draw-on').forEach(function (el) { els.push(el); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in-view'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in-view'); });
  }

  /* ---------- stat count-up ---------- */
  function countUp(el) {
    var raw = el.getAttribute('data-count');
    var target = parseInt(raw, 10);
    if (!isFinite(target)) return;
    var t0 = null, dur = 1100;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = raw;
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { countUp(en.target); cio.unobserve(en.target); }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  /* ---------- scroll-spun gears + parallax drift ---------- */
  var spinners = [].slice.call(document.querySelectorAll('.spin-scroll'));
  var drifters = [].slice.call(document.querySelectorAll('[data-drift]'));
  if (spinners.length || drifters.length) {
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        spinners.forEach(function (g) {
          var k = parseFloat(g.getAttribute('data-spin')) || 0.12;
          g.style.transform = 'rotate(' + (y * k).toFixed(2) + 'deg)';
        });
        drifters.forEach(function (d) {
          var k = parseFloat(d.getAttribute('data-drift')) || 0.06;
          var r = d.getBoundingClientRect();
          var mid = r.top + r.height / 2 - window.innerHeight / 2;
          d.style.transform = 'translateY(' + (-mid * k).toFixed(1) + 'px)';
        });
        ticking = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
