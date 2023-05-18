import requests, logging, re, os, random
from bs4 import BeautifulSoup
from collections import deque
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


load_dotenv()


AMAZON_LINK = 'AMAZON_LINK'
ADEALSWEDEN = 'https://www.adealsweden.com/deals/'
SWEDROID_USERNAME = 'SWEDROID_USERNAME'
SWEDROID_PASSWORD = 'SWEDROID_PASSWORD'
SWEDROID_LOGIN = 'https://swedroid.se/forum/login/login'
SWEDROID = 'https://swedroid.se/forum/threads/fyndtipstraden-amazon-se-inga-diskussioner.186347/'
PROXY_USERNAME = 'PROXY_USERNAME'
PROXY_PASSWORD = 'PROXY_PASSWORD'
PROXY_HOSTS = ['se.socks.nordhold.net', 'stockholm.se.socks.nordhold.net']
HAGGLEZON = 'https://www.hagglezon.com/en/s/'

HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'})


PROXIES = {
    'http': f'socks5://{{PROXY_USERNAME}}:{{PROXY_PASSWORD}}@{{PROXY_HOST}}:1080',
    'https': f'socks5://{{PROXY_USERNAME}}:{{PROXY_PASSWORD}}@{{PROXY_HOST}}:1080'
}


options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
driver = uc.Chrome(options=options)
ip = requests.get('https://jsonip.com/')
ip = ip.json()['ip']
print(ip)
driver.get(ADEALSWEDEN)
WebDriverWait(driver, 10).until(EC.title_contains("Active Deals - Adealsweden"))
response = driver.page_source

driver.quit()
soup = response
name_pattern = r'<a\shref\=\"https\:\/\/www\.adealsweden\.com\/[\w\S]+\/\d+\/\"\starget.*>(.*)<'
price_pattern = r'\<em\>(.*)\<\/em\>\<\/strong\>(.*)\<\/p\>'
url_pattern = r'(?<!>)https://amzn\.to/[^\s"]+'
name_matches = re.findall(name_pattern, soup, re.MULTILINE)
prices_matches = re.findall(price_pattern, soup, re.MULTILINE)
url_matches = re.findall(url_pattern, soup, re.MULTILINE)
print(len(url_matches))



# data_asin_list = [div["data-asin"] for div in soup.select('.s-result-item[data-asin]')]
# asin_list = [x for x in data_asin_list if x]
# url_matches = []
# print(len(asin_list))
# print("111")
# for asin in asin_list:
#     print("test")
#     anchor_tag = soup.select_one(f'a[data-asin="{asin}"]')
#     print(anchor_tag)
#     if anchor_tag:
#         href_link = anchor_tag.get('href')
#         url_matches.append(href_link)
