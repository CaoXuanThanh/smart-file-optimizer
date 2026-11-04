## Demo 90 giây trên máy Windows hiện tại

Chuẩn bị trước buổi báo cáo: mở PowerShell tại thư mục có app.py, cli.py và scripts. Các lệnh dưới đây dùng Python trong .venv của dự án đang chạy được. Nếu dùng bản EXE, mở EXE để chạy giao diện; lệnh verify vẫn dùng bản mã nguồn đã cài Python trên máy của bạn.

```powershell
.\.venv\Scripts\python.exe scripts/make_demo.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Giữ cửa sổ này mở. Sao chép đường dẫn demo_data mà lệnh đầu in ra. Mở PowerShell thứ hai tại cùng thư mục để sẵn lệnh verify.

1. Chọn TOP-K EXPLORER, nhập đường dẫn demo_data và K = 3. Bấm Scan folder. Nói: “Chương trình duyệt thư mục và giữ ba file lớn nhất bằng Min-Heap.”
2. Chọn HUFFMAN LAB. Nén demo_data/notes.txt sang demo_data/notes_baocao.huf. Nói: “Mẫu văn bản này có nhiều ký hiệu lặp nên Huffman giảm dung lượng khoảng 47%.”
3. Giải nén demo_data/notes_baocao.huf sang demo_data/restored_baocao.txt.
4. Trong PowerShell thứ hai, chạy:

```powershell
.\.venv\Scripts\python.exe cli.py verify demo_data/notes.txt demo_data/restored_baocao.txt
```

Chỉ vào `"match": true` và nói: “Mã SHA-256 của dữ liệu khôi phục trùng với nguồn.” Quay lại PowerPoint để kết luận.

Hai tên file đầu ra phải chưa tồn tại. Khi tập lại, dùng tên mới cho cả file nén và file khôi phục, đồng thời sửa lệnh verify cho khớp. Nếu demo_data đã có file tạo từ lần trước, kết quả Top-K có thể thay đổi. Không khẳng định thư mục luôn có đúng năm file.

Nếu giao diện gặp lỗi, dùng CLI dự phòng với tên đích mới:

```powershell
.\.venv\Scripts\python.exe cli.py scan demo_data -k 3
.\.venv\Scripts\python.exe cli.py compress demo_data/notes.txt demo_data/notes_duphong.huf
.\.venv\Scripts\python.exe cli.py decompress demo_data/notes_duphong.huf demo_data/restored_duphong.txt
.\.venv\Scripts\python.exe cli.py verify demo_data/notes.txt demo_data/restored_duphong.txt
```

## Các câu cần trả lời được

**Vì sao dùng Min-Heap?** Gốc là file nhỏ nhất trong K ứng viên. Khi gặp file lớn hơn, ta thay ngay ứng viên nhỏ nhất đó.

**Vì sao không dùng Max-Heap?** Với cách giữ K ứng viên, ta cần truy cập nhanh phần tử nhỏ nhất để loại. Max-Heap đặt phần tử lớn nhất ở gốc nên không phù hợp bằng Min-Heap cho thao tác này.

**Top-K đúng như thế nào?** Sau mỗi file, heap giữ tối đa K file lớn nhất đã gặp. File mới không hơn gốc thì không cần giữ. Nếu lớn hơn gốc, thay ứng viên nhỏ nhất. Lặp đến cuối thì thu được Top-K.

**Heap có sắp xếp toàn bộ không?** Heap chỉ bảo đảm quan hệ cha không lớn hơn con. Chương trình sắp xếp K kết quả cuối để hiển thị giảm dần.

**Độ phức tạp?** Khâu chọn tốn O(N log K), rồi sắp xếp kết quả O(K log K). Heap lưu O(K) phần tử. Đây không phải tổng RAM của cả ứng dụng.

**K lớn hơn số file? K không hợp lệ?** Nếu K > N thì trả N file. K phải là số nguyên dương. Các file bằng kích thước có thứ tự phụ theo đường dẫn để kết quả nhất quán.

**Có tự cài heap không?** Chương trình dùng heapq của Python cho thao tác heap. Phần lựa chọn Top-K, duyệt file và xử lý kết quả do chương trình tổ chức. Không trình bày rằng đã tự viết mọi phép heap nếu mã dùng thư viện.

**Tại sao Huffman giải nén được?** Mã có tính tiền tố. Bộ giải nén dựng lại cùng cây từ thông tin lưu trong file, rồi đọc bit theo cây để khôi phục byte.

**Nén có phải mã hóa bảo mật không?** Huffman biểu diễn dữ liệu bằng mã bit để nén. Nó không cung cấp mật khẩu hay giữ bí mật nội dung.

**File nén có luôn nhỏ hơn không?** Không. Thông tin mô tả cây và phân bố byte có thể khiến file nén lớn hơn nguồn, nhất là dữ liệu khó nén hoặc file rất nhỏ.

**50.000 phần tử là file thật?** Đó là bản ghi tổng hợp để đánh giá khâu chọn Top-K. Phép đo riêng trên thư mục có 10.000 file thật đánh giá thêm chi phí duyệt và đọc thông tin file.

**Vì sao quét file thật không nhanh hơn sort?** Thời gian truy cập file chiếm tỷ trọng lớn, nên hai kết quả gần nhau. Lợi thế rõ hơn trong phép đo này là bộ nhớ.

**Bộ nhớ trong bảng là gì?** Là bộ nhớ cấp phát Python đo bằng tracemalloc, không phải toàn bộ RAM tiến trình. Thời gian và bộ nhớ được đo riêng, lấy trung vị năm lần.

**SHA-256 chứng minh gì?** Hash trùng là bằng chứng mạnh rằng dữ liệu khôi phục trùng nguồn trong lần kiểm tra. Hash không phải chữ ký xác thực và không giúp giữ bí mật dữ liệu.

**Tại sao có giao diện trình duyệt mà vẫn chạy cục bộ?** Python chạy máy chủ trên chính máy của em. Trình duyệt truy cập 127.0.0.1 để hiển thị giao diện.

**GitHub Actions dùng để làm gì?** Tự chạy các lệnh kiểm thử và đóng gói trên môi trường đã cấu hình mỗi khi cập nhật mã nguồn. Đây là phần hỗ trợ kiểm tra và bàn giao sản phẩm.

## Các điểm cần nói chính xác

Không nói heap luôn nhanh hơn sort. Không gọi 50.000 bản ghi là 50.000 file thật. Không nói Huffman luôn giảm dung lượng. Không gọi SHA-256 là mã hóa bảo mật. Không suy từ CI xanh rằng phần mềm đã hết lỗi.

Khi thầy hỏi sâu ngoài phạm vi đã thử, nói rõ: “Trường hợp này em chưa đo trực tiếp. Kết quả hiện tại của em áp dụng cho bộ dữ liệu đã trình bày.”
