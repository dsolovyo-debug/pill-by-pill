// Routes for the v6.x encyclopedia pages. Their modules were added by Gemini's patches, but the
// patches' route wiring did not land in app.js, so every one of these links showed "We couldn't
// find that page". This table maps each #/ref/<slug> and #/explore/<slug> to its page function and
// turns the three result shapes those modules use into the { env, html, mount, current } that
// app.js renders:  {html}  ·  {title, body, lede?, trail?}  ·  draws into a container (no result).
import { html, raw } from "./ui.js";
import { page } from "./layout.js";

const M = (file, fn, opts = {}) => ({ file, fn, ...opts });
// opts.args: how to call it.  "qm" = (query, mode) [default]  ·  "c" = (container, mode)  ·  "m" = (mode)  ·  "q" = (query)  ·  "" = ()
const ROUTES = {
  "adcs-bispecifics-oligos": M("adcs_bispecifics_oligos", "adcsBispecificsOligosPage"),
  "adme": M("adme", "admePage"),
  "amr-antiinfectives": M("amr_antiinfectives", "amrAntiinfectivesPage"),
  "analytical-usp-q12": M("analytical_usp_q12", "analyticalUspQ12Page", { args: "c" }),
  "babe-bcs-nti": M("babe_bcs_nti", "babeBcsNtiPage", { args: "c" }),
  "nonclinical-nams": M("nonclinical_nams", "nonclinicalNamsPage", { args: "c" }),
  "bd-deals": M("bd_deals", "bdDealsPage"),
  "biologics": M("biologics_cgt", "biologicsCgtPage"),
  "atmp": M("biologics_cgt", "biologicsCgtPage"),
  "careers": M("careers", "careersPage"),
  "classes": M("atc_classes", "atcClassesPage", { args: "q" }),
  "combo-products": M("combo_products", "comboProductsPage"),
  "complex-quality": M("complex_quality", "complexQualityPage"),
  "continuous-pat-ai": M("continuous_pat_ai_mfg", "continuousPatAiMfgPage"),
  "controlled-substances": M("controlled_substances", "controlledSubstancesPage"),
  "diagnostics": M("diagnostics", "diagnosticsPage"),
  "cdx": M("diagnostics", "diagnosticsPage"),
  "digital-health": M("digital_health", "digitalHealthPage"),
  "economics": M("economics", "economicsPage", { args: "", explore: "economicsExplorePage" }),
  "software": M("economics", "softwareStackPage", { args: "q" }),
  "excipients-dmfs-nano": M("excipients_dmfs_nano", "excipientsDmfsNanoPage"),
  "gcp-bimo-cdisc": M("gcp_bimo_cdisc", "gcpBimoCdiscPage"),
  "global-reg": M("global_reg_hta", "globalRegHtaPage"),
  "glossary": M("v61b_reference", "glossaryPage"),
  "trace": M("v61b_reference", "traceStoryboardsPage"),
  "ich": M("v61b_reference", "ichMatrixPage", { args: "" }),
  "history-laws": M("history_laws", "historyLawsPage"),
  "ip": M("ip_patents", "ipPatentsPage"),
  "oncology-oce": M("oncology_oce", "oncologyOcePage"),
  "orphan": M("orphan", "orphanPage"),
  "origins": M("origins", "originsGalleryPage", { args: "q" }),
  "otc-compounding": M("otc_compounding", "otcCompoundingPage"),
  "partners": M("partners", "partnersPage", { args: "q", explore: "partnersExplorePage" }),
  "pathways": M("pathways", "pathwaysPage", { args: "m" }),
  "pfdd-coa-expanded-access": M("pfdd_coa_expanded_access", "pfddCoaExpandedAccessPage"),
  "playbooks": M("playbooks", "playbooksPage", { args: "q", explore: "playbooksExplorePage" }),
  "pricing-access": M("pricing_access", "pricingAccessPage"),
  "promotion-transparency": M("promotion_transparency", "promotionTransparencyPage"),
  "radiopharma": M("radiopharma", "radiopharmaPage"),
  "rmat-hctp-cgt-cmc": M("rmat_hctp_cgt_cmc", "rmatHctpCgtCmcPage"),
  "rwe": M("rwe", "rwePage"),
  "safety": M("safety", "safetyPage"),
  "search": M("global_search", "globalSearchPage"),
  "shortages-resilience": M("shortages_resilience", "shortagesResiliencePage"),
  "special-populations": M("special_populations", "specialPopulationsPage"),
  "sterile": M("sterile_mfg", "sterileMfgPage"),
  "sterile-mfg": M("sterile_mfg", "sterileMfgPage"),
  "supply-chain": M("supply_chain", "supplyChainPage"),
  "trials": M("trials", "trialsPage"),
  "vaccines": M("vaccines", "vaccinesPage"),
  "worksheets": M("worksheets", "worksheetsPage", { args: "q" }),
};

export const v6Slugs = Object.keys(ROUTES);

function shape(r, env, current) {
  if (r && r.html != null) return { env, current, ...r, env: r.env && r.env !== "start" ? r.env : env, html: raw(String(r.html)) };
  if (r && r.body != null) {
    const body = raw(String(r.body));
    // most of these modules write their own <h1>; only add page() heading when they did not
    const inner = /<h1[\s>]/.test(String(r.body))
      ? html`<article class="page level-page">${body}</article>`
      : page({ trail: r.trail || [], title: r.title || "Pill by Pill", lede: r.lede, body });
    return { env, current, html: inner, mount: r.mount };
  }
  if (typeof r === "string" || r instanceof Object) return { env, current, html: raw(String(r)) };
  return null;
}

/** Returns a view for #/<env>/<slug>, or null when the slug is not one of these pages. */
export async function v6Route(env, slug, query) {
  const def = ROUTES[slug];
  if (!def) return null;
  const mod = await import(`./${def.file}.js`);
  const current = `#/${env}/${slug}`;
  const fnName = env === "explore" && def.explore ? def.explore : def.fn;
  const fn = mod[fnName];
  if (typeof fn !== "function") throw new Error(`${def.file}.js has no ${fnName}()`);
  const args = env === "explore" && def.explore ? "" : (def.args ?? "qm");
  if (args === "c") {
    return { env, current, html: html`<article class="page level-page" id="v6-mount"><p class="muted">Loading…</p></article>`,
      mount(root) { const el = root.querySelector("#v6-mount"); fn(el, env).catch((e) => { el.innerHTML = ""; el.append(String(e.message || e)); }); } };
  }
  const call = { qm: () => fn(query, env), q: () => fn(query), m: () => fn(env), "": () => fn() }[args];
  const view = shape(await call(), env, current);
  if (!view) throw new Error(`${fnName}() returned nothing`);
  return view;
}
