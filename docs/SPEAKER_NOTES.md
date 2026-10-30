# Lời thuyết trình 8–10 phút

## 1. SMART FILE OPTIMIZER

Mở đầu, 25 giây. Đề tài 18 giữ trọng tâm tìm K file lớn nhất bằng Min-Heap. Huffman là tính năng mở rộng. Sản phẩm phát triển tiếp từ bản Python bàn giao, có dashboard và CLI.

## 2. Bài toán và phạm vi

40 giây. Đầu vào là thư mục và K. Đầu ra là tối đa K file có kích thước lớn nhất, kèm đường dẫn. Chỉ giữ K ứng viên khi duyệt. Không xóa file. Huffman cho phép thử nén và khôi phục sang file mới. Đề cũ ghi C# nhưng phạm vi đã chốt là Python.

## 3. Min-Heap giữ đúng K ứng viên

65 giây. Gốc là phần tử nhỏ nhất trong tập đang giữ, nên là ứng viên cần loại khi gặp file lớn hơn. Sau mỗi file, heap chứa min(K, số file đã duyệt) phần tử lớn nhất. Khi heap đủ, file không hơn gốc không thể vào Top-K; file hơn gốc thay đúng phần tử yếu nhất. Cuối cùng chỉ sort K phần tử. Tie-break dùng đường dẫn giảm dần. Bộ nhớ O(K) chỉ tính khâu chọn, không tính os.walk và lỗi.

## 4. Kiến trúc giữ nguyên nền Python

40 giây. Hai giao diện dùng cùng các module. Phần chọn heap đã tách thành select_top_k để benchmark đo đúng hàm dùng trong app. Huffman giữ cách dựng cây và bảng mã xác định từ bản cũ, cải tiến cách đọc và ghi. Không xây lại toàn bộ từ đầu.

## 5. Thiết kế thực nghiệm

40 giây. Tách benchmark chọn record khỏi benchmark file thật để không nhầm chi phí thuật toán với I/O. Hai phương án nhận dữ liệu cùng seed, cùng quy tắc so sánh. Đo thời gian không bật tracemalloc và đo peak ở lượt riêng. Dùng trung vị 5 lần, warmup trước mỗi cấu hình. Mọi kết quả đều đối chiếu sort.

## 6. 50.000 record: chênh lệch bộ nhớ rõ rệt

55 giây. Nguồn: benchmarks/raw.csv, summary.json, environment.json. K=10. Trung vị của 5 lần. Heap khoảng 5,47 KiB, sort khoảng 8.539,90 KiB. Thời gian 32,09 ms so với 56,71 ms trong môi trường Linux Python 3.12 này. Khâu sinh record nằm trong phép đo, không có quét đĩa. Không suy rộng rằng heap luôn nhanh hơn. Cột heap rất nhỏ vì thang đo tuyến tính.

## 7. 10.000 file thật: I/O làm giảm khác biệt tốc độ

50 giây. Nguồn: benchmarks/disk_and_codec.json. Cùng scan_files cho heap và sort. Fixture tạo trước phép đo, có cache hệ thống. Quét thực tế đủ 10.000 file, oracle khớp. Peak heap 422,70 KiB so với sort 1.840,34 KiB. Runtime gần bằng nhau, không có bằng chứng heap nhanh hơn trên thư mục này. Bộ nhớ quét cao hơn benchmark record do os.walk và đường dẫn.

## 8. Huffman: xử lý theo khối, kiểm tra toàn vẹn

50 giây. Giữ thuật toán cây Huffman từ prototype. Lượt một đọc từng khối để đếm tần suất và hash. Lượt hai ghi bit với bảng mã. HUF2 lưu hash gốc, giải nén kiểm tra hash trước khi báo thành công. HUF1 vẫn đọc được nhưng không thể đảm bảo checksum. Chỉ tạo đích mới bằng xb. Ngoại lệ dọn đích dở, kill cưỡng bức vẫn có thể để lại file dở.

## 9. Nén hiệu quả phụ thuộc dữ liệu

45 giây. Nguồn benchmarks/disk_and_codec.json. Tất cả là fixture tự sinh, không đại diện mọi tài liệu. Văn bản lặp giảm 47,04%. Phân bố byte đều và ngẫu nhiên tăng 0,45% vì header. File rỗng chiếm 46 byte và không có tỷ lệ tiết kiệm có nghĩa. Cả bốn trường hợp đều khôi phục đúng hash.

## 10. Kiểm thử và trạng thái thật

45 giây. Nguồn docs/test_results.txt, tests/test_extended.py, tests/test_ui.py. 28 test đạt Linux Python 3.12, không skip ở lần chạy này. Hai test giao diện dùng AppTest, chưa là thử trên Windows thật. Lỗi quyền được mock có chủ đích vì môi trường quyền cao. CI đã cấu hình, chưa được chạy trên GitHub.

## 11. Demo trực tiếp trong 90 giây

90 giây, có thể chuyển sang app. Chạy scripts/make_demo.py một lần để có 5 file. Quét demo_data K=3 trước khi nén. Kết quả đầu tiên notes.txt 576000 byte, binary.bin 262144 byte, random.bin 131072 byte. Nén notes.txt sang notes.huf chưa tồn tại rồi giải nén sang restored.txt mới. CLI verify xác nhận match true. Nếu đã chạy demo, đổi tên đích, không xóa nguồn. Kết quả bảng này lấy từ lần chạy CLI thực tế, không phải screenshot giả.

## 12. Kết luận và giới hạn

35 giây. Đã giữ nền Python và hoàn thiện chức năng, test, benchmark có dữ liệu gốc và tài liệu chạy demo. Min-Heap có lợi rõ về bộ nhớ khi K nhỏ. Huffman minh họa nén lossless nhưng không bảo đảm tiết kiệm. Chưa production-ready: chưa kiểm thử file nhiều GiB, thư mục thù địch, mất điện hay Windows máy trình bày. Cảm ơn và chuyển hỏi đáp.