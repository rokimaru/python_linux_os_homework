import math
import re
import datetime
import subprocess

from collections import Counter

file_name = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M") + "-scan.txt"

list_of_users = [] # пльзователи системы списком (получаем кол-во процессов)
memory_used = 0 # всего памяти использовано
CPU_used = 0 # всего ЦПУ использовано
result_list = [] #
list_of_string = [] #

# запустить команду ps aux и получить ее результаты в виде списка
result = subprocess.run(["ps", "aux"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
result = result.stdout.decode("utf-8")
result_string = result.split("\n")
# удалить заголовок таблицы результатов и последнюю строку
del result_string[0]
del result_string[-1]
# собрать результаты в словарь
result_dict = {}
for string in result_string:
    s = re.sub(r'\s+', ' ', string).split(" ")
    result_dict['USER'] = s[0]
    result_dict['PID'] = s[1]
    result_dict['%CPU'] = s[2]
    result_dict['%MEM'] = s[3]
    result_dict['VSZ'] = s[4]
    result_dict['RSS'] = s[5]
    result_dict['TTY'] = s[6]
    result_dict['STAT'] = s[7]
    result_dict['START'] = s[8]
    result_dict['TIME'] = s[9]
    result_dict['COMMAND'] = s[10]
    memory_used += float(s[3])
    CPU_used += float(s[2])
    result_list.append(dict(result_dict))
    list_of_users.append(s[0])
# получить  список уникальных юзеров
users = set(list_of_users)
user_dict = Counter(list_of_users)
# найти процесс съедающий самое большое кол-во памяти
after_sort = sorted(result_list, key=lambda mem: float(mem['%MEM']), reverse=True)
mem_app = str(after_sort[0]['COMMAND'])
# найти процесс съедающий самое большое кол-во ЦПУ
after_sort = sorted(result_list, key=lambda cpu: float(cpu['%CPU']), reverse=True)
cpu_app = str(after_sort[0]['COMMAND'])

# записать результаты в файл
with open(file_name, "w") as f:
    f.write(f"Пользователи системы: {str(list(users))}" + "\n")
    f.write(f"Процессов запущено: {str(len(list_of_users))}" + "\n")
    f.write(f"Процессов по пользователям: {str(user_dict)}" + "\n")
    f.write(f"Всего памяти используется: {str(math.ceil(memory_used))}" + "%\n")
    f.write(f"Больше всего памяти ест: {mem_app}" + "\n")
    f.write(f"Всего CPU используется: {str(math.ceil(CPU_used))}" + "%\n")
    f.write(f"Больше всего CPU ест: {cpu_app}" + "\n")

