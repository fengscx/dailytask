from selenium import webdriver
import time
import re
import logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
            self.username = username
            password =  password.encode('utf8')
            self.password = md5(password).hexdigest()
            self.soft_id = soft_id
            self.base_params = {
                'user': self.username,
                'pass2': self.password,
                'softid': self.soft_id,
            }
            self.headers = {
                'Connection': 'Keep-Alive',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
            }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

def getMyCourse():
    browser = webdriver.Chrome(executable_path='./chromedriver.exe')
    browser.get('NJU选课网址')
    time.sleep(1)
    # 填写你的学号和密码
    browser.find_element_by_id('loginName').send_keys('')
    browser.find_element_by_id('loginPwd').send_keys('')
    # 使用超级鹰验证码识别
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
    # count = 0
    while True:
        # if count > 2:
        #    break
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
