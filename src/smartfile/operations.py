"""Local file operations. Never overwrite an existing destination."""

from pathlib import Path
import hashlib
import os
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
    try:
        same_file = os.path.samefile(src, dst)
    except (FileNotFoundError, OSError):
        same_file = os.path.normcase(os.path.abspath(src)) == os.path.normcase(
            os.path.abspath(dst)
        )
    if same_file:
        raise ValueError("Không được ghi đè file nguồn")
    # Path.exists() follows symlinks and returns False for dangling links.
    # Check the directory entry itself before doing any work; exclusive `xb`
    # creation remains the final race-safe guard in the codec.
    if dst.exists() or dst.is_symlink():
        raise FileExistsError("File đích đã tồn tại")
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
