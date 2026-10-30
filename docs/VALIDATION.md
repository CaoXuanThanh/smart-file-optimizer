# Kết quả kiểm chứng 30/10/2026

## Trạng thái

28/28 test đạt trên Linux, Python 3.12. Có hai test tích hợp Streamlit bằng AppTest. CLI scan/compress/decompress/verify đã chạy thực tế và hash trùng nhau. Chưa chạy trên Windows của người trình bày. CI Windows/Linux đã cấu hình nhưng chưa chạy trên GitHub. Chưa có ảnh dashboard từ trình duyệt: môi trường không tải được Chromium, không dùng ảnh giả thay thế.

## Phương pháp đo

`python benchmarks/run.py`: bản ghi tổng hợp (size, path), seed 18. N = 10.000 / 25.000 / 50.000, K = 10 / 100 / 1.000. Hai phương án nhận cùng generator tái tạo theo seed. Có một lượt warmup và 5 lần đo mỗi cấu hình. Thời gian đo không bật tracemalloc. Peak allocation đo ở lượt riêng. Cả hai gồm chi phí sinh record và sắp xếp kết quả. Không gồm I/O ổ đĩa. Đối chiếu đầy đủ tuple với sort sau mỗi lượt. Bộ nhớ là cấp phát Python, không phải RSS toàn ứng dụng.

| N | K | Phương án | Trung vị ms | Peak KiB |
|---:|---:|---|---:|---:|
| 10000 | 10 | heap | 7.36 | 5.47 |
| 10000 | 10 | sort | 8.63 | 1704.81 |
| 10000 | 100 | heap | 6.56 | 20.43 |
| 10000 | 100 | sort | 9.22 | 1704.81 |
| 10000 | 1000 | heap | 8.34 | 179.35 |
| 10000 | 1000 | sort | 10.77 | 1704.81 |
| 25000 | 10 | heap | 16.75 | 5.47 |
| 25000 | 10 | sort | 26.55 | 4267.17 |
| 25000 | 100 | heap | 16.05 | 20.43 |
| 25000 | 100 | sort | 29.41 | 4267.17 |
| 25000 | 1000 | heap | 19.75 | 179.35 |
| 25000 | 1000 | sort | 28.03 | 4267.17 |
| 50000 | 10 | heap | 32.09 | 5.47 |
| 50000 | 10 | sort | 56.71 | 8539.90 |
| 50000 | 100 | heap | 32.89 | 20.43 |
| 50000 | 100 | sort | 56.96 | 8539.90 |
| 50000 | 1000 | heap | 35.17 | 179.35 |
| 50000 | 1000 | sort | 62.98 | 8539.90 |

## Thư mục thật

`python benchmarks/disk_and_codec.py` tạo 10.000 file (100 thư mục × 100 file), mỗi file 0–2.047 byte. Tạo fixture ngoài phép đo. Cùng scanner và cùng quy tắc tie-break. K=10, warmup và 5 lần đo, lượt đo peak tách riêng thời gian. Có cache hệ thống, không phải phép đo cold disk. Quét không có lỗi và Top-K khớp oracle sort.

| Phương án | Trung vị ms | Peak KiB |
|---|---:|---:|
| heap | 138.89 | 422.70 |
| sort | 138.32 | 1840.34 |

Ở lần đo này, thời gian quét đĩa gần bằng nhau vì duyệt và stat chiếm phần lớn chi phí. Lợi ích bộ nhớ vẫn hiện rõ. Không kết luận heap luôn nhanh hơn sort hoặc áp số liệu này cho Windows.

O(K) chỉ là bộ nhớ lựa chọn. `os.walk` còn giữ danh sách tên trong từng thư mục, danh sách lỗi tốn O(E) và bảng giao diện giữ O(K). Thời gian lựa chọn O(N log K), sắp xếp cuối O(K log K), riêng K=1 là O(N).

## Huffman

Fixture tự sinh, mỗi loại chạy một lượt nén và giải nén. Thời gian trong JSON là quan sát tham khảo, không dùng để kết luận tốc độ codec.

| Dữ liệu | Gốc B | HUF2 B | Tiết kiệm | SHA-256 |
|---|---:|---:|---:|---|
| repeated_text | 600000 | 317735 | 47.04% | Khớp |
| uniform_bytes | 524288 | 526638 | -0.45% | Khớp |
| seeded_random | 524288 | 526638 | -0.45% | Khớp |
| empty | 0 | 46 | Không xác định | Khớp |

Dữ liệu lặp giảm khoảng 47%; byte phân bố đều/ngẫu nhiên tăng khoảng 0,45% do header. File rỗng có 46 byte header. Không suy rộng mức tiết kiệm cho file người dùng.

## Audit và giới hạn còn lại

Giữ cấu trúc app/CLI/core/Huffman/operations từ ZIP GitHub. Hai ZIP cũ đã đối chiếu để tham khảo, không thay thế bản tích hợp. Các lỗi sửa: ghi đè ở codec trực tiếp, kiểm tra tồn tại rồi ghi có cửa sổ race, nhánh một ký hiệu bỏ qua payload, không kiểm tra checksum, đọc toàn nguồn vào RAM, mode sai bị coi như giải nén, kết quả quét cũ còn hiển thị khi quét lỗi, widget đích reset theo nguồn.

Lỗi quyền truy cập và file biến mất được giả lập có kiểm soát vì môi trường chạy quyền cao. Test symlink có thể skip trên Windows không cấp quyền. Kết quả pass ở đây không thay thế thử nghiệm máy trình bày. Giới hạn còn lại: không có hủy tác vụ, không khóa nguồn đang bị chỉnh sửa, không ghi đích theo cơ chế publish nguyên tử, không fuzzing đầy đủ, không thử filesystem thù địch hoặc file nhiều GiB. Không production-ready.
