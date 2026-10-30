"""Streaming Huffman codec. Writes HUF2; reads HUF1 and HUF2."""

import heapq
import itertools
import hashlib
from collections import Counter
from pathlib import Path
from contextlib import contextmanager

MAGIC = b"HUF2"
CHUNK = 65536
DEFAULT_LIMIT = 1024**3


@contextmanager
def exclusive_output(destination):
    # Exclusive creation also rejects dangling symlinks and racing creators.
    out = open(destination, "xb")
    try:
        with out:
            yield out
    except BaseException:
        Path(destination).unlink(missing_ok=True)
        raise


def make_codes(tree):
    codes = {}

    def walk(node, bits):
        if isinstance(node, int):
            codes[node] = bits or "0"
        else:
            walk(node[0], bits + "0")
            walk(node[1], bits + "1")

    if tree is not None:
        walk(tree, "")
    return codes


def make_tree_from_frequencies(frequencies):
    serial = itertools.count()
    heap = [(count, next(serial), byte) for byte, count in sorted(frequencies.items())]
    heapq.heapify(heap)
    if not heap:
        return None
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(serial), (left, right)))
    return heap[0][2]


def compress(source, destination):
    frequencies = Counter()
    digest = hashlib.sha256()
    with open(source, "rb") as inp:
        for chunk in iter(lambda: inp.read(CHUNK), b""):
            frequencies.update(chunk)
            digest.update(chunk)
        size = sum(frequencies.values())
        codes = {
            b: (int(c, 2), len(c))
            for b, c in make_codes(make_tree_from_frequencies(frequencies)).items()
        }
        header = MAGIC + size.to_bytes(8, "big") + len(frequencies).to_bytes(2, "big")
        header += b"".join(
            bytes([b]) + n.to_bytes(8, "big") for b, n in sorted(frequencies.items())
        )
        header += digest.digest()
        inp.seek(0)
        check = hashlib.sha256()
        with exclusive_output(destination) as out:
            out.write(header)
            acc = used = 0
            buf = bytearray()
            for chunk in iter(lambda: inp.read(CHUNK), b""):
                check.update(chunk)
                for byte in chunk:
                    if byte not in codes:
                        raise ValueError("File nguồn thay đổi trong khi nén")
                    code, length = codes[byte]
                    acc = (acc << length) | code
                    used += length
                    while used >= 8:
                        used -= 8
                        buf.append((acc >> used) & 255)
                    acc &= (1 << used) - 1
                    if len(buf) >= CHUNK:
                        out.write(buf)
                        buf.clear()
            if used:
                buf.append(acc << (8 - used))
            out.write(buf)
            if check.digest() != digest.digest():
                raise ValueError("File nguồn thay đổi trong khi nén")
    return size, Path(destination).stat().st_size


def decompress(source, destination, max_output_bytes=DEFAULT_LIMIT):
    if type(max_output_bytes) is not int or max_output_bytes < 0:
        raise ValueError("Giới hạn giải nén không hợp lệ")
    with open(source, "rb") as inp:

        def read_exact(n):
            data = inp.read(n)
            if len(data) != n:
                raise ValueError("File nén bị cắt ngắn")
            return data

        magic = read_exact(4)
        if magic not in (b"HUF1", MAGIC):
            raise ValueError("Định dạng không được hỗ trợ")
        size = int.from_bytes(read_exact(8), "big")
        count = int.from_bytes(read_exact(2), "big")
        if size > max_output_bytes:
            raise ValueError("Vượt giới hạn dung lượng giải nén")
        if count > 256 or (size == 0) != (count == 0):
            raise ValueError("Header không hợp lệ")
        frequencies = {}
        for _ in range(count):
            b = read_exact(1)[0]
            n = int.from_bytes(read_exact(8), "big")
            if b in frequencies or n == 0:
                raise ValueError("Bảng tần suất không hợp lệ")
            frequencies[b] = n
        if sum(frequencies.values()) != size:
            raise ValueError("Sai tổng tần suất")
        expected = read_exact(32) if magic == MAGIC else None
        tree = make_tree_from_frequencies(frequencies)
        codes = make_codes(tree)
        total_bits = sum(n * len(codes[b]) for b, n in frequencies.items())
        payload_size = (total_bits + 7) // 8
        if Path(source).stat().st_size != inp.tell() + payload_size:
            raise ValueError("Sai độ dài payload")
        digest = hashlib.sha256()
        actual = Counter()
        written = processed = 0
        node = tree
        buf = bytearray()
        with exclusive_output(destination) as out:
            for chunk in iter(lambda: inp.read(CHUNK), b""):
                for byte in chunk:
                    for shift in range(7, -1, -1):
                        bit = (byte >> shift) & 1
                        if processed >= total_bits:
                            if bit:
                                raise ValueError("Padding không hợp lệ")
                            continue
                        processed += 1
                        if isinstance(tree, int):
                            if bit:
                                raise ValueError("Mã một ký hiệu không hợp lệ")
                            symbol = tree
                        else:
                            node = node[bit]
                            if not isinstance(node, int):
                                continue
                            symbol = node
                            node = tree
                        buf.append(symbol)
                        actual[symbol] += 1
                        written += 1
                        if written > size:
                            raise ValueError("Payload vượt kích thước khai báo")
                        if len(buf) >= CHUNK:
                            out.write(buf)
                            digest.update(buf)
                            buf.clear()
            out.write(buf)
            digest.update(buf)
            if written != size or actual != frequencies or node != tree:
                raise ValueError("Dữ liệu giải nén không hợp lệ")
            if expected is not None and digest.digest() != expected:
                raise ValueError("SHA-256 không khớp: file đã hỏng")
    return {"format": magic.decode(), "integrity_verified": expected is not None}
