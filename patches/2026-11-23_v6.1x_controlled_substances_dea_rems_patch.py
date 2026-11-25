#!/usr/bin/env python3
"""Pill by Pill v6.1x Patch: Controlled Substances, DEA Scheduling (I–V), Abuse-Potential & Opioid REMS Reference (#/ref/controlled-substances, #/explore/controlled-substances, /api/controlled-substances).

1. Adds `pipeline/build_controlled_substances.py` -> `site/data/controlled_substances.json` (6 DEA
   CSA Schedules I–V & 8-Factor pillars, 6 DEA Registration, CSOS/Form 222, Quotas & ARCOS pillars,
   6 FDA Abuse-Potential & Abuse-Deterrent Formulation pillars, and 6 Opioid REMS, Mail-Back
   Envelopes, OTC Naloxone & MATE Act/MOUD pillars — 24 primary-sourced entries).
2. Adds `site/js/controlled_substances.js` (`controlledSubstancesPage` with inline Controlled
   Substances & Risk Mitigation SVG + 4 section filters) and wires `#/ref/controlled-substances`,
   `#/explore/controlled-substances`, `/api/controlled-substances`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `controlled_substances.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/controlled-substances/` static SEO page + sitemap entry
   -> 40 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py --selftest
  python3 2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_CONTROLLED_SUBSTANCES_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1x Controlled Substances, DEA Scheduling, Abuse-Potential & Opioid REMS Reference (`site/data/controlled_substances.json`).

Comprehensive, primary-sourced reference covering:
  1. DEA Controlled Substances Act (CSA) Schedules I–V & 8-Factor Analysis (6 pillars)
  2. DEA Diversion Control: CSOS, Form 222, Quotas & ARCOS (6 pillars)
  3. FDA Abuse-Potential Assessment & Abuse-Deterrent Formulations (ADFs) (6 pillars)
  4. Opioid REMS, Mail-Back Envelopes, OTC Naloxone & MATE Act / MOUD (6 pillars)

All regulatory anchors are verified HTTPS primary sources (DEA, DEA Diversion Control, FDA CDER, SAMHSA).

Usage:
  python3 pipeline/build_controlled_substances.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

DEA_SCHEDULING = [
    {
        "id": "csa-overview",
        "name": "Controlled Substances Act (CSA, 21 U.S.C. § 812) Five-Schedule System",
        "category": "Statutory Framework",
        "plain": "Federal law sorts medicines and chemicals with addiction or misuse risk into five numbered tiers—Schedule I (strictest, no accepted medical use) down to Schedule V (lowest risk).",
        "technical": "CSA places controlled substances into Schedules I–V (21 CFR 1308.11–1308.15) based on accepted US medical use, relative abuse potential, and likelihood of physical or psychological dependence.",
        "url": "https://www.dea.gov/drug-information/csa",
    },
    {
        "id": "csa-schedule-1",
        "name": "Schedule I: High Abuse Potential, No Accepted Medical Use",
        "category": "Schedule I (C-I)",
        "plain": "Schedule I substances cannot be prescribed at a pharmacy and require special federal research registrations and strict vault security.",
        "technical": "Defined under 21 U.S.C. 812(b)(1) as having high potential for abuse, no currently accepted medical use in treatment in the US, and lack of accepted safety under medical supervision (e.g., heroin, LSD).",
        "url": "https://www.dea.gov/drug-information/drug-scheduling",
    },
    {
        "id": "csa-schedule-2",
        "name": "Schedule II: Accepted Medical Use with Severe Dependence Risk",
        "category": "Schedule II (C-II)",
        "plain": "Strong painkillers and ADHD stimulants sit in Schedule II—doctors can prescribe them, but prescriptions cannot carry automatic refills and require tighter security.",
        "technical": "Schedule II (C-II) drugs (e.g., oxycodone, hydromorphone, methadone, amphetamine, methylphenidate) have high abuse potential that may lead to severe psychological or physical dependence; no refills permitted.",
        "url": "https://www.dea.gov/drug-information/drug-scheduling",
    },
    {
        "id": "csa-schedule-3-4",
        "name": "Schedules III & IV: Moderate-to-Low Dependence Potential",
        "category": "Schedules III–IV",
        "plain": "Medicines like buprenorphine (Schedule III) and benzodiazepines or sleep aids (Schedule IV) carry lower risk than Schedule II opioids and allow limited prescription refills.",
        "technical": "Schedule III (moderate/low physical or high psychological dependence) and Schedule IV (low abuse/dependence potential relative to C-III, e.g., benzodiazepines) permit up to 5 refills within 6 months.",
        "url": "https://www.dea.gov/drug-information/drug-scheduling",
    },
    {
        "id": "csa-schedule-5",
        "name": "Schedule V: Lowest Abuse Potential & Limited-Quantity Preparations",
        "category": "Schedule V (C-V)",
        "plain": "Schedule V covers the mildest controlled medicines, including low-dose codeine cough syrups and certain nerve-pain or anti-seizure drugs.",
        "technical": "Schedule V substances have lower abuse potential than Schedule IV and consist primarily of preparations containing limited quantities of certain narcotics (e.g., ≤200 mg codeine per 100 mL) or low-risk CNS agents.",
        "url": "https://www.dea.gov/drug-information/drug-scheduling",
    },
    {
        "id": "csa-8-factor-nda",
        "name": "FDA Controlled Substance Staff (CSS) & NDA Module 1.14 Scheduling Proposal",
        "category": "FDA-DEA Handoff",
        "plain": "When a company seeks FDA approval for a new brain-active medicine, it must submit a formal scheduling analysis so FDA and DEA can assign the right schedule before launch.",
        "technical": "Under 21 CFR 314.50(d)(5)(vii) and MAPP 4200.3 Rev. 2, NDAs for drugs with abuse potential include an abuse-potential evaluation and scheduling proposal in eCTD Module 1.14; FDA transmits an 8-factor analysis to DEA.",
        "url": "https://www.fda.gov/media/71652/download",
    },
]

DEA_DIVERSION_CONTROL = [
    {
        "id": "div-csos",
        "name": "Controlled Substance Ordering System (CSOS) Digital PKI",
        "category": "Electronic Ordering",
        "plain": "Hospitals, pharmacies, and wholesalers order Schedule II controlled drugs electronically using DEA-issued digital certificates instead of mailing paper triplicate forms.",
        "technical": "CSOS uses Public Key Infrastructure (PKI) digital signatures to authenticate DEA registrants/POAs; it is the sole authorized electronic pathway for Schedule I and II orders (no line-item limit) and also supports Schedules III–V.",
        "url": "https://www.deadiversion.usdoj.gov/drugreg/csos/about.html",
    },
    {
        "id": "div-form-222",
        "name": "Single-Sheet DEA Form 222 for Schedule I & II Transfers",
        "category": "Paper Order Form",
        "plain": "When electronic ordering isn't used, every transfer of Schedule I or II drugs requires an official, serially numbered DEA Form 222.",
        "technical": "DEA transitioned from triplicate to single-sheet DEA Form 222 for physical Schedule I and II orders between registrants, providing auditable chain-of-custody records alongside electronic CSOS.",
        "url": "https://www.deadiversion.usdoj.gov/faq/form-222-faq.html",
    },
    {
        "id": "div-quotas",
        "name": "Aggregate Production Quotas (APQ) & Individual Manufacturing Quotas",
        "category": "Supply Caps",
        "plain": "Every year, DEA sets a strict national ceiling on how much Schedule I and II active ingredient—like oxycodone or amphetamine—can be manufactured in the US.",
        "technical": "Under 21 U.S.C. 826, DEA establishes annual Aggregate Production Quotas (APQ) for Schedule I/II substances and List I chemicals (ephedrine, pseudoephedrine, PPA), allocating Individual Manufacturing Quotas (IMQ) per plant.",
        "url": "https://www.deadiversion.usdoj.gov/new.html",
    },
    {
        "id": "div-arcos",
        "name": "Automation of Reports and Consolidated Orders System (ARCOS)",
        "category": "Supply Chain Tracking",
        "plain": "DEA's national tracking system follows every gram of Schedule I and II medicines from the factory through wholesalers down to retail pharmacies and hospitals.",
        "technical": "ARCOS is DEA's automated comprehensive drug reporting system monitoring manufacturing, inventory, and distribution transactions of Schedule I/II (and select Schedule III) controlled substances to detect diversion.",
        "url": "https://www.deadiversion.usdoj.gov/arcos/arcos.html",
    },
    {
        "id": "div-registration",
        "name": "DEA Activity-Specific Registration & Physical Security Vaults",
        "category": "Facility Licensing",
        "plain": "Every factory, warehouse, pharmacy, or research lab handling controlled substances needs its own location-specific DEA registration and alarmed safes or cages.",
        "technical": "CSA requires separate registration per physical location and business activity (manufacturer, distributor, researcher, practitioner, pharmacy) with tiered physical security (vaults/cages for C-I/C-II under 21 CFR 1301.72).",
        "url": "https://www.deadiversion.usdoj.gov/",
    },
    {
        "id": "div-marijuana-research",
        "name": "21 CFR Part 1318 Bulk Marijuana Research Cultivation Framework",
        "category": "Schedule I Supply",
        "plain": "A specialized DEA rule lets federally registered growers cultivate research-grade cannabis under bona fide supply agreements with licensed scientists.",
        "technical": "21 CFR Part 1318 governs DEA-registered bulk Schedule I marijuana manufacturers using DEA Form 189 IMQs, bona fide supply agreements (BFSAs), and DEA-executed Form 222 ownership/distribution steps.",
        "url": "https://www.deadiversion.usdoj.gov/drugreg/marijuana.html",
    },
]

ABUSE_POTENTIAL_ADFS = [
    {
        "id": "adf-abuse-potential",
        "name": "FDA Assessment of Abuse Potential of Drugs (2017 Guidance)",
        "category": "Premarket Safety",
        "plain": "If a new drug enters the brain, FDA requires animal and human studies—plus careful tracking of euphoria or withdrawal in clinical trials—before approval.",
        "technical": "2017 Final Guidance outlines nonclinical (receptor binding, self-administration, drug discrimination, physical dependence), clinical Human Abuse Potential (HAP), and adverse-event signal evaluation for CNS-active NDAs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessment-abuse-potential-drugs",
    },
    {
        "id": "adf-hap-studies",
        "name": "Clinical Human Abuse Potential (HAP) 'Drug Liking' Studies",
        "category": "Pharmacodynamics",
        "plain": "In specialized clinical studies, experienced recreational users compare a new medicine against a placebo and a known controlled drug on 'drug liking' scales.",
        "technical": "Randomized, double-blind, placebo- and positive-controlled crossover PD studies measuring primary endpoints such as Visual Analog Scale (VAS) 'Drug Liking' Emax to quantify relative abuse potential.",
        "url": "https://www.fda.gov/media/116739/download",
    },
    {
        "id": "adf-7-technologies",
        "name": "Seven Abuse-Deterrent Formulation (ADF) Technology Categories",
        "category": "Formulation Design",
        "plain": "Drugmakers engineer abuse-deterrent pills that turn into thick gel when crushed or include a built-in blocker so they can't easily be snorted or injected.",
        "technical": "FDA recognizes 7 ADF approaches: physical/chemical barriers, agonist/antagonist combinations, aversion agents, delivery systems (e.g., depot/implants), new molecular entities/prodrugs, combinations, and novel approaches.",
        "url": "https://www.fda.gov/industry/generic-drug-user-fee-amendments/fy2013-2017-regulatory-science-report-oral-abuse-deterrent-opioid-products",
    },
    {
        "id": "adf-3-tier-testing",
        "name": "Three-Tier Premarket ADF Evaluation (Categories 1, 2 & 3)",
        "category": "Evidence Package",
        "plain": "To earn abuse-deterrent claims on its label, a pill must survive lab crushing/extraction tests, blood-level checks, and human abuse-potential trials.",
        "technical": "FDA's 2015 ADF Final Guidance requires Category 1 (in vitro manipulation/extraction), Category 2 (PK studies after tampering), and Category 3 (clinical PD abuse-potential studies), followed by Category 4 post-market epidemiology.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/abuse-deterrent-opioids-evaluation-and-labeling",
    },
    {
        "id": "adf-approved-labels",
        "name": "Labeled Abuse-Deterrent Opioids & Route Limitations",
        "category": "Labeling Reality",
        "plain": "Approved abuse-deterrent opioids (like OxyContin, Hysingla ER, Xtampza ER, and RoxyBond) deter crushing or injecting, though swallowing intact pills still carries addiction risk.",
        "technical": "FDA-approved ADF labeling specifies the exact deterred routes (e.g., intranasal, intravenous) supported by Categories 1–3 data while warning that oral misuse/overdose remains possible.",
        "url": "https://www.fda.gov/drugs/food-and-drug-administration-overdose-prevention-framework/abuse-deterrent-opioid-analgesics",
    },
    {
        "id": "adf-generic-parity",
        "name": "Generic ADF 'No Less Abuse-Deterrent' Standard",
        "category": "ANDA Equivalence",
        "plain": "A generic copy of an abuse-deterrent opioid must prove in lab and clinical tests that it resists crushing and extraction at least as well as the brand pill.",
        "technical": "FDA's General Principles for Generic Solid Oral Opioid ADFs requires ANDA applicants to demonstrate non-inferior abuse deterrence against the Reference Listed Drug across all potential abuse routes.",
        "url": "https://www.fda.gov/drugs/food-and-drug-administration-overdose-prevention-framework/abuse-deterrent-opioid-analgesics",
    },
]

OPIOID_REMS_MITIGATION = [
    {
        "id": "rems-oa-blueprint",
        "name": "Opioid Analgesic REMS & Updated FDA Prescriber Education Blueprint",
        "category": "Class-Wide REMS",
        "plain": "Manufacturers of outpatient opioid painkillers must fund free, accredited continuing education so doctors and pharmacists learn safer pain management and addiction screening.",
        "technical": "Shared-system Opioid Analgesic (OA) REMS covers immediate-release and ER/LA outpatient opioids, updating terminology ('nonmedical use', 'opioid use disorder') and disposal guidance in the FDA Blueprint.",
        "url": "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/opioid-analgesic-risk-evaluation-and-mitigation-strategy-rems",
    },
    {
        "id": "rems-mail-back",
        "name": "Outpatient Opioid Mail-Back Envelopes (MBEs) Mandate (March 2025)",
        "category": "Safe Disposal",
        "plain": "Opioid manufacturers must supply pre-paid mail-back envelopes to pharmacies upon request so patients can safely mail unused pills for destruction instead of leaving them in medicine cabinets.",
        "technical": "FDA's October 31, 2024 OA REMS modification required outpatient opioid manufacturers to make pre-paid drug Mail-Back Envelopes (MBEs) available to pharmacies and dispensers by March 31, 2025.",
        "url": "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/opioid-analgesic-risk-evaluation-and-mitigation-strategy-rems",
    },
    {
        "id": "rems-naloxone-otc",
        "name": "Over-the-Counter Naloxone Nasal Spray Switches (Narcan & RiVive)",
        "category": "Overdose Reversal",
        "plain": "In 2023, FDA approved the first over-the-counter naloxone nasal sprays so anyone can buy life-saving overdose reversal medicine without a prescription.",
        "technical": "FDA approved nonprescription Narcan (4 mg naloxone HCl, March 2023) and RiVive (July 2023) supported by a validated model Drug Facts Label with pictograms and Human Factors simulated-use studies.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-approves-first-over-counter-naloxone-nasal-spray",
    },
    {
        "id": "rems-mate-act",
        "name": "MATE Act Training & OA REMS Continuing Education Alignment",
        "category": "Prescriber Training",
        "plain": "Before renewing a DEA registration, prescribers must complete 8 hours of substance-use-disorder training—which can be fulfilled using free OA REMS courses.",
        "technical": "Medication Access and Training Expansion (MATE) Act requires DEA-registered practitioners to complete 8 hours of SUD training aligned with SAMHSA Curricular Elements; OA REMS CE satisfies part of MATE Act requirements.",
        "url": "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/opioid-analgesic-risk-evaluation-and-mitigation-strategy-rems",
    },
    {
        "id": "rems-buprenorphine-oud",
        "name": "Buprenorphine & Medications for Opioid Use Disorder (MOUD)",
        "category": "Addiction Treatment",
        "plain": "Eliminating the special federal 'X-waiver' opened the door for any DEA-registered clinician to prescribe buprenorphine for opioid use disorder just like other Schedule III medicines.",
        "technical": "Schedule III partial mu-opioid agonist buprenorphine (plus methadone and naltrexone) forms core evidence-based MOUD; Consolidated Appropriations Act (2023) repealed the DATA-2000 X-waiver requirement.",
        "url": "https://www.samhsa.gov/substance-use/treatment/options/buprenorphine",
    },
    {
        "id": "rems-overdose-framework",
        "name": "FDA Overdose Prevention Framework & Evidence-Based Pain Guidelines",
        "category": "Public Health Strategy",
        "plain": "FDA pairs safer acute-pain prescribing guidelines with harm reduction, OTC reversal agents, and new non-addictive pain treatments to curb overdose deaths.",
        "technical": "FDA Overdose Prevention Framework spans four pillars: primary prevention (rational prescribing), harm reduction (OTC naloxone, DSCSA exemptions), evidence-based SUD treatments, and counterfeit/diverted drug enforcement.",
        "url": "https://www.fda.gov/drugs/food-and-drug-administration-overdose-prevention-framework/supporting-clinical-practice-guidelines-drugs-abuse-potential",
    },
]


def build_controlled_substances(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "dea_scheduling": len(DEA_SCHEDULING),
            "dea_diversion_control": len(DEA_DIVERSION_CONTROL),
            "abuse_potential_adfs": len(ABUSE_POTENTIAL_ADFS),
            "opioid_rems_mitigation": len(OPIOID_REMS_MITIGATION),
        },
        "dea_scheduling": DEA_SCHEDULING,
        "dea_diversion_control": DEA_DIVERSION_CONTROL,
        "abuse_potential_adfs": ABUSE_POTENTIAL_ADFS,
        "opioid_rems_mitigation": OPIOID_REMS_MITIGATION,
    }
    (data_dir / "controlled_substances.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_controlled_substances.py <site/data>")
    print(json.dumps(build_controlled_substances(pathlib.Path(sys.argv[1])), indent=2))
'''

CONTROLLED_SUBSTANCES_JS = '''// Pill by Pill v6.1x: Controlled Substances, DEA Scheduling (I–V), Abuse-Potential & Opioid REMS Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["scheduling", "DEA Schedules I–V", "dea_scheduling"],
  ["diversion", "CSOS, Quotas & ARCOS", "dea_diversion_control"],
  ["adf", "Abuse Potential & ADFs", "abuse_potential_adfs"],
  ["rems", "Opioid REMS & Naloxone", "opioid_rems_mitigation"],
];

function controlledSpectrumSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="DEA scheduling, diversion control, abuse-potential ADFs, and Opioid REMS lifecycle">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. CSA Scheduling</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Schedules I–V (21 CFR 1308)</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">8-Factor &amp; NDA 1.14</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#csa-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Diversion Control</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CSOS PKI &amp; Form 222</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">APQ Quotas &amp; ARCOS</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#csa-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Abuse-Deterrent</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">HAP Drug-Liking Studies</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Cat 1–3 ADF &amp; Generic</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#csa-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. REMS &amp; Reversal</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">OA REMS &amp; Mail-Back</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">OTC Naloxone &amp; MATE</text>
      <defs><marker id="csa-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">DEA and FDA coordinate premarket abuse-potential testing, five-tier scheduling, supply quotas, and post-market Opioid REMS &amp; overdose reversal.</figcaption>
  </figure>`;
}

export async function controlledSubstancesPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/controlled_substances.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/controlled-substances" : "#/ref/controlled-substances";

  const pills = html`<div class="chips" role="navigation" aria-label="Controlled substances and REMS sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Control / Standard</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${controlledSpectrumSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against DEA CSA Schedules I–V, DEA Diversion Control (CSOS/Form 222/ARCOS), FDA Abuse-Potential &amp; ADF Guidances, Opioid Analgesic REMS, and SAMHSA documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Controlled Substances & REMS"]] : [REF_HOME, ["Controlled Substances & REMS"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Controlled Substances, DEA Scheduling, ADFs & Opioid REMS",
      lede: env === "explore"
        ? "How federal drug schedules (I–V), supply quotas, tamper-resistant pills, opioid safety programs, and OTC naloxone protect patients."
        : "CSA Schedules I–V, 8-factor scheduling, CSOS/Form 222/ARCOS, HAP &amp; Category 1–3 ADFs, OA REMS Mail-Back Envelopes, OTC naloxone, and MATE Act.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on controlled substances and REMS.", href: env === "explore" ? "#/ref/controlled-substances" : "#/explore/controlled-substances" },
        { title: "Pharmacovigilance & Drug Safety", text: "FAERS, REMS, and post-market safety monitoring.", href: "#/ref/safety" },
        { title: "Supply Chain & DSCSA", text: "Serialization, cold chain, and drug shortage tracking.", href: "#/ref/supply-chain" },
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
    if 'controlled_substances.js' not in txt:
        for anchor in ('import * as promotionTransparency from "./promotion_transparency.js";\n', 'import * as otcCompounding from "./otc_compounding.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as controlledSubstances from "./controlled_substances.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as controlledSubstances from "./controlled_substances.js";\n' + txt
            changed = True
    if '"/ref/controlled-substances"' not in txt:
        for anchor in ('if (path === "/ref/promotion-transparency")', 'if (path === "/ref/otc-compounding")', 'if (path === "/ref/digital-health")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/controlled-substances") return { env: "ref", current: "#/ref/controlled-substances", ...(await controlledSubstances.controlledSubstancesPage(query, "ref")) };\n  if (path === "/explore/controlled-substances") return { env: "explore", current: "#/explore/controlled-substances", ...(await controlledSubstances.controlledSubstancesPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/controlled-substances" not in txt:
        for anchor in ('["#/ref/promotion-transparency", "Promotion & transparency"]', '["#/ref/otc-compounding", "OTC & compounding"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/controlled-substances", "Controlled substances"]', 1)
                changed = True
                break
    if "#/explore/controlled-substances" not in txt:
        for anchor in ('["#/explore/promotion-transparency", "Promotion & transparency"]', '["#/explore/otc-compounding", "OTC & compounding"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/controlled-substances", "Controlled substances"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_controlled_substances.py" in txt:
        return False
    line = "python3 pipeline/build_controlled_substances.py site/data\n"
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
    if '"/api/controlled-substances"' in txt:
        return False
    route = (
        '\n@app.get("/api/controlled-substances")\n'
        'def api_controlled_substances():\n'
        '    p = DATA_DIR / "controlled_substances.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "controlled_substances.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"controlled_substances.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    csa_ref = _load(data_dir / "controlled_substances.json", {}) or {}\n'
        '    for sec_key, sec_q in [("dea_scheduling", "scheduling"), ("dea_diversion_control", "diversion"), ("abuse_potential_adfs", "adf"), ("opioid_rems_mitigation", "rems")]:\n'
        '        for item in (csa_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "controlled_substances",\n'
        '                "group": "Controlled Substances & REMS",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/controlled-substances?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/controlled-substances?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"DEA controlled substances CSA Schedule I II III IV V CSOS Form 222 ARCOS quota abuse potential HAP ADF opioid REMS mail-back naloxone OTC MATE Act buprenorphine {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"controlled-substances", "#/ref/controlled-substances"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    csa_doc = _load_json(data_dir / "controlled_substances.json")\n'
        '    if isinstance(csa_doc, dict) and csa_doc.get("dea_scheduling"):\n'
        '        csa_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (csa_doc.get("dea_scheduling") or []) + (csa_doc.get("opioid_rems_mitigation") or []))\n'
        '        pages.append(("controlled-substances", "#/ref/controlled-substances", "Controlled Substances, DEA Scheduling, ADFs & Opioid REMS",\n'
        '                      "Primary-sourced guide to DEA CSA Schedules I–V, CSOS/Form 222/ARCOS diversion control, abuse-deterrent formulations, Opioid REMS, and OTC naloxone.",\n'
        '                      f"<ul>{csa_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/controlled-substances"' in txt:
        return False
    for anchor in ('    "/#/explore/promotion-transparency",', '    "/#/explore/otc-compounding",', '    "/#/explore/digital-health",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/controlled-substances",\n    "/#/explore/controlled-substances",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_controlled_substances_py": _write_if_changed(pipe_dir / "build_controlled_substances.py", BUILD_CONTROLLED_SUBSTANCES_PY),
        "controlled_substances_js": _write_if_changed(js_dir / "controlled_substances.js", CONTROLLED_SUBSTANCES_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/promotion-transparency") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/promotion-transparency", "Promotion & transparency"]] }];\nconst EXPLORE_NAV = [["#/explore/promotion-transparency", "Promotion & transparency"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/promotion-transparency",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_controlled_substances.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_controlled_substances.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"dea_scheduling": 6, "dea_diversion_control": 6, "abuse_potential_adfs": 6, "opioid_rems_mitigation": 6}, out

        doc = json.loads((root / "site" / "data" / "controlled_substances.json").read_text(encoding="utf-8"))
        for k in ("dea_scheduling", "dea_diversion_control", "abuse_potential_adfs", "opioid_rems_mitigation"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "controlled_substances.js").read_text(encoding="utf-8")
        print("V61X_CONTROLLED_SUBSTANCES_DEA_REMS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1x Controlled Substances, DEA Scheduling, ADFs & Opioid REMS patch.")
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
