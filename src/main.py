import pytesseract
import cv2
import matplotlib.pyplot as plt
import requests
import json
import urllib.request
from controllers.controller import FabCardController
from PIL import Image
from camera import run_camera

class Reader:
  def __init__(self):
    self.img = None
    self.text = None
    self.card_name = None
    self.fb = FabCardController()

  def process_image(self):
    img = run_camera()
    self.read_image_from_cam(img)

    # self.read_image_from_src(r'src/MON002.png')

    self.get_card_card_name()
    print(self.card_name)
    self.get_card_from_db(self.card_name)

  def read_image_from_cam(self, img):
    self.img = img

    cv2.imshow('prism', self.img)

    # cv2.waitKey(0)
    img_text = pytesseract.image_to_string(self.img)
    print(img_text)
    self.card_name = img_text
    return img_text

  def read_image_from_src(self, src):
    self.img = cv2.imread(src)

    cv2.imshow('prism', self.img)

    # cv2.waitKey(0)
    img_text = pytesseract.image_to_string(self.img);
    print(img_text)
    self.card_name = img_text
    return img_text

  def get_card_card_name(self):
    self.card_name = self.card_name.split("\n")[0]
    return self.card_name

  def log_text(self):
    if (self.card_name):
      print(self.card_name)
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
  
    for i, match in enumerate(matches):
      if i > 0: break
      print(i)
      # print(match['name'])
      self.clean_data(match)

  def get_card_from_db(self, name):
    result = self.fb.get_card_by_name(name)
    print(result)
    return result
    

rd = Reader()
# rd.read_image('MON002.png')
# rd.get_card_title()
# rd.search_card_api()
print('********************************')
rd.process_image()
# rd.get_all_cards()

