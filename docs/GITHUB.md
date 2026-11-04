# Cập nhật repo và viết commit

Repo hiện tại: https://github.com/CaoXuanThanh/smart-file-optimizer. Không tạo lại repo hoặc chạy git init trong thư mục ZIP giải nén để nối lịch sử cũ.

## Cách dùng Git Bash

Nếu thư mục clone hiện tại sạch, chạy `git status`, rồi `git pull --ff-only` trước khi chép tài liệu mới. Nếu có thay đổi chưa commit, giữ lại và xem diff trước, không dùng reset để xóa.

Nếu khó phân biệt thư mục ZIP với repo đã clone, có thể clone vào một thư mục mới có tên chưa tồn tại:

```bash
git clone https://github.com/CaoXuanThanh/smart-file-optimizer.git smart-file-optimizer-final
cd smart-file-optimizer-final
```

Sau đó chép **nội dung bên trong** thư mục smart-file-optimizer của gói mới vào thư mục repo vừa clone. Giữ nguyên thư mục .git do clone tạo ra. Gói ZIP bàn giao không chứa .git.

Trong Git Bash tại repo, kiểm tra và commit phần tài liệu:

```bash
git status --short
git diff --stat
git add README.md README.en.md docs/ .gitignore
git diff --cached --stat
git commit -m "docs: add algorithm diagrams and grading evidence"
git push origin main
```

Xem danh sách staged trước khi commit. Bộ cập nhật này chỉ đổi tài liệu và cấu hình bỏ qua file trình chiếu. Nếu thấy mã Python thay đổi ngoài dự kiến thì xem diff trước khi tiếp tục. Nếu push bị từ chối do remote có commit mới, dừng để đồng bộ lịch sử; không dùng force push.

## Commit thế nào là rõ ràng?

Một câu nêu việc thay đổi là đủ. `docs:` là quy ước tùy chọn giúp nhận biết thay đổi tài liệu, không phải điều kiện Git bắt buộc.

- Lần này: `docs: add algorithm diagrams and grading evidence`
- Chỉnh hình thức slide: `docs: refine presentation layout and transitions`
- Sửa lỗi khởi động: `fix: disable Streamlit development mode in portable launcher`

Có thể viết tiếng Việt, ví dụ: `docs: bổ sung lưu đồ và minh chứng kiểm thử`. Công cụ gợi ý commit chỉ hỗ trợ diễn đạt; kiểm tra câu đó mô tả đúng các file staged rồi mới dùng. Cùng câu commit trên có thể dán vào ô Summary của GitHub Desktop.

## Nếu dùng GitHub web

Chọn Add file → Upload files. Kéo thả file hoặc thư mục có nội dung. GitHub hỗ trợ tải thư mục bằng kéo thả, giới hạn tối đa 100 file mỗi lượt và 25 MiB mỗi file qua trình duyệt.

Để cập nhật repo hiện có, kéo các file và thư mục con ở **bên trong** gói dự án vào gốc repo. Không kéo thêm thư mục cha smart-file-optimizer để tránh tạo một dự án lồng bên trong repo. Kiểm tra đường dẫn hiển thị trước khi commit.

Git không theo dõi thư mục rỗng. Không tải .git, .venv, __pycache__, build hoặc dist lên repo. Upload ZIP/RAR chỉ lưu một file nén, không tự giải nén thành mã nguồn và workflow.

Nếu đã commit qua web, lần tới làm trên clone cục bộ hãy đồng bộ bằng git pull --ff-only khi working tree sạch. Dùng một luồng thao tác nhất quán sẽ dễ theo dõi hơn.

Nguồn: [GitHub Docs: Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), đối chiếu 04/11/2026.

## Tạo commit bằng Copilot trong GitHub Desktop

1. Chọn đúng repo, Fetch origin và Pull origin nếu có cập nhật khi thư mục làm việc sạch.
2. Chép các file mới vào repo. Vào Changes, chọn những thay đổi muốn đưa vào commit.
3. Bấm biểu tượng Copilot cạnh ô Summary, có nhãn Generate commit message with Copilot. Tính năng cần tài khoản có quyền dùng Copilot.
4. Đọc lại Summary và Description, chỉnh nếu cần. Bấm Commit to main, rồi Push origin (nếu nhánh cho phép push trực tiếp).

Copilot dựa trên các thay đổi đã chọn để viết nội dung commit. Không cần tải file lên web trước. Nếu không thấy nút, kiểm tra phiên bản GitHub Desktop và quyền Copilot của tài khoản.

PowerPoint bàn giao riêng và không đưa lên repo. File .gitignore bỏ qua *.ppt và *.pptx; quy tắc này chỉ áp dụng cho file chưa được Git theo dõi.

Nguồn: https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop
