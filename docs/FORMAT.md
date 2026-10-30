# Định dạng .huf

Các số nguyên dùng big-endian, byte không dấu.

| Trường | Số byte |
|---|---:|
| Magic HUF2 (HUF1 khi đọc file cũ) | 4 |
| Kích thước gốc | 8 |
| Số ký hiệu 0..256 | 2 |
| Mỗi ký hiệu: byte + tần suất | 9 |
| SHA-256 dữ liệu gốc, chỉ HUF2 | 32 |
| Payload bit, MSB trước, padding 0 | biến đổi |

Dựng heap theo (tần suất, số thứ tự, nút). Chèn lá theo byte tăng dần. Mỗi lần ghép lấy trái trước, phải sau. Một ký hiệu dùng mã 0 dài một bit. File rỗng HUF2 dài 46 byte.

Giải mã kiểm tra tổng tần suất, số ký hiệu, kích thước payload chính xác, padding, số byte, tần suất khôi phục và SHA-256 nếu có. HUF1 không có checksum nên không đảm bảo phát hiện mọi thay đổi. SHA-256 phát hiện lỗi ngẫu nhiên, không cung cấp xác thực hay mã hóa mật khẩu.

Giới hạn giải nén mặc định 1 GiB. CLI có --max-output-mib. Chương trình không tự đọc tên hay đường dẫn từ archive. Nguồn cần là file ổn định trong suốt thao tác. Nén đọc hai lượt từ cùng file và kiểm tra hash hai lượt.

Tạo đích bằng chế độ xb: từ chối file có sẵn kể cả symlink. File đích hiện hữu trong quá trình xử lý và chưa có giá trị cho tới khi hàm thành công. Ngoại lệ có xử lý sẽ dọn file đang tạo, nhưng mất điện/kill cưỡng bức có thể để lại file dở. Chưa hardening cho thư mục bị tiến trình thù địch sửa đồng thời.
