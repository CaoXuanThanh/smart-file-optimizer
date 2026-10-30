# Đưa lên GitHub

Bản giao có cấu trúc repo, .gitignore, MIT, README song ngữ, test và workflow. Chưa tạo remote hoặc push vì chưa có URL/tài khoản repo được chọn.

1. Tạo repository trống trên GitHub, không khởi tạo README.
2. Mở terminal trong thư mục SmartFileOptimizer, chạy:

```shell
git init
git add .
git commit -m "Complete Python Top-K and streaming Huffman v0.2.0"
git branch -M main
git remote add origin URL_REPOSITORY_CUA_BAN
git push -u origin main
```

3. Chờ Actions chạy trên Windows và Linux. Chỉ tạo tag/release sau khi kiểm tra pass:

```shell
git tag v0.2.0
git push origin v0.2.0
```

Dán nội dung CHANGELOG vào release. Không upload demo_data, file cá nhân, tài liệu đề gốc hay .venv. MIT là lựa chọn cho mã nguồn đồ án trong bản giao này; giữ thông báo bản quyền và tuân thủ quy định nộp bài của môn học.
