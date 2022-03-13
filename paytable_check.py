#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import re
import os
import sys

import globalvar as gl
dir = os.getcwd()
if not dir in sys.path: sys.path.append(dir)

lines = []
with open(gl.path + '\\source\\pay_table_config.js', 'r') as fp:
    js = fp.read()
    js = re.findall(r"pay: [0-9]+", js)
    js = re.findall(r"[0-9]+", str(js))
    js = list(map(float, js))
    # print(js)
    for x in range(len(js)):
        jstmp = js[x] / (1/gl.Denom_1[0])  # 原始paytable數值最小化
        jstmp = str(format(jstmp, '0.2f'))
        lines.append(jstmp)
fp.close()
# print(lines)

### 最小化後計算各投注金額連動之數值
Pay_js = []
for i in range(len(gl.Bet_list)):
    tmp1 = float(gl.Bet_list[i]/gl.Bet_list[0])
    for j in range(len(lines)):
        tmp2 = float(lines[j])
        p = format(tmp1 * tmp2, '0.2f')
        Pay_js.append(p)
print(Pay_js)

###開啟ocr辨識寫下的結果依序比對
def paycheck(name,Pay_js):
    fp_ocr = open(gl.result + '\\' + name + '_Paytable.txt', 'r', encoding="utf-8")
    Pay_ocr = []
    for i in fp_ocr.readlines():
        tmp = i.encode('utf-8').decode('utf-8-sig').strip()
        tmp = tmp.split()
        tmp = "".join(tmp)
        tmp = tmp.replace(',', '')
        if not len(tmp) or tmp.startswith('#'):
            continue
        Pay_ocr.append(tmp)
    fp_ocr.close()

    count1 = -1
    passCount = 0
    failCount = 0
    for i in range(len(Pay_js)):
        if i % len(lines) == 0:
            count1 += 1
            val = format(gl.Bet_list[count1], '0.2f')
        try:
            assert Pay_js[i] == Pay_ocr[i]
            passCount += 1
            print("[PASS] :TotalBet="+val+" ,Pay"+str(i%len(lines)+1)+"--- result --> "+str(Pay_ocr[i])+" = "+str(Pay_js[i]))
        except AssertionError:
            failCount += 1
            print("*[FAIL] :TotalBet="+val+" ,Pay"+str(i%len(lines)+1)+"--- result --> "+str(Pay_ocr[i])+" is not equal to "+str(Pay_js[i]))
    print("TotalPass: " + str(passCount))
    print("TotalFail: " + str(failCount))
    print('===========================')
    if failCount > 0:
        assert False
