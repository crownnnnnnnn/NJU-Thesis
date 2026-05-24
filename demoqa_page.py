# pages/demoqa_page.py
# Page Object — DemoQA
# 封装 DemoQA 所有页面的元素定位与操作方法

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pyautogui


class DemoQAPage:

    URL_PRACTICE_FORM = 'https://demoqa.com/automation-practice-form'
    URL_ALERTS        = 'https://demoqa.com/alerts'
    URL_BROWSER_WIN   = 'https://demoqa.com/browser-windows'
    URL_FRAMES        = 'https://demoqa.com/frames'
    URL_DROPPABLE     = 'https://demoqa.com/droppable'

    # ── 元素定位常量 ──────────────────────────────────────────
    # Practice Form
    _FIRST_NAME      = (By.ID, 'firstName')
    _LAST_NAME       = (By.ID, 'lastName')
    _EMAIL           = (By.ID, 'userEmail')
    _PHONE           = (By.ID, 'userNumber')
    _GENDER_FEMALE   = (By.ID, 'gender-radio-2')
    _CHECKBOX_SPORTS = (By.ID, 'hobbies-checkbox-1')
    _CHECKBOX_READING= (By.ID, 'hobbies-checkbox-2')
    _DATE_INPUT      = (By.ID, 'dateOfBirthInput')
    _DATE_CELL       = (By.XPATH, '//*[@id="dateOfBirth"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[5]')
    _FILE_UPLOAD     = (By.ID, 'uploadPicture')
    _SUBMIT_BTN      = (By.ID, 'submit')
    _SUCCESS_MODAL   = (By.ID, 'example-modal-sizes-title-lg')

    # Alerts
    _ALERT_BTN       = (By.ID, 'alertButton')
    _CONFIRM_BTN     = (By.ID, 'confirmButton')
    _PROMPT_BTN      = (By.ID, 'promtButton')
    _CONFIRM_RESULT  = (By.ID, 'confirmResult')
    _PROMPT_RESULT   = (By.ID, 'promptResult')

    # Browser Windows
    _TAB_BTN         = (By.ID, 'tabButton')

    # Frames
    _FRAME1          = (By.ID, 'frame1')
    _FRAME2          = (By.ID, 'frame2')
    _FRAME_HEADING   = (By.ID, 'sampleHeading')

    # Droppable
    _DRAGGABLE       = (By.ID, 'draggable')
    _DROPPABLE       = (By.ID, 'droppable')
    _DROPPED_TEXT    = (By.XPATH, '//*[@id="droppable"]/p')

    # ── 构造函数 ──────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    # ── 通用工具方法 ──────────────────────────────────────────
    def _find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # ── Practice Form ─────────────────────────────────────────
    def open_practice_form(self):
        self.driver.get(self.URL_PRACTICE_FORM)

    def fill_text_fields(self, first, last, email, phone):
        self._find(self._FIRST_NAME).send_keys(first)
        self._find(self._LAST_NAME).send_keys(last)
        self._find(self._EMAIL).send_keys(email)
        self._find(self._PHONE).send_keys(phone)

    def get_first_name_value(self):
        return self._find(self._FIRST_NAME).get_attribute('value')

    def select_gender_female(self):
        el = self._find(self._GENDER_FEMALE)
        el.click()
        return el

    def select_hobbies(self):
        sports  = self._find(self._CHECKBOX_SPORTS)
        reading = self._find(self._CHECKBOX_READING)
        sports.click()
        reading.click()
        return sports, reading

    def deselect_sports(self, sports_el):
        sports_el.click()

    # def pick_date(self):
    #     date = self._find(self._DATE_INPUT)
    #     date.click()
    #     date.clear()
    #     self._find(self._DATE_CELL).click()
    #     time.sleep(1)
    #     date.send_keys(Keys.TAB)

    # ---------------- 修改 TC16 FIREFOX ----------------------
    def pick_date(self, date_text='01 Oct 2003'):
        date = self.wait.until(
            EC.element_to_be_clickable(self._DATE_INPUT)
        )

        # 先把日期输入框滚动到页面中间，避免 Firefox 下元素位置不稳定
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            date
        )
        time.sleep(0.5)

        # 点击输入框后，直接全选原日期并输入新日期
        date.click()
        date.send_keys(Keys.CONTROL, 'a')
        date.send_keys(date_text)
        date.send_keys(Keys.ENTER)

        time.sleep(0.5)
    # ---------------- 修改 TC16 FIREFOX ----------------------

    def upload_file(self, path):
        self._find(self._FILE_UPLOAD).send_keys(path)

    def get_upload_value(self):
        return self._find(self._FILE_UPLOAD).get_attribute('value')

    # def submit_form(self):
    #     self._click(self._SUBMIT_BTN)

    # ----------- 解决 FIREFOX TC18 -------------
    def submit_form(self):
        submit = self.wait.until(
            EC.presence_of_element_located(self._SUBMIT_BTN)
        )

        # 将 Submit 按钮滚动到页面中间，避免在 Firefox 下被底部 footer 遮挡
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit
        )
        time.sleep(0.5)

        # 等待按钮处于可点击状态后再点击
        self.wait.until(
            EC.element_to_be_clickable(self._SUBMIT_BTN)
        ).click()
    # ----------- 解决 FIREFOX TC18 -------------

    def get_modal_title(self):
        return self.wait.until(
            EC.presence_of_element_located(self._SUCCESS_MODAL)
        ).text

    # ── Alerts ────────────────────────────────────────────────
    def open_alerts(self):
        self.driver.get(self.URL_ALERTS)

    def trigger_alert(self):
        self._click(self._ALERT_BTN)
        time.sleep(1)

    def get_alert_text(self):
        return self.driver.switch_to.alert.text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def trigger_confirm(self):
        self._click(self._CONFIRM_BTN)
        time.sleep(1)

    def dismiss_confirm(self):
        self.driver.switch_to.alert.dismiss()

    def get_confirm_result(self):
        return self._find(self._CONFIRM_RESULT).text

    def trigger_prompt(self):
        self._click(self._PROMPT_BTN)
        time.sleep(1)

    def send_prompt_text(self, text):
        alert = self.driver.switch_to.alert
        alert.send_keys(text)
        time.sleep(1)
        alert.accept()
        time.sleep(1)

    def get_prompt_result(self):
        return self._find(self._PROMPT_RESULT).text

    # ── Browser Windows ───────────────────────────────────────
    def open_browser_windows(self):
        self.driver.get(self.URL_BROWSER_WIN)

    def click_new_tab(self):
        self._click(self._TAB_BTN)
        time.sleep(1)

    def get_all_handles(self):
        return self.driver.window_handles

    def switch_to_window(self, handle):
        self.driver.switch_to.window(handle)

    # ── Frames ────────────────────────────────────────────────
    def open_frames(self):
        self.driver.get(self.URL_FRAMES)

    def switch_into_frame1(self):
        frame = self._find(self._FRAME1)
        self.driver.switch_to.frame(frame)
        time.sleep(0.5)

    def get_frame_heading_text(self):
        return self._find(self._FRAME_HEADING).text

    def switch_to_default(self):
        self.driver.switch_to.default_content()
        time.sleep(0.5)

    def find_frame2(self):
        return self._find(self._FRAME2)

    # ── Droppable（拖拽）─────────────────────────────────────
    def open_droppable(self):
        self.driver.get(self.URL_DROPPABLE)
        time.sleep(1)
        self.driver.maximize_window()
        time.sleep(0.5)

    def drag_to_drop(self):
        """用 pyautogui 分步拖拽，自动处理 DPI 缩放"""
        src = self._find(self._DRAGGABLE)
        dst = self._find(self._DROPPABLE)

        def get_screen_center(element):
            rect = self.driver.execute_script(
                'var r=arguments[0].getBoundingClientRect();'
                'return {x:r.left+r.width/2, y:r.top+r.height/2};', element)
            offset = self.driver.execute_script(
                'return {x:window.screenX,'
                'y:window.screenY+(window.outerHeight-window.innerHeight)};')
            return int(rect['x'] + offset['x']), int(rect['y'] + offset['y'])

        scale = pyautogui.size()[0] / self.driver.execute_script('return window.screen.width')
        sx, sy = get_screen_center(src)
        dx, dy = get_screen_center(dst)
        sx, sy = int(sx * scale), int(sy * scale)
        dx, dy = int(dx * scale), int(dy * scale)

        pyautogui.moveTo(sx, sy, duration=0.5)
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.5)
        steps = 30
        for i in range(1, steps + 1):
            pyautogui.moveTo(sx + (dx - sx) * i // steps,
                             sy + (dy - sy) * i // steps,
                             duration=0.02)
        time.sleep(0.3)
        pyautogui.mouseUp()
        time.sleep(1)

    def get_dropped_text(self):
        return self._find(self._DROPPED_TEXT).text