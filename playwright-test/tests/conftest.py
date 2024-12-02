import pytest
import requests
from playwright.sync_api import sync_playwright


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
    if response.json().get("code") == "200":  # 根据实际返回判断成功条件
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
    username = "admin"  # 替换为实际的用户名
    password = "123456"  # 替换为实际的密码
    return login_and_get_cookies(username, password)


@pytest.fixture(scope="session")
def playwright_instance():
    """
    会话级别的 Playwright Fixture
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
def browser(playwright_instance):
    """
    每个用例启动一个新的 Browser 实例
    """
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser, cookies):
    """
    每个用例启动一个新的 Page，并自动登录
    """
    context = browser.new_context()

    # 将 Cookies 添加到上下文
    if cookies and "JSESSIONID" in cookies:
        context.add_cookies([{
            "name": "JSESSIONID",
            "value": cookies["JSESSIONID"],
            "domain": "192.168.88.130",  # 修改为实际的域名/IP
            "path": "/",
            "httpOnly": True,
            "secure": False  # 如果是 HTTPS，需设为 True
        }])
    else:
        raise RuntimeError("无法设置 Cookies，因为未成功登录！")

    # 打开新页面并访问主界面
    page = context.new_page()
    url = "http://192.168.88.130:8080/cms/manage/index.do"
    page.goto(url)

    yield page

    # 关闭上下文
    context.close()
