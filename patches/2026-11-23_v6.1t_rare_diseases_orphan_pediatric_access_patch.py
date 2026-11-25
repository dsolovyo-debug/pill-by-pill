#!/usr/bin/env python3
"""Pill by Pill v6.1t Patch: Rare Diseases, Orphan Drugs, Pediatric Exclusivity & Expanded Access Reference (#/ref/orphan, #/explore/orphan, /api/orphan).

1. Adds `pipeline/build_orphan.py` -> `site/data/orphan.json` (6 Orphan Drug Act & exclusivity
   pillars, 6 Pediatric BPCA/PREA pillars, 6 Rare Pediatric Disease & PRV pillars, and 6 Expanded
   Access / Right to Try pillars — 24 primary-sourced entries).
2. Adds `site/js/orphan.js` (`orphanPage` with inline Rare-Disease & Pediatric Incentives SVG +
   4 section filters) and wires `#/ref/orphan`, `#/explore/orphan`, `/api/orphan`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `orphan.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/orphan/` static SEO page + sitemap entry -> 36
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py --selftest
  python3 2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ORPHAN_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1t Rare Diseases, Orphan Drugs, Pediatric Exclusivity & Expanded Access Reference (`site/data/orphan.json`).

Comprehensive, primary-sourced reference covering:
  1. Orphan Drug Act, Designation & 7-Year Exclusivity (6 pillars)
  2. Pediatric Drug Development — BPCA (+6 Months) & PREA (6 pillars)
  3. Rare Pediatric Disease Designation & Priority Review Vouchers (6 pillars)
  4. Expanded Access (Compassionate Use) & Right to Try (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OOPD, CDER, CBER).

Usage:
  python3 pipeline/build_orphan.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

ORPHAN_DRUG_ACT = [
    {
        "id": "orp-prevalence",
        "name": "Orphan Drug Designation (<200,000 US Patients)",
        "incentive": "Designation Criteria",
        "plain": "When a disease affects fewer than 200,000 Americans, drugmakers often cannot recoup research costs through normal sales—so the Orphan Drug Act offers tax credits, waived FDA fees, and exclusivity.",
        "technical": "Under the Orphan Drug Act (1983) and 21 CFR Part 316, a drug or biologic qualifies if intended for a rare disease affecting <200,000 persons in the US (or >200,000 with no reasonable expectation of recovering development/marketing costs).",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/designating-orphan-product-drugs-and-biological-products",
    },
    {
        "id": "orp-7yr-exclusivity",
        "name": "7-Year Orphan Drug Marketing Exclusivity",
        "incentive": "Market Protection",
        "plain": "The first company to win FDA approval for an orphan-designated medicine gets 7 years where FDA will not approve the same drug from another company for that same rare disease.",
        "technical": "Runs concurrently with patents and NCE/biologic exclusivity; blocks approval of the 'same drug' (21 CFR 316.3(b)(14)) for the designated rare disease or condition for 7 years unless the competitor demonstrates clinical superiority.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/fda-rare-disease-day-february-28-2011",
    },
    {
        "id": "orp-clinical-sup",
        "name": "Clinical Superiority & Breaking Orphan Exclusivity",
        "incentive": "21 CFR 316.34(c)",
        "plain": "A second company can still win approval during the 7-year window—and earn its own exclusivity—if it proves its version works better, is safer, or offers a major benefit to patients.",
        "technical": "Under 21 CFR 316.20(a) and 316.34(c), a sponsor of an 'otherwise same drug' must present a plausible hypothesis of clinical superiority (greater efficacy, greater safety, or major contribution to patient care) for designation and prove it for exclusivity.",
        "url": "https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/frequently-asked-questions-faq-about-designating-orphan-product",
    },
    {
        "id": "orp-tax-pdufa",
        "name": "Qualified Clinical Testing Tax Credit & PDUFA Fee Waiver",
        "incentive": "Financial Relief",
        "plain": "Orphan drugmakers receive federal tax credits on clinical trial expenses and skip multi-million-dollar FDA application filing fees.",
        "technical": "Provides a federal tax credit for qualified clinical testing costs (26 U.S.C. § 45C) plus exemption from the PDUFA human drug application fee (FD&C Act § 736(a)(1)(F)).",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/fda-rare-disease-day-february-28-2011",
    },
    {
        "id": "orp-hud",
        "name": "Humanitarian Use Device (HUD) & HDE Pathway",
        "incentive": "Rare Medical Devices",
        "plain": "Medical devices for ultra-rare conditions affecting 8,000 or fewer Americans per year can use a special Humanitarian Device Exemption pathway.",
        "technical": "Administered by FDA Office of Orphan Products Development (OOPD): HUD designation (<8,000 US patients/year) enables Humanitarian Device Exemption (HDE) approval based on probable benefit rather than full PMA effectiveness trials.",
        "url": "https://www.fda.gov/about-fda/office-health-advancement/office-orphan-products-development",
    },
    {
        "id": "orp-catalyst",
        "name": "Scope of Orphan Exclusivity (Catalyst Pharms. v. Becerra)",
        "incentive": "Statutory Scope",
        "plain": "Recent court rulings clarified how broadly a 7-year orphan exclusivity shield applies when a medicine treats a rare disease across both adults and children.",
        "technical": "FDA's public overview of Catalyst Pharmaceuticals, Inc. v. Becerra addresses whether orphan exclusivity is tied to the broader designated disease/condition versus the narrower approved indication.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions",
    },
]

PEDIATRIC_BPCA_PREA = [
    {
        "id": "ped-prea",
        "name": "Pediatric Research Equity Act (PREA) — Mandatory Studies",
        "incentive": "Statutory Requirement",
        "plain": "Whenever a company develops a new drug, active ingredient, or dosing form that children might also need, PREA requires studying how it works and what dose is safe in kids.",
        "technical": "FD&C Act § 505B (2003) authorizes FDA to require pediatric assessments (iPSP submitted by end of Phase 2) for new active ingredients, indications, dosage forms, dosing regimens, or routes of administration unless waived or deferred.",
        "url": "https://www.fda.gov/drugs/development-resources/pediatric-research-equity-act-prea",
    },
    {
        "id": "ped-bpca",
        "name": "Best Pharmaceuticals for Children Act (BPCA) — +6 Months Exclusivity",
        "incentive": "Voluntary Incentive",
        "plain": "To reward companies for running tough pediatric clinical trials FDA asks for, BPCA adds 6 extra months of market exclusivity onto the drug's existing patents and exclusivities.",
        "technical": "FD&C Act § 505A grants an additional 6 months of pediatric exclusivity attached to all existing Orange Book patents and NCE/orphan/3-year exclusivities when a sponsor fairly responds to an FDA Written Request (even if pediatric efficacy is not established).",
        "url": "https://www.fda.gov/drugs/development-resources/best-pharmaceuticals-children-act-bpca",
    },
    {
        "id": "ped-scientific",
        "name": "Pediatric Extrapolation & Dose Scaling (ICH E11A)",
        "incentive": "Trial Efficiency",
        "plain": "When a disease behaves the same way in children and adults, doctors can often use PK blood-level matching instead of repeating massive placebo trials in kids.",
        "technical": "FDA May 2023 Guidance on PREA/BPCA Scientific Considerations outlines full vs. partial pediatric extrapolation of efficacy when disease progression and exposure–response relationships are sufficiently similar between adult and pediatric populations.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pediatric-drug-development-under-pediatric-research-equity-act-and-best-pharmaceuticals-children-act",
    },
    {
        "id": "ped-formulations",
        "name": "Age-Appropriate Formulations (Suspensions, Mini-Tablets & Taste)",
        "incentive": "Pediatric CMC",
        "plain": "Babies and toddlers cannot swallow giant adult pills—so pediatric development often requires creating liquid syrups, chewables, or sprinkle capsules with safe excipients.",
        "technical": "PREA and BPCA Written Requests frequently require age-appropriate formulations, excipient safety verification (avoiding benzyl alcohol/propylene glycol toxicity in neonates), and palatability/stability validation.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pediatric-drug-development-regulatory-considerations-complying-pediatric-research-equity-act-and",
    },
    {
        "id": "ped-race-act",
        "name": "RACE for Children Act (Molecularly Targeted Oncology)",
        "incentive": "Pediatric Cancer",
        "plain": "Even if an adult cancer—like lung or colon cancer—does not occur in children, a drug targeting a genetic mutation found in childhood tumors must now be studied in kids too.",
        "technical": "FDARA 2017 amended PREA (effective Aug 2020) to require pediatric molecularly targeted oncology investigations when the drug's target is substantially relevant to the growth or progression of a pediatric cancer, overriding orphan exemptions.",
        "url": "https://www.fda.gov/drugs/development-resources/pediatric-research-equity-act-prea",
    },
    {
        "id": "ped-neonatal",
        "name": "Neonatal & Infant Pharmacology Ethics (21 CFR Part 50 Subpart D)",
        "incentive": "Vulnerable Subjects",
        "plain": "Because newborn livers and kidneys mature week by week, pediatric trials follow strict ethical safeguards and sparse micro-sampling to protect babies.",
        "technical": "Requires IRB Subpart D 'prospect of direct clinical benefit' or minor-increase-over-minimal-risk protections, parental permission/child assent, and population PK sparse-sampling designs.",
        "url": "https://www.fda.gov/science-research/pediatrics/best-pharmaceuticals-children-act-and-pediatric-research-equity-act",
    },
]

RPD_PRV_PROGRAMS = [
    {
        "id": "prv-rpd",
        "name": "Rare Pediatric Disease (RPD) Priority Review Voucher (PRV)",
        "incentive": "Transferable Voucher",
        "plain": "If a company wins approval for a serious rare disease that mainly strikes children, FDA awards a 'fast-pass' voucher that speeds up a future drug review—and can even be sold to another company.",
        "technical": "Under FD&C Act § 529, approval of a qualifying novel drug/biologic for a serious or life-threatening rare pediatric disease awards a Priority Review Voucher cutting a subsequent standard NDA/BLA review from 10 months to 6 months; transferable by sale.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs",
    },
    {
        "id": "prv-sunset-2029",
        "name": "2026 Statutory Reauthorization (Sunset Extended to Sept 30, 2029)",
        "incentive": "Current Law",
        "plain": "Congress extended the Rare Pediatric Disease Priority Review Voucher program in February 2026 so FDA can continue awarding vouchers through September 30, 2029.",
        "technical": "Per the Consolidated Appropriations Act, 2026 (enacted Feb 3, 2026), FDA's authority to award RPD PRVs was extended through September 30, 2029.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs",
    },
    {
        "id": "prv-tropical-mcm",
        "name": "Neglected Tropical Disease & Material Threat MCM PRVs",
        "incentive": "Global & Biodefense",
        "plain": "Similar Priority Review Vouchers reward companies that develop treatments for neglected tropical diseases (like Chagas or malaria) or biodefense medical countermeasures.",
        "technical": "FD&C Act §§ 524 and 565A authorize PRVs for qualifying tropical disease and Material Threat Medical Countermeasure (MCM) applications; redemption requires 90-day advance notice and a priority-review voucher user fee.",
        "url": "https://www.fda.gov/emergency-preparedness-and-response/mcm-legal-regulatory-and-policy-framework/21st-century-cures-act-mcm-related-cures-provisions",
    },
    {
        "id": "prv-cber-rare",
        "name": "CBER Rare Disease & Individualized Gene-Editing Pathways",
        "incentive": "Ultra-Rare CGT",
        "plain": "Many childhood rare diseases affect just a handful of patients worldwide; FDA's biologics center builds bespoke regulatory paths for one-of-a-kind gene therapies.",
        "technical": "CBER Office of Therapeutic Products (OTP) coordinates RPD PRVs for biologics, n-of-1/individualized antisense and genome-editing platforms, and natural-history external controls.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cber-rare-disease-program-frequently-asked-questions",
    },
    {
        "id": "prv-grants",
        "name": "OOPD Orphan Products Clinical Trials & Natural History Grants",
        "incentive": "Public Research Funding",
        "plain": "FDA directly awards research grants to universities and small companies running early clinical trials and natural history studies in rare diseases.",
        "technical": "FDA Office of Orphan Products Development administers congressionally appropriated grants supporting clinical trials of products for rare diseases and prospective natural-history studies.",
        "url": "https://www.fda.gov/about-fda/office-health-advancement/office-orphan-products-development",
    },
    {
        "id": "prv-accelerator",
        "name": "Rare Disease Cures Accelerator & Standardized Endpoints",
        "incentive": "Shared Infrastructure",
        "plain": "Instead of each tiny patient foundation starting from zero, FDA's accelerator initiative builds shared data standards and patient-reported outcome tools for rare diseases.",
        "technical": "Collaborative platform integrating standardized clinical outcome assessments (COAs), natural history registries, and clinical trial readiness across neurodegenerative and rare genetic conditions.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions",
    },
]

EXPANDED_ACCESS = [
    {
        "id": "ea-single-patient",
        "name": "Individual Patient Expanded Access (Compassionate Use, 21 CFR 312.310)",
        "incentive": "FDA-Reviewed Access",
        "plain": "When a patient has a serious or life-threatening illness with no approved options and cannot join a clinical trial, their doctor can ask FDA and the drugmaker for emergency single-patient access.",
        "technical": "Physician submits Form FDA 3926 (with manufacturer Letter of Authorization and IRB review); FDA authorizes emergency requests by phone/email in hours and non-emergency INDs within days.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options",
    },
    {
        "id": "ea-intermediate-treatment",
        "name": "Intermediate-Size & Treatment INDs (21 CFR 312.315 / 312.320)",
        "incentive": "Group Access",
        "plain": "When many patients need an experimental drug—for example between the end of a Phase 3 trial and official FDA approval—companies can open a group Expanded Access program.",
        "technical": "Covers intermediate-size patient populations and widespread Treatment INDs/protocols when the drug is actively being developed for marketing approval and poses no unreasonable risk.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/understanding-investigational-drugs",
    },
    {
        "id": "ea-right-to-try",
        "name": "Federal Right to Try Act (May 2018)",
        "incentive": "Non-FDA Pathway",
        "plain": "The Right to Try law lets terminally ill patients who have exhausted approved options ask a drugmaker directly for an experimental medicine that passed Phase 1 safety testing—without FDA review.",
        "technical": "Applies to life-threatening conditions where the patient exhausted approved options and cannot join a clinical trial; requires physician certification, written informed consent, and an eligible investigational drug (completed Phase 1, under active IND). Manufacturer participation is voluntary.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/right-try",
    },
    {
        "id": "ea-safety-reporting",
        "name": "Expanded Access vs. Right to Try — Safety & IRB Safeguards",
        "incentive": "Key Distinction",
        "plain": "In FDA Expanded Access, FDA and an ethics board (IRB) review the dose and safety plan; under Right to Try, FDA does not review the request and only receives annual summary postings.",
        "technical": "FDA authorizes >99% of Expanded Access requests while providing dosing/safety guidance; under Right to Try, FDA has no pre-treatment authorization role and sponsors submit annual summary reports under 21 CFR 300.200.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/right-try",
    },
    {
        "id": "ea-cost-recovery",
        "name": "Charging for Investigational Drugs (Direct Cost Recovery Only)",
        "incentive": "21 CFR 312.8",
        "plain": "Companies generally give investigational drugs for free in Expanded Access, or may charge only direct manufacturing costs with special FDA permission—never at a commercial profit.",
        "technical": "21 CFR 312.8 permits recovering only direct costs of making the drug available (no R&D amortization or profit) upon written FDA authorization.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/understanding-investigational-drugs",
    },
    {
        "id": "ea-trial-tradeoff",
        "name": "Clinical Trial Eligibility Trade-Offs & Public Policies",
        "incentive": "21st Century Cures",
        "plain": "Taking an experimental medicine outside a clinical trial can sometimes disqualify a patient from future trials, so doctors weigh trial enrollment first whenever possible.",
        "technical": "21st Century Cures Act § 561A requires drugmakers developing serious-disease therapies to post public Expanded Access policies and contact information (linked via ClinicalTrials.gov).",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options",
    },
]


def build_orphan(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "orphan_drug_act": len(ORPHAN_DRUG_ACT),
            "pediatric_bpca_prea": len(PEDIATRIC_BPCA_PREA),
            "rpd_prv_programs": len(RPD_PRV_PROGRAMS),
            "expanded_access": len(EXPANDED_ACCESS),
        },
        "orphan_drug_act": ORPHAN_DRUG_ACT,
        "pediatric_bpca_prea": PEDIATRIC_BPCA_PREA,
        "rpd_prv_programs": RPD_PRV_PROGRAMS,
        "expanded_access": EXPANDED_ACCESS,
    }
    (data_dir / "orphan.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_orphan.py <site/data>")
    print(json.dumps(build_orphan(pathlib.Path(sys.argv[1])), indent=2))
'''

ORPHAN_JS = '''// Pill by Pill v6.1t: Rare Diseases, Orphan Drugs, Pediatric Exclusivity & Expanded Access Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["orphan", "Orphan Drug Act", "orphan_drug_act"],
  ["pediatric", "Pediatric (BPCA & PREA)", "pediatric_bpca_prea"],
  ["prv", "Rare Pediatric & PRVs", "rpd_prv_programs"],
  ["access", "Expanded Access & RTT", "expanded_access"],
];

function rareIncentivesSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Rare disease, orphan drug, pediatric exclusivity, and expanded access incentive framework">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Orphan (&lt;200k US)</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">7-Yr Market Exclusivity</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Tax Credit &amp; Fee Waiver</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#orp-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Pediatric Studies</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PREA Required + RACE</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">BPCA +6 Mo Exclusivity</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#orp-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Priority Vouchers</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Rare Pediatric PRV (2029)</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Tropical &amp; MCM PRVs</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#orp-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Patient Access</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Expanded Access (3926)</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Right to Try (2018)</text>
      <defs><marker id="orp-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Statutory rare-disease and pediatric incentives pair 7-year orphan exclusivity, +6-month BPCA extensions, and Priority Review Vouchers with compassionate-access pathways.</figcaption>
  </figure>`;
}

export async function orphanPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/orphan.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/orphan" : "#/ref/orphan";

  const pills = html`<div class="chips" role="navigation" aria-label="Rare disease and pediatric sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Program / Provision</th><th>Mechanism</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.incentive}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${rareIncentivesSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Office of Orphan Products Development (OOPD), BPCA/PREA, and Expanded Access documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Rare Diseases & Orphan Drugs"]] : [REF_HOME, ["Rare Diseases & Orphan Drugs"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Rare Diseases, Orphan Drugs, Pediatric Exclusivity & Expanded Access",
      lede: env === "explore"
        ? "How special laws encourage medicines for rare diseases and children—and how patients can request experimental treatments early."
        : "Orphan Drug Act (<200k US, 7-yr exclusivity), BPCA (+6 mo) & PREA/RACE, Rare Pediatric Disease PRVs (2029), and Expanded Access / Right to Try.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on rare diseases and pediatric exclusivity.", href: env === "explore" ? "#/ref/orphan" : "#/explore/orphan" },
        { title: "Regulatory Pathways & Exclusivity", text: "Fast Track, Breakthrough, Priority Review, and Accelerated Approval.", href: "#/ref/pathways" },
        { title: "Biologics, Biosimilars & Gene Therapies", text: "CAR-T, AAV, CRISPR genome editing, and RMAT designation.", href: "#/ref/biologics" },
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
    if 'orphan.js' not in txt:
        for anchor in ('import * as vaccines from "./vaccines.js";\n', 'import * as biologicsCgt from "./biologics_cgt.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as orphan from "./orphan.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as orphan from "./orphan.js";\n' + txt
            changed = True
    if '"/ref/orphan"' not in txt:
        for anchor in ('if (path === "/ref/vaccines")', 'if (path === "/ref/biologics")', 'if (path === "/ref/supply-chain")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/orphan") return { env: "ref", current: "#/ref/orphan", ...(await orphan.orphanPage(query, "ref")) };\n  if (path === "/explore/orphan") return { env: "explore", current: "#/explore/orphan", ...(await orphan.orphanPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/orphan" not in txt:
        for anchor in ('["#/ref/vaccines", "Vaccines & adjuvants"]', '["#/ref/biologics", "Biologics & CGT"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/orphan", "Orphan & pediatric"]', 1)
                changed = True
                break
    if "#/explore/orphan" not in txt:
        for anchor in ('["#/explore/vaccines", "Vaccines & adjuvants"]', '["#/explore/biologics", "Biologics & CGT"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/orphan", "Orphan & pediatric"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_orphan.py" in txt:
        return False
    line = "python3 pipeline/build_orphan.py site/data\n"
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
    if '"/api/orphan"' in txt:
        return False
    route = (
        '\n@app.get("/api/orphan")\n'
        'def api_orphan():\n'
        '    p = DATA_DIR / "orphan.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "orphan.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"orphan.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    orp_ref = _load(data_dir / "orphan.json", {}) or {}\n'
        '    for sec_key, sec_q in [("orphan_drug_act", "orphan"), ("pediatric_bpca_prea", "pediatric"), ("rpd_prv_programs", "prv"), ("expanded_access", "access")]:\n'
        '        for item in (orp_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "orphan",\n'
        '                "group": "Orphan & Pediatric",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/orphan?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/orphan?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"orphan drug rare disease 7-year exclusivity BPCA PREA RACE pediatric PRV priority review voucher expanded access right to try {sec_key} {item.get(\'name\', \'\')} {item.get(\'incentive\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"orphan", "#/ref/orphan"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    orp_doc = _load_json(data_dir / "orphan.json")\n'
        '    if isinstance(orp_doc, dict) and orp_doc.get("orphan_drug_act"):\n'
        '        orp_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (orp_doc.get("orphan_drug_act") or []) + (orp_doc.get("pediatric_bpca_prea") or []))\n'
        '        pages.append(("orphan", "#/ref/orphan", "Rare Diseases, Orphan Drugs, Pediatric Exclusivity & Expanded Access",\n'
        '                      "Primary-sourced guide to the Orphan Drug Act, BPCA +6-month pediatric exclusivity, PREA/RACE, Rare Pediatric Disease PRVs, and Expanded Access / Right to Try.",\n'
        '                      f"<ul>{orp_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/orphan"' in txt:
        return False
    for anchor in ('    "/#/explore/vaccines",', '    "/#/explore/biologics",', '    "/#/explore/supply-chain",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/orphan",\n    "/#/explore/orphan",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_orphan_py": _write_if_changed(pipe_dir / "build_orphan.py", BUILD_ORPHAN_PY),
        "orphan_js": _write_if_changed(js_dir / "orphan.js", ORPHAN_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/vaccines") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/vaccines", "Vaccines & adjuvants"]] }];\nconst EXPLORE_NAV = [["#/explore/vaccines", "Vaccines & adjuvants"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/vaccines",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_orphan.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_orphan.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"orphan_drug_act": 6, "pediatric_bpca_prea": 6, "rpd_prv_programs": 6, "expanded_access": 6}, out

        doc = json.loads((root / "site" / "data" / "orphan.json").read_text(encoding="utf-8"))
        for k in ("orphan_drug_act", "pediatric_bpca_prea", "rpd_prv_programs", "expanded_access"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "orphan.js").read_text(encoding="utf-8")
        print("V61T_RARE_DISEASES_ORPHAN_PEDIATRIC_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1t Rare Diseases, Orphan Drugs & Pediatric Exclusivity patch.")
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
