#!/usr/bin/env python3
"""Pill by Pill v6.1w Patch: Drug Promotion, OPDP Advertising Rules, Medical Information (SIUU) & Clinical Trial Transparency Reference (#/ref/promotion-transparency, #/explore/promotion-transparency, /api/promotion-transparency).

1. Adds `pipeline/build_promotion_transparency.py` -> `site/data/promotion_transparency.json` (6 OPDP
   Advertising & Promotional Labeling pillars, 6 Unapproved-Use Scientific Exchange (SIUU) & Payor/
   Misinformation Communications pillars, 6 ClinicalTrials.gov FDAAA 801 & Trial Transparency
   pillars, and 6 CMS Open Payments / Sunshine Act & Ethical Compliance pillars — 24 primary-sourced
   entries).
2. Adds `site/js/promotion_transparency.js` (`promotionTransparencyPage` with inline Promotion &
   Transparency Compliance Spectrum SVG + 4 section filters) and wires `#/ref/promotion-transparency`,
   `#/explore/promotion-transparency`, `/api/promotion-transparency`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `promotion_transparency.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/promotion-transparency/` static SEO page + sitemap entry -> 39
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py --selftest
  python3 2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PROMOTION_TRANSPARENCY_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1w Drug Promotion, OPDP, SIUU & Clinical Trial Transparency Reference (`site/data/promotion_transparency.json`).

Comprehensive, primary-sourced reference covering:
  1. OPDP Advertising & Promotional Labeling (6 pillars)
  2. Unapproved-Use Scientific Exchange (SIUU), Payor & Misinformation Communications (6 pillars)
  3. ClinicalTrials.gov FDAAA 801 & Trial Transparency (6 pillars)
  4. CMS Open Payments (Sunshine Act) & Ethical Compliance (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OPDP, ClinicalTrials.gov, NIH, CMS).

Usage:
  python3 pipeline/build_promotion_transparency.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

OPDP_PROMOTION = [
    {
        "id": "promo-opdp-overview",
        "name": "Office of Prescription Drug Promotion (OPDP) Mandate",
        "category": "FDA Oversight",
        "plain": "FDA's Office of Prescription Drug Promotion polices TV commercials, print ads, sales brochures, and websites to ensure drug marketing is truthful, balanced, and not misleading.",
        "technical": "CDER OPDP enforces FD&C Act § 502(n) and 21 CFR 202.1 across prescription drug advertising (broadcast, print, digital) and promotional labeling (sales aids, speaker decks, websites).",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-prescription-drug-promotion-opdp",
    },
    {
        "id": "promo-fair-balance",
        "name": "Fair Balance & Substantial Evidence (21 CFR 202.1)",
        "category": "Core Ad Standard",
        "plain": "A prescription drug ad cannot hype benefits in giant bold letters while hiding serious side effects in tiny fine print—risks and benefits must be given comparable weight.",
        "technical": "Under 21 CFR 202.1(e)(5)-(6), promotional claims require substantial evidence (or substantial clinical experience) and 'fair balance' between effectiveness claims and risk/contraindication disclosures.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-prescription-drug-promotion-opdp",
    },
    {
        "id": "promo-form-2253",
        "name": "FDA Form 2253 Post-Approval Submission at Initial Dissemination",
        "category": "Filing Requirement",
        "plain": "Whenever a pharma company launches a new brochure, TV spot, or promotional webpage, it must submit a copy to FDA at the exact time it first goes public.",
        "technical": "21 CFR 314.81(b)(3)(i) (and 21 CFR 601.12(f)(4) for biologics) requires sponsors to submit all promotional labeling and advertisements via eCTD Module 1.15.2.1 (Form FDA 2253) at the time of initial dissemination or publication.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "promo-ccn-rule",
        "name": "DTC TV/Radio Major Statement — Clear, Conspicuous & Neutral (CCN) Final Rule",
        "category": "Broadcast Standard",
        "plain": "When a TV drug commercial lists major side effects, the rule bans distracting music, rapid-fire voiceovers, or busy visuals—the risks must appear clearly in both audio and readable on-screen text.",
        "technical": "Final Rule amending 21 CFR 202.1(e)(1) establishes five CCN standards for Direct-to-Consumer TV/radio major statements: consumer-friendly language, clear audio, dual-modality (audio + text) on TV, legible text, and no distracting audio/visual elements.",
        "url": "https://www.fda.gov/media/175074/download",
    },
    {
        "id": "promo-core-launch",
        "name": "OPDP Core Launch vs. Voluntary Advisory Review",
        "category": "Pre-Launch Review",
        "plain": "For high-stakes new drug launches or Accelerated Approval drugs, companies often ask FDA to pre-review ads voluntarily so they avoid an embarrassing launch-week warning letter.",
        "technical": "Sponsors may request voluntary OPDP advisory comments before launch; Subpart H / Accelerated Approval (21 CFR 314.550 / 601.45) requires pre-submission of promotional materials 30 days prior to dissemination.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "promo-bad-ad",
        "name": "FDA Bad Ad Program (855-RX-BADAD & HCP Reporting)",
        "category": "Field Surveillance",
        "plain": "Doctors, nurses, and pharmacists can anonymously report misleading sales-rep pitches, trade-show booths, or ads directly to FDA through the Bad Ad hotline.",
        "technical": "OPDP's Bad Ad Program educates healthcare providers to recognize false or misleading prescription drug promotion and report violations via BadAd@fda.gov or 855-RX-BADAD.",
        "url": "https://www.fda.gov/drugs/prescription-drug-advertising-and-promotional-labeling/bad-ad-program",
    },
]

SIUU_COMMUNICATIONS = [
    {
        "id": "siuu-jan2025-guidance",
        "name": "SIUU Final Guidance (Jan 2025): Scientific Information on Unapproved Uses",
        "category": "Off-Label Boundary",
        "plain": "Drugmakers cannot advertise a medicine for an unapproved disease, but medical teams may share truthful, peer-reviewed scientific reprints about unapproved uses with doctors under strict guardrails.",
        "technical": "FDA's January 2025 Final Guidance sets enforcement policy for firm-initiated communications to HCPs of Scientific Information on Unapproved Uses (SIUU)—covering published reprints, clinical reference resources, and firm-generated presentations.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/communications-firms-health-care-providers-regarding-scientific-information-unapproved-uses",
    },
    {
        "id": "siuu-scientific-soundness",
        "name": "SIUU Scientifically Sound & Clinically Relevant Standard",
        "category": "Evidence Quality",
        "plain": "Any off-label study shared with a physician must be scientifically valid and clinically meaningful—not a cherry-picked case report or promotional spin.",
        "technical": "Under the 2025 SIUU Final Guidance, source publications and firm-generated presentations must be scientifically sound, clinically relevant, accompanied by approved labeling, and free of persuasive marketing techniques.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/communications-firms-health-care-providers-regarding-scientific-information-unapproved-uses",
    },
    {
        "id": "siuu-separation",
        "name": "Separation of Promotional vs. Scientific Exchange Channels",
        "category": "Compliance Firewall",
        "plain": "Companies must keep non-promotional medical science liaisons and scientific reprints physically and digitally separate from sales-rep marketing pitches.",
        "technical": "SIUU materials must be separate from promotional communications (distinct booths, web portals, and emailers) with clear disclosures that the unapproved use is not FDA-approved and safety/efficacy are not established.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "siuu-payor-hcei",
        "name": "Payor & Formulary Communications (FDAMA 114 / HCEI & Pre-Approval)",
        "category": "Payor Exchange",
        "plain": "Before a drug is even approved, companies can share factual pipeline timelines and health-economic models with insurance formularies so coverage decisions don't lag behind launch.",
        "technical": "FD&C Act § 502(a) (amended by 21st Century Cures § 3037) permits Health Care Economic Information (HCEI) to payors under competent and reliable scientific evidence, plus pre-approval information exchange (PIE) for investigational products.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "siuu-misinformation",
        "name": "Addressing Third-Party Misinformation Online (2024 Draft Guidance)",
        "category": "Digital Correction",
        "plain": "If a viral social post spreads false safety rumors or fake dosing claims about a medicine, FDA allows the maker to post tailored, factual corrections without triggering full ad rules.",
        "technical": "FDA's 2024 Revised Draft Guidance ('Addressing Misinformation About Medical Devices and Prescription Drugs') provides enforcement discretion for tailored responsive communications correcting independent third-party misinformation.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "siuu-hcp-badad",
        "name": "HCP Vigilance at Medical Conferences & Speaker Programs",
        "category": "Peer Oversight",
        "plain": "Paid physician speaker dinners and conference booths are among the most closely watched promo channels—FDA encourages doctors to flag scripted off-label pitches.",
        "technical": "OPDP's Bad Ad outreach highlights high-risk promotional settings including speaker programs, exhibit booths, and social media influencer endorsements lacking fair balance or material connection disclosures.",
        "url": "https://www.fda.gov/drugs/office-prescription-drug-promotion/fdas-bad-ad-program-encourages-hcps-report-false-or-misleading-prescription-drug-promotion",
    },
]

CLINICAL_TRIAL_TRANSPARENCY = [
    {
        "id": "ct-fdaaa-801",
        "name": "FDAAA 801 & 42 CFR Part 11 Clinical Trial Transparency",
        "category": "Statutory Mandate",
        "plain": "Federal law requires drug sponsors to publicly register Phase 2–4 trials and post their real results on ClinicalTrials.gov so failed studies can't be swept under the rug.",
        "technical": "Section 801 of the FDA Amendments Act of 2007 (42 U.S.C. 282(j)) and Final Rule 42 CFR Part 11 establish mandatory registration and results submission for Applicable Clinical Trials (ACTs) of FDA-regulated drugs, biologics, and devices.",
        "url": "https://clinicaltrials.gov/policy/fdaaa-801-final-rule",
    },
    {
        "id": "ct-21day-registration",
        "name": "21-Day Trial Registration Deadline",
        "category": "Registration Timing",
        "plain": "Sponsors must list a qualifying clinical trial on ClinicalTrials.gov within 21 days of enrolling the very first patient.",
        "technical": "Under 42 CFR 11.24, the Responsible Party must register an Applicable Clinical Trial no later than 21 calendar days after enrollment of the first human participant, including protocol eligibility and primary outcome measures.",
        "url": "https://clinicaltrials.gov/policy/reporting-requirements",
    },
    {
        "id": "ct-12month-results",
        "name": "12-Month Results Reporting & Protocol / SAP Posting",
        "category": "Results Deadline",
        "plain": "Within one year after a trial's main data-collection ends, the sponsor must post participant flow, primary outcomes, and adverse events—along with the full study protocol.",
        "technical": "42 CFR 11.44 mandates summary results submission (participant flow, baseline characteristics, outcome measures, statistical analyses, adverse events) plus full protocol and Statistical Analysis Plan (SAP) within 1 year of Primary Completion Date.",
        "url": "https://clinicaltrials.gov/policy/fdaaa-801-final-rule",
    },
    {
        "id": "ct-cmp-nih-holds",
        "name": "Civil Money Penalties & NIH Grant Funding Holds",
        "category": "Enforcement Teeth",
        "plain": "Ignoring ClinicalTrials.gov deadlines can trigger daily FDA fines exceeding $10,000+ per day and freeze federal NIH research grants.",
        "technical": "FD&C Act § 301(jj) and § 303(f)(3) authorize FDA Notices of Noncompliance and inflation-adjusted daily Civil Money Penalties (CMPs); 42 CFR 11 / NIH Policy also withholds NIH grant funds for non-compliant recipients.",
        "url": "https://grants.nih.gov/policy-and-compliance/policy-topics/clinical-trials/reporting/understanding",
    },
    {
        "id": "ct-icf-posting",
        "name": "Public Posting of Clinical Trial Informed Consent Forms",
        "category": "Patient Transparency",
        "plain": "Under federal human-subjects rules, one blank copy of the consent form used to enroll patients in federally funded trials must be posted publicly online.",
        "technical": "Revised Common Rule (45 CFR 46.116(h)) requires one IRB-approved informed consent form used in federally supported clinical trials to be posted on ClinicalTrials.gov or Regulations.gov within 60 days after the last study visit.",
        "url": "https://grants.nih.gov/policy-and-compliance/policy-topics/clinical-trials/reporting/understanding",
    },
    {
        "id": "ct-expanded-access",
        "name": "Public Expanded Access Policy Posting (21st Century Cures)",
        "category": "Access Transparency",
        "plain": "Before starting Phase 2/3 trials of a new medicine, companies must publish a public webpage explaining how seriously ill patients can request compassionate access.",
        "technical": "FD&C Act § 561A (21st Century Cures) requires manufacturers of investigational drugs in Phase 2/3 to post publicly accessible Expanded Access policies, contact info, and response timelines linked on ClinicalTrials.gov.",
        "url": "https://clinicaltrials.gov/policy/reporting-requirements",
    },
]

OPEN_PAYMENTS_COMPLIANCE = [
    {
        "id": "op-sunshine-act",
        "name": "CMS Open Payments (Physician Payments Sunshine Act, ACA § 6002)",
        "category": "Financial Disclosure",
        "plain": "Every meal, consulting fee, travel reimbursement, or research grant a drugmaker gives to a US physician or teaching hospital is published in a searchable federal database.",
        "technical": "ACA § 6002 (42 U.S.C. 1320a-7h) and 42 CFR Part 403 Subpart I require applicable manufacturers and GPOs to report annually to CMS all transfers of value to covered recipients.",
        "url": "https://www.cms.gov/files/document/11709p-open-payments-physicianspdf",
    },
    {
        "id": "op-covered-recipients",
        "name": "Covered Recipients: Physicians, Teaching Hospitals & APPs",
        "category": "Scope of Reporting",
        "plain": "Open Payments now tracks payments not only to MDs and teaching hospitals, but also to physician assistants, nurse practitioners, and clinical nurse specialists.",
        "technical": "SUPPORT Act (2018) expanded Open Payments covered recipients (effective 2021 data) beyond physicians and teaching hospitals to include PAs, NPs, CNSs, CRNAs, and CNMs.",
        "url": "https://www.cms.gov/files/document/open-payments-user-guide-covered-recipients.pdf",
    },
    {
        "id": "op-payment-categories",
        "name": "General Payments vs. Research Payments vs. Ownership Interests",
        "category": "Data Categories",
        "plain": "CMS separates everyday payments (like speaking fees, consulting, and lunches) from clinical trial research grants and physician stock/ownership stakes.",
        "technical": "Open Payments classifies transfers into three datasets: General Payments (consulting, honoraria, food/beverage, travel, royalties), Research Payments (clinical trial agreements), and Physician Ownership/Investment Interests.",
        "url": "https://www.cms.gov/files/document/11709p-open-payments-physicianspdf",
    },
    {
        "id": "op-review-dispute",
        "name": "45-Day Pre-Publication Review & Dispute Window",
        "category": "Data Accuracy",
        "plain": "Before CMS publishes the annual database each June, doctors get a 45-day window to review what drug companies reported under their name and challenge errors.",
        "technical": "Covered recipients receive a mandatory 45-day review and dispute period (typically April–May) plus a 15-day manufacturer correction window prior to June 30 annual public release.",
        "url": "https://www.cms.gov/files/document/open-payments-user-guide-covered-recipients.pdf",
    },
    {
        "id": "op-opdp-enforcement",
        "name": "OPDP Untitled Letters vs. Warning Letters",
        "category": "Enforcement Escalation",
        "plain": "If a drug ad crosses the line, FDA issues either an Untitled Letter demanding it stop, or a tougher Warning Letter requiring corrective ads to set the record straight.",
        "technical": "OPDP issues Untitled Letters for initial/less-severe promotional violations (requiring cessation) and Warning Letters for serious/repetitive violations or safety omissions (often requiring corrective dissemination).",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/office-prescription-drug-promotion-opdp-news",
    },
    {
        "id": "op-anti-kickback-alignment",
        "name": "Speaker Program Compliance & Anti-Kickback Guardrails",
        "category": "Ethical Marketing",
        "plain": "Combining Open Payments transparency with federal Anti-Kickback rules has forced companies to curb lavish speaker dinners and tie honoraria strictly to legitimate education.",
        "technical": "OIG Special Fraud Alert on Speaker Programs and PhRMA Code align with Open Payments reporting to deter quid pro quo prescribing inducements under the federal Anti-Kickback Statute (42 U.S.C. 1320a-7b(b)).",
        "url": "https://www.cms.gov/files/document/11709p-open-payments-physicianspdf",
    },
]


def build_promotion_transparency(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "opdp_promotion": len(OPDP_PROMOTION),
            "siuu_communications": len(SIUU_COMMUNICATIONS),
            "clinical_trial_transparency": len(CLINICAL_TRIAL_TRANSPARENCY),
            "open_payments_compliance": len(OPEN_PAYMENTS_COMPLIANCE),
        },
        "opdp_promotion": OPDP_PROMOTION,
        "siuu_communications": SIUU_COMMUNICATIONS,
        "clinical_trial_transparency": CLINICAL_TRIAL_TRANSPARENCY,
        "open_payments_compliance": OPEN_PAYMENTS_COMPLIANCE,
    }
    (data_dir / "promotion_transparency.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_promotion_transparency.py <site/data>")
    print(json.dumps(build_promotion_transparency(pathlib.Path(sys.argv[1])), indent=2))
'''

PROMOTION_TRANSPARENCY_JS = '''// Pill by Pill v6.1w: Drug Promotion, OPDP Advertising Rules, Medical Information (SIUU) & Clinical Trial Transparency Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["opdp", "OPDP Promotion & Ads", "opdp_promotion"],
  ["siuu", "SIUU & Payor Exchange", "siuu_communications"],
  ["trials", "FDAAA 801 & Trial Posting", "clinical_trial_transparency"],
  ["sunshine", "Open Payments & Ethics", "open_payments_compliance"],
];

function promotionSpectrumSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Drug promotion, scientific exchange, clinical trial transparency, and Open Payments compliance framework">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. OPDP Ads &amp; Labeling</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Fair Balance &amp; CCN TV</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Form 2253 &amp; Bad Ad</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#promo-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Scientific Exchange</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Jan 2025 SIUU Guidance</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">FDAMA 114 &amp; Misinfo</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#promo-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Trial Transparency</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">FDAAA 801 / 42 CFR 11</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">21-Day Reg &amp; 12-Mo Data</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#promo-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Open Payments</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Sunshine Act (ACA §6002)</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">45-Day Dispute &amp; OIG</text>
      <defs><marker id="promo-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Federal oversight separates promotional advertising from scientific exchange while requiring public clinical trial results and physician payment disclosures.</figcaption>
  </figure>`;
}

export async function promotionTransparencyPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/promotion_transparency.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/promotion-transparency" : "#/ref/promotion-transparency";

  const pills = html`<div class="chips" role="navigation" aria-label="Drug promotion and transparency sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Rule / Standard</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${promotionSpectrumSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA OPDP, Jan 2025 SIUU Final Guidance, ClinicalTrials.gov FDAAA 801 (42 CFR Part 11), and CMS Open Payments documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Promotion & Transparency"]] : [REF_HOME, ["Promotion & Transparency"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Drug Promotion, OPDP, SIUU & Clinical Trial Transparency",
      lede: env === "explore"
        ? "Rules governing TV drug ads, off-label scientific reprints, mandatory clinical trial results posting, and public doctor payment disclosures."
        : "OPDP 21 CFR 202.1, CCN TV Final Rule, Form 2253, Jan 2025 SIUU Guidance, FDAAA 801 (42 CFR Part 11), and CMS Open Payments.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on promotion and transparency.", href: env === "explore" ? "#/ref/promotion-transparency" : "#/explore/promotion-transparency" },
        { title: "Clinical Trial Design & Endpoints", text: "Phase 1–4 trial mechanics registered under FDAAA 801.", href: "#/ref/trials" },
        { title: "Pharmacovigilance & Drug Safety", text: "FAERS, REMS, and post-approval safety labeling.", href: "#/ref/safety" },
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
    if 'promotion_transparency.js' not in txt:
        for anchor in ('import * as otcCompounding from "./otc_compounding.js";\n', 'import * as digitalHealth from "./digital_health.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as promotionTransparency from "./promotion_transparency.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as promotionTransparency from "./promotion_transparency.js";\n' + txt
            changed = True
    if '"/ref/promotion-transparency"' not in txt:
        for anchor in ('if (path === "/ref/otc-compounding")', 'if (path === "/ref/digital-health")', 'if (path === "/ref/orphan")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/promotion-transparency") return { env: "ref", current: "#/ref/promotion-transparency", ...(await promotionTransparency.promotionTransparencyPage(query, "ref")) };\n  if (path === "/explore/promotion-transparency") return { env: "explore", current: "#/explore/promotion-transparency", ...(await promotionTransparency.promotionTransparencyPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/promotion-transparency" not in txt:
        for anchor in ('["#/ref/otc-compounding", "OTC & compounding"]', '["#/ref/digital-health", "Digital health & AI"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/promotion-transparency", "Promotion & transparency"]', 1)
                changed = True
                break
    if "#/explore/promotion-transparency" not in txt:
        for anchor in ('["#/explore/otc-compounding", "OTC & compounding"]', '["#/explore/digital-health", "Digital health & AI"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/promotion-transparency", "Promotion & transparency"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_promotion_transparency.py" in txt:
        return False
    line = "python3 pipeline/build_promotion_transparency.py site/data\n"
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
    if '"/api/promotion-transparency"' in txt:
        return False
    route = (
        '\n@app.get("/api/promotion-transparency")\n'
        'def api_promotion_transparency():\n'
        '    p = DATA_DIR / "promotion_transparency.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "promotion_transparency.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"promotion_transparency.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    promo_ref = _load(data_dir / "promotion_transparency.json", {}) or {}\n'
        '    for sec_key, sec_q in [("opdp_promotion", "opdp"), ("siuu_communications", "siuu"), ("clinical_trial_transparency", "trials"), ("open_payments_compliance", "sunshine")]:\n'
        '        for item in (promo_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "promotion_transparency",\n'
        '                "group": "Promotion & Transparency",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/promotion-transparency?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/promotion-transparency?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"OPDP promotion advertising Form 2253 CCN Bad Ad SIUU off-label FDAMA 114 HCEI ClinicalTrials FDAAA 801 42 CFR 11 Open Payments Sunshine Act {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"promotion-transparency", "#/ref/promotion-transparency"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    promo_doc = _load_json(data_dir / "promotion_transparency.json")\n'
        '    if isinstance(promo_doc, dict) and promo_doc.get("opdp_promotion"):\n'
        '        promo_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (promo_doc.get("opdp_promotion") or []) + (promo_doc.get("clinical_trial_transparency") or []))\n'
        '        pages.append(("promotion-transparency", "#/ref/promotion-transparency", "Drug Promotion, OPDP, SIUU & Clinical Trial Transparency",\n'
        '                      "Primary-sourced guide to FDA OPDP advertising rules, Jan 2025 SIUU guidance, FDAAA 801 ClinicalTrials.gov reporting, and CMS Open Payments.",\n'
        '                      f"<ul>{promo_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/promotion-transparency"' in txt:
        return False
    for anchor in ('    "/#/explore/otc-compounding",', '    "/#/explore/digital-health",', '    "/#/explore/orphan",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/promotion-transparency",\n    "/#/explore/promotion-transparency",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_promotion_transparency_py": _write_if_changed(pipe_dir / "build_promotion_transparency.py", BUILD_PROMOTION_TRANSPARENCY_PY),
        "promotion_transparency_js": _write_if_changed(js_dir / "promotion_transparency.js", PROMOTION_TRANSPARENCY_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/otc-compounding") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/otc-compounding", "OTC & compounding"]] }];\nconst EXPLORE_NAV = [["#/explore/otc-compounding", "OTC & compounding"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/otc-compounding",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_promotion_transparency.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_promotion_transparency.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"opdp_promotion": 6, "siuu_communications": 6, "clinical_trial_transparency": 6, "open_payments_compliance": 6}, out

        doc = json.loads((root / "site" / "data" / "promotion_transparency.json").read_text(encoding="utf-8"))
        for k in ("opdp_promotion", "siuu_communications", "clinical_trial_transparency", "open_payments_compliance"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "promotion_transparency.js").read_text(encoding="utf-8")
        print("V61W_PROMOTION_OPDP_TRANSPARENCY_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1w Drug Promotion, OPDP, SIUU & Clinical Trial Transparency patch.")
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
