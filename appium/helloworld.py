# -*- codeing: utf-8 -*-
import sys,os,unittest
from time import sleep
from appium import webdriver

'''
appium测试demo
author     Lynxz 阿冏
脚本语言    python 3.5
测试机型:   红米1s android 4.4.4 
在命令行中运行脚本即可: python helloworld.py
'''
class HelloWorld(unittest.TestCase):
    global driver

    # 得加 'test_' 前缀才会自动运行
    def test_addContact(self): 
        global driver  
        print("\n点击添加按钮...")
        # 设置desired capabilities键值对,主要用于通知 Appium 服务器建立需要的session
        desire_caps = {
            'platformName':'Android',
            'platformVersion':'4.4.4',
            # 设置启动的应用及activity西西里
            'appPackage':'com.android.contacts',
            'appActivity':'.activities.PeopleActivity',
            # 设备名称,可以通过 'adb devices' 获取,我同时连接多台设备时会有关系
            'deviceName':'9de1f8c7',
            # 屏蔽系统输入法,这样才可以输入我们预期的字符,包括中文,测试结束后记得在系统设置中修改输入法
            'unicodeKeyboard':True,
            'resetKeyboard':True
        }
      
        # 初始化Appium连接,具体的ip地址与appium gui中设置的相同
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desire_caps)

        # # 判断指定包名的app是否安装,若无则安装指定路径的apk文件,这里系统中可能会弹出授权提醒
        # installed = driver.is_app_installed("lynxz.org.recyclerviewdemo")
        # if not installed:
        #     print("安装app")
        #     driver.install_app("D:\\desk\\tutorial\\python\\appium\\app-debug.apk")

        # 查找创建联系人按钮
        # createContactBtn = driver.find_element_by_id('com.android.contacts:id/floating_action_button')
        createContactBtn = driver.find_element_by_id('com.android.contacts:id/fab')
        createContactBtn.click()
        
        # 单位:秒
        sleep(1)

        # 通过文本查找控件,并输入姓名
        name = driver.find_element_by_name(u"姓名")
        name.click()
        name.send_keys("阿冏lynxz")

        # 输入电话
        phone = driver.find_elements_by_name(u"电话")
        isEnable = phone[0].is_enabled()

        print("phone[0] enabled = %s\n" %(isEnable and "true" or "false"))
        phone[0].click()
        phone[0].send_keys("189***0620")

        # 截屏
        driver.save_screenshot("after_input.png")

        print("current activity " +  driver.current_activity)# 查看当前activity
        print("current context " +  driver.current_context)
        print("context " +  driver.context)
        print('network %d' %(driver.network_connection))


        # 单击完成按钮
        okBtn = driver.find_element_by_id("com.android.contacts:id/ok")
        okBtn.click()

        print("等待1s\n")
        sleep(1)

        # 在结果页面,判断结果是否符合预期
        phoneNumber = driver.find_element_by_id('com.android.contacts:id/data')
        self.assertEqual(phoneNumber.text,"189***0620")

        # 截屏
        # driver.get_screenshot_as_file("D:\\desk\\tutorial\\python\\appium\\scrren.png")
        driver.get_screenshot_as_file("./scrren_01.png")
        # 如果desired capabilities指定的app正在运行,则关闭该程序
        driver.close_app()

    def tearDown(self):
        global driver
        # 退出
        driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HelloWorld)
    unittest.TextTestRunner(verbosity=2).run(suite)