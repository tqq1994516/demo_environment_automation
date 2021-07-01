# -*- coding:utf-8 -*-
import configparser
import os

import allure
from selenium import webdriver
from framework.logger import Logger

logger = Logger(logger="BrowserEngine").getlog()


class BrowserEngine(object):
    # read the browser type from config.ini file, return the driver
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '/config/config.ini', encoding='utf-8')
    browser = config.get("browserType", "browserName")
    browser_dir_path = os.getcwd() + '/driver/' + browser + 'driver.exe'
    driver = None

    def __init__(self):
        # 加载启动项
        if self.browser == 'chrome':
            self.option = webdriver.ChromeOptions()
        elif self.browser == 'firefox':
            self.option = webdriver.FirefoxOptions()
        self.option.add_argument('-headless')  # 隐藏浏览器
        self.option.add_argument('-disable-gpu')
        self.option.add_argument('-no-sandbox')
        if self.browser == 'chrome':
            # self.driver = webdriver.Chrome(executable_path=BrowserEngine.browser_dir_path, options=self.option)  # 无窗口测试
            self.driver = webdriver.Chrome(executable_path=BrowserEngine.browser_dir_path)
            logger.info("Starting Chrome browser.")
        elif self.browser == 'firefox':
            # self.driver = webdriver.Firefox(executable_path=BrowserEngine.browser_dir_path, options=self.option)  # 无窗口测试
            self.driver = webdriver.Firefox(executable_path=BrowserEngine.browser_dir_path)
            logger.info("Starting Firefox browser.")

    @allure.step("打开浏览器")
    def open_browser(self, url):
        logger.info("You had select %s browser." % self.browser)
        logger.info("The test server url is: %s" % url)

        self.driver.get(url)
        allure.attach("驱动类型:{}; url:{}".format(self.driver, url), '操作信息')
        logger.info("Open url: %s" % url)
        self.driver.maximize_window()
        logger.info("Maximize the current window.")
        self.driver.implicitly_wait(2)
        logger.info("Set implicitly wait 2 seconds.")

    @allure.step("关闭浏览器")
    def quit_browser(self):
        logger.info("Now, Close and quit the browser.")
        self.driver.quit()
