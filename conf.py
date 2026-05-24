from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def conf(browser='chrome'):
    """
    启动浏览器并返回 driver。
    browser 参数：'chrome'（默认）、'edge' 或 'firefox'
    """
    if browser == 'edge':
        q1 = EdgeOptions()
        q1.add_experimental_option('detach', True)
        q1.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Edge(
            service=EdgeService('msedgedriver.exe'), options=q1
        )

    elif browser == 'firefox':
        q1 = FirefoxOptions()
        # Firefox 不支持 detach，用环境变量保持浏览器打开
        # 测试结束后由 driver.quit() 手动关闭，行为与 Chrome/Edge 一致
        driver = webdriver.Firefox(
            service=FirefoxService('geckodriver.exe'), options=q1
        )

    else:  # chrome（默认）
        q1 = ChromeOptions()
        q1.add_experimental_option('detach', True)
        q1.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(
            service=ChromeService('chromedriver.exe'), options=q1
        )

    driver.implicitly_wait(10)
    return driver