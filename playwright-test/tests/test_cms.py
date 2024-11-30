import pytest
from pages.cms_page import CMSPage
from playwright.sync_api import Page


class TestCMS:
    @pytest.fixture(scope="class")
    def set_up(self):
        """
        Fixture 初始化 CMSPage，并在类级别共享
        """
        self.cms_page = CMSPage(username="admin", password="123456")
        yield self.cms_page

    def test_example(self):
        """
        示例测试用例
        """
        self.cms_page = CMSPage(Page, username="admin", password="123456")
        self.cms_page.page.get_by_text("用户中心").click()
        self.cms_page.page.get_by_role("link", name="用户管理").click()
        print(self.cms_page.page.url)
