#!/usr/bin/env python3
"""Pill by Pill v6.2l Patch: Continuous Manufacturing (ICH Q13), Process Analytical Technology (PAT / RTRT), FDA ETP / AMT / FRAME & AI in Drug Manufacturing Reference (#/ref/continuous-pat-ai, #/explore/continuous-pat-ai, /api/continuous-pat-ai).

1. Adds `pipeline/build_continuous_pat_ai_mfg.py` -> `site/data/continuous_pat_ai_mfg.json`
   (6 ICH Q13 Continuous Manufacturing pillars, 6 PAT & Real-Time Release Testing pillars, 6 FDA
   ETP / AMT / FRAME pillars, and 6 AI in Drug Manufacturing & Distributed Mfg pillars — 24
   primary-sourced entries).
2. Adds `site/js/continuous_pat_ai_mfg.js` (`continuousPatAiMfgPage` with inline Continuous Mfg,
   PAT & AI Mfg SVG + 4 section filters) and wires `#/ref/continuous-pat-ai`,
   `#/explore/continuous-pat-ai`, `/api/continuous-pat-ai`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `continuous_pat_ai_mfg.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/continuous-pat-ai/` static SEO page + sitemap entry ->
   54 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py --selftest
  python3 2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_CONTINUOUS_PAT_AI_MFG_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2l Continuous Manufacturing (ICH Q13), PAT, ETP/AMT & AI Manufacturing Reference (`site/data/continuous_pat_ai_mfg.json`).

Comprehensive, primary-sourced reference covering:
  1. ICH Q13 Continuous Manufacturing of Drug Substances & Drug Products (6 pillars)
  2. Process Analytical Technology (PAT) & Real-Time Release Testing (RTRT) (6 pillars)
  3. FDA Emerging Technology Program (ETP), AMT & FRAME (6 pillars)
  4. AI in Drug Manufacturing & Distributed / Point-of-Care Mfg (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER OPQ, ICH).

Usage:
  python3 pipeline/build_continuous_pat_ai_mfg.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

ICH_Q13_CONTINUOUS = [
    {
        "id": "cpm-q13-final-2023",
        "name": "ICH Q13 Continuous Manufacturing of Drug Substances & Drug Products",
        "category": "ICH Q13 Final",
        "plain": "Instead of making pills in separate start-and-stop batches, continuous manufacturing feeds powder in one end and presses finished tablets non-stop.",
        "technical": "FDA's March 2023 ICH Q13 Final Guidance harmonizes scientific and regulatory expectations for continuous manufacturing (CM) development, control strategy, validation, and lifecycle management.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q13-continuous-manufacturing-drug-substances-and-drug-products",
    },
    {
        "id": "cpm-q13-rtd-control",
        "name": "Residence Time Distribution (RTD) & Material Diversion",
        "category": "Process Dynamics",
        "plain": "Sensors track exactly how long every gram of powder spends inside a continuous mixer so any brief hiccup can be diverted without scrapping the whole run.",
        "technical": "ICH Q13 requires Residence Time Distribution (RTD) characterization, material traceability, and automated diversion gates to isolate transient disturbances while maintaining a state of control.",
        "url": "https://www.fda.gov/media/174250/download",
    },
    {
        "id": "cpm-q13-batch-def",
        "name": "Continuous Batch Definition & Flexible Scale-Out",
        "category": "21 CFR 210.3 Batch",
        "plain": "In continuous manufacturing, a 'batch' can be defined by run time or total kilograms produced—making it easy to scale up simply by running longer.",
        "technical": "ICH Q13 permits defining CM batch size by output quantity, input material quantity, or run duration—enabling scale-up via extended run time, mass-flow rate adjustment, or equipment duplication.",
        "url": "https://www.fda.gov/media/167327/download",
    },
    {
        "id": "cpm-q13-annexes-ds-dp",
        "name": "ICH Q13 Annexes: Small-Molecule DS, Solid Oral DP & Biologics",
        "category": "Modality Scope",
        "plain": "Continuous manufacturing works across chemical synthesis reactors, tablet presses, and even continuous perfusion bioreactors for biologic antibodies.",
        "technical": "ICH Q13 Annexes I–V provide concrete implementation models for small-molecule APIs, solid oral dosage forms, therapeutic proteins (perfusion), integrated DS/DP lines, and disturbance management.",
        "url": "https://www.fda.gov/media/167327/download",
    },
    {
        "id": "cpm-q13-disturbance",
        "name": "Transient Disturbance Management & State of Control",
        "category": "Control Strategy",
        "plain": "If a feeder momentarily drifts out of range, automated software calculates which tablets were affected and ejects only those seconds of output.",
        "technical": "Under ICH Q13, integrated control strategies combine feed-forward/feed-back loops, RTD-linked diversion logic, and multivariate monitoring to prove continuous state of control.",
        "url": "https://www.fda.gov/media/165775/download",
    },
    {
        "id": "cpm-adv-mfg-mcm",
        "name": "FDA Advanced Manufacturing for Supply & Medical Countermeasures",
        "category": "National Resilience",
        "plain": "Compact continuous-flow factories can be built faster and shifted between medicines during emergencies, reducing reliance on fragile overseas supply chains.",
        "technical": "FDA's Advanced Manufacturing program highlights continuous manufacturing, 3D printing, and modular facilities as core pillars for domestic surge capacity and supply resilience.",
        "url": "https://www.fda.gov/emergency-preparedness-and-response/medical-countermeasure-mcm-issues/advanced-manufacturing",
    },
]

PAT_RTRT_ANALYTICS = [
    {
        "id": "cpm-pat-framework",
        "name": "FDA PAT Framework: Designing, Analyzing & Controlling Manufacturing",
        "category": "2004 PAT Guidance",
        "plain": "Process Analytical Technology (PAT) puts smart optical and chemical sensors right inside mixers and tablet presses so quality is measured live—not days later in a lab.",
        "technical": "FDA's PAT Guidance establishes a risk-based framework for in-line, on-line, and at-line chemical, physical, and microbiological measurements integrated with multivariate process control.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pat-framework-innovative-pharmaceutical-development-manufacturing-and-quality-assurance",
    },
    {
        "id": "cpm-rtrt-211-165",
        "name": "Real-Time Release Testing (RTRT) Under 21 CFR 211.165",
        "category": "Automated Release",
        "plain": "Instead of waiting weeks for destructive lab assays on finished bottles, RTRT releases batches immediately using validated in-process sensor data.",
        "technical": "Real-Time Release Testing (RTRT) satisfies 21 CFR 211.165 finished-product testing by combining process understanding, control strategies, and continuous in-line CQA measurements.",
        "url": "https://www.fda.gov/media/71012/download",
    },
    {
        "id": "cpm-pat-raman-bioreactor",
        "name": "Inline Raman Spectroscopy in Bioreactor Upstream Control",
        "category": "Biologics PAT",
        "plain": "Laser-based Raman probes dip into living cell bioreactors to monitor sugar and protein glycosylation continuously so batches stay on target.",
        "technical": "FDA/URI regulatory science demonstrates PLS-modeled inline Raman spectroscopy for real-time glucose/lactate feedback control in biologics bioreactors, preventing glycosylation drift.",
        "url": "https://www.fda.gov/media/169133/download",
    },
    {
        "id": "cpm-pat-wnmr-noninvasive",
        "name": "Noninvasive Water Proton NMR (wNMR) for Vial & Syringe Inspection",
        "category": "CERSI Research",
        "plain": "Tabletop wNMR scanners inspect sealed vaccine vials and biologics syringes without opening or wasting a single dose.",
        "technical": "FDA–University of Maryland CERSI research evaluates noninvasive tabletop water proton NMR (wNMR) to verify suspension settling, reconstitution, and brand/biosimilar consistency through intact glass.",
        "url": "https://www.fda.gov/science-research/advancing-regulatory-science/noninvasive-process-analytical-technology-pat-manufacturing-automation",
    },
    {
        "id": "cpm-q8-q9-q10-control",
        "name": "ICH Q8/Q9/Q10 Control Strategy & Design Space Integration",
        "category": "Quality by Design",
        "plain": "Quality by Design maps out a safe operating 'Design Space' during R&D so factories can adjust parameters smoothly without needing new FDA approvals.",
        "technical": "FDA's ICH Q8/Q9/Q10 Q&A connects Design Space boundaries, Control Strategy refinement, and RTRT deployment across clinical-to-commercial pharmaceutical lifecycles.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8-q9-q10-questions-and-answers-appendix-qas-training-sessions-q8-q9-q10-points-consider",
    },
    {
        "id": "cpm-pat-built-in-quality",
        "name": "Built-In Quality & Continuous Process Verification (CPV)",
        "category": "Stage 3 Validation",
        "plain": "Quality cannot be tested into a pill at the end—continuous sensor streams prove every single batch meets specs during production.",
        "technical": "PAT-enabled Continuous Process Verification (CPV) uses real-time sensor streams and multivariate control charts so production batch data continuously verifies process validation.",
        "url": "https://www.fda.gov/media/71012/download",
    },
]

ETP_AMT_FRAME = [
    {
        "id": "cpm-etp-program",
        "name": "CDER Emerging Technology Program (ETP) & ETT",
        "category": "OPQ Innovation",
        "plain": "Drugmakers inventing radically new factory tech can meet early with FDA's Emerging Technology Team to solve regulatory questions before filing.",
        "technical": "Created within CDER OPQ, the Emerging Technology Program (ETP) pairs sponsors with cross-functional FDA CMC and OII inspection experts early in development to de-risk novel manufacturing.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/emerging-technology-program-etp",
    },
    {
        "id": "cpm-amt-designation",
        "name": "Advanced Manufacturing Technologies (AMT) Designation (FDORA § 3213)",
        "category": "Statutory Designation",
        "plain": "FDA's AMT Designation gives companies using breakthrough manufacturing methods prioritized agency interactions and faster review of factory upgrades.",
        "technical": "Implementing FDORA § 3213 (FD&C Act § 506L), FDA's AMT Designation Program grants prioritized review and early engagement for novel manufacturing methods improving quality or supply reliability.",
        "url": "https://www.fda.gov/media/174651/download",
    },
    {
        "id": "cpm-frame-initiative",
        "name": "CDER FRAME Initiative (Framework for Advanced Manufacturing Evaluation)",
        "category": "Policy Modernization",
        "plain": "FDA's FRAME initiative updates decades-old factory inspection rules so they fit AI controls, 3D printing, and portable modular drug units.",
        "technical": "CDER's FRAME Initiative aligns 21 CFR 211 cGMP regulations, ICH guidelines, and establishment registration rules for continuous, distributed, point-of-care, and AI-enabled manufacturing.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/cders-framework-regulatory-advanced-manufacturing-evaluation-frame-initiative",
    },
    {
        "id": "cpm-etp-graduated",
        "name": "Graduated ETP Technologies (Continuous Oral Solid & Bioprocessing)",
        "category": "Proven Tech",
        "plain": "Once an emerging technology like continuous tablet compression becomes routine at FDA, it 'graduates' from ETP into standard review.",
        "technical": "CDER tracks technologies that have graduated from ETP into routine OPQ assessment—such as continuous direct compression, continuous hot-melt extrusion, and automated aseptic isolators.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/graduated-etp-technology",
    },
    {
        "id": "cpm-etp-examples",
        "name": "Accepted Emerging Technologies: 3D Printing, Modular & End-to-End CM",
        "category": "Accepted Modalities",
        "plain": "FDA has already accepted 3D-printed fast-dissolving tablets, portable pharmacy-on-a-chip units, and continuous biologics purification into ETP.",
        "technical": "Accepted ETP proposals span 3D binder-jet printing, continuous API-to-tablet lines, closed robotic aseptic filling, and continuous chromatography/viral-inactivation skids.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/examples-accepted-emerging-technologies",
    },
    {
        "id": "cpm-etp-participate",
        "name": "How to Participate in CDER ETP (Pre-Submission Engagement)",
        "category": "Sponsor Onboarding",
        "plain": "Companies submit a brief 5-page technical proposal to join ETP—even before picking a specific drug product.",
        "technical": "Sponsors and technology vendors apply to ETP via CDER-ETT@fda.hhs.gov with a concise description of the novel technology, quality/supply benefits, and development timeline.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/how-participate-emerging-technology-program-etp",
    },
]

AI_DIGITAL_MFG = [
    {
        "id": "cpm-ai-mfg-paper",
        "name": "FDA Discussion Paper: Artificial Intelligence in Drug Manufacturing (2023)",
        "category": "AI in cGMP",
        "plain": "FDA mapped how AI models can predict equipment failures, inspect vials with computer vision, and dynamically tune continuous manufacturing lines.",
        "technical": "CDER's AI in Drug Manufacturing Discussion Paper examines cGMP cloud/edge digital infrastructure, model lifecycle governance (ICH Q9(R1)/Q12), continuous learning vs. locked models, and human-in-the-loop oversight.",
        "url": "https://www.fda.gov/media/165743/download",
    },
    {
        "id": "cpm-ai-drug-dev-hub",
        "name": "CDER Artificial Intelligence for Drug Development & Manufacturing Hub",
        "category": "CDER AI Portal",
        "plain": "FDA's central AI portal connects guidance on AI in clinical trials, drug discovery, and automated factory quality control.",
        "technical": "CDER's AI Hub coordinates policy across AI/ML in Drug Development (revised Feb 2025) and AI in Drug Manufacturing under the FRAME digital-infrastructure roadmap.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/artificial-intelligence-drug-development",
    },
    {
        "id": "cpm-ai-ml-discussion",
        "name": "Using AI & ML Across the Drug & Biologic Product Lifecycle",
        "category": "Lifecycle AI/ML",
        "plain": "Machine learning helps pharma from molecule screening and trial recruitment all the way to predictive factory maintenance and safety monitoring.",
        "technical": "FDA's AI/ML Lifecycle Discussion Paper establishes risk-based credibility, data provenance, bias mitigation, and transparency principles spanning discovery, clinical trials, and manufacturing.",
        "url": "https://www.fda.gov/media/167973/download",
    },
    {
        "id": "cpm-ai-publications",
        "name": "FDA AI Regulatory Science Publications & Workshops",
        "category": "Research Index",
        "plain": "FDA publishes regular workshops and technical papers with industry on validating AI models used in medicine.",
        "technical": "FDA's AI Publications registry indexes cross-center (CDER, CBER, CDRH) discussion papers, Good Machine Learning Practice (GMLP) principles, and PQRI manufacturing workshops.",
        "url": "https://www.fda.gov/science-research/artificial-intelligence-and-medical-products/artificial-intelligence-fda-publications",
    },
    {
        "id": "cpm-distributed-poc",
        "name": "Distributed Manufacturing & Point-of-Care (POC) Drug Production",
        "category": "Modular / Bedside",
        "plain": "Portable, automated mini-factories could one day compound personalized medicines or cell therapies right inside hospital pharmacies under central Quality oversight.",
        "technical": "Under FRAME, FDA is modernizing establishment registration and 21 CFR 211.110 controls for Distributed Manufacturing (DM) mobile units and hospital Point-of-Care (POC) manufacturing systems.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/cders-framework-regulatory-advanced-manufacturing-evaluation-frame-initiative",
    },
    {
        "id": "cpm-fda-roundup-q13-ai",
        "name": "Synchronized 2023 Milestone: ICH Q13 Final + AI Manufacturing Paper",
        "category": "Digital Transformation",
        "plain": "In March 2023, FDA paired final continuous manufacturing rules with its AI manufacturing paper to usher in Pharma 4.0.",
        "technical": "FDA's coordinated March 2023 release of ICH Q13 Final Guidance and the AI in Drug Manufacturing Discussion Paper established the regulatory foundation for Industry 4.0 pharma operations.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-roundup-march-3-2023",
    },
]


def build_continuous_pat_ai_mfg(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "ich_q13_continuous": len(ICH_Q13_CONTINUOUS),
            "pat_rtrt_analytics": len(PAT_RTRT_ANALYTICS),
            "etp_amt_frame": len(ETP_AMT_FRAME),
            "ai_digital_mfg": len(AI_DIGITAL_MFG),
        },
        "ich_q13_continuous": ICH_Q13_CONTINUOUS,
        "pat_rtrt_analytics": PAT_RTRT_ANALYTICS,
        "etp_amt_frame": ETP_AMT_FRAME,
        "ai_digital_mfg": AI_DIGITAL_MFG,
    }
    (data_dir / "continuous_pat_ai_mfg.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_continuous_pat_ai_mfg.py <site/data>")
    print(json.dumps(build_continuous_pat_ai_mfg(pathlib.Path(sys.argv[1])), indent=2))
'''

CONTINUOUS_PAT_AI_MFG_JS = '''// Pill by Pill v6.2l: Continuous Manufacturing (ICH Q13), PAT / RTRT, FDA ETP / AMT / FRAME & AI in Drug Manufacturing Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["q13", "ICH Q13 Continuous Mfg", "ich_q13_continuous"],
  ["pat", "PAT & Real-Time Release", "pat_rtrt_analytics"],
  ["etp", "ETP, AMT & FRAME", "etp_amt_frame"],
  ["aimfg", "AI & Distributed Mfg", "ai_digital_mfg"],
];

function continuousPatAiMfgSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Pharma 4.0 manufacturing: ICH Q13 Continuous Manufacturing, PAT and Real-Time Release, FDA ETP and AMT, and AI and Distributed Manufacturing">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. ICH Q13 CM</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">RTD &amp; Diversion Gates</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Continuous DS &amp; DP</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cpm-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. PAT &amp; RTRT</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Inline Raman &amp; wNMR</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR 211.165 Release</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cpm-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. ETP &amp; AMT</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">FDORA §506L &amp; FRAME</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">3D Print &amp; Modular</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cpm-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. AI &amp; POC Mfg</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Predictive cGMP &amp; Vision</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Distributed / Bedside</text>
      <defs><marker id="cpm-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Pharma 4.0 manufacturing unites ICH Q13 continuous lines, inline PAT/RTRT sensors, FDA ETP/AMT/FRAME pathways, and AI-enabled distributed production.</figcaption>
  </figure>`;
}

export async function continuousPatAiMfgPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/continuous_pat_ai_mfg.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/continuous-pat-ai" : "#/ref/continuous-pat-ai";

  const pills = html`<div class="chips" role="navigation" aria-label="Continuous manufacturing, PAT, ETP, and AI manufacturing sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Program</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${continuousPatAiMfgSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA ICH Q13, PAT/RTRT, CDER Emerging Technology Program (ETP) / AMT / FRAME, and AI in Drug Manufacturing documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Continuous Mfg (Q13), PAT, ETP & AI Mfg"]] : [REF_HOME, ["Continuous Mfg (Q13), PAT, ETP & AI Mfg"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Continuous Manufacturing (ICH Q13), PAT, ETP & AI Manufacturing",
      lede: env === "explore"
        ? "How modern drug factories run non-stop continuous lines, inspect pills live with laser sensors, and use AI and 3D printing to make medicines faster."
        : "ICH Q13 continuous manufacturing (RTD/diversion/batch definition), PAT & 21 CFR 211.165 RTRT, CDER ETP / FDORA AMT / FRAME, and AI/Distributed Manufacturing.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on continuous manufacturing, PAT, ETP, and AI.", href: env === "explore" ? "#/ref/continuous-pat-ai" : "#/explore/continuous-pat-ai" },
        { title: "Sterile Mfg & Bioprocessing", text: "Annex 1 cleanrooms, isolators, and single-use bioprocessing.", href: "#/ref/sterile-mfg" },
        { title: "Drug Shortages & Onshoring", text: "How AMT and continuous flow chemistry strengthen domestic supply.", href: "#/ref/shortages-resilience" },
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
    if 'continuous_pat_ai_mfg.js' not in txt:
        for anchor in ('import * as pfddCoaExpandedAccess from "./pfdd_coa_expanded_access.js";\n', 'import * as rmatHctpCgtCmc from "./rmat_hctp_cgt_cmc.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as continuousPatAiMfg from "./continuous_pat_ai_mfg.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as continuousPatAiMfg from "./continuous_pat_ai_mfg.js";\n' + txt
            changed = True
    if '"/ref/continuous-pat-ai"' not in txt:
        for anchor in ('if (path === "/ref/pfdd-coa-expanded-access")', 'if (path === "/ref/rmat-hctp-cgt-cmc")', 'if (path === "/ref/sterile-mfg")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/continuous-pat-ai") return { env: "ref", current: "#/ref/continuous-pat-ai", ...(await continuousPatAiMfg.continuousPatAiMfgPage(query, "ref")) };\n  if (path === "/explore/continuous-pat-ai") return { env: "explore", current: "#/explore/continuous-pat-ai", ...(await continuousPatAiMfg.continuousPatAiMfgPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/continuous-pat-ai" not in txt:
        for anchor in ('["#/ref/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]', '["#/ref/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/continuous-pat-ai", "Continuous mfg, PAT & AI"]', 1)
                changed = True
                break
    if "#/explore/continuous-pat-ai" not in txt:
        for anchor in ('["#/explore/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]', '["#/explore/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/continuous-pat-ai", "Continuous mfg, PAT & AI"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_continuous_pat_ai_mfg.py" in txt:
        return False
    line = "python3 pipeline/build_continuous_pat_ai_mfg.py site/data\n"
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
    if '"/api/continuous-pat-ai"' in txt:
        return False
    route = (
        '\n@app.get("/api/continuous-pat-ai")\n'
        'def api_continuous_pat_ai():\n'
        '    p = DATA_DIR / "continuous_pat_ai_mfg.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "continuous_pat_ai_mfg.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"continuous_pat_ai_mfg.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    cpm_ref = _load(data_dir / "continuous_pat_ai_mfg.json", {}) or {}\n'
        '    for sec_key, sec_q in [("ich_q13_continuous", "q13"), ("pat_rtrt_analytics", "pat"), ("etp_amt_frame", "etp"), ("ai_digital_mfg", "aimfg")]:\n'
        '        for item in (cpm_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "continuous_pat_ai_mfg",\n'
        '                "group": "Continuous Mfg (ICH Q13), PAT, ETP & AI Mfg",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/continuous-pat-ai?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/continuous-pat-ai?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"continuous manufacturing ICH Q13 RTD diversion PAT process analytical technology RTRT real time release Raman wNMR ETP emerging technology AMT FRAME AI drug manufacturing distributed POC {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"continuous-pat-ai", "#/ref/continuous-pat-ai"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    cpm_doc = _load_json(data_dir / "continuous_pat_ai_mfg.json")\n'
        '    if isinstance(cpm_doc, dict) and cpm_doc.get("ich_q13_continuous"):\n'
        '        cpm_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (cpm_doc.get("ich_q13_continuous") or []) + (cpm_doc.get("pat_rtrt_analytics") or []))\n'
        '        pages.append(("continuous-pat-ai", "#/ref/continuous-pat-ai", "Continuous Manufacturing (ICH Q13), PAT, ETP & AI Manufacturing",\n'
        '                      "Primary-sourced guide to ICH Q13 continuous manufacturing, PAT & RTRT, CDER ETP / AMT / FRAME, and AI in drug manufacturing.",\n'
        '                      f"<ul>{cpm_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/continuous-pat-ai"' in txt:
        return False
    for anchor in ('    "/#/explore/pfdd-coa-expanded-access",', '    "/#/explore/rmat-hctp-cgt-cmc",', '    "/#/explore/adcs-bispecifics-oligos",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/continuous-pat-ai",\n    "/#/explore/continuous-pat-ai",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_continuous_pat_ai_mfg_py": _write_if_changed(pipe_dir / "build_continuous_pat_ai_mfg.py", BUILD_CONTINUOUS_PAT_AI_MFG_PY),
        "continuous_pat_ai_mfg_js": _write_if_changed(js_dir / "continuous_pat_ai_mfg.js", CONTINUOUS_PAT_AI_MFG_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/pfdd-coa-expanded-access") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]] }];\nconst EXPLORE_NAV = [["#/explore/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/pfdd-coa-expanded-access",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_continuous_pat_ai_mfg.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_continuous_pat_ai_mfg.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ich_q13_continuous": 6, "pat_rtrt_analytics": 6, "etp_amt_frame": 6, "ai_digital_mfg": 6}, out

        doc = json.loads((root / "site" / "data" / "continuous_pat_ai_mfg.json").read_text(encoding="utf-8"))
        for k in ("ich_q13_continuous", "pat_rtrt_analytics", "etp_amt_frame", "ai_digital_mfg"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "continuous_pat_ai_mfg.js").read_text(encoding="utf-8")
        print("V62L_CONTINUOUS_PAT_AI_MFG_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2l Continuous Mfg (ICH Q13), PAT, ETP & AI Mfg patch.")
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
