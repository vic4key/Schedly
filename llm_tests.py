from llm import llm_gen_task_list

result = llm_gen_task_list("tôi cần làm task 1 trong 2 giờ, task 2 trong 4 giờ, và task 3 trong 6 giờ")
print(result)

result = llm_gen_task_list("""
Do my laundry about 1 hours
Cancel milk delivery 0.5 hours
Clean fridge in 2 hours
Check passport in 30 minutes
Do web check-in in 4 hours
Download a movie for the flight in 45 minutes
Recharge mobile in 15 minutes
Pack swimsuit in 1 days
""")
print(result)

result = llm_gen_task_list("""
Trong một tuần làm việc, tôi thường bắt đầu mỗi buổi sáng với 30 phút kiểm tra email và cập nhật tiến độ nhóm, sau đó dành 3 tiếng cho các công việc như soạn thảo văn bản và xử lý hồ sơ.
Mỗi tuần, tôi có 2 buổi dành 1 tiếng 30 phút để gọi điện trao đổi với khách hàng về dự án.
Sau giờ nghỉ trưa 1 giờ, tôi dành 30 phút giờ để cập nhật dữ liệu vào hệ thống, 2 tiếng rưỡi xử lý các vấn đề phát sinh, và 30 phút  cuối ngày để tổng hợp báo cáo.
Vào cuối tuần, tôi dành 4 tiếng làm và đọc tài liệu chuyên môn, 1 giờ sắp xếp lại công việc, và 1 ngày để nghỉ ngơi thư giãn.
""")
print(result)



"""
$ python llm_tests.py
🤖 Using the LLM provider 'Local AI' with the model 'auto' at 'http://localhost:1234/v1/'
['task 1, 2 hrs', 'task 2, 4 hrs', 'task 3, 6 hrs']
['Do my laundry, 1 hrs', 'Cancel milk delivery, 0.5 hrs', 'Clean fridge, 2 hrs', 'Check passport, 0.5 hrs', 'Do web check-in, 4 hrs', 'Download a movie for the flight, 0.75 hrs', 'Recharge mobile, 0.25 hrs', 'Pack swimsuit, 24 hrs']
['kiểm tra email và cập nhật tiến độ nhóm, 0.5 hrs', 'soạn thảo văn bản và xử lý hồ sơ, 3 hrs', 'gọi điện trao đổi với khách hàng về dự án, 1.5 hrs', 'cập nhật dữ liệu vào hệ thống, 0.5 hrs', 'xử lý các vấn đề phát sinh, 2.5 hrs', 'tổng hợp báo cáo, 0.5 hrs', 'làm và đọc tài liệu chuyên môn, 4 hrs', 'sắp xếp lại công việc, 1 hrs', 'nghỉ ngơi thư giãn, 24 hrs']
"""
