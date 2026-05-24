# test_demoqa.py
# 补充实验一：DemoQA 表单与组件测试
# 演示地址：https://demoqa.com/
# 覆盖用例：TC13 ~ TC24
# 架构说明：采用 Page Object Model，测试逻辑与页面操作解耦
# 跨浏览器：每个用例支持 browser 参数（'chrome' 或 'edge'）
# 注意：TC24 拖拽依赖 pyautogui 系统鼠标，跨浏览器时若失败记录为限制因素

import time
from conf import conf
from screenshot_utils import take_screenshot
from pages.demoqa_page import DemoQAPage
import logger

MODULE = 'DemoQA'

def _module(browser):
    return f'{MODULE}-{browser.upper()}'

# -------------------------------------------------------
# TC13：文本框输入（姓名、邮箱、手机号）
# -------------------------------------------------------
def tc13_text_input(browser='chrome'):
    tc_id, tc_name = 'TC13', '文本框输入姓名邮箱以及手机号'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        page.fill_text_fields('Celine', 'Kristy', 'helloworld@test.com', '1380001380')
        val = page.get_first_name_value()
        assert 'Celine' in val, f'First Name 输入值不符：{val}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(0.5)
        driver.quit()

# -------------------------------------------------------
# TC14：单选框选择性别
# -------------------------------------------------------
def tc14_select_gender(browser='chrome'):
    tc_id, tc_name = 'TC14', '单选框选择性别'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        el = page.select_gender_female()
        time.sleep(1)
        assert el.is_selected(), 'Female 单选项未被选中'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(0.5)
        driver.quit()

# -------------------------------------------------------
# TC15：复选框选择爱好及状态判断
# -------------------------------------------------------
def tc15_checkbox_hobbies(browser='chrome'):
    tc_id, tc_name = 'TC15', '复选框选择爱好以及状态判断'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        sports, reading = page.select_hobbies()
        assert sports.is_selected(),  'Sports 复选框未被选中'
        assert reading.is_selected(), 'Reading 复选框未被选中'
        time.sleep(1)
        page.deselect_sports(sports)
        assert not sports.is_selected(), 'Sports 复选框取消勾选失败'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC16：日期控件（Date of Birth 输入）
# -------------------------------------------------------
def tc16_date_picker(browser='chrome'):
    tc_id, tc_name = 'TC16', '日期控件选择出生日期'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        page.pick_date()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC17：文件上传
# -------------------------------------------------------
def tc17_file_upload(browser='chrome'):
    tc_id, tc_name = 'TC17', '上传本地测试文件'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        page.upload_file(r'C:\Users\Celine\Documents\NJU\大四\DEMO\Project Demo\main.py')
        time.sleep(1)
        val = page.get_upload_value()
        assert val != '', f'文件上传后控件值异常：{val}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC18：表单提交并验证弹窗内容
# -------------------------------------------------------
def tc18_form_submit(browser='chrome'):
    tc_id, tc_name = 'TC18', '表单提交验证弹窗内容'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_practice_form()
        page.fill_text_fields('Celine', 'Kristy', '', '1380001380')
        page.select_gender_female()
        page.submit_form()
        title = page.get_modal_title()
        assert 'Thanks for submitting the form' in title, f'弹窗标题不符：{title}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC19：Alert 弹窗处理
# -------------------------------------------------------
def tc19_alert(browser='chrome'):
    tc_id, tc_name = 'TC19', 'Alert弹窗获取文本并确认'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_alerts()
        page.trigger_alert()
        text = page.get_alert_text()
        assert text != '', 'Alert 文本为空'
        print(f'    [Alert文本] {text}')
        page.accept_alert()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC20：Confirm 弹窗
# -------------------------------------------------------
def tc20_confirm(browser='chrome'):
    tc_id, tc_name = 'TC20', 'Confirm弹窗点击确认和取消'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_alerts()
        page.trigger_confirm()
        page.dismiss_confirm()
        time.sleep(0.5)
        result = page.get_confirm_result()
        assert 'You selected Cancel' in result, f'取消结果不符：{result}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC21：Prompt 弹窗
# -------------------------------------------------------
def tc21_prompt(browser='chrome'):
    tc_id, tc_name = 'TC21', 'Prompt弹窗输入内容并提交'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_alerts()
        page.trigger_prompt()
        page.send_prompt_text('Hello Selenium')
        result = page.get_prompt_result()
        assert 'Hello Selenium' in result, f'Prompt 结果不符：{result}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC22：多窗口切换
# -------------------------------------------------------
def tc22_multi_window(browser='chrome'):
    tc_id, tc_name = 'TC22', '多窗口打开并切换'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_browser_windows()
        original = driver.current_window_handle
        page.click_new_tab()
        handles = page.get_all_handles()
        assert len(handles) == 2, f'预期2个标签页，实际{len(handles)}个'
        page.switch_to_window(handles[1])
        time.sleep(1)
        print(f'    [新标签页URL] {driver.current_url}')
        page.switch_to_window(original)
        assert driver.current_window_handle == original, '切换回原标签页失败'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC23：iframe 切换
# -------------------------------------------------------
def tc23_iframe(browser='chrome'):
    tc_id, tc_name = 'TC23', 'iframe切换进入操作'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_frames()
        page.switch_into_frame1()
        text = page.get_frame_heading_text()
        print(f'    [iframe内文字] {text}')
        assert text != '', 'iframe 内元素文本为空'
        page.switch_to_default()
        page.find_frame2()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()

# -------------------------------------------------------
# TC24：拖拽操作
# 注意：pyautogui 依赖系统鼠标坐标，Edge 下若坐标偏移导致失败，
#       记录为"跨浏览器拖拽限制"，不视为脚本错误
# -------------------------------------------------------
def tc24_drag_and_drop(browser='chrome'):
    tc_id, tc_name = 'TC24', '拖拽元素到目标区域'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = DemoQAPage(driver)
        page.open_droppable()
        page.drag_to_drop()
        result = page.get_dropped_text()
        assert 'Dropped' in result, f'拖拽结果不符：{result}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败',
                   remark=f'[跨浏览器拖拽限制] {str(e)[:60]} 截图:{screenshot_path}',
                   duration=time.time() - t0)
    finally:
        time.sleep(2)
        driver.quit()


# test_demoqa.py
def runtest2(browser='chrome'):
    print()
    print(f'=== DemoQA 补充实验一 (TC13 ~ TC24) [{browser.upper()}] ===')
    # tc13_text_input(browser)
    # tc14_select_gender(browser)
    # tc15_checkbox_hobbies(browser)
    tc16_date_picker(browser)
    # tc17_file_upload(browser)
    tc18_form_submit(browser)
    # tc19_alert(browser)
    # tc20_confirm(browser)
    # tc21_prompt(browser)
    # tc22_multi_window(browser)
    # tc23_iframe(browser)
    # tc24_drag_and_drop(browser)