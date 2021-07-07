# coding=utf-8
import os
import sys
import time
import allure
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains
from pykeyboard import PyKeyboard
import pyperclip
from pynput.keyboard import Key, Controller
from subprocess import Popen, PIPE

# create a logger instance
logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """

    def __init__(self, driver):
        self.driver = driver

    def quit_browser(self):
        """
        退出浏览器，测试结束执行此函数而close_browser
        :return:
        """
        logger.info("The browser will quit")
        self.driver.quit()

    def forward(self):
        """
        浏览器前进操作
        :return:
        """
        self.driver.forward()
        logger.info("Click forward on current page.")

    def back(self):
        """
        浏览器后退操作
        :return:
        """
        self.driver.back()
        logger.info("Click back on current page.")

    def wait(self, seconds):
        """
        隐式等待
        :param seconds: 隐式等待秒数
        :return:
        """
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    def close(self):
        """
        点击关闭当前窗口
        :return:
        """
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

    @allure.step("等待元素")
    def wait_element(self, wait_time, step, selector):
        """
        每个setp秒就向当前页面查询元素是否存在，存在执行后续动作，超过最大等待时间抛出timeout异常
        :param wait_time: 最大等待时间
        :param step: 查询间隔
        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :return:
        """
        selector_type = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        allure.attach('等待时长:{}(s); 间隔时长:{}(s); 定位类型:{}; 定位值:{};'.format(wait_time, step, selector_type, selector_value),
                      "操作信息")
        wait = WebDriverWait(self.driver, wait_time, poll_frequency=step,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        if selector_type == 'x':
            logger.info('wait element type:{}, value:{} '.format('XPATH', selector_value))
            wait.until(EC.visibility_of_element_located((By.XPATH, selector_value)), "%s not find" % selector_value)
        elif selector_type == 'n':
            logger.info('wait element type:{}, value:{} '.format('NAME', selector_value))
            wait.until(EC.visibility_of_element_located((By.NAME, selector_value)), "%s not find" % selector_value)
        elif selector_type == 'c':
            logger.info('wait element type:{}, value:{} '.format('CLASS_NAME', selector_value))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, selector_value)), "%s not find" % selector_value)
        elif selector_type == 'i':
            logger.info('wait element type:{}, value:{} '.format('ID', selector_value))
            wait.until(EC.presence_of_element_located((By.ID, selector_value)), "%s not find" % selector_value)
        elif selector_type == 's':
            logger.info('wait element type:{}, value:{} '.format('CSS_SELECTOR', selector_value))
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_value)),
                       "%s not find" % selector_value)

    def sleep(self, seconds):
        """

        :param seconds: 强制等待秒数
        :return:
        """
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

    # 定位元素方法
    def find_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector： selenium选择器，以"x=>path"形式传递，详见find_element()
        :return: element：返回选择器指向的html element
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
        """

        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :param text: 向input中输入的内容
        :return:
        """
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
        """

        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :return:
        """
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
        """

        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :return:
        """
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
        """
        Example: self.driver.es("arguments[0].click();", pwd_login_a), 其中arguments[0]为固定写法代表第二个参数选择器指向的html element，arguments[0]方法需要写原生支持js方法
        :param js: js语句
        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :return:
        """
        try:
            if selector:
                allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
                el = self.find_element(selector)
                self.driver.execute_script(js, el)
                logger.info('execute js:{} with element:{}'.format(js, selector))
            else:
                allure.attach('定位类型:{}; 定位值:{}'.format(js.split(').')[0], js.split(').')[1]), "操作信息")
                self.driver.execute_script(js)
                logger.info('execute js:{} with element:{}'.format(js, js.split(').')[0]))
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 获取元素内容
    @allure.step("获取元素内容")
    def get_element_text(self, selector):
        """

        :param selector: selenium选择器，以"x=>path"形式传递，详见find_element()
        :return: 返回元素text
        """
        el_text = self.find_element(selector).text
        allure.attach('定位类型:{}; 定位值:{}; 获取值:{} '.format(selector.split('=>')[0], selector.split('=>')[1], el_text),
                      "操作信息")
        logger.info('text is {}'.format(el_text))
        return el_text

    # 获取网页标题
    @allure.step("获取网页标题")
    def get_page_title(self):
        """

        :return: 返回当前网页title
        """
        logger.info("Current page title is %s" % self.driver.title)
        allure.attach('获取值:{} '.format(self.driver.title), "操作信息")
        return self.driver.title

    # 获取网页URL
    @allure.step("获取网页URL")
    def get_page_url(self):
        """

        :return: 返回当前网页url
        """
        logger.info("Current page title is %s" % self.driver.current_url)
        allure.attach('获取值:{} '.format(self.driver.current_url), "操作信息")
        return self.driver.current_url

    @allure.step("获取新标签页或窗口")
    def get_new_tab(self, url, type):
        """

        :param url: 新开启网址
        :param type: 传递"tab"或"window",tab创建新标签，window创建新窗口
        :return:
        """
        allure.attach('类型:{}; url:{}'.format(type, url), "操作信息")
        # 存储原始窗口的 ID
        self.original_window = self.driver.current_window_handle
        if type == 'tab':
            # 打开新标签页并切换到新标签页
            self.driver.switch_to.new_window('tab')
            logger.info('successful create new tab')
        else:
            # 打开一个新窗口并切换到新窗口
            self.driver.switch_to.new_window('window')
            logger.info('successful create new window')
        # 循环执行，直到找到一个新的窗口句柄
        for window_handle in self.driver.window_handles:
            if window_handle != self.original_window:
                self.driver.switch_to.window(window_handle)
                logger.info('switch to handle {}'.format(window_handle))
                break
        self.driver.get(url)
        logger.info('open new url:{}'.format(url))

    @allure.step("滑动滑块")
    def move_slider(self, target_selector, source_selector=None, x=None, y=None):
        actions = ActionChains(self.driver)
        if source_selector:
            allure.attach('源元素定位类型:{}; 源元素定位值:{}; 目标元素定位类型:{}; 目标元素定位值:{}'.format(source_selector.split('=>')[0],
                                                                                  source_selector.split('=>')[1],
                                                                                  target_selector.split('=>')[0],
                                                                                  target_selector.split('=>')[1]),
                          "操作信息")
            el = self.find_element(source_selector)
            elX = el.location.get('x')
            elY = el.location.get('y')
            el = self.find_element(target_selector)
            actions.move_by_offset(elX, elY).perform()
            logger.info('move slider:{}, offset x:{},y:{}'.format(target_selector, elX, elY))
        else:
            allure.attach('目标元素定位类型:{}; 目标元素定位值:{}; 滑动距离(x:{},y:{})'.format(target_selector.split('=>')[0],
                                                                            target_selector.split('=>')[1], x, y),
                          "操作信息")
            el = self.find_element(target_selector)
            actions.move_by_offset(x, y).perform()
        actions.release().perform()
        logger.info('move slider:{}, offset x:{},y:{}'.format(target_selector, x, y))

    @allure.step("切回之前的窗口或标签")
    def switch_original_window(self):
        """切回之前的窗口或标签"""
        if self.original_window:
            self.driver.switch_to.window(self.original_window)
            logger.info('switch to handle {}'.format(self.original_window))
        else:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info('switch to handle {}'.format(self.driver.window_handles[-1]))

    @allure.step("切换iframe")
    def switch_iframe(self, iframe_id=None, iframe_index=None, selector=None):
        if iframe_id:
            allure.attach('切换iframe_id:{}'.format(iframe_id), "操作信息")
            self.driver.switch_to.frame(iframe_id)
            logger.info('switch to iframe id:{}'.format(iframe_id))
        elif iframe_index:
            allure.attach('切换iframe_index:{}'.format(iframe_index), "操作信息")
            self.driver.switch_to.frame(iframe_index)
            logger.info('switch to iframe index:{}'.format(iframe_index))
        else:
            allure.attach('定位类型:{}; 定位值:{}'.format(selector.split('=>')[0], selector.split('=>')[1]), "操作信息")
            el = self.find_element(selector)
            self.driver.switch_to.frame(el)
            logger.info('switch to iframe el:{}'.format(selector))

    @allure.step("退出iframe")
    def quit_iframe(self):
        """退出iframe"""
        self.driver.switch_to.default_context()
        logger.info('quit iframe')


class UploadFile(object):
    """
    上传文件， 通过将文件传至剪切板后上传窗体中粘贴实现选择文件
    """
    # PyUserInput写法（linux无界面无法使用）
    k = PyKeyboard()

    # pynput写法
    # k = Controller()

    @allure.step("按下按键")
    def keyDown(self, key_name):
        """
        按下按键
        :param key_name: 按下键可选
        :return:
        """
        allure.attach('按键值:{}'.format(key_name), "操作信息")
        try:
            # PyUserInput写法（linux无界面无法使用）
            if key_name[0] == 'f':
                self.k.press_key(self.k.function_keys[int(key_name.lstrip(key_name[0]))])
            elif key_name == 'enter':
                self.k.press_key(self.k.enter_key)
            elif key_name == 'ctrl':
                self.k.press_key(self.k.control_key)
            elif key_name == 'tab':
                self.k.press_key(self.k.tab_key)
            else:
                self.k.press_key(key_name)
            logger.info('press key {}'.format(key_name))

            # pynput写法
            # if key_name[0] == 'f':
            #     if key_name == 'f1':
            #         self.k.press(getattr(Key, key_name))
            # elif key_name == 'enter':
            #     self.k.press(Key.enter)
            # elif key_name == 'ctrl':
            #     self.k.press(Key.ctrl)
            # elif key_name == 'tab':
            #     self.k.press(Key.tab)
            # else:
            #     self.k.press_key(key_name)
            # logger.info('press key {}'.format(key_name))
        except Exception as e:
            logger.info('未按下' + key_name + '键')
            raise e

    @allure.step("抬起按键")
    def keyUp(self, key_name):
        """
        抬起按键
        :param key_name: 按下键可选：enter、ctrl、v
        :return:
        """
        allure.attach('按键值:{}'.format(key_name), "操作信息")
        try:
            # PyUserInput写法（linux无界面无法使用）
            if key_name[0] == 'f':
                self.k.release_key(self.k.function_keys[int(key_name.lstrip(key_name[0]))])
            elif key_name == 'enter':
                self.k.release_key(self.k.enter_key)
            elif key_name == 'ctrl':
                self.k.release_key(self.k.control_key)
            elif key_name == 'tab':
                self.k.release_key(self.k.tab_key)
            else:
                self.k.release_key(key_name)
            logger.info('press key {}'.format(key_name))

            # pynput写法
            # if key_name[0] == 'f':
            #     if key_name == 'f1':
            #         self.k.release(getattr(Key, key_name))
            # elif key_name == 'enter':
            #     self.k.release(Key.enter)
            # elif key_name == 'ctrl':
            #     self.k.release(Key.ctrl)
            # elif key_name == 'tab':
            #     self.k.release(Key.tab)
            # else:
            #     self.k.release(key_name)
            # logger.info('press key {}'.format(key_name))
        except Exception as e:
            logger.info('未松开' + key_name + '键')
            raise e

    @allure.step("模拟单个按键")
    def oneKey(self, key_name, n=1, i=1):
        """
        模拟单个按键
        :param key_name: 按下键
        :param n: 次数
        :param i: 间隔
        :return:
        """
        allure.attach('按键值:{}'.format(key_name), "操作信息")
        try:
            # PyUserInput写法（linux无界面无法使用）
            if key_name[0] == 'f':
                self.k.tap_key(self.k.function_keys[int(key_name.lstrip(key_name[0]))], n, i)
            elif key_name == 'enter':
                self.k.tap_key(self.k.enter_key, n, i)
            elif key_name == 'ctrl':
                self.k.tap_key(self.k.control_key, n, i)
            elif key_name == 'tab':
                self.k.tap_key(self.k.tab_key, n, i)
            else:
                self.k.tap_key(key_name, n, i)

            # pynput写法
            # if key_name[0] == 'f':
            #     if key_name == 'f1':
            #         self.k.tap(getattr(Key, key_name))
            # elif key_name == 'enter':
            #     self.k.tap(Key.enter)
            # elif key_name == 'ctrl':
            #     self.k.tap(Key.ctrl)
            # elif key_name == 'tab':
            #     self.k.tap(Key.tab)
            # else:
            #     self.k.tap(key_name)
            # logger.info('tap key {}'.format(key_name))
        except Exception as e:
            logger.info('未敲击' + key_name + '键')
            raise e

    @allure.step("模拟组合按键")
    def twoKeys(self, key1, key2):
        """
        模拟组合按键， 模拟ctrl+v， key1传ctrl，key2传v
        :param key1: 按下键可选
        :param key2: 按下键可选
        :return:
        """
        allure.attach('按键值1:{}; 按键值1:{}'.format(key1, key2), "操作信息")
        # PyUserInput写法（linux无界面无法使用）
        # self.keyDown(key1)
        # self.keyDown(key2)
        # self.keyUp(key2)
        # self.keyUp(key1)
        # pynput写法
        with self.k.pressed(getattr(Key, key1)):
            self.oneKey(key2)
        logger.info('tap {},{} together'.format(key1, key2))

    @allure.step("获取剪切板的内容")
    def getText(self):
        """
        获取剪切板的内容
        :return: 返回剪切板第一个内容
        """
        value = pyperclip.paste()
        allure.attach('获取内容为:{}'.format(value), "操作信息")
        logger.info('clip value:{}'.format(value))
        return value

    @allure.step("设置剪切板的内容")
    def setText(self, value):
        """
        设置剪切板的内容
        :param value: 上传文件路径
        :return:
        """
        allure.attach('设置内容为:{}'.format(value), "操作信息")
        pyperclip.copy(value)
        logger.info('set clip value:{}'.format(value))

    @allure.step("上传文件")
    def upload_file(self, file_path, file_name):
        """
        通过将文件路径设置至剪切板，在上传窗体依次进行ctrl+v、enter的模拟键盘操作，实现选择文件、确认操作
        :param file_path: 文件路径，结尾不要有分隔符
        :param file_name: 文件名
        :return:
        """
        allure.attach('上传文件为:{}'.format(file_path), "操作信息")
        system = sys.platform
        if 'win' in system:
            self.setText(file_path)
            self.oneKey('f4')
            self.twoKeys('ctrl', 'a')
            self.twoKeys('ctrl', 'v')
            self.oneKey('enter')
            self.oneKey('tab', 6, 1)
            self.setText(file_name)
            self.twoKeys('ctrl', 'v')
            self.oneKey('enter')
        else:
            try:
                self.setText(file_path + os.path.sep + file_name)
            except:
                file = file_path + os.path.sep + file_name
                p = Popen(['xsel', '-bi'], stdin=PIPE)
                p.communicate(input=file)
            self.twoKeys('ctrl', 'v')
            self.oneKey('enter')
        logger.info('upload file success file:{}'.format(file_path + os.path.sep + file_name))
