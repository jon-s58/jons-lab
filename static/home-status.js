(function () {
  'use strict';

  // ---------- Local time ----------
  var timeEl = document.querySelector('[data-local-time]');
  function tickTime() {
    if (!timeEl) return;
    var d = new Date();
    var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
    var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
    timeEl.textContent =
      pad(d.getDate()) + ' ' + months[d.getMonth()] + ' · ' +
      pad(d.getHours()) + ':' + pad(d.getMinutes());
  }
  if (timeEl) { tickTime(); setInterval(tickTime, 30 * 1000); }

  // ---------- Uptime ----------
  var uptimeEl = document.querySelector('[data-uptime]');
  if (uptimeEl) {
    var START = new Date('2024-04-12T00:00:00Z');
    var days = Math.max(0, Math.floor((Date.now() - START.getTime()) / 86400000));
    uptimeEl.textContent = days + 'd';
  }
})();
