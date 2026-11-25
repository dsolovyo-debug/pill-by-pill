#!/usr/bin/env python3
"""Pill by Pill v6.1y Patch: US Drug Pricing, IRA Medicare Negotiation, 340B, Medicaid Best Price & Part B ASP Reference (#/ref/pricing-access, #/explore/pricing-access, /api/pricing-access).

1. Adds `pipeline/build_pricing_access.py` -> `site/data/pricing_access.json` (6 IRA Medicare Drug
   Price Negotiation & Part D Redesign pillars, 6 HRSA 340B Drug Pricing Program pillars, 6 Medicaid
   Drug Rebate Program [MDRP] & Best Price pillars, and 6 Medicare Part B ASP+6% & Gross-to-Net
   Pricing Benchmark pillars — 24 primary-sourced entries).
2. Adds `site/js/pricing_access.js` (`pricingAccessPage` with inline US Drug Pricing & Rebate
   Architecture SVG + 4 section filters) and wires `#/ref/pricing-access`,
   `#/explore/pricing-access`, `/api/pricing-access`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `pricing_access.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/pricing-access/` static SEO page + sitemap entry -> 41
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py --selftest
  python3 2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PRICING_ACCESS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1y US Drug Pricing, IRA Negotiation, 340B, MDRP & Part B ASP Reference (`site/data/pricing_access.json`).

Comprehensive, primary-sourced reference covering:
  1. IRA Medicare Drug Price Negotiation & Part D Redesign (6 pillars)
  2. HRSA 340B Drug Pricing Program & Covered Entities (6 pillars)
  3. Medicaid Drug Rebate Program (MDRP), AMP & Best Price (6 pillars)
  4. Medicare Part B ASP+6% & Commercial Pricing Benchmarks (6 pillars)

All regulatory anchors are verified HTTPS primary sources (CMS, HRSA, Medicaid.gov).

Usage:
  python3 pipeline/build_pricing_access.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

IRA_MEDICARE_NEGOTIATION = [
    {
        "id": "ira-mfp-program",
        "name": "Medicare Drug Price Negotiation Program & Maximum Fair Price (MFP)",
        "category": "Inflation Reduction Act",
        "plain": "Under the Inflation Reduction Act, Medicare can now directly negotiate lower prices—called Maximum Fair Prices—on top-spending prescription drugs without generic competition.",
        "technical": "IRA §§ 11001–11002 (SSA §§ 1191–1198) authorize CMS to select high-expenditure single-source Part D and Part B drugs lacking generic/biosimilar competition and negotiate a binding Maximum Fair Price (MFP).",
        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program",
    },
    {
        "id": "ira-9yr-13yr-clock",
        "name": "9-Year Small Molecule vs. 13-Year Biologic Eligibility Clock",
        "category": "Selection Timing",
        "plain": "Pills become eligible for Medicare price negotiation 9 years after FDA approval, while complex biologic injections get 13 years before negotiation can take effect.",
        "technical": "Drugs are eligible for MFP applicability 9 years (small-molecule NDAs) or 13 years (BLA biologics) post-FDA approval/licensure, subject to orphan, low-spend, and plasma-derived exclusions.",
        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program/regulations-guidance-policy-documents",
    },
    {
        "id": "ira-ipays-cycles",
        "name": "Multi-Year Negotiation Cycles (IPAY 2026, 2027 & 2028)",
        "category": "Rollout Cadence",
        "plain": "CMS negotiated the first 10 Part D drugs for 2026, added 15 more for 2027, and expanded to include Part B clinic-administered drugs starting in 2028.",
        "technical": "CMS published MFPs for 10 Part D drugs (IPAY 2026), selected 15 additional Part D drugs (IPAY 2027), and expanded selection to both Part D and Part B drugs for IPAY 2028+.",
        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program/selected-drugs-negotiated-prices",
    },
    {
        "id": "ira-partd-2000-cap",
        "name": "Medicare Part D $2,000 Annual Out-of-Pocket Cap (2025+)",
        "category": "Patient Affordability",
        "plain": "Starting in 2025, seniors on Medicare Part D never pay more than $2,000 a year out of pocket for covered prescription drugs at the pharmacy.",
        "technical": "IRA Part D benefit redesign eliminates the 5% catastrophic coinsurance, caps annual beneficiary out-of-pocket spending at $2,000 (indexed thereafter), and introduces the Medicare Prescription Payment Plan smoothing option.",
        "url": "https://www.cms.gov/files/document/infographic-negotiated-prices-maximum-fair-prices.pdf",
    },
    {
        "id": "ira-insulin-vaccines",
        "name": "$35 Monthly Insulin Cap & $0 Recommended Part D Vaccines",
        "category": "IRA Cost-Sharing",
        "plain": "Medicare caps covered insulin copays at $35 per month and makes ACIP-recommended adult vaccines—like shingles and RSV shots—free with zero copay.",
        "technical": "IRA limits Medicare Part D and Part B covered insulin cost-sharing to $35/month supply and eliminates cost-sharing for ACIP-recommended adult vaccines under Part D.",
        "url": "https://www.cms.gov/files/document/infographic-negotiated-prices-maximum-fair-prices.pdf",
    },
    {
        "id": "ira-mfp-effectuation",
        "name": "MFP Effectuation, Non-Duplication with 340B & Excise Tax",
        "category": "Compliance Mechanics",
        "plain": "Drugmakers must ensure pharmacies and clinics actually get the negotiated Medicare price—or pay steep federal excise taxes if they refuse to participate.",
        "technical": "CMS Final Guidance establishes Medicare Transaction Facilitator (MTF) workflows to effectuate MFPs via retrospective refunds or prospective discounts and prevent duplicate 340B/MFP discounts.",
        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program/regulations-guidance-policy-documents",
    },
]

HRSA_340B_PROGRAM = [
    {
        "id": "340b-statute",
        "name": "340B Drug Pricing Program Overview (PHS Act § 340B)",
        "category": "Safety-Net Discount",
        "plain": "Safety-net clinics and hospitals serving low-income or rural patients can buy outpatient drugs at steep mandatory discounts (often 25%–50%+ off) under the 340B program.",
        "technical": "Section 340B of the Public Health Service Act requires manufacturers participating in Medicaid to sell covered outpatient drugs to eligible covered entities at or below the statutory 340B Ceiling Price.",
        "url": "https://www.hrsa.gov/opa",
    },
    {
        "id": "340b-covered-entities",
        "name": "Eligible 340B Covered Entities (DSH, CAH, FQHC & Ryan White)",
        "category": "Entity Eligibility",
        "plain": "Qualifying hospitals—such as Disproportionate Share Hospitals, Critical Access Hospitals, and community health centers—must register with HRSA to access 340B pricing.",
        "technical": "Statutory covered entities include Disproportionate Share Hospitals (DSH), Critical Access Hospitals (CAH), Rural Referral Centers (RRC), Sole Community Hospitals (SCH), Children's/Cancer Hospitals, and federal grantees (FQHCs, Ryan White).",
        "url": "https://www.hrsa.gov/opa/eligibility-and-registration",
    },
    {
        "id": "340b-scale-2024",
        "name": "340B Program Scale ($81.4B in 2024 Covered Entity Purchases)",
        "category": "Market Footprint",
        "plain": "The 340B program has grown into a massive part of US pharma distribution, with participating hospitals and clinics purchasing $81.4 billion in discounted drugs in 2024.",
        "technical": "Per HRSA OPA data, 340B covered entities purchased $81.4 billion in covered outpatient drugs at 340B prices in calendar year 2024, making 340B gross-to-net leakage a central commercial and policy focus.",
        "url": "https://www.hrsa.gov/opa/updates/2024-340b-covered-entity-purchases",
    },
    {
        "id": "340b-duplicate-diversion",
        "name": "Prohibition on Diversion & Duplicate Discounts (Medicaid)",
        "category": "Program Integrity",
        "plain": "A 340B hospital cannot resell discounted 340B drugs to ineligible patients or collect both a 340B discount and a Medicaid rebate on the exact same prescription.",
        "technical": "PHS Act § 340B(a)(5) prohibits drug diversion (dispensing to non-patients) and duplicate discounts (claiming both 340B ceiling price and MDRP Medicaid rebate on the same NDC unit), audited via HRSA OPA.",
        "url": "https://www.hrsa.gov/opa",
    },
    {
        "id": "340b-opais-registration",
        "name": "340B Office of Pharmacy Affairs Information System (OPAIS)",
        "category": "Registry & Audits",
        "plain": "Manufacturers and hospitals verify eligibility, contract pharmacies, and quarterly enrollment windows in HRSA's central OPAIS database.",
        "technical": "340B OPAIS tracks active covered entity IDs, child sites, and registered contract pharmacy arrangements with quarterly registration windows (Jan/Apr/Jul/Oct).",
        "url": "https://www.hrsa.gov/opa/340b-opais",
    },
    {
        "id": "340b-rebate-pilot",
        "name": "340B Rebate Model Pilot Program & Acquisition Mechanics",
        "category": "Evolving Policy",
        "plain": "Regulators and manufacturers are testing whether certain 340B discounts can shift from upfront invoice price cuts to post-dispensing rebates to curb duplicate claims.",
        "technical": "HRSA's 340B Rebate Model Pilot Program evaluates transitioning select covered entity acquisitions from upfront 340B ceiling price discounts to claims-verified retrospective rebates.",
        "url": "https://www.hrsa.gov/opa/340b-model-pilot-program",
    },
]

MEDICAID_MDRP = [
    {
        "id": "mdrp-overview",
        "name": "Medicaid Drug Rebate Program (MDRP, SSA § 1927)",
        "category": "Statutory Rebate",
        "plain": "In exchange for Medicaid covering nearly all of a company's FDA-approved drugs, the manufacturer must pay quarterly cash rebates back to state and federal Medicaid programs.",
        "technical": "Under SSA § 1927, manufacturers sign a National Drug Rebate Agreement (NDRA) requiring quarterly Unit Rebate Amount (URA) payments to states as a condition of Medicaid and Medicare Part B coverage.",
        "url": "https://www.medicaid.gov/medicaid/prescription-drugs/medicaid-drug-rebate-program",
    },
    {
        "id": "mdrp-231-best-price",
        "name": "23.1% Minimum Rebate & 'Best Price' Most-Favored-Nation Floor",
        "category": "Rebate Formula",
        "plain": "For brand drugs, Medicaid automatically gets either a 23.1% discount off the average manufacturer price—or the lowest commercial price offered to any private insurer, whichever is deeper.",
        "technical": "Basic rebate for single-source/innovator multiple-source drugs equals the greater of 23.1% of Average Manufacturer Price (AMP) or (AMP minus Best Price); non-innovator generics pay 13% of AMP (clotting factors/pediatric 17.1%).",
        "url": "https://www.medicaid.gov/medicaid/prescription-drugs/medicaid-drug-rebate-program/unit-rebate-amount-calculation",
    },
    {
        "id": "mdrp-cpiu-penalty",
        "name": "CPI-U Inflation Penalty & Removal of the 100% AMP Cap",
        "category": "Price-Hike Deterrent",
        "plain": "If a drugmaker raises its price faster than general inflation, Medicaid's extra rebate penalty grows dollar-for-dollar—and since 2024, that rebate can exceed 100% of the drug's price.",
        "technical": "Additional inflationary rebate equals (quarterly AMP minus inflation-adjusted baseline AMP); ARPA (2021) eliminated the 100%-of-AMP URA cap effective Jan 1, 2024, creating potential >100% Medicaid rebates.",
        "url": "https://www.medicaid.gov/medicaid/prescription-drugs/medicaid-drug-rebate-program/unit-rebate-amount-calculation",
    },
    {
        "id": "mdrp-amp-reporting",
        "name": "Quarterly & Monthly Average Manufacturer Price (AMP) Reporting",
        "category": "Price Reporting",
        "plain": "Drug companies must report their real average factory selling price to wholesalers and retail pharmacies every month and quarter—and errors trigger federal penalties.",
        "technical": "Manufacturers submit monthly and quarterly AMP and quarterly Best Price to CMS within 30 days after quarter-end; 5i rules govern inhalation, infusion, instilled, implanted, and injectable drugs.",
        "url": "https://www.medicaid.gov/medicaid/prescription-drugs/medicaid-drug-rebate-program/medicaid-drug-rebate-program-data",
    },
    {
        "id": "mdrp-vbp-multiple-bp",
        "name": "Value-Based Purchasing (VBP) & Multiple Best Prices Rule",
        "category": "Outcomes Contracts",
        "plain": "Special Medicaid rules let drugmakers offer 'money-back guarantees' if an expensive gene therapy fails to work in a patient, without wrecking their Best Price across the whole country.",
        "technical": "CMS Manufacturer Release No. 116 allows manufacturers to report multiple Best Prices under qualifying outcomes-based Value-Based Purchasing (VBP) arrangements offered to commercial payors and states.",
        "url": "https://www.medicaid.gov/prescription-drugs/downloads/mfr-rel-116-vbp.pdf",
    },
    {
        "id": "mdrp-authorized-generics",
        "name": "Authorized Generics & AMP Exclusion Rules",
        "category": "Generic Launches",
        "plain": "Launching an 'authorized generic' copy of a brand drug can't be used to artificially water down the brand's Medicaid rebate calculations.",
        "technical": "Continuing Appropriations Act (2019) and CMS Release No. 112 exclude authorized generic sales from the brand drug's AMP calculation while treating the AG as a separate NDC for MDRP reporting.",
        "url": "https://www.medicaid.gov/prescription-drugs/downloads/mfr-rel-112.pdf",
    },
]

PART_B_ASP_BENCHMARKS = [
    {
        "id": "asp-partb-plus6",
        "name": "Medicare Part B Average Sales Price (ASP + 6%) Formula",
        "category": "Physician-Administered",
        "plain": "For infused cancer drugs and clinic injections covered under Medicare Part B, Medicare reimburses doctors and hospitals at the drug's national Average Sales Price plus 6%.",
        "technical": "Under SSA § 1847A, Medicare Part B pays ASP + 6% for separately payable physician-administered drugs and biologicals (subject to statutory sequestration), calculated from quarterly manufacturer sales net of discounts.",
        "url": "https://www.cms.gov/cms-guide-medical-technology-companies-and-other-interested-parties/payment/part-b-drugs",
    },
    {
        "id": "asp-reporting-lag",
        "name": "Quarterly ASP Reporting & Two-Quarter Pricing Lag",
        "category": "ASP Mechanics",
        "plain": "Drugmakers report net sales to CMS every quarter, and Medicare updates Part B clinic reimbursement rates two quarters later—meaning steep discounts eventually lower reimbursement.",
        "technical": "Manufacturers submit ASP data within 30 days of quarter close; CMS publishes Part B Drug Payment Limit Files effective two quarters later, embedding rebates/chargebacks into future ASP.",
        "url": "https://www.cms.gov/medicare/payment/part-b-drugs/asp-reporting",
    },
    {
        "id": "asp-wac-launch",
        "name": "Wholesale Acquisition Cost (WAC) & New-Drug Launch Pricing",
        "category": "List Price Benchmark",
        "plain": "Before a brand-new clinic drug has enough sales history to calculate an Average Sales Price, Medicare temporarily pays based on its public list price (Wholesale Acquisition Cost).",
        "technical": "WAC is the manufacturer's published list price to wholesalers/direct purchasers excluding prompt-pay or other discounts; during initial quarters before ASP availability, Part B pays WAC + 3% (or 103% WAC).",
        "url": "https://www.cms.gov/cms-guide-medical-technology-companies-and-other-interested-parties/payment/part-b-drugs",
    },
    {
        "id": "asp-biosimilar-add-on",
        "name": "Part B Biosimilar ASP+8% Add-On & Reference Pricing",
        "category": "Biosimilar Incentive",
        "plain": "To encourage clinics to choose lower-cost biosimilars over brand biologics, Medicare boosted the Part B add-on payment for qualifying biosimilars from 6% to 8% of the reference product's ASP.",
        "technical": "IRA temporarily increased Medicare Part B add-on payment for qualifying biosimilars (whose ASP is below the reference biological's ASP) to 8% of the reference biologic's ASP for a 5-year period.",
        "url": "https://www.cms.gov/medicare/payment/fee-for-service-providers/part-b-drugs/average-drug-sales-price",
    },
    {
        "id": "asp-wamp-amp-oig",
        "name": "OIG WAMP / AMP Substitution & Preventive Vaccine 95% AWP",
        "category": "Price Guardrails",
        "plain": "If a Part B drug's calculated ASP drifts more than 5% above private-market survey prices, federal watchdogs can force Medicare's payment rate down.",
        "technical": "When OIG determines ASP exceeds Widely Available Market Price (WAMP) or AMP by ≥5%, CMS may substitute the lower price; preventive Part B vaccines (flu, pneumococcal, Hep B) are reimbursed at 95% of AWP.",
        "url": "https://www.cms.gov/cms-guide-medical-technology-companies-and-other-interested-parties/payment/part-b-drugs",
    },
    {
        "id": "asp-gtn-stack",
        "name": "Gross-to-Net (GTN) Waterfall: WAC vs. PBM Rebates, 340B & MDRP",
        "category": "Commercial Economics",
        "plain": "A drug's sticker price (WAC) is rarely what the manufacturer actually keeps—after PBM rebates, 340B discounts, Medicaid rebates, and co-pay cards, net revenue is often 40%–60% lower.",
        "technical": "Pharma GTN bridges gross WAC sales to net revenue across PBM formulary rebates, wholesaler fees, 340B ceiling discounts, MDRP/Part D inflation rebates, and patient copay assistance.",
        "url": "https://www.cms.gov/medicare/payment/part-b-drugs/asp-pricing-files",
    },
]


def build_pricing_access(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "ira_medicare_negotiation": len(IRA_MEDICARE_NEGOTIATION),
            "hrsa_340b_program": len(HRSA_340B_PROGRAM),
            "medicaid_mdrp": len(MEDICAID_MDRP),
            "part_b_asp_benchmarks": len(PART_B_ASP_BENCHMARKS),
        },
        "ira_medicare_negotiation": IRA_MEDICARE_NEGOTIATION,
        "hrsa_340b_program": HRSA_340B_PROGRAM,
        "medicaid_mdrp": MEDICAID_MDRP,
        "part_b_asp_benchmarks": PART_B_ASP_BENCHMARKS,
    }
    (data_dir / "pricing_access.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_pricing_access.py <site/data>")
    print(json.dumps(build_pricing_access(pathlib.Path(sys.argv[1])), indent=2))
'''

PRICING_ACCESS_JS = '''// Pill by Pill v6.1y: US Drug Pricing, IRA Medicare Negotiation, 340B, Medicaid Best Price & Part B ASP Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["ira", "IRA Medicare Negotiation", "ira_medicare_negotiation"],
  ["340b", "HRSA 340B Program", "hrsa_340b_program"],
  ["mdrp", "Medicaid MDRP & Best Price", "medicaid_mdrp"],
  ["asp", "Part B ASP & GTN Waterfall", "part_b_asp_benchmarks"],
];

function pricingWaterfallSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="US pharmaceutical pricing, IRA negotiation, 340B, Medicaid Best Price, and Part B ASP architecture">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. IRA &amp; Part D</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">MFP (9-Yr / 13-Yr Clock)</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">$2,000 OOP Cap &amp; $35 Ins</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#prc-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. HRSA 340B</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">DSH / CAH / FQHC Entities</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">$81.4B (2024) &amp; OPAIS</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#prc-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Medicaid MDRP</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">23.1% AMP or Best Price</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CPI-U Penalty (No Cap)</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#prc-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Part B &amp; GTN</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">ASP + 6% / Biosim +8%</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">WAC-to-Net Waterfall</text>
      <defs><marker id="prc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">US drug pricing spans list WAC, PBM rebates, 340B ceiling prices, Medicaid Best Price, Medicare Part B ASP+6%, and IRA Maximum Fair Prices.</figcaption>
  </figure>`;
}

export async function pricingAccessPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/pricing_access.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/pricing-access" : "#/ref/pricing-access";

  const pills = html`<div class="chips" role="navigation" aria-label="Drug pricing and access sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Mechanism / Statute</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Policy Detail"}</th><th>Source</th></tr></thead>
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
    ${pricingWaterfallSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against CMS IRA Medicare Drug Price Negotiation, HRSA 340B OPA, Medicaid MDRP, and Medicare Part B ASP documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Drug Pricing, IRA & 340B"]] : [REF_HOME, ["Drug Pricing, IRA & 340B"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "US Drug Pricing, IRA Negotiation, 340B & Medicaid Best Price",
      lede: env === "explore"
        ? "How Medicare drug price negotiation, $2,000 Part D caps, 340B hospital discounts, and Medicaid rebates shape what medicines cost."
        : "IRA Maximum Fair Price (9-yr/13-yr), Part D $2,000 cap, HRSA 340B ($81.4B), Medicaid MDRP (23.1% / Best Price / CPI-U), and Medicare Part B ASP+6%.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on US drug pricing and access.", href: env === "explore" ? "#/ref/pricing-access" : "#/explore/pricing-access" },
        { title: "Pharma Software & Economics", text: "Gross-to-net economics, R&D capital, and launch models.", href: "#/ref/economics" },
        { title: "Global Regulatory & HTA", text: "Compare US CMS/ICER access with NICE, HAS, and IQWiG.", href: "#/ref/global-reg" },
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
    if 'pricing_access.js' not in txt:
        for anchor in ('import * as controlledSubstances from "./controlled_substances.js";\n', 'import * as promotionTransparency from "./promotion_transparency.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as pricingAccess from "./pricing_access.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as pricingAccess from "./pricing_access.js";\n' + txt
            changed = True
    if '"/ref/pricing-access"' not in txt:
        for anchor in ('if (path === "/ref/controlled-substances")', 'if (path === "/ref/promotion-transparency")', 'if (path === "/ref/otc-compounding")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/pricing-access") return { env: "ref", current: "#/ref/pricing-access", ...(await pricingAccess.pricingAccessPage(query, "ref")) };\n  if (path === "/explore/pricing-access") return { env: "explore", current: "#/explore/pricing-access", ...(await pricingAccess.pricingAccessPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/pricing-access" not in txt:
        for anchor in ('["#/ref/controlled-substances", "Controlled substances"]', '["#/ref/promotion-transparency", "Promotion & transparency"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/pricing-access", "Pricing, IRA & 340B"]', 1)
                changed = True
                break
    if "#/explore/pricing-access" not in txt:
        for anchor in ('["#/explore/controlled-substances", "Controlled substances"]', '["#/explore/promotion-transparency", "Promotion & transparency"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/pricing-access", "Pricing, IRA & 340B"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_pricing_access.py" in txt:
        return False
    line = "python3 pipeline/build_pricing_access.py site/data\n"
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
    if '"/api/pricing-access"' in txt:
        return False
    route = (
        '\n@app.get("/api/pricing-access")\n'
        'def api_pricing_access():\n'
        '    p = DATA_DIR / "pricing_access.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "pricing_access.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pricing_access.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    prc_ref = _load(data_dir / "pricing_access.json", {}) or {}\n'
        '    for sec_key, sec_q in [("ira_medicare_negotiation", "ira"), ("hrsa_340b_program", "340b"), ("medicaid_mdrp", "mdrp"), ("part_b_asp_benchmarks", "asp")]:\n'
        '        for item in (prc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "pricing_access",\n'
        '                "group": "Pricing, IRA & 340B",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/pricing-access?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/pricing-access?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"IRA Medicare Drug Price Negotiation Maximum Fair Price MFP Part D 2000 cap 340B HRSA OPAIS Medicaid MDRP AMP Best Price CPI-U ASP WAC GTN {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pricing-access", "#/ref/pricing-access"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    prc_doc = _load_json(data_dir / "pricing_access.json")\n'
        '    if isinstance(prc_doc, dict) and prc_doc.get("ira_medicare_negotiation"):\n'
        '        prc_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (prc_doc.get("ira_medicare_negotiation") or []) + (prc_doc.get("hrsa_340b_program") or []))\n'
        '        pages.append(("pricing-access", "#/ref/pricing-access", "US Drug Pricing, IRA Negotiation, 340B & Medicaid Best Price",\n'
        '                      "Primary-sourced guide to IRA Medicare Drug Price Negotiation, Part D $2,000 cap, HRSA 340B, Medicaid MDRP Best Price, and Part B ASP+6%.",\n'
        '                      f"<ul>{prc_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/pricing-access"' in txt:
        return False
    for anchor in ('    "/#/explore/controlled-substances",', '    "/#/explore/promotion-transparency",', '    "/#/explore/otc-compounding",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/pricing-access",\n    "/#/explore/pricing-access",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_pricing_access_py": _write_if_changed(pipe_dir / "build_pricing_access.py", BUILD_PRICING_ACCESS_PY),
        "pricing_access_js": _write_if_changed(js_dir / "pricing_access.js", PRICING_ACCESS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/controlled-substances") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/controlled-substances", "Controlled substances"]] }];\nconst EXPLORE_NAV = [["#/explore/controlled-substances", "Controlled substances"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/controlled-substances",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_pricing_access.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_pricing_access.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ira_medicare_negotiation": 6, "hrsa_340b_program": 6, "medicaid_mdrp": 6, "part_b_asp_benchmarks": 6}, out

        doc = json.loads((root / "site" / "data" / "pricing_access.json").read_text(encoding="utf-8"))
        for k in ("ira_medicare_negotiation", "hrsa_340b_program", "medicaid_mdrp", "part_b_asp_benchmarks"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "pricing_access.js").read_text(encoding="utf-8")
        print("V61Y_PRICING_IRA_340B_MDRP_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1y US Drug Pricing, IRA, 340B & MDRP patch.")
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
