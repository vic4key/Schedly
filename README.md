# Schedly

Schedly là web app ứng dụng AI giúp bạn lập lịch công việc nhanh chóng, đơn giản, dễ sử dụng, và thân thiện với người dùng.

## Chức năng chính
- Nhập dữ liệu lập lịch qua giao diện web responsive hiện đại (Bootstrap, Flatpickr)
- Tự động tạo sách công việc từ mô tả tự nhiên
- Xử lý và tạo lịch trình tự động, xét các khoảng nghỉ, ngày nghỉ lễ, etc
- Xem trực tiếp kết quả trên web hoặc tải xuống file CSV

## Tính năng nổi bật & Cách sử dụng
- **Nhập mô tả công việc (AI-powered):** Nhập đoạn văn tự nhiên, nhấn "Tạo danh sách công việc" để AI sinh ra danh sách chuẩn hóa.
- **Accordion hiện đại:** Các phần nhập công việc, thời gian nghỉ được tổ chức dạng accordion, gọn gàng.
- **Thời gian nghỉ:** Thêm/xóa khoảng nghỉ, thêm ngày nghỉ lễ phổ biến chỉ với 1 click.
- **Tự động lưu trạng thái:** Dữ liệu nhập được lưu tự động, không lo mất khi reload trang.
- **Kết quả CSV:** Xem trực tiếp dưới dạng bảng, hoặc tải file về.

## Cài đặt
1. Python 3.
2. Cài thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. (Tùy chọn, nếu dùng AI) Cập nhật file `.env` với AI provider mà bạn có.
4. Chạy ứng dụng:
   ```bash
   python app.py
   ```
5. Mở trình duyệt và truy cập: http://localhost:5000

## Credit
Vic P. with Vibe Coding ❤️