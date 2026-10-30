import sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from smartfile.core import top_k
from smartfile.operations import process, sha256


class Tests(unittest.TestCase):
    def test_topk(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "sub").mkdir()
            for name, size in [("a", 4), ("b", 9), ("sub/c", 12), ("sub/d", 2)]:
                (root / name).write_bytes(b"x" * size)
            rows, n, errors = top_k(root, 2)
            self.assertEqual([s for s, _ in rows], [12, 9])
            self.assertEqual(n, 4)
            self.assertEqual(errors, [])

    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(top_k(d, 3)[0], [])

    def test_roundtrip(self):
        for data in [
            b"",
            b"A" * 1000,
            "Xin chao Viet Nam!".encode() * 1000,
            bytes(range(256)) * 20,
        ]:
            with self.subTest(n=len(data)), tempfile.TemporaryDirectory() as d:
                a = Path(d) / "a"
                b = Path(d) / "b.huf"
                c = Path(d) / "c"
                a.write_bytes(data)
                process("compress", a, b)
                process("decompress", b, c)
                self.assertEqual(a.read_bytes(), c.read_bytes())
                self.assertEqual(sha256(a), sha256(c))

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d) / "a"
            a.write_bytes(b"x")
            with self.assertRaises(ValueError):
                process("compress", a, a)


if __name__ == "__main__":
    unittest.main()
