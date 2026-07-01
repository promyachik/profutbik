(function () {
  'use strict';
  var PATH_RE = /ibrahima-konate-real-madrid/i;
  var VALUES = ['€300K', '€35 млн', '€60 млн', '€45 млн'];

  function isKonatePage() {
    return PATH_RE.test(window.location.pathname || '') || PATH_RE.test(document.body && document.body.innerHTML ? document.body.innerHTML.slice(0, 6000) : '');
  }

  function textOf(el) {
    return (el && (el.textContent || '') || '').replace(/\s+/g, ' ').trim();
  }

  function normalize(v) {
    return String(v || '').replace(/\s+/g, ' ').trim().toLowerCase();
  }

  function hideOnlyWhiteDuplicate(chart) {
    var wanted = normalize('€45 млн');
    var parent = chart.closest('.transfer-side-column, .player-brief, article, main, body') || document.body;
    Array.prototype.forEach.call(parent.querySelectorAll('h1,h2,h3,h4,p,div,span,strong'), function (el) {
      if (chart.contains(el)) return;
      if (el.closest('.promyachik-konate-price-layer-302')) return;
      if (normalize(el.textContent) !== wanted) return;
      var r = el.getBoundingClientRect();
      var cr = chart.getBoundingClientRect();
      if (r.top >= cr.bottom - 4 && r.top <= cr.bottom + 90) {
        el.setAttribute('data-promyachik-hidden-white-current-price-302', '1');
        el.style.setProperty('display', 'none', 'important');
      }
    });
  }

  function buildOverlay() {
    if (!isKonatePage()) return;
    var chart = document.querySelector('.player-market-chart');
    if (!chart) return;
    chart.setAttribute('data-promyachik-konate-302', '1');
    var canvas = chart.querySelector('.player-market-chart__canvas');
    if (!canvas) return;

    var dots = Array.prototype.slice.call(chart.querySelectorAll('.player-market-chart__dot'));
    var pointStrong = Array.prototype.slice.call(chart.querySelectorAll('.player-market-chart__point strong'));
    var values = pointStrong.map(textOf).filter(Boolean);
    if (values.length < 2) values = VALUES.slice();
    var count = Math.min(values.length, dots.length || values.length);
    if (!count) return;

    var layer = chart.querySelector('.promyachik-konate-price-layer-302');
    if (!layer) {
      layer = document.createElement('div');
      layer.className = 'promyachik-konate-price-layer-302';
      canvas.appendChild(layer);
    }
    layer.innerHTML = '';

    var canvasRect = canvas.getBoundingClientRect();
    for (var i = 0; i < count; i++) {
      var label = document.createElement('span');
      label.className = 'promyachik-konate-price-label-302';
      label.textContent = values[i] || VALUES[i] || '';
      var x, y;
      if (dots[i]) {
        var dotRect = dots[i].getBoundingClientRect();
        x = dotRect.left + dotRect.width / 2 - canvasRect.left;
        y = dotRect.top + dotRect.height / 2 - canvasRect.top;
      } else {
        x = ((i + 0.5) / count) * canvasRect.width;
        y = canvasRect.height * 0.7;
      }
      label.style.left = Math.round(x) + 'px';
      label.style.top = Math.round(y) + 'px';
      layer.appendChild(label);
    }
    hideOnlyWhiteDuplicate(chart);
  }

  function schedule() {
    buildOverlay();
    setTimeout(buildOverlay, 80);
    setTimeout(buildOverlay, 300);
    setTimeout(buildOverlay, 900);
    setTimeout(buildOverlay, 1600);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', schedule);
  } else {
    schedule();
  }
  window.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);
})();
