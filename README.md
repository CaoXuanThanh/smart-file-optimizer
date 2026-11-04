# Smart File Optimizer

Tìm các file chiếm nhiều dung lượng trong thư mục và nén file bằng Huffman. Ứng dụng Python chạy cục bộ, cung cấp giao diện trình duyệt và CLI.

## Tính năng

- Quét thư mục và thư mục con, tìm K file lớn nhất bằng Min-Heap.
- Hiển thị kích thước, đường dẫn, biểu đồ và xuất CSV.
- Nén một file sang `.huf`, giải nén và đối chiếu SHA-256.
- Giữ nguyên file nguồn, từ chối ghi đè file đích đã tồn tại.
- Bản Windows portable đóng gói cùng Python và thư viện phụ thuộc.

## Bắt đầu

### Windows portable

Mở [GitHub Actions](https://github.com/CaoXuanThanh/smart-file-optimizer/actions), chọn lượt **Build Windows portable** thành công và tải artifact `SmartFileOptimizer-Windows-x64`.

Giải nén toàn bộ gói, giữ `SmartFileOptimizer.exe` cùng thư mục `_internal`, rồi mở EXE. Truy cập `http://127.0.0.1:8501` nếu trình duyệt chưa tự mở. Giữ cửa sổ chương trình mở trong khi sử dụng; đóng cửa sổ đó để dừng ứng dụng.

### Chạy từ mã nguồn

CI kiểm tra Python 3.11 và 3.12 trên Windows và Linux. Tại thư mục có `app.py`, chạy:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/make_demo.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Trên Linux/macOS, dùng `python3 -m venv .venv` và thay đường dẫn Python bằng `.venv/bin/python`.

Trong **TOP-K EXPLORER**, nhập đường dẫn thư mục, chọn K và bấm Scan folder. Trong **HUFFMAN LAB**, chọn file nguồn cùng một đường dẫn đích chưa tồn tại. Dữ liệu được xử lý trên máy chạy ứng dụng.

## CLI

CLI sử dụng thư viện chuẩn Python và không cần Streamlit. Các ví dụ dùng `python`; có thể thay bằng đường dẫn Python trong `.venv`.

```shell
python cli.py scan demo_data -k 3 --json
python cli.py scan demo_data -k 3 --csv top_k.csv
python cli.py compress demo_data/notes.txt demo_data/notes.huf
python cli.py decompress demo_data/notes.huf demo_data/restored.txt
python cli.py verify demo_data/notes.txt demo_data/restored.txt
```

Chạy `python scripts/make_demo.py` để tạo dữ liệu mẫu. File CSV, file nén và file khôi phục phải chưa tồn tại. Khi chạy lại, chọn tên đầu ra mới.

`verify` trả mã thoát 0 khi SHA-256 khớp, 2 khi khác. Lỗi thao tác trả 1. Dùng `python cli.py --help` để xem các lệnh và `python cli.py decompress --help` để xem giới hạn đầu ra.

## Kiểm thử và phát triển

```shell
python -m unittest discover -s tests -v
python benchmarks/run.py
python benchmarks/disk_and_codec.py
```

Lần kiểm tra Linux ngày 04/11/2026 đạt 28/28 test, không bỏ qua. Xem [log kiểm thử](docs/test_results_latest.txt) và [phạm vi kiểm chứng](docs/VALIDATION.md). CI gồm kiểm thử Windows/Linux và đóng gói Windows với kiểm tra khởi động EXE.

Script benchmark ghi kết quả vào `benchmarks/`. Các số đo công bố có môi trường và phương pháp kèm theo; không phải cam kết tốc độ trên mọi máy.

## Cấu trúc dự án

| Đường dẫn | Nội dung |
|---|---|
| `app.py` | Giao diện Streamlit |
| `cli.py` | Giao diện dòng lệnh |
| `launcher.py` | Điểm khởi động bản portable |
| `src/smartfile/` | Quét thư mục, Top-K, Huffman và kiểm tra dữ liệu |
| `tests/` | Kiểm thử thuật toán và giao diện |
| `benchmarks/` | Công cụ đo và số liệu thực nghiệm |
| `scripts/` | Tạo dữ liệu demo |
| `docs/` | Thiết kế, định dạng file, kiểm chứng và hướng dẫn phát triển |
| `.github/workflows/` | Kiểm thử và đóng gói tự động |

## Định dạng và giới hạn

HUF2 lưu bảng tần suất cùng SHA-256 để kiểm tra dữ liệu khôi phục. Chương trình vẫn đọc HUF1 cũ nhưng định dạng đó không có checksum. Nén đọc nguồn hai lượt với khối 64 KiB, vì vậy nguồn cần ổn định trong suốt thao tác.

- Hỗ trợ một file mỗi thao tác; không đọc ZIP/RAR hay gom thư mục thành archive.
- Dữ liệu khó nén có thể tăng dung lượng do thông tin phụ trong file nén.
- Giới hạn giải nén mặc định 1 GiB; CLI cho phép đặt `--max-output-mib`.
- File đầu ra xuất hiện trong lúc ghi. Dừng tiến trình cưỡng bức có thể để lại file dở.
- Chưa có chức năng hủy tác vụ và thanh tiến độ cho file lớn.
- SHA-256 kiểm tra tính toàn vẹn, không cung cấp mật khẩu hoặc chữ ký xác thực.

Ứng dụng mặc định chỉ lắng nghe trên localhost. Xem [định dạng HUF](docs/FORMAT.md) trước khi tích hợp với công cụ khác.

## Tài liệu

- [Thiết kế thuật toán, lưu đồ và phân tích thực nghiệm](docs/TECHNICAL_REPORT.md)
- [Kết quả kiểm chứng](docs/VALIDATION.md)
- [Hướng dẫn bản Windows portable](docs/PORTABLE_WINDOWS.md)
- [Quy trình cập nhật và commit](docs/GITHUB.md)
- [Lịch sử thay đổi](CHANGELOG.md)

## Giấy phép

Mã nguồn được cung cấp theo [MIT License](LICENSE).
