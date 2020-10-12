#!/usr/bin/python3
from selenium import webdriver
import time
import re
import logging

def login():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(executable_path='/var/dailytask/geckodriver',options=options)
    browser.get('http://authserver.nju.edu.cn/authserver/login?'
                'service=http%3A%2F%2Fehall.nju.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2'
                'Fehall.nju.edu.cn%2Fywtb-portal%2Fofficial%2Findex.html')
    # 输入你的学号
    browser.find_element_by_id('username').send_keys('your student number')
    time.sleep(1)
    # 输入你的统一身份认证的密码
    browser.find_element_by_id('password').send_keys('your password')
    time.sleep(1)
    btn = browser.find_element_by_class_name("auth_login_btn")
    btn.click()
    time.sleep(1)
    browser.get('http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do')
    time.sleep(6)
    text = browser.execute_script('return document.body.innerText')
    rex = re.compile('\w{32}')
    WID = re.search(rex,text).group()
    time.sleep(1)
    browser.get('http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do?'
                'WID='+ WID +
                '&CURR_LOCATION=%E4%B8%AD%E5%9B%BD%E6%B1%9F%E8%8B%8F%E7%9C%81%E5%8D%97%E4%BA%AC%E5%B8%82%E9%B'
                'C%93%E6%A5%BC%E5%8C%BA%E5%B9%BF%E5%B7%9E%E8%B7%AF14-4&IS_TWZC=1&IS_HAS_JKQK='
                '1&JRSKMYS=1&JZRJRSKMYS=1 ')
    time.sleep(5)
    ret = browser.execute_script('return document.body.innerText')
    rex = re.compile('"msg":"(.*?)"')
    ans = re.findall(rex, ret)[0] if re.findall(rex,ret) else None
    # time.sleep(3)
    # 可以捕获异常或输出日志，但没必要
    if ans != '成功':
	#logging.basicConfig(level=logging.ERROR,
         #           filename='daily_health.log',
          #          filemode='a',
           #         format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
            #        )
        print("Something is Wrong -_-")
    browser.quit()
    return

if __name__ == '__main__':
    login()
