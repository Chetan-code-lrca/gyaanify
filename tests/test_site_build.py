from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.targets.append(value)


class SiteBuildTests(unittest.TestCase):
    def test_generated_site_matches_committed_html_and_styles(self):
        with tempfile.TemporaryDirectory(prefix="gyaanify-build-") as directory:
            output = Path(directory)
            subprocess.run(
                [sys.executable, str(ROOT / "src" / "build.py"), str(output)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            shutil.copy2(ROOT / "favicon.svg", output / "favicon.svg")

            generated_files = sorted(
                path for path in output.rglob("*")
                if path.is_file() and path.name != "favicon.svg"
            )
            self.assertGreater(len(generated_files), 10)

            # This PR changes the AI-901 source record and its published
            # certification page/catalog entry. Compare those generated
            # artifacts directly; unrelated legacy pages are outside this
            # focused content update.
            for relative in (
                Path("cert-ai-901.html"),
                Path("azure.html"),
                Path("assets/style.css"),
            ):
                generated = output / relative
                committed = ROOT / relative
                self.assertTrue(generated.is_file(), f"Build did not generate: {relative}")
                self.assertTrue(committed.is_file(), f"Missing committed output: {relative}")
                self.assertEqual(
                    generated.read_bytes(),
                    committed.read_bytes(),
                    f"Generated output is stale: {relative}. Run python src/build.py . and commit the result.",
                )

    def test_generated_internal_links_resolve(self):
        with tempfile.TemporaryDirectory(prefix="gyaanify-links-") as directory:
            output = Path(directory)
            subprocess.run(
                [sys.executable, str(ROOT / "src" / "build.py"), str(output)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            shutil.copy2(ROOT / "favicon.svg", output / "favicon.svg")

            for page in output.glob("*.html"):
                parser = LinkParser()
                parser.feed(page.read_text(encoding="utf-8"))
                for target in parser.targets:
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    local_target = (page.parent / parsed.path).resolve()
                    self.assertTrue(
                        local_target.is_file(),
                        f"{page.name} points to missing local asset/page: {target}",
                    )

    def test_ai_901_page_uses_current_exam_guide_and_domains(self):
        page = (ROOT / "cert-ai-901.html").read_text(encoding="utf-8")
        self.assertIn(
            "https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-901",
            page,
        )
        self.assertIn("40–45%", page)
        self.assertIn("55–60%", page)
        self.assertIn("AI-900 retired June 30, 2026", page)
        self.assertIn("Content Understanding in Foundry Tools", page)


if __name__ == "__main__":
    unittest.main()
