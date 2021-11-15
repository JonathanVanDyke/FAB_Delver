import pytesseract
import cv2
import matplotlib.pyplot as plt
import requests
import json
import urllib.request
# from ..controllers import controller
from ..controllers.controller import FabCardController
from PIL import Image

class Reader:
  def __init__(self):
    self.img = None
    self.text = None
    self.fb = FabCardController()

  def read_image(self, src = 'MON002.png'):
    self.img = cv2.imread(src)

    cv2.imshow('prism', self.img)

    # cv2.waitKey(0)
    img_text = pytesseract.image_to_string(self.img);
    self.text = img_text
    return img_text

  def get_card_title(self):
    print(self.text.split("\n")[0])
    return self.text.split("\n")[0]

  def log_text(self):
    if (self.text):
      print(self.text)
    else:
      print('No text has been read.')

  def search_card_api(self, keyword = 'Prism'):
    query = {'keywords': keyword}
    response = requests.get("http://api.fabdb.net/cards/", params=query)
    stud_obj = json.loads(response.text)
    matches = stud_obj['data']
    print(len(matches), "cards have been found while searching for: ", keyword)


    match = self.find_match(matches, keyword)
    if not match: return "No matches found"

    print('... is this your card? ...')
    self.show_img_url(match['image'])

    # print('... IT IS WORTH: ', match['cost'])

    return stud_obj

  def find_match(self, matches, key_term):
    key_term = key_term.lower()
    for match in matches:
      if match['name'].lower() == key_term:
        return match
      

  def show_img_url(self, url):
    urllib.request.urlretrieve(
      url,
      "img.png")
    img = Image.open("img.png")
    img.show()

  def get_all_cards(self):
    query = {'page': 2}
    response = requests.get("http://api.fabdb.net/cards/", params=query)
    stud_obj = json.loads(response.text)
    matches = stud_obj['data']
    for match in matches:
      print(match['name'])

  def load_card(self, record):
    self.fb.create_record(record)

  def show_db(self):
    self.fb.list_all()
   

rd = Reader()
rd.read_image('MON002.png')
rd.get_card_title()
rd.search_card_api()
print('********************************')
rd.get_all_cards()

