# Smart File Optimizer

**Đề tài 18 · CTDL & GT · Python · v0.2.0**

Tìm K file lớn nhất bằng Min-Heap giới hạn K phần tử, kèm nén/giải nén Huffman không mất dữ liệu. Tiếp tục từ bản Python bàn giao, giữ Streamlit và CLI. Top-K là trọng tâm, Huffman là mở rộng.

## Chạy trên Windows

Cài Python 3.11 hoặc 3.12. Mở terminal trong thư mục repo:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts/make_demo.py
.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

Nếu không có Python 3.12, đổi `py -3.12` thành `py -3.11`. Không cần activate môi trường. Trên Linux/macOS dùng `python3 -m venv .venv`, sau đó `.venv/bin/python`.

Nhập đường dẫn đầy đủ tới `demo_data`, chọn K=3 và Scan folder. Tab Huffman yêu cầu nhập rõ đường dẫn đích chưa tồn tại.

## CLI không cần Streamlit

```shell
python scripts/make_demo.py
python cli.py scan demo_data -k 3 --json
python cli.py scan demo_data -k 3 --csv top_k.csv
python cli.py compress demo_data/notes.txt demo_data/notes.huf
python cli.py decompress demo_data/notes.huf demo_data/restored.txt
python cli.py verify demo_data/notes.txt demo_data/restored.txt
```

Lệnh verify trả exit code 0 khi khớp, 2 khi khác. Lỗi thao tác trả 1. Chạy lại demo cần đổi tên đích; chương trình không tự ghi đè.

## Kiểm chứng

```shell
python -m unittest discover -s tests -v
python benchmarks/run.py
python benchmarks/disk_and_codec.py
```

28 test đạt trong môi trường Linux Python 3.12, gồm 2 test dashboard AppTest. Nếu không cài Streamlit thì hai test UI được bỏ qua. Kết quả, phương pháp và giới hạn nằm trong [VALIDATION.md](docs/VALIDATION.md). Dữ liệu gốc nằm trong `benchmarks/raw.csv`, `summary.json`, `disk_and_codec.json`, `environment.json`.

Benchmark N=50.000 record, K=10: heap 5,47 KiB peak allocation, sort 8.539,90 KiB. Đây là bộ nhớ Python của khâu lựa chọn với generator, không phải RAM toàn app. Thí nghiệm 10.000 file thật đo cả traversal được trình bày riêng. Không tuyên bố tốc độ đồng nhất trên mọi máy.

## Cấu trúc

- `src/smartfile/core.py`: scanner, bộ chọn heap, định dạng kích thước.
- `src/smartfile/huffman.py`: cây/mã Huffman, streaming HUF2 và đọc HUF1.
- `src/smartfile/operations.py`: kiểm tra thao tác và SHA-256.
- `app.py`, `cli.py`: dashboard và dòng lệnh.
- `tests/`, `benchmarks/`, `docs/`, `scripts/`: kiểm thử, bằng chứng và demo.

Chọn file dùng O(K) bộ nhớ, O(N log K) thời gian và O(K log K) sắp xếp đầu ra. Khi bằng kích thước, ưu tiên đường dẫn theo thứ tự giảm dần. K>N trả N file. Không theo symlink. O(K) không bao gồm danh sách tên của os.walk và danh sách lỗi.

## An toàn và giới hạn

Giữ file nguồn. Tạo đích bằng `xb`, không ghi đè. HUF2 kiểm tra SHA-256 và cấu trúc payload; HUF1 cũ không có checksum. Mặc định giải nén tối đa 1 GiB, CLI có `--max-output-mib`. Nén hai lượt đọc với buffer 64 KiB. Chi tiết trong [FORMAT.md](docs/FORMAT.md).

Bản đồ án chạy cục bộ, chưa production-ready. Chỉ dùng file tin cậy và ổn định trong thư mục do mình kiểm soát. File đích xuất hiện trong lúc ghi; mất điện có thể để lại file dở. SHA-256 không phải chữ ký hay mật khẩu. Dữ liệu đã nén hoặc ngẫu nhiên có thể tăng kích thước. Không hỗ trợ ZIP/RAR hay đóng gói nhiều file thành một archive.

Dashboard truy cập filesystem của máy chạy server; chỉ bind localhost. Chưa xác nhận Windows hay chạy CI GitHub. Cấu hình CI đã sẵn sàng, chưa có repo remote được tạo hoặc push.

## GitHub

Xem [GITHUB.md](docs/GITHUB.md) để đưa repo lên tài khoản của bạn. MIT áp dụng mã nguồn dự án trong gói này. Bộ đề và tài liệu bàn giao gốc không được đưa vào repo công khai.

English: a local academic Python application with bounded Min-Heap Top-K selection, a Streamlit dashboard, CLI, streaming Huffman compression and checksum verification. See [README.en.md](README.en.md).
