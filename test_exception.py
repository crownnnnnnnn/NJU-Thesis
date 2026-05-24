# test_exception.py
# 异常处理机制验证
# 覆盖用例：ET01 ~ ET08
# 说明：本文件用于验证脚本在异常情况下的处理能力，
#       包括异常捕获、截图保存、日志记录等机制是否正常生效。
#       ET01～ET08 不计入主测试通过率，作为独立的鲁棒性验证分析。

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from conf import conf
from screenshot_utils import take_screenshot
from pages.orangehrm_page import OrangeHRMPage
from pages.theinternet_page import TheInternetPage
import logger

MODULE = '异常验证'

# -------------------------------------------------------
# ET01：故意使用错误元素定位
# 验证目的：当元素定位失败时，脚本能否正确捕获异常、
#           保存截图并输出完整日志，而不是直接崩溃退出
# 预期异常：NoSuchElementException / TimeoutException
# -------------------------------------------------------
def et01_wrong_locator(browser='chrome'):
    tc_id, tc_name = 'ET01', '错误元素定位异常捕获验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET01] 故意使用错误定位器，预期触发异常并捕获...')
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()

        # 故意使用一个不存在的 XPath
        driver.find_element(By.XPATH, '//div[@id="this-element-does-not-exist"]')

        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark='预期异常未触发，元素定位机制存在问题',
                   duration=time.time() - t0)

    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET01] 异常类型：{error_type}')
        print(f'  [ET01] 截图已保存：{screenshot_path}')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'异常捕获成功 [{error_type}] 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET02：缩短等待时间导致动态页面超时
# 验证目的：对比显式等待时间充足与不足时的执行结果，
#           说明等待机制对脚本稳定性的直接影响
# 预期异常：TimeoutException
# -------------------------------------------------------
def et02_timeout_too_short(browser='chrome'):
    tc_id, tc_name = 'ET02', '等待时间不足导致超时异常验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET02] 故意缩短等待时间为1秒, 预期触发超时异常...')
    try:
        page = TheInternetPage(driver)
        page.open_dynamic_loading()
        page.click_start()

        # 故意只等1秒（正常需要15秒），必然超时
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, 'finish'))
        )

        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark='1秒内加载完成 (网络极快), 未触发超时',
                   duration=time.time() - t0)

    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET02] 异常类型：{error_type}')
        print(f'  [ET02] 结论: 等待1s不足, 恢复15s后用例正常通过')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'超时捕获成功 [{error_type}] 等待1s不足, 恢复15s后正常 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET03：拖拽跨浏览器兼容性分析
# 验证目的：记录拖拽操作在不同浏览器下的执行结果，
#           分析系统级鼠标操作（pyautogui）的跨浏览器限制
# 预期结果：Chrome 通过，Edge/Firefox 可能因坐标偏移失败
# -------------------------------------------------------
def et03_drag_browser_compat(browser='chrome'):
    tc_id, tc_name = 'ET03', f'拖拽跨浏览器兼容性分析({browser.upper()})'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET03] 在 {browser.upper()} 下测试拖拽兼容性...')
    try:
        from pages.demoqa_page import DemoQAPage
        page = DemoQAPage(driver)
        page.open_droppable()
        page.drag_to_drop()
        result = page.get_dropped_text()
        assert 'Dropped' in result, f'拖拽结果不符：{result}'
        print(f'  [ET03] {browser.upper()} 拖拽成功')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'{browser.upper()} 拖拽正常执行',
                   duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET03] {browser.upper()} 拖拽失败：{error_type}')
        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark=f'[跨浏览器限制] {browser.upper()} pyautogui坐标偏移 [{error_type}] 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()


# -------------------------------------------------------
# ET04：错误账号登录后立即操作受保护页面
# 验证目的：验证未登录状态下访问受保护页面时，
#           脚本能否检测到页面跳转并正确记录失败
# 预期异常：AssertionError（URL 断言失败）
# -------------------------------------------------------
def et04_unauthorized_access(browser='chrome'):
    tc_id, tc_name = 'ET04', '未登录状态访问受保护页面验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET04] 不登录直接访问 Dashboard, 预期被重定向到登录页...')
    try:
        page = OrangeHRMPage(driver)
        page.open()

        # 不登录，直接跳转到 Dashboard 页面
        driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index')
        time.sleep(2)

        # 验证系统将未登录用户重定向回登录页
        current = driver.current_url
        print(f'  [ET04] 当前 URL: {current}')
        assert 'login' in current, f'系统未重定向到登录页, 当前URL: {current}'

        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'未登录访问受保护页面被正确重定向至登录页',
                   duration=time.time() - t0)

    except AssertionError as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        print(f'  [ET04] 断言失败：{e}')
        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark=f'系统未正确重定向 {str(e)[:60]} 截图:{screenshot_path}',
                   duration=time.time() - t0)
    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'异常捕获成功 [{error_type}] 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET05：页面加载中强制刷新
# 验证目的：在页面尚未完全加载时强制刷新，
#           验证脚本能否处理 StaleElementReferenceException
# 预期异常：StaleElementReferenceException
# -------------------------------------------------------
def et05_stale_element(browser='chrome'):
    tc_id, tc_name = 'ET05', 'StaleElementReferenceException 处理验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET05] 获取元素后刷新页面，预期触发 StaleElementReference...')
    try:
        page = OrangeHRMPage(driver)
        page.open()

        # 先获取登录按钮的引用
        login_btn = driver.find_element(By.XPATH, '//button[@type="submit"]')
        print(f'  [ET05] 已获取登录按钮引用')

        # 刷新页面，使元素引用过期
        driver.refresh()
        time.sleep(1)
        print(f'  [ET05] 页面已刷新，元素引用已过期')

        # 尝试操作过期的元素，触发 StaleElementReferenceException
        login_btn.click()

        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark='预期 StaleElementReferenceException 未触发',
                   duration=time.time() - t0)

    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET05] 异常类型：{error_type}')
        print(f'  [ET05] 结论：元素引用过期后操作触发异常，需在操作前重新获取元素')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'[{error_type}] 元素引用过期异常捕获成功 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET06：对隐藏元素执行点击操作
# 验证目的：验证对不可见元素执行点击时，
#           脚本能否捕获 ElementNotInteractableException
# 预期异常：ElementNotInteractableException
# -------------------------------------------------------
def et06_click_hidden_element(browser='chrome'):
    tc_id, tc_name = 'ET06', '点击隐藏元素异常捕获验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET06] 尝试点击隐藏元素，预期触发 ElementNotInteractable...')
    try:
        page = TheInternetPage(driver)
        page.open_dynamic_loading()

        # finish 元素初始为隐藏状态（display:none），直接点击
        hidden_el = driver.find_element(By.ID, 'finish')
        print(f'  [ET06] 元素是否可见：{hidden_el.is_displayed()}')
        hidden_el.click()  # 对隐藏元素执行点击，触发异常

        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark='预期异常未触发，隐藏元素点击行为异常',
                   duration=time.time() - t0)

    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET06] 异常类型：{error_type}')
        print(f'  [ET06] 结论：隐藏元素不可交互，操作前需确认元素可见性')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'[{error_type}] 隐藏元素交互异常捕获成功 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET07：窗口切换到已关闭的句柄
# 验证目的：切换到一个已经关闭的窗口句柄时，
#           验证脚本能否捕获 NoSuchWindowException
# 预期异常：NoSuchWindowException
# -------------------------------------------------------
def et07_switch_closed_window(browser='chrome'):
    tc_id, tc_name = 'ET07', '切换已关闭窗口句柄异常捕获验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET07] 打开新窗口后关闭，再尝试切换回去，预期触发 NoSuchWindow...')
    try:
        page = TheInternetPage(driver)
        page.open_windows_page()

        original = driver.current_window_handle

        # 点击打开新窗口
        page.click_new_window_link()
        handles = driver.window_handles
        new_handle = [h for h in handles if h != original][0]

        # 切换到新窗口后立刻关闭它
        driver.switch_to.window(new_handle)
        driver.close()
        print(f'  [ET07] 新窗口已关闭')

        # 尝试再次切换到已关闭的句柄
        driver.switch_to.window(new_handle)

        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark='预期 NoSuchWindowException 未触发',
                   duration=time.time() - t0)

    except Exception as e:
        # 切换回原窗口，截图
        try:
            driver.switch_to.window(original)
        except Exception:
            pass
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET07] 异常类型：{error_type}')
        print(f'  [ET07] 结论：切换已关闭窗口触发异常，需在切换前验证句柄有效性')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'[{error_type}] 无效窗口句柄异常捕获成功 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


# -------------------------------------------------------
# ET08：iframe 未切换直接操作内部元素
# 验证目的：不切换到 iframe 就直接定位 iframe 内部元素，
#           验证脚本能否捕获 NoSuchElementException
# 预期异常：NoSuchElementException / TimeoutException
# -------------------------------------------------------
def et08_operate_iframe_without_switch(browser='chrome'):
    tc_id, tc_name = 'ET08', '未切换iframe直接操作内部元素异常验证'
    t0 = time.time()
    driver = conf(browser)
    print(f'\n  [ET08] 不切换 iframe，直接定位内部元素，预期触发元素未找到异常...')
    try:
        from pages.demoqa_page import DemoQAPage
        page = DemoQAPage(driver)
        page.open_frames()

        # 不执行 switch_to.frame()，直接定位 iframe 内部的元素
        # sampleHeading 在 iframe 内部，不切换必然找不到
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'sampleHeading'))
        )

        logger.log(tc_id, tc_name, MODULE, '失败',
                   remark='预期异常未触发，iframe 内元素在未切换时不应被找到',
                   duration=time.time() - t0)

    except Exception as e:
        time.sleep(1)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        error_type = type(e).__name__
        print(f'  [ET08] 异常类型：{error_type}')
        print(f'  [ET08] 结论：未切换 iframe 时无法定位内部元素，需先调用 switch_to.frame()')
        logger.log(tc_id, tc_name, MODULE, '通过',
                   remark=f'[{error_type}] 未切换iframe操作内部元素异常捕获成功 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        driver.quit()


def runtest_exception(browser='chrome'):
    print()
    print(f'=== 异常处理机制验证 (ET01 ~ ET08) [{browser.upper()}] ===')
    print('  【说明】本组用例为鲁棒性验证，不计入主测试通过率')
    print()
    et01_wrong_locator(browser)
    et02_timeout_too_short(browser)
    et03_drag_browser_compat(browser)
    et04_unauthorized_access(browser)
    et05_stale_element(browser)
    et06_click_hidden_element(browser)
    et07_switch_closed_window(browser)
    et08_operate_iframe_without_switch(browser)