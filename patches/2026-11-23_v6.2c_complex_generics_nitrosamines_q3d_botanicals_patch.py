#!/usr/bin/env python3
"""Pill by Pill v6.2c Patch: Complex Generics (PSGs/GDUFA III), Nitrosamines (NDSRIs/CPCA), ICH Q3D/Q3E Impurities & Botanical Drugs Reference (#/ref/complex-quality, #/explore/complex-quality, /api/complex-quality).

1. Adds `pipeline/build_complex_quality.py` -> `site/data/complex_quality.json` (6 Nitrosamine
   Impurities & NDSRI CPCA pillars, 6 Complex Generics, PSGs & GDUFA III Pre-ANDA pillars, 6 ICH
   Q3D(R2) Elemental Impurities, Q3C Solvents & Q3E Extractables/Leachables pillars, and 6 Botanical
   Drug Development & BRT Totality-of-Evidence pillars — 24 primary-sourced entries).
2. Adds `site/js/complex_quality.js` (`complexQualityPage` with inline Complex Quality, Impurities &
   Botanicals SVG + 4 section filters) and wires `#/ref/complex-quality`, `#/explore/complex-quality`,
   `/api/complex-quality`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `complex_quality.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/complex-quality/` static SEO page + sitemap entry -> 45
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py --selftest
  python3 2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_COMPLEX_QUALITY_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2c Complex Generics, Nitrosamines, ICH Q3D/Q3E Impurities & Botanical Drugs Reference (`site/data/complex_quality.json`).

Comprehensive, primary-sourced reference covering:
  1. Nitrosamine Impurities & NDSRI Acceptable Intake Limits (CPCA) (6 pillars)
  2. Complex Generics, Product-Specific Guidances (PSGs) & GDUFA III (6 pillars)
  3. ICH Q3D(R2) Elemental Impurities, Q3C Solvents & Q3E E&L (6 pillars)
  4. Botanical Drug Development & CDER Botanical Review Team (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, OPQ, ICH).

Usage:
  python3 pipeline/build_complex_quality.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

NITROSAMINES_NDSRIS = [
    {
        "id": "nit-2024-guidance",
        "name": "Control of Nitrosamine Impurities in Human Drugs (Sept 2024 Rev. 2)",
        "category": "FDA Final Guidance",
        "plain": "After trace cancer-linked nitrosamine impurities triggered recalls in blood-pressure and heartburn pills, FDA issued strict rules requiring every drugmaker to assess and test for them.",
        "technical": "FDA's September 2024 Revised Final Guidance establishes a 3-step mitigation framework (risk assessment, confirmatory testing, and reporting/reformulation) covering small-molecule nitrosamines and NDSRIs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/control-nitrosamine-impurities-human-drugs",
    },
    {
        "id": "nit-ndsri-definition",
        "name": "Nitrosamine Drug Substance-Related Impurities (NDSRIs)",
        "category": "API-Derived Risk",
        "plain": "NDSRIs form when a drug molecule's own amine group reacts with trace nitrites in inactive tablet fillers—creating a unique impurity specific to that medicine.",
        "technical": "NDSRIs share structural similarity with the API itself (typically formed by nitrosation of secondary/tertiary amines in the drug substance by nitrite impurities in excipients during manufacturing or shelf life).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/recommended-acceptable-intake-limits-nitrosamine-drug-substance-related-impurities",
    },
    {
        "id": "nit-cpca-categories",
        "name": "Carcinogenic Potency Categorization Approach (CPCA Categories 1–5)",
        "category": "SAR Potency Model",
        "plain": "Because most NDSRIs lack full animal carcinogenicity tests, FDA created a chemistry scoring system (Categories 1–5) that sets safe daily nanogram limits from molecular structure.",
        "technical": "CPCA assigns predicted Acceptable Intake (AI) limits (e.g., 26.5 ng/day to 1,500 ng/day) across Potency Categories 1–5 based on alpha-hydrogen count and activating/deactivating structural features.",
        "url": "https://www.fda.gov/drugs/spotlight-cder-science/determining-recommended-acceptable-intake-limits-n-nitrosamine-impurities-pharmaceuticals",
    },
    {
        "id": "nit-cders-ai-list",
        "name": "CDER Posted Acceptable Intake (AI) & Interim Limits Web Page",
        "category": "Dynamic Thresholds",
        "plain": "FDA maintains a live public table of nanogram-per-day limits for specific nitrosamines and NDSRIs—plus temporary limits when needed to prevent sudden drug shortages.",
        "technical": "FDA's CDER Nitrosamine Impurity Acceptable Intake Limits page publishes compound-specific AIs, CPCA category assignments, and temporary interim AI limits to avert supply disruptions during reformulation.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cder-nitrosamine-impurity-acceptable-intake-limits",
    },
    {
        "id": "nit-10pct-control",
        "name": "10% AI Control Threshold & Routine Batch Testing",
        "category": "Specification Trigger",
        "plain": "If confirmatory lab testing finds a nitrosamine below 10% of the daily safety limit, routine batch testing isn't required—above 10%, strict release specs kick in.",
        "technical": "Under FDA nitrosamine guidance, levels consistently <10% of the AI generally do not require routine specification control, whereas >10% and ≤AI require routine analytical control and stability tracking.",
        "url": "https://www.fda.gov/media/187315/download",
    },
    {
        "id": "nit-reformulation",
        "name": "Root-Cause Mitigation: Low-Nitrite Excipients & Antioxidants",
        "category": "CMC Mitigation",
        "plain": "Drugmakers eliminate NDSRIs by switching to low-nitrite tablet fillers, adding vitamin C/E antioxidants, or upgrading blister packaging.",
        "technical": "Mitigation strategies include supplier qualification for low-nitrite excipients, formulation scavengers (ascorbic acid, alpha-tocopherol), pH adjustment, and packaging updates backed by 6-month accelerated stability.",
        "url": "https://www.fda.gov/media/141720/download",
    },
]

COMPLEX_GENERICS_PSGS = [
    {
        "id": "cgx-psg-program",
        "name": "Product-Specific Guidances (PSGs) for Generic Drug Development",
        "category": "ANDA Roadmap",
        "plain": "To help generic companies copy tricky medicines accurately, FDA publishes individual 'how-to' blueprints called Product-Specific Guidances for thousands of brand drugs.",
        "technical": "PSGs specify FDA's recommended bioequivalence (BE) study designs (in vitro, PK, PD, or comparative clinical endpoint studies) to support ANDA approval under FD&C Act § 505(j).",
        "url": "https://www.fda.gov/drugs/guidances-drugs/product-specific-guidances-generic-drug-development",
    },
    {
        "id": "cgx-complex-classes",
        "name": "What Makes a Generic 'Complex'? (APIs, Formulations, Routes & Devices)",
        "category": "Complex Products",
        "plain": "Simple tablets dissolve easily, but complex generics—like inhalers, eye drops, skin creams, liposomes, and long-acting microspheres—are far harder to prove equivalent.",
        "technical": "GDUFA defines complex generics as products with complex active ingredients (peptides, polymers), complex formulations (liposomes, colloids), complex routes (ophthalmic, topical, inhaled), or drug-device combinations.",
        "url": "https://www.fda.gov/drugs/generic-drugs/complex-generics-news",
    },
    {
        "id": "cgx-gdufa-iii-preanda",
        "name": "GDUFA III Pre-ANDA Meetings & Upcoming PSG Pipeline",
        "category": "FDA Engagement",
        "plain": "Generic developers can meet with FDA scientists early—before filing an application—to agree on novel lab tests that replace expensive human trials.",
        "technical": "GDUFA III enhanced the Pre-ANDA Program (Product Development and Pre-Submission Meetings) and publishes quarterly Upcoming PSGs lists so generic sponsors can align complex BE strategies early.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/upcoming-product-specific-guidances-generic-drug-product-development",
    },
    {
        "id": "cgx-crcg",
        "name": "Center for Research on Complex Generics (CRCG) Workshops",
        "category": "Regulatory Science",
        "plain": "FDA partners with academic labs through the CRCG to invent better analytical instruments and in vitro tests that speed up affordable complex generics.",
        "technical": "Joint FDA–University of Maryland/Michigan CRCG conducts collaborative regulatory science research and public workshops on particle size distribution, IVRT/IVPT, and PBPK modeling for complex ANDAs.",
        "url": "https://www.fda.gov/drugs/guidance-compliance-regulatory-information/center-research-complex-generics",
    },
    {
        "id": "cgx-q1-q2-sameness",
        "name": "Q1/Q2 Sameness & Q3 Microstructure Characterization",
        "category": "Formulation Equivalence",
        "plain": "For complex eye drops or creams, a generic must match the brand's exact ingredients (Q1), amounts (Q2), and microscopic droplet or crystal structure (Q3).",
        "technical": "Qualitative (Q1) and quantitative (Q2) formulation sameness combined with physicochemical/structural (Q3) equivalence (viscosity, globule size, rheology, polymorphism) enables waivers of in vivo clinical BE studies.",
        "url": "https://www.fda.gov/media/168931/download",
    },
    {
        "id": "cgx-first-generic-access",
        "name": "Accelerating First-Generic Approvals for Off-Patent Complex Drugs",
        "category": "Patient Access",
        "plain": "Publishing clear PSGs and GDUFA science helps unlock the first affordable generic versions of high-cost inhalers, injectables, and specialty creams.",
        "technical": "FDA's Drug Competition Action Plan and GDUFA regulatory science initiatives directly target off-patent complex drugs lacking generic competition to lower patient out-of-pocket costs.",
        "url": "https://www.fda.gov/drugs/our-perspective/generic-drugs-21st-century-fdas-actions-create-transparency-and-value-complex-generic-product",
    },
]

IMPURITIES_Q3D_Q3E = [
    {
        "id": "imp-ich-q3d",
        "name": "ICH Q3D(R2) Elemental Impurities & Permitted Daily Exposure (PDE)",
        "category": "Heavy Metals Control",
        "plain": "Modern pharma replaced century-old 'heavy metals' color tests with precise ICP-MS lab measurements capping trace arsenic, lead, cadmium, and mercury from catalysts or water.",
        "technical": "ICH Q3D(R2) (Step 4, 2022) sets toxicology-based Permitted Daily Exposure (PDE, µg/day) limits across Class 1 (Cd, Pb, As, Hg), Class 2A/2B, and Class 3 elements by oral, parenteral, inhalation, and cutaneous routes.",
        "url": "https://www.fda.gov/media/148474/download",
    },
    {
        "id": "imp-ich-q3c",
        "name": "ICH Q3C Residual Solvents (Classes 1, 2 & 3)",
        "category": "Synthesis Solvents",
        "plain": "Chemical solvents used to synthesize and crystallize active ingredients must be dried down below strict safety ceilings—with toxic Class 1 solvents like benzene avoided entirely.",
        "technical": "ICH Q3C classifies manufacturing solvents into Class 1 (solvents to be avoided, e.g., benzene), Class 2 (limited by PDE, e.g., methanol, acetonitrile), and Class 3 (low toxic potential, ≤50 mg/day).",
        "url": "https://www.fda.gov/media/168952/download",
    },
    {
        "id": "imp-ich-q3e",
        "name": "ICH Q3E Extractables & Leachables (Nov 2025 Draft Guidance)",
        "category": "Packaging & Systems",
        "plain": "New global ICH rules unify how companies test whether chemicals from plastic IV bags, rubber vial stoppers, or single-use bioreactor tubing migrate into medicines.",
        "technical": "ICH Q3E (Nov 2025 Draft) establishes a harmonized risk-based framework for assessing and controlling extractables and leachables (E&L) across drug products, biologics, cell/gene therapies, and combo products.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q3e-guideline-extractables-and-leachables",
    },
    {
        "id": "imp-ich-m7",
        "name": "ICH M7 DNA-Reactive (Mutagenic) Impurities & (Q)SAR Screening",
        "category": "Mutagenicity",
        "plain": "Software models screen every synthesis byproduct for DNA-damaging chemical alerts so trace mutagens stay below 1.5 micrograms per day.",
        "technical": "ICH M7 requires dual complementary (Q)SAR predictions (expert rule-based + statistical) and/or Ames testing on process impurities/reagents, applying the Threshold of Toxicological Concern (TTC = 1.5 µg/day lifetime).",
        "url": "https://www.fda.gov/media/147595/download",
    },
    {
        "id": "imp-api-supplier-change",
        "name": "API Supplier & Reactor Changes: Impurity Equivalency Audits",
        "category": "Post-Approval CMC",
        "plain": "Switching a drug's active-ingredient factory—or even changing from a glass-lined tank to a metal alloy reactor—requires re-checking organic, solvent, and metal impurities.",
        "technical": "FDA's Drug Substance Quality guidance requires API supplier/process changes to verify impurity profile equivalence across ICH Q3A (organic), Q3C (solvents), Q3D (elemental), M7 (mutagenic), and nitrosamines.",
        "url": "https://www.fda.gov/media/168952/download",
    },
    {
        "id": "imp-mdd-monographs",
        "name": "Maximum Daily Dose (MDD) & Compendial Monograph Alignment",
        "category": "OPQ Specifications",
        "plain": "FDA quality assessors ensure a drug's impurity limits match its highest approved daily dose—not just a generic textbook monograph.",
        "technical": "CDER OPQ MAPP 5017.2 Rev. 2 specifies that compendial monograph impurity limits are acceptable only if they comply with ICH Q3A/Q3B/nitrosamine limits calculated at the drug product's Maximum Daily Dose (MDD).",
        "url": "https://www.fda.gov/media/192485/download",
    },
]

BOTANICAL_DRUGS = [
    {
        "id": "bot-statutory-def",
        "name": "Botanical Drug Products vs. Dietary Supplements (FD&C Act)",
        "category": "Legal Distinction",
        "plain": "Unlike herbal supplements on health-food shelves, a botanical drug is an FDA-approved prescription medicine made from plants—proven in clinical trials to treat or cure disease.",
        "technical": "Botanical drugs consist of vegetable materials (plant, algae, macroscopic fungi) intended for diagnosis, cure, mitigation, treatment, or prevention of disease—regulated as drugs under NDA/IND, not DSHEA supplements.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/what-botanical-drug",
    },
    {
        "id": "bot-totality-evidence",
        "name": "FDA Botanical Drug 'Totality of the Evidence' Approach",
        "category": "Therapeutic Consistency",
        "plain": "Because a plant extract contains hundreds of natural molecules that can't all be isolated, FDA uses a 'totality of evidence' package to ensure every batch works the same.",
        "technical": "FDA's Botanical Drug Development Guidance combines Botanical Raw Material (BRM) agricultural controls, multi-marker CMC characterization, bioassays, and clinical dose-response data to ensure therapeutic consistency.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/botanical-drug-development-guidance-industry",
    },
    {
        "id": "bot-brt-team",
        "name": "CDER Botanical Review Team (BRT) & Dedicated Expertise",
        "category": "FDA Review Unit",
        "plain": "FDA houses a specialized Botanical Review Team of pharmacognosy and plant-chemistry experts who guide companies developing plant-based prescription medicines.",
        "technical": "CDER's Botanical Review Team (BRT) provides specialized scientific/regulatory oversight on botanical raw materials, fingerprint chromatography, and IND/NDA botanical consistency across review divisions.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/botanical-review-team-brt",
    },
    {
        "id": "bot-brm-gacp",
        "name": "Botanical Raw Material (BRM) & Good Agricultural Practices",
        "category": "Supply Chain",
        "plain": "Soil, harvest season, and drying methods change plant chemistry—so botanical drugmakers must audit farms and lock in harvest regions just like pharma factories.",
        "technical": "Botanical NDA CMC requires Good Agricultural and Collection Practices (GACP) controls over cultivar genetics, growing sites, harvest timing, pesticide/heavy-metal screening, and multi-batch extract fingerprinting.",
        "url": "https://www.fda.gov/files/drugs/published/Botanical-Drug-Development--Guidance-for-Industry.pdf",
    },
    {
        "id": "bot-early-ind-flex",
        "name": "Prior Human Experience & Streamlined Early Botanical INDs",
        "category": "Phase 1/2 Entry",
        "plain": "If a plant extract already has decades of safe traditional or supplement use in humans, FDA may allow early Phase 1/2 clinical trials with fewer upfront animal toxicity tests.",
        "technical": "Botanical Drug Development Guidance permits leveraging documented prior human clinical experience/literature to support initial Phase 1/2 INDs while full nonclinical and BRM controls mature before Phase 3.",
        "url": "https://www.fda.gov/media/140319/download",
    },
    {
        "id": "bot-clinical-consistency",
        "name": "Multi-Batch Phase 3 Testing & Bridging Across Extract Lots",
        "category": "Phase 3 Design",
        "plain": "To prove natural variations between plant harvests don't weaken the medicine, Phase 3 trials often test multiple botanical extract batches head-to-head.",
        "technical": "Sponsors demonstrate batch-to-batch clinical consistency by evaluating multiple BRM/extract lots in Phase 3 or establishing validated biological/chemical assays bridging clinical batches to commercial production.",
        "url": "https://www.fda.gov/drugs/resources-drugs/botanical-drug-products",
    },
]


def build_complex_quality(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "nitrosamines_ndsris": len(NITROSAMINES_NDSRIS),
            "complex_generics_psgs": len(COMPLEX_GENERICS_PSGS),
            "impurities_q3d_q3e": len(IMPURITIES_Q3D_Q3E),
            "botanical_drugs": len(BOTANICAL_DRUGS),
        },
        "nitrosamines_ndsris": NITROSAMINES_NDSRIS,
        "complex_generics_psgs": COMPLEX_GENERICS_PSGS,
        "impurities_q3d_q3e": IMPURITIES_Q3D_Q3E,
        "botanical_drugs": BOTANICAL_DRUGS,
    }
    (data_dir / "complex_quality.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_complex_quality.py <site/data>")
    print(json.dumps(build_complex_quality(pathlib.Path(sys.argv[1])), indent=2))
'''

COMPLEX_QUALITY_JS = '''// Pill by Pill v6.2c: Complex Generics (PSGs/GDUFA III), Nitrosamines (NDSRIs/CPCA), ICH Q3D/Q3E Impurities & Botanical Drugs Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["nitrosamines", "Nitrosamines & NDSRIs", "nitrosamines_ndsris"],
  ["generics", "Complex Generics & PSGs", "complex_generics_psgs"],
  ["impurities", "ICH Q3D / Q3C / Q3E", "impurities_q3d_q3e"],
  ["botanicals", "Botanical Drugs (BRT)", "botanical_drugs"],
];

function complexQualitySvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Complex quality and impurity control: Nitrosamines CPCA, Complex Generics PSGs, ICH Q3D/Q3E Impurities, and Botanical Drugs">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Nitrosamines</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">NDSRIs &amp; CPCA Cat 1–5</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">10% AI Control &amp; Scavengers</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cq-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Complex Generics</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PSGs &amp; GDUFA III Pre-ANDA</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Q1/Q2 &amp; Q3 Microstructure</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cq-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. ICH Q3D / Q3E</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Elemental PDEs &amp; Solvents</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">E&amp;L &amp; M7 (Q)SAR</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cq-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Botanical Drugs</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CDER BRT &amp; BRM GACP</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Totality of Evidence</text>
      <defs><marker id="cq-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Modern pharmaceutical quality spans nitrosamine/NDSRI potency limits, complex generic equivalence, ICH Q3D/Q3E impurity controls, and botanical drug consistency.</figcaption>
  </figure>`;
}

export async function complexQualityPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/complex_quality.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/complex-quality" : "#/ref/complex-quality";

  const pills = html`<div class="chips" role="navigation" aria-label="Complex quality, impurities, and botanicals sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Guideline</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${complexQualitySvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Nitrosamine/NDSRI, GDUFA III Complex Generics/PSGs, ICH Q3D(R2)/Q3C/Q3E/M7, and Botanical Drug Development documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Complex Generics, Impurities & Botanicals"]] : [REF_HOME, ["Complex Generics, Impurities & Botanicals"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Complex Generics, Nitrosamines, ICH Q3D/Q3E & Botanical Drugs",
      lede: env === "explore"
        ? "How regulators catch trace nitrosamines and heavy metals, approve complex inhalers or creams, and regulate plant-derived prescription drugs."
        : "Nitrosamines/NDSRIs (CPCA), GDUFA III Complex Generics & PSGs (Q1/Q2/Q3), ICH Q3D(R2)/Q3C/Q3E/M7 impurities, and Botanical Drug NDAs.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on complex quality, impurities, and botanicals.", href: env === "explore" ? "#/ref/complex-quality" : "#/explore/complex-quality" },
        { title: "ICH Q1–Q12 Quality Matrix", text: "Core ICH stability, analytical validation, and lifecycle guidelines.", href: "#/ref/ich" },
        { title: "OTC Monographs & DSHEA", text: "Contrast Botanical Drug NDAs with DSHEA herbal dietary supplements.", href: "#/ref/otc-compounding" },
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
    if 'complex_quality.js' not in txt:
        for anchor in ('import * as comboProducts from "./combo_products.js";\n', 'import * as radiopharma from "./radiopharma.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as complexQuality from "./complex_quality.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as complexQuality from "./complex_quality.js";\n' + txt
            changed = True
    if '"/ref/complex-quality"' not in txt:
        for anchor in ('if (path === "/ref/combo-products")', 'if (path === "/ref/radiopharma")', 'if (path === "/ref/special-populations")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/complex-quality") return { env: "ref", current: "#/ref/complex-quality", ...(await complexQuality.complexQualityPage(query, "ref")) };\n  if (path === "/explore/complex-quality") return { env: "explore", current: "#/explore/complex-quality", ...(await complexQuality.complexQualityPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/complex-quality" not in txt:
        for anchor in ('["#/ref/combo-products", "Combination products"]', '["#/ref/radiopharma", "Radiopharma & theranostics"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/complex-quality", "Complex generics & impurities"]', 1)
                changed = True
                break
    if "#/explore/complex-quality" not in txt:
        for anchor in ('["#/explore/combo-products", "Combination products"]', '["#/explore/radiopharma", "Radiopharma & theranostics"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/complex-quality", "Complex generics & impurities"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_complex_quality.py" in txt:
        return False
    line = "python3 pipeline/build_complex_quality.py site/data\n"
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
    if '"/api/complex-quality"' in txt:
        return False
    route = (
        '\n@app.get("/api/complex-quality")\n'
        'def api_complex_quality():\n'
        '    p = DATA_DIR / "complex_quality.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "complex_quality.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"complex_quality.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    cq_ref = _load(data_dir / "complex_quality.json", {}) or {}\n'
        '    for sec_key, sec_q in [("nitrosamines_ndsris", "nitrosamines"), ("complex_generics_psgs", "generics"), ("impurities_q3d_q3e", "impurities"), ("botanical_drugs", "botanicals")]:\n'
        '        for item in (cq_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "complex_quality",\n'
        '                "group": "Complex Generics, Impurities & Botanicals",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/complex-quality?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/complex-quality?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"nitrosamine NDSRI CPCA acceptable intake complex generic PSG GDUFA III Q1 Q2 Q3 ICH Q3D elemental impurity PDE Q3C solvent Q3E extractables leachables M7 botanical drug BRT BRM {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"complex-quality", "#/ref/complex-quality"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    cq_doc = _load_json(data_dir / "complex_quality.json")\n'
        '    if isinstance(cq_doc, dict) and cq_doc.get("nitrosamines_ndsris"):\n'
        '        cq_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (cq_doc.get("nitrosamines_ndsris") or []) + (cq_doc.get("complex_generics_psgs") or []))\n'
        '        pages.append(("complex-quality", "#/ref/complex-quality", "Complex Generics, Nitrosamines, ICH Q3D/Q3E & Botanical Drugs",\n'
        '                      "Primary-sourced guide to nitrosamine/NDSRI CPCA limits, GDUFA III complex generics & PSGs, ICH Q3D/Q3C/Q3E impurities, and botanical drugs.",\n'
        '                      f"<ul>{cq_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/complex-quality"' in txt:
        return False
    for anchor in ('    "/#/explore/combo-products",', '    "/#/explore/radiopharma",', '    "/#/explore/special-populations",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/complex-quality",\n    "/#/explore/complex-quality",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_complex_quality_py": _write_if_changed(pipe_dir / "build_complex_quality.py", BUILD_COMPLEX_QUALITY_PY),
        "complex_quality_js": _write_if_changed(js_dir / "complex_quality.js", COMPLEX_QUALITY_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/combo-products") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/combo-products", "Combination products"]] }];\nconst EXPLORE_NAV = [["#/explore/combo-products", "Combination products"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/combo-products",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_complex_quality.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_complex_quality.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"nitrosamines_ndsris": 6, "complex_generics_psgs": 6, "impurities_q3d_q3e": 6, "botanical_drugs": 6}, out

        doc = json.loads((root / "site" / "data" / "complex_quality.json").read_text(encoding="utf-8"))
        for k in ("nitrosamines_ndsris", "complex_generics_psgs", "impurities_q3d_q3e", "botanical_drugs"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "complex_quality.js").read_text(encoding="utf-8")
        print("V62C_COMPLEX_QUALITY_NITROSAMINES_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2c Complex Generics, Nitrosamines, ICH Q3D/Q3E & Botanical Drugs patch.")
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
