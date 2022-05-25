import sys
import requests
import re
from bs4 import BeautifulSoup
from .func import *

SIZE_GUIDE = ['sizeGuide','size Guide','size guide','sizeguide','Sizeguide','Size guide','SizeGuide','Size Guide','SIZEGUIDE','SIZE GUIDE']
TAGS = ['a','div','button','h1','h2','h3','h4']
TABLE = ['table','th','td','tr']
SIZES = ['XXS','XS','S','M','L','XL','XXL','XXXL']
PARAMETERS = ['Chest', 'Waist', 'chest', 'waist', 'CHEST', 'WAIST' ]
REGEX_SIZE_RANGES = '(^([6-8][0-9]|5[0-9]|9[0-9]|1[1-5][0-9]|10[0-9]|16[0-0])$|\-.*([6-8][0-9]|5[0-9]|9[0-9]|1[1-5][0-9]|10[0-9]|16[0-0])$)'
MATCH_ALL = r'.*'

def validate_scraping(url):
  # response = requests.get(url)
  print("True")
  html_text = url.text
  doc = BeautifulSoup(html_text, "html.parser")

  try:
    size_guide = find_size_guide(doc)
    size_guide[0].text
  except AttributeError:
    return ("No size guide") # if no size guide
  except TypeError:
    return ("No size guide")
  else:
    return True # url is valid


# scrapping_size_dict = validate_url(URL)
# print(scrapping_size_dict)

def regex(string):
    """ Return a compiled regular expression that matches the given string with any prefix and postfix,
        e.g. if string = "chest", the returned regex matches r".*cheast.*" """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    reg = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(reg, flags=re.DOTALL)

def scraping(url):
  """ Return a dictionary after web scapping. each key represent the clothing size and the values are list with their range size,
        e.g. "L": [80,85]. """
  response = requests.get(url)
  html_text = response.text
  doc = BeautifulSoup(html_text, "html.parser")
  sizes = doc.find_all(TABLE, string= SIZES)
  ranges = doc.find_all(TABLE, text= re.compile(REGEX_SIZE_RANGES))
  parameter = []

  for param in PARAMETERS:
    valid_param = doc.find(TABLE, text=regex(param))
    if valid_param:
      parameter.append((valid_param.string.split())[0])

  size_list = [size.string for size in sizes]
  size_ranges = []

  for rng in ranges:
    lower, top = rng.string.split('-')
    size_ranges.append([int(lower),int(top)])

  dict_size = dict(zip(size_list, size_ranges))
  return dict_size

def find_size_guide(doc):
  """Find from all given tags in soup which contains the text Size guide.
      If no match or more than one match is found is found, return None. """
  size_guide = doc.find_all(TAGS, string=SIZE_GUIDE)
  if len(size_guide) != 1:
    return None
  return size_guide

def validate_url(url: str):
  if not url:
    return ("No URL specified")
  if url[0:4] != 'http':
    url = 'http://' + url
  try:
    response = requests.get(url)
  except requests.RequestException:
    print("True1")
    return ("Invalid URL!")
  else:
    return validate_scraping(response)
