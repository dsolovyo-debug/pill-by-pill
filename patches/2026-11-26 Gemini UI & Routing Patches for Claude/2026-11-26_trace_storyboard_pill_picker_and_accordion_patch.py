#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 3): Trace One Drug Pill Picker & 8-Stage Accordion Module.

Why:
  Even after fixing the HTML escaping bug on "Trace One Drug End-to-End", the medicine
  selector renders as a dense inline paragraph of long drug names + parenthetical modalities
  separated by middle dots, and all 8 lifecycle stages stack into a long vertical scroll on
  mobile screens.

Fix:
  Stages clean, zero-MutationObserver ES module `.github/site-fixes/js/trace_ui.js` and
  stylesheet `.github/site-fixes/css/trace_ui.css` exporting:
    - `renderTraceDrugPicker(storyboards, activeId, mode)`: compact wrapping pill buttons
      showing Drug Name + short Modality tag with proper unescaped `aria-current="page"`.
    - `renderTraceStageAccordion(stages, opts)`: numbered 1-8 collapsible `<details>` cards
      (Stage 1 open by default on narrow viewports) plus a 1-tap Expand/Collapse all control.

Usage:
  python3 2026-11-26_trace_storyboard_pill_picker_and_accordion_patch.py --selftest
  python3 2026-11-26_trace_storyboard_pill_picker_and_accordion_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

TRACE_UI_JS = """// Clean, zero-MutationObserver UI helpers for Trace One Drug End-to-End
// Import from site/js/trace.js (or wire via prepare_pages.py).
import { html } from "./ui.js";

function shortModality(raw) {
  const s = String(raw || "");
  if (/small molecule/i.test(s)) return "Small Molecule";
  if (/peptide/i.test(s)) return "Peptide";
  if (/sirna|oligo|aso/i.test(s)) return "Oligo / siRNA";
  if (/mrna/i.test(s)) return "mRNA-LNP";
  if (/monoclonal|mab/i.test(s)) return "mAb";
  if (/car-t|cell|gene/i.test(s)) return "Cell & Gene";
  return s.split("(")[0].trim().slice(0, 22) || "Medicine";
}

/**
 * Render compact pill buttons for selecting a flagship medicine on Trace One Drug.
 * Uses tagged `html` template interpolation (never .join() string concatenation) so
 * quotes and anchor markup are never double-escaped.
 */
export function renderTraceDrugPicker(storyboards, activeId, mode = "ref") {
  const list = Array.isArray(storyboards) ? storyboards : [];
  const prefix = mode === "explore" ? "#/explore/trace?drug=" : "#/ref/trace?drug=";
  const pills = list.map((sb) => {
    const isCurrent = sb.id === activeId;
    const tag = shortModality(sb.modality);
    return html`<a
      class="trace-pill${isCurrent ? " is-active" : ""}"
      href="${prefix}${encodeURIComponent(sb.id)}"
      aria-current="${isCurrent ? "page" : "false"}"
    >
      <span class="trace-pill-name">${sb.name || sb.id}</span>
      <span class="trace-pill-tag">${tag}</span>
    </a>`;
  });

  return html`<nav class="trace-picker" aria-label="Choose a medicine to trace">
    <div class="trace-picker-label">Choose a medicine (${list.length})</div>
    <div class="trace-picker-row">${pills}</div>
  </nav>`;
}

/**
 * Render the 8 lifecycle stages as clean collapsible <details> cards with numbered badges.
 */
export function renderTraceStageAccordion(stages, { openFirstOnly = true } = {}) {
  const list = Array.isArray(stages) ? stages : [];
  const cards = list.map((st, idx) => {
    const num = st.stage_number || idx + 1;
    const isOpen = openFirstOnly ? idx === 0 : true;
    const title = st.stage || st.title || `Stage ${num}`;
    const summary = st.summary || st.plain || "";
    const detail = st.detail || st.technical || "";
    return html`<details class="trace-stage" ${isOpen ? "open" : ""}>
      <summary class="trace-stage-summary">
        <span class="trace-stage-num">${num}</span>
        <span class="trace-stage-title">${title}</span>
      </summary>
      <div class="trace-stage-body">
        ${summary ? html`<p class="trace-stage-lead">${summary}</p>` : ""}
        ${detail && detail !== summary ? html`<p class="trace-stage-detail">${detail}</p>` : ""}
      </div>
    </details>`;
  });

  return html`<section class="trace-stages" aria-label="Lifecycle stages">
    <div class="trace-stages-toolbar">
      <button type="button" class="trace-toggle-all" data-trace-toggle="expand">Expand all stages</button>
      <button type="button" class="trace-toggle-all" data-trace-toggle="collapse">Collapse all</button>
    </div>
    ${cards}
  </section>`;
}

/**
 * Attach expand/collapse all handlers inside a mounted trace page container.
 */
export function attachTraceStageControls(container) {
  if (!container) return;
  container.querySelectorAll("[data-trace-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const expand = btn.getAttribute("data-trace-toggle") === "expand";
      container.querySelectorAll("details.trace-stage").forEach((d) => {
        d.open = expand;
      });
    });
  });
}
"""

TRACE_UI_CSS = """/* Trace One Drug compact pill picker & 8-stage accordion */
.trace-picker {
  margin: 10px 0 16px;
}

.trace-picker-label {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  opacity: 0.72;
  margin-bottom: 8px;
}

.trace-picker-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trace-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 999px;
  text-decoration: none;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.18);
  font-size: 0.88rem;
  line-height: 1.2;
}

.trace-pill.is-active,
.trace-pill[aria-current="page"] {
  border-width: 2px;
  font-weight: 700;
}

.trace-pill-tag {
  font-size: 0.74rem;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
  font-weight: 600;
}

.trace-stages-toolbar {
  display: flex;
  gap: 8px;
  margin: 10px 0;
}

.trace-toggle-all {
  padding: 5px 11px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.18);
}

.trace-stage-summary {
  display: flex;
  align-items: center;
  gap: 10px;
}

.trace-stage-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 700;
  background: rgba(22, 35, 59, 0.10);
  flex-shrink: 0;
}

.trace-stage-body {
  padding-top: 4px;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "trace_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != TRACE_UI_JS:
        js_path.write_text(TRACE_UI_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "trace_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != TRACE_UI_CSS:
        css_path.write_text(TRACE_UI_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "trace_ui.js").read_text(encoding="utf-8")
        assert "renderTraceDrugPicker" in js_txt
        assert "renderTraceStageAccordion" in js_txt
        assert "MutationObserver" not in js_txt
        css_txt = (root / ".github" / "site-fixes" / "css" / "trace_ui.css").read_text(encoding="utf-8")
        assert "var(--card" not in css_txt

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("TRACE_STORYBOARD_PILL_PICKER_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Trace One Drug pill picker & 8-stage accordion module")
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
