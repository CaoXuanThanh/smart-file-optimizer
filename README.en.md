# Smart File Optimizer 0.2.0

Python academic project: bounded Min-Heap selection of the K largest local files, plus optional lossless Huffman compression. The existing Python codebase is retained and improved.

Python 3.11/3.12 recommended. Install `requirements.txt`, then run `python -m streamlit run app.py --server.address 127.0.0.1`. CLI works with the standard library alone. Run `python scripts/make_demo.py` to create sample files.

`python cli.py scan demo_data -k 3`, `compress source destination`, `decompress source destination`, and `verify original restored` provide the main operations. Destinations must not exist.

Tests: `python -m unittest discover -s tests -v`. Benchmarks: `python benchmarks/run.py` and `python benchmarks/disk_and_codec.py`. Measured results and limitations are in `docs/VALIDATION.md`. The record benchmark and real-directory benchmark are reported separately. Python peak allocations are not process RSS.

HUF2 adds SHA-256 to the original deterministic Huffman format. HUF1 remains readable without checksum verification. Streaming compression uses two passes and 64 KiB buffers. Default decompression limit is 1 GiB. Source files must remain stable. Output becomes visible during writing; interrupted processes may leave partial output.

Academic local prototype, not production archival software. No encryption, ZIP/RAR compatibility or guarantee of compression savings. Windows and hosted CI remain unverified. MIT license.
