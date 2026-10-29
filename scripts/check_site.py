#!/usr/bin/env python3
"""Validate local links, anchors, shared assets, and theme bootstrap order.

Uses only Python's standard library so contributors do not need to install
project dependencies to run the checks locally.
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP_PAGES = {"shorts.html"}  # Minimal redirect page; it intentionally has no shared shell.


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicates: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.head_assets: list[str] = []
        self.in_head = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicates.add(element_id)
            self.ids.add(element_id)

        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.references.append((attr, value))

        if tag == "head":
            self.in_head = True
        if self.in_head:
            if tag == "script" and values.get("src"):
                self.head_assets.append(values["src"] or "")
            elif tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
                self.head_assets.append(values["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self.in_head = False


def within_root(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    pages = sorted(root.glob("*.html"))
    errors: list[str] = []
    parsers: dict[Path, PageParser] = {}

    if not pages:
        print(f"ERROR: no HTML pages found in {root}")
        return 1

    for page in pages:
        parser = PageParser()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
            parser.close()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{page.relative_to(root)}: cannot parse HTML: {exc}")
            continue
        parsers[page.resolve()] = parser
        if parser.duplicates:
            errors.append(
                f"{page.relative_to(root)}: duplicate id(s): "
                + ", ".join(sorted(parser.duplicates))
            )

        if page.name not in SKIP_PAGES:
            hrefs = [v for attr, v in parser.references if attr == "href"]
            srcs = [v for attr, v in parser.references if attr == "src"]
            for required in ("assets/style.css",):
                if required not in hrefs:
                    errors.append(f"{page.relative_to(root)}: missing {required}")
            for required in ("assets/app.js", "assets/theme-init.js"):
                if required not in srcs:
                    errors.append(f"{page.relative_to(root)}: missing {required}")

            try:
                theme_pos = parser.head_assets.index("assets/theme-init.js")
                style_pos = parser.head_assets.index("assets/style.css")
                if theme_pos > style_pos:
                    errors.append(
                        f"{page.relative_to(root)}: theme-init.js must load before style.css"
                    )
            except ValueError:
                errors.append(
                    f"{page.relative_to(root)}: theme bootstrap and stylesheet must both be in <head>"
                )

    for page, parser in parsers.items():
        for attr, raw_url in parser.references:
            url = urlsplit(raw_url.strip())
            if url.scheme or url.netloc or not url.path and not url.fragment:
                continue
            if raw_url.strip().startswith("#"):
                target = page
            elif url.path:
                decoded_path = unquote(url.path)
                target = (root / decoded_path.lstrip("/")) if decoded_path.startswith("/") else (
                    page.parent / decoded_path
                )
            else:
                target = page
            target = target.resolve()
            if not within_root(target, root):
                errors.append(
                    f"{page.relative_to(root)}: {attr} escapes site root: {raw_url}"
                )
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(
                    f"{page.relative_to(root)}: broken local {attr}: {raw_url}"
                )
                continue
            fragment = unquote(url.fragment)
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsers.get(target.resolve())
                if target_parser and fragment not in target_parser.ids:
                    errors.append(
                        f"{page.relative_to(root)}: missing anchor in "
                        f"{target.relative_to(root)}: #{fragment}"
                    )

    if errors:
        print(f"Site checks failed ({len(errors)} issue(s)):")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Site checks passed: {len(parsers)} HTML pages, local links and anchors valid.")
    print("Shared assets and early theme bootstrap are present on all content pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
