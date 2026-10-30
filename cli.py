"""Zero-dependency command-line interface."""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from smartfile.core import top_k, readable
from smartfile.operations import process, sha256


def main(argv=None):
    parser = argparse.ArgumentParser(description="Smart File Optimizer")
    sub = parser.add_subparsers(dest="mode", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("folder")
    scan.add_argument("-k", type=int, default=10)
    scan.add_argument("--csv", help="New CSV path, never overwritten")
    scan.add_argument("--json", action="store_true")
    for cmd in ("compress", "decompress"):
        p = sub.add_parser(cmd)
        p.add_argument("source")
        p.add_argument("destination")
        if cmd == "decompress":
            p.add_argument("--max-output-mib", type=int, default=1024)
    verify = sub.add_parser("verify")
    verify.add_argument("original")
    verify.add_argument("restored")
    args = parser.parse_args(argv)
    try:
        if args.mode == "scan":
            rows, total, errors = top_k(args.folder, args.k)
            if args.csv:
                with open(args.csv, "x", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["bytes", "path"])
                    writer.writerows(rows)
            if args.json:
                print(
                    json.dumps(
                        {"rows": rows, "scanned": total, "errors": errors},
                        ensure_ascii=False,
                    )
                )
            else:
                print(f"Đã quét {total} file. Top {len(rows)}:")
                for i, (size, path) in enumerate(rows, 1):
                    print(i, readable(size), path)
                if errors:
                    print("Bỏ qua", len(errors), "file/thư mục lỗi", file=sys.stderr)
        elif args.mode == "verify":
            a, b = sha256(args.original), sha256(args.restored)
            print(
                json.dumps(
                    {"match": a == b, "original_sha256": a, "restored_sha256": b}
                )
            )
            return 0 if a == b else 2
        else:
            kwargs = (
                {"max_output_bytes": args.max_output_mib * 1024**2}
                if args.mode == "decompress"
                else {}
            )
            print(
                json.dumps(
                    process(args.mode, args.source, args.destination, **kwargs),
                    ensure_ascii=False,
                )
            )
        return 0
    except (OSError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
