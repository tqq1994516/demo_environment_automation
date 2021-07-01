# coding=utf-8
import os
import time

import allure
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# create a logger instance
logger = Logger(logger="BasePage").getlog()


@allure.step("等待元素")
def wait_element(driver, wait_time, step, selector_type, selector):
    allure.attach('等待时长:{}(s); 间隔时长:{}(s); 定位类型:{}; 定位值:{};'.format(wait_time, step, selector_type, selector), "操作信息")
    wait = WebDriverWait(driver, wait_time, poll_frequency=step,
                         ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    if selector_type == 'x':
        wait.until(EC.visibility_of_element_located((By.XPATH, selector)), "%s not find" % selector)
    elif selector_type == 'n':
        wait.until(EC.visibility_of_element_located((By.NAME, selector)), "%s not find" % selector)
    elif selector_type == 'c':
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, selector)), "%s not find" % selector)
    elif selector_type == 'i':
        wait.until(EC.presence_of_element_located((By.ID, selector)), "%s not find" % selector)
    elif selector_type == 's':
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)), "%s not find" % selector)


def sleep(seconds):
    time.sleep(seconds)
    logger.info("Sleep for %d seconds" % seconds)


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """

    def __init__(self, driver):
        self.driver = driver

    # quit browser and end testing
    def quit_browser(self):
        logger.info("The browser will quit")
        self.driver.quit()

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and close the browser.")
        except NameError as e:
            logger.error("Failed to close the browser with %s" % e)

    # 保存图片
    def save_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """

        file_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Screenshots/'

        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'

        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /Screenshots")
            print(
                "<a href='" + screen_name + "' title='" + rq + "'>" + "<img src='" + screen_name + "' width=400 />" + "</a>")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.save_img()

    # 定位元素方法
    def find_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector
        :return: element
        """
        element = ''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        if selector_by == "i" or selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "n" or selector_by == 'name':
            try:
                element = self.driver.find_element_by_name(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "c" or selector_by == 'class_name':
            try:
                element = self.driver.find_element_by_class_name(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "l" or selector_by == 'link_text':
            try:
                element = self.driver.find_element_by_link_text(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "p" or selector_by == 'partial_link_text':
            try:
                element = self.driver.find_element_by_partial_link_text(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "t" or selector_by == 'tag_name':
            try:
                element = self.driver.find_element_by_tag_name(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        elif selector_by == "s" or selector_by == 'selector_selector':
            try:
                element = self.driver.find_element_by_css_selector(selector_value)
                logger.info("Had find the element {} successful by {} via value: {} ".format(element.text, selector_by,
                                                                                             selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                # self.save_img()  # take screenshot
        else:
            raise NameError("Please enter a valid type of targeting elements.")
        return element

    # 输入
    @allure.step("输入信息")
    def enter(self, selector, text):
        allure.attach('定位类型:{}; 定位值:{}; 输入值:{}'.format(selector.split('=>')[0], selector.split('=>')[1], text), "操作信息")
        el = self.find_element(selector)
        try:
            el.send_keys(text)
            logger.info("Had enter %s in inputBox" % text)
        except NameError as e:
            logger.error("Failed to enter in input box with %s" % e)
            self.save_img()

    # 清除文本框
    @allure.step("清空元素")
    def clear(self, selector):
        allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
        el = self.find_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.save_img()

    # 点击元素
    @allure.step("点击元素")
    def click(self, selector):
        allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
        el = self.find_element(selector)
        try:
            logger.info("The element %s was clicked." % el.text)
            el.click()
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 调用js操作
    @allure.step("调用js操作")
    def es(self, js, selector=None):
        try:
            if selector:
                allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
                el = self.find_element(selector)
                self.driver.execute_script(js, el)
            else:
                allure.attach('定位类型:{}; 定位值:{}'.format(js.split(').')[0], js.split(').')[1]), "操作信息")
                self.driver.execute_script(js)
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 获取元素内容
    @allure.step("获取元素内容")
    def get_element_text(self, selector):
        el_text = self.find_element(selector).text
        allure.attach('定位类型:{}; 定位值:{}; 获取值:{} '.format(selector.split('=>')[0], selector.split('=>')[1], el_text),
                      "操作信息")
        return el_text

    # 获取网页标题
    @allure.step("获取网页标题")
    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        allure.attach('获取值:{} '.format(self.driver.title), "操作信息")
        return self.driver.title

    # 获取网页URL
    @allure.step("获取网页URL")
    def get_page_url(self):
        logger.info("Current page title is %s" % self.driver.current_url)
        allure.attach('获取值:{} '.format(self.driver.current_url), "操作信息")
        return self.driver.current_url

    @allure.step("获取新标签页或窗口")
    def get_new_tab(self, url, type):
        allure.attach('类型:{}; url:{}'.format(type, url), "操作信息")
        # 存储原始窗口的 ID
        self.original_window = self.driver.current_window_handle
        if type == 'tab':
            # 打开新标签页并切换到新标签页
            self.driver.switch_to.new_window('tab')
        else:
            # 打开一个新窗口并切换到新窗口
            self.driver.switch_to.new_window('window')
        # 循环执行，直到找到一个新的窗口句柄
        for window_handle in self.driver.window_handles:
            if window_handle != self.original_window:
                self.driver.switch_to.window(window_handle)
                break
        self.driver.get(url)

    @allure.step("滑动滑块")
    def move_slider(self, target_selector, source_selector=None, x=None, y=None):
        el = self.find_element(target_selector)
        actions = ActionChains(self.driver)
        if source_selector:
            allure.attach('源元素定位类型:{}; 源元素定位值:{}; 目标元素定位类型:{}; 目标元素定位值:{}'.format(source_selector.split('=>')[0],
                                                                                  source_selector.split('=>')[1],
                                                                                  target_selector.split('=>')[0],
                                                                                  target_selector.split('=>')[1]),
                          "操作信息")
            elX = el.location.get('x')
            elY = el.location.get('y')
            actions.move_by_offset(elX, elY).perform()
        else:
            allure.attach('目标元素定位类型:{}; 目标元素定位值:{}; 滑动距离(x:{},y:{})'.format(target_selector.split('=>')[0],
                                                                            target_selector.split('=>')[1], x, y),
                          "操作信息")
            actions.move_by_offset(x, y).perform()
        actions.release().perform()

    @allure.step("切回之前的窗口或标签")
    def switch_original_window(self):
        if self.original_window:
            self.driver.switch_to.window(self.original_window)
        else:
            self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("切换iframe")
    def switch_iframe(self, iframe_id=None, iframe_index=None, selector=None):
        if iframe_id:
            allure.attach('切换iframe_id:{}'.format(iframe_id), "操作信息")
            self.driver.switch_to.frame(iframe_id)
        elif iframe_index:
            allure.attach('切换iframe_index:{}'.format(iframe_index), "操作信息")
            self.driver.switch_to.frame(iframe_index)
        else:
            allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
            el = self.find_element(selector)
            self.driver.switch_to.frame(el)

    @allure.step("退出iframe")
    def quit_iframe(self):
        self.driver.switch_to.default_context()
