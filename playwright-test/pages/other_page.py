from playwright.sync_api import Page  # 导入Page类型

class otherPage:
    def __init__(self, page: Page):
        self.page = page

