"""Generate the AI coding stages SVG.

Usage: python3 gen_ai_stages.py [ai-coding-stages.svg]
"""
import os, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ai-coding-stages.svg")

W, H = 2000, 1010
C = {
    "bg": "#fbfaf7", "ink": "#1f2328", "muted": "#5f6672", "grid": "#e4dfd4", "card": "#ffffff",
    "tool": "#4b5563", "claude": "#c15f3c", "me": "#2f3fb0",
}

# (color, when, title, tools, [(row label, lines)])
STAGES = [
    ("tool", "Oct 2024 · first PRs", "Inline completion", "GitHub Copilot", [
        ("I describe", ["Nothing. I find the module and", "function, then start typing"]),
        ("AI does", ["Completes the current", "word or line"]),
        ("I still own", ["Reading every module end to end,", "most of the code, unit tests,", "design patterns and interfaces"]),
    ]),
    ("tool", "Up to early 2026", "Multi-file editing", "Copilot multi-line & edits · Cursor", [
        ("I describe", ["Which files and functions", "to change, and how"]),
        ("AI does", ["Multi-line suggestions and", "edits across several files"]),
        ("I still own", ["Locating the change in the", "codebase, reviewing every edit"]),
    ]),
    ("claude", "Apr 2026 → now", "Agent collaboration", "Claude Code · Opus 5.5 / Fable", [
        ("I describe", ["Intent in the right domain: control", "vs data plane, module boundaries,", "rough control flow"]),
        ("AI does", ["70-80% of a feature end to end,", "dependency / rebase conflicts,", "fixing CI"]),
        ("I still own", ["Judgment: architecture, interface", "design, reviewing large features"]),
    ]),
]

out = []
a = out.append
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang TC', sans-serif"
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
a(f"""<style>
 text {{ fill: {C['ink']}; }}
 .h1 {{ font-size: 40px; font-weight: 750; }}
 .h2 {{ font-size: 22px; fill: {C['muted']}; }}
 .when {{ font-size: 21px; font-weight: 600; fill: #ffffff; }}
 .title {{ font-size: 34px; font-weight: 750; }}
 .tools {{ font-size: 21px; fill: {C['muted']}; }}
 .row {{ font-size: 18px; font-weight: 700; letter-spacing: 1.5px; }}
 .body {{ font-size: 23px; }}
 .axis {{ font-size: 22px; font-weight: 650; }}
 .tick {{ font-size: 21px; fill: {C['muted']}; }}
</style>""")
a(f'<rect width="{W}" height="{H}" rx="18" fill="{C["bg"]}"/>')
a('<text x="70" y="60" class="h1">How I work with AI coding tools, stage by stage</text>')
a('<text x="70" y="96" class="h2">What I tell the AI keeps moving up a level, while judgment stays with me</text>')

CW, GAP, X0, Y0, CH = 590, 45, 70, 140, 715
ROW_Y = [215, 395, 560]
for i, (k, when, title, tools, rows) in enumerate(STAGES):
    x = X0 + i * (CW + GAP)
    a(f'<rect x="{x}" y="{Y0}" width="{CW}" height="{CH}" rx="16" fill="{C["card"]}" stroke="{C[k]}" stroke-width="{3.5 if k == "claude" else 2}"/>')
    pw = 22 + 11.5 * len(when)
    a(f'<rect x="{x+30}" y="{Y0+36}" width="{pw:.0f}" height="38" rx="19" fill="{C[k]}"/>')
    a(f'<text x="{x+30+pw/2:.0f}" y="{Y0+62}" text-anchor="middle" class="when">{escape(when)}</text>')
    a(f'<text x="{x+30}" y="{Y0+122}" class="title">{i+1}. {escape(title)}</text>')
    a(f'<text x="{x+30}" y="{Y0+156}" class="tools">{escape(tools)}</text>')
    for (label, lines), ry in zip(rows, ROW_Y):
        y = Y0 + ry
        a(f'<line x1="{x+30}" y1="{y-8}" x2="{x+CW-30}" y2="{y-8}" stroke="{C["grid"]}" stroke-width="1.5"/>')
        color = C["me"] if label != "AI does" else C[k]
        a(f'<text x="{x+30}" y="{y+28}" class="row" fill="{color}" style="fill:{color}">{label.upper()}</text>')
        for j, line in enumerate(lines):
            a(f'<text x="{x+30}" y="{y+66+j*33}" class="body">{escape(line)}</text>')
    if i < len(STAGES) - 1:
        ax = x + CW + 6
        a(f'<path d="M{ax},{Y0+CH/2-16} L{ax+32},{Y0+CH/2} L{ax},{Y0+CH/2+16} Z" fill="{C["muted"]}"/>')

# bottom axis: level of what I describe
ay = Y0 + CH + 75
a(f'<line x1="{X0}" y1="{ay}" x2="{W-70}" y2="{ay}" stroke="{C["ink"]}" stroke-width="3"/>')
a(f'<path d="M{W-70},{ay-10} L{W-48},{ay} L{W-70},{ay+10} Z" fill="{C["ink"]}"/>')
a(f'<text x="{X0}" y="{ay-18}" class="axis">Level of what I tell the AI</text>')
for i, t in enumerate(["line", "file & function", "intent & boundaries"]):
    cx = X0 + i * (CW + GAP) + CW / 2
    a(f'<circle cx="{cx:.0f}" cy="{ay}" r="8" fill="{C[STAGES[i][0]]}"/>')
    a(f'<text x="{cx:.0f}" y="{ay+38}" text-anchor="middle" class="tick">{escape(t)}</text>')

a("</svg>")
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
