# pages/theinternet_page.py
# Page Object — The Internet
# 封装 The Internet 所有页面的元素定位与操作方法

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class TheInternetPage:

    BASE = 'https://the-internet.herokuapp.com'

    URL_FLOATING_MENU   = f'{BASE}/floating_menu'
    URL_BROKEN_IMAGES   = f'{BASE}/broken_images'
    URL_INFINITE_SCROLL = f'{BASE}/infinite_scroll'
    URL_NOTIFICATION    = f'{BASE}/notification_message_rendered'
    URL_DYN_CONTROLS    = f'{BASE}/dynamic_controls'
    URL_DYN_LOADING     = f'{BASE}/dynamic_loading/1'
    URL_HOVERS          = f'{BASE}/hovers'
    URL_KEY_PRESSES     = f'{BASE}/key_presses'
    URL_SLIDER          = f'{BASE}/horizontal_slider'
    URL_TABLES          = f'{BASE}/sortable_data_tables'
    URL_WINDOWS         = f'{BASE}/windows'
    URL_DISAPPEARING    = f'{BASE}/disappearing_elements'

    # ── 元素定位常量 ──────────────────────────────────────────
    _MENU               = (By.ID,           'menu')
    _MENU_LINKS         = (By.CSS_SELECTOR,  '#menu a')
    _ALL_IMAGES         = (By.CSS_SELECTOR,  'div.example img')
    _SCROLL_ITEMS       = (By.CLASS_NAME,    'jscroll-added')
    _FLASH_MSG          = (By.ID,            'flash')
    _NOTIFICATION_LINK  = (By.XPATH,         '//*[@id="content"]/div/p/a')
    _CHECKBOX_EL        = (By.XPATH,         '//*[@id="checkbox"]')
    _CHECKBOX_BTN       = (By.XPATH,         '//*[@id="checkbox-example"]/button')
    _CHECKBOX_MSG       = (By.CSS_SELECTOR,  '#checkbox-example #message')
    _INPUT_BOX          = (By.CSS_SELECTOR,  '#input-example input')
    _INPUT_BTN          = (By.CSS_SELECTOR,  '#input-example button')
    _START_BTN          = (By.CSS_SELECTOR,  '#start button')
    _LOADING_BAR        = (By.ID,            'loading')
    _FINISH_TEXT        = (By.ID,            'finish')
    _FIGURES            = (By.CSS_SELECTOR,  '.figure')
    _FIGCAPTION         = (By.CSS_SELECTOR,  '.figcaption')
    _KEY_TARGET         = (By.ID,            'target')
    _KEY_RESULT         = (By.ID,            'result')
    _SLIDER_INPUT       = (By.CSS_SELECTOR,  'input[type="range"]')
    _SLIDER_VALUE       = (By.ID,            'range')
    _TABLE_ROWS         = (By.CSS_SELECTOR,  '#table1 tbody tr')
    _TABLE_HEADER_LN    = (By.XPATH,         '//table[@id="table1"]//th[text()="Last Name"]')
    _WIN_LINK           = (By.LINK_TEXT,     'Click Here')
    _WIN_HEADING        = (By.TAG_NAME,      'h3')
    _MENU_ITEMS         = (By.CSS_SELECTOR,  '.example li a')

    # ── 构造函数 ──────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    # ── 通用工具方法 ──────────────────────────────────────────
    def _find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _find_all(self, locator):
        return self.driver.find_elements(*locator)

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # ── TC25 Floating Menu ────────────────────────────────────
    def open_floating_menu(self):
        self.driver.get(self.URL_FLOATING_MENU)
        time.sleep(1)

    def get_menu_element(self):
        return self._find(self._MENU)

    def scroll_to(self, px):
        self.driver.execute_script(f'window.scrollTo(0, {px})')
        time.sleep(0.5)

    def scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.5)

    def get_menu_links(self):
        return self._find_all(self._MENU_LINKS)

    # ── TC26 Broken Images ────────────────────────────────────
    def open_broken_images(self):
        self.driver.get(self.URL_BROKEN_IMAGES)
        time.sleep(2)

    def get_image_status(self):
        """返回 (ok列表, broken列表)"""
        imgs = self._find_all(self._ALL_IMAGES)
        ok, broken = [], []
        for img in imgs:
            src = img.get_attribute('src') or ''
            if not src:
                continue
            loaded = self.driver.execute_script(
                'return arguments[0].complete && arguments[0].naturalWidth > 0', img)
            (ok if loaded else broken).append(src.split('/')[-1])
        return ok, broken

    # ── TC27 Infinite Scroll ──────────────────────────────────
    def open_infinite_scroll(self):
        self.driver.get(self.URL_INFINITE_SCROLL)
        time.sleep(1)

    def get_scroll_item_count(self):
        return len(self._find_all(self._SCROLL_ITEMS))

    def scroll_down_multiple(self, times=10, wait=1.5):
        for _ in range(times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(wait)

    # ── TC28 Notification Message ─────────────────────────────
    def open_notification(self):
        self.driver.get(self.URL_NOTIFICATION)
        time.sleep(0.5)

    def click_next_notification(self):
        self._click(self._NOTIFICATION_LINK)

    def get_flash_text(self):
        el = self.wait.until(EC.presence_of_element_located(self._FLASH_MSG))
        return el.text.strip().split('\n')[0]

    # ── TC29 Dynamic Controls ─────────────────────────────────
    def open_dynamic_controls(self):
        self.driver.get(self.URL_DYN_CONTROLS)

    def get_checkbox_element(self):
        return self._find(self._CHECKBOX_EL)

    def click_checkbox_btn(self):
        self._click(self._CHECKBOX_BTN)

    def wait_checkbox_gone(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#checkbox input'))
        )

    def get_checkbox_msg(self):
        return self._find(self._CHECKBOX_MSG).text

    def wait_checkbox_back(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, 'checkbox'))
        )

    def get_input_box(self):
        return self._find(self._INPUT_BOX)

    def click_input_btn(self):
        self._click(self._INPUT_BTN)

    def wait_input_enabled(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self._INPUT_BOX).is_enabled()
        )

    def type_into_input(self, text):
        el = self._find(self._INPUT_BOX)
        el.send_keys(text)
        return el

    # ── TC30 Dynamic Loading ──────────────────────────────────
    def open_dynamic_loading(self):
        self.driver.get(self.URL_DYN_LOADING)

    def click_start(self):
        self._click(self._START_BTN)

    def wait_loading_done(self):
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(self._LOADING_BAR)
        )

    def get_finish_text(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self._FINISH_TEXT)
        ).text

    # ── TC31 Hovers ───────────────────────────────────────────
    def open_hovers(self):
        self.driver.get(self.URL_HOVERS)

    def get_figures(self):
        return self._find_all(self._FIGURES)

    def hover_figure(self, figure_el):
        ActionChains(self.driver).move_to_element(figure_el).perform()
        time.sleep(2)

    def get_figcaption(self, figure_el):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of(figure_el.find_element(*self._FIGCAPTION))
        )

    # ── TC32 Key Presses ──────────────────────────────────────
    def open_key_presses(self):
        self.driver.get(self.URL_KEY_PRESSES)

    def send_key_to_target(self, key):
        self._find(self._KEY_TARGET).send_keys(key)
        time.sleep(0.5)

    def get_key_result(self):
        return self.driver.find_element(*self._KEY_RESULT).text

    # ── TC33 Multiple Windows ─────────────────────────────────
    def open_windows_page(self):
        self.driver.get(self.URL_WINDOWS)

    def click_new_window_link(self):
        self._click(self._WIN_LINK)
        time.sleep(1)

    def get_all_handles(self):
        return self.driver.window_handles

    def switch_to_window(self, handle):
        self.driver.switch_to.window(handle)

    def get_window_heading(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._WIN_HEADING)
        ).text

    # ── TC34 Disappearing Elements ────────────────────────────
    def open_disappearing(self):
        self.driver.get(self.URL_DISAPPEARING)
        time.sleep(1)

    def get_menu_item_texts(self):
        return [el.text for el in self._find_all(self._MENU_ITEMS)]

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(0.5)