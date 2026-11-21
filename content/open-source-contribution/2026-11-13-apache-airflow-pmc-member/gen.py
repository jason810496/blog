"""Generate the Airflow x AI timeline SVG.

Usage: python3 gen.py [prs.json] [airflow-ai-timeline.svg]
Refresh the data first with: python3 fetch.py
"""
import json, os, sys, datetime as dt
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "prs.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "airflow-ai-timeline.svg")

prs = json.load(open(SRC))
D = lambda s: dt.date.fromisoformat(s[:10])
fmt = lambda d: d.strftime("%Y-%m-%d")

W, H, MID = 2000, 960, 580
# compressed zone (before contributing) and linear zone
C0, C1, CX0, CX1 = D("2021-01-01"), D("2024-09-15"), 70, 600
L0, L1, LX0, LX1 = D("2024-10-01"), D("2026-12-01"), 650, 1950

FIRST_PR, COMMITTER, ASTRONOMER, PMC = D("2024-10-10"), D("2025-03-14"), D("2026-03-02"), D("2026-11-13")


def x(d):
    if d < L0:
        return CX0 + (d - C0).days / (C1 - C0).days * (CX1 - CX0)
    return LX0 + (d - L0).days / (L1 - L0).days * (LX1 - LX0)


merged = sorted(D(r["merged"]) for r in prs["authored"] if r["merged"])
reviewed = [D(t) for t in prs["reviewed"]]
count_by = lambda dates, day: sum(1 for d in dates if d <= day)

C = {
    "bg": "#fbfaf7", "ink": "#1f2328", "muted": "#5f6672", "grid": "#e4dfd4",
    "release": "#0f8a83", "me": "#d4572a", "authored": "#2f3fb0", "reviewed": "#6d5bd0",
    "claude": "#c15f3c", "tool": "#4b5563",
}

# ---- top: lanes (height above the midline) ----
LANES = [
    ("release", 75, "Airflow releases"),
    ("authored", 165, "Merged PRs"),
    ("reviewed", 255, "Reviewed PRs"),
    ("me", 355, "Milestones"),
]
LANE_H = {k: h for k, h, _ in LANES}

# (lane, date, label, lines-below-label)
top = []
for v, d in [("3.0", "2025-04-22"), ("3.1", "2025-09-25"), ("3.2", "2026-04-07"),
             ("3.3", "2026-07-06"), ("3.4", "2026-11-06")]:
    top.append(("release", D(d), f"Airflow {v}", [fmt(D(d))]))
for n in (100, 200, 300, 400):
    d = merged[n - 1]
    top.append(("authored", d, f"{n}", [d.strftime("%b '%y")]))
for n in (100, 250, 500, 750, 1000, 1250):
    d = reviewed[n - 1]
    top.append(("reviewed", d, f"{n:,}", [d.strftime("%b '%y")]))
top += [
    ("me", FIRST_PR, "First PR (#42902)", [fmt(FIRST_PR)]),
    ("me", COMMITTER, "Airflow Committer",
     [fmt(COMMITTER), f"{count_by(merged, COMMITTER)} merged · {count_by(reviewed, COMMITTER)} reviewed PRs"]),
    ("me", ASTRONOMER, "Joined Astronomer", [fmt(ASTRONOMER)]),
    ("me", PMC, "Airflow PMC Member", [fmt(PMC)]),
]

# ---- bottom: AI tooling (depth below the midline alternates) ----
bottom = [
    ("tool", "2021-06-29", "Copilot preview", "word / line suggestions"),
    ("tool", "2022-06-21", "Copilot GA", "multi-line completions"),
    ("tool", "2023-03-14", "Cursor", "AI-native editor"),
    ("claude", "2024-06-20", "Claude 3.5 Sonnet", "first strong coding model"),
    ("tool", "2024-10-29", "Copilot Edits", "multi-file editing"),
    ("claude", "2025-02-24", "Claude Code preview", "+ Claude 3.7 Sonnet"),
    ("claude", "2025-05-22", "Claude Code GA", "+ Claude Opus 4"),
    ("claude", "2026-06-09", "Claude Fable 5", "Mythos-class model"),
    ("claude", "2026-09-22", "Claude Opus 5.5", ""),
]
DEPTHS = [80, 195]

out = []
a = out.append
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang TC', sans-serif"
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
a(f"""<style>
 text {{ fill: {C['ink']}; }}
 .halo {{ paint-order: stroke; stroke: {C['bg']}; stroke-width: 7px; stroke-linejoin: round; }}
 .lbl {{ font-size: 24px; font-weight: 650; }}
 .big {{ font-size: 28px; font-weight: 700; }}
 .num {{ font-size: 24px; font-weight: 700; }}
 .date {{ font-size: 19px; fill: {C['muted']}; }}
 .pdate {{ font-size: 16.5px; fill: {C['muted']}; }}
 .stat {{ font-size: 19px; font-weight: 600; fill: {C['me']}; }}
 .sub {{ font-size: 19px; fill: {C['muted']}; font-style: italic; }}
 .lane {{ font-size: 22px; font-weight: 650; }}
 .tick {{ font-size: 19px; fill: {C['muted']}; }}
 .year {{ font-size: 21px; font-weight: 700; }}
 .h1 {{ font-size: 40px; font-weight: 750; }}
 .h2 {{ font-size: 22px; fill: {C['muted']}; }}
</style>""")
a(f'<rect width="{W}" height="{H}" rx="18" fill="{C["bg"]}"/>')

a(f'<text x="40" y="60" class="h1">Growing with Apache Airflow, alongside AI coding tools</text>')
a(f'<text x="40" y="96" class="h2">Top: Airflow releases &amp; my contributions to apache/airflow · Bottom: the evolution of AI coding tools</text>')

# contributor / committer span shading on the top half
top_y = MID - 450
cx, px = x(COMMITTER), x(PMC)
a(f'<rect x="{x(L0):.1f}" y="{top_y}" width="{cx-x(L0):.1f}" height="{MID-top_y}" fill="{C["release"]}" opacity="0.035"/>')
a(f'<rect x="{cx:.1f}" y="{top_y}" width="{px-cx:.1f}" height="{MID-top_y}" fill="{C["me"]}" opacity="0.05"/>')

# lane guides + lane names (left; the compressed zone has no top events)
for k, h, name in LANES:
    y = MID - h
    a(f'<line x1="{LX0-20}" y1="{y}" x2="{LX1}" y2="{y}" stroke="{C["grid"]}" stroke-width="1.5" stroke-dasharray="2 6"/>')
    a(f'<circle cx="50" cy="{y}" r="8" fill="{C[k]}"/>')
    a(f'<text x="68" y="{y+8}" class="lane">{name}</text>')

# top events: stems first so label halos cover crossing stems
for k, d, *_ in top:
    X, y = x(d), MID - LANE_H[k]
    a(f'<line x1="{X:.1f}" y1="{MID}" x2="{X:.1f}" y2="{y}" stroke="{C[k]}" stroke-width="{3 if k=="me" else 2}" opacity="{0.9 if k in ("me","release") else 0.55}"/>')
for k, d, label, lines in top:
    X, y = x(d), MID - LANE_H[k]
    a(f'<circle cx="{X:.1f}" cy="{y}" r="{11 if k == "me" else 7.5}" fill="{C[k]}" stroke="{C["bg"]}" stroke-width="2.5"/>')
    anchor, tx = "middle", X
    if X > W - 160:
        anchor, tx = "end", X + 14
    cls = {"me": "big", "authored": "num", "reviewed": "num"}.get(k, "lbl")
    ly = y - 20
    for i, line in enumerate(reversed(lines)):
        c = "stat" if (k == "me" and i == 0 and len(lines) > 1) else ("pdate" if k in ("authored", "reviewed") else "date")
        a(f'<text x="{tx:.1f}" y="{ly}" text-anchor="{anchor}" class="{c} halo">{escape(line)}</text>')
        ly -= 25
    a(f'<text x="{tx:.1f}" y="{ly-3}" text-anchor="{anchor}" class="{cls} halo">{escape(label)}</text>')

# bottom events
for i, (k, d, *_ ) in enumerate(bottom):
    X, y = x(D(d)), MID + DEPTHS[i % 2]
    a(f'<line x1="{X:.1f}" y1="{MID}" x2="{X:.1f}" y2="{y}" stroke="{C[k]}" stroke-width="2.2" opacity="0.8"/>')
for i, (k, d, label, sub) in enumerate(bottom):
    d = D(d)
    X, y = x(d), MID + DEPTHS[i % 2]
    a(f'<circle cx="{X:.1f}" cy="{y}" r="9" fill="{C[k]}" stroke="{C["bg"]}" stroke-width="2.5"/>')
    a(f'<text x="{X:.1f}" y="{y+36}" text-anchor="middle" class="lbl halo">{escape(label)}</text>')
    a(f'<text x="{X:.1f}" y="{y+60}" text-anchor="middle" class="date halo">{fmt(d)}</text>')
    if sub:
        a(f'<text x="{X:.1f}" y="{y+84}" text-anchor="middle" class="sub halo">{escape(sub)}</text>')

# footer: note + legend
a(f'<text x="40" y="{H-30}" class="tick">apache/airflow only · merged by merge date, reviewed by first review date · data as of {dt.date.today()}</text>')
lx = LX1 - 400
for i, (k, name) in enumerate([("claude", "Anthropic Claude"), ("tool", "Other AI coding tools")]):
    a(f'<circle cx="{lx + i*190}" cy="{H-37}" r="8" fill="{C[k]}"/>')
    a(f'<text x="{lx + i*190 + 16}" y="{H-30}" class="tick">{name}</text>')

# midline axis (drawn last so it sits on top of stems)
a(f'<line x1="40" y1="{MID}" x2="{CX1+12}" y2="{MID}" stroke="{C["ink"]}" stroke-width="2.5" stroke-dasharray="7 6"/>')
a(f'<line x1="{LX0-12}" y1="{MID}" x2="{LX1+20}" y2="{MID}" stroke="{C["ink"]}" stroke-width="3.5"/>')
a(f'<path d="M{LX1+20},{MID-9} L{LX1+38},{MID} L{LX1+20},{MID+9} Z" fill="{C["ink"]}"/>')
bx = (CX1 + LX0) / 2
for off in (-7, 7):
    a(f'<line x1="{bx+off-7}" y1="{MID+14}" x2="{bx+off+7}" y2="{MID-14}" stroke="{C["ink"]}" stroke-width="2.5"/>')
a(f'<text x="{(CX0+CX1)/2}" y="{MID-44}" text-anchor="middle" class="tick">(compressed scale)</text>')

for yr in (2021, 2022, 2023, 2024):
    X = x(D(f"{yr}-01-01"))
    a(f'<line x1="{X:.1f}" y1="{MID-7}" x2="{X:.1f}" y2="{MID+7}" stroke="{C["ink"]}" stroke-width="2.5"/>')
    a(f'<text x="{X+6:.1f}" y="{MID-14}" class="year halo">{yr}</text>')
d = L0
while d < L1:
    X = x(d)
    if d.month == 1:
        a(f'<line x1="{X:.1f}" y1="{MID-10}" x2="{X:.1f}" y2="{MID+10}" stroke="{C["ink"]}" stroke-width="3"/>')
        a(f'<text x="{X+7:.1f}" y="{MID-14}" class="year halo">{d.year}</text>')
    elif d.month in (4, 7, 10):
        a(f'<line x1="{X:.1f}" y1="{MID-6}" x2="{X:.1f}" y2="{MID+6}" stroke="{C["ink"]}" stroke-width="2"/>')
        lab = d.strftime("%b") + (f" {d.year}" if d == L0 else "")
        a(f'<text x="{X+6:.1f}" y="{MID+27}" class="tick halo">{lab}</text>')
    d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)

a("</svg>")
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
