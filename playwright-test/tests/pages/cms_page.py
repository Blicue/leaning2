from playwright.sync_api import Page
from models.cms_login import login_and_get_cookies, setup_playwright


class CMSPage:
    def __init__(self, page: Page, username="admin", password="123456"):
        self.username = username
        self.password = password
        self.page = None
        self.playwright = None
        self.browser = None
        self.frame = None
        self.page = self._initialize_context()

    def _initialize_context(self):
        """
        登录并初始化 Playwright 上下文和页面
        """
        cookies = login_and_get_cookies(self.username, self.password)
        if not cookies:
            raise Exception("登录失败，无法初始化 CMSPage！")
        self.playwright, self.browser, self.page = setup_playwright(cookies)

        # 跳转到首页
        url = "http://192.168.88.130:8080/cms/manage/index.do"
        self.page.goto(url)
        return self.page

