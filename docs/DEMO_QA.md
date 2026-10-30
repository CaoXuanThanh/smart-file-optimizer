# Demo 90 giây và phản biện

## Chuẩn bị

Chạy `python scripts/make_demo.py`. Chạy `python -m streamlit run app.py --server.address 127.0.0.1`. Nhập đường dẫn demo_data (script in ra đường dẫn tuyệt đối). Chọn K=3. Trước khi tạo file nén, thư mục có 5 file, Top-3 là notes.txt 576.000 B, binary.bin 262.144 B và random.bin 131.072 B.

1. 0–25 giây: Scan folder, chỉ vào bảng Top-K và tải CSV.
2. 25–55 giây: Huffman Lab, chọn notes.txt, đích notes.huf chưa tồn tại. Kết quả lần chạy ở đây là 304.762 B, tiết kiệm 47,09%.
3. 55–80 giây: Giải nén notes.huf sang restored.txt mới. HUF2 kiểm tra checksum trước báo thành công.
4. 80–90 giây: `python cli.py verify demo_data/notes.txt demo_data/restored.txt`, giải thích `match: true`.

Nếu đích đã tồn tại, đổi tên đích mới. Không xóa file nguồn để diễn demo. Quét sau khi nén/giải nén sẽ thấy thêm file, nên Top-K có thể khác bảng chuẩn.

## Khi demo có lỗi

- Sai thư mục: sao chép đường dẫn đầy đủ từ File Explorer.
- Đích tồn tại: đổi tên mới, ứng dụng cố ý chặn overwrite.
- Thư viện thiếu: dùng đúng `.venv\Scripts\python -m pip install -r requirements.txt`.
- UI không mở: chuyển CLI, dùng chính bộ lệnh trong README.
- File không giảm kích thước: dùng notes.txt mẫu để minh họa dữ liệu lặp; nêu rõ dữ liệu ngẫu nhiên có thể tăng.
- Máy trình bày lỗi chưa rõ: gửi nguyên thông báo terminal và kết quả test, không chỉ ảnh cửa sổ trống.

## Phản biện ngắn

**Vì sao Min-Heap?** Cần loại nhanh file nhỏ nhất trong K ứng viên lớn nhất, nên giữ nó ở gốc.

**Heap có sắp toàn bộ dữ liệu?** Không, chỉ đảm bảo cha không lớn hơn con. Sort K kết quả cuối để hiển thị.

**Chứng minh Top-K đúng?** Bất biến: sau mỗi file, giữ min(K, số đã duyệt) ứng viên lớn nhất. File mới không hơn gốc thì không lọt nhóm; nếu hơn thì thay phần tử nhỏ nhất. Khởi tạo rỗng và quy nạp qua N file.

**K>N hay bằng kích thước?** Trả tất cả N file; tie-break theo đường dẫn giảm dần để kết quả xác định.

**Heap khác BST?** Heap ưu tiên gốc nhỏ nhất và quan hệ cha-con; BST dùng thứ tự trái/phải để tìm kiếm theo khóa.

**O(K) có phải RAM cả app?** Không. Chỉ khâu lựa chọn; os.walk còn danh sách tên, lỗi có O(E), dashboard có bảng và thư viện riêng.

**Benchmark 50.000 là file thật?** Không, đó là record tái lập. Có phép đo riêng 10.000 file thật, kèm dữ liệu gốc và hai phương án cùng scanner.

**Heap luôn nhanh hơn?** Không. Khi chi phí I/O chiếm phần lớn, chênh lệch thời gian rất nhỏ. Điểm mạnh ở đây là bộ nhớ khi K nhỏ so với N.

**Huffman có mất dữ liệu?** Giải mã theo cùng cây mã tiền tố khôi phục byte. Các fixture đã kiểm tra hash trùng. HUF2 tự kiểm tra SHA-256. HUF1 không có checksum.

**Hash có chống giả mạo?** Không. Người sửa được cả dữ liệu và hash có thể tạo archive hợp lệ. Đây không phải chữ ký hay mã hóa.

**Vì sao file có thể lớn hơn?** Header và phân bố byte ít lệch. File rỗng HUF2 cũng tốn 46 B.

**Streaming có cần đọc hai lần?** Có. Lượt đầu đếm tần suất để biết bảng mã, lượt hai mã hóa theo khối. Hash hai lượt giúp phát hiện nguồn thay đổi.

**Đã production-ready?** Chưa. Chưa fuzzing toàn diện, chưa kiểm tra file nhiều GiB hay sự cố mất điện, chưa chạy máy Windows trình bày. Gói này là sản phẩm đồ án có kiểm chứng và giới hạn rõ ràng.
