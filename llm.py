import os, re
from datetime import date, timedelta
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if http_proxy := os.environ.get("HTTP_PROXY"):
    os.environ["http_proxy"] = http_proxy
if https_proxy := os.environ.get("HTTPS_PROXY"):
    os.environ["https_proxy"] = https_proxy
os.environ["no_proxy"] = "127.0.0.1,localhost,.local"

llm_api = {
    "provider": os.getenv("LLM_PROVIDER"),
    "url": os.getenv("LLM_API_URL"),
    "api_key": os.getenv("LLM_API_KEY"),
    "model": os.getenv("LLM_MODEL_NAME"),
}

llm_client = None

def llm_chat(user_prompt: str, system_prompt: str = "You are a helpful assistant") -> str:
    response = ""
    try:
        global llm_client
        if not llm_client:
            llm_client = OpenAI(
                base_url=llm_api["url"],
                api_key=llm_api["api_key"],
            )
            print(f"🤖 Using the LLM provider '{llm_api['provider']}' with the model '{llm_api['model']}' at '{llm_api['url']}'")

        if llm_model_suffix := os.getenv("LLM_MODEL_SUFFIX"):
            user_prompt += "\n"
            user_prompt += llm_model_suffix

        completion = llm_client.chat.completions.create(
            model=llm_api["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        response = completion.choices[0].message.content

        llm_model_no_think = False
        if temp := os.getenv("LLM_MODEL_NO_THINK"):
            if temp.lower() in ["1", "true"]:
                llm_model_no_think = True

        if llm_model_no_think:
            response = re.sub(r'<think>.*?</think>\n*', '', response, flags=re.DOTALL)
            response = response.strip()
    except Exception as e:
        print("❌ LLM Error:", str(e))
        response = ""
    return response

# Ví dụ: sử dụng OpenAI GPT (có thể thay thế bằng provider khác)
# Hàm này mô phỏng, bạn cần điền API key và endpoint thực tế nếu dùng thật

def llm_get_holidays(year: int) -> list:
    """
    Get a list of popular public holidays in Vietnam for a given year.
    Only holidays with a valid date and occurring today or later are included.

    Args:
        year (int): The year for which to retrieve the list of holidays.

    Returns:
        list: A list of popular public holidays in Vietnam.
        Each containing 'name' (holiday name) and 'date' (string in yyyy/mm/dd format).
    """
    def parse_date_flexible(d):
        try:
            # Hỗ trợ cả yyyy/m/d, yyyy/mm/dd, yyyy-m-d, yyyy-mm-dd
            parts = d.replace('-', '/').split('/')
            if len(parts) != 3:
                return None
            y, m, day = map(int, parts)
            return date(y, m, day)
        except Exception: return None

    holidays = [
        {"name": "Tết Dương lịch", "date": "2025/01/01"},  # 🎉 Được nghỉ
        {"name": "Tết Nguyên Đán", "date": "2025/01/27"},  # 🎉 Được nghỉ (bắt đầu kỳ nghỉ Tết Âm lịch)
        {"name": "Giỗ tổ Hùng Vương", "date": "2025/04/07"},  # 🎉 Được nghỉ
        {"name": "Ngày Giải phóng miền Nam", "date": "2025/04/30"},  # 🎉 Được nghỉ
        {"name": "Ngày Quốc tế Lao động", "date": "2025/05/01"},  # 🎉 Được nghỉ
        {"name": "Ngày nghỉ hoán đổi (nghỉ)", "date": "2025/05/02"},  # 🎉 Được nghỉ (thay cho làm bù 26/04)
        {"name": "Ngày nghỉ hoán đổi (làm bù)", "date": "2025/04/26"},  # ❌ Đi làm bù
        {"name": "Ngày Quốc khánh", "date": "2025/09/02"},  # 🎉 Được nghỉ
        {"name": "Ngày Quốc khánh (nghỉ thêm)", "date": "2025/09/01"},  # 🎉 Được nghỉ
        # {"name": "Ngày Thầy thuốc Việt Nam", "date": "2025/02/27"},  # ❌ Không nghỉ
        # {"name": "Ngày Quốc tế Phụ nữ", "date": "2025/03/08"},  # ❌ Không nghỉ
        # {"name": "Ngày Quốc tế Thiếu nhi", "date": "2025/06/01"},  # ❌ Không nghỉ
        # {"name": "Ngày Nhà giáo Việt Nam", "date": "2025/11/20"},  # ❌ Không nghỉ
        # {"name": "Ngày thành lập Quân đội Nhân dân Việt Nam", "date": "2025/12/22"},  # ❌ Không nghỉ
    ]

    # Add all Saturdays and Sundays of the year as holidays (easier to read)
    weekends = []
    d = date(year, 1, 1)
    last = date(year, 12, 31)
    while d <= last:
        if d.weekday() == 5:
            weekends.append({"name": "Cuối tuần (T7)", "date": d.strftime("%Y/%m/%d")})
        elif d.weekday() == 6:
            weekends.append({"name": "Cuối tuần (CN)", "date": d.strftime("%Y/%m/%d")})
        d += timedelta(days=1)
    holidays.extend(weekends)

    # To filter and sort valid holidays, only include holidays from today onwards
    today = date.today()
    holidays = [h for h in holidays if parse_date_flexible(h['date'])]
    holidays.sort(key=lambda h: parse_date_flexible(h['date']))
    holidays = [h for h in holidays if parse_date_flexible(h['date']) >= today]

    return holidays

def llm_gen_task_list(text: str) -> List[str]:
    """
    Processes input text to generate a list of tasks with estimated hours in the specified format.

    Notes:
    - Maintains original language of task names
    - Formats output with commas and spaces between task name and hours
    - Extracts task names and hours from input text
    - Handles language-specific formatting (e.g., "hrs" for English)
    - Returns only task lines without additional metadata

    Args:
        text (str): The text that describe all tasks.

    Returns:
        List[str]: A list of strings, each representing a task in the format: "Name, X hrs"
    """
    instruction_prompt = """
Bạn sẽ nhận được một đoạn văn bản đầu vào từ người dùng liệt kê các task và thời gian ước tính thực hiện.
Hãy xử lý và chuẩn hóa văn bản thành định dạng yêu yêu cầu:

1. Giữ nguyên ngôn ngữ tên task:  
   - Sử dụng cùng ngôn ngữ cho tên các task như trong văn bản đầu vào (ví dụ, nếu đầu vào là tiếng Việt thì giữ tên task bằng tiếng Việt; nếu là tiếng Anh thì giữ bằng tiếng Anh).

2. Định dạng:  
   - Với mỗi task, xuất ra theo định dạng: Tên task, X hrs
   - Trong đó "Tên task" là tên của task như trong đầu vào, và "X" là số giờ ước tính để hoàn thành task)
   - Giữa tên task và số giờ phải có dấu phẩy và một khoảng trắng.
   - Nếu đầu vào không ghi rõ từ "giờ" hoặc từ tương đương, hãy thêm "hrs" (nếu tiếng Anh) hoặc từ viết tắt phù hợp theo ngôn ngữ đầu vào.
   - Phải đảm bảo thời gian của tất cả các task phải chuyển đổi sang đơn vị giờ (ví dụ các đơn vị như ngày, phút, etc phải chuyển đổi sang đơn vị giờ)

3. Mỗi task một dòng:  
   - Mỗi task phải được xuất trên một dòng riêng biệt.

4. Trích xuất và chuẩn hóa:  
   - Bỏ qua các thông tin hoặc cột thừa, trừ khi chúng là một phần của tên task hoặc số giờ ước tính.
   - Trích xuất tên task và số giờ ước tính từ mỗi dòng hoặc câu trong đầu vào.
   - Tên task phải ngắn gọn, đơn giản, không chứa thông tin bổ sung.

5. Chỉ trả về danh sách task, không thêm bất cứ thông tin hay tóm tắt nào khác trong phản hồi.

Dưới đây là ví dụ cho bạn tham khảo (chú ý: chỉ sử dụng ví dụ này để tham khảo, không xử lý ví dụ này):

Input:
tôi cần làm task 1 trong 2 giờ, task 2 trong 4 giờ, và task 3 trong 6 giờ

Output:
task 1, 2 hrs
task 2, 4 hrs
task 3, 6 hrs
"""
    user_prompt = f"{instruction_prompt}\n\nBây giờ, bạn hãy làm theo các hướng dẫn đã mô tả ở trên để xử lý cho đoạn văn bản dưới đây:\n\n```{text}```"
    response = llm_chat(user_prompt)
    return [line.strip() for line in response.split('\n') if line.strip()]
