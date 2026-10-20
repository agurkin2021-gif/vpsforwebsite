import base64
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("site_integrity", Path(__file__).with_name("audit-site-integrity.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class IntegrityAuditTests(unittest.TestCase):
    def test_valid_relative_unicode_redirect_and_css_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fr").mkdir()
            (root / "fr/été").mkdir()
            (root / "css").mkdir()
            (root / "fonts").mkdir()
            css = b'@font-face{src:url("../fonts/site.woff2")}body{color:green}'
            (root / "css/site.css").write_bytes(css)
            (root / "fonts/site.woff2").write_bytes(b"font")
            sri = "sha256-" + base64.b64encode(hashlib.sha256(css).digest()).decode()
            (root / "fr/index.html").write_text(
                '<base href="https://vpsforwebsite.com/fr/">'
                '<a href="%C3%A9t%C3%A9/?x=1#title">Article</a>'
                f'<link rel="stylesheet" href="../css/site.css" integrity="{sri}">'
                '<a href="https://example.com/">External</a>', encoding="utf-8")
            (root / "fr/été/index.html").write_text('<h1 id="title">Article</h1>', encoding="utf-8")
            (root / "index.html").write_text('<meta http-equiv="refresh" content="0; url=/fr/">', encoding="utf-8")
            self.assertEqual(module.audit(root)["errors"], [])

    def test_missing_page_stylesheet_and_font_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<a href="/missing/">Missing</a>'
                '<link rel="stylesheet" href="/gone.css">'
                '<link rel="stylesheet" href="/site.css">', encoding="utf-8")
            (root / "site.css").write_text('@font-face{src:url("gone.woff2")}', encoding="utf-8")
            errors = module.audit(root)["errors"]
            for expected in ("/missing/", "/gone.css", "gone.woff2"):
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_corrupted_stylesheet_fails_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sri = "sha256-" + base64.b64encode(hashlib.sha256(b"original").digest()).decode()
            (root / "index.html").write_text(
                f'<link href="/site.css" integrity="{sri}">', encoding="utf-8")
            (root / "site.css").write_bytes(b"corrupted")
            self.assertTrue(any("invalid integrity" in e for e in module.audit(root)["errors"]))


if __name__ == "__main__":
    unittest.main()
