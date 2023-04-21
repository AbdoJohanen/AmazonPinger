import requests, logging, re, os, random
from models import Adealsweden, Swedroid, Amazon
from bs4 import BeautifulSoup
from collections import deque


ADEALSWEDEN = 'https://www.adealsweden.com/deals/8/'
SWEDROID_LOGIN = 'https://swedroid.se/forum/login/login'
SWEDROID = 'https://swedroid.se/forum/threads/fyndtipstraden-amazon-se-inga-diskussioner.186347/'


response = requests.get(ADEALSWEDEN, timeout=5)
response_text = response.text
name_pattern = r'<a\shref\=\"https\:\/\/www\.adealsweden\.com\/[\w\S]+\/\d+\/\"\starget.*>(.*)<'
price_pattern = r'\<em\>(.*)\<\/em\>\<\/strong\>(.*)\<\/p\>'
url_pattern = r'\"(https://amzn\.to.*)\"\s'
name_matches = re.findall(name_pattern, response_text, re.MULTILINE)
prices_matches = re.findall(price_pattern, response_text, re.MULTILINE)
url_matches = re.findall(url_pattern, response_text, re.MULTILINE)

for x in prices_matches:
    print(x)
    print("\n")