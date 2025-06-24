import os
import requests

# Ví dụ: sử dụng OpenAI GPT (có thể thay thế bằng provider khác)
# Hàm này mô phỏng, bạn cần điền API key và endpoint thực tế nếu dùng thật

def request_holidays_llm(prompt: str, year: int) -> list:
    """
    Gửi prompt tới LLM provider để lấy danh sách ngày nghỉ lễ cho năm tương ứng.
    Trả về list dict: [{"name": ..., "date": ...}, ...]
    """
    # Ví dụ prompt: "Liệt kê các ngày nghỉ lễ lớn của Việt Nam năm 2025, trả về dạng JSON [{name, date}] với date dạng YYYY/MM/DD"
    # Dưới đây là mô phỏng, bạn có thể thay bằng call thực tế tới OpenAI hoặc provider khác
    # Nếu dùng OpenAI:
    # response = openai.ChatCompletion.create(...)
    # holidays = ...
    # return holidays
    
    # MOCK: trả về mẫu
    return [
        {"name": "Tết Dương lịch", "date": f"{year}/01/01"},
        {"name": "Giỗ tổ Hùng Vương", "date": f"{year}/04/18"},
        {"name": "30/4", "date": f"{year}/04/30"},
        {"name": "1/5", "date": f"{year}/05/01"},
        {"name": "2/9", "date": f"{year}/09/02"},
        {"name": "Tết Nguyên Đán", "date": f"{year}/01/28"},
        {"name": "Tết Nguyên Đán", "date": f"{year}/01/29"},
        {"name": "Tết Nguyên Đán", "date": f"{year}/01/30"},
        {"name": "Tết Nguyên Đán", "date": f"{year}/01/31"},
        {"name": "Tết Nguyên Đán", "date": f"{year}/02/01"},
    ] 