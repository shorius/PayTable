#!/usr/bin/python
# -*- coding: utf-8 -*-
from jpype import *
import time, os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import HTMLTestRunner
from parameterized import parameterized
import pyautogui
import os
import cv2
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
## 截圖問題
# options = webdriver.ChromeOptions()
# options.add_argument('disable-gpu')
# driver=webdriver.Chrome(chrome_options = options)
browser = webdriver.Chrome(chromedrive)
browser.maximize_window()

# pyautogui座標
### selenium可沿用但y座標須扣掉-110

location_help = (230, 994)
location_help_next = (1685, 634)
location_help_close = (1688, 330)
location_bet_plus = (1516, 980)

challenge1 = (620, 497)
challenge2 = (1000, 497)
challenge3 = (1320, 497)

sc_left = Region(590, 705, 185, 102)
sc_right = Region(1288, 702, 219, 130)

p_r1 = Region(406, 717, 183, 71)
p_r2 = Region(754, 722, 195, 65)
p_r3 = Region(1102, 723, 185, 61)
p_r4 = Region(1448, 725, 192, 62)

### 每一頁的辨識區域,page_total=頁數列表
page_0 = [p_r1, p_r2, p_r3, p_r4]
# page_1 = [p_r1, p_r2, p_r3, p_r4]
# page_2 = [p_r1, p_r2, p_r3]
# page_3 = [p_r1, p_r2, p_r3]
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
        a = 'https://dev-api.iplaystar.net/game/'
        b = '/?access_token=(*--)aa62ffb88b300f6be6654615f17ce6fa&lang=' + gl.language[
            lan] + '&ccy=CNY&sm=00&subid=0&fullscr=1&lc=en-US&pm=0&ns=0&origin=https%3a%2f%2fdev-api.iplaystar.net&uid=3cMBz6ywu2h1dlEc8ZmKAfgNcV2TJOcliK1h%2bc4F%2bHA%3d&anal=8&lb=1&stf=1'
        url = a + str(gl.gameid) + b

        browser.get(url)
        time.sleep(10)

        # 如果有刮刮樂/大挑戰再加下面那段
        ActionChains(browser).move_by_offset(challenge1[0], challenge1[1] - 110).click().perform()
        time.sleep(0.3)
        ActionChains(browser).move_by_offset(-challenge1[0], -(challenge1[1] - 110)).perform()
        time.sleep(1)
        # ActionChains(browser).move_by_offset(challenge1[0],challenge1[1]-110).click().perform()
        # time.sleep(0.3)
        # ActionChains(browser).move_by_offset(-challenge1[0],-(challenge1[1]-110)).perform()
        # time.sleep(1)

        for x in range(len(gl.Bet_list)):
            totalbet_num = x
            click_help_open()
            time.sleep(0.5)
            # click_next() ### 如果點開help第0頁就有連動的Scatter,則此行不需要
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
    # suiteTest = unittest.TestSuite()
    # suiteTest.addTest(CalculateFolderSize_TestCase(example))
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
