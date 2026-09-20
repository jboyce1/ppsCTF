const { test } = require('node:test');
const assert = require('node:assert/strict');
const { selectSession } = require('../assets/js/schedule.js');
const events = require('../_data/season.json');
const at = time => selectSession(events, Date.parse(time));
test('before kickoff, points to the first meeting', () => {
  assert.equal(at('2026-09-10T12:00:00Z').event.id, 'session-10-20');
  assert.equal(at('2026-09-10T12:00:00Z').status, 'Next meeting');
});
test('meeting is ongoing from its exact start until its end, then advances', () => {
  assert.equal(at('2026-10-22T17:44:59-04:00').status, 'Next meeting');
  assert.equal(at('2026-10-22T17:45:00-04:00').status, 'Ongoing now');
  assert.equal(at('2026-10-22T19:44:59-04:00').event.id, 'session-10-22');
  assert.equal(at('2026-10-22T19:45:00-04:00').event.id, 'session-10-27');
});
test('Eastern standard time is respected after the DST change', () => {
  assert.equal(at('2026-11-05T22:44:59Z').status, 'Next meeting');
  assert.equal(at('2026-11-05T22:45:00Z').status, 'Ongoing now');
  assert.equal(at('2026-11-06T00:45:00Z').event.id, 'session-11-10');
});
test('breaks are skipped and untimed events do not claim to be ongoing meetings', () => {
  assert.equal(at('2026-11-03T12:00:00-05:00').event.id, 'session-11-05');
  assert.equal(at('2026-11-25T12:00:00-05:00').event.id, 'session-12-01');
  assert.equal(at('2026-10-31T12:00:00-04:00').status, 'Today · Time to be announced');
  assert.equal(at('2026-11-01T00:00:00-04:00').event.id, 'session-11-05');
});
test('scheduled closeout takes precedence over the overlapping competition window', () => {
  assert.equal(at('2026-12-23T12:00:00-05:00').status, 'Competition window open');
  assert.equal(at('2026-12-23T17:45:00-05:00').event.id, 'session-12-23');
  assert.equal(at('2026-12-23T17:45:00-05:00').status, 'Ongoing now');
});
test('after the season, does not show stale meetings', () => {
  assert.equal(at('2026-12-24T00:00:00-05:00').event, null);
  assert.equal(at('2026-12-24T00:00:00-05:00').status, 'Season complete');
});
