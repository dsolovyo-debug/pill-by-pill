#!/usr/bin/env python3
"""Mobile card density, pill lists with show-more toggle, and collapsible sections on mobile."""
from __future__ import annotations

import pathlib
import sys

UI_ENHANCER_CSS = """
<style id="pbp-mobile-density-css">
.pbp-pill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 8px 0 12px;
}
.pbp-pill-list a,
.pbp-pill-list button {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 0.84rem;
  line-height: 1.25;
  text-decoration: none;
  border: 1px solid #d5dde9;
  background: #f8fafc;
  color: #16233b;
}
.pbp-pill-toggle {
  cursor: pointer;
  font-weight: 600;
  background: #eef2f8 !important;
}
details.pbp-compact-details {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 12px;
  margin: 10px 0;
  background: #ffffff;
}
details.pbp-compact-details > summary {
  cursor: pointer;
  font-weight: 600;
  color: #16233b;
  list-style: none;
}
details.pbp-compact-details > summary::-webkit-details-marker {
  display: none;
}
@media (max-width: 680px) {
  h1 {
    font-size: 1.55rem !important;
    line-height: 1.2 !important;
  }
  main p {
    max-width: 100%;
  }
}
</style>
"""

UI_ENHANCER_JS = """
<script id="pbp-mobile-density-js">
(function () {
  const MAX_VISIBLE_PILLS = 6;

  function compactLongLinkLists(root) {
    const containers = root.querySelectorAll("main p, main div, section p, section div");
    containers.forEach((el) => {
      if (el.dataset.pbpCompacted || el.closest(".pbp-subnav-bar, .pbp-submenu-panel, nav")) return;
      const links = Array.from(el.children).filter((c) => c.tagName === "A");
      if (links.length < 8) return;

      el.dataset.pbpCompacted = "1";
      const wrap = document.createElement("div");
      wrap.className = "pbp-pill-list";

      links.forEach((a, idx) => {
        const clone = a.cloneNode(true);
        if (idx >= MAX_VISIBLE_PILLS) {
          clone.classList.add("pbp-extra-pill");
          clone.style.display = "none";
        }
        wrap.appendChild(clone);
      });

      const extraCount = links.length - MAX_VISIBLE_PILLS;
      if (extraCount > 0) {
        const toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "pbp-pill-toggle";
        toggle.textContent = `+${extraCount} more`;
        toggle.addEventListener("click", () => {
          const expanded = toggle.dataset.expanded === "1";
          wrap.querySelectorAll(".pbp-extra-pill").forEach((node) => {
            node.style.display = expanded ? "none" : "inline-flex";
          });
          toggle.dataset.expanded = expanded ? "0" : "1";
          toggle.textContent = expanded ? `+${extraCount} more` : "Show less";
        });
        wrap.appendChild(toggle);
      }

      el.replaceWith(wrap);
    });
  }

  function wrapDenseSections(root) {
    if (window.innerWidth > 768) return;
    const cards = root.querySelectorAll("main section, main article, .card, .stage-card");
    cards.forEach((sec) => {
      if (sec.dataset.pbpWrapped || sec.querySelector("details")) return;
      const textLen = (sec.textContent || "").trim().length;
      const heading = sec.querySelector("h2, h3");
      if (!heading || textLen < 420) return;

      sec.dataset.pbpWrapped = "1";
      const title = heading.textContent.trim();
      const details = document.createElement("details");
      details.className = "pbp-compact-details";

      const summary = document.createElement("summary");
      summary.textContent = title;
      details.appendChild(summary);

      const bodyNodes = Array.from(sec.children).filter((c) => c !== heading);
      bodyNodes.forEach((n) => details.appendChild(n));
      heading.replaceWith(details);
    });
  }

  function runPass() {
    const target = document.getElementById("app") || document.body;
    if (!target) return;
    compactLongLinkLists(target);
    wrapDenseSections(target);
  }

  const obs = new MutationObserver(() => runPass());
  obs.observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("hashchange", () => setTimeout(runPass, 40));
  window.addEventListener("DOMContentLoaded", runPass);
})();
</script>
"""


def apply_patch(root: pathlib.Path) -> list[str]:
    changed: list[str] = []
    for html_path in root.rglob("*.html"):
        if not html_path.is_file():
            continue
        raw = html_path.read_text(encoding="utf-8", errors="ignore")
        if "pbp-mobile-density-css" in raw or "</body>" not in raw:
            continue
        updated = raw.replace("</body>", f"{UI_ENHANCER_CSS}\n{UI_ENHANCER_JS}\n</body>", 1)
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
