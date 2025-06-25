from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import schedly
import llm

app = Flask(__name__)
app.secret_key = 'your-very-secret-key-1234567890'  # Thay bằng chuỗi bí mật mạnh hơn khi triển khai thực tế

@app.route("/", methods=["GET"])
def index_get():
    csv_content = session.pop('csv_content', None)
    result = session.pop('result', None)
    return render_template("index.html", result=result, csv_content=csv_content)

@app.route("/", methods=["POST"])
def index_post():
    result = ""
    csv_content = ""
    try:
        working_day_time_range = [s.strip() for s in request.form["working_day_time_range"].split(",") if s.strip()]
        start_time = request.form["start_time"].strip()
        # Task nhập từng dòng: Tên task,estimate_time
        task_lines = [l.strip() for l in request.form["task_list"].split("\n") if l.strip()]
        task_list = []
        for line in task_lines:
            if "," in line:
                name, estimate_time = line.split(",", 1)
                task_list.append({"name": name.strip(), "estimate_time": estimate_time.strip()})
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
        # Sau khi render, chuyển hướng về GET để tránh hiển thị lại csv_content khi refresh
        session['csv_content'] = csv_content
        session['result'] = result
        return redirect(url_for('index_get'))
    except Exception as e:
        print("❌ LLM Error:", str(e))
        session['result'] = []
        session['csv_content'] = None
        return redirect(url_for('index_get'))

@app.route("/api/holidays", methods=["GET"])
def api_get_holidays():
    year = request.args.get("year", type=int)
    prompt = request.args.get("prompt", default="", type=str)
    if not year:
        return jsonify({"error": "Missing year"}), 400
    holidays = llm.llm_get_holidays(prompt, year)
    return jsonify(holidays)

@app.route("/api/gen_task_list", methods=["POST"])
def api_gen_task_list():
    task_list = []
    if text := request.json.get("text"):
        task_list = llm.llm_gen_task_list(text)
    return jsonify({"task_list": task_list})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)