/* Explicit Eastern-time offsets in season.json keep selection independent of the viewer's timezone. */
function selectSession(events, now) {
  const sessions = events.filter(event => event.kind !== 'break');
  const active = sessions.filter(event => Date.parse(event.start) <= now && now < Date.parse(event.end));
  const current = active.find(event => event.kind === 'meeting') || active[0];
  if (current) return { event: current, status: current.kind === 'meeting' ? 'Ongoing now' : current.kind === 'window' ? 'Competition window open' : 'Today · Time to be announced' };
  const next = sessions.filter(event => Date.parse(event.start) > now).sort((a, b) => Date.parse(a.start) - Date.parse(b.start))[0];
  return next ? { event: next, status: next.kind === 'meeting' ? 'Next meeting' : 'Next event' } : { event: null, status: 'Season complete' };
}
if (typeof module !== 'undefined' && module.exports) module.exports = { selectSession };
if (typeof document !== 'undefined') {
  const rows = [...document.querySelectorAll('.season-row')];
  const events = rows.map(row => ({ ...row.dataset, row }));
  const status = document.getElementById('next-status');
  let lastSelection = '';
  function updateSchedule() {
    const selection = selectSession(events, Date.now());
    const event = selection.event;
    const key = selection.status + (event ? event.row.id : '');
    if (key === lastSelection) return;
    lastSelection = key;
    rows.forEach(row => {
      row.classList.remove('selected-session');
      row.removeAttribute('aria-current');
      row.querySelector('.session-marker').hidden = true;
    });
    status.textContent = selection.status;
    const links = document.getElementById('next-links');
    links.replaceChildren();
    if (!event) {
      document.getElementById('next-title').textContent = 'Thanks for a great season.';
      document.getElementById('next-time').textContent = 'Revisit the lessons below. The next season will appear here when its schedule is announced.';
      const link = document.createElement('a');
      link.href = '#classes'; link.textContent = 'Browse class resources →'; links.append(link);
      return;
    }
    const row = event.row;
    row.classList.add('selected-session');
    row.setAttribute('aria-current', 'true');
    const marker = row.querySelector('.session-marker');
    marker.hidden = false; marker.textContent = '→ ' + selection.status;
    document.getElementById('next-title').textContent = row.querySelector('.session-title').textContent;
    document.getElementById('next-time').textContent = [...row.querySelector('.session-date').children].slice(0, 2).map(el => el.textContent).join(' · ');
    row.querySelectorAll('.session-resources a').forEach(link => links.append(link.cloneNode(true)));
    const jump = document.createElement('a');
    jump.href = '#' + row.id; jump.textContent = 'View in schedule ↓'; links.append(jump);
  }
  if (status && rows.length) {
    updateSchedule();
    setInterval(updateSchedule, 15000);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) updateSchedule(); });
    window.addEventListener('focus', updateSchedule);
  }
}
