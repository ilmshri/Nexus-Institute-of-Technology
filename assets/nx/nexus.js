/* NEXUS INSTITUTE OF TECHNOLOGY — platform behavior. Zero dependencies. */
(function () {
  document.documentElement.classList.add('js');

  /* ---------- language toggle (EN <-> AR, with RTL) ---------- */
  var LANG_KEY = 'nx-lang';
  var btn = document.getElementById('langBtn');
  function applyLang(lang) {
    var ar = lang === 'ar';
    document.documentElement.lang = ar ? 'ar' : 'en';
    document.documentElement.dir = ar ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-ar]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.textContent);
      el.textContent = ar ? el.getAttribute('data-ar') : el.getAttribute('data-en');
    });
    document.querySelectorAll('[data-ar-placeholder]').forEach(function (el) {
      if (!el.hasAttribute('data-en-placeholder'))
        el.setAttribute('data-en-placeholder', el.getAttribute('placeholder') || '');
      el.setAttribute('placeholder', ar ? el.getAttribute('data-ar-placeholder')
                                        : el.getAttribute('data-en-placeholder'));
    });
    if (btn) btn.textContent = ar ? 'English' : 'العربية';
    if (typeof renderProgress === 'function') renderProgress();
  }
  var saved = null;
  try { saved = localStorage.getItem(LANG_KEY); } catch (e) {}
  if (btn && saved === 'ar') applyLang('ar');  /* Arabic on hold: never auto-apply without the toggle */
  if (btn) btn.addEventListener('click', function () {
    var next = document.documentElement.lang === 'ar' ? 'en' : 'ar';
    applyLang(next);
    try { localStorage.setItem(LANG_KEY, next); } catch (e) {}
  });

  /* ---------- completion store (localStorage) ---------- */
  var DONE_KEY = 'nx-done';
  function getDone() {
    try { return JSON.parse(localStorage.getItem(DONE_KEY)) || {}; } catch (e) { return {}; }
  }
  function setDone(d) {
    try { localStorage.setItem(DONE_KEY, JSON.stringify(d)); } catch (e) {}
  }
  function isAr() { return document.documentElement.lang === 'ar'; }

  function renderProgress() {
    var done = getDone();

    // lesson player: outline ticks + progress + complete button
    var outline = document.getElementById('outline');
    if (outline) {
      var links = outline.querySelectorAll('a[data-key]');
      var n = 0;
      links.forEach(function (a) {
        var d = !!done[a.getAttribute('data-key')];
        a.classList.toggle('done', d);
        if (d) n++;
      });
      var bar = outline.querySelector('.oh .bar i');
      var ptext = outline.querySelector('.oh .ptext');
      if (bar) bar.style.width = links.length ? Math.round(100 * n / links.length) + '%' : '0%';
      if (ptext) ptext.textContent = isAr()
        ? n + ' من ' + links.length + ' مكتمل'
        : n + ' of ' + links.length + ' complete';
    }
    var btn = document.getElementById('completeBtn');
    if (btn) {
      var d = !!done[btn.getAttribute('data-key')];
      btn.classList.toggle('done', d);
      btn.textContent = d ? (isAr() ? '✓ مكتمل — إلغاء العلامة' : '✓ Completed — click to undo')
                          : (isAr() ? 'وضع علامة مكتمل' : 'Mark as complete');
    }

    // course syllabus ticks + resume button
    var rows = document.querySelectorAll('.syl[data-key]');
    if (rows.length) {
      var firstOpen = null, doneCount = 0;
      rows.forEach(function (r) {
        var d = !!done[r.getAttribute('data-key')];
        r.classList.toggle('done', d);
        if (d) doneCount++;
        else if (!firstOpen) firstOpen = r;
      });
      var resume = document.getElementById('resumeBtn');
      if (resume) {
        var target = firstOpen || rows[0];
        resume.setAttribute('href', target.getAttribute('data-href'));
        var no = target.querySelector('.no') ? target.querySelector('.no').textContent : '01';
        resume.textContent = doneCount === 0
          ? (isAr() ? 'ابدأ الدرس ' + no : 'Start lesson ' + no)
          : doneCount === rows.length
            ? (isAr() ? 'راجع الدرس 01' : 'Review lesson 01')
            : (isAr() ? 'تابع — الدرس ' + no : 'Resume — lesson ' + no);
      }
    }

    // catalog: per-course progress bars
    document.querySelectorAll('.course-card[data-key]').forEach(function (card) {
      var key = card.getAttribute('data-key') + '/';
      var total = parseInt(card.getAttribute('data-n') || '0', 10);
      var n2 = 0;
      for (var k in done) if (done[k] && k.indexOf(key) === 0) n2++;
      var bar2 = card.querySelector('.pbar i');
      var note = card.querySelector('.pnote');
      if (bar2) bar2.style.width = total ? Math.round(100 * Math.min(n2, total) / total) + '%' : '0%';
      if (note) note.textContent = n2
        ? (isAr() ? n2 + '/' + total + ' مكتمل' : n2 + '/' + total + ' complete')
        : (isAr() ? 'لم يبدأ بعد' : 'not started');
    });
  }

  var cbtn = document.getElementById('completeBtn');
  if (cbtn) cbtn.addEventListener('click', function () {
    var d = getDone();
    var k = cbtn.getAttribute('data-key');
    if (d[k]) delete d[k]; else d[k] = true;
    setDone(d);
    renderProgress();
  });

  renderProgress();

  /* ---------- catalog semester filter chips ---------- */
  var chipRow = document.getElementById('semChips');
  if (chipRow) {
    chipRow.addEventListener('click', function (e) {
      var c = e.target.closest('.chip');
      if (!c) return;
      chipRow.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on');
      var sem = c.getAttribute('data-sem');
      document.querySelectorAll('.course-card[data-sem]').forEach(function (card) {
        card.hidden = (sem !== 'all' && card.getAttribute('data-sem') !== sem);
      });
    });
  }

  /* ---------- side drop-down section menu ---------- */
  var sm = document.getElementById('sideMenu');
  if (sm) {
    sm.querySelector('button').addEventListener('click', function () {
      sm.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!sm.contains(e.target)) sm.classList.remove('open');
    });
    sm.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        sm.classList.remove('open');
        var tab = a.getAttribute('data-tab');
        if (tab) {
          e.preventDefault();
          var b = document.querySelector('.tabs button[data-tab="' + tab + '"]');
          if (b) { b.click(); b.scrollIntoView({ block: 'center' }); }
        }
      });
    });
  }

  /* ---------- lesson tabs (no JS: all panels stacked) ---------- */
  var bar = document.querySelector('.tabs');
  if (bar) {
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-tab]');
      if (!b) return;
      bar.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); });
      document.querySelectorAll('.tabpanel').forEach(function (p) { p.classList.remove('on'); });
      b.classList.add('on');
      var panel = document.getElementById(b.getAttribute('data-tab'));
      if (panel) panel.classList.add('on');
    });
  }

  /* ---------- hidden-answer reveals (tier-1 lecture checks) ---------- */
  document.querySelectorAll('.check').forEach(function (box) {
    var b = box.querySelector('button');
    var panel = box.querySelector('.a');
    if (!b || !panel) return;
    b.addEventListener('click', function () {
      var open = panel.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.textContent = open ? 'Hide worked answer' : 'Reveal worked answer';
    });
  });

  /* ---------- quiz engine (dynamic swap on wrong answer, owner #4) ----------
     On a wrong MC answer the engine does NOT immediately reveal: it swaps the
     question for a same-concept variant and grants a retry. An authored variant
     (data-variants) is used first; otherwise the same question is re-posed with
     its options reshuffled — a genuine re-pose that invents no new physics.
     After the retry (or Reveal answer) the correct choice + solution show. */
  function qtxt(ar, en) { return document.documentElement.lang === 'ar' ? ar : en; }

  function reletter(item) {
    var keys = item.querySelectorAll('.choices .quiz-choice .key');
    keys.forEach(function (k, i) { k.textContent = String.fromCharCode(65 + i); });
  }
  function shuffleChoices(item) {
    var box = item.querySelector('.choices');
    var arr = Array.prototype.slice.call(box.children);
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    arr.forEach(function (node) { box.appendChild(node); });
    reletter(item);
  }
  function wireChoices(item) {
    item.querySelectorAll('.quiz-choice').forEach(function (c) {
      c.disabled = false;
      c.classList.remove('sel', 'right', 'wrong');
      c.addEventListener('click', function () {
        if (item.dataset.locked === '1') return;
        item.querySelectorAll('.quiz-choice').forEach(function (k) { k.classList.remove('sel'); });
        c.classList.add('sel');
      });
    });
  }
  function loadVariant(item, v) {
    var q = item.querySelector('.q');
    var tag = q.querySelector('.tag');
    q.innerHTML = (tag ? tag.outerHTML : '') + v.q;
    var box = item.querySelector('.choices');
    box.innerHTML = '';
    v.choices.forEach(function (ch, j) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'quiz-choice';
      if (j === v.answer) b.setAttribute('data-ok', '1');
      b.innerHTML = '<span class="key">' + String.fromCharCode(65 + j) + '</span><span>' + ch + '</span>';
      box.appendChild(b);
    });
    if (v.solution) item.querySelector('.quiz-sol').innerHTML = v.solution;
    wireChoices(item);
    if (window.MathJax && MathJax.typesetPromise) { MathJax.typesetPromise([item]); }
  }
  function gradeSel(item) {
    var sel = item.querySelector('.quiz-choice.sel');
    return { sel: sel, ok: !!(sel && sel.getAttribute('data-ok') === '1') };
  }
  function settleCorrect(item) {
    var sel = item.querySelector('.quiz-choice.sel');
    if (sel) sel.classList.add('right');
    var verdict = item.querySelector('.quiz-verdict');
    if (verdict) {
      verdict.textContent = qtxt('✓ إجابة صحيحة. الشرح الكامل أدناه.',
                                 '✓ Correct. The full explanation is below.');
      verdict.className = 'quiz-verdict ok'; verdict.hidden = false;
    }
    item.querySelector('.quiz-sol').classList.add('open');
    item.querySelectorAll('.quiz-choice').forEach(function (k) { k.disabled = true; });
    item.dataset.locked = '1';
    var actions = item.querySelector('.quiz-item-actions');
    if (actions) actions.hidden = true;
  }
  function revealItem(item, msg) {
    item.querySelectorAll('.quiz-choice[data-ok="1"]').forEach(function (k) { k.classList.add('right'); });
    var sel = item.querySelector('.quiz-choice.sel');
    if (sel && sel.getAttribute('data-ok') !== '1') sel.classList.add('wrong');
    var verdict = item.querySelector('.quiz-verdict');
    if (verdict) { verdict.textContent = msg; verdict.className = 'quiz-verdict no'; verdict.hidden = false; }
    item.querySelector('.quiz-sol').classList.add('open');
    item.querySelectorAll('.quiz-choice').forEach(function (k) { k.disabled = true; });
    item.dataset.locked = '1';
    var actions = item.querySelector('.quiz-item-actions');
    if (actions) actions.hidden = true;
  }
  function enterRetry(item) {
    var verdict = item.querySelector('.quiz-verdict');
    var used = parseInt(item.dataset.vused || '0', 10);
    var variants = [];
    try { variants = JSON.parse(item.getAttribute('data-variants') || '[]'); } catch (e) {}
    if (variants.length > used) {
      loadVariant(item, variants[used]);
      item.dataset.vused = (used + 1);
      verdict.textContent = qtxt('✗ ليس بعد — إليك صيغة أخرى للمفهوم نفسه. حاول مرة أخرى.',
                                 '✗ Not quite — here is another version of the same idea. Try it, then Check again.');
    } else {
      item.querySelectorAll('.quiz-choice').forEach(function (k) {
        k.disabled = false; k.classList.remove('sel', 'right', 'wrong');
      });
      shuffleChoices(item);
      verdict.textContent = qtxt('✗ ليس بعد — نفس السؤال بترتيب جديد. اختر وتحقّق مرة أخرى.',
                                 '✗ Not quite — same question, options reordered. Pick again, then Check again.');
    }
    verdict.className = 'quiz-verdict retry'; verdict.hidden = false;
    var actions = item.querySelector('.quiz-item-actions');
    if (actions) actions.hidden = false;
  }

  document.querySelectorAll('.quiz-item').forEach(function (item) {
    var sol = item.querySelector('.quiz-sol');
    var rbtn = item.querySelector('.quiz-reveal');
    if (rbtn && sol) {
      rbtn.addEventListener('click', function () {
        var open = sol.classList.toggle('open');
        rbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        rbtn.textContent = open ? qtxt('إخفاء الحل الكامل', 'Hide the full solution')
                                : qtxt('إظهار الحل الكامل', 'Show the full solution');
      });
    }
    if (item.querySelector('.quiz-choice')) {
      wireChoices(item);
      var recheck = item.querySelector('.quiz-recheck');
      if (recheck) recheck.addEventListener('click', function () {
        var g = gradeSel(item);
        if (!g.sel) return;
        if (g.ok) settleCorrect(item);
        else revealItem(item, qtxt('✗ لا يزال غير صحيح — الحل الكامل أدناه.',
                                   '✗ Still not right — here is the full worked solution below.'));
      });
      var give = item.querySelector('.quiz-reveal-ans');
      if (give) give.addEventListener('click', function () {
        revealItem(item, qtxt('الإجابة الصحيحة مظلَّلة، والحل الكامل أدناه.',
                              'The correct answer is highlighted; the full solution is below.'));
      });
    }
  });

  /* ---------- quiz submit: grade all; wrong items swap + offer a retry ---------- */
  document.querySelectorAll('.quiz-submit').forEach(function (sbtn) {
    sbtn.addEventListener('click', function () {
      var quiz = sbtn.closest('.quiz');
      var items = quiz.querySelectorAll('.quiz-item[data-kind="mc"]');
      var right = 0;
      items.forEach(function (item) {
        if (item.dataset.locked === '1') return;
        var g = gradeSel(item);
        if (g.ok) { right++; settleCorrect(item); }
        else { enterRetry(item); }
      });
      var score = quiz.querySelector('.quiz-score');
      if (score) {
        score.textContent = qtxt('نتيجة المحاولة الأولى: ' + right + ' من ' + items.length,
                                 'First-attempt score: ' + right + ' of ' + items.length);
        score.className = 'quiz-score ' + (right === items.length ? 'ok' : 'mid');
        score.hidden = false;
      }
      sbtn.disabled = true;
      sbtn.textContent = right === items.length
        ? qtxt('✓ تم الإرسال', '✓ All correct — submitted')
        : qtxt('✓ تم الإرسال', '✓ Submitted — retry each missed question above');
    });
  });

  /* ---------- client-side lesson search ---------- */
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

  /* ---------- PWA service worker ---------- */
  if ('serviceWorker' in navigator) {
    var root = document.documentElement.getAttribute('data-root') || './';
    navigator.serviceWorker.register(root + 'sw.js').catch(function () {});
  }
})();

/* ---------- interactive workshop (homepage): pointer parallax + gear train.
   Hand-coded, zero dependencies; disabled under prefers-reduced-motion. ---------- */
(function () {
  var scene = document.getElementById('nxScene');
  if (!scene) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var layers = [].slice.call(scene.querySelectorAll('[data-depth]'));
  var gears = [].slice.call(document.querySelectorAll('.gear-spin'));
  var tx = 0, ty = 0, cx = 0, cy = 0, spin = 0, vel = 0, lastX = null;
  window.addEventListener('pointermove', function (e) {
    var r = scene.getBoundingClientRect();
    tx = (e.clientX - r.left) / Math.max(r.width, 1) - 0.5;
    ty = (e.clientY - r.top) / Math.max(r.height, 1) - 0.5;
    if (lastX !== null) vel += (e.clientX - lastX) * 0.12;
    lastX = e.clientX;
  }, { passive: true });
  (function tick() {
    cx += (tx - cx) * 0.08; cy += (ty - cy) * 0.08;
    vel *= 0.93; spin += 0.12 + vel * 0.02;
    for (var i = 0; i < layers.length; i++) {
      var d = parseFloat(layers[i].getAttribute('data-depth')) || 0;
      layers[i].style.transform =
        'translate(' + (cx * d * 20).toFixed(1) + 'px,' + (cy * d * 14).toFixed(1) + 'px)';
    }
    for (var g = 0; g < gears.length; g++) {
      var ratio = parseFloat(gears[g].getAttribute('data-ratio')) || 1;
      gears[g].style.transform = 'rotate(' + (spin / ratio).toFixed(2) + 'deg)';
    }
    requestAnimationFrame(tick);
  })();
})();
