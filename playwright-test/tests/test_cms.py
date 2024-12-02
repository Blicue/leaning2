import pytest
from tests.pages.cms_page import CMSPage


class TestCMS:
    @pytest.fixture(scope="function", autouse=True)
    def setup_page(self, page):
        """
        每个测试用例自动初始化 CMSPage 对象,yield后接清理操作
        """
        self.cms_page = CMSPage(page)
        yield

    def test_add_user(self):
        """
        验证添加用户
        """
        self.cms_page.navigate_to_user_management()
        self.cms_page.add_user("juyunlong", "女", "13144445555", "1234@qq.com", "adminjyl", "123456")
        self.cms_page.assert_user_exist("juyunlong")

    def test_ban_user(self):
        """
        验证停用用户
        """
        self.cms_page.navigate_to_user_management()
        self.cms_page.ban_user("juyunlong")
        self.cms_page.assert_ban_msg()

    def test_delete_user(self):
        """
        验证删除用户
        """
        self.cms_page.navigate_to_user_management()
        self.cms_page.delete_user("juyunlong")
        self.cms_page.assert_delete_msg()
