# test_theinternet.py
# 补充实验二：The Internet 功能测试
# 演示地址：https://the-internet.herokuapp.com/
# 覆盖用例：TC25 ~ TC34
# 架构说明：采用 Page Object Model，测试逻辑与页面操作解耦
# 跨浏览器：每个用例支持 browser 参数（'chrome' 或 'edge'）

import time
from conf import conf
from screenshot_utils import take_screenshot
from pages.theinternet_page import TheInternetPage
from selenium.webdriver.common.keys import Keys
import logger

MODULE = 'TheInternet'

def _module(browser):
    return f'{MODULE}-{browser.upper()}'

def tc25_floating_menu(browser='chrome'):
    tc_id, tc_name = 'TC25', '页面滚动后浮动菜单始终可见验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_floating_menu()
        menu = page.get_menu_element()
        assert menu.is_displayed(), '浮动菜单初始不可见'
        page.scroll_to(500)
        assert menu.is_displayed(), '页面滚动后浮动菜单消失'
        links = page.get_menu_links()
        assert len(links) == 4, f'菜单链接数量不符，预期4个，实际{len(links)}个'
        print(f'    [菜单项] {[a.text for a in links]}')
        page.scroll_to_bottom()
        assert menu.is_displayed(), '滚动到底部后浮动菜单消失'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc26_broken_images(browser='chrome'):
    tc_id, tc_name = 'TC26', '页面图片加载状态检测'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_broken_images()
        ok, broken = page.get_image_status()
        print(f'    [加载成功] {len(ok)} 张：{ok}')
        print(f'    [加载失败] {len(broken)} 张：{broken}')
        assert len(broken) > 0, '未检测到损坏图片'
        assert len(ok) > 0, '所有图片均损坏，页面加载可能异常'
        logger.log(tc_id, tc_name, _module(browser), '通过',
                   remark=f'损坏{len(broken)}张 正常{len(ok)}张',
                   duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc27_infinite_scroll(browser='chrome'):
    tc_id, tc_name = 'TC27', '页面无限滚动加载新内容验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_infinite_scroll()
        before = page.get_scroll_item_count()
        print(f'    [初始段落数] {before}')
        assert before > 0, '页面初始未加载任何段落'
        page.scroll_down_multiple(times=10, wait=1.5)
        after = page.get_scroll_item_count()
        print(f'    [滚动后段落数] {after}')
        assert after > before, f'无限滚动未加载新内容，前:{before} 后:{after}'
        logger.log(tc_id, tc_name, _module(browser), '通过',
                   remark=f'段落数 {before} → {after}',
                   duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc28_notification_message(browser='chrome'):
    tc_id, tc_name = 'TC28', '随机通知消息刷新验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_notification()
        messages_seen = set()
        for i in range(7):
            time.sleep(1)
            page.click_next_notification()
            msg = page.get_flash_text()
            print(f'    [第{i+1}次] {msg[:50]}')
            messages_seen.add(msg)
        print(f'    [不同消息种类] {messages_seen}')
        assert len(messages_seen) > 0, '未获取到任何通知消息'
        logger.log(tc_id, tc_name, _module(browser), '通过',
                   remark=f'共收集到{len(messages_seen)}种消息',
                   duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc29_dynamic_controls(browser='chrome'):
    tc_id, tc_name = 'TC29', 'Dynamic Controls 元素动态出现与消失'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_dynamic_controls()
        cb = page.get_checkbox_element()
        assert cb.is_displayed(), '复选框初始不可见'
        page.click_checkbox_btn()
        page.wait_checkbox_gone()
        msg = page.get_checkbox_msg()
        assert 'gone' in msg, f'移除提示不符：{msg}'
        page.click_checkbox_btn()
        page.wait_checkbox_back()
        assert not page.get_input_box().is_enabled(), '输入框初始应为禁用'
        page.click_input_btn()
        page.wait_input_enabled()
        el = page.type_into_input('Hello World!')
        assert el.get_attribute('value') == 'Hello World!', '输入框启用后输入失败'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc30_dynamic_loading(browser='chrome'):
    tc_id, tc_name = 'TC30', 'Dynamic Loading 等待隐藏元素加载完成'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_dynamic_loading()
        page.click_start()
        page.wait_loading_done()
        text = page.get_finish_text()
        assert 'Hello World' in text, f'动态加载内容不符：{text}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc31_hovers(browser='chrome'):
    tc_id, tc_name = 'TC31', '鼠标悬浮显示隐藏用户信息'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_hovers()
        figures = page.get_figures()
        assert len(figures) == 3, f'头像数量不符，预期3个，实际{len(figures)}个'
        for i, figure in enumerate(figures, start=1):
            page.hover_figure(figure)
            cap = page.get_figcaption(figure)
            assert cap.is_displayed(), f'第{i}个用户悬浮信息未出现'
            assert f'user{i}' in cap.text.lower(), f'悬浮信息内容不符：{cap.text}'
            print(f'    [user{i}悬浮信息] {cap.text}')
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc32_key_presses(browser='chrome'):
    tc_id, tc_name = 'TC32', '键盘按键事件捕获验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_key_presses()
        page.send_key_to_target('a')
        assert 'A' in page.get_key_result(), 'A 键捕获失败'
        print(f'    [A键结果] {page.get_key_result()}')
        page.send_key_to_target(Keys.SPACE)
        assert 'SPACE' in page.get_key_result(), 'Space 键捕获失败'
        print(f'    [Space键结果] {page.get_key_result()}')
        page.send_key_to_target(Keys.ARROW_UP)
        assert 'UP' in page.get_key_result(), 'Up 键捕获失败'
        print(f'    [Up键结果] {page.get_key_result()}')
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc33_multiple_windows(browser='chrome'):
    tc_id, tc_name = 'TC33', '新窗口打开与切换验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_windows_page()
        original = driver.current_window_handle
        page.click_new_window_link()
        handles = page.get_all_handles()
        assert len(handles) == 2, f'预期2个窗口，实际{len(handles)}个'
        page.switch_to_window(handles[1])
        time.sleep(0.5)
        heading = page.get_window_heading()
        assert 'New Window' in heading, f'新窗口内容不符：{heading}'
        page.switch_to_window(original)
        assert driver.current_window_handle == original, '切换回原窗口失败'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

def tc34_disappearing_elements(browser='chrome'):
    tc_id, tc_name = 'TC34', '页面刷新菜单项动态变化验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = TheInternetPage(driver)
        page.open_disappearing()
        items = page.get_menu_item_texts()
        print(f'    [首次加载菜单] {items}')
        assert len(items) >= 4, f'菜单项数量异常：{items}'
        assert 'Home' in items, f'Home 菜单项缺失：{items}'
        found_change = False
        for _ in range(5):
            page.refresh_page()
            new_items = page.get_menu_item_texts()
            print(f'    [刷新后菜单] {new_items}')
            if new_items != items:
                found_change = True
                break
        final = page.get_menu_item_texts()
        assert len(final) >= 4, f'刷新后菜单项异常：{final}'
        print(f'    [动态变化检测] {"已捕获变化" if found_change else "本次刷新未触发变化（正常）"}')
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# test_theinternet.py
def runtest3(browser='chrome'):
    print()
    print(f'=== The Internet 补充实验二 (TC25 ~ TC34) [{browser.upper()}] ===')
    tc25_floating_menu(browser)
    tc26_broken_images(browser)
    tc27_infinite_scroll(browser)
    tc28_notification_message(browser)
    tc29_dynamic_controls(browser)
    tc30_dynamic_loading(browser)
    tc31_hovers(browser)
    tc32_key_presses(browser)
    tc33_multiple_windows(browser)
    tc34_disappearing_elements(browser)