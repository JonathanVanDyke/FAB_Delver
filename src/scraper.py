import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controllers.controller import FabCardController


test_url = "https://shop.tcgplayer.com/price-guide/flesh-and-blood-tcg/monarch"


class WebTableTest:
  def __init__(self):
    self.fb = FabCardController()

  def setUp(self):
    self.driver = webdriver.Chrome()
    # self.driver.maximize_window()

  def get_row_col_len(self):
    pre_xpath = "/html/body/div[5]/div[2]/div/div[2]/table/tbody/tr["
    after_td_xpath = "]/td["
    after_tr_xpath = "]"

    driver = self.driver
    driver.get(test_url)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "priceGuideTable")))

    num_rows = len(driver.find_elements_by_xpath(
        "/html/body/div[5]/div[2]/div/div[2]/table/tbody/tr"))
    print("Rows in table are " + repr(num_rows))

    num_cols = len(driver.find_elements_by_xpath(
        "/html/body/div[5]/div[2]/div/div[2]/table/tbody[1]/tr[1]/td"))
    print("Columns in table are " + repr(num_cols))

    res = [[]]

    for r in range(1, num_rows):
      for c in range(1, num_cols):
        final_xpath = pre_xpath + str(r) + after_td_xpath + str(c) + after_tr_xpath
        cell_text = driver.find_element_by_xpath(final_xpath).text
        
        if "//" in cell_text:
          cell_text = cell_text.split("//")
          cell_text = cell_text[0][:-1]
          # print(cell_text, len(cell_text))

        res[-1].append(cell_text)

        if len(res[-1]) >= 5:
          res[-1][-1] = 'https://shop.tcgplayer.com/price-guide/flesh-and-blood-tcg/monarch'
          res.append([])
    res.pop()

    if len(res) == num_rows - 1: self.tearDown()

    self.load_cards(res)

    return [num_rows, num_cols]

  def tearDown(self):
    self.driver.close()
    self.driver.quit()

  def load_cards(self, cards):
    # self.fb.delete_all_records()
    for card in cards:
      self.fb.create_record(card)

  def show_db(self):
    self.fb.list_all()


if __name__ == "__main__":
  wt = WebTableTest()
  print("... DB prior to load: ")
  
  wt.setUp()
  wt.show_db()
  r,c = wt.get_row_col_len()
  print("... DB after load: ")
  wt.show_db()
  # wt.tearDown()

  print('rows: ', r, ' cols: ', c)

