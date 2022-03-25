import time
import unittest

from Saucedeomo import LoggingToPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from util.base_command import BaseCommand

from util.field import Field


class TestLogging(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("headless")

        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
        self.driver.get("https://www.saucedemo.com/")

        self.base_command = BaseCommand(self.driver)

    def test_one_logging(self):
        LoggingToPage.logging_to_page(self)
        self.assertEqual(self.base_command.get_element_text(Field.home_page), "PRODUCTS")

        # sort elements
        LoggingToPage.sort_items(self)
        self.assertEqual(self.base_command.get_element_text(Field.sort_order).lower(), "price (high to low)")

        # add products to cart
        LoggingToPage.add_items_to_cart(self)
        self.assertEqual(self.base_command.get_element_text(Field.numer_of_items_in_cart), "3")

        # go to the cart
        LoggingToPage.open_cart(self)
        self.assertEqual(self.base_command.get_element_text(Field.cart_page).lower(), "your cart")

        # Open Checkout Page
        LoggingToPage.open_checkout_page(self)
        self.assertEqual(self.base_command.get_element_text(Field.checkout_page).lower(),
                         "checkout: your information")

        # Fill fields on Checkout page
        LoggingToPage.fill_checkout(self)
        #self.assertTrue(self.base_command.get_element_text(Field.checkout_first_name).get_attribute("John"))

        # Continue after filling the checkout fields
        LoggingToPage.click_checkout_continue_button(self)
        self.assertEqual(self.base_command.get_element_text(Field.checkout_overview).lower(),
                         "checkout: overview")

        # Check Tax calculation
        tax = LoggingToPage.check_that_taxes_are_calculated_wright(self)
        self.assertAlmostEqual(float(tax), float(self.base_command.tax_text(Field.tax)))

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()