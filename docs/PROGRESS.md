# Nhật ký thực hiện

Chỉ ghi mốc có bằng chứng trong dữ liệu bàn giao và kết quả kiểm tra. Không gán công việc cho người chưa được xác nhận, không dựng lại ngày bắt đầu hoặc kế hoạch nhóm giả định.

| Mốc | Công việc / kết quả | Căn cứ |
|---|---|---|
| 30/10/2026 | Hoàn thiện bản tích hợp Top-K, Huffman, CLI và dashboard; đo các cấu hình dữ liệu tổng hợp, quét 10.000 file thực | benchmarks/environment.json, raw.csv, summary.json, disk_and_codec.json; log test lưu ngày 30/10 |
| 30/10/2026 | Đưa mã lên GitHub và bổ sung workflow Windows portable | Commit 189db37, thông tin lịch sử Git trong bản bàn giao |
| Sau lượt CI đầu lỗi | Sửa đối chiếu đường dẫn Windows và kiểm tra đích là symlink hỏng | tests/test_extended.py, operations.py; ảnh CI commit 9da8fed trong quá trình bàn giao |
| 01/11/2026 | Đồng bộ launcher để tắt developmentMode khi chạy EXE; hai workflow thành công | Ảnh Actions: Python checks #2, Build Windows portable #3, commit 2ffec51 |
| 01/11/2026 | Hoàn thiện PowerPoint 18 slide và hướng dẫn tập thuyết trình | Smart_File_Optimizer_BAO_CAO.pptx, docs/SPEAKER_NOTES.md |
| 04/11/2026 | Đọc thang điểm mới, bổ sung lưu đồ, lựa chọn tài liệu, bảng kiểm thử; đối chiếu phiên bản với GitHub | README.md, docs/VERSION_CHECK.md và log test ngày 04/11 |

## Việc còn lại của người trình bày

1. Tập demo và lời dẫn trên máy Windows đang sử dụng.
2. Bàn giao slide cho người chỉnh hình thức theo docs/PRESENTATION_HANDOFF.md.
3. Xem lại slide sau chỉnh hình thức, kiểm tra số liệu và thứ tự thao tác demo.
4. Nộp hồ sơ theo hình thức giảng viên yêu cầu. Nếu phiếu chấm cần họ tên, chữ ký hay công việc từng người, ghi đúng người và phần việc thực tế.

Các việc này là kế hoạch tiếp theo, không ghi là đã hoàn thành.
