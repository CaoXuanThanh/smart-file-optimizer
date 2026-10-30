"""Create predictable demo data. Existing files are preserved."""

from pathlib import Path
import random

root = Path("demo_data")
root.mkdir(exist_ok=True)
fixtures = {
    "notes.txt": ("Cau truc du lieu va giai thuat. Min-Heap Top-K.\n" * 12000).encode(),
    "binary.bin": bytes(range(256)) * 1024,
    "random.bin": random.Random(18).randbytes(131072),
    "small.txt": b"Hello Python!",
    "empty.txt": b"",
}
for name, data in fixtures.items():
    path = root / name
    if not path.exists():
        path.write_bytes(data)
print(root.resolve())
