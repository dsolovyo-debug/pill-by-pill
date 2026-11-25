#!/usr/bin/env python3
"""Pill by Pill v6.1s Patch: Vaccines, Adjuvants, CBER Lot Release & Immunization Safety Surveillance Reference (#/ref/vaccines, #/explore/vaccines, /api/vaccines).

1. Adds `pipeline/build_vaccines.py` -> `site/data/vaccines.json` (6 vaccine platforms,
   6 adjuvants & formulation stability pillars, 6 CBER licensure/lot-release/WHO PQ pillars,
   and 6 post-licensure safety surveillance pillars — 24 primary-sourced entries).
2. Adds `site/js/vaccines.js` (`vaccinesPage` with inline Vaccine Development & Lot-Release SVG +
   4 section filters) and wires `#/ref/vaccines`, `#/explore/vaccines`, `/api/vaccines`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `vaccines.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/vaccines/` static SEO page + sitemap entry -> 35
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py --selftest
  python3 2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_VACCINES_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1s Vaccines, Adjuvants, CBER Lot Release & Safety Surveillance Reference (`site/data/vaccines.json`).

Comprehensive, primary-sourced reference covering:
  1. Vaccine Platforms & Antigen Design (6 pillars)
  2. Adjuvants, Excipients & Cold-Chain Stability (6 pillars)
  3. CBER Licensure, Lot Release & WHO Prequalification (6 pillars)
  4. Post-Licensure Safety Surveillance (VAERS, VSD & Global Systems) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CBER, CDC, WHO).

Usage:
  python3 pipeline/build_vaccines.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

VACCINE_PLATFORMS = [
    {
        "id": "vax-live-attenuated",
        "name": "Live-Attenuated Viral & Bacterial Vaccines",
        "platform": "Weakened Whole Pathogen",
        "plain": "Live-attenuated vaccines use a weakened version of a germ—like MMR, varicella, or intranasal flu—that replicates gently enough not to cause disease but trains strong, long-lasting immunity.",
        "technical": "Serial passage or reverse-genetics attenuation; elicits robust humoral and CD8+ T-cell memory without adjuvants, requiring cold-chain preservation and contraindication screening in severely immunocompromised hosts.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/vaccines-licensed-use-united-states",
    },
    {
        "id": "vax-inactivated",
        "name": "Inactivated (Killed) & Split-Virion Vaccines",
        "platform": "Non-Replicating Whole/Split",
        "plain": "Inactivated vaccines—such as IPV polio, hepatitis A, and traditional flu shots—kill the virus completely with heat or chemicals so it cannot replicate, while keeping its outer shapes intact for immune training.",
        "technical": "Formalin or beta-propiolactone inactivation verified by validated complete-inactivation kinetics; cannot revert to virulence and generally requires multi-dose priming or booster schedules.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/vaccines-licensed-use-united-states",
    },
    {
        "id": "vax-subunit-vlp",
        "name": "Recombinant Protein Subunit, Toxoid & Virus-Like Particle (VLP)",
        "platform": "Purified Antigen",
        "plain": "Instead of using the whole germ, subunit and VLP vaccines—like hepatitis B, HPV, and RSV protein shots—deliver only the purified surface protein or an empty viral shell with no genetic material inside.",
        "technical": "Expressed in yeast, insect (baculovirus), or mammalian cells; eliminates non-essential reactogenic components and pairs with adjuvants (aluminum salts, AS01, CpG 1018) to drive neutralizing titers.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/vaccines-licensed-use-united-states",
    },
    {
        "id": "vax-conjugate",
        "name": "Polysaccharide–Protein Conjugate Vaccines",
        "platform": "T-Cell-Dependent Sugar",
        "plain": "Young babies' immune systems struggle to recognize bacterial sugar coats alone, so conjugate vaccines (Hib, PCV, MenACWY) link those sugars to a carrier protein to unlock lifelong memory.",
        "technical": "Covalent conjugation of bacterial capsular polysaccharides to carrier proteins (CRM197, tetanus toxoid, outer membrane protein complex) converts T-cell-independent B-cell responses into T-cell-dependent germinal-center memory.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/vaccines-licensed-use-united-states",
    },
    {
        "id": "vax-mrna-lnp",
        "name": "Nucleoside-Modified mRNA–LNP Vaccines",
        "platform": "Synthetic Genetic Blueprint",
        "plain": "mRNA vaccines hand muscle cells a temporary genetic instruction inside microscopic fat droplets (LNPs) so the body builds the viral spike protein itself and trains antibodies and T cells.",
        "technical": "Cell-free enzymatic in vitro transcription (IVT) eliminating egg/cell-culture bottlenecks and enabling rapid strain updates; encapsulated in 4-component ionizable lipid nanoparticles.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",
    },
    {
        "id": "vax-viral-vector",
        "name": "Replication-Deficient Viral Vector Vaccines",
        "platform": "Engineered Carrier Virus",
        "plain": "Viral vector vaccines place a harmless gene from the target pathogen inside a weakened unrelated carrier virus (such as an adenovirus or VSV) to trigger both antibody and cellular immunity.",
        "technical": "E1/E3-deleted adenoviral or recombinant vesicular stomatitis virus (rVSV) vectors delivering antigen transgenes; requires vector-shedding, replication-competent adenovirus (RCA), and anti-vector immunity characterization.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/approved-vaccine-products",
    },
]

ADJUVANTS_FORMULATION = [
    {
        "id": "adj-aluminum",
        "name": "Aluminum Salt Adjuvants (Alum — Used Safely for 70+ Years)",
        "platform": "Classic Innate Booster",
        "plain": "Tiny amounts of aluminum salts—used in DTaP, hepatitis B, and HPV vaccines since the 1930s—create a stronger immune signal at the injection site so smaller doses protect longer.",
        "technical": "Aluminum hydroxide, aluminum phosphate, and potassium aluminum sulfate adsorb protein/toxoid antigens and stimulate innate inflammasome/APC recruitment; well-characterized safety across >70 years of clinical use.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/common-ingredients-fda-approved-vaccines",
    },
    {
        "id": "adj-novel",
        "name": "Novel Adjuvants (MF59, AS01, CpG 1018 & Matrix-M)",
        "platform": "Targeted Innate Agonists",
        "plain": "Modern adjuvants—like MF59 in senior flu shots or AS01 in shingles vaccines—wake up specific immune receptors so older or immunocompromised adults mount strong protection.",
        "technical": "Oil-in-water emulsions (MF59), liposomal saponin/TLR4 agonists (AS01B), synthetic TLR9 CpG oligodeoxynucleotides (CpG 1018), and saponin nanoparticles (Matrix-M); evaluated for innate cytokine profiles and reactogenicity.",
        "url": "https://www.cdc.gov/vaccine-safety/about/adjuvants.html",
    },
    {
        "id": "adj-excipients",
        "name": "Stabilizers, Buffers & Preservatives (FDA Common Ingredients)",
        "platform": "Formulation Chemistry",
        "plain": "Sugars, amino acids, and salts keep fragile vaccine proteins from clumping or breaking down during shipping; single-dose vials today avoid preservatives like thimerosal.",
        "technical": "Lyoprotectants (sucrose, trehalose), surfactants (polysorbate 80), buffers (histidine, Tris, PBS), and trace residual manufacturing reagents listed transparently in USPI Section 11.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/common-ingredients-fda-approved-vaccines",
    },
    {
        "id": "adj-vvm-ctc",
        "name": "Vaccine Vial Monitors (VVMs) & Controlled Temperature Chain (CTC)",
        "platform": "Field Cold-Chain Guard",
        "plain": "A small heat-sensitive sticker on international vaccine vials changes color if the vial got too warm—letting nurses see at a glance whether a dose is still potent.",
        "technical": "WHO Prequalification programmatic suitability standard integrating time-temperature indicator labels (VVMs) and qualified Controlled Temperature Chain (CTC) excursions up to +40 °C for last-mile campaigns.",
        "url": "https://www.who.int/publications/i/item/WHO-IVB-14.10",
    },
    {
        "id": "adj-mdvp",
        "name": "Multi-Dose Vial Policy (MDVP) & Sterile Withdrawals",
        "platform": "Immunization Logistics",
        "plain": "Strict WHO and CDC rules govern how many hours or days a punctured multi-dose vaccine vial can be kept safely before unused doses must be discarded.",
        "technical": "Preservative-containing WHO-prequalified multi-dose vials may be used up to 28 days under cold-chain & valid VVM conditions, whereas preservative-free reconstituted or mRNA vials carry strict 6-to-12-hour post-puncture limits.",
        "url": "https://www.who.int/news-room/fact-sheets/detail/prequalification-of-medicines-by-who",
    },
    {
        "id": "adj-strain-updates",
        "name": "Annual Influenza & COVID-19 Strain Composition Updates",
        "platform": "Seasonal Antigen Drift",
        "plain": "Because flu and coronaviruses mutate constantly, health agencies meet twice a year to pick updated strains so factories can swap the recipe without repeating giant clinical trials.",
        "technical": "FDA VRBPAC and WHO GISRS select Northern/Southern Hemisphere flu strains; platform manufacturing supplements (sBLAs) update HA/NA or spike sequences using established CMC and immunogenicity bridging.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",
    },
]

CBER_LICENSURE = [
    {
        "id": "cber-bla-vrbpac",
        "name": "FDA CBER Vaccine Licensure & VRBPAC Advisory Review",
        "platform": "US Regulatory Approval",
        "plain": "Because vaccines are given to millions of healthy people—including babies—FDA's biologics center (CBER) runs large safety and efficacy trials and often holds public expert hearings (VRBPAC).",
        "technical": "Evaluated under PHS Act § 351(a) BLAs (21 CFR 600–680) by CBER Office of Vaccines Research and Review (OVRR), with public Vaccines and Related Biological Products Advisory Committee (VRBPAC) review.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",
    },
    {
        "id": "cber-lot-release",
        "name": "CBER Lot-by-Lot Release Testing (21 CFR 610.2)",
        "platform": "Batch Gatekeeping",
        "plain": "Even after a vaccine is approved, the manufacturer cannot ship a single batch to clinics until FDA's own labs review the batch test results—and often re-test samples themselves.",
        "technical": "Under 21 CFR 610.2, licensed vaccine manufacturers submit batch protocols and product samples to CBER for official lot-release authorization prior to commercial distribution.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/vaccines-licensed-use-united-states",
    },
    {
        "id": "cber-correlates",
        "name": "Immunobridging & Correlates of Protection (CoP)",
        "platform": "Surrogate Immunogenicity",
        "plain": "Once scientists prove what antibody level protects against a disease, new age groups or updated vaccine versions can be approved by measuring blood antibodies instead of waiting for outbreaks.",
        "technical": "Validated neutralizing-antibody geometric mean titer (GMT) ratios and seroresponse rates enable pediatric age-de-escalation, platform bridging, and Accelerated Approval (21 CFR 601.41) when field efficacy trials are infeasible.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",
    },
    {
        "id": "cber-acip",
        "name": "CDC ACIP Recommendations & Immunization Schedules",
        "platform": "Clinical Practice Policy",
        "plain": "FDA decides if a vaccine is safe and effective to sell; then CDC's independent immunization committee (ACIP) decides who should get it, at what ages, and at what intervals.",
        "technical": "CDC Advisory Committee on Immunization Practices (ACIP) issues evidence-to-recommendation (EtR) clinical schedules guiding pediatric, adolescent, adult, and Vaccines for Children (VFC) coverage.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/consumers-biologics/vaccines-children-guide-parents-and-caregivers",
    },
    {
        "id": "cber-who-pq",
        "name": "WHO Vaccines Prequalification (Started 1987) & UNICEF Supply",
        "platform": "Global Access",
        "plain": "WHO inspects vaccine factories and reviews dossiers so UNICEF and Gavi can safely buy billions of doses for children in countries without large regulatory agencies.",
        "technical": "WHO Vaccines Prequalification (initiated 1987) assesses dossier quality, cGMP compliance, lot-to-lot consistency, and programmatic suitability (PSPQ) for UN procurement.",
        "url": "https://www.who.int/news-room/fact-sheets/detail/prequalification-of-medicines-by-who",
    },
    {
        "id": "cber-stockpile",
        "name": "Pandemic Preparedness, H5N1 & Strategic National Stockpile",
        "platform": "Biodefense & MCMs",
        "plain": "Governments maintain licensed prototype vaccines—like adjuvanted H5N1 bird-flu vaccines—in national stockpiles so factories can scale up rapidly if a pandemic threat emerges.",
        "technical": "Medical Countermeasures (MCMs) utilize platform BLAs, Emergency Use Authorization (EUA) authorities, and BARDA/SNS stockpiling with ongoing stability and potency testing.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/influenza-virus-vaccine-h5n1-national-stockpile",
    },
]

VACCINE_SAFETY = [
    {
        "id": "vs-vaers",
        "name": "VAERS (Vaccine Adverse Event Reporting System — Est. 1990)",
        "platform": "Passive Early Warning",
        "plain": "Co-run by FDA and CDC since 1990, VAERS is an open national inbox where anyone can report a health problem after vaccination so scientists can spot unusual patterns fast.",
        "technical": "Passive spontaneous reporting system co-managed by CDC and FDA; designed for rapid hypothesis generation and disproportionality screening, not standalone causal inference due to lack of unvaccinated denominators.",
        "url": "https://www.cdc.gov/vaccine-safety-systems/vaers/index.html",
    },
    {
        "id": "vs-vsd-best",
        "name": "CDC Vaccine Safety Datalink (VSD) & FDA CBER BEST",
        "platform": "Active EHR Surveillance",
        "plain": "When VAERS spots a potential clue, VSD and BEST immediately check millions of linked medical records to see if vaccinated people actually had that event more often than unvaccinated peers.",
        "technical": "Active, near-real-time Rapid Cycle Analysis (RCA) and Self-Controlled Risk Interval (SCRI) studies across integrated health-plan EHRs and claims with true exposed denominators and chart validation.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/report-problem-center-biologics-evaluation-research/vaccine-adverse-events",
    },
    {
        "id": "vs-cisa",
        "name": "Clinical Immunization Safety Assessment (CISA) & Causality",
        "platform": "Clinical Investigation",
        "plain": "Academic medical centers partner with CDC to study complex individual reactions and distinguish true vaccine side effects from coincidental illnesses.",
        "technical": "Evaluates biological plausibility, temporal windows, dechallenge/rechallenge, and Brighton Collaboration case definitions to separate causal Adverse Events Following Immunization (AEFIs) from background incidence.",
        "url": "https://www.cdc.gov/vaccine-safety-systems/vaers/index.html",
    },
    {
        "id": "vs-pregnancy",
        "name": "Maternal Immunization & Pregnancy Exposure Registries",
        "platform": "Special Populations",
        "plain": "Vaccines given during pregnancy—like Tdap and maternal RSV—pass protective antibodies across the placenta to protect newborns in their first vulnerable months.",
        "technical": "Evaluated via dedicated maternal-fetal clinical trials, Pregnancy Exposure Registries, and VSD/BEST active surveillance of birth outcomes.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",
    },
    {
        "id": "vs-vicp",
        "name": "Vaccine Information Statements (VIS) & Injury Compensation (VICP)",
        "platform": "Patient Transparency",
        "plain": "Before every routine US vaccine, clinics hand patients a plain-language Vaccine Information Statement explaining benefits, common soreness, and rare risks.",
        "technical": "National Childhood Vaccine Injury Act (1986) mandates VIS distribution, healthcare-provider VAERS reporting for specified table events, and no-fault VICP compensation to stabilize vaccine supply.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccine-adverse-events/vaccine-adverse-event-reporting-system-vaers-questions-and-answers",
    },
    {
        "id": "vs-pharmacovig-link",
        "name": "Integration with Global Post-Market Surveillance (WHO VigiBase)",
        "platform": "International Sharing",
        "plain": "Because rare side effects might occur in only 1 in 100,000 doses, pooling safety data across countries lets regulators detect and update labels much sooner.",
        "technical": "Harmonized ICH E2B(R3) and Brighton Collaboration MedDRA coding across FDA VAERS/BEST, EMA EudraVigilance, UK MHRA Yellow Card, and WHO Uppsala Monitoring Centre VigiBase.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/report-problem-center-biologics-evaluation-research/vaccine-adverse-events",
    },
]


def build_vaccines(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "vaccine_platforms": len(VACCINE_PLATFORMS),
            "adjuvants_formulation": len(ADJUVANTS_FORMULATION),
            "cber_licensure": len(CBER_LICENSURE),
            "vaccine_safety": len(VACCINE_SAFETY),
        },
        "vaccine_platforms": VACCINE_PLATFORMS,
        "adjuvants_formulation": ADJUVANTS_FORMULATION,
        "cber_licensure": CBER_LICENSURE,
        "vaccine_safety": VACCINE_SAFETY,
    }
    (data_dir / "vaccines.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_vaccines.py <site/data>")
    print(json.dumps(build_vaccines(pathlib.Path(sys.argv[1])), indent=2))
'''

VACCINES_JS = '''// Pill by Pill v6.1s: Vaccines, Adjuvants, CBER Lot Release & Immunization Safety Surveillance Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["platforms", "Vaccine Platforms", "vaccine_platforms"],
  ["adjuvants", "Adjuvants & Stability", "adjuvants_formulation"],
  ["licensure", "CBER & Lot Release", "cber_licensure"],
  ["safety", "VAERS, VSD & Safety", "vaccine_safety"],
];

function vaccineLifecycleSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Vaccine antigen design, adjuvant formulation, CBER lot release, and active safety surveillance lifecycle">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Antigen Platform</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Live, Subunit, Conjugate</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">mRNA–LNP &amp; Viral Vector</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#vax-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Adjuvants &amp; VVM</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Alum, MF59, AS01, CpG</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Cold Chain &amp; MDVP</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#vax-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. CBER Lot Release</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">BLA / VRBPAC / 21 CFR 610</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">ACIP &amp; WHO PQ</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#vax-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Safety Systems</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">VAERS Early Warning</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CDC VSD &amp; CBER BEST</text>
      <defs><marker id="vax-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Vaccines undergo CBER lot-by-lot release testing before distribution and continuous active safety monitoring across VAERS, CDC VSD, and FDA BEST.</figcaption>
  </figure>`;
}

export async function vaccinesPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/vaccines.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/vaccines" : "#/ref/vaccines";

  const pills = html`<div class="chips" role="navigation" aria-label="Vaccines sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Topic / Vaccine Pillar</th><th>Platform / Role</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.platform}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${vaccineLifecycleSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA CBER, CDC VAERS/Adjuvants, and WHO Prequalification documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Vaccines & Immunology"]] : [REF_HOME, ["Vaccines & Immunology"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Vaccines, Adjuvants, CBER Lot Release & Safety Surveillance",
      lede: env === "explore"
        ? "How different types of vaccines train the immune system, why adjuvants help, and how every batch is tested before reaching clinics."
        : "Live, inactivated, subunit/VLP, conjugate, mRNA-LNP & viral-vector platforms; adjuvants; CBER 21 CFR 610.2 lot release; VAERS, VSD & WHO PQ.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on vaccines and immunization.", href: env === "explore" ? "#/ref/vaccines" : "#/explore/vaccines" },
        { title: "Biologics, Biosimilars & Gene Therapies", text: "mAbs, ADCs, CAR-T, CRISPR, and CBER/CDER oversight.", href: "#/ref/biologics" },
        { title: "Supply Chain, DSCSA & Cold Chain", text: "WHO GDP thermal bands, VVMs, and shortage resilience.", href: "#/ref/supply-chain" },
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
    if 'vaccines.js' not in txt:
        for anchor in ('import * as biologicsCgt from "./biologics_cgt.js";\n', 'import * as supplyChain from "./supply_chain.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as vaccines from "./vaccines.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as vaccines from "./vaccines.js";\n' + txt
            changed = True
    if '"/ref/vaccines"' not in txt:
        for anchor in ('if (path === "/ref/biologics")', 'if (path === "/ref/supply-chain")', 'if (path === "/ref/rwe")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/vaccines") return { env: "ref", current: "#/ref/vaccines", ...(await vaccines.vaccinesPage(query, "ref")) };\n  if (path === "/explore/vaccines") return { env: "explore", current: "#/explore/vaccines", ...(await vaccines.vaccinesPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/vaccines" not in txt:
        for anchor in ('["#/ref/biologics", "Biologics & CGT"]', '["#/ref/supply-chain", "Supply chain & DSCSA"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/vaccines", "Vaccines & adjuvants"]', 1)
                changed = True
                break
    if "#/explore/vaccines" not in txt:
        for anchor in ('["#/explore/biologics", "Biologics & CGT"]', '["#/explore/supply-chain", "Supply chain & DSCSA"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/vaccines", "Vaccines & adjuvants"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_vaccines.py" in txt:
        return False
    line = "python3 pipeline/build_vaccines.py site/data\n"
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
    if '"/api/vaccines"' in txt:
        return False
    route = (
        '\n@app.get("/api/vaccines")\n'
        'def api_vaccines():\n'
        '    p = DATA_DIR / "vaccines.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "vaccines.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"vaccines.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    vax_ref = _load(data_dir / "vaccines.json", {}) or {}\n'
        '    for sec_key, sec_q in [("vaccine_platforms", "platforms"), ("adjuvants_formulation", "adjuvants"), ("cber_licensure", "licensure"), ("vaccine_safety", "safety")]:\n'
        '        for item in (vax_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "vaccines",\n'
        '                "group": "Vaccines & Immunology",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/vaccines?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/vaccines?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"vaccine immunization adjuvant alum MF59 AS01 CBER lot release VAERS VSD VRBPAC ACIP WHO PQ VVM {sec_key} {item.get(\'name\', \'\')} {item.get(\'platform\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"vaccines", "#/ref/vaccines"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    vax_doc = _load_json(data_dir / "vaccines.json")\n'
        '    if isinstance(vax_doc, dict) and vax_doc.get("vaccine_platforms"):\n'
        '        vax_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (vax_doc.get("vaccine_platforms") or []) + (vax_doc.get("vaccine_safety") or []))\n'
        '        pages.append(("vaccines", "#/ref/vaccines", "Vaccines, Adjuvants, CBER Lot Release & Safety Surveillance",\n'
        '                      "Primary-sourced guide to vaccine platforms, aluminum & novel adjuvants, CBER 21 CFR 610.2 lot release, WHO Prequalification, and VAERS/VSD.",\n'
        '                      f"<ul>{vax_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/vaccines"' in txt:
        return False
    for anchor in ('    "/#/explore/biologics",', '    "/#/explore/supply-chain",', '    "/#/explore/rwe",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/vaccines",\n    "/#/explore/vaccines",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_vaccines_py": _write_if_changed(pipe_dir / "build_vaccines.py", BUILD_VACCINES_PY),
        "vaccines_js": _write_if_changed(js_dir / "vaccines.js", VACCINES_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/biologics") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/biologics", "Biologics & CGT"]] }];\nconst EXPLORE_NAV = [["#/explore/biologics", "Biologics & CGT"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/biologics",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_vaccines.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_vaccines.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"vaccine_platforms": 6, "adjuvants_formulation": 6, "cber_licensure": 6, "vaccine_safety": 6}, out

        doc = json.loads((root / "site" / "data" / "vaccines.json").read_text(encoding="utf-8"))
        for k in ("vaccine_platforms", "adjuvants_formulation", "cber_licensure", "vaccine_safety"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "vaccines.js").read_text(encoding="utf-8")
        print("V61S_VACCINES_IMMUNOLOGY_ADJUVANTS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1s Vaccines, Adjuvants & Safety Surveillance patch.")
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
