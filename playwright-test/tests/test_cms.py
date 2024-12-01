import pytest
from pages.cms_page import CMSPage
from playwright.sync_api import Page


class TestCMS:
    @pytest.fixture(scope="function")
    def set_up(self):
        """
        Fixture 初始化 CMSPage，并在类级别共享
        """
        self.cms_page = CMSPage(Page)
        yield self.cms_page

    def test_add_user(self, set_up):
        """
        验证添加用户
        """
        set_up
        # 进入用户中心用户管理页面
        self.cms_page.page.get_by_text("用户中心").click()
        self.cms_page.page.get_by_role("link", name="用户管理").click()
        # 执行添加用户操作
        self.cms_page.add_user("juyunlong", "女", "13144445555", "1234@qq.com", "adminjyl", "123456")
        self.cms_page.assert_user_exist("juyunlong")
    
    def test_ban_user(self, set_up):
        """
        验证停用用户
        """
        set_up
        # 进入用户中心用户管理页面
        self.cms_page.page.get_by_text("用户中心").click()
        self.cms_page.page.get_by_role("link", name="用户管理").click()
        # 执行停用用户操作
        self.cms_page.ban_user("juyunlong")
        self.cms_page.assert_ban_msg()
           
    def test_delete_user(self, set_up):
        """
        验证删除用户
        """
        set_up
        # 进入用户中心用户管理页面
        self.cms_page.page.get_by_text("用户中心").click()
        self.cms_page.page.get_by_role("link", name="用户管理").click()
        # 执行删除用户操作
        self.cms_page.delete_user("juyunlong")
        self.cms_page.assert_delete_msg()
        
        
        
