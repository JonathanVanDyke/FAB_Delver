import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

test_url = "https://www.w3schools.com/html/html_tables.asp"


class WebTableTest:

    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()

    def test_1_get_num_rows_(self):
        driver = self.driver
        driver.get(test_url)

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "w3-example")))

        num_rows = len(driver.find_elements_by_xpath(
            "//*[@id='customers']/tbody/tr"))
        print("Rows in table are " + repr(num_rows))

    def test_2_get_num_cols_(self):
        driver = self.driver
        driver.get(test_url)

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "w3-example")))
        # num_cols = len (driver.find_elements_by_xpath("//*[@id='customers']/tbody/tr/th"))
        num_cols = len(driver.find_elements_by_xpath(
            "//*[@id='customers']/tbody/tr[2]/td"))
        print("Columns in table are " + repr(num_cols))

    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    wt = WebTableTest()
    wt.setUp()
    wt.test_1_get_num_rows_()
    wt.test_2_get_num_cols_()
