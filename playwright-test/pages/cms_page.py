from playwright.sync_api import Page


class CMSPage:
    def __init__(self, page: Page):
        """
        初始化 CMSPage
        :param page: 已登录并导航到 CMS 页面主界面的 Playwright Page 对象
        """
        self.page = page
        # 定位主框架
        self.main_frame = self.page.locator("iframe[name=\"\\/cms\\/manage\\/user-list\\.html\"]").content_frame
        self.user_add_frame = self.main_frame.locator("iframe[name=\"xubox_iframe1\"]").content_frame

    def navigate_to_user_management(self):
        """
        导航到用户管理页面
        """
        self.page.get_by_text("用户中心").click()
        self.page.get_by_role("link", name="用户管理").click()

    def add_user(self, username, sex, phone, email, login_account, password):
        """
        添加用户
        username: 用户名
        sex: 性别
        phone: 手机号
        email: 邮箱
        login_account: 登录帐号
        password: 密码
        """
        self.main_frame.get_by_role("link", name="添加用户").click()
        self.user_add_frame.get_by_placeholder("用户姓名").click()
        self.user_add_frame.get_by_placeholder("用户姓名").fill(username)
        self.user_add_frame.get_by_label(sex).check()
        self.user_add_frame.get_by_placeholder("手机号码").click()
        self.user_add_frame.get_by_placeholder("手机号码").fill(phone)
        self.user_add_frame.get_by_placeholder("邮箱").click()
        self.user_add_frame.get_by_placeholder("邮箱").fill(email)
        self.user_add_frame.get_by_placeholder("登录帐号").click()
        self.user_add_frame.get_by_placeholder("登录帐号").fill(login_account)
        self.user_add_frame.get_by_placeholder("登录密码").click()
        self.user_add_frame.get_by_placeholder("登录密码").fill(password)
        self.user_add_frame.get_by_placeholder("确认密码").click()
        self.user_add_frame.get_by_placeholder("确认密码").fill(password)
        self.user_add_frame.get_by_role("button", name="确定").click()

    def delete_user(self, username):
        """
        删除用户
        username: 用户名
        """
        path = f"//tr[@class='text-c' and .//u[text()='{username}']]"
        self.main_frame.locator(path).get_by_role("link").nth(3).click()
        self.main_frame.get_by_role("link", name="确定").click()

    def ban_user(self, username):
        """
        停用用户
        username: 用户名
        """
        path = f"//tr[@class='text-c' and .//u[text()='{username}']]"
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
        path = f"//tr[@class='text-c' and .//u[text()='{username}']]"
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
