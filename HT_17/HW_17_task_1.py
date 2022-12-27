import time
import os
import csv
import wget
from fpdf import FPDF, HTMLMixin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class OrderRobot:
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-ssl-errors=true')
    options.add_argument('--start-maximized')

    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches',
                                    ['enable-automation'])
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    path_output = 'output'

    def get_orders(self):
        self._check_folder(self.path_output)
        self.open_site()
        self.go_to_order()
        order_values = self._get_values_from_csv()

        for order in order_values:
            self.click_to_start_order()
            self.set_values_to_fields(order)
            self.move_to_preview()
            self.get_order()
            self.get_preview()
            self.get_html_of_preview()
            self.generate_pdf()
            self.go_to_order_another()

        os.remove(os.path.join('tmp_page.html'))

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

        self.driver.find_element(By.XPATH,
                                 "//input[@placeholder="
                                 "'Enter the part number for the legs']"). \
            send_keys(order_values['Legs'])
        self.driver.find_element(By.XPATH, "//input[@placeholder="
                                           "'Shipping address']").send_keys(
            order_values['Address'])

    def move_to_preview(self):
        self.driver.find_element(By.ID, 'preview').click()

    def get_order(self):
        retries = 5
        while retries > 0:
            try:
                self.wait_element('ID', 'order').click()
                self.driver.find_element(By.CSS_SELECTOR,
                                         '.badge.badge-success')
                break
            except Exception:
                time.sleep(1)
                if retries > 0:
                    retries -= 1
                else:
                    raise

    def get_preview(self):
        text = self.driver.find_element(By.CSS_SELECTOR,
                                        '.badge.badge-success').text
        name = f'output/{text}_robot.png'

        self.wait_element('XPATH', "//img[@alt='Legs']")
        preview = self.driver.find_element(By.ID,
                                           'robot-preview-image')
        preview.screenshot(name)

    def get_html_of_preview(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        with open('tmp_page.html', 'w', encoding='utf-8') as order_html:
            order_html.write(str(soup.find('div', {'id': 'receipt'})))

    def generate_pdf(self):
        pdf = MyFPDF()
        pdf.add_page()
        file = open('tmp_page.html', 'r')
        name = self.driver.find_element(By.CSS_SELECTOR,
                                        '.badge.badge-success').text
        data = file.read()
        pdf.write_html(data)
        tmp_name = f'{name}_robot.png'
        pdf.image(f'output/{tmp_name}', 40, 60)
        pdf.output(f'output/{name}_robot.pdf', 'F')
        os.remove(os.path.join('output', f'{name}_robot.png'))

    def go_to_order_another(self):
        self.wait_element('ID', 'order-another').click()

    def wait_element(self, type_find, element):
        wait = WebDriverWait(self.driver, 10)
        if type_find == 'ID':
            return wait.until(EC.element_to_be_clickable((By.ID, element)))
        elif type_find == 'CSS':
            return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          element)))
        elif type_find == "XPATH":
            return wait.until(EC.visibility_of_element_located((
                By.XPATH, element)))
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
    def _check_folder(folder):
        is_exist = os.path.exists(folder)
        if not is_exist:
            os.makedirs(folder)
        else:
            files = os.listdir(folder)
            if len(files) > 0:
                for file in files:
                    os.remove(os.path.join(folder, file))
            else:
                return


class MyFPDF(FPDF, HTMLMixin):
    pass


if __name__ == '__main__':
    orders = OrderRobot()
    orders.get_orders()
