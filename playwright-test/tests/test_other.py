from pages.other_page import otherPage
from playwright.sync_api import Page
import pytest


class TestOther:
    @pytest.mark.skip(reason="已使用完毕")
    def test_other(self, page: Page):
        self.other_page = otherPage(page)
        self.other_page.page.goto("https://shikai.info/message-board")
        self.other_page.page.locator("base-comment-item").get_by_role("img").first.click()
    
    @pytest.mark.skip(reason="已使用完毕")
    def test_1(self, page: Page):
        self.other_page = otherPage(page)
        self.other_page.page.goto("https://docs.dingtalk.com/i/nodes/G53mjyd80p96ExL2TEY1ZYla86zbX04v")
        self.other_page.page.pause()
