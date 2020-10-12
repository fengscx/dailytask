# 预约
def bash_appointment():
    # 设置浏览器参数
    options = Options()
    # 无头
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
    browser.get('http://authserver.nju.edu.cn/authserver/login?'
                'service=http%3A%2F%2Fehall.nju.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2'
                'Fehall.nju.edu.cn%2Fywtb-portal%2Fofficial%2Findex.html')
    browser.find_element_by_id('username').send_keys('your student num')
    time.sleep(1)
    browser.find_element_by_id('password').send_keys('your password')
    time.sleep(1)
    btn = browser.find_element_by_class_name("auth_login_btn")
    btn.click()
    time.sleep(1)
    browser.get('http://ehallapp.nju.edu.cn/qljfwapp/sys/lwAppointmentBathroom/*default/index.do#/')
    # 不睡一会获取不到内容。。。坑！
    time.sleep(3)
    element = browser.find_elements_by_class_name("lib-orders")
    # 不断尝试
    n = 1
    while not element:
        # browser.get('http://ehallapp.nju.edu.cn/qljfwapp/sys/lwAppointmentBathroom/*default/index.do#/')
        time.sleep(3*n)
        element = browser.find_elements_by_class_name("lib-orders")
        n += 1
        if not element and n== 10:
            print(" Some Errors ")
            return

    element[0].click()
    # # 输入本身有阻塞，所以不需要sleep
    # app_time = input("请输入想预约的时间（13:00 ~ 23:00）:")
    # # 时间格式处理
    # hour,minute = int(app_time[0:2]), int(app_time[3:5])
    # if hour == 17:
    #     print("17~18 休息嗷")
    #     return
    #
    # if hour > 17:
    #     hour = hour-1
    # 从1开始计数
    # num = (hour- 13)*3 + ( minute//20) + 1

    # 自动脚本不支持动态时间设置
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[23]').click()
    time.sleep(3)
    browser.find_element_by_class_name("mt-btn-primary").click()
    time.sleep(3)
    browser.quit()
    return

if __name__ == '__main__':
    bash_appointment()
