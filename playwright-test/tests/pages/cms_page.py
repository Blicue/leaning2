from playwright.sync_api import Page
from models.cms_login import login_and_get_cookies, setup_playwright


class CMSPage:
    def __init__(self, page: Page, username="admin", password="123456"):
        self.username = username
        self.password = password
        self.page = None
        self.playwright = None
        self.browser = None
        cookies = login_and_get_cookies(self.username, self.password)
        if not cookies:
            raise Exception("登录失败，无法初始化 CMSPage！")
        self.playwright, self.browser, self.page = setup_playwright(cookies)
        # 跳转到首页
        url = "http://192.168.88.130:8080/cms/manage/index.do"
        self.page.goto(url)
        self.main_frame = self.page.locator("iframe[name=\"\\/cms\\/manage\\/user-list\\.html\"]").content_frame
        self.xubox_frame = self.main_frame.locator("iframe[name=\"xubox_iframe1\"]").content_frame

    def add_user(self, username, gendar, phone, email, login_account ,password):
        """
        添加用户
        username: 用户名
        gendar: 性别
        phone: 手机号
        email: 邮箱
        login_account: 登录帐号
        password: 密码
        """
        self.main_frame.get_by_role("link", name="添加用户").click()
        self.xubox_frame.get_by_placeholder("用户姓名").click()
        self.xubox_frame.get_by_placeholder("用户姓名").fill(username)
        self.xubox_frame.get_by_label(gendar).check()
        self.xubox_frame.get_by_placeholder("手机号码").click()
        self.xubox_frame.get_by_placeholder("手机号码").fill(phone)
        self.xubox_frame.get_by_placeholder("邮箱").click()
        self.xubox_frame.get_by_placeholder("邮箱").fill(email)
        self.xubox_frame.get_by_placeholder("登录帐号").click()
        self.xubox_frame.get_by_placeholder("登录帐号").fill(login_account)
        self.xubox_frame.get_by_placeholder("登录密码").click()
        self.xubox_frame.get_by_placeholder("登录密码").fill(password)
        self.xubox_frame.get_by_placeholder("确认密码").click()
        self.xubox_frame.get_by_placeholder("确认密码").fill(password)
        self.xubox_frame.get_by_role("button", name="确定").click()
        
    def delete_user(self, username):
        """
        删除用户
        username: 用户名
        """
        path = (
            f"//tr[@class='text-c' and .//u[text()='{username}']]"
        )
        self.main_frame.locator(path).get_by_role("link").nth(3).click()
        self.main_frame.get_by_role("link", name="确定").click()

    def ban_user(self, username):
        """
        停用用户
        username: 用户名
        """
        path = (
            f"//tr[@class='text-c' and .//u[text()='{username}']]"
        )
        self.main_frame.locator(path).get_by_role("link").nth(0).click()
        self.main_frame.get_by_role("link", name="确定").click()

    def assert_delete_msg(self):
        """
        断言删除成功
        """
        self.main_frame.get_by_text("已删除!").wait_for(state="visible")
        msg = self.main_frame.get_by_text("已删除!")
        assert msg.is_visible()
        
    def assert_user_exist(self, username):
        """
        断言用户存在
        """
        path = (
            f"//tr[@class='text-c' and .//u[text()='{username}']]"
        )
        self.main_frame.locator(path).wait_for(state="visible")
        userdata = self.main_frame.locator(path)
        assert userdata.is_visible()
        
    def assert_ban_msg(self):
        """
        断言停用成功
        """
        self.main_frame.get_by_text("已停用!").wait_for(state="visible")
        msg = self.main_frame.get_by_text("已停用!")
        assert msg.is_visible()
           