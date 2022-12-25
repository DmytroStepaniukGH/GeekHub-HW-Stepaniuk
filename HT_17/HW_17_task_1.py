import time
import wget
import os
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderRobot:
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--ignore-ssl-errors=true')
    options.add_argument('--start-maximized')

    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches',
                                    ['enable-automation'])
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    def get_orders(self):
        self._check_folder()
        self.open_site()
        self.go_to_order()
        order_values = self._get_values_from_csv()

        for order in order_values:
            self.click_to_start_order()
            self.set_values_to_fields(order)
            self.get_preview()
            self.get_order()
            self.go_to_order_another()

    def open_site(self):
        self.driver.get('https://robotsparebinindustries.com/')

    def go_to_order(self):
        self.driver.find_element(By.LINK_TEXT, 'Order your robot!').click()

    def click_to_start_order(self):
        self.wait_element('CSS', '.btn.btn-dark').click()

    def set_values_to_fields(self, order_values):
        select = Select(self.wait_element('ID', 'head'))
        for option in select.options:
            if option.get_attribute('value') == order_values['Head']:
                option.click()
                break

        radio_btn = self.driver.find_elements(By.CSS_SELECTOR,
                                              '.form-check-input')
        for btn in radio_btn:
            if btn.get_attribute('value') == order_values['Body']:
                btn.click()
                break

        fields = self.driver.find_elements(By.CSS_SELECTOR, '.form-control')
        fields[0].send_keys(order_values['Legs'])
        fields[1].send_keys(order_values['Address'])

    def get_preview(self):
        self.driver.find_element(By.ID, 'preview').click()
        self.wait_element('CSS', 'a.attribution')
        time.sleep(1)
        preview = self.driver.find_element(By.ID, 'robot-preview-image')
        preview.screenshot('output/tmp_name.png')

    def get_order(self):
        retries = 5
        while retries:
            try:
                self.wait_element('ID', 'order').click()
                text = self.driver.find_element(By.CSS_SELECTOR,
                                                '.badge.badge-success').text
                print(text)
                old_name = 'output/tmp_name.png'
                new_name = 'output/' + text + '_robot.png'
                os.rename(old_name, new_name)
                break
            except Exception:
                time.sleep(1)
                if retries > 0:
                    retries -= 1
                else:
                    raise

    def go_to_order_another(self):
        self.wait_element('ID', 'order-another').click()

    def wait_element(self, type_find, element):
        wait = WebDriverWait(self.driver, 10)
        if type_find == 'ID':
            return wait.until(EC.element_to_be_clickable((By.ID, element)))
        elif type_find == 'CSS':
            return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          element)))
        else:
            raise Exception('Заданий тип не знайдено')

    @staticmethod
    def _get_values_from_csv():
        wget.download('https://robotsparebinindustries.com/orders.csv')
        data = []
        with open('orders.csv', encoding='utf-8') as file:
            for line in csv.DictReader(file):
                data.append(line)

        return data

    @staticmethod
    def _check_folder():
        path = 'output'
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)
        else:
            dir = 'output'
            files = os.listdir(dir)
            if len(files) > 0:
                for file in files:
                    os.remove(os.path.join(dir, file))
            else:
                return


if __name__ == '__main__':
    orders = OrderRobot()
    orders.get_orders()
