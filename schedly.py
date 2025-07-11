# Đã đổi tên file này thành schedly_core.py để đồng bộ với tên project Schedly
from dateutil.parser import parse
from datetime import timedelta
from typing import List, Dict, Optional
import pandas as pd
import re

def parse_hours(estimate_time_str: str) -> float:
    """Chuyển chuỗi thời lượng (vd: '2 hrs', '1.5hr') thành số giờ float."""
    try:
        num = float(estimate_time_str.lower().replace('hrs', '').replace('hr', '').strip())
        if num < 0:
            raise ValueError("Estimated hours must be non-negative.")
        return num
    except Exception as e:
        raise ValueError(f"Không thể parse estimate_time: '{estimate_time_str}'. Lỗi: {e}")

def parse_datetime_range(range_str: str):
    """
    Nhận vào chuỗi 'YYYY/MM/DD HH:MM-YYYY/MM/DD HH:MM' hoặc
    'YYYY/MM/DD HH:MM đến YYYY/MM/DD HH:MM', trả về tuple 2 datetime.
    """
    # Chuẩn hóa dấu ngăn cách
    range_str = range_str.replace(" đến ", "-").replace("Đến", "-").replace("đến", "-")
    # Tìm 2 mốc thời gian
    parts = re.split(r"\s*-\s*", range_str)
    if len(parts) != 2:
        raise ValueError(f"Khoảng nghỉ không đúng định dạng: {range_str}")
    start = parse(parts[0].strip())
    end = parse(parts[1].strip())
    return (start, end)

def allocate_tasks_by_time_range(
    working_day_time_range: List[str],
    start_time: str,
    task_list: List[Dict],
    non_working_day_date_time_range: Optional[List[str]] = None
) -> List[Dict]:
    """
    Phân bổ các công việc vào các khoảng thời gian làm việc, xét đến các khoảng nghỉ (nếu có).
    Args:
        working_day_time_range (List[str]): VD ["08:00-12:00", "13:00-17:00"]
        start_time (str): VD "2025/06/03 13:00"
        task_list (List[Dict]): [{"name":..., "est":...}, ...]
        non_working_day_date_time_range (Optional[List[str]]): VD ["2025/06/03 15:00-2025/06/03 17:00"]
    Returns:
        List[Dict]: [{"name":..., "slots":..., "est":...}, ...]
    """
    # Parse non-working ranges
    non_working_ranges = []
    if non_working_day_date_time_range:
        for r in non_working_day_date_time_range:
            if r.strip():
                try:
                    non_working_ranges.append(parse_datetime_range(r))
                except Exception as ex:
                    raise ValueError(f"Lỗi ở khoảng nghỉ '{r}': {ex}")

    # Parse working hours trong ngày (hh:mm)
    working_hours = []
    for slot in working_day_time_range:
        start_str, end_str = slot.split('-')
        working_hours.append((start_str.strip(), end_str.strip()))

    def next_working_slot(current_dt):
        for start_str, end_str in working_hours:
            start = current_dt.replace(hour=int(start_str[:2]), minute=int(start_str[3:]), second=0, microsecond=0)
            end = current_dt.replace(hour=int(end_str[:2]), minute=int(end_str[3:]), second=0, microsecond=0)
            if current_dt < start:
                return start, end
            elif start <= current_dt < end:
                return current_dt, end
        # Sang hôm sau
        next_day = current_dt + timedelta(days=1)
        start = next_day.replace(hour=int(working_hours[0][0][:2]), minute=int(working_hours[0][0][3:]), second=0, microsecond=0)
        end = next_day.replace(hour=int(working_hours[0][1][:2]), minute=int(working_hours[0][1][3:]), second=0, microsecond=0)
        return start, end

    def split_by_non_working_ranges(start, end):
        allowed = []
        cur_start = start
        periods = sorted(non_working_ranges)
        for nw_start, nw_end in periods:
            if nw_end <= cur_start:
                continue
            if nw_start >= end:
                break
            if nw_start <= cur_start < nw_end:
                cur_start = max(cur_start, nw_end)
            elif cur_start < nw_start < end:
                allowed.append((cur_start, nw_start))
                cur_start = nw_end
        if cur_start < end:
            allowed.append((cur_start, end))
        return allowed

    results = []
    current_dt = parse(start_time)
    for task in task_list:
        name = task['name']
        duration = parse_hours(task['estimate_time'])
        allocations = []
        remaining = timedelta(hours=duration)
        while remaining > timedelta(0):
            slot_start, slot_end = next_working_slot(current_dt)
            # Loại trừ khoảng nghỉ
            if non_working_ranges:
                working_periods = split_by_non_working_ranges(slot_start, slot_end)
            else:
                working_periods = [(slot_start, slot_end)]

            allocated_in_this_slot = False
            for period_start, period_end in working_periods:
                if period_start >= period_end or remaining <= timedelta(0):
                    continue
                slot_available = period_end - period_start
                time_to_allocate = min(slot_available, remaining)
                alloc_end = period_start + time_to_allocate
                slot_duration_hrs = round(time_to_allocate.total_seconds() / 3600, 6)
                allocations.append({
                    "range": f"[{period_start.strftime('%Y/%m/%d %H:%M')}-{alloc_end.strftime('%H:%M')}]",
                    "estimate_time": slot_duration_hrs
                })
                remaining -= time_to_allocate
                current_dt = alloc_end
                allocated_in_this_slot = True
                if remaining <= timedelta(0):
                    break
            if not allocated_in_this_slot:
                current_dt = slot_end
        results.append({"name": name, "slots": allocations, "estimate_time": duration})
    return results

def convert_schedule_output_to_csv(schedule_output: List[Dict], output_format: str = "details", date_time_format: str = None) -> str:
    """
    Chuyển đổi kết quả sang chuỗi CSV với các cột: task_name, est, start_time, end_time.
    Nếu output_format="simple" thì mỗi task chỉ có 1 dòng, thời gian start là slot đầu tiên, end là slot cuối cùng.
    Nếu date_time_format="%Y/%m/%d %H:%M" or "%Y/%m/%d" đây là định dạng thời gian được dùng để format lại cột start_time, end_time.
    Sau khi tạo DataFrame, sẽ format lại cột start_time, end_time theo date_time_format nếu có.
    """
    output_details = output_format and output_format == "details"
    rows = []
    for task in schedule_output:
        for slot in task['slots']:
            slot_range = slot["range"] if isinstance(slot, dict) else slot
            slot_est = slot["estimate_time"] if output_details else task["estimate_time"]
            slot_range_str = slot_range.strip("[]")
            start_str, end_str = slot_range_str.split('-')
            start_time = start_str.strip()
            if len(end_str.strip()) == 5:
                date_part = start_time.split()[0]
                end_time = f"{date_part} {end_str.strip()}"
            else:
                end_time = end_str.strip()
            rows.append({
                "task_name": task["name"],
                "estimate_time": slot_est,
                "start_time": start_time,
                "end_time": end_time
            })

    if not output_details: # simple
        # Gom nhóm theo task_name, start là start_time đầu của dòng đầu, end là end_time cuối của dòng cuối
        from collections import OrderedDict
        grouped = OrderedDict()
        for row in rows:
            name = row["task_name"]
            if name not in grouped:
                grouped[name] = {
                    "task_name": name,
                    "estimate_time": row["estimate_time"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"]
                }
            else:
                # update end_time liên tục để lấy cái cuối cùng
                grouped[name]["end_time"] = row["end_time"]
        rows = list(grouped.values())

    df = pd.DataFrame(rows, columns=["task_name", "estimate_time", "start_time", "end_time"])

    if date_time_format:
        for idx, row in df.iterrows():
            start_dt = pd.to_datetime(row["start_time"], errors='coerce')
            df.at[idx, "start_time"] = start_dt.strftime(date_time_format)
            end_dt = pd.to_datetime(row["end_time"], errors='coerce')
            df.at[idx, "end_time"] = end_dt.strftime(date_time_format)

    return df.to_csv(index=False)