import threading
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

  def run(self):
    self.process_image()     

  def process_image(self):
    # TODO: CONSIDER storing all card_names in cache and matching on them
    img = run_camera()
    
    self.read_image_from_cam(img)

    # self.read_image_from_src(r'src/MON002.png')

    self.get_card_card_name()
    print(self.card_name)
    self.get_card_from_db(self.card_name)

  def run_local_cam(self):
    cam = cv2.VideoCapture(0)
    ret, self.img = cam.read()
    cv2.imshow("test", self.img)

  def clean_image(self):
    gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    cv2.imshow('thresh', thresh)
    cv2.waitKey()

    cv2.imshow('opening', opening)
    cv2.waitKey()
    cv2.imshow('invert', invert)
    cv2.waitKey()
    self.img = kernel

  def read_image_from_cam(self, img):
    self.img = img
    # self.clean_image()

    # cv2.imshow('prism', self.img)

    # cv2.waitKey(0)
    img_text = pytesseract.image_to_string(
        self.img, lang='eng', config='--psm 3')

    img_boxes = pytesseract.image_to_boxes(self.img)

    img_h, img_w, _ = self.img.shape

    for boxes in img_boxes.splitlines():
      boxes = boxes.split(' ')
      x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
      cv2.rectangle(self.img, (x, img_h-y), (w, img_w-h) , (0,0,255),3)

    print('The following text was found: ', img_text)
    self.card_name = img_text
    return img_text

  def read_image_from_src(self, src):
    self.img = cv2.imread(src)

    cv2.imshow('prism', self.img)

    # cv2.waitKey(0)
    img_text = pytesseract.image_to_string(self.img);

    # print(img_text)
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

  def example(self):
    font_scale = 1.5
    font = cv2.FONT_HERSHEY_PLAIN

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
      cap = cv2.VideoCapture(0)
    if not cap.isOpened():
      raise IOError("Cannot open video")
    
    counter = 0
    while True:
      ret, img = cap.read()
      counter += 1
      if ((counter % 5) == 0):
        img_h, img_w, _ = img.shape
        x1, y1, w1, h1 = 0, 0, img_h, img_w

        img_text = pytesseract.image_to_string(img)


        img_boxes = pytesseract.image_to_boxes(img)
        for boxes in img_boxes.splitlines():
          boxes = boxes.split(' ')
          x, y, w, h = int(boxes[1]), int(
              boxes[2]), int(boxes[3]), int(boxes[4])
          cv2.rectangle(img, (x, img_h-y), (w, img_h-h), (0, 0, 255), 3)

        cv2.putText(img, img_text, ( x1 + int(w1/50), y1 + int(h1/50) ) , cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.imshow('Detect', img)

        if cv2.waitKey(2) & 0xFF == ord('q'):
          break

rd = Reader()
# rd.read_image('MON002.png')
# rd.get_card_title()
# rd.search_card_api()
print('********************************')
# rd.process_image()

rd.example()


# rd.get_all_cards()

