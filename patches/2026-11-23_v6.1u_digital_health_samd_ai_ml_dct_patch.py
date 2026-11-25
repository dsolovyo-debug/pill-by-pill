#!/usr/bin/env python3
"""Pill by Pill v6.1u Patch: Digital Health, AI/ML SaMD, PCCPs, PDURS & Decentralized Clinical Trials Reference (#/ref/digital-health, #/explore/digital-health, /api/digital-health).

1. Adds `pipeline/build_digital_health.py` -> `site/data/digital_health.json` (6 SaMD & AI/ML
   device pillars, 6 Predetermined Change Control Plan (PCCP) & lifecycle pillars, 6 PDURS &
   drug-companion software pillars, and 6 Decentralized Clinical Trial (DCT) & DHT pillars — 24
   primary-sourced entries).
2. Adds `site/js/digital_health.js` (`digitalHealthPage` with inline Digital Health & AI/ML
   Lifecycle SVG + 4 section filters) and wires `#/ref/digital-health`, `#/explore/digital-health`,
   `/api/digital-health`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `digital_health.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/digital-health/` static SEO page + sitemap entry -> 37
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py --selftest
  python3 2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_DIGITAL_HEALTH_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1u Digital Health, AI/ML SaMD, PCCPs, PDURS & Decentralized Clinical Trials Reference (`site/data/digital_health.json`).

Comprehensive, primary-sourced reference covering:
  1. Software as a Medical Device (SaMD) & AI/ML Oversight (6 pillars)
  2. Predetermined Change Control Plans (PCCPs) & Adaptive AI (6 pillars)
  3. Prescription Drug Use-Related Software (PDURS) & Combination Apps (6 pillars)
  4. Decentralized Clinical Trials (DCTs) & Digital Health Technologies (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDRH Digital Health Center of Excellence, CDER OMP, FD&C Act § 515C).

Usage:
  python3 pipeline/build_digital_health.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

SAMD_AIML = [
    {
        "id": "dh-samd-def",
        "name": "Software as a Medical Device (SaMD — IMDRF & FDA Definition)",
        "domain": "Standalone Software",
        "plain": "Software that diagnoses, monitors, or treats a medical condition on its own—running on a phone, PC, or cloud server without needing custom hardware—is regulated as a medical device.",
        "technical": "Defined by IMDRF and FDA as software intended for one or more medical purposes without being part of a hardware medical device; distinct from SiMD (Software in a Medical Device) and manufacturing/maintenance software.",
        "url": "https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd",
    },
    {
        "id": "dh-imdrf-risk",
        "name": "IMDRF 4-Tier SaMD Risk Categorization (Categories I–IV)",
        "domain": "Risk Classification",
        "plain": "Health software is graded from low risk (Category I) to critical (Category IV) based on how serious the illness is and whether the app merely informs a doctor or drives immediate treatment.",
        "technical": "Crosses Healthcare Situation (Critical / Serious / Non-serious) with Significance of Information (Treat/Diagnose, Drive clinical management, Inform clinical management) to calibrate QMS and premarket review rigor.",
        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/global-approach-software-medical-device",
    },
    {
        "id": "dh-aiml-devices",
        "name": "AI/ML-Enabled Medical Devices Registry & Transparency",
        "domain": "CDRH Digital Health",
        "plain": "FDA maintains a public directory of more than a thousand authorized AI and machine-learning medical tools—mostly in radiology, cardiology, and pathology.",
        "technical": "FDA Digital Health Center of Excellence tracks AI/ML-enabled devices cleared/approved via 510(k), De Novo, and PMA, emphasizing Good Machine Learning Practice (GMLP), bias mitigation, and real-world performance monitoring.",
        "url": "https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices",
    },
    {
        "id": "dh-aiml-drug-dev",
        "name": "AI & Machine Learning in Drug & Biological Product Development",
        "domain": "CDER / CBER / OCP",
        "plain": "Beyond hospital apps, pharma companies use AI to design molecules, predict toxicity, pick clinical trial sites, and monitor factory quality—with FDA issuing cross-center guidance.",
        "technical": "CDER, CBER, CDRH, and OCP coordinate risk-based credibility assessment for AI/ML models used across discovery, PK/PD modeling, clinical trial enrichment, pharmacovigilance, and advanced manufacturing (FRAME).",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-medical-policy",
    },
    {
        "id": "dh-estar",
        "name": "Electronic Submission Template for Medical Devices (eSTAR)",
        "domain": "510(k) / De Novo",
        "plain": "All standard US 510(k) device and software submissions now use FDA's interactive electronic eSTAR template so reviewers get complete, structured files from day one.",
        "technical": "Mandatory interactive PDF/XML submission template for 510(k)s (since Oct 2023) standardizing software architecture, cybersecurity, interoperability, and clinical/analytical performance sections.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-roundup-september-19-2023",
    },
    {
        "id": "dh-cybersecurity",
        "name": "Medical Device Cybersecurity, SBOM & Patch Management",
        "domain": "Connected Safety",
        "plain": "Connected insulin pumps, pacemakers, and cloud diagnostic apps must include a 'Software Bill of Materials' and rapid security-patching plans to protect patients from cyberattacks.",
        "technical": "FD&C Act § 524B (refuse-to-accept authority for cyber devices) requires secure-by-design architecture, Software Bill of Materials (SBOM), and coordinated vulnerability disclosure/patching across product lifecycles.",
        "url": "https://www.fda.gov/medical-devices",
    },
]

PCCP_LIFECYCLE = [
    {
        "id": "pccp-515c",
        "name": "Predetermined Change Control Plans (PCCPs — FD&C Act § 515C)",
        "domain": "Statutory Authority",
        "plain": "Normally, updating an AI medical tool requires a whole new FDA review; a PCCP lets developers get future algorithm updates pre-approved upfront as part of the original clearance.",
        "technical": "Section 515C of the FD&C Act authorizes FDA to approve a Predetermined Change Control Plan inside a 510(k), De Novo, or PMA so specified post-market modifications can be deployed without new marketing submissions.",
        "url": "https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/predetermined-change-control-plans",
    },
    {
        "id": "pccp-aiml-guidance",
        "name": "Marketing Submission Recommendations for AI-Enabled Device PCCPs",
        "domain": "AI/ML Updates",
        "plain": "An AI PCCP spells out three things before launch: what the model is allowed to change, how the team will test and validate the update, and how they will measure patient impact.",
        "technical": "Final/Draft PCCP framework requires: (1) Description of Modifications (locked vs. automatic updates), (2) Modification Protocol (data management, retraining, performance evaluation, update procedures), and (3) Impact Assessment.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence",
    },
    {
        "id": "pccp-general-devices",
        "name": "PCCPs for Hardware & Combination Medical Devices (Aug 2024)",
        "domain": "Broad Device Scope",
        "plain": "Predetermined Change Control Plans aren't just for AI—they also cover planned sensor, software, and device-led combination product upgrades.",
        "technical": "FDA August 2024 Draft Guidance extends PCCP recommendations across 510(k), De Novo, and PMA medical devices, including device-led combination products, without altering intended use.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-medical-devices",
    },
    {
        "id": "pccp-guiding-principles",
        "name": "FDA / Health Canada / MHRA Joint PCCP Guiding Principles",
        "domain": "International Alignment",
        "plain": "US, Canadian, and UK regulators published five shared rules so AI health tools can stay safe and transparent when updated across borders.",
        "technical": "Five joint guiding principles (Oct 2023): Focused & Bounded, Risk-Based, Evidence-Based, Transparent to users, and Total Product Lifecycle (TPLC) perspective.",
        "url": "https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/predetermined-change-control-plans-machine-learning-enabled-medical-devices-guiding-principles",
    },
    {
        "id": "pccp-intended-use",
        "name": "Boundary Between Pre-Authorized PCCP & New Intended Use",
        "domain": "Regulatory Guardrail",
        "plain": "An AI update can sharpen accuracy or work on new scanner brands under a PCCP, but if it starts predicting a brand-new disease, it still needs a fresh FDA review.",
        "technical": "Modifications that alter the device's indications for use or introduce significantly different clinical risks fall outside an authorized PCCP and require a new 510(k), De Novo, or PMA supplement.",
        "url": "https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/predetermined-change-control-plans",
    },
    {
        "id": "pccp-transparency",
        "name": "Public Labeling & User Notification of AI Updates",
        "domain": "Clinical Trust",
        "plain": "Doctors and hospitals must be told when an AI tool updates under a PCCP, including what changed and how the updated model performed.",
        "technical": "PCCP update procedures require transparent release notes, versioned labeling, performance monitoring plans, and rollback mechanisms if real-world drift degrades clinical performance.",
        "url": "https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/predetermined-change-control-plans-machine-learning-enabled-medical-devices-guiding-principles",
    },
]

PDURS_COMBO = [
    {
        "id": "pdurs-guidance",
        "name": "Prescription Drug Use-Related Software (PDURS — Final Guidance)",
        "domain": "Drug-Companion Apps",
        "plain": "When a pharma company builds a mobile app to go alongside its prescription drug—like tracking asthma inhalations or reminding patients how to titrate doses—FDA treats the app's output as drug labeling.",
        "technical": "Applies FDA drug labeling authorities to sponsor-disseminated software producing end-user outputs that supplement, explain, or textually relate to a prescription drug, regardless of whether the software is also a medical device.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/regulatory-considerations-prescription-drug-use-related-software",
    },
    {
        "id": "pdurs-device-connected",
        "name": "Device-Connected vs. Standalone Drug Software Functions",
        "domain": "Software Taxonomy",
        "plain": "Smart inhalers and connected auto-injector pens send real dosing data to an app (device-connected), whereas symptom e-diaries rely on what the patient types in (standalone).",
        "technical": "Distinguishes device-connected software functions (relying on data from a combination product's device constituent part) from standalone functions (relying on user-entered data); only functions essential to safe/effective use or showing meaningful clinical outcome improvement belong in the Prescribing Information (PI).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/regulatory-considerations-prescription-drug-use-related-software",
    },
    {
        "id": "pdurs-promo-labeling",
        "name": "Promotional Labeling vs. FDA-Required Prescribing Information",
        "domain": "CDER OPDP Review",
        "plain": "Most companion medication apps count as promotional labeling submitted at launch rather than requiring a formal drug-label rewrite—unless the drug cannot be used safely without the app.",
        "technical": "Standalone PDURS outputs are generally regulated as promotional labeling (submitted on Form FDA 2253 at initial dissemination), whereas device-connected or clinical-outcome-enhancing functions may be incorporated into FDA-required labeling (PI/IFU).",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-medical-policy",
    },
    {
        "id": "pdurs-pdt",
        "name": "Prescription Digital Therapeutics (PDTs) & Software-Delivered Therapy",
        "domain": "Software as Therapy",
        "plain": "Some smartphone apps don't just track pills—they deliver clinically proven behavioral or cognitive therapy by prescription for insomnia, substance use, or ADHD.",
        "technical": "Cleared/authorized by CDRH (De Novo or 510(k)) as SaMD based on randomized controlled trial endpoints; may be prescribed standalone or alongside pharmacotherapy.",
        "url": "https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd",
    },
    {
        "id": "pdurs-smart-devices",
        "name": "Smart Inhalers, Connected Auto-Injectors & Digital Pills",
        "domain": "Drug–Device Combinations",
        "plain": "Sensors built into inhalers, injection pens, and blister packs can confirm when a dose was taken—helping doctors spot adherence gaps before raising a patient's dose.",
        "technical": "Drug-led combination products (21 CFR Part 4) pairing CDER/CBER pharmaceuticals with embedded electronics/Bluetooth telemetry; generic ANDA applicants must assess sameness impacts when referencing RLD software features.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-medical-policy",
    },
    {
        "id": "pdurs-cds",
        "name": "Clinical Decision Support (CDS) & Non-Device Software Exemptions",
        "domain": "21st Century Cures § 3060",
        "plain": "Simple reference calculators, electronic medical libraries, and wellness step counters are exempt from FDA device regulation, whereas opaque black-box alerts stay regulated.",
        "technical": "Under FD&C Act § 520(o), non-device CDS must allow healthcare professionals to independently review the basis for recommendations without replacing clinical judgment for time-critical decisions.",
        "url": "https://www.fda.gov/medical-devices/digital-health-center-excellence/digital-health-terms",
    },
]

DCT_DHT = [
    {
        "id": "dct-guidance",
        "name": "Decentralized Clinical Trials (DCTs — Sept 2024 Final Guidance)",
        "domain": "Remote Trial Execution",
        "plain": "Instead of forcing patients to drive hours to a research hospital for every checkup, decentralized trials bring visits home via telehealth, local clinics, and direct-to-patient medicine shipping.",
        "technical": "FDA September 2024 Final Guidance outlines protocol design, remote telehealth/home visits, local healthcare provider (HCP) delegation, direct-to-participant investigational product distribution, and safety monitoring plans.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",
    },
    {
        "id": "dct-local-hcp",
        "name": "Delegation to Local Healthcare Providers & Telehealth Visits",
        "domain": "Investigator Oversight",
        "plain": "A participant's neighborhood doctor or visiting nurse can perform routine vitals and blood draws, while specialized trial-trained staff handle protocol-specific assessments.",
        "technical": "Investigators retain responsibility for supervising delegated local HCPs performing routine clinical-practice tasks (without needing Form FDA 1572 listing for routine care), while protocol-unique procedures require trained trial personnel.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",
    },
    {
        "id": "dct-direct-ip",
        "name": "Direct-to-Participant Investigational Product (IP) Shipping",
        "domain": "Clinical Supply Logistics",
        "plain": "Oral pills and self-injected trial medicines can be couriered directly to a volunteer's home with temperature tracking and receipt confirmation.",
        "technical": "Requires documented stability during transit, tamper-evident packaging, participant receipt tracking, and return/disposition accounting under investigator supervision (21 CFR 312.60).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",
    },
    {
        "id": "dct-dht-validation",
        "name": "Digital Health Technologies (DHTs) for Remote Endpoint Capture",
        "domain": "Sensors & Wearables",
        "plain": "Watches, actigraphy sensors, and home spirometers capture continuous movement, heart rhythm, and breathing data in real life—requiring proof the sensor is accurate outside a lab.",
        "technical": "FDA DHT Guidance mandates verification (sensor accuracy/precision), analytical & clinical validation in the target population, usability testing, and end-to-end 21 CFR Part 11 audit trails.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-medical-policy",
    },
    {
        "id": "dct-econsent",
        "name": "Electronic Informed Consent (eConsent) & Remote Verification",
        "domain": "Participant Protection",
        "plain": "Interactive video and tablet consent forms help volunteers understand trial risks clearly at home before signing electronically.",
        "technical": "Complies with 21 CFR Part 11 electronic signatures, 21 CFR Part 50 informed consent elements, identity verification, and IRB oversight of multimedia eConsent materials.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",
    },
    {
        "id": "dct-diversity-access",
        "name": "Expanding Trial Diversity & Reducing Travel Burden",
        "domain": "Equitable Enrollment",
        "plain": "Bringing clinical trials to local communities and homes lets rural patients, caregivers, and working adults join studies that used to be out of reach.",
        "technical": "Supports FDA Diversity Action Plan goals by lowering geographic, mobility, and socioeconomic barriers while controlling measurement variability across remote vs. on-site visits.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",
    },
]


def build_digital_health(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "samd_aiml": len(SAMD_AIML),
            "pccp_lifecycle": len(PCCP_LIFECYCLE),
            "pdurs_combo": len(PDURS_COMBO),
            "dct_dht": len(DCT_DHT),
        },
        "samd_aiml": SAMD_AIML,
        "pccp_lifecycle": PCCP_LIFECYCLE,
        "pdurs_combo": PDURS_COMBO,
        "dct_dht": DCT_DHT,
    }
    (data_dir / "digital_health.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_digital_health.py <site/data>")
    print(json.dumps(build_digital_health(pathlib.Path(sys.argv[1])), indent=2))
'''

DIGITAL_HEALTH_JS = '''// Pill by Pill v6.1u: Digital Health, AI/ML SaMD, PCCPs, PDURS & Decentralized Clinical Trials Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["samd", "SaMD & AI/ML", "samd_aiml"],
  ["pccp", "AI PCCPs & Updates", "pccp_lifecycle"],
  ["pdurs", "Drug Software (PDURS)", "pdurs_combo"],
  ["dct", "Decentralized Trials", "dct_dht"],
];

function digitalHealthSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Digital health, AI/ML medical software, PDURS, and decentralized clinical trial ecosystem">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. SaMD &amp; AI/ML</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">IMDRF Risk Cat I–IV</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">eSTAR &amp; § 524B Cyber</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dh-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Adaptive PCCPs</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">FD&amp;C Act § 515C</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Pre-Authorized Updates</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dh-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Drug Apps (PDURS)</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Device-Connected vs. App</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">PI vs. Promo Labeling</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dh-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Decentralized Trials</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Telehealth &amp; Local HCPs</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">DHTs &amp; Direct-to-Patient</text>
      <defs><marker id="dh-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">FDA digital health oversight spans standalone AI/ML SaMD and § 515C PCCPs to drug-companion apps (PDURS) and decentralized clinical trials.</figcaption>
  </figure>`;
}

export async function digitalHealthPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/digital_health.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/digital-health" : "#/ref/digital-health";

  const pills = html`<div class="chips" role="navigation" aria-label="Digital health sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Framework / Technology</th><th>Domain</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.domain}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${digitalHealthSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Digital Health Center of Excellence, § 515C PCCP, PDURS, and Decentralized Clinical Trials guidances.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Digital Health & AI/ML"]] : [REF_HOME, ["Digital Health & AI/ML"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Digital Health, AI/ML SaMD, PCCPs, PDURS & Decentralized Trials",
      lede: env === "explore"
        ? "How medical AI apps, smart inhalers, and home-based clinical trials are tested, updated safely, and regulated."
        : "IMDRF SaMD risk tiers, AI/ML Predetermined Change Control Plans (§ 515C), PDURS drug-companion software, and FDA Decentralized Clinical Trials.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on digital health and AI/ML.", href: env === "explore" ? "#/ref/digital-health" : "#/explore/digital-health" },
        { title: "Real-World Evidence (RWE) & DHTs", text: "Remote sensor data, EHRs, and target trial emulation.", href: "#/ref/rwe" },
        { title: "Clinical Trial Design & Endpoints", text: "Randomization, adaptive designs, and Phase I–IV endpoints.", href: "#/ref/trials" },
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
    if 'digital_health.js' not in txt:
        for anchor in ('import * as orphan from "./orphan.js";\n', 'import * as vaccines from "./vaccines.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as digitalHealth from "./digital_health.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as digitalHealth from "./digital_health.js";\n' + txt
            changed = True
    if '"/ref/digital-health"' not in txt:
        for anchor in ('if (path === "/ref/orphan")', 'if (path === "/ref/vaccines")', 'if (path === "/ref/biologics")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/digital-health") return { env: "ref", current: "#/ref/digital-health", ...(await digitalHealth.digitalHealthPage(query, "ref")) };\n  if (path === "/explore/digital-health") return { env: "explore", current: "#/explore/digital-health", ...(await digitalHealth.digitalHealthPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/digital-health" not in txt:
        for anchor in ('["#/ref/orphan", "Orphan & pediatric"]', '["#/ref/vaccines", "Vaccines & adjuvants"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/digital-health", "Digital health & AI"]', 1)
                changed = True
                break
    if "#/explore/digital-health" not in txt:
        for anchor in ('["#/explore/orphan", "Orphan & pediatric"]', '["#/explore/vaccines", "Vaccines & adjuvants"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/digital-health", "Digital health & AI"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_digital_health.py" in txt:
        return False
    line = "python3 pipeline/build_digital_health.py site/data\n"
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
    if '"/api/digital-health"' in txt:
        return False
    route = (
        '\n@app.get("/api/digital-health")\n'
        'def api_digital_health():\n'
        '    p = DATA_DIR / "digital_health.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "digital_health.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"digital_health.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    dh_ref = _load(data_dir / "digital_health.json", {}) or {}\n'
        '    for sec_key, sec_q in [("samd_aiml", "samd"), ("pccp_lifecycle", "pccp"), ("pdurs_combo", "pdurs"), ("dct_dht", "dct")]:\n'
        '        for item in (dh_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "digital_health",\n'
        '                "group": "Digital Health & AI/ML",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/digital-health?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/digital-health?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"digital health SaMD AI ML PCCP 515C PDURS prescription drug software decentralized clinical trial DCT DHT eSTAR {sec_key} {item.get(\'name\', \'\')} {item.get(\'domain\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"digital-health", "#/ref/digital-health"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    dh_doc = _load_json(data_dir / "digital_health.json")\n'
        '    if isinstance(dh_doc, dict) and dh_doc.get("samd_aiml"):\n'
        '        dh_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (dh_doc.get("samd_aiml") or []) + (dh_doc.get("dct_dht") or []))\n'
        '        pages.append(("digital-health", "#/ref/digital-health", "Digital Health, AI/ML SaMD, PCCPs, PDURS & Decentralized Trials",\n'
        '                      "Primary-sourced guide to IMDRF SaMD risk tiers, AI/ML Predetermined Change Control Plans (§ 515C), PDURS drug-companion apps, and Decentralized Clinical Trials.",\n'
        '                      f"<ul>{dh_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/digital-health"' in txt:
        return False
    for anchor in ('    "/#/explore/orphan",', '    "/#/explore/vaccines",', '    "/#/explore/biologics",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/digital-health",\n    "/#/explore/digital-health",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_digital_health_py": _write_if_changed(pipe_dir / "build_digital_health.py", BUILD_DIGITAL_HEALTH_PY),
        "digital_health_js": _write_if_changed(js_dir / "digital_health.js", DIGITAL_HEALTH_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/orphan") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/orphan", "Orphan & pediatric"]] }];\nconst EXPLORE_NAV = [["#/explore/orphan", "Orphan & pediatric"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/orphan",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_digital_health.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_digital_health.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"samd_aiml": 6, "pccp_lifecycle": 6, "pdurs_combo": 6, "dct_dht": 6}, out

        doc = json.loads((root / "site" / "data" / "digital_health.json").read_text(encoding="utf-8"))
        for k in ("samd_aiml", "pccp_lifecycle", "pdurs_combo", "dct_dht"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "digital_health.js").read_text(encoding="utf-8")
        print("V61U_DIGITAL_HEALTH_SAMD_AIML_DCT_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1u Digital Health, AI/ML SaMD & DCT patch.")
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
