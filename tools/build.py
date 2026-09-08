#!/usr/bin/env python3
"""Render profile.md -> site/index.html for jw3b-dev.github.io (Tailwind, TOC, dark mode, print CSS).

Supported markdown: #..#### headings, *, -, 1. lists, **bold**, *em*, `code`, [text](url),
fenced ``` code blocks, | pipe | tables |, > blockquotes. Sections are split on '---' lines.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "profile.md"
DST = HERE.parent / "site" / "index.html"

# Section heading prefix -> side illustration (sections without one render full width)
IMAGES: dict[str, str] = {}
# Attribution for images whose licence requires it (rendered as a caption under the image)
CREDITS: dict[str, tuple[str, str]] = {}
LIVE_STATUS_URL = "https://live.jw3b.dev/status.json" Pi feed, see pi/README.md# Pi feed, see pi/README.md

SECTION_KEY = re.compile(r"^## ((?:Mod|Part) \d+[a-z]?)\b", re.M)

# jw3b.dev brand header (BrandHeader.jsx, mode="full") translated to static Tailwind.
# BRAND ASSET: Copyright (c) 2026 John Wellard (jw3b.dev). All rights reserved.
# Not covered by the repository MIT license; see brand/LICENSE-BRAND.md.
BRAND_HEADER = (
 Pi feed, see pi/README.md  '<a href="https://jw3b.dev" class="jw3b-brand font-mono flex items-center gap-2 select-none mr-2 shrink-0" title="jw3b.dev">'
 Pi feed, see pi/README.md  '<span class="text-emerald-400 font-semibold tracking-tight"><span class="mr-[0.35em]">~❯</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-t text-slate-100" style="--i:0">J</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-t text-slate-100" style="--i:1">W</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-t text-cyan-400" style="--i:2">3</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-t text-slate-100" style="--i:3">B</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-t text-cyan-400" style="--i:4">.</span>'
 Pi feed, see pi/README.md  '<span class="jw3b-cursor text-emerald-400" aria-hidden="true">_</span></span></a>'
)

HEAD = """<!DOCTYPE html>
<!-- Content: MIT (github.com/jw3b-dev/jw3b-dev.github.io). Brand assets (JW3B. mark, prompt, // STAY WEIRD, header/footer): (c) 2026 John Wellard, all rights reserved. -->
<html lang="en" class="dark">
<head>
 Pi feed, see pi/README.md  <meta charset="UTF-8">
 Pi feed, see pi/README.md  <meta name="viewport" content="width=device-width, initial-scale=1.0">
 Pi feed, see pi/README.md  <title>jw3b.dev // John Wellard</title>
 Pi feed, see pi/README.md  <meta name="description" content="John Wellard (JW3B / AgileGypsy) — Senior Agentic AI Developer &amp; Smart-Contract Auditor. GitHub profile site; the operable portfolio lives at jw3b.dev.">
 Pi feed, see pi/README.md  <meta name="color-scheme" content="dark">
 Pi feed, see pi/README.md  <meta name="theme-color" content="#020617">
 Pi feed, see pi/README.md  <script src="https://cdn.tailwindcss.com"></script>
 Pi feed, see pi/README.md  <script>tailwind.config = { darkMode: 'class', theme: { extend: { fontFamily: { mono: ['"IBM Plex Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'], sans: ['Geist', 'ui-sans-serif', 'system-ui', 'sans-serif'] } } } }</script>
 Pi feed, see pi/README.md  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
 Pi feed, see pi/README.md  <style>
 Pi feed, see pi/README.md      html { scroll-behavior: smooth; scroll-padding-top: 4.5rem; }
 Pi feed, see pi/README.md      body {
 Pi feed, see pi/README.md          font-family: 'Geist', ui-sans-serif, system-ui, sans-serif; background-color: #020617; color: #cbd5e1;
 Pi feed, see pi/README.md          background-image: linear-gradient(rgba(34,211,238,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(34,211,238,.045) 1px, transparent 1px);
 Pi feed, see pi/README.md          background-size: 32px 32px;
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md      .mono { font-family: 'IBM Plex Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace; }
 Pi feed, see pi/README.md      .glow { text-shadow: 0 0 18px rgba(34,211,238,.35); }
 Pi feed, see pi/README.md      .panel { background: rgba(15,23,42,.72); border: 1px solid #1e293b; box-shadow: 0 0 0 1px rgba(34,211,238,.04), 0 20px 60px -30px rgba(34,211,238,.25); backdrop-filter: blur(6px); }
 Pi feed, see pi/README.md      .panel-bar { border-bottom: 1px solid #1e293b; background: rgba(2,6,23,.6); }
 Pi feed, see pi/README.md      .content p { margin-bottom: 1rem; line-height: 1.7; }
 Pi feed, see pi/README.md      .content li { margin-bottom: 0.5rem; line-height: 1.6; }
 Pi feed, see pi/README.md      .content ul > li::marker { color: #22d3ee; }
 Pi feed, see pi/README.md      .content ol > li::marker { color: #34d399; font-family: 'IBM Plex Mono', ui-monospace, monospace; }
 Pi feed, see pi/README.md      .content code { font-family: 'IBM Plex Mono', ui-monospace, monospace; background: rgba(34,211,238,.08); color: #67e8f9; border: 1px solid rgba(34,211,238,.15); padding: 0.1rem 0.4rem; border-radius: 0.25rem; font-size: 0.85em; }
 Pi feed, see pi/README.md      .content pre { font-family: 'IBM Plex Mono', ui-monospace, monospace; background: #020617; color: #a7f3d0; border: 1px solid #1e293b; border-left: 3px solid #34d399; padding: 1rem 1.25rem; border-radius: 0.375rem; overflow-x: auto; margin: 0 0 1rem; font-size: 0.82rem; line-height: 1.55; }
 Pi feed, see pi/README.md      .content pre code { background: none; border: 0; color: inherit; padding: 0; font-size: inherit; }
 Pi feed, see pi/README.md      .content table { width: 100%; border-collapse: collapse; margin: 0 0 1.25rem; font-size: 0.88rem; }
 Pi feed, see pi/README.md      .content th, .content td { border: 1px solid #1e293b; padding: 0.55rem 0.75rem; text-align: left; vertical-align: top; }
 Pi feed, see pi/README.md      .content th { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-weight: 600; font-size: 0.75rem; letter-spacing: .06em; text-transform: uppercase; color: #22d3ee; background: rgba(2,6,23,.7); }
 Pi feed, see pi/README.md      .content tr:nth-child(even) td { background: rgba(2,6,23,.35); }
 Pi feed, see pi/README.md      .content blockquote { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: 0.85rem; border: 1px solid rgba(251,191,36,.35); border-left: 3px solid #fbbf24; background: rgba(251,191,36,.06); color: #fde68a; padding: 0.75rem 1rem; margin: 0 0 1rem; border-radius: 0 0.375rem 0.375rem 0; }
 Pi feed, see pi/README.md      .content blockquote p { margin: 0; }
 Pi feed, see pi/README.md      .content blockquote p::before { content: "// WARN  "; color: #fbbf24; font-weight: 700; }
 Pi feed, see pi/README.md      .content a { color: #22d3ee; text-decoration: underline; text-decoration-color: rgba(34,211,238,.4); text-underline-offset: 3px; }
 Pi feed, see pi/README.md      .content a:hover { color: #67e8f9; text-decoration-color: #67e8f9; }
 Pi feed, see pi/README.md      .content h2 .hash { color: #22d3ee; margin-right: .5rem; }
 Pi feed, see pi/README.md      .table-wrap { overflow-x: auto; }
 Pi feed, see pi/README.md      .no-scrollbar { scrollbar-width: none; } .no-scrollbar::-webkit-scrollbar { display: none; }
 Pi feed, see pi/README.md      .fig { border: 1px solid #1e293b; border-radius: .375rem; overflow: hidden; background: #020617; }
 Pi feed, see pi/README.md      .fig img { filter: saturate(.85) contrast(1.05); opacity: .9; transition: all .3s; }
 Pi feed, see pi/README.md      .fig:hover img { filter: none; opacity: 1; }
 Pi feed, see pi/README.md      /* jw3b.dev brand: the mark types itself in after the prompt, then a terminal cursor blinks */
 Pi feed, see pi/README.md      .jw3b-t { opacity: 0; animation: jw3b-in 0.01s steps(1) forwards; animation-delay: calc(0.5s + var(--i) * 0.14s); }
 Pi feed, see pi/README.md      .jw3b-cursor { animation: jw3b-blink 1s steps(1, end) infinite; }
 Pi feed, see pi/README.md      .jw3b-brand:hover .jw3b-t { animation: jw3b-in 0.01s steps(1) forwards; animation-delay: calc(var(--i) * 0.12s); opacity: 0; }
 Pi feed, see pi/README.md      .hero-line { opacity: 0; animation: jw3b-in 0.01s steps(1) forwards; }
 Pi feed, see pi/README.md      @keyframes jw3b-in { to { opacity: 1; } }
 Pi feed, see pi/README.md      @keyframes jw3b-blink { 0%, 50% { opacity: 1; } 50.01%, 100% { opacity: 0; } }
 Pi feed, see pi/README.md      @keyframes scan { from { transform: translateY(-100%); } to { transform: translateY(100vh); } }
 Pi feed, see pi/README.md      .scan { pointer-events: none; position: fixed; left: 0; right: 0; top: 0; height: 2px; background: linear-gradient(90deg, transparent, rgba(34,211,238,.25), transparent); animation: scan 9s linear infinite; z-index: 5; }
 Pi feed, see pi/README.md      @media (prefers-reduced-motion: reduce) {
 Pi feed, see pi/README.md          .jw3b-t, .jw3b-brand:hover .jw3b-t, .hero-line { animation: none; opacity: 1; }
 Pi feed, see pi/README.md          .jw3b-cursor, .scan { animation: none; }
 Pi feed, see pi/README.md          .scan { display: none; }
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md      @media print {
 Pi feed, see pi/README.md          nav, .hero-img, footer, .scan { display: none !important; }
 Pi feed, see pi/README.md          body { background: #fff !important; color: #000 !important; background-image: none !important; }
 Pi feed, see pi/README.md          .panel { background: #fff !important; border: 1px solid #ccc !important; box-shadow: none !important; break-inside: avoid; }
 Pi feed, see pi/README.md          .content pre { background: #f3f4f6 !important; color: #000 !important; border: 1px solid #ccc; }
 Pi feed, see pi/README.md          a { color: #000 !important; text-decoration: none; }
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md  </style>
</head>
<body class="antialiased">
 Pi feed, see pi/README.md  <div class="scan"></div>

 Pi feed, see pi/README.md  <!-- Hero: a terminal window. The brand mark types itself in; the readouts are the current jw3b.dev status. -->
 Pi feed, see pi/README.md  <header class="max-w-6xl mx-auto px-6 pt-10 pb-4">
 Pi feed, see pi/README.md      <div class="panel rounded-lg overflow-hidden">
 Pi feed, see pi/README.md          <div class="panel-bar px-4 py-2 flex items-center gap-3 mono text-xs text-slate-500">
 Pi feed, see pi/README.md              <span class="flex gap-1.5"><span class="h-3 w-3 rounded-full bg-rose-500/80"></span><span class="h-3 w-3 rounded-full bg-amber-400/80"></span><span class="h-3 w-3 rounded-full bg-emerald-400/80"></span></span>
 Pi feed, see pi/README.md              <span>jw3b@agilegypsy-labs: ~</span>
 Pi feed, see pi/README.md              <span class="ml-auto hidden sm:inline">build __BUILD__ · <span id="jw3b-net-top">🟢 connected</span> <span id="jw3b-live-top" class="text-slate-600">· live: probing…</span></span>
 Pi feed, see pi/README.md          </div>
 Pi feed, see pi/README.md          <div class="grid lg:grid-cols-5 gap-8 px-6 sm:px-10 py-10">
 Pi feed, see pi/README.md              <div class="lg:col-span-3 mono">
 Pi feed, see pi/README.md                  <div class="text-5xl sm:text-7xl font-semibold tracking-tight glow mb-6 jw3b-brand">
 Pi feed, see pi/README.md                      <span class="text-emerald-400 mr-[0.2em]">~❯</span><span class="jw3b-t text-slate-100" style="--i:0">J</span><span class="jw3b-t text-slate-100" style="--i:1">W</span><span class="jw3b-t text-cyan-400" style="--i:2">3</span><span class="jw3b-t text-slate-100" style="--i:3">B</span><span class="jw3b-t text-cyan-400" style="--i:4">.</span><span class="jw3b-cursor text-emerald-400" aria-hidden="true">_</span>
 Pi feed, see pi/README.md                  </div>
 Pi feed, see pi/README.md                  <p class="hero-line text-slate-500 text-sm mb-1" style="animation-delay:1.4s"><span class="text-emerald-400">~❯</span> cat about.md</p>
 Pi feed, see pi/README.md                  <h1 class="hero-line text-2xl sm:text-3xl font-bold text-slate-100 leading-tight mb-3" style="animation-delay:1.6s">John Wellard <span class="text-cyan-400">//</span> Senior Agentic AI Developer &amp; Smart-Contract Auditor</h1>
 Pi feed, see pi/README.md                  <p class="hero-line font-sans text-slate-400 text-base leading-relaxed max-w-xl" style="animation-delay:1.8s">AgileGypsy Labs: live products with paying users, not slideware. Ships agentic AI end-to-end, from multi-agent pipelines and graph retrieval to edge RAG, and audits smart contracts with a competitive record behind it. This is the GitHub mirror; the portfolio you can actually operate is at <a href="https://jw3b.dev" class="text-cyan-300 underline underline-offset-4">jw3b.dev</a>.</p>
 Pi feed, see pi/README.md                  <p class="hero-line mt-5 flex flex-wrap gap-2 text-xs" style="animation-delay:2.0s">
 Pi feed, see pi/README.md                      <a href="https://jw3b.dev/hire-me" class="border border-cyan-400/40 text-cyan-300 px-3 py-1 rounded hover:bg-cyan-400/10">./hire-me</a>
 Pi feed, see pi/README.md                      <a href="https://jw3b.dev/audit" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-cyan-400/40 hover:text-cyan-300">./audit</a>
 Pi feed, see pi/README.md                      <a href="https://jw3b.dev/ctf" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-cyan-400/40 hover:text-cyan-300">./ctf</a>
 Pi feed, see pi/README.md                      <a href="https://jw3b.dev/work" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-cyan-400/40 hover:text-cyan-300">./work</a>
 Pi feed, see pi/README.md                      <a href="https://github.com/jw3b-dev" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-emerald-400/40 hover:text-emerald-300">gh repo list</a>
 Pi feed, see pi/README.md                  </p>
 Pi feed, see pi/README.md              </div>
 Pi feed, see pi/README.md              <div class="lg:col-span-2 mono text-xs hero-line" style="animation-delay:1.2s">
 Pi feed, see pi/README.md                  <div class="border border-slate-800 rounded bg-slate-950/80 p-4 space-y-1.5">
 Pi feed, see pi/README.md                      <div class="text-slate-500 mb-2">// status · synced with jw3b.dev</div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">handle</span><span class="text-slate-100">JW3B <span class="text-slate-500">/ AgileGypsy</span></span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">role</span><span class="text-cyan-300 text-right">agentic AI dev · smart-contract auditor</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">labs</span><span class="text-slate-300">AgileGypsy Labs · UK</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">codehawks</span><span class="text-emerald-400 text-right">#124 · 17 findings · 8 High</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">exp</span><span class="text-emerald-400">1,430</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">stack</span><span class="text-slate-300 text-right">Claude · React 19 · Workers · Foundry · Base</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">live_surfaces</span><span class="text-slate-300">/audit · /ctf · /work · concierge</span></div>
 Pi feed, see pi/README.md                      <div class="flex justify-between gap-4"><span class="text-slate-400">availability</span><span class="text-amber-300">open to engagements</span></div>
 Pi feed, see pi/README.md                      <div id="jw3b-live-rows" hidden class="pt-2 mt-2 border-t border-slate-800 space-y-1.5"></div>
 Pi feed, see pi/README.md                      <div class="pt-2 mt-2 border-t border-slate-800 text-slate-500">verdict: <span class="text-cyan-300">ships. audits. stays weird.</span></div>
 Pi feed, see pi/README.md                  </div>
 Pi feed, see pi/README.md              </div>
 Pi feed, see pi/README.md          </div>
 Pi feed, see pi/README.md      </div>
 Pi feed, see pi/README.md  </header>
"""

FOOT = """
 Pi feed, see pi/README.md  <!-- IdeFooter.jsx translated to static Tailwind; status values are live, not hardcoded.
 Pi feed, see pi/README.md       BRAND ASSET: (c) 2026 John Wellard (jw3b.dev). All rights reserved. See brand/LICENSE-BRAND.md. -->
 Pi feed, see pi/README.md  <footer class="mt-12 bg-slate-950 border-t border-slate-800 font-mono text-slate-500">
 Pi feed, see pi/README.md      <div class="max-w-6xl mx-auto px-6 py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm">
 Pi feed, see pi/README.md          <div class="flex items-center gap-3">
 Pi feed, see pi/README.md              <a href="https://jw3b.dev" class="font-semibold tracking-tight text-slate-100 hover:text-cyan-400">JW<span class="text-cyan-400">3</span>B<span class="text-cyan-400">.</span></a>
 Pi feed, see pi/README.md              <span class="text-slate-700">|</span>
 Pi feed, see pi/README.md              <a href="https://github.com/jw3b-dev" class="hover:text-cyan-400">github.com/jw3b-dev</a>
 Pi feed, see pi/README.md              <span class="text-slate-700">|</span>
 Pi feed, see pi/README.md              <a href="https://jw3b-dev.github.io/crosshair15-cooling/" class="hover:text-cyan-400">crosshair15-cooling</a>
 Pi feed, see pi/README.md          </div>
 Pi feed, see pi/README.md          <div class="text-slate-600 text-xs text-right">jw3b.dev &middot; AgileGypsy Labs &middot; GitHub profile site &middot; <a href="https://github.com/jw3b-dev/jw3b-dev.github.io/blob/main/LICENSE" class="hover:text-cyan-400">code MIT</a><br>&copy; 2026 John Wellard &middot; JW3B. mark, prompt and <span class="text-slate-500">// STAY WEIRD</span> are brand assets, <a href="https://github.com/jw3b-dev/jw3b-dev.github.io/blob/main/brand/LICENSE-BRAND.md" class="hover:text-cyan-400">all rights reserved</a></div>
 Pi feed, see pi/README.md      </div>
 Pi feed, see pi/README.md      <div class="h-6 w-full bg-slate-950 border-t border-slate-800 px-3 flex items-center justify-between text-xs">
 Pi feed, see pi/README.md          <div class="flex items-center gap-3">
 Pi feed, see pi/README.md              <span class="flex items-center gap-1 text-emerald-400">
 Pi feed, see pi/README.md                  <span class="relative flex h-2 w-2"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span></span>
 Pi feed, see pi/README.md                  THERMAL_GUIDE_ONLINE
 Pi feed, see pi/README.md              </span>
 Pi feed, see pi/README.md              <span>|</span>
 Pi feed, see pi/README.md              <span>ENV: PRODUCTION</span>
 Pi feed, see pi/README.md              <span class="hidden sm:inline">|</span>
 Pi feed, see pi/README.md              <span id="jw3b-live-foot" class="hidden sm:inline text-slate-600">PI: probing…</span>
 Pi feed, see pi/README.md              <span class="hidden sm:inline">|</span>
 Pi feed, see pi/README.md              <span class="hidden sm:inline">BUILD: __BUILD__ | <span id="jw3b-net">🟢 connected</span> | latency: <span id="jw3b-lat">…</span></span>
 Pi feed, see pi/README.md          </div>
 Pi feed, see pi/README.md          <div class="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
 Pi feed, see pi/README.md              <span>// STAY WEIRD</span>
 Pi feed, see pi/README.md              <span class="text-sm">👽</span>
 Pi feed, see pi/README.md          </div>
 Pi feed, see pi/README.md      </div>
 Pi feed, see pi/README.md  </footer>
 Pi feed, see pi/README.md  <script>
 Pi feed, see pi/README.md    (function () {
 Pi feed, see pi/README.md      var lat = document.getElementById('jw3b-lat'), net = document.getElementById('jw3b-net');
 Pi feed, see pi/README.md      function tick() {
 Pi feed, see pi/README.md        var nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
 Pi feed, see pi/README.md        var ms = nav ? Math.max(1, Math.round(nav.responseStart - nav.requestStart)) : null;
 Pi feed, see pi/README.md        if (lat) lat.textContent = ms ? ms + 'ms' : 'n/a';
 Pi feed, see pi/README.md        var txt = navigator.onLine ? '🟢 connected' : '🔴 offline';
 Pi feed, see pi/README.md        if (net) net.textContent = txt;
 Pi feed, see pi/README.md        var top = document.getElementById('jw3b-net-top'); if (top) top.textContent = txt;
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md      tick(); window.addEventListener('online', tick); window.addEventListener('offline', tick);
 Pi feed, see pi/README.md      var URL_ = '__LIVE_STATUS_URL__', top_ = document.getElementById('jw3b-live-top'), foot = document.getElementById('jw3b-live-foot'), rows = document.getElementById('jw3b-live-rows');
 Pi feed, see pi/README.md      function row(k, v, cls) { return '<div class="flex justify-between gap-4"><span class="text-slate-400">' + k + '</span><span class="' + (cls || 'text-slate-300') + ' text-right">' + v + '</span></div>'; }
 Pi feed, see pi/README.md      function fmtUp(s) { var d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600); return (d ? d + 'd ' : '') + h + 'h'; }
 Pi feed, see pi/README.md      function down(why) {
 Pi feed, see pi/README.md        if (top_) { top_.textContent = '· live: offline'; top_.className = 'text-slate-600'; }
 Pi feed, see pi/README.md        if (foot) { foot.textContent = 'PI_OFFLINE · ' + why + ' · static fallback'; foot.className = 'hidden sm:inline text-slate-600'; }
 Pi feed, see pi/README.md        if (rows) rows.hidden = true;
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md      function live() {
 Pi feed, see pi/README.md        var t0 = performance.now(), ctl = new AbortController(), tm = setTimeout(function () { ctl.abort(); }, 4000);
 Pi feed, see pi/README.md        fetch(URL_, { signal: ctl.signal, cache: 'no-store' }).then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); }).then(function (s) {
 Pi feed, see pi/README.md          clearTimeout(tm); var ms = Math.round(performance.now() - t0);
 Pi feed, see pi/README.md          var svc = Object.keys(s.services || {}).map(function (k) { return k + '=' + s.services[k]; }).join(' ');
 Pi feed, see pi/README.md          if (top_) { top_.textContent = '· live: ' + s.host + ' · ' + (s.cpu_temp_c != null ? s.cpu_temp_c + '°C · ' : '') + 'load ' + s.load1; top_.className = 'text-emerald-400'; }
 Pi feed, see pi/README.md          if (foot) { foot.textContent = 'PI_ONLINE · ' + s.host + ' · rtt ' + ms + 'ms'; foot.className = 'hidden sm:inline text-emerald-400'; }
 Pi feed, see pi/README.md          if (rows) {
 Pi feed, see pi/README.md            rows.innerHTML = '<div class="text-slate-500">// live · ' + (s.model || s.arch) + '</div>'
 Pi feed, see pi/README.md              + row('uptime', fmtUp(s.uptime_s)) + row('load', s.load1) + (s.cpu_temp_c != null ? row('cpu_temp', s.cpu_temp_c + ' °C', s.cpu_temp_c > 70 ? 'text-amber-300' : 'text-emerald-400') : '')
 Pi feed, see pi/README.md              + row('mem / disk', s.mem_used_pct + '% / ' + s.disk_used_pct + '%') + (svc ? row('services', svc, 'text-cyan-300') : '');
 Pi feed, see pi/README.md            rows.hidden = false;
 Pi feed, see pi/README.md          }
 Pi feed, see pi/README.md        }).catch(function (e) { clearTimeout(tm); down(e.name === 'AbortError' ? 'timeout' : 'unreachable'); });
 Pi feed, see pi/README.md      }
 Pi feed, see pi/README.md      live(); setInterval(live, 30000);
 Pi feed, see pi/README.md    })();
 Pi feed, see pi/README.md  </script>
</body>
</html>
"""


def slug(text: str) -> str:
 Pi feed, see pi/README.md  s = re.sub(r"<[^>]+>", "", text).lower()
 Pi feed, see pi/README.md  s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
 Pi feed, see pi/README.md  return s or "section"


def inline(text: str) -> str:
 Pi feed, see pi/README.md  """Escape HTML, then apply inline markdown."""
 Pi feed, see pi/README.md  t = html.escape(text, quote=False)
 Pi feed, see pi/README.md  t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
 Pi feed, see pi/README.md  t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
 Pi feed, see pi/README.md  # bare URLs (not already inside an href or a markdown link)
 Pi feed, see pi/README.md  t = re.sub(r'(?<!["\'>(])(https?://[^\s<>"]+?)(?=[.,;:)]*(?:\s|$))',
 Pi feed, see pi/README.md             r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
 Pi feed, see pi/README.md  t = re.sub(r"\*\*(.+?)\*\*", r'<strong class="text-slate-100 font-semibold">\1</strong>', t)
 Pi feed, see pi/README.md  t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r'<em class="text-slate-400">\1</em>', t)
 Pi feed, see pi/README.md  return t


def render_table(rows: list[str]) -> str:
 Pi feed, see pi/README.md  cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
 Pi feed, see pi/README.md  if len(cells) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in cells[1] if c):
 Pi feed, see pi/README.md      head, body = cells[0], cells[2:]
 Pi feed, see pi/README.md  else:
 Pi feed, see pi/README.md      head, body = None, cells
 Pi feed, see pi/README.md  out = ['<div class="table-wrap"><table>']
 Pi feed, see pi/README.md  if head:
 Pi feed, see pi/README.md      out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
 Pi feed, see pi/README.md  out.append("<tbody>")
 Pi feed, see pi/README.md  for r in body:
 Pi feed, see pi/README.md      out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
 Pi feed, see pi/README.md  out.append("</tbody></table></div>")
 Pi feed, see pi/README.md  return "\n".join(out) + "\n"


class Renderer:
 Pi feed, see pi/README.md  def __init__(self):
 Pi feed, see pi/README.md      self.out: list[str] = []
 Pi feed, see pi/README.md      self.list_type: str | None = None
 Pi feed, see pi/README.md      self.table: list[str] = []
 Pi feed, see pi/README.md      self.quote: list[str] = []
 Pi feed, see pi/README.md      self.toc: list[tuple[str, str]] = []

 Pi feed, see pi/README.md  def close_list(self):
 Pi feed, see pi/README.md      if self.list_type:
 Pi feed, see pi/README.md          self.out.append(f"</{self.list_type}>\n")
 Pi feed, see pi/README.md          self.list_type = None

 Pi feed, see pi/README.md  def flush_table(self):
 Pi feed, see pi/README.md      if self.table:
 Pi feed, see pi/README.md          self.out.append(render_table(self.table))
 Pi feed, see pi/README.md          self.table = []

 Pi feed, see pi/README.md  def flush_quote(self):
 Pi feed, see pi/README.md      if self.quote:
 Pi feed, see pi/README.md          self.out.append("<blockquote>" + "".join(f"<p>{inline(q)}</p>" for q in self.quote) + "</blockquote>\n")
 Pi feed, see pi/README.md          self.quote = []

 Pi feed, see pi/README.md  def flush_all(self):
 Pi feed, see pi/README.md      self.close_list()
 Pi feed, see pi/README.md      self.flush_table()
 Pi feed, see pi/README.md      self.flush_quote()

 Pi feed, see pi/README.md  def section(self, text: str) -> str:
 Pi feed, see pi/README.md      self.out = []
 Pi feed, see pi/README.md      lines = text.strip("\n").split("\n")
 Pi feed, see pi/README.md      i = 0
 Pi feed, see pi/README.md      while i < len(lines):
 Pi feed, see pi/README.md          raw = lines[i]
 Pi feed, see pi/README.md          line = raw.strip()

 Pi feed, see pi/README.md          if line.startswith("```"):
 Pi feed, see pi/README.md              self.flush_all()
 Pi feed, see pi/README.md              lang = line[3:].strip()
 Pi feed, see pi/README.md              buf = []
 Pi feed, see pi/README.md              i += 1
 Pi feed, see pi/README.md              while i < len(lines) and not lines[i].strip().startswith("```"):
 Pi feed, see pi/README.md                  buf.append(lines[i])
 Pi feed, see pi/README.md                  i += 1
 Pi feed, see pi/README.md              cls = f' class="language-{lang}"' if lang else ""
 Pi feed, see pi/README.md              self.out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre>\n")
 Pi feed, see pi/README.md              i += 1
 Pi feed, see pi/README.md              continue

 Pi feed, see pi/README.md          if line.startswith("|"):
 Pi feed, see pi/README.md              self.close_list(); self.flush_quote()
 Pi feed, see pi/README.md              self.table.append(line)
 Pi feed, see pi/README.md              i += 1
 Pi feed, see pi/README.md              continue
 Pi feed, see pi/README.md          self.flush_table()

 Pi feed, see pi/README.md          if line.startswith(">"):
 Pi feed, see pi/README.md              self.close_list()
 Pi feed, see pi/README.md              self.quote.append(line[1:].strip())
 Pi feed, see pi/README.md              i += 1
 Pi feed, see pi/README.md              continue
 Pi feed, see pi/README.md          self.flush_quote()

 Pi feed, see pi/README.md          if not line:
 Pi feed, see pi/README.md              i += 1
 Pi feed, see pi/README.md              continue

 Pi feed, see pi/README.md          if line.startswith("# "):
 Pi feed, see pi/README.md              pass  # document title lives in the hero
 Pi feed, see pi/README.md          elif line.startswith("## "):
 Pi feed, see pi/README.md              self.close_list()
 Pi feed, see pi/README.md              title = inline(line[3:])
 Pi feed, see pi/README.md              sid = slug(line[3:])
 Pi feed, see pi/README.md              self.toc.append((sid, line[3:]))
 Pi feed, see pi/README.md              self.out.append(f'<h2 id="{sid}" class="mono text-2xl sm:text-3xl font-bold text-slate-100 tracking-tight mb-6 mt-2"><span class="hash">#</span>{title}</h2>\n')
 Pi feed, see pi/README.md          elif line.startswith("### "):
 Pi feed, see pi/README.md              self.close_list()
 Pi feed, see pi/README.md              self.out.append(f'<h3 class="mono text-lg font-semibold text-cyan-300 mt-8 mb-4"><span class="text-slate-600 mr-2">##</span>{inline(line[4:])}</h3>\n')
 Pi feed, see pi/README.md          elif line.startswith("#### "):
 Pi feed, see pi/README.md              self.close_list()
 Pi feed, see pi/README.md              self.out.append(f'<h4 class="mono text-xs font-semibold text-emerald-400 mt-6 mb-2 uppercase tracking-widest">{inline(line[5:])}</h4>\n')
 Pi feed, see pi/README.md          elif line.startswith(("* ", "- ")):
 Pi feed, see pi/README.md              if self.list_type != "ul":
 Pi feed, see pi/README.md                  self.close_list()
 Pi feed, see pi/README.md                  self.out.append('<ul class="list-disc pl-6 mb-4 space-y-2 text-slate-300">\n')
 Pi feed, see pi/README.md                  self.list_type = "ul"
 Pi feed, see pi/README.md              self.out.append(f"<li>{inline(line[2:])}</li>\n")
 Pi feed, see pi/README.md          elif re.match(r"^\d+\.\s", line):
 Pi feed, see pi/README.md              if self.list_type != "ol":
 Pi feed, see pi/README.md                  self.close_list()
 Pi feed, see pi/README.md                  start = int(line.split(".", 1)[0])
 Pi feed, see pi/README.md                  attr = f' start="{start}"' if start != 1 else ""
 Pi feed, see pi/README.md                  self.out.append(f'<ol{attr} class="list-decimal pl-6 mb-4 space-y-2 text-slate-300">\n')
 Pi feed, see pi/README.md                  self.list_type = "ol"
 Pi feed, see pi/README.md              self.out.append(f'<li class="pl-2">{inline(re.sub(r"^\d+\.\s*", "", line))}</li>\n')
 Pi feed, see pi/README.md          else:
 Pi feed, see pi/README.md              self.close_list()
 Pi feed, see pi/README.md              self.out.append(f'<p class="text-slate-300">{inline(line)}</p>\n')
 Pi feed, see pi/README.md          i += 1

 Pi feed, see pi/README.md      self.flush_all()
 Pi feed, see pi/README.md      return "".join(self.out)


def build_id() -> str:
 Pi feed, see pi/README.md  import subprocess
 Pi feed, see pi/README.md  try:
 Pi feed, see pi/README.md      return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, stderr=subprocess.DEVNULL, text=True).strip()
 Pi feed, see pi/README.md  except Exception:
 Pi feed, see pi/README.md      return "dev"


def convert_to_html():
 Pi feed, see pi/README.md  md = SRC.read_text()
 Pi feed, see pi/README.md  sections = [s for s in re.split(r"\n---+\n", md) if s.strip()]
 Pi feed, see pi/README.md  r = Renderer()

 Pi feed, see pi/README.md  rendered = []
 Pi feed, see pi/README.md  for sec in sections:
 Pi feed, see pi/README.md      m = SECTION_KEY.search(sec)
 Pi feed, see pi/README.md      img = IMAGES.get(m.group(1)) if m else None
 Pi feed, see pi/README.md      credit = CREDITS.get(m.group(1)) if m else None
 Pi feed, see pi/README.md      caption = (f'<p class="mono text-[10px] text-slate-500 mt-2 text-center">// photo: <a href="{credit[1]}" class="underline" target="_blank" rel="noopener">{credit[0]}</a></p>'
 Pi feed, see pi/README.md                 if credit else "")
 Pi feed, see pi/README.md      body = r.section(sec)
 Pi feed, see pi/README.md      h = re.search(r"^## (.+)$", sec, re.M)
 Pi feed, see pi/README.md      label = slug(h.group(1)) if h else "readme"
 Pi feed, see pi/README.md      bar = f'<div class="panel-bar px-5 py-1.5 mono text-[11px] text-slate-500 flex items-center gap-2"><span class="text-emerald-400">~❯</span> less {label}.md <span class="ml-auto text-slate-700">jw3b.dev</span></div>'
 Pi feed, see pi/README.md      if img:
 Pi feed, see pi/README.md          rendered.append(
 Pi feed, see pi/README.md              f'<section class="panel rounded-lg overflow-hidden">{bar}<div class="flex flex-col lg:flex-row">\n'
 Pi feed, see pi/README.md              f'<div class="p-6 sm:p-8 content lg:w-2/3">{body}</div>\n'
 Pi feed, see pi/README.md              '<div class="lg:w-1/3 flex flex-col items-center justify-start p-6 sm:p-8 border-t lg:border-t-0 lg:border-l border-slate-800 hero-img">'
 Pi feed, see pi/README.md              f'<div class="fig lg:sticky lg:top-24"><img src="{img}" alt="Mod Illustration" loading="lazy" onerror="this.closest(\'.hero-img\').remove()" class="max-w-full h-auto object-contain max-h-80"></div>{caption}</div>\n'
 Pi feed, see pi/README.md              "</div></section>"
 Pi feed, see pi/README.md          )
 Pi feed, see pi/README.md      else:
 Pi feed, see pi/README.md          rendered.append(
 Pi feed, see pi/README.md              f'<section class="panel rounded-lg overflow-hidden">{bar}<div class="p-6 sm:p-8 content">'
 Pi feed, see pi/README.md              f"{body}</div></section>"
 Pi feed, see pi/README.md          )

 Pi feed, see pi/README.md  nav = (
 Pi feed, see pi/README.md      '<nav class="sticky top-0 z-20 bg-slate-950/90 backdrop-blur border-y border-slate-800 mb-10">'
 Pi feed, see pi/README.md      '<div class="max-w-6xl mx-auto px-6 py-2 flex flex-nowrap items-center gap-x-4 text-xs mono overflow-x-auto no-scrollbar">'
 Pi feed, see pi/README.md      + BRAND_HEADER +
 Pi feed, see pi/README.md      '<span class="text-slate-700 hidden sm:inline">|</span>'
 Pi feed, see pi/README.md      + "".join(
 Pi feed, see pi/README.md          f'<a href="#{sid}" class="text-slate-400 hover:text-cyan-300 whitespace-nowrap">{inline(t.split(":")[0])}</a>'
 Pi feed, see pi/README.md          for sid, t in r.toc
 Pi feed, see pi/README.md      )
 Pi feed, see pi/README.md      + "</div></nav>\n"
 Pi feed, see pi/README.md  )

 Pi feed, see pi/README.md  out = HEAD.replace("__BUILD__", build_id()) + nav + '<main class="max-w-6xl mx-auto px-6 pb-6 space-y-10">\n' + "\n".join(rendered) + "\n</main>" + FOOT.replace("__BUILD__", build_id()).replace("__LIVE_STATUS_URL__", LIVE_STATUS_URL)
 Pi feed, see pi/README.md  DST.parent.mkdir(parents=True, exist_ok=True)
 Pi feed, see pi/README.md  DST.write_text(out)
 Pi feed, see pi/README.md  print(f"wrote {DST} ({len(out):,} bytes, {len(r.toc)} sections)")


if __name__ == "__main__":
 Pi feed, see pi/README.md  convert_to_html()
