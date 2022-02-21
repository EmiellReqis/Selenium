import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from util.base_command import BaseCommand

from util.field import Field


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("headless")

        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
        self.driver.get("https://www.saucedemo.com/")

        self.base_command = BaseCommand(self.driver)


    def test_homework(self):
        self.base_command.clear_element(Field.username_textfield)
        self.base_command.send_text_to_element(Field.username_textfield, "standard_user")

        self.base_command.clear_element(Field.username_passwordfield)
        self.base_command.send_text_to_element(Field.username_passwordfield, "secret_sauce")

        self.base_command.click_element(Field.login_button)
        self.base_command.click_element(Field.sort_order)

        self.base_command.click_element(Field.item1)
        self.base_command.click_element(Field.item2)
        self.base_command.click_element(Field.item3)

        self.base_command.click_element(Field.cart)

        self.base_command.click_element(Field.checkout)
        self.base_command.send_text_to_element(Field.checkout_first_name, "John")
        self.base_command.send_text_to_element(Field.checkout_last_name, "Doe")
        self.base_command.send_text_to_element(Field.checkout_zip_code, "12-345")

        self.base_command.click_element(Field.checkout_continue)

        item_total_price = self.base_command.item_total_price_text(Field.item_total)
        total_price = self.base_command.total_price_text(Field.total)
        tax_calculated = float(total_price) - float(item_total_price)
        tax = self.base_command.tax_text(Field.tax)

        self.assertAlmostEqual(tax_calculated, float(tax))

        time.sleep(5)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()