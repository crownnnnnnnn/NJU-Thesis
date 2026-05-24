# test_orangehrm.py
# 核心实验：OrangeHRM Demo 功能测试
# 演示地址：https://opensource-demo.orangehrmlive.com/
# 覆盖用例：TC01 ~ TC12
# 架构说明：采用 Page Object Model，测试逻辑与页面操作解耦
# 跨浏览器：每个用例支持 browser 参数（'chrome' 或 'edge'）

import time
from conf import conf
from screenshot_utils import take_screenshot
from pages.orangehrm_page import OrangeHRMPage
import logger

MODULE = 'OrangeHRM'

def _module(browser):
    return f'{MODULE}-{browser.upper()}'

# -------------------------------------------------------
# TC01：正确账号密码登录
# -------------------------------------------------------
def tc01_login_success(browser='chrome'):
    tc_id, tc_name = 'TC01', '正确账号密码登录'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC02：错误密码登录，验证错误提示
# -------------------------------------------------------
def tc02_login_wrongpassword(browser='chrome'):
    tc_id, tc_name = 'TC02', '错误密码登录验证错误提示'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login_only('Admin', 'wrongpassword')
        error = page.get_login_error_text()
        assert 'Invalid credentials' in error, f'错误提示内容不符：{error}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC03：用户名以及密码为空，验证必填提示
# -------------------------------------------------------
def tc03_login_empty_fields(browser='chrome'):
    tc_id, tc_name = 'TC03', '空值登录验证必填信息'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.click_login_empty()
        msg1 = page.get_required_msg_1()
        assert 'Required' in msg1, f'必填提示不符：{msg1}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC04：登录后验证 Dashboard 页面是否正常加载
# -------------------------------------------------------
def tc04_dashboard_load(browser='chrome'):
    tc_id, tc_name = 'TC04', '登陆后首页Dashboard加载验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        title = page.wait_dashboard()
        assert title.is_displayed(), 'Dashboard 标题不可见'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC05：菜单导航测试（Admin / PIM / Leave）
# -------------------------------------------------------
def tc05_menu_navigation(browser='chrome'):
    tc_id, tc_name = 'TC05', '菜单导航跳转测试'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_admin()
        page.goto_pim()
        page.goto_leave()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC06：员工查询
# -------------------------------------------------------
def tc06_employee_search(browser='chrome'):
    tc_id, tc_name = 'TC06', '员工姓名搜索测试'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_pim()
        page.search_employee('Emily')
        cards = page.get_table_cards()
        assert len(cards) > 0, '搜索结果为空'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC07：表格显示验证
# -------------------------------------------------------
def tc07_table_display(browser='chrome'):
    tc_id, tc_name = 'TC07', '表格列标题显示验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_admin()
        header = page.get_table_header()
        assert header.is_displayed(), '表格标题行不可见'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC08：下拉框选择 User Role
# -------------------------------------------------------
def tc08_dropdown_select(browser='chrome'):
    tc_id, tc_name = 'TC08', '下拉框选择User Role验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_admin()
        page.select_user_role_admin()
        text = page.get_selected_role_text()
        assert 'Admin' in text, f'下拉框选择结果不符：{text}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC09：分页测试
# -------------------------------------------------------
def tc09_pagination(browser='chrome'):
    tc_id, tc_name = 'TC09', '表格分页切换测试'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_recruitment()
        pages = page.click_search_and_get_pagination()
        if len(pages) > 1:
            pages[2].click()
            time.sleep(1)
            logger.log(tc_id, tc_name, _module(browser), '通过', remark='分页按钮正常', duration=time.time() - t0)
        else:
            logger.log(tc_id, tc_name, _module(browser), '通过', remark='数据不足两页，无需分页', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC10：填写表单以及上传文件
# -------------------------------------------------------
def tc10_form_insert(browser='chrome'):
    tc_id, tc_name = 'TC10', '填写表单以及上传文件'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.goto_pim()
        page.goto_add_employee()
        page.fill_employee_form(
            'Chris', 'Evan', 'Jones',
            photo_path=r'C:\Users\Celine\Documents\NJU\大四\DEMO\Project Demo\foto.png'
        )
        page.submit_form()
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC11：页面刷新后验证登录状态保持
# -------------------------------------------------------
def tc11_refresh_keep_login(browser='chrome'):
    tc_id, tc_name = 'TC11', '页面刷新后登录状态保持验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        el = page.refresh_and_check_dashboard()
        assert el.is_displayed(), '刷新后未保持登录状态'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()

# -------------------------------------------------------
# TC12：退出登录，验证返回登录页
# -------------------------------------------------------
def tc12_logout(browser='chrome'):
    tc_id, tc_name = 'TC12', '退出登录返回登录页验证'
    t0 = time.time()
    driver = conf(browser)
    try:
        page = OrangeHRMPage(driver)
        page.open()
        page.login()
        page.logout()
        assert 'login' in driver.current_url, f'未跳转到登录页：{driver.current_url}'
        logger.log(tc_id, tc_name, _module(browser), '通过', duration=time.time() - t0)
    except Exception as e:
        time.sleep(2)
        screenshot_path = take_screenshot(driver, f'{tc_id}_{browser}')
        logger.log(tc_id, tc_name, _module(browser), '失败', remark=f'{str(e)[:80]} 截图:{screenshot_path}', duration=time.time() - t0)
    finally:
        driver.quit()


# test_orangehrm.py
def runtest1(browser='chrome'):
    print()
    print(f'=== OrangeHRM Demo 核心实验 (TC01 ~ TC12) [{browser.upper()}] ===')
    tc01_login_success(browser)
    tc02_login_wrongpassword(browser)
    tc03_login_empty_fields(browser)
    tc04_dashboard_load(browser)
    tc05_menu_navigation(browser)
    tc06_employee_search(browser)
    tc07_table_display(browser)
    tc08_dropdown_select(browser)
    tc09_pagination(browser)
    tc10_form_insert(browser)
    tc11_refresh_keep_login(browser)
    tc12_logout(browser)