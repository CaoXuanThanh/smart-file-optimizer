# Hướng dẫn tập thuyết trình Smart File Optimizer

Dùng với Smart_File_Optimizer_BAO_CAO.pptx, 18 slide. Mục tiêu tập: khoảng 10–12 phút, gồm demo 90 giây. Đây là thời lượng gợi ý để tập, không phải yêu cầu của giảng viên.

## Cách tập

Lượt 1: đọc lời dẫn và thao tác demo để hiểu mạch bài. Lượt 2: chỉ nhìn tiêu đề slide và nói lại bằng lời của mình. Lượt 3: bấm giờ, tập cả phần chuyển sang ứng dụng rồi quay lại PowerPoint.

Dành nhiều thời gian nhất cho slide 6–8 và 12–14. Slide 1–3, 15 và 17 nói ngắn. Khi trình bày bảng, chỉ vào số liệu đang so sánh và nêu nhận xét, không đọc lần lượt mọi ô.

## Lời dẫn từng slide

### Slide 1. Mở đầu

Kính chào thầy cô và các bạn. Em xin trình bày đồ án học phần Cấu trúc dữ liệu và Giải thuật.

### Slide 2. Tên đề tài

Đề tài tập trung tìm các file lớn nhất trong thư mục bằng Min-Heap. Chương trình bổ sung nén Huffman để minh họa ứng dụng của cây nhị phân và hàng đợi ưu tiên.

### Slide 3. Bố cục

Bài trình bày đi từ yêu cầu đến cách xử lý bằng cấu trúc dữ liệu. Sau đó em giới thiệu chương trình và dùng kết quả đo để đánh giá lựa chọn thuật toán.

### Slide 4. Bài toán

Ví dụ, với một thư mục tải xuống có rất nhiều file, người dùng chỉ cần xem 10 file lớn nhất. Chương trình duyệt cả thư mục con và trả về kích thước cùng đường dẫn để xác định đúng file.

### Slide 5. Chức năng

Chức năng chính của đề tài là chọn Top-K theo kích thước. Huffman là phần mở rộng xử lý một file do người dùng chọn. Chương trình không tự xóa hoặc tự nén các file trong kết quả quét.

### Slide 6. Min-Heap

Gốc của Min-Heap là phần tử nhỏ nhất trong K ứng viên đang giữ. Nhờ vậy, mỗi file mới chỉ cần so sánh với gốc để quyết định có thay thế hay không. Sau mỗi bước, heap giữ K phần tử lớn nhất đã duyệt. Sắp xếp kết quả cuối tốn thêm O(K log K). O(K) chỉ nói về phần chọn, không bao gồm danh sách thư mục hoặc dữ liệu giao diện.

### Slide 7. Ví dụ Top-K

Khi gặp file 35 MB, chương trình thay file 20 MB vì đây là ứng viên nhỏ nhất. File 10 MB không thể lọt Top-3 nên được bỏ qua. Các giá trị trong bảng được viết theo thứ tự tăng để dễ theo dõi, không phải cách lưu nội bộ của mảng heap.

### Slide 8. Huffman

Cây Huffman được dựng bằng cách liên tục ghép hai nút có tần suất nhỏ nhất. Mã thu được có tính chất tiền tố nên giải mã không cần dấu phân cách. Bản cài đặt xử lý dữ liệu theo khối 64 KiB, quét nguồn hai lượt khi nén. HUF2 lưu thêm SHA-256 để phát hiện dữ liệu khôi phục sai.

### Slide 9. Cài đặt

Cả app.py và cli.py đều gọi chung phần xử lý trong src/smartfile, nên không phải viết hai bộ thuật toán. Giao diện tại 127.0.0.1 chạy ngay trên máy người dùng. Trình duyệt hiển thị kết quả, còn Python thực hiện việc đọc và xử lý file.

### Slide 10. Bảo vệ dữ liệu

Chương trình giữ nguyên file nguồn và yêu cầu một đường dẫn đích chưa tồn tại, kể cả liên kết tượng trưng hỏng. Nếu giải nén gặp dữ liệu không hợp lệ, chương trình báo lỗi và dọn file đầu ra đang tạo. Trường hợp tiến trình bị dừng cưỡng bức vẫn cần cải thiện bằng cơ chế ghi file nguyên tử.

### Slide 11. Kiểm thử

Em kiểm tra Top-K bằng cách đối chiếu với kết quả sắp xếp toàn bộ. Với Huffman, em kiểm tra dữ liệu sau giải nén có trùng nguồn hay không. Ngoài dữ liệu bình thường còn có thư mục rỗng, K không hợp lệ và file nén hỏng. Bộ kiểm thử có 28 ca. Hai workflow kiểm thử và đóng gói Windows đã thành công.

### Slide 12. 50.000 bản ghi

Dữ liệu được sinh có kiểm soát và kết quả Top-K được đối chiếu với sort. Thời gian và bộ nhớ được đo riêng để tránh ảnh hưởng của công cụ đo bộ nhớ lên thời gian. Bộ nhớ trong bảng là cấp phát Python đo bằng tracemalloc, không phải tổng RAM của tiến trình.

### Slide 13. 10.000 file thật

Khi quét thư mục thật, chi phí đọc thông tin file chiếm phần lớn thời gian, vì vậy lợi thế tốc độ của heap không còn rõ. Bộ nhớ vẫn thấp hơn phương án gom toàn bộ danh sách để sắp xếp. Kết quả này không chứng minh heap luôn nhanh hơn trong mọi điều kiện.

### Slide 14. Demo nén

Khi demo, em nén notes.txt sang một tên .huf mới, giải nén sang tên .txt mới rồi chạy verify để đối chiếu. Tỷ lệ giảm tính bằng (1 − 304762/576000) × 100. Kết quả match: true xác nhận hash trùng nhau. Đây là mẫu văn bản lặp nên nén tốt, không phải tỷ lệ chung cho mọi loại file.

### Slide 15. Bản Windows

Ứng dụng có bản đóng gói Windows kèm thư viện cần thiết. Người dùng giải nén toàn bộ gói, mở file EXE và sử dụng giao diện trong trình duyệt. Dữ liệu được xử lý trên máy đang chạy ứng dụng.

### Slide 16. Kết luận

Điểm chính của đề tài là áp dụng cấu trúc dữ liệu để giảm lượng thông tin phải lưu khi chỉ cần một phần kết quả. Với Huffman, hiệu quả nén phụ thuộc phân bố tần suất byte. Hướng phát triển ưu tiên là trải nghiệm thao tác file lớn và độ an toàn khi tác vụ bị gián đoạn.

### Slide 17. Tham khảo

Tài liệu kỹ thuật và mã nguồn được liệt kê tại đây để tra cứu. Toàn bộ số liệu thực nghiệm có trong thư mục benchmarks của dự án.

### Slide 18. Cảm ơn

Em xin kết thúc phần trình bày. Em cảm ơn thầy cô và các bạn đã lắng nghe.

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
