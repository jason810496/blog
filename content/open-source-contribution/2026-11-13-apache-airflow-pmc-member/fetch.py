"""Fetch apache/airflow PR timestamps for jason810496. Usage: python3 fetch.py [prs.json]"""
import json, subprocess, time, datetime as dt, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "prs.json")
def gh(args):
    for i in range(5):
        r = subprocess.run(["gh","api",*args],capture_output=True,text=True)
        if r.returncode==0: return json.loads(r.stdout)
        time.sleep(20)
    raise SystemExit(r.stderr)
def search(q):
    dates=[]
    # monthly windows
    d=dt.date(2024,10,1)
    while d<=dt.date.today():
        n=(d.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
        page=1
        while True:
            res=gh(["-X","GET","search/issues","-f",f"q={q} created:{d}..{n-dt.timedelta(days=1)}","-f","per_page=100","-f",f"page={page}"])
            time.sleep(2.2)
            dates+= [{"created":it["created_at"],"merged":it["pull_request"].get("merged_at")} for it in res["items"]]
            if len(res["items"])<100: break
            page+=1
        d=n
    return sorted(dates, key=lambda r: r["created"])
def reviews():
    first={}
    y=dt.datetime(2024,10,1)
    while y<dt.datetime.utcnow():
        e=min(y.replace(year=y.year+1)-dt.timedelta(seconds=1), dt.datetime.utcnow().replace(microsecond=0))
        cur=None
        while True:
            after=f',after:"{cur}"' if cur else ''
            q='{user(login:"jason810496"){contributionsCollection(from:"%s",to:"%s"){pullRequestReviewContributionsByRepository(maxRepositories:25){repository{nameWithOwner} contributions(first:100%s){pageInfo{hasNextPage endCursor} nodes{occurredAt pullRequest{number}}}}}}}'%(y.isoformat()+"Z",e.isoformat()+"Z",after)
            res=gh(["graphql","-f",f"query={q}"])
            repos=[r for r in res["data"]["user"]["contributionsCollection"]["pullRequestReviewContributionsByRepository"] if r["repository"]["nameWithOwner"]=="apache/airflow"]
            if not repos: break
            c=repos[0]["contributions"]
            for nd in c["nodes"]:
                k=nd["pullRequest"]["number"]; t=nd["occurredAt"]
                if k not in first or t<first[k]: first[k]=t
            if not c["pageInfo"]["hasNextPage"]: break
            cur=c["pageInfo"]["endCursor"]
        y=e+dt.timedelta(seconds=1)
    return sorted(first.values())
data={"authored":search("repo:apache/airflow is:pr author:jason810496"),
      "reviewed":reviews()}
json.dump(data,open(OUT,"w"))
for k,v in data.items(): print(k,len(v),v[0],v[-1])
print("merged", sum(1 for r in data["authored"] if r["merged"]))
