#!/usr/bin/python
# -*- coding: utf-8 -*-
from jpype import *
import time
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import HTMLTestRunner
from parameterized import parameterized
import pyautogui
### 測試案例
import paytable_check
import globalvar as gl

### JVM,java.class.path要改自己的sikulixapi路徑
jvmPath = getDefaultJVMPath()
startJVM(jvmPath, '-ea', '-Djava.class.path=D:\\sikuli\\sikulixapi.jar', convertStrings=False)
app = JClass('org.sikuli.script.App')
Screen = JClass('org.sikuli.script.Screen')
Region = JClass('org.sikuli.script.Region')
screen = Screen()

path = os.getcwd()

# chromedrive
chromedrive = "C:/Python37/chromedriver"
chromedrive = chromedrive
# 截圖問題
# options = webdriver.ChromeOptions()
# options.add_argument('disable-gpu')
# driver=webdriver.Chrome(chrome_options = options)
browser = webdriver.Chrome(chromedrive)
browser.maximize_window()

# pyautogui座標
# selenium可沿用但y座標須扣掉-110
# 每一頁的辨識區域,page_total=頁數列表
page_0 = [p_r1, p_r2, p_r3, p_r4]
page_1 = [p_r1, p_r2, p_r3, p_r4]
page_total = [page_0]


# ###確認區域用的highlight
# for num in range(4):
#    page_1[num].highlight(0.5)
#    print(page_1[num].text())


def click_help_open():
    ActionChains(browser).move_by_offset(location_help[0], location_help[1] - 110).click().perform()
    time.sleep(0.3)
    ActionChains(browser).move_by_offset(-location_help[0], -(location_help[1] - 110)).perform()
    time.sleep(0.5)


def click_next():
    ActionChains(browser).move_by_offset(location_help_next[0], location_help_next[1] - 110).click().perform()
    time.sleep(0.5)
    ActionChains(browser).move_by_offset(-location_help_next[0], -(location_help_next[1] - 110)).perform()
    time.sleep(0.5)


def click_close_and_plus():
    ActionChains(browser).move_by_offset(location_help_close[0], location_help_close[1] - 110).click().perform()
    time.sleep(0.5)
    ActionChains(browser).move_by_offset(-location_help_close[0], -(location_help_close[1] - 110)).perform()
    time.sleep(0.5)
    ActionChains(browser).move_by_offset(location_bet_plus[0], location_bet_plus[1] - 110).click().perform()
    time.sleep(0.5)
    ActionChains(browser).move_by_offset(-location_bet_plus[0], -(location_bet_plus[1] - 110)).perform()
    time.sleep(0.5)


def into_game():
    count = 0
    lan = -1
    for m in range(len(gl.language)):
        count += 1
        lan += 1
        wfp = open(gl.result + '\\' + gl.language[lan] + '_Paytable.txt', 'w', encoding="utf-8")
        a = "API_URL
        b = 'token' + gl.language[lan]
        url = a + str(gl.gameid) + b

        browser.get(url)
        time.sleep(10)

        # <editor-fold desc="如果有event再加下面那段">
        ActionChains(browser).move_by_offset(challenge1[0], challenge1[1] - 110).click().perform()
        time.sleep(0.3)
        ActionChains(browser).move_by_offset(-challenge1[0], -(challenge1[1] - 110)).perform()
        time.sleep(1)
        # </editor-fold>

        for x in range(len(gl.Bet_list)):
            totalbet_num = x
            click_help_open()
            time.sleep(0.5)
            # click_next()
            time.sleep(0.5)
            for n in range(len(page_total)):
                now_page = page_total[n]
                # browser.get_screenshot_as_file(gl.imageSave + '\\' + str(gl.language[lan]) + '_Paytable_' + str(
                #     totalbet_num) + '-' + str(n) + '.png')
                img = pyautogui.screenshot(region=[0, 110, 1920, 926])  # x,y,w,h
                img.save(gl.imageSave + '\\' + str(gl.language[lan]) + '_Paytable_' + str(
                    totalbet_num) + '-' + str(n) + '.png')

                for now_region in range(len(now_page)):
                    value_reg = now_page[now_region]
                    value = value_reg.text()
                    # print(str(value))
                    wfp.write(str(value))
                if n == len(page_total) - 1:
                    click_close_and_plus()
                else:
                    click_next()
                    time.sleep(0.5)
        print(gl.language[lan] + ' Status: Done')
        wfp.close()
    browser.quit()


class paytable(unittest.TestCase):

    def test_01_paytable_ocr(self):
        gl.create()
        into_game()
        print('finished')

    @parameterized.expand([
        ["eng"],
        ["sch"],
        ["tch"],
        ["tai"],
    ])
    def test_sequence(self, name):
        print('Language:' + name + '\n')
        print('Paytable Compare Result:' + '\n')
        paytable_check.paycheck(name, paytable_check.Pay_js)


def Suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(paytable)
    return suite


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    fp = open(now + '_Paytable_TestReport.html', 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='Paytable Test Report',
        description=' ',
    )

    runner.run(Suite())
    fp.close()
shutdownJVM()
