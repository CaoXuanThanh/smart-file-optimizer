# Windows portable (build candidate)

Gói nguồn có workflow để GitHub tạo executable Windows x64. Chưa có bản EXE được build/xác nhận trong môi trường hỗ trợ này.

## Trên máy nhận (không cần Python)

1. Giải nén toàn bộ artifact SmartFileOptimizer-Windows-x64.
2. Giữ SmartFileOptimizer.exe và thư mục _internal cạnh nhau. Không chỉ copy mỗi EXE.
3. Nhấp đúp SmartFileOptimizer.exe, giữ cửa sổ terminal đang mở.
4. Trình duyệt mở ứng dụng; nếu không tự mở, truy cập http://127.0.0.1:8501.
5. Nhập đường dẫn tồn tại trên máy mới. Đóng cửa sổ terminal để dừng.

Cần Windows x64 có trình duyệt. Gói này không dành cho macOS/Linux. Không cần mạng cho xử lý file cục bộ sau khi đã tải gói. Nếu cổng 8501 đang được app khác dùng, đóng phiên SmartFileOptimizer cũ trước.

## GitHub từ đầu

1. Đăng nhập github.com, bấm dấu +, New repository.
2. Đặt tên smart-file-optimizer, chọn Private. Bật Add README để dễ upload rồi Create repository.
3. Add file > Upload files. Kéo toàn bộ NỘI DUNG thư mục SmartFileOptimizer vào, gồm .github, src, tests, docs, benchmarks, scripts và các file ở gốc. Không upload ZIP nguyên khối, .venv, __pycache__, demo_data.
4. Bấm Commit changes. Ở gốc repo phải thấy app.py, launcher.py, requirements.txt, .github.
5. Mở Actions > Build Windows portable. Lần push main tự chạy. Nếu cần chạy lại: Run workflow > main > Run workflow.
6. Khi xanh, mở lần chạy đó, kéo xuống Artifacts, tải SmartFileOptimizer-Windows-x64. Giải nén và dùng như hướng dẫn trên.
7. Nếu đỏ, mở job build, mở bước có dấu X và gửi log lỗi.

Nếu upload thiếu .github: Add file > Create new file, nhập .github/workflows/windows-portable.yml và dán nội dung file cùng tên trong gói nguồn, rồi Commit changes. Làm tương tự tests.yml nếu thiếu.

Python checks kiểm thử mã trên Linux/Windows. Build Windows portable kiểm thử rồi đóng gói với Python 3.12, độc lập Python 3.14 trên máy bạn. Startup smoke check chỉ xác nhận server EXE phản hồi health, chưa chứng minh mọi thao tác UI trong gói hoạt động. Cần thử quét/nén/giải nén trên một máy Windows sạch trước khi phát hành rộng.

Đóng gói không đồng nghĩa production-ready. Chưa code-sign EXE. Không tắt antivirus để chạy file bị cảnh báo; kiểm tra nguồn và log trước.
