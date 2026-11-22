"""Collect who authored apache/airflow commits since 2024-10-01.

Commits are read offline from a local clone; GitHub is only used to resolve
commit emails to handles (one batched GraphQL lookup per unique email), to read
profile `company` fields, and to list the public members of the opensource4you
and astronomer GitHub orgs.

Usage: python3 fetch_share.py [--repo ~/airflow-workspace] [--remote upstream] [--no-fetch] [--out share.json]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SINCE = "2024-10-01"
ORGS = ["opensource4you", "astronomer"]


def run(*cmd, cwd=None):
    for _ in range(5):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=False)
        if r.returncode == 0:
            return r.stdout
        time.sleep(10)
    raise SystemExit(f"{' '.join(cmd[:4])} failed: {r.stderr}")


FAILED = object()  # a query that kept failing; distinct from None (= GitHub says not found)


def graphql_batch(fields, size=40):
    """fields: list of GraphQL selections; yields (offset, results) per chunk.

    Big aliased queries occasionally time out or get reset, so each chunk is
    retried and split in half until it succeeds.
    """
    def query(chunk):
        q = "{" + " ".join(f"a{j}: {f}" for j, f in enumerate(chunk)) + "}"
        for _ in range(3):
            r = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"],
                               capture_output=True, text=True, check=False)
            try:
                data = json.loads(r.stdout).get("data")
            except json.JSONDecodeError:
                data = None
            if data is not None:  # missing users / partial errors come back as null fields
                return [data.get(f"a{j}") for j in range(len(chunk))]
            time.sleep(5)
        if len(chunk) == 1:
            print(f"giving up on {chunk[0][:80]}", file=sys.stderr)
            return [FAILED]
        mid = len(chunk) // 2
        return query(chunk[:mid]) + query(chunk[mid:])

    for i in range(0, len(fields), size):
        yield i, query(fields[i:i + size])


p = argparse.ArgumentParser()
p.add_argument("--repo", default=os.path.expanduser("~/airflow-workspace"))
p.add_argument("--remote", default="upstream", help="remote in --repo that points at apache/airflow")
p.add_argument("--no-fetch", action="store_true", help="use <remote>/main as it is")
p.add_argument("--out", default=os.path.join(HERE, "share.json"))
p.add_argument("--cache", default=os.path.join(HERE, "github_cache.json"),
               help="email->login and login->company lookups; only cache misses hit GitHub")
args = p.parse_args()

if not args.no_fetch:
    run("git", "fetch", "--no-tags", args.remote, "main", cwd=args.repo)
head = run("git", "rev-parse", f"{args.remote}/main", cwd=args.repo).strip()

commits = []
for line in run("git", "log", head, f"--since={SINCE}", "--format=%H%x09%ae%x09%aI", cwd=args.repo).splitlines():
    sha, email, date = line.split("\t")
    commits.append({"sha": sha, "email": email.lower(), "date": date})

# GitHub lookups are cached across runs and checkpointed after every chunk, so a
# rerun (or a resumed, interrupted run) only queries emails/logins it has not seen.
# email_login[e] == "" means "looked up, no GitHub user"; absent means never looked up.
cache = {"email_login": {}, "companies": {}}
if os.path.exists(args.cache):
    with open(args.cache) as f:
        cache.update(json.load(f))
email_login, companies = cache["email_login"], cache["companies"]


def save_cache():
    with open(args.cache + ".tmp", "w") as f:
        json.dump(cache, f, indent=0, sort_keys=True)
    os.replace(args.cache + ".tmp", args.cache)


# email -> GitHub login: noreply addresses carry the login; resolve the rest via one commit each
sample = {}
for c in commits:
    m = re.match(r"(?:\d+\+)?([^@]+)@users\.noreply\.github\.com$", c["email"])
    if m:
        email_login[c["email"]] = m.group(1)
    elif c["email"] not in email_login:
        sample.setdefault(c["email"], c["sha"])
emails = sorted(sample)
print(f"resolving {len(emails)} uncached emails", file=sys.stderr)
for off, res in graphql_batch([
        f'repository(owner: "apache", name: "airflow") {{ object(oid: "{sample[e]}") {{ ... on Commit {{ author {{ user {{ login }} }} }} }} }}'
        for e in emails]):
    for e, r in zip(emails[off:], res):
        if r is not FAILED:  # failed queries stay uncached so the next run retries them
            user = (((r or {}).get("object") or {}).get("author") or {}).get("user")
            email_login[e] = user["login"] if user else ""
    save_cache()

logins = sorted({email_login[c["email"]] for c in commits if email_login.get(c["email"])})
todo = [l for l in logins if l not in companies]
print(f"fetching {len(todo)} uncached profiles", file=sys.stderr)
for off, res in graphql_batch([f"user(login: {json.dumps(l)}) {{ company }}" for l in todo]):
    for l, r in zip(todo[off:], res):
        if r is not FAILED:  # None = deleted account / bot: cache as no company
            companies[l] = (r or {}).get("company") or ""
    save_cache()

members = {org: sorted(run("gh", "api", f"orgs/{org}/members", "--paginate", "--jq", ".[].login").split())
           for org in ORGS}

with open(args.out, "w") as f:
    json.dump({"since": SINCE, "head": head, "commits": commits,
               "email_login": {c["email"]: email_login.get(c["email"], "") for c in commits},
               "companies": {l: companies.get(l, "") for l in logins}, "org_members": members}, f, indent=0)
print(f"head={head[:10]} commits={len(commits)} emails={len(email_login)} logins={len(logins)} "
      + " ".join(f"{o}={len(m)}" for o, m in members.items()))
