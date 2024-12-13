import pytest
import requests
import os
import shutil
from playwright.sync_api import sync_playwright, Page, Browser


# 登录函数
def login_and_get_cookies(username, password):
    """
    使用 requests 登录并获取 Cookies
    """
    session = requests.Session()
    login_url = "http://192.168.88.130:8080/cms/manage/loginJump.do"
    data = {
        "userAccount": username,
        "loginPwd": password
    }
    response = session.post(login_url, data=data)
    if response.json().get("code") == "200":
        print("登录成功!")
        return session.cookies.get_dict()  # 返回 Cookies
    else:
        print("登录失败!", response.text)
        return None


@pytest.fixture(scope="session")
def cookies():
    """
    会话级别的 Cookies Fixture
    """
    username = "admin"
    password = "123456"
    return login_and_get_cookies(username, password)


@pytest.fixture(scope="session")
def playwright_instance():
    """
    会话级别的 Playwright Fixture
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """
    会话级别的 Browser 实例
    浏览器会话将在所有用例执行完毕后关闭
    """
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


def clear_reports():
    """
    清除 reports 下的视频和截图文件
    """
    video_dir = "reports/videos"
    screenshot_dir = "reports/screenshot"

    # 删除视频目录下的所有文件
    if os.path.exists(video_dir):
        for file in os.listdir(video_dir):
            file_path = os.path.join(video_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # 删除截图目录下的所有文件
    if os.path.exists(screenshot_dir):
        for file in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


@pytest.fixture(scope="session")
def page(browser, cookies):
    """
    会话级别的 Page fixture
    所有用例共享一个 Page，执行完后返回首页
    """

    # 清理 reports 下的视频和截图文件
    clear_reports()

    # 确保视频和截图保存目录存在
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("reports/screenshot", exist_ok=True)

    # 创建上下文时使用 record_video 配置
    context = browser.new_context(
        record_video_dir="reports/videos",  # 视频保存路径
    )

    # 将 Cookies 添加到上下文
    if cookies and "JSESSIONID" in cookies:
        context.add_cookies([{
            "name": "JSESSIONID",
            "value": cookies["JSESSIONID"],
            "domain": "192.168.88.130",
            "path": "/",
            "httpOnly": True,
            "secure": False  # 如果是 HTTPS，需设为 True
        }])
    else:
        raise RuntimeError("无法设置 Cookies，因为未成功登录！")

    # 打开页面并访问主界面
    page = context.new_page()
    url = "http://192.168.88.130:8080/cms/manage/index.do"
    page.goto(url)

    yield page

    # 每个用例结束后都回到首页
    page.reload()

    # 截图保存路径
    screenshot_path = "reports/screenshot/test_screenshot.png"  # 可以根据需要调整文件名
    page.screenshot(path=screenshot_path)

    # 获取视频路径
    if page.video:
        video_path = page.video.path()
        print(f"视频保存路径：{video_path}")
    else:
        print("没有录制视频！")

    # 关闭上下文
    context.close()
