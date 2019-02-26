import requests
import os
import time


def get_you(str):
    index = 0
    for i in str:
        if i == '无':
            index += 1
    return index


index = 0
L = [['k528',2], ['K512', 3], ['T170', 4], ['Z100', 2]]
while 1:
    print(index)
    time.sleep(1)
    index += 1
    req = requests.get(
        'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=2019-02-22&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SHH&purpose_codes=ADULT')
    a = req.json()
    for j in a['data']['result']:
        for t in L:
            if j.find(t[0]) != -1:
                if get_you(j) != t[1]:
                    print(t)
                    os.system('C:/Users/qsl/Videos/Captures/111.mp4')
