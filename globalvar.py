#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

### 存檔路徑
path = 'D:\\PycharmProjects\\paytable v1.0\\'

language = ['eng', 'sch', 'tch', 'tai']
id = "GAMEID"
### 押注設定要填小數點
cost = 1.0
Denom_1 = [0.2, 0.5, 5.0, 6.0, 50.0]
Times_1 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]

### 如果沒有第二組面額跟倍數,填空值即可 Denom_2=[]
Denom_2 = []
Times_2 = []

### 計算總投注
func = lambda x, y: [round(float(x[i // len(Times_1)] * Times_1[i % len(Times_1)]), 2) for i in
                     range(len(Denom_1) * len(Times_1))]
D1T1 = func(Denom_1, Times_2)
if len(Denom_2) > 0:
    func2 = lambda x, y: [round(float(x[i // len(Times_2)] * Times_2[i % len(Times_2)]), 2) for i in
                          range(len(Denom_2) * len(Times_2))]
    D2T2 = func2(Denom_2, Times_2)
    Bet_list = sorted(list(set(map(lambda x: round(float(x * cost), 2), D1T1 + D2T2))))
    print(Bet_list)
else:
    Bet_list = sorted(list(set(map(lambda x: round(float(x * cost), 2), D1T1))))
    print(Bet_list)

gameid = 'XXX-XX-%05d' % id
gamepath = path + gameid + '\\'

imageSave = gamepath + 'photo'
result = gamepath + 'payresult'


### 建立截圖&結果存放資料夾
def create():
    global path, gameid, imageSave, result
    try:
        os.mkdir(path + gameid)
        os.mkdir(imageSave)
        os.mkdir(result)
        print('Gameid: [' + gameid + '] Folders Created Successfully!')
    except:
        pass
