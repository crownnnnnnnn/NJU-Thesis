import os
import time

def take_screenshot(driver, tc_id):
    folder = 'screenshots'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder,f'{tc_id}_{int(time.time())}.png')
    driver.get_screenshot_as_file(path)  # Selenium API
    print(f'[截图已保存] {path}')  # 控制台输出路径
    return path