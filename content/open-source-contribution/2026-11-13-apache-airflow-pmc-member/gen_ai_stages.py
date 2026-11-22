"""Generate the AI coding stages SVG.

Usage: python3 gen_ai_stages.py [ai-coding-stages.svg]
"""
import os, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ai-coding-stages.svg")

W, H = 2000, 640
PW, GAP, X0, Y0, PH = 600, 50, 50, 120, 470
C = {
    "bg": "#fbfaf7", "ink": "#1f2328", "muted": "#5f6672", "line": "#d9d4c9",
    "editor": "#ffffff", "bar": "#f1eee7", "code": "#24292f", "kw": "#8250df", "str": "#0a7f55",
    "ghost": "#a3a9b3", "add": "#1a7f37", "del": "#cf222e",
    "term": "#1f2328", "tterm": "#e6e6e6", "tmuted": "#8b949e", "claude": "#d97757", "ok": "#3fb950",
    "tool": "#4b5563",
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
LH = 31

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{SANS}">')
a(f"""<style>
 .label {{ font-size: 26px; font-weight: 700; fill: {C['ink']}; }}
 .sub {{ font-size: 20px; fill: {C['muted']}; }}
 .mono {{ font-family: {MONO}; font-size: 19px; white-space: pre; }}
 .tab {{ font-size: 17px; fill: {C['muted']}; }}
 .tabon {{ font-size: 17px; fill: {C['ink']}; font-weight: 600; }}
</style>""")
a(f'<rect width="{W}" height="{H}" rx="18" fill="{C["bg"]}"/>')


def window(x, dark=False, title=""):
    fill = C["term"] if dark else C["editor"]
    bar = "#2d333b" if dark else C["bar"]
    a(f'<rect x="{x}" y="{Y0}" width="{PW}" height="{PH}" rx="14" fill="{fill}" stroke="{C["line"] if not dark else C["term"]}" stroke-width="2"/>')
    a(f'<path d="M{x},{Y0+46} V{Y0+14} a14,14 0 0 1 14,-14 H{x+PW-14} a14,14 0 0 1 14,14 V{Y0+46} Z" fill="{bar}"/>')
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        a(f'<circle cx="{x+26+i*22}" cy="{Y0+23}" r="7" fill="{col}"/>')
    if title:
        a(f'<text x="{x+PW/2}" y="{Y0+29}" text-anchor="middle" class="tab" style="fill:{C["tmuted"] if dark else C["muted"]}">{escape(title)}</text>')


def code(x, y, parts):
    """parts: list of (text, color)."""
    spans = "".join(f'<tspan fill="{C[c]}">{escape(t)}</tspan>' for t, c in parts)
    a(f'<text x="{x}" y="{y}" class="mono" xml:space="preserve">{spans}</text>')


def gutter(x, y, n, color="ghost"):
    a(f'<text x="{x}" y="{y}" class="mono" fill="{C[color]}" text-anchor="end">{n}</text>')


def caption(x, num, title, sub):
    a(f'<text x="{x}" y="{Y0-52}" class="label">{num}  {escape(title)}</text>')
    a(f'<text x="{x}" y="{Y0-20}" class="sub">{escape(sub)}</text>')


# ---- 1. inline suggestion ----
x = X0
caption(x, "1", "Inline suggestion", "GitHub Copilot")
window(x, title="dags.py")
cx, cy = x + 62, Y0 + 100
lines = [
    [('@router.get(', "code"), ('"/dags/{dag_id}"', "str"), (")", "code")],
    [("def ", "kw"), ("get_dag(dag_id: str, session):", "code")],
    [("    dag = session.get(DagModel, dag_id)", "code")],
    [("    if ", "kw"), ("dag ", "code"), ("is None", "kw"), (":", "code")],
    [("        raise ", "kw"), ("HTTPException(", "code"), ('404, "Not found")', "ghost")],
    [("    return ", "kw"), ("dag", "code")],
]
for i, parts in enumerate(lines):
    gutter(x + 40, cy + i * LH, i + 1)
    code(cx, cy + i * LH, parts)
# cursor and Tab hint on the suggestion line
ly = cy + 4 * LH
cur = cx + len("        raise HTTPException(") * 11.45
a(f'<rect x="{cur:.0f}" y="{ly-20}" width="2.5" height="25" fill="{C["ink"]}"/>')
a(f'<rect x="{x+30}" y="{ly-24}" width="{PW-60}" height="33" rx="4" fill="#0969da" opacity="0.06"/>')
by = Y0 + PH - 64
a(f'<rect x="{x+PW/2-90}" y="{by}" width="64" height="38" rx="7" fill="{C["bar"]}" stroke="{C["line"]}" stroke-width="2"/>')
a(f'<text x="{x+PW/2-58}" y="{by+26}" text-anchor="middle" style="font-size:19px;font-weight:600;fill:{C["ink"]}">Tab</text>')
a(f'<text x="{x+PW/2-14}" y="{by+26}" class="sub">to accept</text>')

# ---- 2. multi-line / multi-file ----
x = X0 + PW + GAP
caption(x, "2", "Multi-line, multi-file", "Copilot Edits · Cursor")
window(x)
tabs = [("dags.py", True), ("models.py", False), ("test_dags.py", False)]
tx = x + 100
for name, on in tabs:
    w = 34 + len(name) * 9.6
    a(f'<rect x="{tx}" y="{Y0+8}" width="{w:.0f}" height="38" rx="6" fill="{C["editor"] if on else C["bar"]}"/>')
    a(f'<text x="{tx+w/2:.0f}" y="{Y0+33}" text-anchor="middle" class="{"tabon" if on else "tab"}">{name}</text>')
    a(f'<circle cx="{tx+w-9:.0f}" cy="{Y0+16}" r="4" fill="{C["add"]}"/>')
    tx += w + 6
cy = Y0 + 100
lines2 = [
    [("@router.delete(", "code"), ('"/dags/{dag_id}"', "str"), (")", "code")],
    [("def ", "kw"), ("delete_dag(dag_id: str, session):", "code")],
    [("    dag = session.get(DagModel, dag_id)", "ghost")],
    [("    if dag is None:", "ghost")],
    [('        raise HTTPException(404, "Not found")', "ghost")],
    [("    session.delete(dag)", "ghost")],
]
for i, parts in enumerate(lines2):
    gutter(x + 40, cy + i * LH, i + 1)
    code(x + 62, cy + i * LH, parts)
a(f'<rect x="{x+50}" y="{cy+2*LH-24}" width="4" height="{4*LH}" fill="{C["add"]}"/>')
# changed files strip
fy = Y0 + PH - 105
a(f'<line x1="{x+30}" y1="{fy-20}" x2="{x+PW-30}" y2="{fy-20}" stroke="{C["line"]}" stroke-width="1.5"/>')
for i, (name, add, dele) in enumerate([("dags.py", "+18", "-2"), ("models.py", "+6", "-1"), ("test_dags.py", "+42", "")]):
    yy = fy + 10 + i * 30
    a(f'<text x="{x+40}" y="{yy}" class="mono" style="font-size:17px" fill="{C["code"]}">{name}</text>')
    a(f'<text x="{x+260}" y="{yy}" class="mono" style="font-size:17px" fill="{C["add"]}">{add}</text>')
    if dele:
        a(f'<text x="{x+320}" y="{yy}" class="mono" style="font-size:17px" fill="{C["del"]}">{dele}</text>')

# ---- 3. agent ----
x = X0 + 2 * (PW + GAP)
caption(x, "3", "Agent", "Claude Code · Opus 5.5 / Fable")
window(x, dark=True, title="claude")
cy = Y0 + 92
term = [
    [("> ", "claude"), ("Run Go tasks through the coordinator", "tterm")],
    [("  so they work on any executor", "tterm")],
    [],
    [("● ", "claude"), ("Read ", "tterm"), ("task-sdk/coordinators/", "tmuted")],
    [("● ", "claude"), ("Update ", "tterm"), ("go-sdk/worker.go ", "tmuted"), ("+148 ", "ok"), ("-36", "del")],
    [("● ", "claude"), ("Update ", "tterm"), ("5 more files", "tmuted")],
    [("● ", "claude"), ("Bash ", "tterm"), ("go test ./... ", "tmuted"), ("✓ passed", "ok")],
    [("● ", "claude"), ("Fix ", "tterm"), ("CI lint and rebase conflict", "tmuted")],
    [("✻ ", "claude"), ("Ready for review", "tterm")],
]
for i, parts in enumerate(term):
    if parts:
        code(x + 30, cy + i * LH, parts)
py = Y0 + PH - 56
a(f'<rect x="{x+24}" y="{py}" width="{PW-48}" height="40" rx="6" fill="none" stroke="#444c56" stroke-width="1.5"/>')
code(x + 40, py + 27, [("> ", "tmuted")])
a(f'<rect x="{x+64}" y="{py+9}" width="11" height="22" fill="{C["tterm"]}"/>')

# arrows between panels
for i in range(2):
    ax = X0 + (i + 1) * PW + i * GAP + 9
    ay = Y0 + PH / 2
    a(f'<path d="M{ax},{ay-14} L{ax+30},{ay} L{ax},{ay+14} Z" fill="{C["muted"]}"/>')

a("</svg>")
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
