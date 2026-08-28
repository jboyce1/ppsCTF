---
layout: default
title: 2026–27 Tentative Season
---

<style>
.season-page { --ctf:#ffb347; --tactics:#75cfff; --partner:#c8a2ff; --pause:#b8bec7; }
.season-page h1 { margin-top:2.75rem; padding-top:.5rem; border-top:3px solid #555; }
.season-page > h1:first-of-type { margin-top:0; border-top:0; }
.season-hero { padding:1.5rem; border:1px solid #555; border-left:6px solid #9bf; background:#191919; }
.season-hero h2 { margin-top:0; font-size:clamp(1.4rem,4vw,2.2rem); }
.tentative-notice { padding:.8rem 1rem; border:1px solid #826f39; background:#302915; }
.card-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1rem 0 2rem; }
.season-card { padding:1rem; border:1px solid #555; border-radius:6px; background:#292929; }
.season-card h2,.season-card h3 { margin-top:0; }
.season-button,.season-button:visited { display:inline-block; margin:.3rem .25rem .3rem 0; padding:.55rem .75rem; border:1px solid #9bf; border-radius:4px; color:#9bf; font-weight:bold; }
.season-button:hover,.season-button:focus { color:#111; background:#9bf; }
.season-button.disabled { color:#ccc; border-color:#777; cursor:not-allowed; }
.track-techniques { border-top:5px solid var(--ctf); }
.track-operations { border-top:5px solid var(--tactics); }
.crossover { padding:1rem; border-left:5px solid #9bf; background:#292929; }
.schedule-key { display:flex; flex-wrap:wrap; gap:.5rem; margin:1rem 0; }
.schedule-label { display:inline-block; padding:.16rem .45rem; border-radius:3px; color:#111; font-size:.8rem; font-weight:bold; }
.label-ctf { background:var(--ctf); }.label-tactics { background:var(--tactics); }.label-partner { background:var(--partner); }.label-pause { background:var(--pause); }
.schedule-month { margin:2rem 0; }.schedule-month > h2 { padding-bottom:.4rem; border-bottom:2px solid #555; }
.schedule-event { margin:.7rem 0; padding:.8rem 1rem; border-left:5px solid var(--ctf); background:#292929; }
.schedule-event.partner { border-left-color:var(--partner); }.schedule-event.tactics { border-left-color:var(--tactics); }.schedule-event.pause { border-left-color:var(--pause); background:#252525; }
.schedule-event p { margin:.25rem 0 0; }.spring-callout { padding:1rem; border:2px solid var(--partner); background:#292929; }
@media screen and (max-width:768px) { .card-grid { grid-template-columns:1fr; } .season-page h1 { overflow-wrap:anywhere; } }
</style>

<div class="season-page" markdown="1">

# 2026–27 Tentative Competition Season

<div class="season-hero" markdown="1">

## Two tracks. Multiple entry points. One regional cybersecurity community.

CyberTacticsForge is supporting a **CTF / techniques track** and an **operational / force-on-force track**. Students may move between them as their skills and interests develop.

<p class="tentative-notice"><strong>Tentative Schedule —</strong> Dates may change based on school calendars, partner competitions, and team availability.</p>
</div>

<div class="card-grid">
<article class="season-card" markdown="1">

## CyberPatriot 19 — Team Interest

CyberTacticsForge will sponsor and coordinate interested teams for the 2026–27 season. Returning and advanced students are especially encouraged to participate. Robert Morris University student mentors will provide team coaching and technical support.

<!-- TODO: Replace with CYBERPATRIOT_INTEREST_FORM_URL when available. -->
<span class="season-button disabled" aria-disabled="true">Express Interest in CyberPatriot — Coming Soon</span>

<a class="season-button" href="https://www.uscyberpatriot.org/competition/current-competition/competition-schedule" target="_blank" rel="noopener noreferrer">View Official CyberPatriot Schedule ↗</a>
</article>
<article class="season-card" markdown="1">

## CyLab Security Academy — CTF Interest

Students interested in additional CTF opportunities can express interest now. CyberTacticsForge plans to connect students with Carnegie Mellon University student mentors and local support as Academy competitions are announced.

<!-- TODO: Replace with CYLAB_INTEREST_FORM_URL when available. -->
<span class="season-button disabled" aria-disabled="true">Express Interest in CyLab Security Academy — Coming Soon</span>

<a class="season-button" href="https://www.cylabacademy.org/" target="_blank" rel="noopener noreferrer">Visit CyLab Security Academy ↗</a>
</article>
</div>

# Two Development Tracks

<div class="card-grid">
<article class="season-card track-techniques" markdown="1">

## CTF / Techniques Track

### pps{CyberTechniquesFest}

**CyberTacticsForge-led · Fall 2026**

Instruction and hands-on challenges in network and host investigation, enumeration, traffic analysis, credential/password work, web and service interaction, defensive analysis, and a Capture-the-Flag competition.

### CyLab Security Academy

**Optional continuing CTF opportunity · Dates announced by CyLab**

CyberTacticsForge will help connect interested students with CMU student mentors and local support where available. CyLab Security Academy controls and announces its own competitions.
</article>
<article class="season-card track-operations" markdown="1">

## Operational / Force-on-Force Track

### CyberPatriot

**CyberTacticsForge-sponsored and coordinated · Primarily RMU-coached · Fall 2026–January 2027**

An external competition emphasizing defensive system administration and hardening. Returning and advanced students are a natural fit, but the pathway remains open and invitational.

### pps{CyberTactics}

**CyberTacticsForge-led · Winter 2027**

A live team-vs-team environment focused on system administration, network operations, service uptime, segmentation, monitoring, detection, response, authorized red-team operations, communications, and tactical decision-making.
</article>
</div>

<p class="crossover"><strong>Students may move between tracks.</strong> New participants may begin with pps{CyberTechniquesFest} and later join pps{CyberTactics}. Returning students may spend the fall in CyberPatriot, then recruit teammates from the fall cohort.</p>

# 2026–27 Master Tentative Schedule

All dates are **tentative and subject to change**. Regular instruction follows the Tuesday and Thursday, 7:00–9:00 PM cadence, with selected Saturday labs and events.

<div class="schedule-key"><span class="schedule-label label-ctf">pps{CyberTechniquesFest}</span><span class="schedule-label label-tactics">pps{CyberTactics}</span><span class="schedule-label label-partner">External partner event</span><span class="schedule-label label-pause">Pause / no session</span></div>

<section class="schedule-month" markdown="1">

## October 2026 — Season Launch

<div class="schedule-event partner" markdown="1">**Thursday, October 1 — CyberPatriot 19 Registration Deadline** <span class="schedule-label label-partner">CyberPatriot</span>

Administrative milestone. Teams must be organized and registered; no CyberTacticsForge instruction is scheduled before October.</div>

<div class="schedule-event" markdown="1">**Tuesday, October 6 · 7:00–9:00 PM — pps{CyberTechniquesFest} Kickoff**

Welcome, team formation, environment access, tools and expectations, and an introduction to both tracks.</div>

<div class="schedule-event" markdown="1">**Thursday, October 8 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event" markdown="1">**Tuesday, October 13 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event" markdown="1">**Thursday, October 15 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event" markdown="1">**Saturday, October 17 — Optional Hands-On Lab**

Environment setup, VM/network familiarity, extended technical work, and open challenge time.</div>
<div class="schedule-event" markdown="1">**Tuesday, October 20 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event partner" markdown="1">**October 7–20 — CyberPatriot Practice Round** <span class="schedule-label label-partner">CyberPatriot</span>

External practice window; not a CyberTacticsForge instructional session.</div>
<div class="schedule-event partner" markdown="1">**October 22–25 — CyberPatriot Round 1** <span class="schedule-label label-partner">CyberPatriot</span>

External competition round with RMU-supported coaching.</div>
<div class="schedule-event" markdown="1">**Thursday, October 22 · 7:00–9:00 PM — CyberTechniquesFest Training**

Separate from CyberPatriot, with flexibility for students competing in that round.</div>
<div class="schedule-event" markdown="1">**Tuesday, October 27 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event" markdown="1">**Thursday, October 29 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event partner" markdown="1">**October 30–January 19 — CyberPatriot Training Round 2** <span class="schedule-label label-partner">CyberPatriot</span>

External CyberPatriot training window.</div>
</section>

<section class="schedule-month" markdown="1">

## November 2026 — Skill Building and Integration

<div class="schedule-event pause" markdown="1">**Tuesday, November 3 — No CyberTechniquesFest Session** <span class="schedule-label label-pause">No session</span>

PPS Election Day / no school.</div>
<div class="schedule-event" markdown="1">**Thursday, November 5 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event" markdown="1">**Saturday, November 7 — Mini-CTF / Open Lab**

Optional short challenge set and time-pressure practice.</div>
<div class="schedule-event" markdown="1">**Tuesday, November 10 · 7:00–9:00 PM — CyberTechniquesFest Training**</div>
<div class="schedule-event partner" markdown="1">**November 12–15 — CyberPatriot Round 2** <span class="schedule-label label-partner">CyberPatriot</span>

External competition round with RMU-supported coaching.</div>
<div class="schedule-event" markdown="1">**Thursday, November 12 · 7:00–9:00 PM — CyberTechniquesFest Training / Flexible Attendance**

The session remains available while accommodating CyberPatriot competitors.</div>
<div class="schedule-event" markdown="1">**Tuesday, November 17 · 7:00–9:00 PM — Integrated CyberTechniquesFest Challenges**</div>
<div class="schedule-event" markdown="1">**Thursday, November 19 · 7:00–9:00 PM — Integrated CyberTechniquesFest Challenges**</div>
<div class="schedule-event" markdown="1">**Saturday, November 21 — Full-Environment Lab**

Longer hands-on block, multi-role practice, and competition preparation.</div>
<div class="schedule-event pause" markdown="1">**November 24–26 — Thanksgiving Pause** <span class="schedule-label label-pause">Pause</span>

No required CyberTacticsForge sessions.</div>
</section>

<section class="schedule-month" markdown="1">

## December 2026 — CyberTechniquesFest Competition and Closeout

<div class="schedule-event" markdown="1">**Tuesday, December 1 · 7:00–9:00 PM — Competition Preparation / Final Rehearsal**</div>
<div class="schedule-event" markdown="1">**Thursday, December 3 · 7:00–9:00 PM — Competition Preparation / Final Rehearsal**</div>
<div class="schedule-event" markdown="1">**Saturday, December 5 — Optional Open Range / Technical Check**</div>
<div class="schedule-event" markdown="1">**December 7–9 — pps{CyberTechniquesFest} Competition Window** <span class="schedule-label label-ctf">Fall capstone</span>

The main fall CyberTacticsForge competition: a technique-focused CTF environment. Exact team slots may be scheduled separately.</div>
<div class="schedule-event partner" markdown="1">**December 10–13 — CyberPatriot State Round** <span class="schedule-label label-partner">CyberPatriot</span>

External competition round with RMU-supported coaching.</div>
<div class="schedule-event" markdown="1">**Tuesday, December 15 · 7:00–9:00 PM — CyberTechniquesFest After Action Review**

Results, feedback, recognition, and lessons learned.</div>
<div class="schedule-event" markdown="1">**Thursday, December 17 · 7:00–9:00 PM — Fall Season Closeout + pps{CyberTactics} Interest**

Recognize participants and introduce the distinct winter force-on-force model.</div>
<div class="schedule-event pause" markdown="1">**December 18–January 25 — Winter Pause** <span class="schedule-label label-pause">Pause</span>

No regular CyberTacticsForge instruction. CyberPatriot teams may continue independently with RMU coaches.</div>
</section>

<section class="schedule-month" markdown="1">

## January 2027 — pps{CyberTactics} Begins

The winter season is intentionally shorter, more mature, and operational. It is not another CTF: teams must keep systems functioning while defending, detecting, responding, and conducting authorized offensive operations.

<div class="schedule-event partner" markdown="1">**January 21–23 — CyberPatriot Semifinals** <span class="schedule-label label-partner">CyberPatriot</span>

For qualifying teams only; an external competition with RMU-supported coaching.</div>
<div class="schedule-event tactics" markdown="1">**Tuesday, January 26 · 7:00–9:00 PM — pps{CyberTactics} Kickoff: Operate the Network**

Team structure, topology, addressing, required services, scoring, uptime, change management, and operational responsibilities.</div>
<div class="schedule-event tactics" markdown="1">**Thursday, January 28 · 7:00–9:00 PM — Operate the Hosts**

Linux/Windows administration, permissions, services, configuration, backups, and restoration.</div>
</section>

<section class="schedule-month" markdown="1">

## February 2027 — Build, Operate, and Adapt

<div class="schedule-event tactics" markdown="1">**Tuesday, February 2 · 7:00–9:00 PM — Control the Network**

Routing, DNS/DHCP, firewall rules, segmentation, exposed services, and attack-surface management.</div>
<div class="schedule-event tactics" markdown="1">**Thursday, February 4 · 7:00–9:00 PM — See and Respond**

Logging, monitoring, Zeek/Suricata/SIEM concepts, triage, detection, incident response, communications, and rules of engagement.</div>
<div class="schedule-event tactics" markdown="1">**Saturday, February 6 — CyberTactics Build Day**

Configure the environment, assign roles, establish services, test connectivity, and baseline systems.</div>
<div class="schedule-event tactics" markdown="1">**Tuesday, February 9 · 7:00–9:00 PM — Team Build / Service Operations**</div>
<div class="schedule-event tactics" markdown="1">**Thursday, February 11 · 7:00–9:00 PM — Team Build / Attack Surface Review**</div>
<div class="schedule-event tactics" markdown="1">**Saturday, February 13 — Scrimmage #1: Controlled**

A bounded introduction to live opposing-team activity, focused on learning.</div>
<div class="schedule-event tactics" markdown="1">**Tuesday, February 16 · 7:00–9:00 PM — Scrimmage AAR / Defensive Restoration**</div>
<div class="schedule-event tactics" markdown="1">**Thursday, February 18 · 7:00–9:00 PM — Red-Team Planning / Defensive Adaptation**</div>
<div class="schedule-event tactics" markdown="1">**Saturday, February 20 — Scrimmage #2: Less Scripted**

More freedom and realistic service-defense pressure, with required communication and restoration.</div>
<div class="schedule-event tactics" markdown="1">**Tuesday, February 23 · 7:00–9:00 PM — Fix What Broke / Operational Improvement**</div>
<div class="schedule-event tactics" markdown="1">**Thursday, February 25 · 7:00–9:00 PM — Tactics, Communications, and Resilience**</div>
<div class="schedule-event tactics" markdown="1">**Saturday, February 27 — Full-Range Rehearsal**

Validate near-final rules, environment, scoring, resets, and infrastructure.</div>
</section>

<section class="schedule-month" markdown="1">

## March 2027 — Force-on-Force Capstone

<div class="schedule-event tactics" markdown="1">**Tuesday, March 2 · 7:00–9:00 PM — Final Configuration / Rules Review**</div>
<div class="schedule-event tactics" markdown="1">**Thursday, March 4 · 7:00–9:00 PM — Final Readiness**

Final technical checks and expectations; no major new instruction.</div>
<div class="schedule-event tactics" markdown="1">**Saturday, March 6 — pps{CyberTactics} Force-on-Force Competition** <span class="schedule-label label-tactics">Winter capstone</span>

Teams operate and defend functional network services against live adversarial activity. Success reflects service availability, defense, detection, recovery, offensive execution, and team decision-making.</div>
<div class="schedule-event tactics" markdown="1">**Tuesday, March 9 · 7:00–9:00 PM — CyberTactics AAR / Recognition / Season Close**</div>
<div class="schedule-event partner" markdown="1">**March 12–16 — CyberPatriot National Finals** <span class="schedule-label label-partner">CyberPatriot</span>

External national competition, only if a supported team qualifies.</div>
</section>

<div class="spring-callout" markdown="1">

## Spring 2027 — Optional CyLab Security Academy CTF Opportunities

**Dates: To Be Announced by CyLab Security Academy**

Students who want to continue developing CTF skills after pps{CyberTechniquesFest} may participate in CyLab Security Academy mini-competitions or its annual U.S. middle/high-school competition when dates are announced. CyberTacticsForge will help connect interested students with Carnegie Mellon University student mentors and local support where available.

Participation is optional and does not depend on pps{CyberTactics}. CyLab Security Academy operates and schedules its own competitions.

<!-- TODO: Replace with CYLAB_INTEREST_FORM_URL when available. -->
<span class="season-button disabled" aria-disabled="true">Express Interest — Coming Soon</span>
<a class="season-button" href="https://www.cylabacademy.org/" target="_blank" rel="noopener noreferrer">Visit CyLab Security Academy ↗</a>
</div>

# Which Track Is for Me?

These are recommended pathways, not hard prerequisites.

<div class="card-grid">
<article class="season-card" markdown="1">

## I like solving technical puzzles and finding flags.

Start with **pps{CyberTechniquesFest}** and consider **CyLab Security Academy**.
</article>
<article class="season-card" markdown="1">

## I like configuring systems, defending networks, and working on an operational team.

Consider **CyberPatriot** and **pps{CyberTactics}**.
</article>
<article class="season-card" markdown="1">

## I am new and do not know yet.

Start with **pps{CyberTechniquesFest}**. You can move between tracks as your interests and skills develop.
</article>
<article class="season-card" markdown="1">

## I have already competed for a year or two.

Consider **CyberPatriot in the fall**, then return for **pps{CyberTactics}** and recruit teammates from the fall cohort.
</article>
</div>

## A Nod of Respect to Those Who Help This Process

- Carnegie Mellon University's CTF community — coaches and mentors
- BlackGirlsHack — coaches and mentors
- Robert Morris University students — CyberPatriot coaching and technical support

</div>
