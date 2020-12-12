from selenium import webdriver
import time
import re
import logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import requests
from hashlib import md5

def getMyCourse():
    browser = webdriver.Chrome(executable_path='./chromedriver.exe')
    browser.get('https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/index_nju.html')
    time.sleep(1)
    browser.find_element_by_id('loginName').send_keys('')
    browser.find_element_by_id('loginPwd').send_keys('')
    chaojiying = Chaojiying_Client('', '', '906486')
    src = browser.find_element_by_id('vcodeImg').get_attribute('src')
    r = requests.get(url=src,stream=True)
    open('./img.jfif','wb').write(r.content)
    im = open('./img.jfif', 'rb').read()
    vc = chaojiying.PostPic(im, 1902)['pic_str']
    time.sleep(1)
    browser.find_element_by_id('verifyCode').send_keys(vc)
    browser.find_element_by_id('studentLoginBtn').click()
    time.sleep(3)
    browser.find_element_by_id('courseBtn').click()
    time.sleep(3)
    # test
    count = 0
    while True:
        if count > 2:
            break
        btns = browser.find_elements_by_class_name('zeromodal-btn')
        # print(len(btns))
        # break
        if not btns:
            browser.get('https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/course_nju.html')
            time.sleep(2)
            btns = browser.find_elements_by_class_name('zeromodal-btn')
            if len(btns)<5:
                print('Success')
                break
        # 选课
        btns[1].click()
        time.sleep(1)
        # 弹出框确定1
        browser.find_elements_by_class_name('zeromodal-btn')[5].click()
        time.sleep(1)
        # 弹出框确定2
        browser.find_elements_by_class_name('zeromodal-btn')[5].click()
        # count += 1

    browser.quit()
