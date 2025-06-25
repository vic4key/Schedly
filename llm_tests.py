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



"""
$ python llm_tests.py
['task 1, 2 hrs', 'task 2, 4 hrs', 'task 3, 6 hrs']
['do laundry, 1 hrs', 'cancel milk delivery, 0.5 hrs', 'clean fridge, 2 hrs', 'check passport, 0.5 hrs', 'do web check-in, 4 hrs', 'download movie for flight, 0.75 hrs', 'recharge mobile, 0.25 hrs', 'pack swimsuit, 24 hrs']
"""