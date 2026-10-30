import unittest
import tempfile
import random
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from smartfile.core import top_k, select_top_k
from smartfile.operations import process, sha256
from smartfile.huffman import compress, decompress


class ExtendedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.a, self.b, self.c = [self.root / n for n in ("a", "b", "c")]
        self.a.write_bytes(b"ABACABA" * 100)

    def test_invalid_k(self):
        for k in (0, -1, 1.5, True, "2"):
            with self.subTest(k=k), self.assertRaises(ValueError):
                top_k(self.root, k)

    def test_missing_folder(self):
        with self.assertRaises(NotADirectoryError):
            top_k(self.root / "missing", 1)

    def test_k_above_n_and_ties(self):
        self.b.write_bytes(self.a.read_bytes())
        rows, n, _ = top_k(self.root, 10)
        self.assertEqual(
            rows, sorted([(700, str(self.a)), (700, str(self.b))], reverse=True)
        )
        self.assertEqual(n, 2)

    def test_random_top_k_oracle(self):
        r = random.Random(18)
        for n in (1, 100, 10000):
            values = [(r.randrange(100), str(i)) for i in range(n)]
            for k in (1, 10, n + 1):
                self.assertEqual(
                    select_top_k(iter(values), k), sorted(values, reverse=True)[:k]
                )

    def test_symlinks_skipped(self):
        try:
            self.b.symlink_to(self.a)
        except OSError:
            self.skipTest("Symlinks unavailable")
        self.assertEqual(top_k(self.root, 5)[1], 1)

    def test_walk_permission_error(self):
        def walk(*args, **kwargs):
            kwargs["onerror"](PermissionError("simulated permission denial"))
            return iter([])

        with patch("smartfile.core.os.walk", walk):
            self.assertEqual(len(top_k(self.root, 1)[2]), 1)

    def test_disappearing_file(self):
        with patch(
            "smartfile.core.os.walk",
            return_value=iter([(str(self.root), [], ["missing"])]),
        ):
            self.assertEqual(top_k(self.root, 1)[1], 0)

    def test_existing_destination_preserved(self):
        self.b.write_bytes(b"KEEP")
        for fn in (compress, lambda a, b: process("compress", a, b)):
            with self.assertRaises(FileExistsError):
                fn(self.a, self.b)
            self.assertEqual(self.b.read_bytes(), b"KEEP")

    def test_dangling_symlink_preserved(self):
        try:
            self.b.symlink_to(self.c)
        except OSError:
            self.skipTest("Symlinks unavailable")
        with self.assertRaises(FileExistsError):
            process("compress", self.a, self.b)
        self.assertTrue(self.b.is_symlink())
        self.assertFalse(self.c.exists())

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            process("oops", self.a, self.b)
        self.assertFalse(self.b.exists())

    def test_missing_input(self):
        with self.assertRaises(FileNotFoundError):
            process("compress", self.c, self.b)

    def test_multichunk_roundtrip(self):
        self.a.write_bytes(random.Random(18).randbytes(1048576))
        process("compress", self.a, self.b)
        result = process("decompress", self.b, self.c)
        self.assertTrue(result["integrity_verified"])
        self.assertEqual(sha256(self.a), sha256(self.c))

    def test_truncated_archives(self):
        compress(self.a, self.b)
        data = self.b.read_bytes()
        for cut in (0, 4, 12, 14, 20, len(data) - 1):
            self.b.write_bytes(data[:cut])
            with self.subTest(cut=cut), self.assertRaises(ValueError):
                decompress(self.b, self.c)
            self.assertFalse(self.c.exists())

    def test_checksum_corruption_cleanup(self):
        compress(self.a, self.b)
        data = bytearray(self.b.read_bytes())
        data[-2] ^= 1
        self.b.write_bytes(data)
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)
        self.assertFalse(self.c.exists())

    def test_trailing_garbage(self):
        compress(self.a, self.b)
        with self.b.open("ab") as f:
            f.write(b"x")
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)

    def test_output_limit(self):
        compress(self.a, self.b)
        with self.assertRaises(ValueError):
            decompress(self.b, self.c, 10)
        self.assertFalse(self.c.exists())

    def test_single_symbol_truncation(self):
        self.a.write_bytes(b"x" * 1000)
        compress(self.a, self.b)
        self.b.write_bytes(self.b.read_bytes()[:-1])
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)

    def test_bad_padding(self):
        self.a.write_bytes(b"x")
        compress(self.a, self.b)
        data = bytearray(self.b.read_bytes())
        data[-1] |= 1
        self.b.write_bytes(data)
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)

    def test_legacy_huf1(self):
        # Fixture matches old deterministic two-symbol tree A=0, B=1.
        self.b.write_bytes(
            b"HUF1"
            + (4).to_bytes(8, "big")
            + (2).to_bytes(2, "big")
            + b"A"
            + (2).to_bytes(8, "big")
            + b"B"
            + (2).to_bytes(8, "big")
            + b"\x50"
        )
        result = decompress(self.b, self.c)
        self.assertEqual(self.c.read_bytes(), b"ABAB")
        self.assertFalse(result["integrity_verified"])

    def test_wrong_magic(self):
        self.b.write_bytes(b"BAD!" + b"\0" * 20)
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)

    def test_duplicate_symbols(self):
        self.b.write_bytes(
            b"HUF1"
            + (2).to_bytes(8, "big")
            + (2).to_bytes(2, "big")
            + (b"A" + (1).to_bytes(8, "big")) * 2
            + b"\0"
        )
        with self.assertRaises(ValueError):
            decompress(self.b, self.c)

    def test_incompressible_expands(self):
        self.a.write_bytes(bytes(range(256)) * 100)
        result = process("compress", self.a, self.b)
        self.assertLess(result["saving_percent"], 0)


if __name__ == "__main__":
    unittest.main()
