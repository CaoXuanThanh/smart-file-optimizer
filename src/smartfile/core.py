"""Directory traversal and bounded Min-Heap selection."""

import heapq
import os
from pathlib import Path


def scan_files(folder, errors=None):
    """Yield regular non-symlink files; directory errors are reported."""
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Không thấy thư mục {root}")
    errors = errors if errors is not None else []
    for current, dirs, files in os.walk(
        root, followlinks=False, onerror=lambda exc: errors.append(str(exc))
    ):
        for name in files:
            path = Path(current) / name
            try:
                if path.is_symlink() or not path.is_file():
                    continue
                yield path.stat().st_size, str(path)
            except OSError as exc:
                errors.append(str(exc))


def select_top_k(entries, k):
    """O(K) selection memory. Equal sizes use descending path as tie-break."""
    if type(k) is not int or k < 1:
        raise ValueError("K phải là số nguyên > 0")
    heap = []
    for entry in entries:
        if len(heap) < k:
            heapq.heappush(heap, entry)
        elif entry > heap[0]:
            heapq.heapreplace(heap, entry)
    return sorted(heap, reverse=True)


def top_k(folder, k):
    errors = []
    scanned = 0

    def counted():
        nonlocal scanned
        for entry in scan_files(folder, errors):
            scanned += 1
            yield entry

    rows = select_top_k(counted(), k)
    return rows, scanned, errors


def readable(n):
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or unit == "TiB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.2f} {unit}"
        n /= 1024
