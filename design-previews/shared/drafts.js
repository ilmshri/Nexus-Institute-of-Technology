/* Nexus design-draft previews — shared behavior layer.
   Implements the same DOM contracts as the live site's nexus.js
   (tabs, quiz engine, semester chips) so real page content works
   unmodified inside every draft shell. Preview-only code. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  /* ---------- lesson tabs ---------- */
  var tabButtons = document.querySelectorAll('[data-tab]');
  tabButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-tab');
      document.querySelectorAll('[data-tab]').forEach(function (b) { b.classList.toggle('on', b === btn); });
      document.querySelectorAll('.tabpanel').forEach(function (p) { p.classList.toggle('on', p.id === id); });
      var bar = document.querySelector('.tabs');
      if (bar) {
        var y = bar.getBoundingClientRect().top + window.scrollY - (parseInt(document.body.dataset.tabOffset || '70', 10));
        if (window.scrollY > y) window.scrollTo({ top: y, behavior: 'auto' });
      }
    });
  });

  /* ---------- quiz: solve-item reveal ---------- */
  document.querySelectorAll('.quiz-reveal').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var sol = btn.parentElement.querySelector('.quiz-sol');
      if (!sol) return;
      var open = sol.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Hide the solution' : 'Show the full solution';
    });
  });

  /* ---------- quiz: MC select-then-submit ---------- */
  document.querySelectorAll('.quiz-item[data-kind="mc"]').forEach(function (item) {
    item.querySelectorAll('.quiz-choice').forEach(function (choice) {
      choice.addEventListener('click', function () {
        if (item.dataset.locked === '1') return;
        item.querySelectorAll('.quiz-choice').forEach(function (c) { c.classList.remove('sel'); });
        choice.classList.add('sel');
        item.classList.remove('unanswered');
      });
    });
  });
  document.querySelectorAll('.quiz-actions .quiz-submit').forEach(function (submit) {
    submit.addEventListener('click', function () {
      var scope = submit.closest('.quiz');
      if (!scope) return;
      var items = scope.querySelectorAll('.quiz-item[data-kind="mc"]');
      var unanswered = 0, right = 0;
      items.forEach(function (item) {
        if (!item.querySelector('.quiz-choice.sel')) { unanswered++; item.classList.add('unanswered'); }
      });
      var score = scope.querySelector('.quiz-score');
      if (unanswered) {
        if (score) { score.hidden = false; score.className = 'quiz-score mid'; score.textContent = unanswered + ' question' + (unanswered > 1 ? 's' : '') + ' still unanswered — select an answer for every problem, then submit.'; }
        return;
      }
      items.forEach(function (item) {
        item.dataset.locked = '1';
        var verdict = item.querySelector('.quiz-verdict');
        var ok = false;
        item.querySelectorAll('.quiz-choice').forEach(function (c) {
          c.disabled = true;
          var correct = c.hasAttribute('data-ok');
          if (c.classList.contains('sel')) {
            if (correct) { ok = true; c.classList.add('right'); }
            else c.classList.add('wrong');
          } else if (correct) { c.classList.add('right'); }
        });
        if (ok) right++;
        if (verdict) {
          verdict.hidden = false;
          verdict.className = 'quiz-verdict ' + (ok ? 'ok' : 'no');
          verdict.textContent = ok ? 'Correct.' : 'Not quite — the correct choice is highlighted.';
        }
        var sol = item.querySelector('.quiz-sol');
        if (sol) sol.classList.add('open');
      });
      if (score) {
        score.hidden = false;
        var frac = right / (items.length || 1);
        score.className = 'quiz-score ' + (frac >= 0.8 ? 'ok' : 'mid');
        score.textContent = 'Score: ' + right + ' / ' + items.length + ' multiple-choice.';
      }
      submit.disabled = true;
    });
  });

  /* ---------- curriculum: semester chips + search filter ---------- */
  var chips = document.querySelectorAll('.chip[data-sem]');
  function applyFilter() {
    var active = document.querySelector('.chip[data-sem].on');
    var sem = active ? active.dataset.sem : 'all';
    var q = (document.getElementById('lessonSearch') || {}).value || '';
    q = q.trim().toLowerCase();
    document.querySelectorAll('[data-course]').forEach(function (card) {
      var okSem = sem === 'all' || card.dataset.sem === sem;
      var okQ = !q || card.dataset.search.indexOf(q) !== -1;
      card.hidden = !(okSem && okQ);
    });
    document.querySelectorAll('[data-semgroup]').forEach(function (group) {
      var any = group.querySelector('[data-course]:not([hidden])');
      group.hidden = !any;
    });
  }
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.toggle('on', c === chip); });
      applyFilter();
    });
  });
  var search = document.getElementById('lessonSearch');
  if (search) search.addEventListener('input', applyFilter);

  /* ---------- ⌘K focuses search where present ---------- */
  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      var s = document.getElementById('lessonSearch');
      if (s) { e.preventDefault(); s.focus(); s.select(); }
    }
  });

  /* ---------- outline ticks: purely visual demo state ---------- */
  document.querySelectorAll('[data-demo-done]').forEach(function (el) { el.classList.add('done'); });
})();
