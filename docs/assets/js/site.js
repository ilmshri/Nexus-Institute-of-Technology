(function () {
  // Answer reveal panels
  document.querySelectorAll('.check').forEach(function (box) {
    var btn = box.querySelector('button');
    var panel = box.querySelector('.a');
    if (!btn || !panel) return;
    btn.addEventListener('click', function () {
      var open = panel.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Hide worked answer' : 'Reveal worked answer';
    });
  });

  // Scroll reveals — progressive enhancement: content is visible without JS
  var els = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }
  document.documentElement.classList.add('js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
  els.forEach(function (e) { io.observe(e); });
})();

(function () {
  // Worked-example quizzes: solve-then-reveal and multiple choice
  document.querySelectorAll('.quiz-item').forEach(function (item) {
    var sol = item.querySelector('.quiz-sol');
    var verdict = item.querySelector('.quiz-verdict');

    var rbtn = item.querySelector('.quiz-reveal');
    if (rbtn && sol) {
      rbtn.addEventListener('click', function () {
        var open = sol.classList.toggle('open');
        rbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        rbtn.textContent = open ? 'Hide the full solution' : 'Show the full solution';
      });
    }

    var choices = item.querySelectorAll('.quiz-choice');
    if (choices.length) {
      choices.forEach(function (c) {
        c.addEventListener('click', function () {
          if (item.classList.contains('answered')) return;
          item.classList.add('answered');
          var right = c.getAttribute('data-ok') === '1';
          c.classList.add(right ? 'right' : 'wrong');
          if (!right) {
            item.querySelectorAll('.quiz-choice[data-ok="1"]').forEach(function (k) {
              k.classList.add('right');
            });
          }
          if (verdict) {
            verdict.textContent = right
              ? '✓ Correct. The full explanation is below.'
              : '✗ Not quite — the correct answer is highlighted. Read why below.';
            verdict.className = 'quiz-verdict ' + (right ? 'ok' : 'no');
            verdict.hidden = false;
          }
          if (sol) sol.classList.add('open');
          choices.forEach(function (k) { k.disabled = true; });
        });
      });
    }
  });
})();

(function () {
  // Lesson-page tabs — progressive enhancement (no JS: all panels stacked)
  var bar = document.querySelector('.tabs');
  if (bar) {
    document.documentElement.classList.add('js');
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-tab]');
      if (!btn) return;
      bar.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); });
      document.querySelectorAll('.tabpanel').forEach(function (p) { p.classList.remove('on'); });
      btn.classList.add('on');
      var panel = document.getElementById(btn.getAttribute('data-tab'));
      if (panel) panel.classList.add('on');
    });
  }

  // Client-side lesson search (curriculum index)
  var input = document.getElementById('lessonSearch');
  var out = document.getElementById('searchResults');
  if (input && out) {
    var idx = null;
    function load(cb) {
      if (idx) return cb();
      fetch(input.getAttribute('data-index')).then(function (r) { return r.json(); })
        .then(function (d) { idx = d; cb(); }).catch(function () {});
    }
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) { out.hidden = true; out.innerHTML = ''; return; }
      load(function () {
        var hits = [];
        for (var i = 0; i < idx.length && hits.length < 12; i++) {
          var e = idx[i];
          if ((e.t + ' ' + e.c + ' ' + e.k).toLowerCase().indexOf(q) !== -1) hits.push(e);
        }
        out.innerHTML = hits.length
          ? hits.map(function (e) {
              return '<a href="' + e.u + '"><b>' + e.t + '</b><span>' + e.c + '</span></a>';
            }).join('')
          : '<div class="none">No lessons match "' + q.replace(/[<>&"]/g, '') + '"</div>';
        out.hidden = false;
      });
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.searchbox')) { out.hidden = true; }
    });
  }
})();
