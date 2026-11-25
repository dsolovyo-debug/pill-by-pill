"""Pill by Pill v5.26: optional FastAPI server.

The static site (the Netlify zip) is the product. This server exists for local work and for anyone who wants a JSON API.
It has no data of its own: it serves the same site folder and answers API calls by reading the same JSON files the
browser reads, so the two cannot drift apart. (v4 kept a second hand-typed copy of the data in this file.)

Run:   pip install fastapi uvicorn
       python -m uvicorn app:app            then open http://127.0.0.1:8000
The site folder is ./site, or the folder named in the PBP_SITE environment variable.
"""
import json, os, pathlib
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

SITE = pathlib.Path(os.environ.get("PBP_SITE", pathlib.Path(__file__).parent / "site")).resolve()
DATA = SITE / "data"
FLAGS = {"structure": 1, "sequence": 2, "us": 4, "ema": 8, "withdrawn": 16, "boxed": 32, "story": 64, "binding": 128, "ca": 256, "jp": 512, "eml": 1024}
HAS_FILTERS = {
    **{k: (lambda f, bit=v: bool(f & bit)) for k, v in FLAGS.items()},
    "nous": lambda f: not (f & FLAGS["us"]),
    "both": lambda f: bool(f & FLAGS["us"]) and bool(f & FLAGS["ema"]),
    "all4": lambda f: all(f & FLAGS[k] for k in ("us", "ema", "ca", "jp")),
    "euonly": lambda f: bool(f & FLAGS["ema"]) and not (f & FLAGS["us"]),
}

app = FastAPI(title="Pill by Pill API", version="5.26")


@lru_cache(maxsize=None)
def load(relative):
    path = (DATA / relative).resolve()
    if DATA not in path.parents or not path.is_file():
        raise HTTPException(404, "not found")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def index():
    d = load("drug_index.json")
    return [dict(zip(d["cols"], row)) for row in d["rows"]]


def search(text, limit):
    """Same order as searchDrugs() in site/js/data.js: name starts with, name contains, brand starts with, other names."""
    q = text.strip().lower()
    if len(q) < 2:
        return []
    rows = index()
    starts = [d for d in rows if d["name"].lower().startswith(q)]
    contains = [d for d in rows if q in d["name"].lower() and not d["name"].lower().startswith(q)]
    brands = [d for d in rows if q not in d["name"].lower() and (d["brand"] or "").lower().startswith(q)]
    found = starts + contains + brands
    if len(found) < limit and len(q) >= 3:
        seen = {d["id"] for d in found}
        for alias, i in load("drug_aliases.json").items():
            if alias.startswith(q) and rows[i]["id"] not in seen:
                seen.add(rows[i]["id"])
                found.append(dict(rows[i], via=alias))
                if len(found) >= limit:
                    break
    return found[:limit]


@app.get("/api/stats")
def stats():
    return load("catalogue_stats.json")


@app.get("/api/search")
def api_search(q: str, limit: int = Query(20, le=100)):
    return search(q, limit)


@app.get("/api/drugs")
def drugs(q: str = "", type: str = "", atc: str = "", decade: int = 0, flag: str = "", has: str = "", limit: int = Query(100, le=1000), offset: int = 0):
    """Filter the catalogue. Same filters as the #/ref/drugs page (accepts ?flag= and/or ?has=, including composite has filters)."""
    for k in (flag, has):
        if k and k not in HAS_FILTERS:
            raise HTTPException(400, f"flag must be one of {sorted(HAS_FILTERS)}")
    ql = q.lower()
    rows = [d for d in index()
            if (not ql or ql in d["name"].lower() or ql in (d["brand"] or "").lower())
            and (not type or d["type"] == type) and (not atc or atc in d["atc"])
            and (not decade or (d["year"] and d["year"] // 10 * 10 == decade))
            and (not flag or HAS_FILTERS[flag](d["flags"]))
            and (not has or HAS_FILTERS[has](d["flags"]))]
    return {"total": len(rows), "rows": rows[offset:offset + limit]}


@app.get("/api/drugs/{drug_id}")
def drug(drug_id: str):
    return load(f"drugs/{drug_id}.json")


@app.get("/api/molecules/{drug_id}")
def molecule(drug_id: str):
    path = (SITE / "mol" / f"{drug_id}.json").resolve()
    if SITE / "mol" not in path.parents or not path.is_file():
        raise HTTPException(404, "no drawing for this drug")
    return json.loads(path.read_text())


@app.get("/api/binding/{drug_id}")
def binding_site(drug_id: str):
    """Binding-site coordinates and contacts cut from the experimental structure named in the drug's "binding" block."""
    path = (SITE / "bind" / f"{drug_id}.json").resolve()
    if SITE / "bind" not in path.parents or not path.is_file():
        raise HTTPException(404, "no bound structure for this drug")
    return json.loads(path.read_text())


@app.get("/api/topics")
def topics():
    return load("topics.json")


@app.get("/api/topics/{key}")
def topic(key: str):
    return load(f"topics/{key}.json")


@app.get("/api/quiz")
def quiz():
    return load("quiz.json")


# v4 endpoint names that scripts may still call, mapped to the v5 topic that holds the same rows.
V4_ALIASES = {"peptides": "peptides", "failed-peptides": "failed-peptides", "failed-oligos": "failed-oligos", "pipeline": "pipeline",
              "ancient-traditions": "ancient", "interactions": "interactions", "meps-top-drugs": "meps", "oligo-timeline": "oligo-timeline",
              "biosimilars-2026": "biosimilars", "cms-part-d": "medicare", "global-agencies": "agencies", "global-divergences": "divergences",
              "global-pharmacovigilance": "pharmacovigilance", "global-access-programs": "access", "global-hta-agencies": "hta",
              "pill-identification": "pill-id", "submission-pathways": "submissions", "pediatric-and-vaccines": "pediatric",
              "controlled-substances": "controlled", "pharmacogenomics": "pgx", "otc-and-switches": "otc",
              "excipients-and-delivery": "excipients", "medical-discoveries": "discoveries", "careers": "careers"}


@app.get("/stats/{name}")
def v4_stats(name: str):
    if name not in V4_ALIASES:
        raise HTTPException(404, "this v4 endpoint has no v5 equivalent; see /api/topics")
    return load(f"topics/{V4_ALIASES[name]}.json")


app.mount("/", StaticFiles(directory=SITE, html=True), name="site")
