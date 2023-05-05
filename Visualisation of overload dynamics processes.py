import json
from openpyxl import Workbook
import plotly as py
import pandas as pd
import plotly_express as px
import datetime
import sys
def load_file(file_address):
    with open(file_address) as json_file:
        new_file = json.load(json_file)
    return new_file
overload_p_t = {}
for i in range(1,9):
    b_name = "中断" + str(i) + "天实验\\overload way.json"
    aim_file = load_file(b_name)
    for key in aim_file.keys():
        p_name = aim_file[key][0]
        overload_s = aim_file[key][1]
        if p_name not in overload_p_t.keys():
            overload_p_t[p_name] = datetime.datetime.strptime(overload_s,"%Y-%m-%d %H:%M")
        else:
            s_time1 = datetime.datetime.strptime(overload_s,"%Y-%m-%d %H:%M")

            if s_time1 < overload_p_t[p_name]:
                overload_p_t[p_name] = datetime.datetime.strptime(overload_s,"%Y-%m-%d %H:%M")

overload_p_t_order = sorted(overload_p_t.items(),key = lambda x:x[1])
# print(overload_p_t_order)
# sys.exit()
for i in range(1,9):
    break_time = "中断" + str(i) + "天实验"
    file_name = break_time + "\\overload way.json"
    over_load = load_file(file_name)

    time_min = "2020-03-31 12:00"
    tim_max = "2020-09-28 08:00"

    new_overload_dict = {"Port":[],"Start time":[],"End time":[]}
    k = 0
    for port_index in overload_p_t_order:
        if k < len(overload_p_t_order)/2:
            new_overload_dict['Port'].append(port_index[0])
            new_overload_dict['Start time'].append(time_min)
            new_overload_dict["End time"].append(time_min)
        else:
            new_overload_dict['Port'].append(port_index[0])
            new_overload_dict['Start time'].append(tim_max)
            new_overload_dict["End time"].append(tim_max)
        k += 1
    # 记录已有港口信息的字典
    for key in over_load.keys():
        key2 = over_load[key][0]
        new_overload_dict['Port'].append(key2)
        new_overload_dict['Start time'].append(over_load[key][1])
        new_overload_dict["End time"].append(over_load[key][2])


        # new_overload_dict[port].append(str(over_load[key][3]))
        # new_overload_dict[port].append(str(over_load[key][4]))

    pyoff = py.offline.plot
    data = pd.DataFrame(new_overload_dict)

    fig = px.timeline(data,x_start="Start time",x_end="End time",y="Port")  #这里有些取巧，color参数并没用来设置颜色，当color参数与y参数一致时就会同时出现多条对应时间线，固直接把Task列表传给color参数
    fig.update_layout(title = {'text':str(i)+ " days",'x':0.5,'y':0.99},
                      xaxis_title = "Date and time",
                      yaxis_title = "Ports",
                      font=dict(family = 'Times New Roman',
                                size = 28,
                                color = "black"))


    pyoff(fig, filename= break_time + '\\过载甘特图.html')
