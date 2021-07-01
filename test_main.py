import os
from datetime import date
import pytest
from framework.browser_engine import BrowserEngine
from framework.base_page import BasePage, UploadFile
from framework.send_email import send_email
import json
import allure
import win32gui
import win32con


with open(os.getcwd() + "/config/url_info.json", encoding='utf-8') as f:
    load_dict = json.load(f)


@allure.feature('验证演示环境各链接是否活跃')
class TestClass(object):
    @classmethod
    def setup_method(cls):
        cls.browser = BrowserEngine()
        cls.driver = BasePage(cls.browser.driver)

    @classmethod
    def teardown_method(cls):
        cls.driver.quit_browser()

    def test_upload(self):
        url = '''https://element-plus.gitee.io/#/zh-CN/component/upload'''
        btn = "x=>/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div[1]/section/div[1]/div[1]/div/div/div[1]/button"
        file_path = r'C:\Users\tianchenxu\Desktop'
        file_name = '111.txt'
        assert_element = "x=>/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div[1]/section/div[1]/div[1]/div/div/ul/li[3]/a"
        assert_str = "111.txt"
        self.browser.open_browser(url)
        self.driver.wait_element(20, 1, btn)
        self.driver.click(btn)
        # 强制等待 不然窗体未完全加载粘贴会失败
        self.driver.sleep(3)
        upload = UploadFile()
        upload.upload_file(file_path, file_name)
        # 强制等待 等待文件上传完毕
        self.driver.sleep(3)
        actual_str = self.driver.get_element_text(assert_element)
        with allure.step("断言结果"):
            allure.attach('期望结果:{}; 实际结果:{}'.format(assert_str, actual_str), "断言结论")
            assert assert_str in actual_str, "failed!!! 预期结果:{}; 与实际结果不符:{}".format(assert_str, actual_str)



    # def str_split(self, s):
    #     t = s.split('=>')[0]
    #     v = s.split('=>')[1]
    #     return t, v
    #
    # def verify(self, index, username, pwd, btn, ass_el):
    #     username_type, username_value = self.str_split(username)
    #     pwd_type, pwd_value = self.str_split(pwd)
    #     btn_type, btn_value = self.str_split(btn)
    #     username_text = load_dict[index]['account']
    #     pwd_text = load_dict[index]['pwd']
    #     assert_element = ass_el
    #     assert_element_type, assert_element_value = self.str_split(assert_element)
    #     assert_str = load_dict[index]['assert_str']
    #     '''
    #         注意：
    #         不直接使用变量driver作为wait_element()中driver参数，因为browser.driver为原始webDriver类型,变量driver类型为BasePage,
    #         调用后续方法是会有限从内部方法中选取，内部存在find_element()时会与selenium库中方法冲突!!!
    #     '''
    #     self.browser.open_browser(load_dict[index]['url'])
    #     wait_element(self.browser.driver, 20, 1, username_type, username_value)
    #     self.driver.clear(username)
    #     self.driver.enter(username, username_text)
    #     wait_element(self.browser.driver, 20, 1, pwd_type, pwd_value)
    #     self.driver.clear(pwd)
    #     self.driver.enter(pwd, pwd_text)
    #     wait_element(self.browser.driver, 20, 1, btn_type, btn_value)
    #     self.driver.click(btn)
    #     wait_element(self.browser.driver, 30, 1, assert_element_type, assert_element_value)
    #     actual_str = self.driver.get_element_text(assert_element)
    #     with allure.step("断言结果"):
    #         allure.attach('期望结果:{}; 实际结果:{}'.format(assert_str, actual_str), "断言结论")
    #         assert assert_str in actual_str, "failed!!! 预期结果:{}; 与实际结果不符:{}".format(assert_str, actual_str)
    #
    # @allure.story(load_dict[0]['name'])
    # def test_subject_demo(self):
    #     username = 'n=>username'
    #     pwd = 'n=>userpass'
    #     btn = 'c=>login-form-btn'
    #     assert_element = 'c=>logo'
    #     self.verify(0, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[1]['name'])
    # def test_Northwest_University_demo(self):
    #     username = 'n=>username'
    #     pwd = 'n=>userpass'
    #     btn = 'c=>login-form-btn'
    #     assert_element = 'x=>/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/span'
    #     self.verify(1, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[2]['name'])
    # def test_Nankai_University_demo(self):
    #     username = 'n=>username'
    #     pwd = 'n=>userpass'
    #     btn = 'c=>login-form-btn'
    #     assert_element = 'x=>/html/body/div[1]/div[1]/div/div[1]/div/div/ul/li[1]/a/span/span[2]'
    #     self.verify(2, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[3]['name'])
    # def test_China_Public_Security_University_demo(self):
    #     username = 'x=>/html/body/div/div/div/div[2]/div/form/div[1]/div/div[1]/input'
    #     pwd = 'x=>/html/body/div/div/div/div[2]/div/form/div[2]/div/div[1]/input'
    #     btn = 'x=>/html/body/div/div/div/div[2]/div/div/div/button'
    #     assert_element = 'x=>/html/body/div/div[1]/div/div[1]/div/div/ul/li[1]/a/span/span[2]'
    #     self.verify(3, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[4]['name'])
    # def test_claim_demo(self):
    #     username = 'n=>form[user_name]'
    #     pwd = 'n=>form[user_pwd]'
    #     btn = 'c=>login-btn'
    #     assert_element = 'x=>/html/body/div[2]/div/ul/li[1]/a'
    #     self.verify(4, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[5]['name'])
    # def test_Academic_libraries_demo(self):
    #     username = 'x=>/html/body/div/div[2]/div/div/div/div[2]/form/div[1]/input'
    #     username_type, username_value = self.str_split(username)
    #     username_text = load_dict[5]['account']
    #     pwd = 'x=>/html/body/div[1]/div[2]/div/div/div/div[2]/form/div[2]/input'
    #     pwd_type, pwd_value = self.str_split(pwd)
    #     pwd_text = load_dict[5]['pwd']
    #     btn = 'x=>/html/body/div/div[2]/div/div/div/div[2]/form/button'
    #     btn_type, btn_value = self.str_split(btn)
    #     self.browser.open_browser(load_dict[5]['url'])
    #     login_a = 'c=>sign-in'
    #     login_a_type, login_a_value = self.str_split(login_a)
    #     wait_element(self.browser.driver, 30, 1, login_a_type, login_a_value)
    #     self.driver.click(login_a)
    #     pwd_login_a = 's=>a[href="#password"]'
    #     pwd_login_a_type, pwd_login_a_value = self.str_split(pwd_login_a)
    #     wait_element(self.browser.driver, 30, 1, pwd_login_a_type, pwd_login_a_value)
    #     self.driver.es("arguments[0].click();", pwd_login_a)
    #     wait_element(self.browser.driver, 20, 1, username_type, username_value)
    #     self.driver.es("$('#username1').val('" + username_text + "');")
    #     wait_element(self.browser.driver, 20, 1, pwd_type, pwd_value)
    #     self.driver.es("$('#passwd1').val('" + pwd_text + "');")
    #     wait_element(self.browser.driver, 20, 1, btn_type, btn_value)
    #     self.driver.es("arguments[0].click();", btn)
    #     self.browser.open_browser(load_dict[5]['url'])
    #     assert_element = 'x=>/html/body/div[1]/div[1]/div[1]/div/span/span/a'
    #     assert_element_type, assert_element_value = self.str_split(assert_element)
    #     assert_str = load_dict[5]['assert_str']
    #     wait_element(self.browser.driver, 30, 1, assert_element_type, assert_element_value)
    #     actual_str = self.driver.get_element_text(assert_element)
    #     with allure.step("断言结果"):
    #         allure.attach('期望结果:{}; 实际结果:{}'.format(assert_str, actual_str), "断言结论")
    #         assert assert_str in actual_str, "failed!!! 预期结果:{}; 与实际结果不符:{}".format(assert_str, actual_str)
    #
    # @allure.story(load_dict[6]['name'])
    # def test_Academic_map_demo(self):
    #     assert_element = 'c=>logo'
    #     assert_element_type, assert_element_value = self.str_split(assert_element)
    #     assert_str = load_dict[6]['assert_str']
    #     self.browser.open_browser(load_dict[6]['url'])
    #     wait_element(self.browser.driver, 30, 1, assert_element_type, assert_element_value)
    #     actual_str = self.driver.get_element_text(assert_element)
    #     with allure.step("断言结果"):
    #         allure.attach('期望结果:{}; 实际结果:{}'.format(assert_str, actual_str), "断言结论")
    #         assert assert_str in actual_str, "failed!!! 预期结果:{}; 与实际结果不符:{}".format(assert_str, actual_str)
    #
    # @allure.story(load_dict[7]['name'])
    # def test_Research_assistant_demo(self):
    #     username = 'x=>/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/div[1]/input'
    #     pwd = 'x=>/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/div[2]/input'
    #     btn = 'x=>/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/button'
    #     assert_element = 'x=>/html/body/div[1]/div[1]/div/a'
    #     self.verify(7, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[8]['name'])
    # def test_Traditional_Chinese_Medicine_University_Of_Guangzhou_demo(self):
    #     username = 'x=>/html/body/div[1]/div/div[1]/div[2]/div/form/div[1]/div/div[1]/input'
    #     pwd = 'x=>/html/body/div[1]/div/div[1]/div[2]/div/form/div[2]/div/div[1]/input'
    #     btn = 'x=>/html/body/div/div/div[1]/div[2]/div/div/div/button'
    #     assert_element = 'x=>/html/body/div[1]/div[1]/div[2]/div[2]/ul/li[1]/div/span/a'
    #     self.verify(8, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[9]['name'])
    # def test_Beijing_Institute_of_Technology_demo(self):
    #     username = 'x=>/html/body/div/div/div[1]/div[2]/div/form/div[1]/div/div[1]/input'
    #     pwd = 'x=>/html/body/div/div/div[1]/div[2]/div/form/div[2]/div/div[1]/input'
    #     btn = 'x=>/html/body/div/div/div[1]/div[2]/div/div/div/button/span/span'
    #     assert_element = 'x=>/html/body/div[1]/div[2]/div[1]/div/ul/li[1]/a'
    #     self.verify(9, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[10]['name'])
    # def test_Beijing_University_of_Posts_and_Telecommunications_demo(self):
    #     username = 'n=>username'
    #     pwd = 'n=>userpass'
    #     btn = 'c=>login-form-btn'
    #     assert_element = 'c=>header-left'
    #     self.verify(10, username, pwd, btn, assert_element)
    #
    # @allure.story(load_dict[11]['name'])
    # def test_Sichuan_Vocational_College_of_Mechanical_and_Electrical_Technology_demo(self):
    #     username = 'n=>username'
    #     pwd = 'n=>userpass'
    #     btn = 'c=>login-form-btn'
    #     assert_element = 'c=>head_litterTitle'
    #     self.verify(11, username, pwd, btn, assert_element)


if __name__ == '__main__':
    rq = str(date.today())
    html_file = os.path.dirname(os.path.realpath(__file__)) + '/html/' + rq + "演示环境测试报告.html"
    '''
        "-v" 显示详细信息
        "-q" 显示简要信息与-v相反
        "-l" 显示失败用例详细信息（堆栈中局部变量及值）
        "-m 【标记名称】" 只执行对应标记测试用例配合装饰器@pytest.mark.【标记名称】进行使用
        "-x" 遇到用例失败直接结束执行，debug必备
        "-s" 打印print函数输出
    '''
    pytest.main(["-q", "test_main.py", "--html=" + html_file, "--self-contained-html", "--alluredir=./result"])
    try:
        send_email(html_file)
        print("发送成功")
    except Exception as e:
        print("发送失败", e)
