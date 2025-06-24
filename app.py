from flask import Flask, render_template, request
import schedly

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    csv_content = ""
    if request.method == "POST":
        try:
            working_day_time_range = [s.strip() for s in request.form["working_day_time_range"].split(",") if s.strip()]
            start_time = request.form["start_time"].strip()
            # Task nhập từng dòng: Tên task,est
            task_lines = [l.strip() for l in request.form["task_list"].split("\n") if l.strip()]
            task_list = []
            for line in task_lines:
                if "," in line:
                    name, est = line.split(",", 1)
                    task_list.append({"name": name.strip(), "est": est.strip()})
            # Lấy tất cả các input cùng tên (danh sách khoảng nghỉ)
            non_working_day_date_time_range = request.form.getlist("non_working_day_date_time_range")
            # Loại bỏ trường hợp user để trống input
            non_working_day_date_time_range = [s.strip() for s in non_working_day_date_time_range if s.strip()]
            if not non_working_day_date_time_range:
                non_working_day_date_time_range = None

            schedule_output = schedly.allocate_tasks_by_time_range(
                working_day_time_range,
                start_time,
                task_list,
                non_working_day_date_time_range=non_working_day_date_time_range
            )

            result = schedule_output

            # Xử lý option details
            output_format = "details" if request.form.get("output_format") == "details" else "simple"

            csv_content = schedly.convert_schedule_output_to_csv(schedule_output, output_format=output_format)
        except Exception as ex:
            result = f"Lỗi: {ex}"

    return render_template("index.html", result=result, csv_content=csv_content)

if __name__ == "__main__":
    app.run(debug=True)