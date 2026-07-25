import React, { useState, useEffect, useMemo } from "react";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";
import {
  Home, BarChart3, Music2, Users, Radio, Settings, Search, Bell,
  TrendingUp, TrendingDown, Play, MoreHorizontal, Sparkles,
} from "lucide-react";

// ---- Aurora Analytics — dashboard for an independent artist tracking their
// listener growth across streaming platforms. Aurora ribbons double as the
// audio waveform motif: the top-track "now playing" bar literally is an
// aurora ribbon. ----

const streamData = [
  { day: "Mon", streams: 12400, saves: 620 },
  { day: "Tue", streams: 13100, saves: 700 },
  { day: "Wed", streams: 15800, saves: 910 },
  { day: "Thu", streams: 14200, saves: 830 },
  { day: "Fri", streams: 19600, saves: 1240 },
  { day: "Sat", streams: 24300, saves: 1680 },
  { day: "Sun", streams: 21100, saves: 1450 },
];

const topTracks = [
  { name: "Nightbloom", plays: "1.2M", change: "+18%", up: true, color: "#00FFAA" },
  { name: "Static Halo", plays: "884K", change: "+6%", up: true, color: "#00E5FF" },
  { name: "Low Tide", plays: "612K", change: "-3%", up: false, color: "#7B2FBE" },
  { name: "Glass Fields", plays: "401K", change: "+11%", up: true, color: "#FF0080" },
];

const navItems = [
  { icon: Home, label: "Overview", active: true },
  { icon: BarChart3, label: "Analytics" },
  { icon: Music2, label: "Catalog" },
  { icon: Users, label: "Audience" },
  { icon: Radio, label: "Live" },
];

function AuroraBackground() {
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", zIndex: 0 }}>
      <div className="aurora-blob b1" />
      <div className="aurora-blob b2" />
      <div className="aurora-blob b3" />
      <div className="grain" />
    </div>
  );
}

function StatCard({ label, value, delta, up, accent }) {
  return (
    <div className="card stat-card" style={{ "--accent": accent }}>
      <div className="stat-top">
        <span className="stat-label">{label}</span>
        <span className={`stat-delta ${up ? "up" : "down"}`}>
          {up ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
          {delta}
        </span>
      </div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="tooltip">
      <div className="tooltip-label">{label}</div>
      <div className="tooltip-value">{payload[0].value.toLocaleString()} streams</div>
    </div>
  );
}

export default function AuroraDashboard() {
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setLoaded(true), 60);
    return () => clearTimeout(t);
  }, []);

  const totalStreams = useMemo(
    () => streamData.reduce((s, d) => s + d.streams, 0).toLocaleString(),
    []
  );

  return (
    <div className={`shell ${loaded ? "loaded" : ""}`}>
      <style>{css}</style>
      <AuroraBackground />

      <div className="layout">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="brand">
            <Sparkles size={18} className="brand-icon" />
            <span>Nocturne</span>
          </div>
          <nav>
            {navItems.map((item) => (
              <button key={item.label} className={`nav-item ${item.active ? "active" : ""}`}>
                <item.icon size={17} />
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
          <div className="sidebar-footer">
            <button className="nav-item">
              <Settings size={17} />
              <span>Settings</span>
            </button>
          </div>
        </aside>

        {/* Main */}
        <main className="main">
          <header className="topbar">
            <div>
              <h1>Overview</h1>
              <p className="sub">Your week in listeners, at a glance</p>
            </div>
            <div className="topbar-actions">
              <div className="search">
                <Search size={15} />
                <span>Search tracks, cities…</span>
              </div>
              <button className="icon-btn"><Bell size={16} /></button>
              <div className="avatar">JR</div>
            </div>
          </header>

          {/* Signature: now-playing aurora waveform ribbon */}
          <section className="card now-playing">
            <div className="np-left">
              <button className="play-btn"><Play size={16} fill="currentColor" /></button>
              <div>
                <div className="np-title">Nightbloom</div>
                <div className="np-sub">Now trending — 340 new listeners this hour</div>
              </div>
            </div>
            <svg className="ribbon" viewBox="0 0 600 60" preserveAspectRatio="none">
              <defs>
                <linearGradient id="ribbonGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#00FFAA" />
                  <stop offset="35%" stopColor="#00E5FF" />
                  <stop offset="65%" stopColor="#7B2FBE" />
                  <stop offset="100%" stopColor="#FF0080" />
                </linearGradient>
              </defs>
              <path
                className="ribbon-path"
                d="M0,30 C40,10 80,50 120,30 C160,10 200,50 240,30 C280,10 320,50 360,30 C400,10 440,50 480,30 C520,10 560,50 600,30"
                fill="none"
                stroke="url(#ribbonGrad)"
                strokeWidth="3"
                strokeLinecap="round"
              />
            </svg>
          </section>

          <section className="stat-row">
            <StatCard label="Total streams" value={totalStreams} delta="+14.2%" up accent="#00FFAA" />
            <StatCard label="New followers" value="8,204" delta="+9.1%" up accent="#00E5FF" />
            <StatCard label="Saves" value="7,430" delta="+21.6%" up accent="#7B2FBE" />
            <StatCard label="Skip rate" value="18.3%" delta="-2.4%" up={false} accent="#FF0080" />
          </section>

          <section className="grid-2">
            <div className="card chart-card">
              <div className="card-head">
                <h2>Streams this week</h2>
                <span className="pill">Last 7 days</span>
              </div>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height={220}>
                  <AreaChart data={streamData} margin={{ top: 10, right: 8, left: -18, bottom: 0 }}>
                    <defs>
                      <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#00E5FF" stopOpacity={0.45} />
                        <stop offset="100%" stopColor="#00E5FF" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                    <XAxis dataKey="day" stroke="rgba(255,255,255,0.4)" tickLine={false} axisLine={false} fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.4)" tickLine={false} axisLine={false} fontSize={12} width={40} />
                    <Tooltip content={<CustomTooltip />} />
                    <Area type="monotone" dataKey="streams" stroke="#00E5FF" strokeWidth={2.5} fill="url(#areaFill)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="card tracks-card">
              <div className="card-head">
                <h2>Top tracks</h2>
                <button className="icon-btn small"><MoreHorizontal size={15} /></button>
              </div>
              <ul className="track-list">
                {topTracks.map((t) => (
                  <li key={t.name} className="track-row">
                    <span className="track-dot" style={{ background: t.color }} />
                    <span className="track-name">{t.name}</span>
                    <span className="track-plays">{t.plays}</span>
                    <span className={`track-change ${t.up ? "up" : "down"}`}>{t.change}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

const css = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

.shell {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: #0A0A2E;
  font-family: 'Inter', -apple-system, sans-serif;
  color: #EDEFFF;
  overflow: hidden;
  opacity: 0;
  transition: opacity 0.6s ease;
}
.shell.loaded { opacity: 1; }

.aurora-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.35;
  animation: drift 22s ease-in-out infinite;
}
.b1 { width: 480px; height: 480px; background: #00FFAA; top: -160px; left: -100px; animation-delay: 0s; }
.b2 { width: 520px; height: 520px; background: #7B2FBE; top: 20%; right: -180px; animation-delay: -7s; }
.b3 { width: 420px; height: 420px; background: #0066FF; bottom: -180px; left: 30%; animation-delay: -14s; }

@keyframes drift {
  0%, 100% { transform: translate(0,0) scale(1); }
  50% { transform: translate(40px, -30px) scale(1.08); }
}

.grain {
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
}

.layout {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 100vh;
}

.sidebar {
  padding: 28px 16px;
  border-right: 1px solid rgba(255,255,255,0.07);
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.brand {
  display: flex; align-items: center; gap: 8px;
  padding: 0 10px;
  font-weight: 500; font-size: 15px; letter-spacing: 0.02em;
}
.brand-icon { color: #00FFAA; filter: drop-shadow(0 0 6px rgba(0,255,170,0.6)); }

nav { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.nav-item {
  display: flex; align-items: center; gap: 11px;
  background: none; border: none; color: rgba(237,239,255,0.55);
  padding: 10px 12px; border-radius: 10px;
  font-family: inherit; font-size: 13.5px; font-weight: 400;
  cursor: pointer; text-align: left;
  transition: background 0.2s, color 0.2s;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: #EDEFFF; }
.nav-item.active {
  background: linear-gradient(90deg, rgba(0,255,170,0.14), rgba(0,229,255,0.05));
  color: #00FFAA;
  box-shadow: inset 1px 0 0 #00FFAA;
}
.sidebar-footer { border-top: 1px solid rgba(255,255,255,0.07); padding-top: 12px; }

.main { padding: 32px 40px 60px; min-width: 0; }

.topbar {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 24px; flex-wrap: wrap; gap: 16px;
}
.topbar h1 { font-size: 22px; font-weight: 500; margin: 0 0 4px; letter-spacing: -0.01em; }
.sub { margin: 0; font-size: 13px; color: rgba(237,239,255,0.5); font-weight: 300; }
.topbar-actions { display: flex; align-items: center; gap: 10px; }

.search {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 8px 14px; border-radius: 20px;
  font-size: 12.5px; color: rgba(237,239,255,0.45);
  min-width: 200px;
}
.icon-btn {
  width: 34px; height: 34px; border-radius: 50%;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
  color: rgba(237,239,255,0.7); display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}
.icon-btn.small { width: 28px; height: 28px; }
.avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(135deg, #00FFAA, #7B2FBE);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 600; color: #0A0A2E;
}

.card {
  background: linear-gradient(160deg, rgba(255,255,255,0.055), rgba(255,255,255,0.015));
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 18px;
  padding: 20px 22px;
  position: relative;
}

.now-playing {
  display: flex; align-items: center; justify-content: space-between;
  gap: 24px; margin-bottom: 20px; flex-wrap: wrap;
  border-image: none;
}
.now-playing::before {
  content: ""; position: absolute; inset: 0; border-radius: 18px; padding: 1px;
  background: linear-gradient(120deg, #00FFAA, #00E5FF, #7B2FBE, #FF0080);
  opacity: 0.35; -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}
.np-left { display: flex; align-items: center; gap: 14px; }
.play-btn {
  width: 42px; height: 42px; border-radius: 50%; border: none; cursor: pointer;
  background: linear-gradient(135deg, #00FFAA, #00E5FF);
  color: #0A0A2E; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 20px rgba(0,255,170,0.35);
}
.np-title { font-size: 15px; font-weight: 500; }
.np-sub { font-size: 12px; color: rgba(237,239,255,0.5); font-weight: 300; margin-top: 2px; }
.ribbon { width: 260px; height: 44px; flex-shrink: 0; }
.ribbon-path { stroke-dasharray: 6 1000; animation: flow 5s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -1000; } }

.stat-row {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px;
}
.stat-card { transition: transform 0.2s, box-shadow 0.2s; }
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 0 1px var(--accent, #00FFAA) inset, 0 8px 24px -8px rgba(0,0,0,0.5);
}
.stat-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.stat-label { font-size: 12px; color: rgba(237,239,255,0.5); font-weight: 400; }
.stat-delta { display: flex; align-items: center; gap: 3px; font-size: 11.5px; font-weight: 500; }
.stat-delta.up { color: #00FFAA; }
.stat-delta.down { color: #FF0080; }
.stat-value { font-size: 25px; font-weight: 500; letter-spacing: -0.01em; }

.grid-2 { display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; }

.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.card-head h2 { font-size: 14.5px; font-weight: 500; margin: 0; }
.pill {
  font-size: 11px; padding: 4px 10px; border-radius: 20px;
  background: rgba(0,229,255,0.1); color: #00E5FF; font-weight: 500;
}

.chart-wrap { margin: 0 -6px; }
.tooltip {
  background: #12123a; border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px; padding: 8px 12px; font-size: 12px;
}
.tooltip-label { color: rgba(237,239,255,0.5); margin-bottom: 2px; font-size: 11px; }
.tooltip-value { font-weight: 500; }

.track-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
.track-row {
  display: grid; grid-template-columns: 8px 1fr auto auto; align-items: center; gap: 12px;
  padding: 10px 8px; border-radius: 10px; transition: background 0.2s;
}
.track-row:hover { background: rgba(255,255,255,0.04); }
.track-dot { width: 8px; height: 8px; border-radius: 50%; }
.track-name { font-size: 13px; font-weight: 400; }
.track-plays { font-size: 12.5px; color: rgba(237,239,255,0.5); font-variant-numeric: tabular-nums; }
.track-change { font-size: 12px; font-weight: 500; font-variant-numeric: tabular-nums; }
.track-change.up { color: #00FFAA; }
.track-change.down { color: #FF0080; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .grid-2 { grid-template-columns: 1fr; }
  .stat-row { grid-template-columns: repeat(2, 1fr); }
  .main { padding: 24px 18px 40px; }
}

@media (prefers-reduced-motion: reduce) {
  .aurora-blob, .ribbon-path { animation: none; }
}
`;
