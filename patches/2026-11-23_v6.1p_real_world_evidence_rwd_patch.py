#!/usr/bin/env python3
"""Pill by Pill v6.1p Patch: Real-World Evidence (RWE), Real-World Data (RWD) & Post-Market Healthcare Data Reference (#/ref/rwe, #/explore/rwe, /api/rwe).

1. Adds `pipeline/build_rwe.py` -> `site/data/rwe.json` (6 RWD sources & data-quality pillars,
   6 FDA/EMA RWE regulatory frameworks, 6 RWE study designs & causal-inference methods, and
   6 global RWE networks & post-market applications — 24 primary-sourced entries).
2. Adds `site/js/rwe.js` (`rwePage` with inline RWD-to-RWE Evidence Pipeline SVG + 4 section
   filters) and wires `#/ref/rwe`, `#/explore/rwe`, `/api/rwe`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `rwe.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/rwe/` static SEO page + sitemap entry -> 32
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1p_real_world_evidence_rwd_patch.py --selftest
  python3 2026-11-23_v6.1p_real_world_evidence_rwd_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_RWE_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1p Real-World Evidence (RWE) & Real-World Data (RWD) Reference (`site/data/rwe.json`).

Comprehensive, primary-sourced reference covering:
  1. Real-World Data (RWD) Sources & Fitness-for-Use (6 pillars)
  2. FDA & EMA Regulatory RWE Frameworks (6 pillars)
  3. RWE Study Designs & Causal Inference (6 pillars)
  4. Global RWE Networks & Post-Market Applications (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA, EMA).

Usage:
  python3 pipeline/build_rwe.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

RWD_SOURCES = [
    {
        "id": "rwd-ehr",
        "name": "Electronic Health Records (EHRs) & Clinical Notes",
        "category": "Routine Clinical Care",
        "plain": "Hospital and clinic computer charts capture lab values, diagnoses, prescriptions, and doctor notes from everyday care—offering rich clinical detail beyond billing codes.",
        "technical": "FDA July 2024 Final Guidance details assessing EHR relevance and reliability (provenance, validation of unstructured NLP-extracted variables, missingness, and longitudinal linkage) for regulatory effectiveness and safety studies.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-electronic-health-records-and-medical-claims-data-support-regulatory",
    },
    {
        "id": "rwd-claims",
        "name": "Medical & Pharmacy Claims Databases",
        "category": "Administrative Billing",
        "plain": "Insurance billing records track every filled prescription, ER visit, and procedure across millions of patients—making them ideal for spotting rare side effects and long-term patterns.",
        "technical": "Longitudinal payer claims provide near-complete capture of reimbursed encounters and outpatient pharmacy dispensings across care sites, though lacking clinical severity/biomarker granularity unless linked to EHR or registry data.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-electronic-health-records-and-medical-claims-data-support-regulatory",
    },
    {
        "id": "rwd-registries",
        "name": "Disease, Product & Pregnancy Registries",
        "category": "Curated Cohorts",
        "plain": "Registries follow a defined group of patients—such as people with a rare genetic disease or pregnant patients on a new medicine—with standardized checkups over years.",
        "technical": "FDA December 2023 Final Guidance outlines fitness-for-use criteria for disease and product registries: common data elements, active follow-up for outcome ascertainment, governance, and linkage to external mortality/claims sources.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-registries-support-regulatory-decision-making-drug-and-biological-products",
    },
    {
        "id": "rwd-dht",
        "name": "Digital Health Technologies (DHTs) & Wearables",
        "category": "Remote Acquisition",
        "plain": "Smartwatches, continuous glucose monitors, and home spirometers measure how patients actually sleep, move, and breathe between clinic visits.",
        "technical": "FDA December 2023 Guidance on Digital Health Technologies for Remote Data Acquisition covers verification, analytical/clinical validation, usability, and 21 CFR Part 11/data-integrity controls for sensor-derived RWD endpoints.",
        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",
    },
    {
        "id": "rwd-data-standards",
        "name": "RWD Data Standards & Common Data Models (CDISC / OMOP)",
        "category": "Interoperability",
        "plain": "Because hospitals format charts differently, researchers translate records into shared 'common data models' so the same analysis can run consistently across many health systems.",
        "technical": "FDA Guidance on Data Standards for Drug and Biological Product Submissions Containing RWD addresses mapping heterogeneous EHR/claims/registry tables into FDA-supported CDISC (SDTM/ADaM) submission formats via documented ETL pipelines.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/center-biologics-evaluation-and-research-center-drug-evaluation-and-research-real-world-evidence",
    },
    {
        "id": "rwd-relevance-reliability",
        "name": "Data Relevance & Reliability (Accrual & Quality Assurance)",
        "category": "Fit-for-Purpose Audit",
        "plain": "Before trusting real-world data for a drug approval, regulators check two things: does the dataset actually cover the right patients and outcomes (relevance), and was it recorded accurately (reliability)?",
        "technical": "Core FDA RWE Framework pillar evaluating data accrual (how data were captured), data quality control (completeness, plausibility, conformance), and adequacy of exposure/outcome/confounder definitions.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/fda-use-real-world-evidence-regulatory-decision-making",
    },
]

RWE_REGULATORY = [
    {
        "id": "reg-21st-cures",
        "name": "21st Century Cures Act (FD&C Act § 505F) & FDA RWE Framework",
        "category": "US Statutory Mandate",
        "plain": "Congress directed FDA to build a formal program for using real-world evidence—not just traditional randomized trials—to support new drug uses and post-approval safety studies.",
        "technical": "Section 505F of the FD&C Act (21 U.S.C. 355g) defines RWE and directed FDA's 2018 Framework for evaluating RWE to support new indications for approved drugs or satisfy post-approval study requirements.",
        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",
    },
    {
        "id": "reg-advancing-rwe",
        "name": "FDA Advancing Real-World Evidence Program (PDUFA VII)",
        "category": "Sponsor Consultation",
        "plain": "A dedicated FDA fast-track consultation program where drugmakers can co-design real-world studies with FDA reviewers early—before spending years collecting data.",
        "technical": "PDUFA VII commitment providing sponsors early, iterative Type C-style engagement with CDER/CBER reviewers on study protocols, RWD sources, and statistical analysis plans intended to support regulatory decisions.",
        "url": "https://www.fda.gov/drugs/development-resources/advancing-real-world-evidence-program",
    },
    {
        "id": "reg-external-controls",
        "name": "Externally Controlled Trials (Draft Guidance, Feb 2023)",
        "category": "Single-Arm Comparators",
        "plain": "When a disease is so rare or fatal that giving half the patients a placebo would be unethical, an external control arm built from real-world patient records can serve as the comparison group.",
        "technical": "FDA Draft Guidance on Considerations for the Design and Conduct of Externally Controlled Trials addresses baseline comparability, index-date alignment (immortal-time bias), outcome ascertainment equivalence, and unmeasured confounding sensitivity.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-and-conduct-externally-controlled-trials-drug-and-biological-products",
    },
    {
        "id": "reg-non-interventional",
        "name": "Non-Interventional (Observational) Studies for Drugs & Biologics",
        "category": "Protocol Pre-Specification",
        "plain": "To prevent 'cherry-picking' results from huge medical databases, FDA expects researchers to lock in their hypothesis, patient rules, and analysis plan before looking at the outcomes.",
        "technical": "FDA Draft Guidance on Considerations Regarding Non-Interventional Studies emphasizes pre-specified protocols/SAPs, audit trails of feasibility vs. hypothesis-testing analyses, and bias mitigation (confounding by indication, selection bias).",
        "url": "https://www.fda.gov/science-research/real-world-evidence/center-biologics-evaluation-and-research-center-drug-evaluation-and-research-real-world-evidence",
    },
    {
        "id": "reg-pragmatic-rcts",
        "name": "Pragmatic & Point-of-Care Randomized Trials in Routine Practice",
        "category": "Hybrid Interventional RWE",
        "plain": "Pragmatic trials randomize patients to different treatments right inside normal clinics and use routine medical charts instead of expensive extra study visits.",
        "technical": "FDA Draft Guidance on Integrating Randomized Controlled Trials Into Routine Clinical Practice streamlines informed consent, local-clinician monitoring, and RWD endpoint capture while preserving randomization against confounding.",
        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",
    },
    {
        "id": "reg-device-rwe",
        "name": "RWE for Medical Devices & Companion Diagnostics (CDRH)",
        "category": "Device Lifecycle",
        "plain": "Medical device and diagnostic makers can also use hospital registries and lab records to expand a test's approved uses or track long-term implant safety.",
        "technical": "FDA Guidance on Use of Real-World Evidence to Support Regulatory Decision-Making for Medical Devices clarifies sufficiency criteria for 510(k), De Novo, PMA, and post-market surveillance studies using RWD.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-real-world-evidence-support-regulatory-decision-making-medical-devices",
    },
]

STUDY_DESIGNS = [
    {
        "id": "des-target-trial",
        "name": "Target Trial Emulation & Active-Comparator New-User Design",
        "category": "Causal Inference",
        "plain": "Epidemiologists mimic a randomized clinical trial inside health records—comparing patients who just started Drug A against similar patients who just started Drug B.",
        "technical": "Aligns eligibility, treatment assignment (time zero), and follow-up to eliminate immortal-time and prevalent-user biases; pairs new-user active comparators with propensity score matching or IPTW.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/fda-use-real-world-evidence-regulatory-decision-making",
    },
    {
        "id": "des-sccs",
        "name": "Self-Controlled Case Series (SCCS) & Case-Crossover",
        "category": "Within-Person Safety",
        "plain": "Instead of comparing different people, each patient acts as their own control—comparing side-effect rates right after taking a vaccine or drug against other weeks in the same person's life.",
        "technical": "Within-individual design automatically controls for all fixed, time-invariant confounders (genetics, chronic baseline risk); widely used by FDA Sentinel for vaccine and acute drug safety signal evaluation.",
        "url": "https://www.fda.gov/safety/fdas-sentinel-initiative",
    },
    {
        "id": "des-propensity",
        "name": "Propensity Score Matching, Stratification & IPTW",
        "category": "Confounder Balancing",
        "plain": "Because doctors do not prescribe drugs randomly, statistical weighting balances age, lab results, and other illnesses so treated and untreated groups start on equal footing.",
        "technical": "Estimates probability of treatment conditional on measured baseline covariates; standardized mean differences (<0.10) verify covariate balance, supplemented by quantitative bias analysis (E-values) for unmeasured confounding.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-and-conduct-externally-controlled-trials-drug-and-biological-products",
    },
    {
        "id": "des-bias-checks",
        "name": "Negative Control Outcomes & Immortal-Time Bias Prevention",
        "category": "Internal Validity",
        "plain": "Researchers test 'negative control' outcomes that a drug cannot possibly cause—if the database still shows a fake effect, hidden bias is distorting the study.",
        "technical": "Negative control exposures/outcomes calibrate residual confounding and p-value inflation; strict time-zero alignment prevents immortal-time bias when defining responder or treatment-duration cohorts.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/real-world-evidence-rwe-resources",
    },
    {
        "id": "des-natural-history",
        "name": "Rare-Disease Natural History & Historical Control Studies",
        "category": "Orphan Drug Development",
        "plain": "For ultra-rare childhood diseases, natural history studies map how the illness progresses without treatment so single-arm gene-therapy trials can measure real improvement.",
        "technical": "Prospective or retrospective longitudinal characterization of untreated disease trajectory; informs biomarker/endpoint selection and serves as external benchmark when concurrent randomized controls are infeasible.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-registries-support-regulatory-decision-making-drug-and-biological-products",
    },
    {
        "id": "des-submission-pkg",
        "name": "RWD/RWE Regulatory Submission & Traceability Package",
        "category": "eCTD Documentation",
        "plain": "Every real-world study sent to regulators must include a transparent paper trail showing exactly where the data came from, how records were cleaned, and every line of analysis code.",
        "technical": "FDA Guidance on Submitting Documents Utilizing RWD/RWE specifies flagging RWD/RWE submissions in cover letters, documenting data curation/linkage lineage, and providing reproducible analytical scripts.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/center-biologics-evaluation-and-research-center-drug-evaluation-and-research-real-world-evidence",
    },
]

RWE_NETWORKS = [
    {
        "id": "net-darwin-eu",
        "name": "EMA DARWIN EU (Data Analysis and Real World Interrogation Network)",
        "category": "European Union",
        "plain": "Europe's federated real-world evidence network connects vetted hospital, GP, and registry databases across EU countries so EMA can run rapid drug-safety and usage studies.",
        "technical": "Established by EMA and HMA using the OMOP Common Data Model via a Coordination Centre; delivers regulator-led non-interventional studies across European healthcare data partners to inform CHMP, PRAC, and EU HTAR decisions.",
        "url": "https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/real-world-evidence/data-analysis-real-world-interrogation-network-darwin-eu",
    },
    {
        "id": "net-sentinel",
        "name": "FDA Sentinel Initiative & BEST (Biologics Effectiveness and Safety)",
        "category": "United States",
        "plain": "FDA's distributed safety network queries anonymized claims and EHRs from tens of millions of Americans without ever moving private patient files out of their health plans.",
        "technical": "Mandated by FDAAA 2007 using the Sentinel Common Data Model (SCDM) and modular analytic tools; CBER's parallel BEST system expands active surveillance for vaccines, blood products, and cell/gene therapies.",
        "url": "https://www.fda.gov/safety/fdas-sentinel-initiative",
    },
    {
        "id": "net-hma-ema-cat",
        "name": "HMA–EMA Catalogues of RWD Sources & Studies",
        "category": "Transparency Registry",
        "plain": "A public European directory listing verified healthcare databases and ongoing observational studies so regulators, payers, and scientists can see what real-world evidence exists.",
        "technical": "Replaced the legacy ENCePP Resources Database in 2024; provides standardized metadata on European RWD data sources, OMOP/CDM readiness, and registered non-interventional study protocols.",
        "url": "https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/real-world-evidence",
    },
    {
        "id": "net-label-expansion",
        "name": "Post-Approval Label Expansion & Pediatric / Rare Approvals",
        "category": "Regulatory Impact",
        "plain": "Real-world evidence has already helped expand approved drug labels—such as adding male breast cancer or transplant indications—when everyday clinic data confirmed the medicine worked.",
        "technical": "FDA RWE examples include label expansions, confirmatory evidence under Accelerated Approval, and post-marketing requirement (PMR) fulfillment where randomized trials are impractical or unethical.",
        "url": "https://www.fda.gov/science-research/real-world-evidence/fda-use-real-world-evidence-regulatory-decision-making",
    },
    {
        "id": "net-hta-payer",
        "name": "HTA, Outcomes-Based Contracts & Post-Launch Value",
        "category": "Market Access",
        "plain": "Health insurers and European HTA bodies increasingly use real-world survival and hospitalization data to decide whether an expensive therapy works as well in clinics as it did in trials.",
        "technical": "Supports Coverage with Evidence Development (CED), Managed Entry Agreements (MEAs), and comparative effectiveness modeling under EU HTAR Joint Clinical Assessments and national HTA reassessments.",
        "url": "https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/real-world-evidence",
    },
    {
        "id": "net-privacy-hipaa",
        "name": "Patient Privacy, De-Identification & Federated Querying",
        "category": "Data Governance",
        "plain": "Federated networks send the statistical question to each hospital rather than pooling raw patient files into one giant database—protecting patient privacy by design.",
        "technical": "Applies HIPAA Safe Harbor/Expert Determination de-identification (US) and GDPR data-minimization/pseudonymization (EU) alongside distributed common-data-model execution where only aggregate counts cross institutional boundaries.",
        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",
    },
]


def build_rwe(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "rwd_sources": len(RWD_SOURCES),
            "rwe_regulatory": len(RWE_REGULATORY),
            "study_designs": len(STUDY_DESIGNS),
            "rwe_networks": len(RWE_NETWORKS),
        },
        "rwd_sources": RWD_SOURCES,
        "rwe_regulatory": RWE_REGULATORY,
        "study_designs": STUDY_DESIGNS,
        "rwe_networks": RWE_NETWORKS,
    }
    (data_dir / "rwe.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_rwe.py <site/data>")
    print(json.dumps(build_rwe(pathlib.Path(sys.argv[1])), indent=2))
'''

RWE_JS = '''// Pill by Pill v6.1p: Real-World Evidence (RWE), Real-World Data (RWD) & Post-Market Healthcare Data Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["sources", "RWD Sources", "rwd_sources"],
  ["regulatory", "FDA & EMA Frameworks", "rwe_regulatory"],
  ["designs", "Study Designs & Bias", "study_designs"],
  ["networks", "Networks & Impact", "rwe_networks"],
];

function rwePipelineSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Real-World Data to Regulatory Real-World Evidence pipeline">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Routine RWD</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">EHRs, Claims, Registries</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">DHTs &amp; Lab Feeds</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rwe-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Fitness &amp; CDM</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Relevance &amp; Reliability</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">OMOP / Sentinel / CDISC</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rwe-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Causal Design</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Target Trial / SCCS</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Propensity &amp; Bias Checks</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rwe-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Regulatory RWE</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Label Expansion &amp; PMRs</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Safety &amp; HTA Decisions</text>
      <defs><marker id="rwe-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Real-world evidence transforms routinely collected healthcare records into regulatory-grade safety, effectiveness, and value evidence.</figcaption>
  </figure>`;
}

export async function rwePage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/rwe.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/rwe" : "#/ref/rwe";

  const pills = html`<div class="chips" role="navigation" aria-label="RWE sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Topic / Method</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.category}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${rwePipelineSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA 21st Century Cures / PDUFA VII RWE guidance and EMA DARWIN EU documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Real-World Evidence"]] : [REF_HOME, ["Real-World Evidence"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Real-World Evidence (RWE) & Post-Market Healthcare Data",
      lede: env === "explore"
        ? "How doctors and regulators learn from everyday medical charts, insurance claims, and patient registries after a medicine is approved."
        : "EHRs, claims, registries, FDA 21st Century Cures / PDUFA VII RWE guidances, target trial emulation, FDA Sentinel, and EMA DARWIN EU.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on RWE and healthcare data.", href: env === "explore" ? "#/ref/rwe" : "#/explore/rwe" },
        { title: "Pharmacovigilance & Drug Safety", text: "FDA AEMS, Sentinel active surveillance, and EudraVigilance.", href: "#/ref/safety" },
        { title: "Global Regulatory & HTA", text: "How regulators and payers evaluate post-launch evidence.", href: "#/ref/global-reg" },
      ],
    }),
  };
}
'''


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
    if 'rwe.js' not in txt:
        for anchor in ('import * as diagnostics from "./diagnostics.js";\n', 'import * as globalRegHta from "./global_reg_hta.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as rwe from "./rwe.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as rwe from "./rwe.js";\n' + txt
            changed = True
    if '"/ref/rwe"' not in txt:
        for anchor in ('if (path === "/ref/diagnostics")', 'if (path === "/ref/global-reg")', 'if (path === "/ref/sterile")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/rwe") return { env: "ref", current: "#/ref/rwe", ...(await rwe.rwePage(query, "ref")) };\n  if (path === "/explore/rwe") return { env: "explore", current: "#/explore/rwe", ...(await rwe.rwePage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/rwe" not in txt:
        for anchor in ('["#/ref/diagnostics", "Diagnostics & CDx"]', '["#/ref/global-reg", "Global reg & HTA"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/rwe", "Real-World Evidence"]', 1)
                changed = True
                break
    if "#/explore/rwe" not in txt:
        for anchor in ('["#/explore/diagnostics", "Diagnostics & CDx"]', '["#/explore/global-reg", "Global reg & HTA"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/rwe", "Real-World Evidence"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_rwe.py" in txt:
        return False
    line = "python3 pipeline/build_rwe.py site/data\n"
    if "build_global_search.py" in txt:
        txt = txt.replace("python3 pipeline/build_global_search.py", line + "python3 pipeline/build_global_search.py", 1)
    else:
        txt = txt + ("" if txt.endswith("\n") else "\n") + line
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/rwe"' in txt:
        return False
    route = (
        '\n@app.get("/api/rwe")\n'
        'def api_rwe():\n'
        '    p = DATA_DIR / "rwe.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "rwe.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rwe.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    rwe_ref = _load(data_dir / "rwe.json", {}) or {}\n'
        '    for sec_key, sec_q in [("rwd_sources", "sources"), ("rwe_regulatory", "regulatory"), ("study_designs", "designs"), ("rwe_networks", "networks")]:\n'
        '        for item in (rwe_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "rwe",\n'
        '                "group": "Real-World Evidence",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/rwe?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/rwe?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"real world evidence RWE RWD EHR claims registry OMOP DARWIN EU Sentinel target trial {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rwe", "#/ref/rwe"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    rwe_doc = _load_json(data_dir / "rwe.json")\n'
        '    if isinstance(rwe_doc, dict) and rwe_doc.get("rwd_sources"):\n'
        '        rwe_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (rwe_doc.get("rwd_sources") or []) + (rwe_doc.get("rwe_regulatory") or []))\n'
        '        pages.append(("rwe", "#/ref/rwe", "Real-World Evidence (RWE) & Post-Market Healthcare Data",\n'
        '                      "Primary-sourced guide to EHRs, claims, registries, FDA 21st Century Cures RWE guidances, target trial emulation, Sentinel, and EMA DARWIN EU.",\n'
        '                      f"<ul>{rwe_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/rwe"' in txt:
        return False
    for anchor in ('    "/#/explore/diagnostics",', '    "/#/explore/global-reg",', '    "/#/explore/sterile",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/rwe",\n    "/#/explore/rwe",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_rwe_py": _write_if_changed(pipe_dir / "build_rwe.py", BUILD_RWE_PY),
        "rwe_js": _write_if_changed(js_dir / "rwe.js", RWE_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/diagnostics") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/diagnostics", "Diagnostics & CDx"]] }];\nconst EXPLORE_NAV = [["#/explore/diagnostics", "Diagnostics & CDx"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/diagnostics",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_rwe.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_rwe.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"rwd_sources": 6, "rwe_regulatory": 6, "study_designs": 6, "rwe_networks": 6}, out

        doc = json.loads((root / "site" / "data" / "rwe.json").read_text(encoding="utf-8"))
        for k in ("rwd_sources", "rwe_regulatory", "study_designs", "rwe_networks"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "rwe.js").read_text(encoding="utf-8")
        print("V61P_REAL_WORLD_EVIDENCE_RWD_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1p Real-World Evidence & RWD patch.")
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
