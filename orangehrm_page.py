# pages/orangehrm_page.py
# Page Object — OrangeHRM Demo
# 封装 OrangeHRM 所有页面的元素定位与操作方法
# 测试用例通过调用本类方法与页面交互，不直接操作 driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class OrangeHRMPage:

    URL = 'https://opensource-demo.orangehrmlive.com/'

    # ── 元素定位常量 ──────────────────────────────────────────
    # 登录页
    _USERNAME        = (By.NAME,  'username')
    _PASSWORD        = (By.NAME,  'password')
    _LOGIN_BTN       = (By.XPATH, '//button[@type="submit"]')
    _LOGIN_ERROR     = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/p')
    _ERROR_MSG_1     = (By.XPATH, '(//span[contains(@class,"oxd-input-field-error-message")])[1]')
    _ERROR_MSG_2     = (By.XPATH, '(//span[contains(@class,"oxd-input-field-error-message")])[2]')

    # Dashboard
    _DASHBOARD_TITLE  = (By.XPATH,      '//h6[text()="Dashboard"]')
    _DASHBOARD_WIDGET = (By.CLASS_NAME,  'orangehrm-dashboard-widget')

    # 菜单
    _MENU_ADMIN       = (By.XPATH, '//span[text()="Admin"]')
    _MENU_PIM         = (By.XPATH, '//span[text()="PIM"]')
    _MENU_LEAVE       = (By.XPATH, '//span[text()="Leave"]')
    _MENU_RECRUITMENT = (By.XPATH, '//span[text()="Recruitment"]')

    # Admin 页
    _ADMIN_TITLE      = (By.XPATH, '//h5[text()="System Users"]')
    _DROPDOWN_ROLE    = (By.XPATH, '(//div[@class="oxd-select-text-input"])[1]')
    _DROPDOWN_ADMIN   = (By.XPATH, '//div[@role="option"]//span[text()="Admin"]')

    # PIM 页
    _PIM_TITLE        = (By.XPATH, '//h5[text()="Employee Information"]')
    _EMPLOYEE_INPUT   = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[1]/div/div[1]/div/div[2]/div/div/input')
    _TABLE_CARD       = (By.CLASS_NAME, 'oxd-table-card')
    _TABLE_HEADER     = (By.CLASS_NAME, 'oxd-table-header')
    _SEARCH_BTN       = (By.XPATH, '//button[@type="submit"]')

    # Leave 页
    _LEAVE_TITLE      = (By.XPATH, '//h5[text()="Leave List"]')

    # Recruitment 页
    _RECRUITMENT_TITLE = (By.XPATH,      '//h6[text()="Recruitment"]')
    _PAGINATION        = (By.CLASS_NAME,  'oxd-pagination-page-item')
    _TABLE_ROWS        = (By.XPATH,       '//div[@class="oxd-table-body"]//div[@role="row"]')

    # Add Employee 页
    _ADD_EMP_LINK     = (By.XPATH, '//a[text()="Add Employee"]')
    _ADD_EMP_TITLE    = (By.XPATH, '//h6[text()="Add Employee"]')
    _FIRST_NAME       = (By.NAME,  'firstName')
    _MIDDLE_NAME      = (By.NAME,  'middleName')
    _LAST_NAME        = (By.NAME,  'lastName')
    _PHOTO_UPLOAD     = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[1]/div/div[2]/div/button')

    # 登出
    _USER_DROPDOWN    = (By.CLASS_NAME, 'oxd-userdropdown-tab')
    _LOGOUT_BTN       = (By.XPATH,      '//a[text()="Logout"]')

    # ── 构造函数 ──────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    # ── 通用工具方法 ──────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)

    def _find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # ── 登录操作 ──────────────────────────────────────────────
    def login(self, username='Admin', password='admin123'):
        """输入用户名密码并点击登录，等待 Dashboard 出现"""
        self._find(self._USERNAME).send_keys(username)
        self._find(self._PASSWORD).send_keys(password)
        self._click(self._LOGIN_BTN)
        self.wait.until(EC.presence_of_element_located(self._DASHBOARD_TITLE))

    def login_only(self, username, password):
        """仅点击登录按钮，不等待结果（用于负面测试）"""
        self._find(self._USERNAME).send_keys(username)
        self._find(self._PASSWORD).send_keys(password)
        self._click(self._LOGIN_BTN)

    def click_login_empty(self):
        """不输入任何内容直接点击登录"""
        self._click(self._LOGIN_BTN)

    def get_login_error_text(self):
        return self._find(self._LOGIN_ERROR).text

    def get_required_msg_1(self):
        return self._find(self._ERROR_MSG_1).text

    def get_required_msg_2(self):
        return self._find(self._ERROR_MSG_2).text

    # ── Dashboard ─────────────────────────────────────────────
    def wait_dashboard(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self._DASHBOARD_WIDGET)
        )
        return self._find(self._DASHBOARD_TITLE)

    def refresh_and_check_dashboard(self):
        self.driver.refresh()
        time.sleep(2)
        return self._find(self._DASHBOARD_TITLE)

    # ── 菜单导航 ──────────────────────────────────────────────
    def goto_admin(self):
        self._click(self._MENU_ADMIN)
        self.wait.until(EC.presence_of_element_located(self._ADMIN_TITLE))

    def goto_pim(self):
        self._click(self._MENU_PIM)
        self.wait.until(EC.presence_of_element_located(self._PIM_TITLE))

    def goto_leave(self):
        self._click(self._MENU_LEAVE)
        self.wait.until(EC.presence_of_element_located(self._LEAVE_TITLE))

    def goto_recruitment(self):
        self._click(self._MENU_RECRUITMENT)
        self.wait.until(EC.presence_of_element_located(self._RECRUITMENT_TITLE))

    # ── 员工搜索 ──────────────────────────────────────────────
    def search_employee(self, name):
        self._find(self._EMPLOYEE_INPUT).send_keys(name)
        self._click(self._SEARCH_BTN)
        self.wait.until(EC.presence_of_element_located(self._TABLE_CARD))

    def get_table_cards(self):
        return self.driver.find_elements(*self._TABLE_CARD)

    def get_table_header(self):
        return self._find(self._TABLE_HEADER)

    # ── 下拉框操作 ────────────────────────────────────────────
    def select_user_role_admin(self):
        self._click(self._DROPDOWN_ROLE)
        time.sleep(1)
        self._click(self._DROPDOWN_ADMIN)
        time.sleep(1)

    def get_selected_role_text(self):
        return self._find(self._DROPDOWN_ROLE).text

    # ── 分页 ──────────────────────────────────────────────────
    def click_search_and_get_pagination(self):
        self._click(self._SEARCH_BTN)
        self.wait.until(EC.presence_of_element_located(self._TABLE_ROWS))
        return self.driver.find_elements(*self._PAGINATION)

    # ── Add Employee 表单 ─────────────────────────────────────
    def goto_add_employee(self):
        self.wait.until(EC.presence_of_element_located(self._ADD_EMP_LINK))
        self._click(self._ADD_EMP_LINK)
        self.wait.until(EC.presence_of_element_located(self._ADD_EMP_TITLE))

    def fill_employee_form(self, first, middle, last, photo_path=None):
        self._find(self._FIRST_NAME).send_keys(first)
        self._find(self._MIDDLE_NAME).send_keys(middle)
        self._find(self._LAST_NAME).send_keys(last)
        if photo_path:
            self._find(self._PHOTO_UPLOAD).send_keys(photo_path)

    def submit_form(self):
        self._click(self._LOGIN_BTN)

    # ── 登出 ──────────────────────────────────────────────────
    def logout(self):
        self._click(self._USER_DROPDOWN)
        time.sleep(1)
        self._click(self._LOGOUT_BTN)
        self.wait.until(EC.presence_of_element_located(self._USERNAME))