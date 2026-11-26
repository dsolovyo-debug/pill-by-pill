// In-depth (Reference) side navigation: ~55 links grouped into short collapsible sections, with a
// "for you" shortlist when the reader has picked Clinician, Chemist or Industry. Every page stays
// reachable (at most two taps); links a future patch adds to REF_NAV land in "More topics".
// Plain <details> elements: no script, works with keyboards and screen readers.
import { html } from "./ui.js";

const GROUPS = [
  ["Medicines", ["#/ref/search", "#/ref", "#/ref/drugs", "#/ref/families", "#/ref/compare", "#/ref/topics", "#/ref/routes", "#/ref/trace"]],
  ["Clinical & safety", ["#/ref/trials", "#/ref/safety", "#/ref/diagnostics", "#/ref/rwe", "#/ref/special-populations", "#/ref/controlled-substances",
    "#/ref/orphan", "#/ref/oncology-oce", "#/ref/pfdd-coa-expanded-access", "#/ref/babe-bcs-nti"]],
  ["Science & modalities", ["#/ref/adme", "#/ref/playbooks", "#/ref/biologics", "#/ref/vaccines", "#/ref/adcs-bispecifics-oligos", "#/ref/rmat-hctp-cgt-cmc",
    "#/ref/radiopharma", "#/ref/nonclinical-nams", "#/ref/amr-antiinfectives", "#/ref/digital-health"]],
  ["Manufacturing & quality", ["#/ref/departments", "#/ref/sterile", "#/ref/continuous-pat-ai", "#/ref/analytical-usp-q12", "#/ref/complex-quality",
    "#/ref/excipients-dmfs-nano", "#/ref/combo-products", "#/ref/supply-chain", "#/ref/shortages-resilience", "#/ref/vendors", "#/ref/equipment", "#/ref/software"]],
  ["Regulatory & policy", ["#/ref/pathways", "#/ref/ich", "#/ref/global-reg", "#/ref/gcp-bimo-cdisc", "#/ref/ip", "#/ref/otc-compounding",
    "#/ref/promotion-transparency", "#/ref/pricing-access", "#/ref/history-laws"]],
  ["Business & careers", ["#/ref/economics", "#/ref/bd-deals", "#/ref/partners", "#/ref/careers"]],
  ["About the data", ["#/ref/glossary", "#/ref/data"]],
];

const FOR_ROLE = {
  clinician: ["For clinicians & pharmacists", ["#/ref/drugs", "#/ref/compare", "#/ref/families", "#/ref/routes", "#/ref/safety", "#/ref/trials",
    "#/ref/diagnostics", "#/ref/rwe", "#/ref/special-populations", "#/ref/controlled-substances", "#/ref/babe-bcs-nti", "#/ref/adme"]],
  chemist: ["For chemists & researchers", ["#/ref/drugs", "#/ref/families", "#/ref/trace", "#/ref/playbooks", "#/ref/adme", "#/ref/biologics",
    "#/ref/adcs-bispecifics-oligos", "#/ref/nonclinical-nams", "#/ref/analytical-usp-q12", "#/ref/sterile", "#/ref/excipients-dmfs-nano", "#/ref/equipment"]],
  industry: ["For industry & regulatory", ["#/ref/pathways", "#/ref/ich", "#/ref/global-reg", "#/ref/vendors", "#/ref/supply-chain", "#/ref/shortages-resilience",
    "#/ref/ip", "#/ref/pricing-access", "#/ref/economics", "#/ref/bd-deals", "#/ref/partners", "#/ref/careers"]],
};

export function refNav(nav, current, role) {
  const label = new Map(nav.map(([h, l]) => [h, l]));
  const link = (h) => html`<a href="${h}"${current === h ? html` aria-current="page"` : ""}>${label.get(h)}</a>`;
  const placed = new Set();
  const groups = GROUPS.map(([name, hrefs]) => {
    const items = hrefs.filter((h) => label.has(h));
    items.forEach((h) => placed.add(h));
    return [name, items];
  });
  const rest = nav.map(([h]) => h).filter((h) => !placed.has(h));
  if (rest.length) groups.push(["More topics", rest]);
  const pick = FOR_ROLE[role];
  const picks = pick ? pick[1].filter((h) => label.has(h)) : [];
  // open the section holding the current page; with no role picked, open Medicines on the overview
  // Wide screens: open the section holding the current page (Medicines on the overview) and the
  // role shortlist. Phones: everything starts closed, so the page content is one screen down at most.
  const wide = typeof matchMedia === "function" ? matchMedia("(min-width: 821px)").matches : true;
  const openName = wide ? ((groups.find(([, items]) => items.includes(current)) || [])[0] || (pick ? null : "Medicines")) : null;
  return html`${pick ? html`<details class="r-group r-picks"${wide ? html` open` : ""}><summary>${pick[0]} <span class="n">${picks.length}</span></summary>${picks.map(link)}</details>` : ""}
    <div class="r-groups">${groups.filter(([, items]) => items.length).map(([name, items]) =>
      html`<details class="r-group"${name === openName ? html` open` : ""}><summary>${name} <span class="n">${items.length}</span></summary>${items.map(link)}</details>`)}</div>
    <a class="r-fund" href="#/fund">Funding</a>`;
}
