"""Local file operations. Never overwrite an existing destination."""

from pathlib import Path
import hashlib
from .huffman import compress, decompress, DEFAULT_LIMIT


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def process(mode, source, target, max_output_bytes=DEFAULT_LIMIT):
    if mode not in ("compress", "decompress"):
        raise ValueError("Chế độ không hợp lệ")
    src = Path(source).expanduser().resolve()
    dst = Path(target).expanduser().absolute()
    if not src.is_file():
        raise FileNotFoundError("Không tìm thấy file nguồn")
    if src == dst.resolve():
        raise ValueError("Không được ghi đè file nguồn")
    if mode == "compress":
        before, after = compress(src, dst)
        return {
            "before": before,
            "after": after,
            "format": "HUF2",
            "saving_percent": (1 - after / before) * 100 if before else 0,
        }
    result = decompress(src, dst, max_output_bytes)
    return dict(result, after=dst.stat().st_size, sha256=sha256(dst))
