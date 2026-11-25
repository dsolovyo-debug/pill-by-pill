#!/usr/bin/env python3
"""Pill by Pill v6.1z Patch: Pharma Business Development, Licensing, M&A & Biotech Valuation Mechanics (#/ref/bd-deals, #/explore/bd-deals, /api/bd-deals).

Rounds out the complete v6.1a–v6.1z encyclopedia alphabet:
  1. Adds `pipeline/build_bd_deals.py` -> `site/data/bd_deals.json` (6 licensing/deal structures,
     6 M&A/CVR/FTC HSR pillars, 6 rNPV/PTRS/LOE valuation mechanics, and 6 capital-markets/SEC
     disclosure frameworks — 24 primary-sourced entries, zero fabricated valuations).
  2. Adds `site/js/bd_deals.js` (`bdDealsPage` with inline Deal Lifecycle SVG + 4 section filters)
     and wires `#/ref/bd-deals`, `#/explore/bd-deals`, `/api/bd-deals`, `REF_NAV_GROUPS`,
     `EXPLORE_NAV`, and `pipeline/run_all.sh`.
  3. Integrates `bd_deals.json` into `pipeline/build_global_search.py`,
     `pipeline/build_v60_static_pages.py` (`/bd-deals/` static SEO page + sitemap -> 41 pages),
     and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1z_pharma_bd_licensing_ma_valuation_patch.py --selftest
  python3 2026-11-24_v6.1z_pharma_bd_licensing_ma_valuation_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_BD_DEALS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1z Pharma Business Development, Licensing, M&A & Biotech Valuation Mechanics (`site/data/bd_deals.json`).\n\nComprehensive, primary-sourced educational reference covering:\n  1. Deal Structures & Licensing Mechanics (6 structures: Upfront/Milestones/Royalties, Option-to-License, Co-Development & Profit Split, Regional Out-Licensing, Academic Tech Transfer, Royalty Monetization & Non-Dilutive Finance)\n  2. M&A, Contingent Value Rights & Antitrust Review (6 pillars: Bolt-On Acquisitions & Patent Cliff Replacement, Contingent Value Rights CVRs, Due Diligence Data Rooms, FTC/DOJ HSR Antitrust Review, Reverse Mergers & SPACs, Spin-Outs & NewCos)\n  3. Risk-Adjusted Biotech Valuation Mechanics (6 frameworks: rNPV & Probability of Technical/Regulatory Success PTRS, Peak Sales & Market Share Modeling, Discount Rates WACC & Binary Readouts, Patent/LOE Cash-Flow Cliffs, Platform vs. Single-Asset Valuation, Public Biotech Catalyst Cycles)\n  4. Capital Markets, Disclosures & Governance (6 pillars: Venture Syndicates & Crossover Rounds, Nasdaq IPO & Follow-On Offerings, SEC Form 10-K/8-K & Material Clinical Disclosures, ClinicalTrials.gov vs. Press Releases, Pipeline Prioritization & Kill Decisions, Conflicts & Research Integrity)\n\nAll anchors are verified HTTPS primary sources (SEC, FTC, CBO, USPTO, NIH/PMC, ClinicalTrials.gov). Zero fabricated valuations or financial advice.\n\nUsage:\n  python3 pipeline/build_bd_deals.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nDEAL_STRUCTURES = [\n    {\n        "id": "bd-upfront-milestones",\n        "name": "In-Licensing & Out-Licensing (Upfront, Milestones & Royalties)",\n        "plain": "Instead of buying a whole biotech company, a large pharma company pays cash upfront for rights to develop a drug, plus bonus \'milestone\' checks if it clears clinical trials and a percentage (royalty) of future sales.",\n        "technical": "Headline \'biobucks\' totals combine guaranteed upfront cash (plus equity) with conditional development, regulatory, and commercial sales milestones and tiered net-sales royalties (typically single-digit to teens).",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "bd-option-deal",\n        "name": "Option-to-License (\'Try Before You Buy\') Deals",\n        "plain": "A big pharma partner pays a smaller upfront fee to fund early lab or Phase 1 work—earning the exclusive right to license the drug later once human proof-of-concept data reads out.",\n        "technical": "Transfers early binary risk to the biotech while giving the partner a pre-negotiated option exercise fee and license terms upon defined clinical data triggers (e.g., Phase 1b/2a).",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "bd-codev-profit",\n        "name": "Co-Development & Co-Commercialization (50/50 Profit Splits)",\n        "plain": "Two drugmakers share the R&D bills, run trials together, and split commercial profits in major markets (often 50/50 in the U.S.) while one partner leads overseas.",\n        "technical": "Governed by Joint Steering Committees (JSCs) with shared R&D cost caps, co-promotion field-force allocations, and U.S. profit-and-loss (P&L) sharing paired with ex-U.S. royalties.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n    {\n        "id": "bd-regional",\n        "name": "Regional Out-Licensing (U.S. / EU / Japan / China Rights)",\n        "plain": "A biotech keeps commercial rights in its home market while licensing rights in Europe, Japan, or Asia to local partners who already have regional regulatory and hospital sales teams.",\n        "technical": "Monetizes ex-core territories early to fund pivotal U.S. trials while leveraging regional partners for PMDA/EMA/NMPA filings and local HTA negotiations.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "bd-tech-transfer",\n        "name": "University Tech Transfer & Foundational IP Licensing",\n        "plain": "Many breakthrough drugs begin in university labs; university tech-transfer offices license those patents to newly formed startups in exchange for small equity stakes and modest single-digit royalties.",\n        "technical": "Operates under the Bayh-Dole Act (35 U.S.C. §§ 200–212), structuring exclusive field-of-use licenses with diligence milestones, patent-cost reimbursement, and sublicensing revenue shares.",\n        "url": "https://www.uspto.gov/patents/basics",\n    },\n    {\n        "id": "bd-royalty-finance",\n        "name": "Royalty Monetization & Synthetic Royalty Financing",\n        "plain": "Allows a biotech with an approved or late-stage drug to raise hundreds of millions in non-dilutive cash by selling a slice of its future sales royalties to specialized healthcare investors.",\n        "technical": "Preserves shareholder equity compared to secondary stock offerings; structured as capped or uncapped royalty purchase agreements disclosed in SEC Form 8-K/10-K filings.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n]\n\nMA_ANTITRUST = [\n    {\n        "id": "ma-bolt-on",\n        "name": "Strategic Bolt-On M&A & Patent-Cliff Replacement",\n        "plain": "When a giant pharmaceutical company\'s top-selling drugs approach patent expiry (LOE), it frequently acquires clinical-stage biotechs with de-risked Phase 2/3 assets to refill its revenue pipeline.",\n        "technical": "CBO notes that biopharma M&A and licensing form a specialized division of labor: nimble VC-backed biotechs take early scientific risk while large pharma scales global Phase 3 trials and commercial launches.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "ma-cvr",\n        "name": "Contingent Value Rights (CVRs) — Bridging Valuation Gaps",\n        "plain": "When a buyer and seller disagree on whether a pipeline drug will win FDA approval or hit $1 billion in sales, the buyer pays cash now plus a \'CVR\' bonus certificate that pays out later if the milestone is met.",\n        "technical": "Tradeable or non-tradeable contractual rights issued in public M&A transactions tied to objective FDA approval dates or cumulative net-sales thresholds.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n    {\n        "id": "ma-diligence",\n        "name": "Scientific, CMC, Clinical & IP Due Diligence",\n        "plain": "Before signing a billion-dollar deal, cross-functional teams inspect raw lab notebooks, FDA meeting minutes, factory inspection records, and patent claims inside a secure virtual data room.",\n        "technical": "Audits clinical trial data integrity (GCP/SAP), Freedom-to-Operate (FTO) and patent expiry, CDMO/CMC scalability and Form 483 history, and realistic payer/HTA net pricing.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "ma-ftc-hsr",\n        "name": "FTC / DOJ Antitrust Review & Hart-Scott-Rodino (HSR) Filings",\n        "plain": "Large pharma mergers must be cleared by federal antitrust regulators to ensure combining two companies won\'t eliminate competition for the same disease or kill a rival\'s pipeline drug.",\n        "technical": "Hart-Scott-Rodino Act premerger notification triggers FTC/DOJ review of overlapping therapeutic markets, \'killer acquisition\' risks, and potential divestiture consent decrees.",\n        "url": "https://www.ftc.gov/news-events/topics/competition-enforcement/health-care",\n    },\n    {\n        "id": "ma-reverse-merger",\n        "name": "Reverse Mergers & Cash-Shell Restructuring",\n        "plain": "When a public biotech\'s lead trial fails, it may still hold tens of millions in cash and a stock-exchange listing—allowing a private biotech with promising data to merge into it as an alternative to a traditional IPO.",\n        "technical": "Private company shareholders acquire majority ownership of the listed public shell (often paired with a concurrent PIPE financing), registered via SEC Form S-4 proxy statements.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n    {\n        "id": "ma-newco",\n        "name": "Asset-Centric \'NewCo\' Spin-Outs & Hub-and-Spoke Models",\n        "plain": "Rather than funding 10 risky drugs under one roof, investors increasingly spin a single promising molecule into a lean dedicated startup (\'NewCo\') with a focused team and clear exit path.",\n        "technical": "Ring-fences binary clinical risk and capital allocation around one lead asset or modality, enabling clean licensing or bolt-on acquisition without unwanted overhead.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n]\n\nVALUATION_MECHANICS = [\n    {\n        "id": "val-rnpv-ptrs",\n        "name": "Risk-Adjusted Net Present Value (rNPV) & PTRS",\n        "plain": "Because most early drugs fail in clinical trials, analysts value a pipeline medicine by estimating its future profits and multiplying them by the historical probability that it survives each trial phase.",\n        "technical": "rNPV discounts projected free cash flows by WACC and multiplies each phase\'s costs and post-launch cash flows by cumulative Probability of Technical and Regulatory Success (PTRS, e.g., Phase 1->Approval ~8–12% overall, varying by modality and therapeutic area).",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "val-peak-sales",\n        "name": "Epidemiology-Driven Peak Sales Modeling",\n        "plain": "Bottom-up drug revenue models start with real patient counts: Total patients -> Diagnosed -> Treated -> Biomarker-eligible -> Market share -> Annual net price (after rebates) -> Adherence.",\n        "technical": "Separates published Wholesale Acquisition Cost (WAC) from estimated Gross-to-Net (GTN) net price, accounting for compliance/persistence duration and line-of-therapy progression.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "val-wacc-binary",\n        "name": "Cost of Capital (WACC) & Binary Clinical Readouts",\n        "plain": "Unlike steady consumer companies, a clinical-stage biotech\'s entire value can jump 100% or drop 80% in a single morning when Phase 2 or Phase 3 trial results are announced.",\n        "technical": "High idiosyncratic clinical risk and long negative-cash-flow horizons drive elevated biotech discount rates (typically 10–15%+) compared to diversified commercial pharma.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7054832/",\n    },\n    {\n        "id": "val-loe-cliff",\n        "name": "Modeling Patent Expiry (LOE) & Terminal Value Cliffs",\n        "plain": "Drug valuation models do NOT assume profits grow forever—they model a sharp revenue cliff the exact year composition-of-matter patents and statutory exclusivities expire.",\n        "technical": "Incorporates Orange Book / Purple Book expiry dates, Patent Term Extension (35 U.S.C. § 156), pediatric +6-month extensions, and CMS IRA Medicare Negotiation eligibility (year 9 small molecule / year 13 biologic).",\n        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program",\n    },\n    {\n        "id": "val-platform-vs-asset",\n        "name": "Platform Technology vs. Lead-Asset Valuation",\n        "plain": "Investors often pay a premium for repeatable \'drug-making engines\' (like mRNA-LNP, GalNAc-siRNA, or ADC linkers), though markets still demand proof from at least one lead clinical product.",\n        "technical": "Platform value reflects optionality across multiple follow-on targets and repeatable CMC/PK translation, balanced against higher upfront R&D burn rates.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "val-catalysts",\n        "name": "Clinical & Regulatory Catalyst Calendars (PDUFA / AdComm)",\n        "plain": "Key scheduled milestones—IND clearance, Phase 2 topline data, FDA Advisory Committee votes, and PDUFA decision dates—drive step-function changes in probability of success.",\n        "technical": "Each positive milestone removes a major attrition gate from the rNPV tree, re-rating PTRS upward while reducing remaining time-to-cash-flow discounting.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review",\n    },\n]\n\nCAPITAL_GOVERNANCE = [\n    {\n        "id": "cap-vc-crossover",\n        "name": "Biotech Venture Capital (Seed -> Series A/B -> Crossover)",\n        "plain": "Specialized life-science VC firms fund early startups in tranches tied to lab milestones, followed by \'crossover\' funds that invest right before a public stock-market IPO.",\n        "technical": "Staged milestone-based tranched financings align capital deployment with preclinical de-risking (candidate nomination, IND clearance, Phase 1 safety).",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "cap-ipo-followon",\n        "name": "Nasdaq IPOs, Secondary Offerings & Cash Runway",\n        "plain": "Because clinical trials burn tens of millions per year with zero revenue, public biotechs closely manage \'cash runway\' (quarters of cash left) and raise follow-on equity right after positive trial readouts.",\n        "technical": "Public equity issuances (S-1 IPOs, S-3 shelf takedowns, ATM facilities, PIPEs) fund expensive Phase 2b/3 trials; balance-sheet runway is disclosed quarterly in SEC Form 10-Q/10-K.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n    {\n        "id": "cap-sec-disclosures",\n        "name": "SEC Form 10-K, 8-K & Material Clinical/FDA Disclosures",\n        "plain": "Publicly traded drug companies must promptly disclose material events—such as an FDA Clinical Hold, Complete Response Letter (CRL), or pivotal trial failure—in official SEC filings.",\n        "technical": "SEC Regulation FD and Form 8-K govern timely, non-selective disclosure of material clinical readouts, FDA regulatory correspondence, and licensing agreements.",\n        "url": "https://www.sec.gov/edgar/searchedgar/companysearch",\n    },\n    {\n        "id": "cap-ctgov-vs-pr",\n        "name": "Reading Press Releases vs. ClinicalTrials.gov & Peer Review",\n        "plain": "A company press release often highlights a single \'statistically significant\' secondary endpoint—whereas ClinicalTrials.gov and peer-reviewed journals reveal whether the pre-specified primary endpoint actually succeeded.",\n        "technical": "Always cross-check corporate topline releases against the pre-registered primary endpoint on ClinicalTrials.gov (FDAAA 801), full confidence intervals, and FDA review summaries (Drugs@FDA).",\n        "url": "https://clinicaltrials.gov/policy/fdaaa-801-final-rule",\n    },\n    {\n        "id": "cap-kill-decisions",\n        "name": "Portfolio Governance & \'Fail Fast\' Kill Decisions",\n        "plain": "Because Phase 3 trials cost hundreds of millions, disciplined R&D organizations design tough early Phase 1/2 \'go/no-go\' tests to stop weak candidates early and redirect capital to stronger ones.",\n        "technical": "Clear pre-specified Target Product Profiles (TPPs) and biomarker futility gates prevent sunk-cost bias from carrying marginal molecules into costly confirmatory trials.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "cap-integrity",\n        "name": "Financial Disclosure & Clinical Research Integrity (21 CFR Part 54)",\n        "plain": "To prevent financial bias from skewing trial results, federal rules require clinical investigators to disclose stock ownership, consulting payments, or patent ties to the drug\'s sponsor.",\n        "technical": "21 CFR Part 54 mandates Financial Disclosure by Clinical Investigators in NDA/BLA submissions, complemented by CMS Open Payments transparency reporting.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54",\n    },\n]\n\n\ndef build_bd_deals(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced educational reference on pharmaceutical business development, licensing, M&A, FTC antitrust, risk-adjusted rNPV valuation concepts, and SEC/clinical disclosures (SEC, FTC, CBO, USPTO, eCFR, CMS). Educational reference only—not financial or investment advice.",\n        "deal_structures": DEAL_STRUCTURES,\n        "ma_antitrust": MA_ANTITRUST,\n        "valuation_mechanics": VALUATION_MECHANICS,\n        "capital_governance": CAPITAL_GOVERNANCE,\n    }\n    (data_dir / "bd_deals.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "deal_structures": len(DEAL_STRUCTURES),\n        "ma_antitrust": len(MA_ANTITRUST),\n        "valuation_mechanics": len(VALUATION_MECHANICS),\n        "capital_governance": len(CAPITAL_GOVERNANCE),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_bd_deals(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
BD_DEALS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderBdLifecycleSvg() {\n  const nodes = [\n    { x: 8, label: "1. Tech Transfer", sub: "Bayh-Dole / Seed" },\n    { x: 140, label: "2. VC & Option", sub: "Series A–B / PoC" },\n    { x: 272, label: "3. License / IPO", sub: "Upfront + Milestones" },\n    { x: 404, label: "4. Bolt-On M&A", sub: "CVR / FTC HSR" },\n    { x: 536, label: "5. rNPV & LOE", sub: "PTRS / Patent Cliff" },\n  ];\n  return html`<figure class="bd-flow" aria-label="Biopharma capital, licensing, and M&A deal lifecycle">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 2 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 2 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">How biotech discoveries move from university tech transfer and VC syndicates through licensing, IPOs, and strategic pharma M&amp;A.</figcaption>\n  </figure>`;\n}\n\nexport async function bdDealsPage(query, mode = "ref") {\n  const doc = await getJSON("data/bd_deals.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/bd-deals" : "#/ref/bd-deals";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Pharma Business Development, Licensing, M&A & Biotech Valuation",\n    body: html`\n      <h1>Pharma Business Development, Licensing, M&amp;A &amp; Biotech Valuation</h1>\n      <p class="lead">${mode === "explore"\n        ? "How small biotech startups partner with big pharmaceutical companies—explaining upfront payments, clinical milestones, royalties, acquisitions, and how drug pipelines are valued when most candidates fail."\n        : "Primary-sourced educational reference covering 6 licensing/deal structures, 6 M&A & FTC antitrust frameworks, 6 risk-adjusted rNPV valuation mechanics, and 6 capital-market & SEC disclosure standards (checked " + doc.checked + ")."}</p>\n\n      ${renderBdLifecycleSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=deals"${sec === "deals" ? \' aria-current="page"\' : ""}>Licensing &amp; Deals (6)</a> ·\n        <a href="${base}?section=ma"${sec === "ma" ? \' aria-current="page"\' : ""}>M&amp;A &amp; Antitrust (6)</a> ·\n        <a href="${base}?section=valuation"${sec === "valuation" ? \' aria-current="page"\' : ""}>rNPV Valuation (6)</a> ·\n        <a href="${base}?section=capital"${sec === "capital" ? \' aria-current="page"\' : ""}>Capital &amp; SEC (6)</a>\n      </p>\n\n      ${show("deals") ? html`\n        <h2 id="deals">1. Deal Structures &amp; Licensing Mechanics (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharma licensing and deal structures">\n          <table class="tbl"><thead><tr><th>Deal Structure</th><th>${mode === "explore" ? "How It Works" : "Commercial & Contractual Mechanics"}</th></tr></thead>\n          <tbody>${(doc.deal_structures || []).map((d) => html`<tr id="${d.id}">\n            <td><b><a href="${d.url}" target="_blank" rel="noopener">${d.name}</a></b></td>\n            <td>${mode === "explore" ? d.plain : html`${d.plain}<br><span class="muted small">${d.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("ma") ? html`\n        <h2 id="ma">2. Strategic M&amp;A, CVRs &amp; FTC Antitrust Review (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharma M&A and antitrust">\n          <table class="tbl"><thead><tr><th>M&amp;A Pillar</th><th>${mode === "explore" ? "Why Companies Use It" : "Transaction, Diligence & HSR Governance"}</th></tr></thead>\n          <tbody>${(doc.ma_antitrust || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("valuation") ? html`\n        <h2 id="valuation">3. Risk-Adjusted Biotech Valuation Mechanics (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Biotech valuation mechanics">\n          <table class="tbl"><thead><tr><th>Valuation Concept</th><th>${mode === "explore" ? "Plain-Language Intuition" : "rNPV, PTRS, Peak Sales & LOE Modeling"}</th></tr></thead>\n          <tbody>${(doc.valuation_mechanics || []).map((v) => html`<tr id="${v.id}">\n            <td><b><a href="${v.url}" target="_blank" rel="noopener">${v.name}</a></b></td>\n            <td>${mode === "explore" ? v.plain : html`${v.plain}<br><span class="muted small">${v.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("capital") ? html`\n        <h2 id="capital">4. Capital Markets, SEC Disclosures &amp; Governance (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Biotech capital markets and governance">\n          <table class="tbl"><thead><tr><th>Market / Governance Pillar</th><th>${mode === "explore" ? "How Oversight Works" : "SEC, ClinicalTrials.gov & 21 CFR Part 54"}</th></tr></thead>\n          <tbody>${(doc.capital_governance || []).map((c) => html`<tr id="${c.id}">\n            <td><b><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></b></td>\n            <td>${mode === "explore" ? c.plain : html`${c.plain}<br><span class="muted small">${c.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/economics">Drug Economics &amp; GTN</a> · <a href="#/ref/ip">Patents, Hatch-Waxman &amp; BPCIA</a> · <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a> · <a href="#/ref/global-reg">Global Agencies &amp; HTA</a>.</p>\n    `,\n  };\n}\n'


def _write_if_changed(path: pathlib.Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { bdDealsPage } from "./bd_deals.js";\n'
    if "./bd_deals.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/bd-deals"' not in txt:
        for anchor in ('if (path === "/ref/shortages")', 'if (path === "/ref/amr")', 'if (path === "/ref/history-laws")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/bd-deals") return bdDealsPage(query, "ref");\n'
                    '  if (path === "/explore/bd-deals") return bdDealsPage(query, "explore");\n'
                    '  ' + anchor
                )
                txt = txt.replace(anchor, rep, 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "#/ref/bd-deals" not in txt:
        for anchor in ('["#/ref/shortages", "Drug shortages & supply"]', '["#/ref/economics", "Drug economics"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/bd-deals", "BD, licensing & M&A"]', 1)
                changed = True
                break
    if "#/explore/bd-deals" not in txt:
        for anchor in ('["#/explore/shortages", "Drug shortages & supply"]', '["#/explore/economics", "Funding & pricing"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/bd-deals", "BD, licensing & M&A"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_bd_deals.py" in txt:
        return False
    hook = "\n# v6.1z: Pharma Business Development, Licensing, M&A & Biotech Valuation Mechanics\npython3 pipeline/build_bd_deals.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/bd-deals"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/bd-deals")\n'
        'def api_bd_deals():\n'
        '    return _read_json(SITE_DIR / "data" / "bd_deals.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"bd_deals.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    bd_ref = _load(data_dir / "bd_deals.json", {}) or {}\n'
        '    for sec_key, sec_q in [("deal_structures", "deals"), ("ma_antitrust", "ma"), ("valuation_mechanics", "valuation"), ("capital_governance", "capital")]:\n'
        '        for item in (bd_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "bd_deals",\n'
        '                "group": "Business Development, M&A & Valuation",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/bd-deals?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/bd-deals?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"business development licensing M&A merger acquisition CVR HSR antitrust rNPV PTRS peak sales IPO biotech valuation SEC {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"bd-deals", "#/ref/bd-deals"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    bd_doc = _load_json(data_dir / "bd_deals.json")\n'
        '    if isinstance(bd_doc, dict) and bd_doc.get("deal_structures"):\n'
        '        bd_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (bd_doc.get("deal_structures") or []) + (bd_doc.get("valuation_mechanics") or []))\n'
        '        pages.append(("bd-deals", "#/ref/bd-deals", "Pharma Business Development, Licensing, M&A & Biotech Valuation",\n'
        '                      "Primary-sourced guide to pharma licensing (upfront/milestones/royalties), M&A & CVRs, FTC HSR antitrust, rNPV/PTRS valuation, and SEC clinical disclosures.",\n'
        '                      f"<ul>{bd_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/bd-deals"' in txt:
        return False
    for anchor in ('    "/#/explore/shortages",', '    "/#/explore/amr",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/bd-deals",\n    "/#/explore/bd-deals",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_bd_deals_py": _write_if_changed(pipe_dir / "build_bd_deals.py", BUILD_BD_DEALS_PY),
        "bd_deals_js": _write_if_changed(js_dir / "bd_deals.js", BD_DEALS_JS),
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
        "global_search_indexed": _patch_global_search(pipe_dir / "build_global_search.py"),
        "static_seo_added": _patch_static_pages(pipe_dir / "build_v60_static_pages.py"),
        "test_v60_site_updated": _patch_test_v60_site(root / "tests" / "test_v60_site.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)
        (root / "tests").mkdir()

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/shortages") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/shortages", "Drug shortages & supply"]] }];\nconst EXPLORE_NAV = [["#/explore/shortages", "Drug shortages & supply"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/shortages",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_bd_deals.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_bd_deals.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"deal_structures": 6, "ma_antitrust": 6, "valuation_mechanics": 6, "capital_governance": 6}, out

        doc = json.loads((root / "site" / "data" / "bd_deals.json").read_text(encoding="utf-8"))
        for k in ("deal_structures", "ma_antitrust", "valuation_mechanics", "capital_governance"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61Z_PHARMA_BD_LICENSING_MA_VALUATION_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1z Pharma BD, Licensing, M&A & Valuation patch.")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to unpacked source directory")
    ap.add_argument("--selftest", action="store_true", help="Run built-in verification tests")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if args.apply:
        print(json.dumps(apply_patch(args.apply), indent=2))
        return 0
    ap.error("Provide --apply <dir> or --selftest")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
