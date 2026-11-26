#!/usr/bin/env python3
"""Role-adaptive page body section ordering and quick-jump chips in main."""
from __future__ import annotations

import pathlib
import sys

ROLE_ADAPT_CSS = """
<style id="pbp-role-adapt-css">
.pbp-role-focus-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  margin: 0 0 12px;
  border-radius: 8px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  font-size: 0.85rem;
}
.pbp-role-focus-bar strong {
  color: #0f172a;
  margin-right: 4px;
}
.pbp-role-chip {
  border: 1px solid #94a3b8;
  background: #ffffff;
  color: #0f172a;
  border-radius: 999px;
  padding: 3px 9px;
  font-size: 0.8rem;
  cursor: pointer;
}
.pbp-role-dimmed {
  opacity: 0.58;
  order: 2;
}
.pbp-role-featured {
  order: 1;
  border-left: 3px solid #1e3a8a;
  padding-left: 10px;
}
main {
  display: flex;
  flex-direction: column;
}
</style>
"""

ROLE_ADAPT_JS = """
<script id="pbp-role-adapt-js">
(function () {
  const ROLE_KEYWORDS = {
    clinician: ["clinical", "trial", "endpoint", "safety", "pharmacovigilance", "dosing", "route", "diagnostic", "cdx", "real-world", "patient", "label", "rems"],
    chemist: ["discovery", "modality", "synthesis", "formulation", "analytical", "qc", "bioprocess", "sterile", "protac", "peptide", "oligonucleotide", "assay", "nam"],
    industry: ["cmc", "ich", "approval", "regulatory", "cdmo", "manufacturer", "supply chain", "dscsa", "patent", "ip", "economics", "pricing", "licensing", "m&a"]
  };

  function currentRole(root) {
    const active = root.querySelector('[aria-pressed="true"], .active, [aria-selected="true"]');
    const label = (active ? active.textContent : "").toLowerCase();
    if (label.includes("clinician") || label.includes("pharmacist")) return "clinician";
    if (label.includes("chemist") || label.includes("researcher")) return "chemist";
    if (label.includes("industry") || label.includes("regulatory")) return "industry";
    return "industry";
  }

  function applyRoleFocus() {
    const root = document.getElementById("app") || document.body;
    const main = root && root.querySelector("main");
    if (!main) return;

    const role = currentRole(root);
    const keywords = ROLE_KEYWORDS[role] || ROLE_KEYWORDS.industry;
    const blocks = Array.from(main.children).filter((el) => !el.classList.contains("pbp-role-focus-bar"));
    if (blocks.length < 2) return;

    let bar = main.querySelector(".pbp-role-focus-bar");
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "pbp-role-focus-bar";
      main.prepend(bar);
    }

    const roleTitle =
      role === "clinician"
        ? "Clinician & Pharmacist focus"
        : role === "chemist"
        ? "Chemist & Researcher focus"
        : "Industry & Regulatory focus";

    bar.innerHTML = `<strong>${roleTitle}:</strong>`;

    let matchedCount = 0;
    blocks.forEach((blk, i) => {
      blk.classList.remove("pbp-role-featured", "pbp-role-dimmed");
      const hay = (blk.textContent || "").toLowerCase();
      const hits = keywords.some((k) => hay.includes(k));
      if (hits) {
        blk.classList.add("pbp-role-featured");
        matchedCount += 1;
        const h = blk.querySelector("h2, h3");
        if (h && matchedCount <= 4) {
          if (!h.id) h.id = `pbp-sec-${i}`;
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "pbp-role-chip";
          chip.textContent = h.textContent.trim().slice(0, 32);
          chip.addEventListener("click", () => {
            h.scrollIntoView({ behavior: "smooth", block: "start" });
          });
          bar.appendChild(chip);
        }
      } else if (blocks.length >= 4) {
        blk.classList.add("pbp-role-dimmed");
      }
    });
  }

  const obs = new MutationObserver(() => applyRoleFocus());
  obs.observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("click", (e) => {
    if (e.target && e.target.closest("button, [role='tab'], a")) {
      setTimeout(applyRoleFocus, 50);
    }
  });
  window.addEventListener("hashchange", () => setTimeout(applyRoleFocus, 50));
})();
</script>
"""


def apply_patch(root: pathlib.Path) -> list[str]:
    changed: list[str] = []
    for html_path in root.rglob("*.html"):
        if not html_path.is_file():
            continue
        raw = html_path.read_text(encoding="utf-8", errors="ignore")
        if "pbp-role-adapt-css" in raw or "</body>" not in raw:
            continue
        updated = raw.replace("</body>", f"{ROLE_ADAPT_CSS}\n{ROLE_ADAPT_JS}\n</body>", 1)
        html_path.write_text(updated, encoding="utf-8")
        changed.append(str(html_path.relative_to(root)))
    return changed


def main() -> int:
    target = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    changed = apply_patch(target)
    print({"patched_files": changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
