import requests
from playwright.sync_api import sync_playwright


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
    if response.json()["code"] == "200":  # 根据实际返回判断成功条件
        print("登录成功!")
        return session.cookies.get_dict()  # 返回 Cookies
    else:
        print("登录失败!", response.text)
        return None


def setup_playwright(cookies):
    """
    设置 Playwright 上下文并返回 Browser 和 Page 对象
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)  # 设置为 True 启用无头模式
    context = browser.new_context()

    # 添加 JSESSIONID Cookie
    if "JSESSIONID" in cookies:
        context.add_cookies([{
            "name": "JSESSIONID",
            "value": cookies["JSESSIONID"],
            "domain": "192.168.88.130",  # 修改为实际的域名/IP
            "path": "/",
            "httpOnly": True,
            "secure": False  # 如果是 HTTPS，需设为 True
        }])
    else:
        print("JSESSIONID 未找到，无法设置 Cookie！")
        return None, None, None

    # 打开新页面并访问主界面
    page = context.new_page()
    url = "http://192.168.88.130:8080/cms/manage/index.do"
    page.goto(url)

    return playwright, browser, page
