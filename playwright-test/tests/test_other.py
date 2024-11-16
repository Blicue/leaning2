from pages.other_page import otherPage
from playwright.sync_api import Page
import pytest


class TestOther:
    @pytest.mark.parametrize("run", range(1))
    def test_other(self, page: Page, run):
        self.other_page = otherPage(page)
        self.other_page.page.goto("https://shikai.info/message-board")
        self.other_page.page.locator("base-comment-item").get_by_role("img").first.click()
