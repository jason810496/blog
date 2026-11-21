"""Donut chart of apache/airflow commit share since 2024-10 by affiliation.

Usage: python3 gen_share.py [share.json] [airflow-contribution-share.svg] [--debug]
Refresh the data first with: python3 fetch_share.py

Every commit lands in exactly one slice, decided per commit in this order:
  1. OVERRIDES (per person, optionally by date range)
  2. public member of the astronomer GitHub org
  3. vendor by any commit-email domain of the person or their GitHub profile company
  4. public member of the opensource4you GitHub org
  5. any other company on the GitHub profile ("Other companies")
  6. everyone else: independent, students, unknown
Bot commits are excluded.
"""
import json, math, os, re, sys
from collections import Counter, defaultdict
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC = args[0] if args else os.path.join(HERE, "share.json")
OUT = args[1] if len(args) > 1 else os.path.join(HERE, "airflow-contribution-share.svg")
data = json.load(open(SRC))

OS4Y = {m.lower() for m in data["org_members"]["opensource4you"]}
ASTRO = {m.lower() for m in data["org_members"]["astronomer"]}

JAREK = "Jarek Potiuk (independent)"
INDEP = "Independent & unaffiliated"
# login -> [(from, until, slice)]; dates are commit dates, from inclusive / until exclusive
OVERRIDES = {
    "eladkal": [(None, "2026-04-01", "AWS"), ("2026-04-01", None, "Astronomer")],  # joined Astronomer Apr 2026
    "potiuk": [(None, None, JAREK)],
}

# (slice, email-domain regex, profile-company regex)
VENDORS = [
    ("Astronomer", r"astronomer\.io$", r"astronomer"),
    ("AWS", r"(^|\.)amazon\.[a-z.]+$|(^|\.)aws\.", r"\bamazon\b|\baws\b"),
    ("Google", r"(^|\.)google\.com$", r"\bgoogle\b|\bgcp\b"),
    ("Other vendors", r"(^|\.)(microsoft|databricks|snowflake|teradata|ibm|cloudera|confluent|"
                      r"getindata|qubole|oracle|salesforce|dbtlabs|redhat)\.",
     r"microsoft|databricks|snowflake|teradata|\bibm\b|cloudera|confluent|getindata|qubole|"
     r"oracle|salesforce|dbt labs|red ?hat"),
]
ORDER = ["Astronomer", "AWS", "Google", "Other vendors", "Other companies", INDEP, JAREK, "opensource4you"]
# categorical hues checked with the dataviz palette validator in pie order (opensource4you wraps
# round to Astronomer); independents share a neutral family: light gray, Jarek darker gray
COLOR = {
    "Astronomer": "#2a78d6", "AWS": "#eda100", "Google": "#1baf7a", "Other vendors": "#6250d6",
    "Other companies": "#e87ba4", INDEP: "#d3d0c7", JAREK: "#8f8b80", "opensource4you": "#eb6834",
}
BOT = re.compile(r"\[bot\]|^dependabot|^github-actions|bot@", re.I)

# profile company -> canonical company name, or None when it is not an employer
NOT_EMPLOYER = re.compile(r"^(apache( software foundation)?|asf|self\b.*|-select-|none|n/?a|freelanc\w*|independent|"
                          r"student|personal|home)$", re.I)
ACADEMIA = re.compile(r"universit|college|institute|school|\biiit\b|\bnyu\b|\bucla\b|\bntust?\b|\bnycu\b|"
                      r"\bncku\b|\bmsis\b|\bcsie\b", re.I)
CANONICAL = [(r"bosch", "Bosch"), (r"datadog", "Datadog"), (r"visa\b", "Visa"), (r"experian", "Experian"),
             (r"qualcomm", "Qualcomm"), (r"samsung", "Samsung"), (r"apple", "Apple"), (r"ncr voyix", "NCR Voyix"),
             (r"mollie", "Mollie"), (r"g-research", "G-Research"), (r"linkedin", "LinkedIn")]
DOMAIN_COMPANY = {"bosch.com": "Bosch", "datadoghq.com": "Datadog"}


def employer(company, domains):
    for d in domains:
        if d in DOMAIN_COMPANY:
            return DOMAIN_COMPANY[d]
    if not company or ACADEMIA.search(company):
        return None
    current = company.split("->")[-1]  # "@kakao -> @LINE -> @webtoon" means webtoon now
    parts = [p.strip(" @,.") for p in re.split(r"[|/,]|\s(?=@)", current)]
    parts = [p for p in parts if p and not NOT_EMPLOYER.match(p)]
    if not parts:
        return None
    name = parts[0]
    for pat, canon in CANONICAL:
        if re.search(pat, name, re.I):
            return canon
    name = re.sub(r"\s+(inc\.?|gmbh|ltd\.?|llc|uk)$", "", name, flags=re.I)
    return name if name[:1].isupper() else name.title()


# every email a handle has committed with, so one @astronomer.io commit marks the person
emails_of = defaultdict(set)
for e, l in data["email_login"].items():
    emails_of[l.lower() if l else e].add(e)


def classify(email, login, company, date):
    """-> (slice, employer name or None)"""
    key = login.lower()
    for since, until, s in OVERRIDES.get(key, []):
        if (since is None or date >= since) and (until is None or date < until):
            return s, None
    domains = [e.split("@")[-1] for e in emails_of.get(key or email, {email})]
    if key in ASTRO:
        return "Astronomer", None
    for name, dom_re, comp_re in VENDORS:
        if any(re.search(dom_re, d) for d in domains) or (company and re.search(comp_re, company, re.I)):
            return name, None
    if key in OS4Y:
        return "opensource4you", None
    emp = employer(company, domains)
    return ("Other companies", emp) if emp else (INDEP, None)


counts, authors, os4y_in, companies = Counter(), defaultdict(set), Counter(), Counter()
for c in data["commits"]:
    login = data["email_login"].get(c["email"], "")
    if BOT.search(login) or BOT.search(c["email"]):
        continue
    s, emp = classify(c["email"], login, data["companies"].get(login, ""), c["date"][:10])
    counts[s] += 1
    authors[s].add((login or c["email"]).lower())
    if emp:
        companies[emp] += 1
    if login.lower() in OS4Y and s != "opensource4you":
        os4y_in[s] += 1
total = sum(counts.values())

if "--debug" in sys.argv:
    for s in ORDER:
        print(f"{s:30} {counts[s]:6} {counts[s]/total:6.1%} authors={len(authors[s])} os4y={os4y_in[s]}")
    print(companies.most_common(25))
    sys.exit()

# ---- render ----
W, H = 1600, 1030
CX, CY, R0, R1 = 500, 540, 195, 330
INK, MUTED, BG, RULE = "#1f2328", "#5f6672", "#fbfaf7", "#e4dfd4"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang TC', sans-serif"
o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
a(f"""<style>
 text {{ fill: {INK}; }}
 .h1 {{ font-size: 40px; font-weight: 750; }}
 .h2 {{ font-size: 22px; fill: {MUTED}; }}
 .name {{ font-size: 25px; font-weight: 650; }}
 .pct {{ font-size: 25px; font-weight: 750; }}
 .meta {{ font-size: 19px; fill: {MUTED}; }}
 .co {{ font-size: 19px; fill: {INK}; }}
 .center {{ font-size: 54px; font-weight: 750; }}
 .note {{ font-size: 18px; fill: {MUTED}; }}
</style>""")
a(f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>')
a(f'<text x="40" y="60" class="h1">Who builds Apache Airflow?</text>')
a(f'<text x="40" y="96" class="h2">Share of commits to apache/airflow main since {data["since"][:7]} by contributor affiliation</text>')

slices = [(s, counts[s]) for s in ORDER if counts[s]]
ang = -math.pi / 2
for s, n in slices:
    sweep = n / total * 2 * math.pi
    a0, a1 = ang, ang + sweep
    large = 1 if sweep > math.pi else 0
    p = lambda r, t: (CX + r * math.cos(t), CY + r * math.sin(t))
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(R1, a0), p(R1, a1), p(R0, a1), p(R0, a0)
    a(f'<path d="M{x0:.1f},{y0:.1f} A{R1},{R1} 0 {large} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} '
      f'A{R0},{R0} 0 {large} 0 {x3:.1f},{y3:.1f} Z" fill="{COLOR[s]}" stroke="{BG}" stroke-width="3"/>')
    ang = a1
a(f'<text x="{CX}" y="{CY+8}" text-anchor="middle" class="center">{total:,}</text>')
a(f'<text x="{CX}" y="{CY+44}" text-anchor="middle" class="meta">commits</text>')

# legend table on the right: swatch, name, share, commits/authors
lx, ly, LW = 960, 165, 580
for s, n in slices:
    a(f'<rect x="{lx}" y="{ly-21}" width="24" height="24" rx="5" fill="{COLOR[s]}"/>')
    a(f'<text x="{lx+38}" y="{ly}" class="name">{escape(s)}</text>')
    a(f'<text x="{lx+LW}" y="{ly}" text-anchor="end" class="pct">{n/total*100:.1f}%</text>')
    meta = f"{n:,} commits · {len(authors[s]):,} " + ("author" if len(authors[s]) == 1 else "authors")
    if os4y_in[s]:
        meta += f" · incl. {os4y_in[s]:,} by OS4Y members"
    a(f'<text x="{lx+38}" y="{ly+28}" class="meta">{escape(meta)}</text>')
    if s == "Other companies":  # name the biggest ones, wrapped to the legend width
        line, lines = "", []
        for co, k in companies.most_common(10):
            item = f"{co} {k:,}"
            if line and len(line) + len(item) + 3 > 50:
                lines.append(line)
                line = ""
            line = f"{line} · {item}" if line else item
        lines.append(line)
        lines = lines[:3]
        lines[-1] += " …"
        for i, t in enumerate(lines):
            a(f'<text x="{lx+38}" y="{ly+56+i*26}" class="co">{escape(t)}</text>')
        ly += 26 * len(lines)
    ly += 78

os4y_total = counts["opensource4you"] + sum(os4y_in.values())
ly += 6
a(f'<line x1="{lx}" y1="{ly-38}" x2="{lx+LW}" y2="{ly-38}" stroke="{RULE}" stroke-width="2"/>')
a(f'<text x="{lx}" y="{ly}" class="name">All opensource4you members</text>')
a(f'<text x="{lx+LW}" y="{ly}" text-anchor="end" class="pct">{os4y_total/total*100:.1f}%</text>')
a(f'<text x="{lx}" y="{ly+28}" class="meta">{os4y_total:,} commits, incl. members working at a company above</text>')

a(f'<text x="40" y="{H-56}" class="note">Affiliation: public astronomer GitHub org members, then commit email domain or GitHub profile company; '
  f'opensource4you = public members of the</text>')
a(f'<text x="40" y="{H-30}" class="note">opensource4you GitHub org not at a vendor. Elad Kalif counted as AWS before 2026-04, Astronomer after. '
  f'Bots excluded. main @ {data["head"][:10]}.</text>')
a("</svg>")
with open(OUT, "w") as f:
    f.write("\n".join(o))
print("wrote", OUT)
