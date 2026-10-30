"""Optional dashboard integration tests; install requirements.txt first."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(
    importlib.util.find_spec("streamlit"), "Streamlit is optional for CLI"
)
class DashboardTests(unittest.TestCase):
    def test_scan_and_error_state(self):
        from streamlit.testing.v1 import AppTest

        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "hello.txt").write_text("hello")
            app = AppTest.from_file(
                str(Path(__file__).resolve().parents[1] / "app.py")
            ).run()
            self.assertFalse(app.exception)
            app.text_input[0].set_value(d)
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.metric[0].value, "1")
            app.text_input[0].set_value(str(Path(d) / "missing"))
            app.button[0].click().run()
            self.assertTrue(app.error)
            self.assertEqual(len(app.metric), 0)

    def test_compress_decompress_ui(self):
        from streamlit.testing.v1 import AppTest

        with tempfile.TemporaryDirectory() as d:
            a, b, c = [Path(d) / x for x in ("input", "packed", "restored")]
            a.write_bytes(b"abc" * 100)
            app = AppTest.from_file(
                str(Path(__file__).resolve().parents[1] / "app.py")
            ).run()
            app.text_input[1].set_value(str(a))
            app.text_input[2].set_value(str(b))
            app.button[1].click().run()
            self.assertFalse(app.exception)
            self.assertTrue(b.exists())
            app.radio[0].set_value("Giải nén file")
            app.text_input[1].set_value(str(b))
            app.text_input[2].set_value(str(c))
            app.button[1].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(a.read_bytes(), c.read_bytes())
