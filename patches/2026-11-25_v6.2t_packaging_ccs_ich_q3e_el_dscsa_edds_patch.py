#!/usr/bin/env python3
"""Pill by Pill v6.2t Patch: Pharmaceutical Packaging & Container Closure Systems (CCS), Extractables & Leachables (ICH Q3E), Tamper-Evident/Barcode Controls (21 CFR 211.132 / 201.25), and DSCSA Enhanced Drug Distribution Security (EDDS / EPCIS) Reference (#/ref/packaging-el-dscsa, #/explore/packaging-el-dscsa, /api/packaging-el-dscsa).

1. Adds `pipeline/build_packaging_el_dscsa.py` -> `site/data/packaging_el_dscsa.json`
   (6 CCS & Component Changes pillars, 6 ICH Q3E Extractables & Leachables pillars, 6
   Tamper-Evident/Barcode/OTC Packaging pillars, and 6 DSCSA EDDS/EPCIS pillars — 24
   primary-sourced entries).
2. Adds `site/js/packaging_el_dscsa.js` (`packagingElDscsaPage` with inline Packaging,
   ICH Q3E E&L & DSCSA EDDS SVG + 4 section filters) and wires `#/ref/packaging-el-dscsa`,
   `#/explore/packaging-el-dscsa`, `/api/packaging-el-dscsa`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `packaging_el_dscsa.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/packaging-el-dscsa/` static SEO page + sitemap
   entry -> 62 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py --selftest
  python3 2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PACKAGING_EL_DSCSA_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2t Packaging (CCS), Extractables & Leachables (ICH Q3E), Tamper-Evident & DSCSA EDDS Reference (`site/data/packaging_el_dscsa.json`).

Comprehensive, primary-sourced reference covering:
  1. Container Closure Systems (CCS), Glass/Stopper Changes & Storage (6 pillars)
  2. Extractables & Leachables (ICH Q3E) & Toxicological Thresholds (6 pillars)
  3. Tamper-Evident Packaging (21 CFR 211.132), Barcodes & OTC Labeling (6 pillars)
  4. DSCSA Enhanced Drug Distribution Security (EDDS), EPCIS & Exemptions (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER/CBER/OPQ, ICH).

Usage:
  python3 pipeline/build_packaging_el_dscsa.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-25"

CCS_PACKAGING_211 = [
    {
        "id": "ped-ccs-1999-guidance",
        "name": "Container Closure Systems for Human Drugs & Biologics",
        "category": "CCS Guidance",
        "plain": "Bottles, vials, rubber stoppers, and blister packs must protect medicines from moisture, oxygen, light, and microbes until expiration.",
        "technical": "FDA's Container Closure Systems guidance defines CMC documentation for primary and protective secondary packaging, compatibility, functionality, and safety across oral, sterile, inhalation, and topical dosage forms.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/container-closure-systems-packaging-human-drugs-and-biologics",
    },
    {
        "id": "ped-ccs-2026-draft",
        "name": "2026 Container Closure Systems Draft Guidance (CDER/CBER/OCP)",
        "category": "2026 CCS Update",
        "plain": "Modernized 2026 FDA packaging guidance updates expectations for biologics, combination products, and delivery-device reservoirs.",
        "technical": "FDA's August 2026 Container Closure Systems Draft Guidance updates CMC quality expectations for drug/biologic CCSs, including device constituent parts that store drug or biological products.",
        "url": "https://www.fda.gov/media/194220/download",
    },
    {
        "id": "ped-ccs-biologics-bulk",
        "name": "Biologics Bulk Storage & Shipping Container Suitability",
        "category": "Biologic Storage",
        "plain": "Large stainless or single-use bags that hold biologic drug substance before final bottling must also be proven safe in the application.",
        "technical": "FDA's CCS Q&A specifies that while small-molecule shipping containers rely on CGMP retention data, biologics and protein bulk storage/shipping containers require suitability data inside the BLA.",
        "url": "https://www.fda.gov/media/70794/download",
    },
    {
        "id": "ped-ccs-glass-vials",
        "name": "Container Closure Component Changes: Glass Vials & Stoppers",
        "category": "Component Changes",
        "plain": "Switching glass vial suppliers or rubber stoppers requires targeted compatibility and integrity checks to prevent glass delamination or leaks.",
        "technical": "FDA's Component Changes guidance addresses post-approval transitions in glass vials, elastomeric stoppers, and seals—evaluating extractables, CCI, and stability without disrupting supply.",
        "url": "https://www.fda.gov/media/167925/download",
    },
    {
        "id": "ped-ccs-vs-device",
        "name": "Containers & Closures vs. Delivery Devices (21 CFR 4 & 211)",
        "category": "21 CFR Part 4",
        "plain": "A plain bottle only holds a drug, whereas a prefilled syringe or inhaler delivers it—triggering medical device quality rules too.",
        "technical": "Under 21 CFR Part 4, FDA distinguishes mere containers/closures (21 CFR Part 211 only) from container closures that also deliver the drug, which are regulated as combination product device constituents.",
        "url": "https://www.fda.gov/media/90425/download",
    },
    {
        "id": "ped-ccs-ophthalmic-771",
        "name": "Topical Ophthalmic Packaging, Preservatives & USP <771>",
        "category": "Ophthalmic / USP <771>",
        "plain": "Eye drop bottles must keep drops sterile across weeks of squeezing and prevent packaging chemicals from irritating the eye.",
        "technical": "FDA's Quality Considerations for Topical Ophthalmic Drug Products integrates 21 CFR 200.50, USP <771>, container leachables, and multi-dose antimicrobial preservative controls.",
        "url": "https://www.fda.gov/media/172937/download",
    },
]

EXTRACTABLES_LEACHABLES_Q3E = [
    {
        "id": "ped-ich-q3e-2025",
        "name": "ICH Q3E Guideline for Extractables and Leachables (Nov 2025)",
        "category": "ICH Q3E Draft",
        "plain": "Tiny chemicals can slowly migrate from plastic tubing, rubber stoppers, or labels into liquid medicines—ICH Q3E sets global rules to control them.",
        "technical": "FDA's November 2025 ICH Q3E Draft Guidance establishes a harmonized, risk-based framework for assessing and controlling extractables and leachables (E&L) across new drugs, biologics, CGTs, and combination products.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q3e-guideline-extractables-and-leachables",
    },
    {
        "id": "ped-q3e-risk-matrix",
        "name": "ICH Q3E Risk Matrix, Leaching Propensity & Simulated Studies",
        "category": "E&L Risk Matrix",
        "plain": "Solvents, surfactants, and long storage times increase leaching risk—guiding how aggressively labs must test packaging materials.",
        "technical": "ICH Q3E pairs formulation leaching propensity (pH, co-solvents, surfactants) with clinical route, dose frequency, and treatment duration to determine simulated leachable and migration testing.",
        "url": "https://www.fda.gov/media/189890/download",
    },
    {
        "id": "ped-q3e-class3-monographs",
        "name": "ICH Q3E Class 3 Leachable Monographs Supporting Documentation",
        "category": "Class 3 Monographs",
        "plain": "Reference safety monographs list acceptable daily limits for common plasticizers, antioxidants, and rubber additives.",
        "technical": "ICH Q3E's Class 3 Leachable Monographs provide standardized toxicological derivations and Permitted Daily Exposures (PDEs) for recurring packaging and manufacturing-system leachables.",
        "url": "https://www.fda.gov/media/189891/download",
    },
    {
        "id": "ped-generic-el-aet-sct",
        "name": "Generic E&L Safety Assessment: AET, SCT & Controlled Correspondence",
        "category": "OGD E&L Review",
        "plain": "Sensitive routes like spinal or eye injections require ultra-low analytical detection thresholds so trace leachables cannot slip through.",
        "technical": "OGD's E&L review standards evaluate Analytical Evaluation Thresholds (AET), Safety Concern Thresholds (e.g., 0.15 µg/day for sensitive routes), and Controlled Correspondences for MDD/E&L queries.",
        "url": "https://www.fda.gov/media/194101/download",
    },
    {
        "id": "ped-ccs-cmc-stability",
        "name": "Packaging CMC Integration & Stability Verification",
        "category": "Packaging CMC",
        "plain": "Real-time stability batches stored in the final commercial bottle confirm that packaging protects the drug throughout shelf life.",
        "technical": "FDA's CCS framework links primary packaging specifications and material compatibility directly to formal stability protocols verifying strength, purity, and container integrity.",
        "url": "https://www.fda.gov/media/70788/download",
    },
    {
        "id": "ped-ccs-supply-continuity",
        "name": "Container Closure Component Equivalency & Supply Continuity",
        "category": "Supply Resilience",
        "plain": "Standardized risk-based testing lets factories qualify backup vial or stopper suppliers quickly during global glass shortages.",
        "technical": "FDA's CCS component-change framework outlines comparability assessments—headspace, dye/deterministic CCI, and extractables screening—to qualify alternative primary packaging components.",
        "url": "https://www.fda.gov/media/146428/download",
    },
]

TEP_BARCODES_OTC = [
    {
        "id": "ped-tep-21cfr211-132",
        "name": "Tamper-Evident Packaging (21 CFR 211.132) & Label Statements",
        "category": "21 CFR 211.132",
        "plain": "Foil induction seals, shrink bands, and blister packs make it immediately obvious if an over-the-counter bottle was opened before purchase.",
        "technical": "21 CFR 211.132 mandates tamper-evident packaging with a distinctive design indicator and prominent labeling alert on OTC human drugs (and applicable OTC combination products).",
        "url": "https://www.fda.gov/media/72441/download",
    },
    {
        "id": "ped-barcodes-201-25",
        "name": "Linear Bar Codes (21 CFR 201.25), Lot Numbers & NDC Placement",
        "category": "21 CFR 201.25",
        "plain": "Every hospital-administered drug package carries a machine-readable NDC barcode so nurses can scan the right drug and dose at the bedside.",
        "technical": "21 CFR 201.25 requires linear NDC bar codes on prescription and select OTC drugs, paired with 21 CFR 201.18 lot/control numbers and 21 CFR 207.35 NDC formatting.",
        "url": "https://www.fda.gov/drugs/how-drugs-are-developed-and-approved/ophthalmic-dosage-form-questions-0",
    },
    {
        "id": "ped-otc-drug-facts-pack",
        "name": "OTC Drug Facts Packaging Format & Lot-Specific Excipients",
        "category": "21 CFR 201.66",
        "plain": "Standardized Drug Facts boxes on OTC cartons keep active ingredients, warnings, and dosing easy to read even on small bottles.",
        "technical": "21 CFR 201.66 enforces ≥6-point minimum type, standardized headings, and cGMP batch traceability (21 CFR Part 211) whenever alternative inactive ingredients vary across packaged lots.",
        "url": "https://www.fda.gov/media/76481/download",
    },
    {
        "id": "ped-kit-packaging-part4",
        "name": "Co-Packaged Kits & Combination Product Packaging Inspections",
        "category": "Co-Packaged Kits",
        "plain": "When a drug vial and syringe are boxed together as a kit, FDA inspects both drug and device packaging controls.",
        "technical": "Under 21 CFR 4.2 and FDA's Combination Products Inspection Program, co-packaged kits trigger streamlined Part 4 cGMP oversight covering both 21 CFR Part 211 and device QS requirements.",
        "url": "https://www.fda.gov/media/138592/download",
    },
    {
        "id": "ped-ophthalmic-cap-colors",
        "name": "Uniform Cap Color Coding for Topical Ophthalmic Medications",
        "category": "Ophthalmic Safety",
        "plain": "Standardized cap colors help eye-drop patients and clinicians tell glaucoma, dilation, and steroid bottles apart at a glance.",
        "technical": "FDA's CCS Q&A references the American Academy of Ophthalmology (AAO) uniform cap-and-label color-coding system to reduce wrong-drop medication errors.",
        "url": "https://www.fda.gov/media/70794/download",
    },
    {
        "id": "ped-pressurized-aerosol-pack",
        "name": "Pressurized Dispenser Warnings & Container Labeling",
        "category": "Aerosol Packaging",
        "plain": "Pressurized spray cans and inhalers must carry clear warnings not to puncture or incinerate the container.",
        "technical": "Under 21 CFR 201.66(c)(5)(vi) and 369.21, drugs in pressurized dispensers must display standardized flammability, puncture, and storage-temperature warnings on the package label.",
        "url": "https://www.fda.gov/media/72441/download",
    },
]

DSCSA_EDDS_EPCIS = [
    {
        "id": "ped-dscsa-edds-package",
        "name": "Enhanced Drug Distribution Security (EDDS) at the Package Level",
        "category": "DSCSA § 582",
        "plain": "Every individual prescription drug box carries a unique 2D barcode serial number tracked electronically from factory to pharmacy.",
        "technical": "DSCSA § 582(g)(1) (21 U.S.C. 360eee-1) requires interoperable, electronic package-level product tracing, verification, and suspect-product investigation across all Authorized Trading Partners.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/enhanced-drug-distribution-security-package-level-under-drug-supply-chain-security-act",
    },
    {
        "id": "ped-dscsa-epcis-arch",
        "name": "GS1 EPCIS Interoperable Electronic Tracing Architecture",
        "category": "GS1 EPCIS",
        "plain": "Manufacturers, wholesalers, and pharmacies exchange standardized EPCIS shipment events so every handoff is digitally verified.",
        "technical": "FDA's EDDS and DSCSA Standards guidances recommend GS1 Electronic Product Code Information Services (EPCIS) to exchange Transaction Information (TI) and Transaction Statements (TS) securely.",
        "url": "https://www.fda.gov/media/171666/download",
    },
    {
        "id": "ped-dscsa-ti-ts-standards",
        "name": "DSCSA Standards for Interoperable Transaction Information Exchange",
        "category": "Interoperable TI/TS",
        "plain": "Standardized digital data formats prevent incompatible software systems from delaying critical hospital and pharmacy deliveries.",
        "technical": "FDA's DSCSA Standards guidance defines technical attributes for machine-readable 2D DataMatrix product identifiers (GTIN, serial, lot, expiration) and interoperable TI/TS data exchange.",
        "url": "https://www.fda.gov/media/171796/download",
    },
    {
        "id": "ped-dscsa-tracing-faqs",
        "name": "DSCSA Product Tracing & Salable Returns Verification FAQs",
        "category": "Tracing & VRS",
        "plain": "Before a wholesaler can resell a returned medicine box, it must verify the serial number directly against the manufacturer's database.",
        "technical": "FDA's DSCSA Product Tracing FAQs clarify package-level verification via Verification Router Services (VRS), aggregation inference, and Authorized Trading Partner (ATP) licensure checks.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/drug-supply-chain-security-act-product-tracing-requirements-frequently-asked-questions",
    },
    {
        "id": "ped-dscsa-exemptions",
        "name": "DSCSA Exemptions & Small Dispenser Waivers (§ 582)",
        "category": "Waivers & Exemptions",
        "plain": "FDA grants targeted phased exemptions so smaller independent pharmacies can upgrade scanning software without disrupting patient refills.",
        "technical": "Under DSCSA § 582(a)(3), FDA administers waivers, exceptions, and exemptions—including small-dispenser EDDS transition relief—documented on FDA's DSCSA Exemptions portal.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act",
    },
    {
        "id": "ped-dscsa-supply-integrity",
        "name": "Supply Chain Integrity: Detecting Counterfeit & Diverted Packs",
        "category": "Anti-Counterfeit",
        "plain": "Package-level serial verification blocks counterfeit, stolen, or contaminated boxes from ever reaching pharmacy shelves.",
        "technical": "FDA's DSCSA distribution framework requires quarantine and 24-hour Form FDA 3911 notification when trading partners identify illegitimate or counterfeit serialized packages.",
        "url": "https://www.fda.gov/media/165681/download",
    },
]


def build_packaging_el_dscsa(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2t",
        "checked": CHECKED,
        "ccs_packaging_211": CCS_PACKAGING_211,
        "extractables_leachables_q3e": EXTRACTABLES_LEACHABLES_Q3E,
        "tep_barcodes_otc": TEP_BARCODES_OTC,
        "dscsa_edds_epcis": DSCSA_EDDS_EPCIS,
    }
    (out_dir / "packaging_el_dscsa.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "ccs_packaging_211": len(CCS_PACKAGING_211),
        "extractables_leachables_q3e": len(EXTRACTABLES_LEACHABLES_Q3E),
        "tep_barcodes_otc": len(TEP_BARCODES_OTC),
        "dscsa_edds_epcis": len(DSCSA_EDDS_EPCIS),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_packaging_el_dscsa(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

PACKAGING_EL_DSCSA_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderPackagingSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Pharmaceutical packaging CCS, ICH Q3E Extractables and Leachables, Tamper-Evident controls, and DSCSA EDDS serialization">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. Container Closures</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">2026 CCS Draft &amp; Vials</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">Biologics Bulk Storage</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">Part 4 Device Delivery</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">21 CFR 211.94 / USP &lt;771&gt;</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. ICH Q3E E&amp;L</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">Extractables &amp; Leachables</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">Class 3 PDE Monographs</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">AET &amp; SCT (0.15 µg/d)</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Nov 2025 ICH Q3E</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. TEP &amp; Barcodes</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">21 CFR 211.132 Seals</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">21 CFR 201.25 NDC Scan</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">Drug Facts &amp; Cap Color</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Patient-Level Safety</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. DSCSA EDDS</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">2D DataMatrix Serial</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">GS1 EPCIS TI / TS</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">VRS &amp; Form 3911</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">FD&amp;C Act § 582(g)(1)</text>
      </svg>
    </div>`;
}

function renderSection(items, exploreMode) {
  return `<div class="grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;margin:.75rem 0 1.5rem">
    ${items.map(it => `
      <article class="panel" style="padding:1rem;border:1px solid var(--border,#d8dee6);border-radius:10px;background:var(--paper,#fff)">
        <div style="font-size:.78rem;font-weight:700;color:var(--accent,#1d4ed8);margin-bottom:.25rem">${esc(it.category || "")}</div>
        <h3 style="margin:.1rem 0 .45rem;font-size:1rem">${esc(it.name)}</h3>
        <p style="margin:0 0 .6rem;font-size:.92rem;line-height:1.45">${esc(exploreMode ? it.plain : it.technical)}</p>
        <a href="${esc(it.url)}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem">Official FDA / ICH source ↗</a>
      </article>`).join("")}
  </div>`;
}

export async function packagingElDscsaPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/packaging_el_dscsa.json");
  const sections = [
    { key: "ccs_packaging_211", title: "1. Container Closure Systems (CCS), Component Changes & Storage", items: data.ccs_packaging_211 || [] },
    { key: "extractables_leachables_q3e", title: "2. Extractables & Leachables (ICH Q3E) & Toxicological Thresholds", items: data.extractables_leachables_q3e || [] },
    { key: "tep_barcodes_otc", title: "3. Tamper-Evident Packaging (21 CFR 211.132), Barcodes & OTC Labeling", items: data.tep_barcodes_otc || [] },
    { key: "dscsa_edds_epcis", title: "4. DSCSA Enhanced Drug Distribution Security (EDDS), EPCIS & Exemptions", items: data.dscsa_edds_epcis || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Packaging &amp; Serialization" : "Reference · Packaging &amp; Serialization"}</p>
        <h1>Packaging (CCS), Extractables &amp; Leachables (ICH Q3E) &amp; DSCSA EDDS</h1>
        <p class="lede">${exploreMode
          ? "How pharmaceutical bottles, vials, tamper-evident seals, chemical safety checks, and digital 2D serial barcodes protect every medicine to the pharmacy."
          : "Primary-sourced reference covering 21 CFR 211.94 &amp; 2026 CCS Draft, ICH Q3E Extractables &amp; Leachables, 21 CFR 211.132/201.25 TEP &amp; barcodes, and DSCSA § 582 EDDS/EPCIS."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-25")} · <a href="#/${exploreMode ? "ref" : "explore"}/packaging-el-dscsa">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderPackagingSvg()}
      <div class="filter-bar" role="group" aria-label="Filter packaging, ICH Q3E, tamper-evident, and DSCSA sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["ccs_packaging_211", "CCS Packaging (6)"], ["extractables_leachables_q3e", "ICH Q3E E&L (6)"], ["tep_barcodes_otc", "TEP & Barcodes (6)"], ["dscsa_edds_epcis", "DSCSA EDDS (6)"]].map(([k, lbl]) => `
          <button type="button" class="btn ${active === k ? "btn-primary" : "btn-secondary"}" data-sec="${k}">${esc(lbl)}</button>`).join("")}
      </div>
      ${visible.map(s => `<h2>${esc(s.title)}</h2>${renderSection(s.items, exploreMode)}`).join("")}
    `;
    container.querySelectorAll("[data-sec]").forEach(btn => {
      btn.addEventListener("click", () => {
        active = btn.getAttribute("data-sec");
        draw();
      });
    });
  };
  draw();
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
    imp = 'import { packagingElDscsaPage } from "./packaging_el_dscsa.js";\n'
    if "packagingElDscsaPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/packaging-el-dscsa") return packagingElDscsaPage(view, "ref");\n'
        '  if (path === "/explore/packaging-el-dscsa") return packagingElDscsaPage(view, "explore");\n'
    )
    if '"/ref/packaging-el-dscsa"' not in txt:
        anchor = 'if (path === "/ref/discovery-sbdd-protacs")'
        if anchor in txt:
            txt = txt.replace(anchor, route_snip + "  " + anchor, 1)
        else:
            txt += "\n" + route_snip
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "#/ref/packaging-el-dscsa" not in txt:
        anchor = '["#/ref/discovery-sbdd-protacs"'
        item = '["#/ref/packaging-el-dscsa", "Packaging, ICH Q3E & DSCSA"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/packaging-el-dscsa" not in txt:
        anchor2 = '["#/explore/discovery-sbdd-protacs"'
        item2 = '["#/explore/packaging-el-dscsa", "Packaging, ICH Q3E & DSCSA"], '
        if anchor2 in txt:
            txt = txt.replace(anchor2, item2 + anchor2, 1)
        else:
            txt += f'\n// {item2}\n'
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    line = "python3 pipeline/build_packaging_el_dscsa.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/packaging-el-dscsa"' in txt:
        return False
    block = (
        '\n@app.get("/api/packaging-el-dscsa")\n'
        'def api_packaging_el_dscsa():\n'
        '    p = DATA_DIR / "packaging_el_dscsa.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "packaging_el_dscsa.json" in txt:
        return False
    snippet = '''    ped_path = data_dir / "packaging_el_dscsa.json"
    if ped_path.is_file():
        ped_doc = json.loads(ped_path.read_text(encoding="utf-8"))
        for sec in ("ccs_packaging_211", "extractables_leachables_q3e", "tep_barcodes_otc", "dscsa_edds_epcis"):
            for item in ped_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Packaging, ICH Q3E & DSCSA",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/packaging-el-dscsa",
                })
'''
    anchor = '    payload = {"checked":'
    if anchor in txt:
        txt = txt.replace(anchor, snippet + "\n" + anchor, 1)
    else:
        txt = txt.rstrip() + "\n" + snippet
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "/packaging-el-dscsa/" in txt:
        return False
    snippet = '''    # v6.2t Packaging CCS, ICH Q3E E&L, Tamper-Evident & DSCSA EDDS SEO landing page
    ped_dir = site_dir / "packaging-el-dscsa"
    ped_dir.mkdir(parents=True, exist_ok=True)
    (ped_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Packaging (CCS), Extractables &amp; Leachables (ICH Q3E) &amp; DSCSA EDDS | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to 21 CFR 211.94 CCS, ICH Q3E Extractables &amp; Leachables, 21 CFR 211.132/201.25 TEP &amp; barcodes, and DSCSA EDDS/EPCIS.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/packaging-el-dscsa/'>"
        "<script>location.replace('/#/explore/packaging-el-dscsa');</script>"
        "</head><body><h1>Packaging (CCS), Extractables &amp; Leachables (ICH Q3E) &amp; DSCSA EDDS</h1>"
        "<p><a href='/#/explore/packaging-el-dscsa'>Explore</a> · <a href='/#/ref/packaging-el-dscsa'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/packaging-el-dscsa/")
'''
    anchor = "    written_urls = []"
    if anchor in txt:
        txt = txt.replace(anchor, anchor + "\n" + snippet, 1)
    else:
        txt = txt.rstrip() + "\n" + snippet
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "#/ref/packaging-el-dscsa" in txt:
        return False
    anchor = '"/#/explore/discovery-sbdd-protacs",'
    add = '"/#/explore/discovery-sbdd-protacs",\n    "/#/ref/packaging-el-dscsa",\n    "/#/explore/packaging-el-dscsa",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/packaging-el-dscsa /#/explore/packaging-el-dscsa\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_packaging_el_dscsa_py": _write_if_changed(pipe_dir / "build_packaging_el_dscsa.py", BUILD_PACKAGING_EL_DSCSA_PY),
        "packaging_el_dscsa_js": _write_if_changed(js_dir / "packaging_el_dscsa.js", PACKAGING_EL_DSCSA_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/discovery-sbdd-protacs") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/discovery-sbdd-protacs", "Discovery: qHTS, SBDD & PROTACs"]] }];\nconst EXPLORE_NAV = [["#/explore/discovery-sbdd-protacs", "Discovery: qHTS, SBDD & PROTACs"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/discovery-sbdd-protacs",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_packaging_el_dscsa.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_packaging_el_dscsa.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ccs_packaging_211": 6, "extractables_leachables_q3e": 6, "tep_barcodes_otc": 6, "dscsa_edds_epcis": 6}, out

        doc = json.loads((root / "site" / "data" / "packaging_el_dscsa.json").read_text(encoding="utf-8"))
        for k in ("ccs_packaging_211", "extractables_leachables_q3e", "tep_barcodes_otc", "dscsa_edds_epcis"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "packaging_el_dscsa.js").read_text(encoding="utf-8")
        print("V62T_PACKAGING_EL_DSCSA_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2t Packaging CCS, ICH Q3E E&L & DSCSA EDDS patch.")
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
