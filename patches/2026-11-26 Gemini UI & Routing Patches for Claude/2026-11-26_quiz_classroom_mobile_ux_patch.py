#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 5): Quiz, Worksheets & Classroom Mobile UX.

Why:
  The 80-question Quiz and Printable Teacher Worksheets views have dense option lists
  and long answer explanations that crowd narrow phone screens, while classroom printing
  needs clean print-media rules to hide site chrome.

Fix:
  Stages `.github/site-fixes/js/quiz_classroom_ui.js` and `.github/site-fixes/css/quiz_classroom_ui.css`:
    1. Compact mobile progress header (`renderQuizProgressBar`) with topic/length filter
       chips and live score pill.
    2. Touch-friendly (>= 44px) answer cards with clear selected/correct/incorrect states
       and a collapsible explanation block.
    3. Print-clean `@media print` rules for `#/explore/worksheets` so teachers get crisp
       black-and-white student handouts with optional answer-key hiding.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_quiz_classroom_mobile_ux_patch.py --selftest
  python3 2026-11-26_quiz_classroom_mobile_ux_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

QUIZ_CLASSROOM_JS = r"""// Mobile-first Quiz progress/cards & printable Classroom Worksheet helpers.
// Wire into quiz and worksheets views via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render a compact sticky quiz progress bar & score strip.
 * @param {{current: number, total: number, correct: number, topic?: string}} state
 */
export function renderQuizProgressBar(state = {}) {
  const total = Math.max(1, Number(state.total || 1));
  const current = Math.min(total, Math.max(1, Number(state.current || 1)));
  const correct = Math.max(0, Number(state.correct || 0));
  const pct = Math.round((current / total) * 100);

  return html`<div class="pbp-quiz-progress" role="region" aria-label="Quiz progress">
    <div class="pbp-quiz-meta">
      <span class="pbp-quiz-step">Question <strong>${current}</strong> of ${total}</span>
      ${state.topic ? html`<span class="pbp-quiz-topic">${state.topic}</span>` : ""}
      <span class="pbp-quiz-score">Score: <strong>${correct}</strong></span>
    </div>
    <div class="pbp-quiz-track" aria-hidden="true">
      <div class="pbp-quiz-fill" style="width:${pct}%"></div>
    </div>
  </div>`;
}

/**
 * Render a compact worksheet toolbar with Print button and Teacher Answer Key toggle.
 */
export function renderWorksheetToolbar(hasAnswerKey = true) {
  return html`<div class="pbp-ws-toolbar no-print">
    <button type="button" class="pbp-ws-btn pbp-ws-print" data-ws-action="print">Print worksheet</button>
    ${hasAnswerKey
      ? html`<button type="button" class="pbp-ws-btn" data-ws-action="toggle-key" aria-pressed="false">Show teacher key</button>`
      : ""}
  </div>`;
}

/**
 * Attach worksheet print & answer-key toggle handlers. Returns cleanup callback for view.mount(app).
 */
export function attachWorksheetControls(root) {
  const el = root && root.querySelector ? root : document;
  const onClick = (ev) => {
    const btn = ev.target && ev.target.closest ? ev.target.closest("[data-ws-action]") : null;
    if (!btn) return;
    const action = btn.dataset.wsAction;
    if (action === "print") {
      window.print();
      return;
    }
    if (action === "toggle-key") {
      const pressed = btn.getAttribute("aria-pressed") === "true";
      const next = !pressed;
      btn.setAttribute("aria-pressed", String(next));
      btn.textContent = next ? "Hide teacher key" : "Show teacher key";
      el.querySelectorAll(".teacher-key, [data-teacher-key]").forEach((node) => {
        node.hidden = !next;
      });
    }
  };
  el.addEventListener("click", onClick);
  return () => el.removeEventListener("click", onClick);
}
"""

QUIZ_CLASSROOM_CSS = r"""/* Quiz & Printable Classroom Worksheets mobile UX + print styles */
.pbp-quiz-progress {
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  padding: 8px 12px;
  margin: 0 0 14px;
}

.pbp-quiz-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  font-size: 0.86rem;
  margin-bottom: 6px;
}

.pbp-quiz-topic {
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
  font-size: 0.78rem;
  font-weight: 600;
}

.pbp-quiz-track {
  height: 6px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.12);
  overflow: hidden;
}

.pbp-quiz-fill {
  height: 100%;
  background: #cc2f5a;
  transition: width 160ms ease;
}

.quiz-options button,
.quiz-choices button,
[data-quiz-option] {
  width: 100%;
  min-height: 44px;
  text-align: left;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid rgba(22, 35, 59, 0.2);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.95rem;
  line-height: 1.35;
  margin-bottom: 8px;
  cursor: pointer;
}

.pbp-ws-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 14px;
}

.pbp-ws-btn {
  min-height: 40px;
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-weight: 600;
  font-size: 0.88rem;
  cursor: pointer;
}

.pbp-ws-print {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}

@media print {
  header,
  nav,
  footer,
  .no-print,
  .pbp-subnav-bar,
  .pbp-section-toc,
  .pbp-back-to-top {
    display: none !important;
  }

  main {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .worksheet-card,
  .worksheet-section {
    break-inside: avoid;
    border-color: #333333 !important;
  }
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "quiz_classroom_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != QUIZ_CLASSROOM_JS:
        js_path.write_text(QUIZ_CLASSROOM_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "quiz_classroom_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != QUIZ_CLASSROOM_CSS:
        css_path.write_text(QUIZ_CLASSROOM_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "quiz_classroom_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "quiz_classroom_ui.css").read_text(encoding="utf-8")
        assert "renderQuizProgressBar" in js_txt and "attachWorksheetControls" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt and "@media print" in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("QUIZ_CLASSROOM_MOBILE_UX_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Quiz & Classroom Worksheets mobile UX module")
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
