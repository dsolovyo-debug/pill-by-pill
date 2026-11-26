#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 4): Drug Dossier At-a-Glance Summary & Collapsible Deep Panels.

Why:
  Individual medicine dossier pages carry rich multi-domain sections (Overview, Mechanism & 3D
  binding, Clinical Trials, Manufacturing & CMC, Regulatory Approvals, Patents & Economics,
  Sources). On mobile, rendering every section fully expanded creates a 10+ screen scroll.

Fix:
  Stages `.github/site-fixes/js/dossier_ui.js` and `.github/site-fixes/css/dossier_ui.css`:
    1. Compact "At a glance" 2x2 metadata strip (Modality, Route, First Approval, Agencies)
       pinned right under the medicine heading.
    2. Collapsible `<details>` deep-dive panels with the first panel open by default on phones
       and Expand all / Collapse all toolbar buttons.
    3. Clean `attachDossierControls(root)` returning a cleanup hook for `view.mount(app)`.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_drug_dossier_quick_glance_and_sections_patch.py --selftest
  python3 2026-11-26_drug_dossier_quick_glance_and_sections_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

DOSSIER_UI_JS = r"""// Compact "At a glance" summary strip & collapsible deep-dive panels for drug dossiers.
// Wire into drug dossier renderer and view.mount(app) via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render a 4-item "At a glance" summary strip at the top of a drug dossier.
 * @param {Array<{label: string, value: string}>} facts
 */
export function renderDossierGlance(facts) {
  const items = (Array.isArray(facts) ? facts : []).filter((f) => f && f.value);
  if (!items.length) return "";
  return html`<dl class="pbp-dossier-glance" aria-label="Medicine at a glance">
    ${items.map(
      (f) => html`<div class="pbp-glance-item">
        <dt>${f.label}</dt>
        <dd>${f.value}</dd>
      </div>`
    )}
  </dl>`;
}

/**
 * Render collapsible dossier sections with Expand all / Collapse all controls.
 * @param {Array<{id?: string, title: string, badge?: string, body: any, defaultOpen?: boolean}>} sections
 */
export function renderDossierAccordion(sections) {
  const list = (Array.isArray(sections) ? sections : []).filter((s) => s && s.title);
  if (!list.length) return "";

  return html`<div class="pbp-dossier-accordion" data-pbp-dossier-acc>
    <div class="pbp-dossier-toolbar">
      <button type="button" class="pbp-dossier-btn" data-dossier-action="expand">Expand all</button>
      <button type="button" class="pbp-dossier-btn" data-dossier-action="collapse">Collapse all</button>
    </div>
    ${list.map((sec, idx) => {
      const isOpen = sec.defaultOpen !== undefined ? Boolean(sec.defaultOpen) : idx === 0;
      return html`<details class="pbp-dossier-sec" id="${sec.id || `dossier-sec-${idx + 1}`}" ${isOpen ? "open" : ""}>
        <summary class="pbp-dossier-summary">
          <span class="pbp-dossier-title">${sec.title}</span>
          ${sec.badge ? html`<span class="pbp-dossier-badge">${sec.badge}</span>` : ""}
        </summary>
        <div class="pbp-dossier-body">${sec.body}</div>
      </details>`;
    })}
  </div>`;
}

/**
 * Attach Expand all / Collapse all handlers. Returns cleanup function for view.mount(app).
 */
export function attachDossierControls(root) {
  const el = root && root.querySelector ? root : document;
  const onClick = (ev) => {
    const btn = ev.target && ev.target.closest ? ev.target.closest("[data-dossier-action]") : null;
    if (!btn) return;
    const acc = btn.closest("[data-pbp-dossier-acc]");
    if (!acc) return;
    const expand = btn.dataset.dossierAction === "expand";
    acc.querySelectorAll("details.pbp-dossier-sec").forEach((d) => {
      if (expand) d.setAttribute("open", "");
      else d.removeAttribute("open");
    });
  };
  el.addEventListener("click", onClick);
  return () => el.removeEventListener("click", onClick);
}
"""

DOSSIER_UI_CSS = r"""/* Drug dossier "At a glance" grid & collapsible deep-dive panels */
.pbp-dossier-glance {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
  gap: 8px;
  margin: 10px 0 16px;
  padding: 0;
}

.pbp-glance-item {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 8px 11px;
}

.pbp-glance-item dt {
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  opacity: 0.68;
  margin: 0 0 2px;
}

.pbp-glance-item dd {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 600;
  line-height: 1.25;
}

.pbp-dossier-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
  margin-bottom: 8px;
}

.pbp-dossier-btn {
  min-height: 34px;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.2);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-dossier-sec {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  margin-bottom: 8px;
  padding: 0;
  overflow: hidden;
}

.pbp-dossier-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 10px 13px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.96rem;
  list-style: none;
}

.pbp-dossier-summary::-webkit-details-marker {
  display: none;
}

.pbp-dossier-badge {
  font-size: 0.78rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
}

.pbp-dossier-body {
  padding: 0 13px 12px;
  border-top: 1px solid rgba(22, 35, 59, 0.08);
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "dossier_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != DOSSIER_UI_JS:
        js_path.write_text(DOSSIER_UI_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "dossier_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != DOSSIER_UI_CSS:
        css_path.write_text(DOSSIER_UI_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "dossier_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "dossier_ui.css").read_text(encoding="utf-8")
        assert "renderDossierGlance" in js_txt and "renderDossierAccordion" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("DRUG_DOSSIER_QUICK_GLANCE_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage drug dossier at-a-glance & collapsible sections module")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo root")
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
